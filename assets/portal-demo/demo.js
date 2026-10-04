/* Owner Portal interactive demo. Host page provides #pd-phone (src/components/portal-demo.html) and,
   optionally, #pd-now-h / #pd-now-p (caption), #pd-explore (mobile full-screen button). */
(()=>{
const phone=document.getElementById('pd-phone'); if(!phone) return;
const $=s=>phone.querySelector(s), $$=s=>[...phone.querySelectorAll(s)];
const BASE='/assets/portal/', W=1206;                // all coordinates below are in 1206px image space
const IV=(document.currentScript&&new URL(document.currentScript.src).search)||''; // reuse demo.js ?v= so edited images aren't served stale
const u=px=>(px/W*100).toFixed(3)+'cqw';
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const ss={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}};

const SCREENS={
 'my-slip':{tab:'my-slip',h:'My Slip',p:"Your boat's status, next visit and protection at a glance.",hgt:2536,
   alt:"My Slip screen: a welcome-back greeting, the Salty Dog boat card (43 ft Mag Bay, Boca Raton, service scheduled), notifications, a protection status ring counting down to the next visit, the next scheduled Signature Wash, a Report a Spot card, latest photos, the service log and a paid-up balance.",
   hot:[{x:36,y:2721,w:1134,h:235,label:'Report a Spot',act:()=>openSpot()}]},
 'on-water':{tab:'on-water',h:'On the Water',p:'Know the conditions before you leave the dock.',hgt:4300,
   alt:"On the Water screen for Boca Raton: a weather alert, current conditions with wind, seas, water temperature and chance of rain, boating day scores for the week (scroll sideways), a day forecast, hour-by-hour forecast, tide table, sunrise, sunset and moon, peak bite windows, and a Book a wash prompt.",
   scores:{x:39,y:2040,w:1127,h:366,full:1841,snaps:[246,246,222,1127]}},
 'photos':{tab:'photos',h:'Every visit, documented.',p:'See the photos from each visit, kept with the boat.',hgt:1494,
   alt:"Vessel Photos screen: a two-column grid of photos of the boat from service visits, including the helm, seating, outboard engines and the Mag Bay transom."},
 'book-a-service':{tab:'svc',h:'Book a service',p:'Pick a day and request the time that works for you.',hgt:3094,
   alt:"Book a Service screen on the Signature Wash tab: a description of the Signature Wash, an October calendar with available days, the selected date with location and cover preference, a Request a Signature Wash button and a list of upcoming confirmed visits.",
   hot:[{x:597,y:317,w:558,h:131,label:'Request a quote tab',act:()=>show('book-a-service-quote')}]},
 'book-a-service-quote':{tab:'svc',h:'Need more than a wash?',p:'Choose the services you want and we will put a quote together.',hgt:2398,
   alt:"Book a Service screen on the Request a Quote tab: one-time services, detailing and correction, ceramic coating and teak options to choose from, a notes field and a Submit request button.",
   hot:[{x:51,y:321,w:546,h:131,label:'Signature Wash tab',act:()=>show('book-a-service')}]},
 'membership':{tab:'svc',h:'Your plan',p:'Your membership and everything it covers.',hgt:4479,
   alt:"Membership screen headed Choose your level, we'll handle the rest: the active Platinum membership with a Change Plan option, the Gold and Silver plans with what each includes and custom pricing billed monthly, and the full list of what Platinum includes with the contract dates."},
 'services':{tab:'svc',h:'The Full Service Menu',p:'Browse every service and request a quote in a tap.',hgt:10827,
   alt:"Services screen: the full service menu grouped into one-time services, detailing and correction, ceramic coating and teak, with a description of each service."},
 'payments':{tab:'act',h:'Invoices & payments',p:'View and pay invoices right in the portal, with every receipt kept on file.',hgt:2249,
   alt:"Invoice screen for invoice PWM-1234, marked paid: the Propwash Marine Detailing header, bill to Jack at jack@propwashmarine.com, vessel Salty Dog, a Signature Wash line item with the rate, subtotal and grand total shown as Custom, paid Oct 2, 2026, and a Download PDF button."},
 'messages':{tab:'act',h:'Talk to your detailer.',p:'Message us directly and catch our latest news.',hgt:1133,scrollTo:690,
   alt:"News and Messages screen on the Messages tab: a conversation with Jack, your detailer, on Wednesday, September 16 between 2:14 and 2:40 PM about a Sunday washdown, covers and a new gate code, with a message field below.",
   hot:[{x:36,y:490,w:567,h:142,label:'Announcements tab',act:()=>show('announcements')}]},
 'announcements':{tab:'act',h:'News from the crew.',p:'Updates on the weather, the season and what is new in your portal.',hgt:1182,
   alt:"News and Messages screen on the Announcements tab: On the Water is live (Oct 2, 2026), Heading back down this season? (Sep 22, 2026) and After the storm (Aug 18, 2026).",
   hot:[{x:603,y:490,w:555,h:142,label:'Messages tab',act:()=>show('messages')}]},
};
const EXTRA={assistant:{h:'Answers on hand.',p:'Ask about your boat, your plan or your schedule, any time.'},
  spot:{h:'See a spot? Send it to us.',p:"Tell us where it is, add a photo and we'll take care of it. Included with Platinum."}};

// ---------- build screens ----------
const views=$('#pd-views'); let current='my-slip';
function lazyImg(src,w,h,alt){const i=new Image();i.width=w;i.height=h;i.alt=alt||'';i.decoding='async';i.dataset.src=src+IV;return i;}
for(const [id,s] of Object.entries(SCREENS)){
  const v=document.createElement('div'); v.className='pd-view'; v.id='pd-view-'+id; v.tabIndex=0;
  v.setAttribute('aria-label',s.h+' screen');
  const page=document.createElement('div'); page.className='pd-page';
  const img=lazyImg(BASE+'portal-'+id+'.webp',600,s.hgt,s.alt);
  img.addEventListener('load',()=>v.classList.add('ready'),{once:true});
  page.appendChild(img);
  (s.hot||[]).forEach(h=>{const b=document.createElement('button');b.type='button';b.className='pd-hot';b.setAttribute('aria-label',h.label);
    Object.assign(b.style,{left:u(h.x),top:u(h.y),width:u(h.w),height:u(h.h)});b.addEventListener('click',e=>{e.stopPropagation();h.act();});page.appendChild(b);});
  if(s.scores){const c=s.scores, sc=document.createElement('div');sc.className='pd-scores';sc.setAttribute('role','group');sc.setAttribute('aria-label','Boating day scores, Friday to Thursday, scroll sideways');sc.tabIndex=0;
    Object.assign(sc.style,{left:u(c.x),top:u(c.y),width:u(c.w),height:u(c.h)});
    const t=document.createElement('div');t.className='pd-track';t.style.width=u(c.full);t.dataset.bg=BASE+'portal-on-water-scores.webp'+IV;
    c.snaps.forEach(wd=>{const sp=document.createElement('span');sp.style.width=u(wd);t.appendChild(sp);});
    sc.appendChild(t);page.appendChild(sc);}
  const sk=document.createElement('div');sk.className='pd-skel';sk.setAttribute('aria-hidden','true');sk.innerHTML='<i></i><i></i><i></i><i></i><i></i>';
  v.append(page,sk); views.appendChild(v);
}
function load(v){const i=v.querySelector('.pd-page>img');if(i&&!i.src)i.src=i.dataset.src;const t=v.querySelector('.pd-track');if(t&&!t.style.backgroundImage)t.style.backgroundImage=`url(${t.dataset.bg})`;}

// ---------- caption ----------
const capH=document.getElementById('pd-now-h'), capP=document.getElementById('pd-now-p'), cap=capH&&capH.closest('.pd-now');
let capT=0;
function setCopy(c){ if(!capH) return; const apply=()=>{capH.textContent=c.h;capP.textContent=c.p;};
  clearTimeout(capT); if(reduced||!cap){apply();return;} cap.classList.add('swap'); capT=setTimeout(()=>{apply();cap.classList.remove('swap');},160);}
function activeCopy(){ return assistOpen?EXTRA.assistant: spotOpen?EXTRA.spot: SCREENS[current]; }

// ---------- navigation ----------
function show(id){
  const s=SCREENS[id]; if(!s) return;
  const v=phone.querySelector('#pd-view-'+id); load(v);
  if(id!==current) phone.querySelector('#pd-view-'+current).classList.remove('on');
  v.classList.add('on'); current=id;
  const top=s.scrollTo?s.scrollTo/W*v.clientWidth:0;
  requestAnimationFrame(()=>{v.scrollTop=top;});
  $$('.pd-tab').forEach(t=>{const own=t.dataset.screen===id||(t.dataset.pop==='pd-pop-svc'&&s.tab==='svc')||(t.dataset.pop==='pd-pop-act'&&s.tab==='act');
    if(t.dataset.screen){own?t.setAttribute('aria-current','page'):t.removeAttribute('aria-current');} t.classList.toggle('lit',own&&!!t.dataset.pop);});
  setCopy(activeCopy());
}

// ---------- menus and dropdowns ----------
let openPop=null, opener=null;
function closePop(focus){ if(!openPop) return; openPop.classList.remove('open'); if(opener){opener.setAttribute('aria-expanded','false'); if(focus) opener.focus({preventScroll:true});} openPop=null; opener=null; }
function togglePop(btn){ const pop=phone.querySelector('#'+btn.dataset.pop);
  if(openPop===pop){closePop(false);return;} closePop(false); closeAssist(false);
  pop.classList.add('open'); btn.setAttribute('aria-expanded','true'); openPop=pop; opener=btn;
  const f=pop.querySelector('[role="menuitem"]'); if(f&&btn.getAttribute('aria-haspopup')==='menu') f.focus({preventScroll:true}); }
$$('[data-pop]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();togglePop(b);}));
$$('.pd-tab[data-screen]').forEach(b=>b.addEventListener('click',()=>{closePop(false);closeAssist(false);closeSpot(false);show(b.dataset.screen);}));
$$('.pd-pop [data-screen]').forEach(b=>b.addEventListener('click',()=>{const t=opener;closePop(false);closeSpot(false);show(b.dataset.screen);if(t)t.focus({preventScroll:true});}));
$$('.pd-pop [aria-disabled="true"]').forEach(b=>b.addEventListener('click',()=>closePop(true)));
$$('.pd-pop').forEach(p=>p.addEventListener('click',e=>e.stopPropagation()));
document.addEventListener('click',()=>{closePop(false); if(spotOpen) closeSpot(false);});
$$('[role="menu"]').forEach(m=>m.addEventListener('keydown',e=>{const it=[...m.querySelectorAll('[role="menuitem"]')],i=it.indexOf(document.activeElement);
  if(e.key==='ArrowDown'){e.preventDefault();it[(i+1)%it.length].focus();} if(e.key==='ArrowUp'){e.preventDefault();it[(i-1+it.length)%it.length].focus();}}));

// ---------- assistant ----------
const fab=$('.pd-fab'), sheet=$('#pd-sheet'), scrim=$('.pd-scrim'), note=$('.pd-note'), bubble=$('.pd-bubble');
let assistOpen=false;
function openAssist(){ closePop(false); closeSpot(false); hideBubble(); fab.classList.remove('unread'); const i=sheet.querySelector('img'); if(!i.src){i.src=i.dataset.src;sheet.classList.add('loaded');}
  assistOpen=true; phone.classList.add('assist-open'); sheet.classList.add('open'); scrim.classList.add('open'); fab.setAttribute('aria-expanded','true'); setCopy(EXTRA.assistant); sheet.querySelector('.x').focus({preventScroll:true}); }
function closeAssist(focus){ if(!assistOpen) return; assistOpen=false; resetChat(); phone.classList.remove('assist-open'); sheet.classList.remove('open'); scrim.classList.remove('open'); note.classList.remove('show');
  fab.setAttribute('aria-expanded','false'); setCopy(activeCopy()); if(focus) fab.focus({preventScroll:true}); }
fab.addEventListener('click',e=>{e.stopPropagation(); assistOpen?closeAssist(true):openAssist();});
sheet.querySelector('.x').addEventListener('click',e=>{e.stopPropagation();closeAssist(true);});
let noteT=0; sheet.querySelector('.ask').addEventListener('click',e=>{e.stopPropagation();note.classList.add('show');clearTimeout(noteT);noteT=setTimeout(()=>note.classList.remove('show'),1800);});
sheet.addEventListener('click',e=>e.stopPropagation());

// Suggested questions: question bubble, ~1s typing indicator (skipped with reduced motion), then the answer.
// Every open starts fresh, like the portal. The text input stays inert.
const chat=sheet.querySelector('.pd-chat'), qs=[...chat.querySelectorAll('.pd-q')];
let replyT=0, replying=false;
function chatMsg(who,text){ const m=document.createElement('div'); m.className='pd-msg pd-turn'+(who==='user'?' user':'');
  if(who!=='user'){ const a=document.createElement('span'); a.className='pd-av'; a.setAttribute('aria-hidden','true'); m.append(a); }
  const b=document.createElement('p'); b.className='pd-b';
  if(text==null){ b.innerHTML='<span class="pd-typing" role="status" aria-label="Assistant is replying"><i></i><i></i><i></i></span>'; } else b.textContent=text;
  m.append(b); chat.append(m); return m; }
function setReplying(on){ replying=on; qs.forEach(q=>q.setAttribute('aria-disabled',String(on))); }
// Keep the newest message in view; if a question and its answer don't both fit, keep the question's top visible.
function keepInView(first){ const max=chat.scrollHeight-chat.clientHeight, pad=parseFloat(getComputedStyle(chat).paddingTop)||0;
  chat.scrollTo({top:Math.max(0,Math.min(max,first.offsetTop-pad)),behavior:reduced?'auto':'smooth'}); }
function resetChat(){ clearTimeout(replyT); setReplying(false); chat.querySelectorAll('.pd-turn').forEach(n=>n.remove()); chat.scrollTop=0; }
qs.forEach(q=>q.addEventListener('click',e=>{ e.stopPropagation(); if(replying) return;
  const asked=chatMsg('user',q.textContent), answer=q.dataset.a;
  if(reduced){ chatMsg('bot',answer); keepInView(asked); return; }
  setReplying(true); const typing=chatMsg('bot',null); keepInView(asked);
  replyT=setTimeout(()=>{ typing.remove(); chatMsg('bot',answer); setReplying(false); keepInView(asked); },1000); }));
scrim.addEventListener('click',e=>{e.stopPropagation(); if(assistOpen) closeAssist(true); else closeSpot(true);});

// greeting bubble: once per visit, ~1s after the demo is ~50% in view
let bubbleT=0;
function hideBubble(){ bubble.classList.remove('show'); clearTimeout(bubbleT); }
function showBubble(){ if(assistOpen) return; bubble.classList.add('show'); fab.classList.add('unread'); ss.set('pdGreeted','1'); bubbleT=setTimeout(hideBubble,8000); }
bubble.querySelector('.msg').addEventListener('click',e=>{e.stopPropagation();openAssist();});
bubble.querySelector('.x').addEventListener('click',e=>{e.stopPropagation();hideBubble();});
if(!ss.get('pdGreeted') && 'IntersectionObserver' in window){
  let armed=0; const io=new IntersectionObserver(es=>{es.forEach(en=>{ if(en.intersectionRatio>=.5&&!armed){armed=setTimeout(()=>{io.disconnect();showBubble();},1000);} else if(en.intersectionRatio<.5&&armed){clearTimeout(armed);armed=0;} });},{threshold:[0,.5,1]});
  io.observe($('.pd-screen'));
}

// ---------- Report a Spot ----------
const spot=$('#pd-spot'); let spotOpen=false, spotBuilt=false, hinted=!!ss.get('pdPinHint');
const HULL=[[300,705],[480,700],[480,592],[665,590],[665,690],[1015,676],[1000,703],[970,732],[940,761],[910,783],[880,796],[300,797]];
const PIN0={x:780,y:712};
function inside(p){let c=false;for(let i=0,j=HULL.length-1;i<HULL.length;j=i++){const [xi,yi]=HULL[i],[xj,yj]=HULL[j];if(((yi>p.y)!==(yj>p.y))&&(p.x<(xj-xi)*(p.y-yi)/(yj-yi)+xi))c=!c;}return c;}
function clampHull(p){ if(inside(p)) return p; let best=null;
  for(let i=0,j=HULL.length-1;i<HULL.length;j=i++){const [ax,ay]=HULL[j],[bx,by]=HULL[i];const dx=bx-ax,dy=by-ay;let t=((p.x-ax)*dx+(p.y-ay)*dy)/(dx*dx+dy*dy);t=Math.max(0,Math.min(1,t));
    const q={x:ax+t*dx,y:ay+t*dy},d=(q.x-p.x)**2+(q.y-p.y)**2; if(!best||d<best.d)best={...q,d};} return {x:best.x,y:best.y}; }
function buildSpot(){
  spotBuilt=true;
  const page=document.createElement('div'); page.className='pd-page';
  const img=lazyImg(BASE+'portal-report-a-spot.webp',600,1617,"Report a Spot panel, Flag it, we'll handle it, on Salty Dog: an outline of the boat to drop a pin on, a reminder to call for anything urgent, request or question, area, side, title, details, add photos and a Report Spot button.");
  img.src=img.dataset.src; page.appendChild(img);
  const badge=document.createElement('span'); badge.className='pd-badge'; badge.textContent='Platinum'; Object.assign(badge.style,{left:u(440),top:u(64)}); page.appendChild(badge);
  const x=document.createElement('button'); x.type='button'; x.className='pd-hot'; x.setAttribute('aria-label','Close Report a Spot'); Object.assign(x.style,{left:u(1080),top:u(24),width:u(100),height:u(100)}); x.addEventListener('click',e=>{e.stopPropagation();closeSpot(true);}); page.appendChild(x);
  const pin=document.createElement('button'); pin.type='button'; pin.className='pd-pin'; pin.setAttribute('aria-label','Pin on the boat. Drag to move, or use the arrow keys.');
  pin.innerHTML='<svg viewBox="0 0 36 46" aria-hidden="true"><path d="M18 44c-1.2 0-16-14.4-16-26.5C2 8.4 9.2 2 18 2s16 6.4 16 15.5C34 29.6 19.2 44 18 44Z" fill="#F5A623" stroke="#fff" stroke-width="3"/><circle cx="18" cy="17" r="6" fill="none" stroke="#fff" stroke-width="3"/></svg>';
  const hint=document.createElement('span'); hint.className='pd-hint'; hint.textContent='Drag me';
  let p={...PIN0};
  const place=()=>{pin.style.left=u(p.x);pin.style.top=u(p.y);hint.style.left=u(p.x);hint.style.top=u(p.y);};
  place(); page.append(pin,hint);
  const toImg=e=>{const r=page.getBoundingClientRect();return {x:(e.clientX-r.left)/r.width*W,y:(e.clientY-r.top)/r.width*W};};
  let dragging=false, grab={x:0,y:0};
  pin.addEventListener('pointerdown',e=>{dragging=true;pin.setPointerCapture(e.pointerId);const q=toImg(e);grab={x:p.x-q.x,y:p.y-q.y};hint.classList.remove('show');hinted=true;ss.set('pdPinHint','1');e.preventDefault();});
  pin.addEventListener('pointermove',e=>{if(!dragging)return;const q=toImg(e);p=clampHull({x:q.x+grab.x,y:q.y+grab.y});place();});
  const end=()=>{dragging=false;}; pin.addEventListener('pointerup',end); pin.addEventListener('pointercancel',end);
  pin.addEventListener('keydown',e=>{const k={ArrowLeft:[-12,0],ArrowRight:[12,0],ArrowUp:[0,-12],ArrowDown:[0,12]}[e.key];if(!k)return;e.preventDefault();p=clampHull({x:p.x+k[0],y:p.y+k[1]});place();});
  const sent=document.createElement('div'); sent.className='pd-sent'; sent.setAttribute('role','status'); sent.setAttribute('aria-live','polite'); sent.style.top=u(2930);
  const send=document.createElement('button'); send.type='button'; send.className='pd-hot'; send.setAttribute('aria-label','Report Spot (demo, nothing is sent)'); Object.assign(send.style,{left:u(60),top:u(3060),width:u(1086),height:u(96)});
  let sentT=0; send.addEventListener('click',e=>{e.stopPropagation();sent.textContent="Sent to the crew. We'll take care of it.";sent.classList.add('show');clearTimeout(sentT);sentT=setTimeout(()=>sent.classList.remove('show'),2000);});
  page.append(sent,send); spot.appendChild(page);
  spot.addEventListener('click',e=>e.stopPropagation());
  spot._hint=hint;
}
function openSpot(){ closePop(false); closeAssist(false); if(!spotBuilt) buildSpot(); spotOpen=true; spot.scrollTop=0; spot.classList.add('open'); scrim.classList.add('open'); setCopy(EXTRA.spot);
  if(!hinted){ setTimeout(()=>spot._hint.classList.add('show'),reduced?0:400); setTimeout(()=>spot._hint.classList.remove('show'),4000); }
  setTimeout(()=>spot.querySelector('.pd-pin').focus({preventScroll:true}),reduced?0:320); }
function closeSpot(focus){ if(!spotOpen) return; spotOpen=false; spot.classList.remove('open'); if(!assistOpen) scrim.classList.remove('open'); setCopy(activeCopy());
  if(focus){const h=phone.querySelector('#pd-view-my-slip .pd-hot'); if(h&&current==='my-slip') h.focus({preventScroll:true});} }

// ---------- full screen (mobile) ----------
const explore=document.getElementById('pd-explore'); let isFull=false, holder=null, savedY=0;
function openFull(){ if(isFull) return; isFull=true; savedY=scrollY; holder=document.createComment('pd-phone'); phone.before(holder); document.body.appendChild(phone);
  phone.classList.add('is-full'); document.documentElement.classList.add('pd-locked'); document.body.style.position='fixed'; document.body.style.top=(-savedY)+'px'; document.body.style.width='100%';
  history.pushState({pdFull:true},''); $('.pd-fsclose').focus({preventScroll:true}); }
function closeFull(fromPop){ if(!isFull) return; isFull=false; phone.classList.remove('is-full'); holder.replaceWith(phone); holder=null;
  document.documentElement.classList.remove('pd-locked'); document.body.style.position=''; document.body.style.top=''; document.body.style.width=''; scrollTo({top:savedY,left:0,behavior:'instant'});
  if(!fromPop&&history.state&&history.state.pdFull) history.back(); if(explore) explore.focus({preventScroll:true}); }
if(explore) explore.addEventListener('click',()=>openFull());
$('.pd-fsclose').addEventListener('click',e=>{e.stopPropagation();closeFull(false);});
addEventListener('popstate',()=>{ if(isFull) closeFull(true); });

document.addEventListener('keydown',e=>{ if(e.key!=='Escape') return;
  if(openPop) closePop(true); else if(assistOpen) closeAssist(true); else if(spotOpen) closeSpot(true); else if(isFull) closeFull(false); });

// public hook for "Try it" links
window.pdDemo={openSpot:()=>{ if(current!=='my-slip') show('my-slip'); openSpot(); }, openFull, isNarrow:()=>!!explore&&getComputedStyle(explore).display!=='none'};
show('my-slip');
})();
