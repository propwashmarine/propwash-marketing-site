/* Owner Portal interactive demo. Host page provides #pd-phone (src/components/portal-demo.html) and,
   optionally, #pd-now-h / #pd-now-p (caption), #pd-explore (mobile full-screen button). */
(()=>{
const phone=document.getElementById('pd-phone'); if(!phone) return;
// ?hotspots=1 outlines every tap area (debug).
if(new URLSearchParams(location.search).get('hotspots')==='1') phone.classList.add('pd-debug');
const $=s=>phone.querySelector(s), $$=s=>[...phone.querySelectorAll(s)];
const BASE='/assets/portal/', W=1206;                // all coordinates below are in 1206px image space
const IV=(document.currentScript&&new URL(document.currentScript.src).search)||''; // reuse demo.js ?v= so edited images aren't served stale
const u=px=>(px/W*100).toFixed(3)+'cqw';
// Tap areas over a screenshot: a box in 1206px image space as percentages of that image (hgt = WebP height at 600 wide).
const pct=v=>(v*100).toFixed(4)+'%';
const placeBox=(el,r,w,h)=>Object.assign(el.style,{left:pct(r.x/w),top:pct(r.y/h),width:pct(r.w/w),height:pct(r.h/h)});
const placeHot=(el,r,hgt)=>{const H=hgt*W/600; Object.assign(el.style,{left:pct(r.x/W),top:pct(r.y/H),width:pct(r.w/W),height:pct(r.h/H)});};
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const ss={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}};

// Service section views and Schedule Care choices (the portal's own dropdowns, rebuilt in HTML).
const VIEWS=[['Upcoming Visits','upcoming-visits'],['Service History','service-history'],['Services','services'],['Schedule Care','schedule-care']];
const CARE=[['Additional wash','schedule-care'],['Trip Ready','schedule-care-trip'],['After-trip washdown','schedule-care-washdown']];
const VIEW_OF={'schedule-care-trip':'schedule-care','schedule-care-washdown':'schedule-care','schedule-care-quote':'schedule-care'};

const SCREENS={
 'my-slip':{tab:'my-slip',h:'My Slip',p:"Your boat's status, next visit and protection at a glance.",hgt:2429,
   alt:"My Slip screen: a welcome-back greeting for Jack, the Salty Dog boat card (43 ft Mag Bay, Boca Raton, service scheduled), you're all caught up, a protection status ring counting down 4 days to the next visit (we'll be by Nov 3; ceramic booster in about 2 months), the next visit, a Full Detail on Tuesday, Nov 3 at 8:00 AM in Boca Raton with a Move link, a Report a Spot card, latest photos, the service log with Member Washes on Tuesday, Oct 27, Oct 20 and Oct 13, and a paid-up balance.",
   hot:[{x:36,y:2677,w:1134,h:285,label:'Report a Spot',act:()=>openSpot()},
     {x:95,y:3129,w:311,h:190,label:'Latest photo 1, open Photos',act:()=>show('photos')},
     {x:447,y:3129,w:311,h:190,label:'Latest photo 2, open Photos',act:()=>show('photos')},
     {x:799,y:3129,w:311,h:190,label:'13 more photos, open Photos',act:()=>show('photos')},
     {x:60,y:3322,w:270,h:190,label:'View all photos',act:()=>show('photos')},
     {x:93,y:3700,w:1019,h:190,label:'Member Wash, Tue, Oct 27, open Service History',act:()=>show('service-history')},
     {x:93,y:3901,w:1019,h:190,label:'Member Wash, Tue, Oct 20, open Service History',act:()=>show('service-history')},
     {x:93,y:4102,w:1019,h:190,label:'Member Wash, Tue, Oct 13, open Service History',act:()=>show('service-history')},
     {x:60,y:4294,w:270,h:190,label:'View all service history',act:()=>show('service-history')},
     {x:60,y:4638,w:400,h:190,label:'View payments',act:()=>show('payments')}]},
 'on-water':{tab:'on-water',h:'On the Water',p:'Know the conditions before you leave the dock.',hgt:4300,
   alt:"On the Water screen for Boca Raton: a weather alert, current conditions with wind, seas, water temperature and chance of rain, boating day scores for the week (scroll sideways), a day forecast, hour-by-hour forecast, tide table, sunrise, sunset and moon, peak bite windows, and a Book a wash prompt.",
   scores:{x:39,y:2040,w:1127,h:366,full:1841,snaps:[246,246,222,1127]},
   hot:[{x:92,y:7642,w:1019,h:190,label:'Book a wash, open Schedule Care',act:()=>show('schedule-care')}]},
 'photos':{tab:'photos',h:'Every visit, documented.',p:'See the photos from each visit, kept with the boat.',hgt:1494,
   alt:"Vessel Photos screen: a two-column grid of photos of the boat from service visits, including the helm, seating, outboard engines and the Mag Bay transom."},
 'membership':{tab:'svc',h:'Your plan',p:'Your membership and everything it covers.',hgt:4699,
   alt:"Membership screen headed Choose your level, we'll handle the rest: the active Platinum membership on Salty Dog (43 ft) with Change Plan open, the Gold plan (complete maintenance, keeps it maintained) and the Silver plan (essential care, keeps it clean), each priced for your boat as Custom, billed monthly, with what each handles, including recurring Member Washes, and Request Gold and Request Silver buttons; then My Membership with a Contract PDF link and what's included: 3 Member Washes a month every 7 days, 1 Full Detail a month, 4 booster events a year, a full exterior wash and salt rinse every visit, two Trip Ready preps a month, a dedicated detailer, on-call washdowns, See a Spot, top priority, first access to new services, invite-only for 15 boats; typical and booster months shown as Custom; active since Sep 29, 2026, renewing Sep 29, 2027; and Cancel membership."},
 'upcoming-visits':{tab:'svc',h:'Upcoming visits',p:'Confirm a date, request a change or cancel a visit without affecting your membership.',hgt:1558,
   alt:"Services and Visits screen on Upcoming Visits: four scheduled visits for Salty Dog in Boca Raton, each with a Manage visit button: a Full Detail on Tuesday, November 3, 2026 at 08:00, then Member Washes on November 10, 17 and 24, 2026 at 08:00 with covers put back on, and a Need to cancel? link.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS}],
   hot:[{x:80,y:1360,w:1046,h:190,label:'Manage visit, Full Detail, Tue, Nov 3',act:()=>openModal('manage-visit')}]},
 'service-history':{tab:'svc',h:'Every visit, on the record.',p:'Open a completed visit to see what was done, the photos and the invoice.',hgt:1767,
   alt:"Services and Visits screen on Service History: four completed visits. The Member Wash on October 27, 2026 is open, showing its service description, detailer Jack, notes, a photo and its related invoice, PWM-1234. Below it, completed Member Washes on October 20 and 13, 2026 and a Full Detail on October 6, 2026.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS}],
   hot:[{x:143,y:1913,w:188,h:187,label:'Visit photo, open Photos',act:()=>show('photos')},{x:141,y:2223,w:924,h:132,label:'View invoice PWM-1234',act:()=>show('invoice')}]},
 'services':{tab:'svc',h:'The Full Service Menu',p:'Browse every service and request a quote in a tap.',hgt:12285,
   alt:"Services and Visits screen on Services: a Request a Quote link and every Propwash service with a description of each, in five open sections: Included with membership (Member Wash, Full Detail, Ceramic Booster, Member Wax, Post-Trip Washdown, Trip Ready), One time services (Captain's Wash, Full Detail, Trip Ready, Freshwater Rinse and three Interior Deep Clean options), Detailing and correction (Full Detail and Wax, polish, compound and wet-sand packages), Ceramic coating packages, and Teak (Clean and Brighten, Restoration, Seal).",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS}],
   hot:[{x:40,y:980,w:420,h:80,label:'Request a Quote',act:()=>show('schedule-care-quote')}]},
 'schedule-care':{tab:'svc',h:'Book a service',p:'Pick a day and request the time that works for you.',hgt:2175,
   alt:"Services and Visits screen on Schedule Care, Schedule Care tab, with Additional wash chosen (an additional Member Wash at your signed member rate): Schedule member care for Platinum, an October 2026 calendar with Friday, October 30 marked as today, the selected date panel, location Boca Raton, covers back on or off after the visit, and a Request a Member Wash button.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS},{box:{x:42,y:1077,w:1122,h:132},top:1222,kind:'care',label:'Choose care',options:CARE}],
   hot:[{x:606,y:786,w:543,h:117,label:'Request a Quote tab',act:()=>show('schedule-care-quote')}]},
 'schedule-care-trip':{tab:'svc',h:'Book a service',p:'Pick a day and request the time that works for you.',hgt:2342,
   alt:"Services and Visits screen on Schedule Care with Trip Ready chosen: Platinum includes up to two Trip Ready preps each month. Schedule member care with an October 2026 calendar with Friday, October 30 marked as today, the selected date, what time the boat should be ready (10:00 AM), location Boca Raton, covers back on or off, and a Request Trip Ready button.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS},{box:{x:42,y:1077,w:1122,h:132},top:1222,kind:'care',label:'Choose care',options:CARE}],
   hot:[{x:606,y:786,w:543,h:117,label:'Request a Quote tab',act:()=>show('schedule-care-quote')}]},
 'schedule-care-washdown':{tab:'svc',h:'Book a service',p:'Pick a day and request the time that works for you.',hgt:2448,
   alt:"Services and Visits screen on Schedule Care with After-trip washdown chosen: an on-call freshwater washdown is included with Platinum. Schedule member care with an October 2026 calendar with Friday, October 30 marked as today, the selected date, what time you will be off the water (10:00 AM, confirmed by the crew), location Boca Raton, covers back on or off, and a Request washdown button.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS},{box:{x:42,y:1077,w:1122,h:132},top:1222,kind:'care',label:'Choose care',options:CARE}],
   hot:[{x:606,y:786,w:543,h:117,label:'Request a Quote tab',act:()=>show('schedule-care-quote')}]},
 'schedule-care-quote':{tab:'svc',h:'Need more than a wash?',p:'Choose the services you want and we will put a quote together.',hgt:2560,
   alt:"Services and Visits screen on Schedule Care, Request a Quote tab: choose one service, with teak as an optional add-on, from Full Detail, the detailing and correction packages, the ceramic coating packages and the teak services (Teak Seal is an add-on to Teak Clean and Brighten or Teak Restoration), then notes and a Submit request button.",
   selects:[{box:{x:42,y:543,w:1122,h:132},top:688,kind:'view',label:'Service section',options:VIEWS}],
   hot:[{x:57,y:786,w:543,h:117,label:'Schedule Care tab',act:()=>show('schedule-care')}]},
 'payments':{tab:'act',h:'Invoices & payments',p:'View and pay invoices right in the portal, with every receipt kept on file.',hgt:564,
   alt:"Invoices and Payments screen: paid up, we're all settled with nothing due right now, and under Paid / past invoices, invoice PWM-1234 for the Platinum Membership plus 4 more, paid October 29, 2026, with View invoice and PDF buttons.",
   hot:[{x:60,y:895,w:380,h:95,label:'View invoice PWM-1234',act:()=>show('invoice')}]},
 'invoice':{tab:'act',h:'Every invoice, on file.',p:'Each line shows the visit it covers, with the receipt kept in the portal.',hgt:3343,
   alt:"Invoice PWM-1234, marked paid: the Propwash Marine Detailing header with billing@propwashmarine.com, bill to Jack at jack@propwashmarine.com, vessel Salty Dog (Mag Bay, 43 ft, Boca Raton), invoice date 2026-10-28, the Platinum Plan membership invoice for October 2026 billed as delivered: the Platinum Membership monthly tier fee, a Full Detail on October 6, and Member Washes on October 13, 20 and 27, 2026, each with its rate, with every amount, the subtotal and the grand total shown as Custom; paid October 29, 2026, and a Download PDF button.",
   hot:[{x:30,y:80,w:450,h:95,label:'Back to payments',act:()=>show('payments')}]},
 'messages':{tab:'act',h:'Talk to your detailer.',p:'Message us directly and catch our latest news.',hgt:1112,scrollTo:650,
   alt:"News and Messages screen on the Messages tab: a Talk to a Detailer conversation with Jack, your detailer, on October 4 between 12:15 and 12:25 PM. The owner asks for a Sunday washdown after a Saturday on the water, Jack says Sunday afternoon works and asks about the covers, the owner says the new gate code will be in the access notes, and Jack says they will send photos when they are done. A message field and Send button are below.",
   hot:[{x:43,y:196,w:754,h:190,label:'Ask the Propwash Assistant',act:()=>openAssist()},{x:36,y:470,w:567,h:128,label:'Announcements tab',act:()=>show('announcements')}]},
 'announcements':{tab:'act',h:'News from the crew.',p:'Updates on the weather, the season and what is new in your portal.',hgt:1182,
   alt:"News and Messages screen on the Announcements tab: On the Water is live (Oct 2, 2026), Heading back down this season? (Sep 22, 2026) and After the storm (Aug 18, 2026).",
   hot:[{x:36,y:204,w:755,h:190,label:'Ask the Propwash Assistant',act:()=>openAssist()},{x:603,y:490,w:555,h:142,label:'Messages tab',act:()=>show('messages')}]},
};
const EXTRA={assistant:{h:'Answers on hand.',p:'Ask about your boat, your plan or your schedule, any time.'},
  spot:{h:'See a spot? Send it to us.',p:"Tell us where it is, add a photo and we'll take care of it. Included with Platinum."}};

// ---------- dropdowns (Service section picker, Choose care) ----------
let openSel=null;
function closeSel(focus){ if(!openSel) return; openSel.list.classList.remove('open'); openSel.btn.setAttribute('aria-expanded','false'); if(focus) openSel.btn.focus({preventScroll:true}); openSel=null; }
function buildSelect(screenId,c){
  const wrap=document.createElement('div'); wrap.className='pd-sel';
  const btn=document.createElement('button'); btn.type='button'; btn.className='pd-hot';
  const cur=c.kind==='view'?(VIEW_OF[screenId]||screenId):screenId;
  const curLabel=(c.options.find(o=>o[1]===cur)||c.options[0])[0];
  btn.setAttribute('aria-label',`${c.label}: ${curLabel}`); btn.setAttribute('aria-haspopup','listbox'); btn.setAttribute('aria-expanded','false');
  placeHot(btn,c.box,SCREENS[screenId].hgt);
  const list=document.createElement('div'); list.className='pd-list pd-list-'+c.kind; list.setAttribute('role','listbox'); list.setAttribute('aria-label',c.label);
  Object.assign(list.style,{left:u(42),top:u(c.top),width:u(1126)});
  c.options.forEach(([label,target])=>{ const o=document.createElement('button'); o.type='button'; o.setAttribute('role','option');
    const on=target===cur; o.setAttribute('aria-selected',String(on)); o.innerHTML='<span></span>'+(on?'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>':'');
    o.firstChild.textContent=label;
    o.addEventListener('click',e=>{e.stopPropagation(); closeSel(false); if(target!==current) show(target);}); list.appendChild(o); });
  btn.addEventListener('click',e=>{e.stopPropagation(); const was=openSel&&openSel.list===list; closeSel(false); if(was) return;
    closePop(false); list.classList.add('open'); btn.setAttribute('aria-expanded','true'); openSel={list,btn}; list.querySelector('[aria-selected="true"]')?.focus({preventScroll:true}); });
  list.addEventListener('click',e=>e.stopPropagation());
  wrap.append(btn,list); return wrap;
}

// ---------- build screens ----------
// The phone screen clips, it never scrolls: a focused or scrolled-to tap area near an edge must not shift the whole UI.
const screenEl=$('.pd-screen'); screenEl.addEventListener('scroll',()=>{screenEl.scrollTop=0;screenEl.scrollLeft=0;});
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
    placeHot(b,h,s.hgt);b.addEventListener('click',e=>{e.stopPropagation();closePop(false);h.act();});page.appendChild(b);});
  (s.selects||[]).forEach(c=>page.appendChild(buildSelect(id,c)));
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
  const s=SCREENS[id]; if(!s) return; closeSel(false); closeModal(false);
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
document.addEventListener('click',()=>{closePop(false); closeSel(false); if(spotOpen) closeSpot(false);});
$$('[role="menu"]').forEach(m=>m.addEventListener('keydown',e=>{const it=[...m.querySelectorAll('[role="menuitem"]')],i=it.indexOf(document.activeElement);
  if(e.key==='ArrowDown'){e.preventDefault();it[(i+1)%it.length].focus();} if(e.key==='ArrowUp'){e.preventDefault();it[(i-1+it.length)%it.length].focus();}}));

// ---------- assistant ----------
const fab=$('.pd-fab'), sheet=$('#pd-sheet'), scrim=$('.pd-scrim'), note=$('.pd-note'), bubble=$('.pd-bubble');
let assistOpen=false;
function openAssist(){ closePop(false); closeSpot(false); hideBubble(); fab.classList.remove('unread'); const i=sheet.querySelector('img'); if(!i.src){i.src=i.dataset.src;sheet.classList.add('loaded');}
  assistOpen=true; phone.classList.add('assist-open'); sheet.classList.add('open'); scrim.classList.add('open'); fab.setAttribute('aria-expanded','true'); setCopy(EXTRA.assistant); sheet.querySelector('.x').focus({preventScroll:true}); }
function closeAssist(focus){ if(!assistOpen) return; assistOpen=false; resetChat(); setHistory(false); phone.classList.remove('assist-open'); sheet.classList.remove('open'); scrim.classList.remove('open'); note.classList.remove('show');
  fab.setAttribute('aria-expanded','false'); setCopy(activeCopy()); if(focus) fab.focus({preventScroll:true}); }
fab.addEventListener('click',e=>{e.stopPropagation(); assistOpen?closeAssist(true):openAssist();});
sheet.querySelector('.x').addEventListener('click',e=>{e.stopPropagation();closeAssist(true);});
// History: the history icon shows the Recent chats screen; tapping it again (the back arrow there) or
// closing the assistant returns to the panel. History rows are not tappable.
const histBtn=sheet.querySelector('.hist'), histImg=sheet.querySelector('.pd-hist');
function setHistory(on){ sheet.classList.toggle('history',on); histBtn.setAttribute('aria-pressed',String(on));
  histBtn.setAttribute('aria-label',on?'Back to the assistant':'Conversation history'); if(on&&!histImg.src) histImg.src=histImg.dataset.src; }
histBtn.addEventListener('click',e=>{e.stopPropagation(); setHistory(!sheet.classList.contains('history'));});
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
  const x=document.createElement('button'); x.type='button'; x.className='pd-hot'; x.setAttribute('aria-label','Close Report a Spot'); placeHot(x,{x:1080,y:24,w:100,h:100},1617); x.addEventListener('click',e=>{e.stopPropagation();closeSpot(true);}); page.appendChild(x);
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
  const send=document.createElement('button'); send.type='button'; send.className='pd-hot'; send.setAttribute('aria-label','Report Spot (demo, nothing is sent)'); placeHot(send,{x:60,y:3060,w:1086,h:96},1617);
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

// ---------- visit windows (Manage visit, Request another date or time, Need to cancel?) ----------
// Each is the portal's own window over the screenshot's own dimmed backdrop (a full-screen image), not over a live
// demo screen. Coordinates are in the source image's pixels (bg: 1206 wide; a scrolling window's content: its own width).
// act: 'close' closes the window, 'inert' shows "Available in your portal", or a function.
const MODALS={
 'manage-visit':{label:'Manage visit',bg:'portal-manage-visit.webp',w:1206,h:2376,
   alt:"Manage visit window for the Full Detail on Tuesday, November 3, 2026 at 08:00, over the dimmed Upcoming Visits screen: a Request a change button, a Cancel this visit button, and the note: Approved schedule changes are free. Cancellations under 12 hours incur $50; cancellations within 2 hours incur $99.",
   win:{x:48,y:810,w:1110,h:756},
   hot:[{x:990,y:815,w:160,h:170,label:'Close Manage visit',act:'close'},
        {x:99,y:1029,w:1008,h:168,label:'Request a change',act:'inert'},
        {x:99,y:1197,w:1008,h:168,label:'Cancel this visit',act:'inert'}]},
};
const modals={}; let modalOpen=null, modalOpener=null;
const app=$('.pd-app');
function buildModal(id){ const c=MODALS[id];
  const m=document.createElement('div'); m.className='pd-modal'+(c.center?' center':''); m.id='pd-modal-'+id;
  m.setAttribute('role','dialog'); m.setAttribute('aria-modal','true'); m.setAttribute('aria-label',c.label);
  const st=document.createElement('div'); st.className='pd-mstage'; st.style.aspectRatio=c.w+'/'+c.h;
  const bg=new Image(); bg.className='pd-mbg'; bg.alt=c.alt; bg.decoding='async'; bg.src=BASE+c.bg+IV; st.appendChild(bg);
  const win=document.createElement('div'); win.className='pd-mwin'; placeBox(win,c.win,c.w,c.h); st.appendChild(win);
  let host=st, hw=c.w, hh=c.h;
  if(c.scroll){ win.classList.add('scroll'); win.tabIndex=0; win.setAttribute('aria-label',c.label+', scrolls');
    const pg=document.createElement('div'); pg.className='pd-page'; const im=new Image(); im.alt=c.scroll.alt; im.decoding='async'; im.src=BASE+c.scroll.src+IV;
    pg.appendChild(im); win.appendChild(pg); host=pg; hw=c.scroll.w; hh=c.scroll.h; }
  win.addEventListener('click',e=>e.stopPropagation());   // taps inside the window never close it
  const note=document.createElement('div'); note.className='pd-note pd-mnote'; note.setAttribute('role','status'); note.setAttribute('aria-live','polite'); note.textContent='Available in your portal';
  let noteT=0; const inert=()=>{note.classList.add('show');clearTimeout(noteT);noteT=setTimeout(()=>note.classList.remove('show'),1800);};
  c.hot.forEach(h=>{ const b=document.createElement('button'); b.type='button'; b.className='pd-hot'; b.setAttribute('aria-label',h.label); if(h.act==='close') b.dataset.close='';
    placeBox(b,h,hw,hh); b.addEventListener('click',e=>{e.stopPropagation(); if(h.act==='close') closeModal(true); else if(h.act==='inert') inert(); else h.act();}); host.appendChild(b); });
  m.append(st,note); m.addEventListener('click',e=>{e.stopPropagation(); closeModal(true);});   // the scrim
  $('.pd-screen').appendChild(m); modals[id]=m; return m; }
function openModal(id){ const m=modals[id]||buildModal(id);
  closePop(false); closeSel(false); closeAssist(false); closeSpot(false);
  if(modalOpen) modalOpen.classList.remove('open'); else modalOpener=document.activeElement;
  modalOpen=m; m.classList.add('open'); app.inert=true; fab.inert=true;
  const w=m.querySelector('.pd-mwin.scroll'); if(w) w.scrollTop=0;
  m.querySelector('[data-close]')?.focus({preventScroll:true}); }
function closeModal(focus){ if(!modalOpen) return; modalOpen.classList.remove('open'); modalOpen=null; app.inert=false; fab.inert=false;
  if(focus&&modalOpener&&modalOpener.isConnected) modalOpener.focus({preventScroll:true}); modalOpener=null; }

document.addEventListener('keydown',e=>{ if(e.key!=='Escape') return;
  if(modalOpen) closeModal(true); else if(openSel) closeSel(true); else if(openPop) closePop(true); else if(assistOpen) closeAssist(true); else if(spotOpen) closeSpot(true); else if(isFull) closeFull(false); });

// public hook for "Try it" links
window.pdDemo={openSpot:()=>{ if(current!=='my-slip') show('my-slip'); openSpot(); }, openFull, isNarrow:()=>!!explore&&getComputedStyle(explore).display!=='none'};
show('my-slip');
})();
