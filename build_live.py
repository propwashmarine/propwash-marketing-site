from pathlib import Path
import json
import re
import shutil
import subprocess


ROOT = Path(__file__).parent
TEMPLATE = ROOT / "src" / "v4-template.html"
MEDIA = Path("/Volumes/Jack's Hard Drive/Propwash/Website Media")
DERIVED = ROOT / "src" / "media-derived"
OUT = ROOT / "assets" / "v4"
DIST = ROOT / "dist"


def require_replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected source fragment was not found: {old[:120]}")
    return text.replace(old, new)


def save_image(source: Path, destination: Path, longest_side: int = 2000, quality: int = 84) -> None:
    subprocess.run(
        ["sips", "-Z", str(longest_side), "-s", "format", "jpeg", "-s", "formatOptions", str(quality), str(source), "--out", str(destination)],
        check=True,
        stdout=subprocess.DEVNULL,
    )


source = TEMPLATE.read_text()
styles = re.search(r"<style>([\s\S]*?)</style>", source).group(1)
markup_start = source.index('<div id="pw-redesign-v3">')
markup_end = source.index("<script>", markup_start)
markup = source[markup_start:markup_end].strip()
script = re.search(r"<script>([\s\S]*?)</script>", source).group(1)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "logo").mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "video").mkdir(parents=True, exist_ok=True)

if not (ROOT / "assets" / "logo" / "brandmark.png").exists():
    shutil.copy2(MEDIA / "L01.png", ROOT / "assets" / "logo" / "brandmark.png")
if not (ROOT / "assets" / "logo" / "wordmark.png").exists():
    shutil.copy2(MEDIA / "L02.png", ROOT / "assets" / "logo" / "wordmark.png")
shutil.copy2(MEDIA / "H01.mp4", ROOT / "assets" / "video" / "hero-v4.mp4")

image_sources = {
    "hero": MEDIA / "H02.jpg",
    "signature": DERIVED / "signature.png",
    "detailMain": MEDIA / "S02.jpeg",
    "detailBright": MEDIA / "S02 Brightwork.jpg",
    "detailHatch": DERIVED / "hatch.png",
    "detailInterior": MEDIA / "S02 interior.jpg",
    "detailSeats": MEDIA / "S02 Seats.jpg",
    "detailTop": DERIVED / "hardtop.png",
    "detailTower": MEDIA / "DSC04465 copy.jpg",
    "wax": MEDIA / "S03.JPG",
    "compound": MEDIA / "S04 copy.JPG",
    "ceramic": MEDIA / "S05.jpg",
    "plans": MEDIA / "New Maintenance Plan Photo.JPG",
    "memberSilver": MEDIA / "M01.jpg",
    "memberGold": DERIVED / "member-gold.png",
    "memberPlatinum": MEDIA / "M03.jpg",
    "dashboard": DERIVED / "owner-portal.png",
    "covers": MEDIA / "Covers.jpg",
    "gallery1": MEDIA / "G01.jpg",
    "gallery2": MEDIA / "G02.png",
    "gallery3": MEDIA / "G03.jpeg",
    "gallery4": DERIVED / "shiny-console.png",
    "blog1": MEDIA / "B01.jpg",
    "blog2": MEDIA / "B02.png",
    "blog3": MEDIA / "B03.JPG",
}

asset_urls = {
    "brandmark": "assets/logo/brandmark.png",
    "wordmark": "assets/logo/wordmark.png",
    "video": "assets/video/hero-v4.mp4",
    "wajerVideo": "assets/video/wajer-walkthrough.mp4",
    "reflectionVideo": "assets/video/gelcoat-reflections.mp4",
    "beadingVideo": "assets/video/water-beading.mp4",
}

for key, path in image_sources.items():
    legacy_name = "hero-poster.webp" if key == "hero" else f"{key}.webp"
    legacy = ROOT / "assets" / "v3" / legacy_name
    if key not in {"plans", "gallery4"} and legacy.exists():
        filename = legacy_name
        shutil.copy2(legacy, OUT / filename)
    else:
        filename = f"{key}.jpg"
        save_image(path, OUT / filename, 1800 if key == "plans" else 2200, 82)
    asset_urls[key] = f"assets/v4/{filename}"

markup = require_replace(
    markup,
    '<div class="pw-reviewbar"><span>MOCKUP V4 / FINAL CONTENT REVIEW</span><div class="pw-reviewactions"><button class="pw-motion" id="pw-motion" type="button" aria-pressed="true"><span>◉</span> Motion on</button><button class="pw-motion" id="pw-preview-confirmation" type="button">Preview confirmation</button></div></div>',
    '<button class="pw-motion" id="pw-motion" type="button" aria-pressed="true" hidden><span>◉</span> Motion on</button><button class="pw-motion" id="pw-preview-confirmation" type="button" hidden>Preview confirmation</button>',
)
markup = markup.replace("preload=\"auto\"", "preload=\"metadata\"")
markup = markup.replace("Captured from the current My Slip portal for this design review.", "Your real service history, visit photos and payments in one place.")
markup = markup.replace("Run hard. Look right. / V4 design concept for approval", "Run hard. Look right. / South Florida dockside detailing")
markup = markup.replace(
    '<a href="#pw-area">Stuart → Fort Lauderdale</a><a href="#pw-quote">Get a quote</a>',
    '<a href="#pw-area">Stuart → Fort Lauderdale</a><a href="https://propwash.base44.app/login" target="_blank" rel="noopener">Client login</a><a href="#pw-quote">Get a quote</a>',
)

markup = require_replace(
    markup,
    '<div class="pw-walkthroughrail"><article><video data-pw-video="wajerVideo" aria-label="Wajer boat walkthrough" muted loop playsinline preload="metadata"></video><strong>Wajer walkthrough</strong></article><article><video data-pw-video="reflectionVideo" aria-label="Gelcoat reflection close-up" muted loop playsinline preload="metadata"></video><strong>Gelcoat reflections</strong></article><article><video data-pw-video="beadingVideo" aria-label="Water beading on the protected finish" muted loop playsinline preload="metadata"></video><strong>Water beading</strong></article></div>',
    '<div class="pw-walkthroughrail" role="group" aria-label="Choose a walkthrough video"><button class="pw-walkitem is-active" type="button" data-walk="0" aria-pressed="true"><video data-pw-video="wajerVideo" aria-hidden="true" muted loop playsinline preload="metadata"></video><span class="pw-walkcaption"><strong>Wajer walkthrough</strong><small>Complete care, bow to stern.</small></span></button><button class="pw-walkitem" type="button" data-walk="1" aria-pressed="false"><video data-pw-video="reflectionVideo" aria-hidden="true" muted loop playsinline preload="metadata"></video><span class="pw-walkcaption"><strong>Gelcoat reflections</strong><small>Depth you can see at the dock.</small></span></button><button class="pw-walkitem" type="button" data-walk="2" aria-pressed="false"><video data-pw-video="beadingVideo" aria-hidden="true" muted loop playsinline preload="metadata"></video><span class="pw-walkcaption"><strong>Water beading</strong><small>Protection working on contact.</small></span></button></div>',
)

markup = require_replace(
    markup,
    '<section id="pw-area" class="pw-area pw-section pw-wrap"><div><div class="pw-kicker pw-eyebrow pw-muted">07 / Our stretch of coast</div><h2>South Florida.<br> At your Slip.</h2><p>Based in Boca Raton. Mobile detailing from Stuart to Fort Lauderdale, at your Slip, lift or driveway. Just outside that stretch? Ask us.</p></div><div><div class="pw-locationlist">',
    '<section id="pw-area" class="pw-area pw-section pw-wrap"><div><div class="pw-kicker pw-eyebrow pw-muted">07 / Our stretch of coast</div><h2>South Florida.<br> At your Slip.</h2><p>Based in Boca Raton. Mobile detailing from Stuart to Fort Lauderdale, at your Slip, lift or driveway. Just outside that stretch? Ask us.</p><div class="pw-coastroute" aria-hidden="true"><span class="pw-routetrack"><i></i></span><b style="--pw-stop:0%"></b><b style="--pw-stop:51%"></b><b style="--pw-stop:100%"></b></div></div><div><div class="pw-locationlist">',
)

markup = require_replace(
    markup,
    '</footer></div>\n<section id="pw-membership-page"',
    '</footer><nav class="pw-mobileactions" aria-label="Quick actions"><a href="tel:+19043866658">Call</a><a href="https://propwash.base44.app/login" target="_blank" rel="noopener">Client login</a><a href="#pw-quote">Get a quote</a></nav></div>\n<section id="pw-membership-page"',
)

markup = require_replace(
    markup,
    '<form id="pw-quote-form" class="pw-form">',
    '<form id="pw-quote-form" class="pw-form" name="quote-request" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data"><input type="hidden" name="form-name" value="quote-request"><label class="pw-hp" aria-hidden="true">Leave this field empty<input name="bot-field" tabindex="-1" autocomplete="off"></label>',
)
markup = require_replace(
    markup,
    '<button class="pw-cta" id="pw-preview-request" type="button">Preview request </button>',
    '<button class="pw-cta" id="pw-preview-request" type="submit">Send request</button>',
)
markup = markup.replace(
    'FORM PREVIEW / Nothing is sent or saved. Try the flow with sample details. For same-day or urgent requests, call us.',
    'Send the request and we will follow up with the right scope for your boat. For same-day or urgent work, call us.',
)
markup = markup.replace('Quote flow preview', 'Quote request').replace('This is a design preview. Nothing has been sent.', 'Your request is ready to submit.')
markup = markup.replace('MOCKUP / No request was sent', 'Propwash Marine Detailing')

markup = require_replace(
    markup,
    '<form id="pw-member-form" class="pw-memberform pw-wrap">',
    '<form id="pw-member-form" class="pw-memberform pw-wrap" name="membership-inquiry" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="membership-inquiry"><input type="hidden" id="pw-member-plan" name="membership_plan" value="Platinum"><label class="pw-hp" aria-hidden="true">Leave this field empty<input name="bot-field" tabindex="-1" autocomplete="off"></label>',
)
markup = markup.replace('Inquiry preview', 'Membership inquiry').replace('This design preview sends and stores nothing.', 'Your membership request is ready to submit.')
member_names = {
    "pw-member-length": "boat_length",
    "pw-member-make": "make_model",
    "pw-member-location": "boat_location",
    "pw-member-storage": "storage",
    "pw-member-cadence": "wash_cadence",
    "pw-member-goals": "care_goals",
    "pw-member-first": "first_name",
    "pw-member-last": "last_name",
    "pw-member-phone": "phone",
    "pw-member-email": "email",
    "pw-member-source": "referral_source",
    "pw-member-notes": "notes",
}
for field_id, field_name in member_names.items():
    markup = re.sub(rf'(id="{re.escape(field_id)}")(?![^>]*\bname=)', rf'\1 name="{field_name}"', markup)

markup = require_replace(
    markup,
    '<button class="pw-cta" id="pw-member-preview" type="button">Preview inquiry </button>',
    '<button class="pw-cta" id="pw-member-preview" type="submit">Request membership</button>',
)

script = script.replace("const assets=__PW_ASSETS__;", "const assets=" + json.dumps(asset_urls, separators=(",", ":")) + ";")
script = script.replace(
    "root.querySelectorAll('[data-pw-img]').forEach(img=>{img.src=assets[img.dataset.pwImg];});",
    "root.querySelectorAll('[data-pw-img]').forEach(img=>{img.src=assets[img.dataset.pwImg];img.decoding='async';if(!img.closest('.pw-v2hero')&&!img.closest('.pw-logo'))img.loading='lazy';});",
)

script = require_replace(
    script,
    """const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let moving=!reduced;
function syncVideo(){const toggle=byId('pw-video-toggle');toggle.setAttribute('aria-pressed',String(moving));toggle.textContent=moving?'Ⅱ Pause video':'▶ Play video';if(moving){const play=video.play();if(play)play.catch(()=>{toggle.textContent='▶ Play video';toggle.setAttribute('aria-pressed','false');});walkVideos.forEach(v=>{const p=v.play();if(p)p.catch(()=>{});});}else{video.pause();walkVideos.forEach(v=>v.pause());}}""",
    """const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let moving=!reduced,walkInView=false;
function syncWalkVideos(){walkVideos.forEach(v=>{const active=v.closest('.pw-walkitem')?.classList.contains('is-active');if(moving&&walkInView&&active){const p=v.play();if(p)p.catch(()=>{});}else v.pause();});}
function syncVideo(){const toggle=byId('pw-video-toggle');toggle.setAttribute('aria-pressed',String(moving));toggle.textContent=moving?'Ⅱ Pause video':'▶ Play video';if(moving){const play=video.play();if(play)play.catch(()=>{toggle.textContent='▶ Play video';toggle.setAttribute('aria-pressed','false');});}else video.pause();syncWalkVideos();}""",
)

script = require_replace(
    script,
    """const gallery={gallery1:['Dockside ready','Deep reflection along the waterfront'],gallery2:['Wherever you are','At the trailer, lift or Slip—we bring professional care to wherever the boat sits.'],gallery3:['Brightwork in focus','Brightwork, transom and engines brought back into focus'],gallery4:['Console clarity','A clean helm, polished stainless and a finish that catches the light.']};
root.querySelectorAll('[data-gallery]').forEach(btn=>btn.addEventListener('click',()=>{root.querySelectorAll('[data-gallery]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));const key=btn.dataset.gallery;byId('pw-gallery-feature').src=assets[key];byId('pw-gallery-feature').alt=gallery[key][0]+' from the Propwash work gallery';byId('pw-gallery-name').textContent=gallery[key][0];byId('pw-gallery-detail').textContent=gallery[key][1];animate(byId('pw-gallery-feature'));}));""",
    """const gallery={gallery1:['Dockside ready','Deep reflection along the waterfront'],gallery2:['Wherever you are','At the trailer, lift or Slip—we bring professional care to wherever the boat sits.'],gallery3:['Brightwork in focus','Brightwork, transom and engines brought back into focus'],gallery4:['Console clarity','A clean helm, polished stainless and a finish that catches the light.']};
const galleryDrift={gallery1:['1.4%','-.5%'],gallery2:['-1.1%','.6%'],gallery3:['.8%','-.8%'],gallery4:['-1.3%','-.3%']};
root.querySelectorAll('[data-gallery]').forEach(btn=>btn.addEventListener('click',()=>{root.querySelectorAll('[data-gallery]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));const key=btn.dataset.gallery,feature=byId('pw-gallery-feature');feature.src=assets[key];feature.alt=gallery[key][0]+' from the Propwash work gallery';feature.style.setProperty('--pw-drift-x',galleryDrift[key][0]);feature.style.setProperty('--pw-drift-y',galleryDrift[key][1]);feature.style.animation='none';requestAnimationFrame(()=>{feature.style.animation='';});byId('pw-gallery-name').textContent=gallery[key][0];byId('pw-gallery-detail').textContent=gallery[key][1];animate(feature);}));""",
)

enhancements = """
root.querySelectorAll('.pw-walkitem').forEach((item,index)=>item.addEventListener('click',()=>{root.querySelectorAll('.pw-walkitem').forEach((candidate,i)=>{const active=i===index;candidate.classList.toggle('is-active',active);candidate.setAttribute('aria-pressed',String(active));});walkVideos[index].currentTime=0;syncWalkVideos();}));
const walkSection=root.querySelector('.pw-walkthroughs'),areaSection=byId('pw-area');
if('IntersectionObserver' in window){new IntersectionObserver(entries=>{walkInView=entries[0]?.isIntersecting||false;syncWalkVideos();},{threshold:.25}).observe(walkSection);new IntersectionObserver(entries=>{if(entries[0]?.isIntersecting){areaSection.classList.add('pw-route-visible');}},{threshold:.3}).observe(areaSection);}else{walkInView=true;areaSection.classList.add('pw-route-visible');syncWalkVideos();}
"""
script = require_replace(script, "\n})();", "\n" + enhancements + "\n})();")

old_quote = """function completePreview(){if(![...contact.querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))return;const request=byId('pw-interest').value;byId('pw-request-summary').textContent=byId('pw-length').value+' ft boat · '+request+'. Your boat details and contact information would accompany this request.';step(3);}
byId('pw-preview-request').addEventListener('click',completePreview);
form.addEventListener('submit',e=>{e.preventDefault();if(!contact.hidden)completePreview();});"""
new_quote = """form.addEventListener('submit',e=>{if(contact.hidden){e.preventDefault();byId('pw-next').click();return;}const valid=[...contact.querySelectorAll('input,select,textarea')].every(el=>el.reportValidity());if(!valid){e.preventDefault();return;}boat.querySelectorAll('input,select').forEach(el=>el.disabled=false);const send=byId('pw-preview-request');send.disabled=true;send.firstChild.textContent='Sending ';});"""
script = require_replace(script, old_quote, new_quote)

old_member = """byId('pw-member-next').addEventListener('click',()=>{if([...byId('pw-member-step1').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(2);});byId('pw-member-prev').addEventListener('click',()=>memberStep(1));byId('pw-member-preview').addEventListener('click',()=>{if([...byId('pw-member-step2').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(3);});byId('pw-member-restart').addEventListener('click',()=>memberStep(1));byId('pw-member-form').addEventListener('submit',e=>e.preventDefault());"""
new_member = """byId('pw-member-next').addEventListener('click',()=>{if([...byId('pw-member-step1').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(2);});byId('pw-member-prev').addEventListener('click',()=>memberStep(1));byId('pw-member-restart').addEventListener('click',()=>memberStep(1));byId('pw-member-form').addEventListener('submit',e=>{if(!byId('pw-member-step1').hidden){e.preventDefault();byId('pw-member-next').click();return;}const valid=[...byId('pw-member-step2').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity());if(!valid){e.preventDefault();return;}byId('pw-member-plan').value=byId('pw-member-selected').textContent;byId('pw-member-step1').querySelectorAll('input,select,textarea').forEach(el=>el.disabled=false);const send=byId('pw-member-preview');send.disabled=true;send.firstChild.textContent='Sending ';});"""
script = require_replace(script, old_member, new_member)

live_css = """
html{scroll-behavior:smooth;background:#0A1A2F}
body{margin:0;background:#0A1A2F;overflow-x:hidden}
#pw-redesign-v3{width:100%;min-height:100vh}
#pw-redesign-v3 .pw-hp{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
#pw-redesign-v3 .pw-v2hero .pw-nav{position:relative;z-index:3}
#pw-redesign-v3 .pw-cta:disabled{opacity:.7;cursor:wait;transform:none}
#pw-redesign-v3 .pw-walkthroughrail{display:flex;gap:14px;align-items:stretch}
#pw-redesign-v3 .pw-walkitem{position:relative;flex:1 1 0;height:360px;overflow:hidden;background:#14283E;border:1px solid #38516A;color:#F4F8FC;padding:0;text-align:left;transition:flex .55s cubic-bezier(.2,.7,.2,1),border-color .3s,transform .3s;isolation:isolate}
#pw-redesign-v3 .pw-walkitem.is-active{flex:1.72 1 0;border-color:#70B8FF;transform:translateY(-4px)}
#pw-redesign-v3 .pw-walkitem:after{content:'';position:absolute;z-index:1;inset:36% 0 0;background:linear-gradient(transparent,#06111FEE);pointer-events:none}
#pw-redesign-v3 .pw-walkitem video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#071625;transform:scale(1.01);transition:filter .35s,transform .55s}
#pw-redesign-v3 .pw-walkitem:not(.is-active) video{filter:saturate(.55) brightness(.72)}
#pw-redesign-v3 .pw-walkitem:hover video{transform:scale(1.04)}
#pw-redesign-v3 .pw-walkcaption{position:absolute;z-index:2;left:18px;right:18px;bottom:17px;display:grid;gap:6px}
#pw-redesign-v3 .pw-walkcaption strong{position:static;font:500 17px/1.2 Oswald,Arial,sans-serif;text-transform:uppercase}
#pw-redesign-v3 .pw-walkcaption small{font-size:10px;line-height:1.45;color:#C6D5E3;opacity:0;transform:translateY(5px);transition:opacity .3s,transform .3s}
#pw-redesign-v3 .pw-walkitem.is-active .pw-walkcaption small{opacity:1;transform:none}
#pw-redesign-v3 .pw-metal{overflow:hidden;isolation:isolate;transform-style:preserve-3d}
#pw-redesign-v3 .pw-metal:before{pointer-events:none}
#pw-redesign-v3 .pw-metal[aria-pressed=true]{box-shadow:0 17px 46px rgba(0,0,0,.22),inset 0 1px rgba(255,255,255,.2)}
#pw-redesign-v3 .pw-coastroute{position:relative;height:46px;margin:34px 0 2px;max-width:440px}
#pw-redesign-v3 .pw-routetrack{position:absolute;left:0;right:0;top:21px;height:2px;background:#425C76;overflow:hidden}
#pw-redesign-v3 .pw-routetrack i{display:block;width:100%;height:100%;background:linear-gradient(90deg,#70B8FF,#D9EBFA);transform:scaleX(0);transform-origin:left;transition:transform 1.55s cubic-bezier(.2,.75,.2,1)}
#pw-redesign-v3 .pw-coastroute b{position:absolute;left:var(--pw-stop);top:15px;width:14px;height:14px;border:2px solid #91A8C0;background:#10243B;border-radius:50%;transform:translateX(-50%) scale(.7);transition:transform .35s .2s,background .35s}
#pw-redesign-v3 .pw-coastroute b:first-of-type{transform:translateX(0) scale(.7)}
#pw-redesign-v3 .pw-coastroute b:last-of-type{transform:translateX(-100%) scale(.7)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-routetrack i{transform:scaleX(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b{background:#70B8FF;transform:translateX(-50%) scale(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b:first-of-type{transform:translateX(0) scale(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b:last-of-type{transform:translateX(-100%) scale(1)}
#pw-redesign-v3 .pw-gallerymain img{--pw-drift-x:1.2%;--pw-drift-y:-.5%;animation:pw-finish-drift 13s ease-in-out infinite alternate;transform-origin:center}
#pw-redesign-v3 .pw-gallerymain:hover img{animation-duration:7s}
@keyframes pw-finish-drift{from{transform:scale(1.035) translate(0,0)}to{transform:scale(1.075) translate(var(--pw-drift-x),var(--pw-drift-y))}}
#pw-redesign-v3 .pw-mobileactions{display:none}
#pw-redesign-v3.pw-still .pw-routetrack i{transition:none;transform:scaleX(1)}
#pw-redesign-v3.pw-still .pw-coastroute b{transition:none;background:#70B8FF}
#pw-redesign-v3.pw-still .pw-gallerymain img{animation:none;transform:scale(1.035)}
@container(max-width:700px){
 #pw-redesign-v3 #pw-home-view{padding-bottom:62px}
 #pw-redesign-v3 .pw-mobileactions{position:fixed;z-index:50;display:grid;grid-template-columns:.72fr 1fr 1.2fr;left:0;right:0;bottom:0;min-height:58px;background:#081728F5;border-top:1px solid #4A6077;box-shadow:0 -12px 30px rgba(1,9,18,.3);backdrop-filter:blur(13px)}
 #pw-redesign-v3 .pw-mobileactions a{display:grid;place-items:center;min-height:58px;padding:8px 6px;border-right:1px solid #344A61;color:#E9F2FA;font-size:10px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;text-align:center}
 #pw-redesign-v3 .pw-mobileactions a:last-child{border-right:0;background:#2F91E8;color:#07192D}
}
@container(max-width:600px){
 #pw-redesign-v3 .pw-walkthroughrail{display:grid;grid-template-columns:1fr 1fr;gap:9px}
 #pw-redesign-v3 .pw-walkitem{height:225px;min-width:0}
 #pw-redesign-v3 .pw-walkitem.is-active{grid-column:1/-1;height:420px;transform:none}
 #pw-redesign-v3 .pw-walkcaption{left:12px;right:12px;bottom:13px}
 #pw-redesign-v3 .pw-walkcaption strong{font-size:13px}
}
@media(prefers-reduced-motion:reduce){#pw-redesign-v3 .pw-routetrack i,#pw-redesign-v3 .pw-coastroute b{transition:none}#pw-redesign-v3 .pw-gallerymain img{animation:none!important}#pw-redesign-v3 .pw-walkitem{transition:none}}
"""

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Do I need to be there?", "acceptedAnswer": {"@type": "Answer", "text": "No. Give us access and we handle it. Photos land in your Owner Portal after the visit."}},
        {"@type": "Question", "name": "How long does a Full Detail take?", "acceptedAnswer": {"@type": "Answer", "text": "Timing depends on length, condition and the work needed. We confirm the schedule when we quote the boat."}},
        {"@type": "Question", "name": "Wax or ceramic?", "acceptedAnswer": {"@type": "Answer", "text": "The right choice depends on the boat's finish, use and maintenance plan. Surface preparation comes first."}},
        {"@type": "Question", "name": "How often should we schedule a wash?", "acceptedAnswer": {"@type": "Answer", "text": "We match the cadence to how the boat is stored and used. Silver offers weekly, bi-weekly or monthly washes. Gold and Platinum offer a custom cadence."}},
    ],
}

business_schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": "https://propwashmarine.com/#business",
    "name": "Propwash Marine Detailing",
    "description": "Mobile and dockside boat detailing across South Florida.",
    "url": "https://propwashmarine.com/",
    "telephone": "+1-904-386-6658",
    "image": "https://propwashmarine.com/assets/v4/hero-poster.webp",
    "areaServed": ["Stuart", "Boca Raton", "Fort Lauderdale"],
    "sameAs": ["https://instagram.com/propwashmarine"],
}

document = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>South Florida Mobile Boat Detailing | Propwash Marine</title>
<meta name="description" content="Dockside boat detailing from Stuart to Fort Lauderdale. Signature washes, Full Details, correction, wax, ceramic coating and recurring maintenance plans.">
<link rel="canonical" href="https://propwashmarine.com/">
<link rel="icon" href="assets/logo/favicon.png" type="image/png">
<meta name="theme-color" content="#0A1A2F">
<meta property="og:type" content="website">
<meta property="og:title" content="South Florida Mobile Boat Detailing | Propwash Marine">
<meta property="og:description" content="Salt never sleeps. Neither do we. Dockside boat detailing from Stuart to Fort Lauderdale.">
<meta property="og:image" content="https://propwashmarine.com/assets/v4/hero-poster.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{styles}{live_css}</style>
<script type="application/ld+json">{json.dumps(business_schema, separators=(",", ":"))}</script>
<script type="application/ld+json">{json.dumps(faq_schema, separators=(",", ":"))}</script>
</head>
<body>
{markup}
<script>{script}</script>
</body>
</html>
'''

(ROOT / "index.html").write_text(document)
if DIST.exists():
    shutil.rmtree(DIST)
(DIST / "assets" / "logo").mkdir(parents=True)
(DIST / "assets" / "video").mkdir(parents=True)
shutil.copytree(OUT, DIST / "assets" / "v4")
for filename in ("brandmark.png", "wordmark.png", "favicon.png"):
    shutil.copy2(ROOT / "assets" / "logo" / filename, DIST / "assets" / "logo" / filename)
for filename in ("hero-v4.mp4", "wajer-walkthrough.mp4", "gelcoat-reflections.mp4", "water-beading.mp4"):
    shutil.copy2(ROOT / "assets" / "video" / filename, DIST / "assets" / "video" / filename)
for filename in ("index.html", "thank-you.html", "robots.txt", "sitemap.xml"):
    shutil.copy2(ROOT / filename, DIST / filename)
print(f"Built {ROOT / 'index.html'} ({len(document.encode()):,} bytes)")
print(f"Created {len(image_sources)} optimized production images and four full videos")
print(f"Prepared deployable folder at {DIST}")
