// Single intake point for the membership page's lead forms (quote + invite).
// Phase 1 (tonight): always email the lead via Resend.
// Phase 2 (later): writeToBackend() gains a Base44 write. Nothing else changes —
// that isolation is the entire point of routing both forms through one function.

const RESEND_ENDPOINT = "https://api.resend.com/emails";
const FROM_ADDRESS = "Propwash Leads <onboarding@resend.dev>";
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

  try {
    await sendLeadEmail(type, record);
  } catch (err) {
    console.error("lead-intake: email send failed", err);
    return json(500, { ok: false, error: "Could not send notification email." });
  }

  try {
    await writeToBackend({ type, ...record });
  } catch (err) {
    // A backend failure must never block the email or the response — the
    // email already captured the lead.
    console.error("lead-intake: writeToBackend failed", err);
  }

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
    rows.push(["What interested them in Platinum", record.platinumInterest]);
  }
  return rows;
}

async function sendLeadEmail(type, record) {
  const apiKey = process.env.RESEND_API_KEY;
  const notifyEmail = process.env.LEAD_NOTIFY_EMAIL;
  if (!apiKey || !notifyEmail) {
    throw new Error("RESEND_API_KEY or LEAD_NOTIFY_EMAIL is not configured.");
  }

  const subject =
    type === "invite"
      ? `Platinum invite request — ${record.firstName} ${record.lastName} (${record.boatLength}ft)`
      : `New quote request — ${record.firstName} ${record.lastName} (${record.boatLength}ft)`;

  const rows = buildFieldRows(type, record)
    .map(([label, value]) => `<tr><td style="padding:4px 12px 4px 0;color:#667;"><strong>${esc(label)}</strong></td><td style="padding:4px 0;">${esc(value) || "—"}</td></tr>`)
    .join("");

  const html = `
    <p><strong>Phone:</strong> ${esc(record.phone)}<br>
    <strong>Email:</strong> ${esc(record.email)}</p>
    <table cellpadding="0" cellspacing="0">${rows}</table>
    <p style="color:#889;font-size:12px;">Submitted from propwashmarine.com/membership/ — ${type === "invite" ? "Platinum invite request" : "quote request"}.</p>
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

// Phase 2 hook. Routing (once implemented): type "quote" -> Base44 Lead
// entity (Leads tab); type "invite" -> Base44 MembershipRequest entity
// (Membership requests section). No-op tonight so a backend failure can
// never block the email or the response above.
async function writeToBackend(record) {
  return; // TODO Base44
}
