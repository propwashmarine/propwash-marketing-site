// Single intake point for the site's lead forms: quote requests (/membership/
// and homepage) and membership inquiries (/membership/ Platinum invite and the
// homepage Silver/Gold/Platinum form).
// The Base44 portal is the system of record: writeToBackend() runs first and
// decides the visitor's result. The Resend admin email is a best-effort
// notification after it — an email failure is logged, never shown to the
// visitor and never blocks the lead.

const RESEND_ENDPOINT = "https://api.resend.com/emails";
// Must be on a Resend-verified domain (propwashmarine.com). Not a real inbox;
// replies go to the customer via reply_to.
const FROM_ADDRESS = "Propwash Leads <leads@propwashmarine.com>";
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const REQUIRED_FIELDS = ["boatLength", "boatLocation", "firstName", "lastName", "phone", "email"];

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return json(405, { ok: false, error: "Method Not Allowed" });
  }

  let record;
  try {
    record = JSON.parse(event.body || "{}");
  } catch (err) {
    return json(400, { ok: false, error: "Invalid request body." });
  }

  // Honeypot: bots fill hidden fields. Pretend success, write nothing.
  if (typeof record.company === "string" && record.company.trim() !== "") {
    return json(200, { ok: true });
  }

  const type = record.type === "invite" ? "invite" : record.type === "quote" ? "quote" : null;
  if (!type) {
    return json(400, { ok: false, error: "Missing or invalid request type." });
  }

  const missing = REQUIRED_FIELDS.filter((field) => !isNonEmpty(record[field]));
  if (missing.length) {
    return json(400, { ok: false, error: `Missing required field(s): ${missing.join(", ")}.` });
  }
  if (!EMAIL_RE.test(String(record.email).trim())) {
    return json(400, { ok: false, error: "Please provide a valid email address." });
  }

  let saved = true;
  try {
    await writeToBackend({ type, ...record });
  } catch (err) {
    saved = false;
    console.error(`lead-intake: BASE44 WRITE FAILED (${type}) — lead NOT saved to portal: ${err.message}`);
  }

  // Still email when the Base44 write failed: the email is then the only
  // copy of the lead.
  try {
    await sendLeadEmail(type, record);
  } catch (err) {
    console.error(`lead-intake: EMAIL SEND FAILED (${type}) — ${saved ? "lead is saved in Base44" : "lead was NOT saved anywhere"}: ${err.message}`);
  }

  if (!saved) return json(500, { ok: false, error: "Could not save your request." });
  return json(200, { ok: true });
};

function isNonEmpty(value) {
  return typeof value === "string" && value.trim() !== "";
}

function json(statusCode, body) {
  return {
    statusCode,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

function esc(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

const TIERS = ["Silver", "Gold", "Platinum"];

// Tier for an "invite": the homepage form sends membershipPlan; the
// /membership/ form only sends invites for Platinum.
function tierOf(record) {
  const plan = clean(record.membershipPlan);
  return TIERS.find((t) => t.toLowerCase() === plan.toLowerCase()) || "Platinum";
}

function pageOf(record) {
  return record.formSource === "home" ? "propwashmarine.com (homepage)" : "propwashmarine.com/membership/";
}

function buildFieldRows(type, record) {
  const rows = [
    ["First name", record.firstName],
    ["Last name", record.lastName],
    ["Phone", record.phone],
    ["Email", record.email],
    ["Boat length (ft)", record.boatLength],
    ["Make / model", record.makeModel],
    ["Where the boat sits", record.boatLocation],
  ];
  if (type === "quote") {
    rows.push(
      ["Service interest", record.serviceInterest],
      ["How they heard about us", record.referralSource],
      ["Notes", record.notes]
    );
  } else {
    rows.push(
      ["Membership tier", tierOf(record)],
      ["What interested them in Platinum", record.platinumInterest],
      ["Storage", record.storage],
      ["Preferred wash cadence", record.washCadence],
      ["What they want handled", record.careGoals],
      ["How they heard about us", record.referralSource],
      ["Notes", record.notes]
    );
  }
  return rows;
}

async function sendLeadEmail(type, record) {
  const apiKey = process.env.RESEND_API_KEY;
  // LEAD_NOTIFY_EMAIL may list several recipients, comma-separated.
  const notifyEmail = (process.env.LEAD_NOTIFY_EMAIL || "").split(",").map((e) => e.trim()).filter(Boolean);
  if (!apiKey || !notifyEmail.length) {
    throw new Error("RESEND_API_KEY or LEAD_NOTIFY_EMAIL is not configured.");
  }

  const subject =
    type === "invite"
      ? `[Propwash Lead] ${tierOf(record) === "Platinum" ? "Platinum invite" : `${tierOf(record)} membership inquiry`} — ${record.firstName} ${record.lastName} (${record.boatLength}ft)`
      : `[Propwash Lead] Quote request — ${record.firstName} ${record.lastName} (${record.boatLength}ft)`;

  const rows = buildFieldRows(type, record)
    .map(([label, value]) => `<tr><td style="padding:4px 12px 4px 0;color:#667;"><strong>${esc(label)}</strong></td><td style="padding:4px 0;">${esc(value) || "—"}</td></tr>`)
    .join("");

  const html = `
    <p><strong>Phone:</strong> ${esc(record.phone)}<br>
    <strong>Email:</strong> ${esc(record.email)}</p>
    <table cellpadding="0" cellspacing="0">${rows}</table>
    <p style="color:#889;font-size:12px;">Submitted from ${esc(pageOf(record))} — ${type === "invite" ? `${tierOf(record)} membership request` : "quote request"}.${record.photoAttached ? " A boat photo was attached — see the Netlify Forms submission." : ""}</p>
  `;

  const res = await fetch(RESEND_ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM_ADDRESS,
      to: notifyEmail,
      reply_to: record.email,
      subject,
      html,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Resend API error ${res.status}: ${text}`);
  }
}

// Write the lead into the Base44 portal. type "quote" -> Lead (Leads tab,
// stage "New"); type "invite" -> MembershipRequest for its tier (Membership
// Requests, "New Request"). Throws on failure; the handler decides the response.
const BASE44_LEAD_URL = "https://propwash.base44.app/functions/createLead";
const BASE44_MEMBERSHIP_URL = "https://propwash.base44.app/functions/createMembershipRequest";
const BASE44_TIMEOUT_MS = 8000; // stay inside Netlify's 10s function limit

// Referral options on the form that the Lead.source enum spells differently.
const LEAD_SOURCE_ALIASES = { Nextdoor: "Next Door" };

async function writeToBackend(record) {
  const apiKey = (process.env.BASE44_API_KEY || "").trim();
  if (!apiKey) throw new Error("BASE44_API_KEY is not configured.");
  const authHeader = process.env.BASE44_AUTH_HEADER || "Authorization";
  const authPrefix = process.env.BASE44_AUTH_PREFIX ?? "Bearer";

  const [url, body] = record.type === "invite"
    ? [BASE44_MEMBERSHIP_URL, toMembershipRequest(record)]
    : [BASE44_LEAD_URL, toLead(record)];

  const res = await fetch(url, {
    method: "POST",
    headers: {
      [authHeader]: authPrefix ? `${authPrefix} ${apiKey}` : apiKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(BASE44_TIMEOUT_MS),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Base44 ${record.type} write failed ${res.status}: ${text.slice(0, 300)}`);
  }
  const created = await res.json().catch(() => ({}));
  console.log(`lead-intake: Base44 ${record.type} created ${created.id || "(no id)"}`);
}

function clean(value) {
  return typeof value === "string" ? value.trim() : value == null ? "" : String(value);
}

// Free-text extras the Base44 record has no dedicated field for.
function extraNotes(pairs) {
  return pairs.filter(([, v]) => clean(v)).map(([label, v]) => `${label}: ${clean(v)}`).join("\n");
}

function toLead(r) {
  const referral = clean(r.referralSource);
  return {
    first_name: clean(r.firstName),
    last_name: clean(r.lastName),
    phone: clean(r.phone),
    email: clean(r.email),
    length_ft: clean(r.boatLength),
    maker: clean(r.makeModel),
    location: clean(r.boatLocation),
    service: clean(r.serviceInterest),
    source: LEAD_SOURCE_ALIASES[referral] || referral || "Website",
    notes: [
      clean(r.notes),
      extraNotes([
        ["Heard about us", referral],
        ["Boat photo", r.photoAttached ? "attached — see the Netlify Forms submission" : ""],
      ]),
    ].filter(Boolean).join("\n\n"),
  };
}

function toMembershipRequest(r) {
  return {
    customer_name: `${clean(r.firstName)} ${clean(r.lastName)}`.trim(),
    customer_email: clean(r.email),
    phone: clean(r.phone),
    requested_tier: tierOf(r),
    boat_length: clean(r.boatLength),
    maker: clean(r.makeModel),
    source: "Website",
    notes: [
      clean(r.platinumInterest),
      clean(r.careGoals),
      extraNotes([
        ["Boat location", r.boatLocation],
        ["Storage", r.storage],
        ["Preferred wash cadence", r.washCadence],
        ["Heard about us", r.referralSource],
        ["Notes", r.notes],
      ]),
    ].filter(Boolean).join("\n\n"),
  };
}
