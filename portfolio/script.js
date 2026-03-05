/* ── CURSOR ── */
const dot=document.getElementById('dot'),ring=document.getElementById('ring');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;dot.style.left=mx+'px';dot.style.top=my+'px'});
setInterval(()=>{rx+=(mx-rx)*.12;ry+=(my-ry)*.12;ring.style.left=rx+'px';ring.style.top=ry+'px'},16);

/* ── NAVBAR ── */
window.addEventListener('scroll',()=>{
  document.getElementById('nav').classList.toggle('pinned',scrollY>60);
  ['home','about','expertise','projects','contact','thankyou'].forEach(id=>{
    const el=document.getElementById(id),a=document.querySelector(`.n-links a[href="#${id}"]`);
    if(el&&a){const r=el.getBoundingClientRect();a.classList.toggle('act',r.top<=110&&r.bottom>80);}
  });
});
function toggleNav(){document.getElementById('navLinks').classList.toggle('show')}
document.querySelectorAll('.n-links a').forEach(a=>a.addEventListener('click',()=>document.getElementById('navLinks').classList.remove('show')));

/* ── TYPING ── */
const words=['Full Stack Developer','UI / UX Designer','Python Enthusiast','Problem Solver','Creative Coder'];
let wi=0,ci=0,del=false;
function type(){
  const el=document.getElementById('typer');if(!el)return;
  const w=words[wi];
  if(del){el.textContent=w.slice(0,--ci);if(!ci){del=false;wi=(wi+1)%words.length;setTimeout(type,380);return;}}
  else{el.textContent=w.slice(0,++ci);if(ci===w.length){setTimeout(()=>{del=true;type()},2000);return;}}
  setTimeout(type,del?55:90);
}
setTimeout(type,900);

/* ── REVEAL ON SCROLL ── */
const obs=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('up');obs.unobserve(e.target);}});
},{threshold:.07,rootMargin:'0px 0px -20px 0px'});
document.querySelectorAll('.reveal').forEach(el=>{
  obs.observe(el);
  // Reveal anything already in viewport immediately
  if(el.getBoundingClientRect().top<window.innerHeight)el.classList.add('up');
});

/* ── TIMELINE ── */
const tlo=new IntersectionObserver(es=>{
  es.forEach((e,i)=>{if(e.isIntersecting)setTimeout(()=>e.target.classList.add('shown'),i*120)});
},{threshold:.1});
document.querySelectorAll('.tl-item').forEach(t=>tlo.observe(t));

/* ── SKILL BARS ── */
const sbo=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){e.target.style.width=e.target.dataset.w+'%';sbo.unobserve(e.target);}});
},{threshold:.1});
document.querySelectorAll('.sk-bar').forEach(b=>{b.style.transition='width 1.5s cubic-bezier(.25,1,.5,1)';sbo.observe(b);});

/* ── COUNTERS ── */
const cto=new IntersectionObserver(es=>{
  es.forEach(e=>{
    if(e.isIntersecting&&!e.target.dataset.done){
      e.target.dataset.done='1';
      const t=+e.target.dataset.t;let c=0;
      const iv=setInterval(()=>{c=Math.min(c+Math.max(1,Math.ceil(t/50)),t);e.target.textContent=c+(t===100?'%':'+');if(c>=t)clearInterval(iv);},28);
    }
  });
},{threshold:.5});
document.querySelectorAll('.stat-n').forEach(s=>cto.observe(s));

/* ── PROJECTS ── */
const PROJS=[
  {id:1,cat:'web',icon:'❓',bg:'linear-gradient(135deg,#1a0d20,#7a3560)',title:'Quiz App',desc:'Interactive quiz application with multiple categories, timed questions, score tracking and a dynamic leaderboard. Built with a clean UI and smooth transitions.',tags:['HTML','CSS','JavaScript','Python'],demo:'https://patelprachi0217.github.io/Quiz'},
  {id:2,cat:'web',icon:'🌿',bg:'linear-gradient(135deg,#0d1a10,#2d6a45)',title:'Botanica',desc:'Beautiful plant shop web app featuring product listings, cart functionality, search & filter, and a fully responsive layout with an elegant botanical theme.',tags:['HTML','CSS','JavaScript','Django'],demo:'https://patelprachi0217.github.io/botanica'},
  {id:3,cat:'web',icon:'🛋️',bg:'linear-gradient(135deg,#1a100d,#6a3a20)',title:'Cushie Corner',desc:'Full-featured e-commerce store for home furnishings built with Django. Includes product management, user authentication, cart, wishlist and checkout with MySQL.',tags:['Django','Python','MySQL','Bootstrap'],demo:'https://patelprachi0217.github.io/cushie_corner_django'},
];
let curF='all';
function rp(){
  const g=document.getElementById('pg');
  const list=curF==='all'?PROJS:PROJS.filter(p=>p.cat===curF);
  g.innerHTML=list.map(p=>`
  <div class="p-card" onclick="om(${p.id})">
    <div class="p-thumb" style="background:${p.bg}">
      <div class="p-thumb-inner">${p.icon}</div>
      <div class="p-overlay">
        <a class="p-btn pb-w" href="${p.demo||'#'}" target="_blank" onclick="event.stopPropagation()"><i class="fas fa-external-link-alt"></i> Live Demo</a>
      </div>
    </div>
    <div class="p-body">
      <h3>${p.title}</h3>
      <p>${p.desc.slice(0,92)}…</p>
      <div class="tags">${p.tags.map(t=>`<span class="t-chip">${t}</span>`).join('')}</div>
    </div>
  </div>`).join('');
}
function fp(cat,btn){
  curF=cat;
  document.querySelectorAll('.ft').forEach(b=>b.classList.remove('on'));btn.classList.add('on');
  const g=document.getElementById('pg');
  g.style.cssText='opacity:0;transform:translateY(10px);transition:all .3s';
  setTimeout(()=>{rp();g.style.cssText='opacity:1;transform:none;transition:all .35s'},200);
}
function om(id){
  const p=PROJS.find(x=>x.id===id);if(!p)return;
  document.getElementById('mc').style.background=p.bg;document.getElementById('mc').textContent=p.icon;
  document.getElementById('mt').textContent=p.title;
  document.getElementById('md').textContent=p.desc+' Built with clean architecture and a user-centered design approach.';
  document.getElementById('mch').innerHTML=p.tags.map(t=>`<span class="t-chip">${t}</span>`).join('');
  const dmEl=document.getElementById('mdm');if(dmEl){dmEl.href=p.demo||'#';}
  document.getElementById('mv').classList.add('open');
}
function cm(){document.getElementById('mv').classList.remove('open')}
document.getElementById('mv').addEventListener('click',e=>{if(e.target===e.currentTarget)cm()});
rp();

/* ── FORM ── */
function sf(){
  const fs=[
    {id:'fN',ok:v=>v.length>1},
    {id:'fE',ok:v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)},
    {id:'fS',ok:v=>v.length>2},
    {id:'fM',ok:v=>v.length>5},
  ];
  let ok=true;
  fs.forEach(f=>{
    const el=document.getElementById(f.id),g=el.closest('.fg');
    g.classList.toggle('err',!f.ok(el.value.trim()));
    if(!f.ok(el.value.trim()))ok=false;
  });
  if(!ok)return;

  const btn=document.querySelector('#fw .btn');
  btn.disabled=true;
  btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Sending…';

  emailjs.send('service_portfolio','template_contact',{
    from_name:  document.getElementById('fN').value.trim(),
    from_email: document.getElementById('fE').value.trim(),
    subject:    document.getElementById('fS').value.trim(),
    message:    document.getElementById('fM').value.trim(),
    to_email:   'patelprachi0217@gmail.com',
  })
  .then(()=>{
    document.getElementById('fw').style.display='none';
    document.getElementById('fok').classList.add('show');
  })
  .catch(err=>{
    console.error('EmailJS error',err);
    btn.disabled=false;
    btn.innerHTML='<i class="fas fa-paper-plane"></i> Send Message';
    alert('Oops! Something went wrong. Please try again or reach out via WhatsApp. 🌸');
  });
}
function rf(){
  ['fN','fE','fS','fM'].forEach(id=>document.getElementById(id).value='');
  document.querySelectorAll('.fg').forEach(g=>g.classList.remove('err'));
  document.getElementById('fw').style.display='block';
  document.getElementById('fok').classList.remove('show');
}

/* ── TERMINAL ── */
let tOpen=false,tHist=[],tHI=-1;
const TC={
  help:{f:()=>`<div class="thi" style="margin-bottom:.3rem">Commands</div><div class="tok">  nav &lt;section&gt;  — jump to section</div><div class="tok">  sections       — list sections</div><div class="tok">  whoami         — about Prachi</div><div class="tok">  stack          — tech stack</div><div class="tok">  projects       — project list</div><div class="tok">  contact        — contact info</div><div class="tok">  social         — social links</div><div class="tok">  clear / exit   — clear / close</div>`},
  sections:{f:()=>`<div class="tok">home · about · expertise · projects · contact · thankyou</div>`},
  whoami:{f:()=>`<div class="tok">Prachi Patel — Full Stack Developer 🌸</div><div class="tok">📍 Ahmedabad, India | 🎓 B.Tech CS, GTU</div><div class="tok">💻 React · Django · Python · Node.js</div>`},
  stack:{f:()=>`<div class="thi">Frontend:</div><div class="tok">HTML · CSS · Tailwind · JS · React</div><div class="thi">Backend:</div><div class="tok">Python · Django · Node.js · Express</div><div class="thi">DB:</div><div class="tok">MySQL · SQLite · MongoDB</div><div class="thi">Tools:</div><div class="tok">Git · VS Code · Figma · Postman</div>`},
  projects:{f:()=>PROJS.map((p,i)=>`<div class="tok">${i+1}. ${p.title} — <span style="color:var(--rose)">${p.cat}</span></div>`).join('')},
  contact:{f:()=>`<div class="tok">📧 patelprachi0217@gmail.com</div><div class="tok">📱 +91 98987 30192</div><div class="tok">📍 Ahmedabad, India</div>`},
  social:{f:()=>`<div class="tok">GitHub   → github.com/patelprachi0217</div><div class="tok">LinkedIn → linkedin.com/in/prachipatel0217</div><div class="tok">Email    → patelprachi0217@gmail.com</div><div class="tok">WhatsApp → +91 98987 30192</div>`},
  clear:{f:()=>{document.getElementById('tb2').innerHTML='';return null}},
  exit:{f:()=>{setTimeout(()=>{tOpen=false;document.getElementById('tw').classList.remove('open')},150);return`<div class="tdm">Goodbye! 🌸</div>`}},
};
function ta(showP,cmd,out){
  const b=document.getElementById('tb2');
  if(showP&&cmd){const l=document.createElement('div');l.style.cssText='display:flex;gap:.4rem;margin-bottom:.1rem';l.innerHTML=`<span class="tp">prachi:~$</span><span style="color:var(--text)">${cmd}</span>`;b.appendChild(l);}
  if(out!=null){const d=document.createElement('div');d.innerHTML=out;b.appendChild(d);}
  b.scrollTop=b.scrollHeight;
}
function tk(e){
  const inp=document.getElementById('ti');
  if(e.key==='Enter'){
    const raw=inp.value.trim();if(!raw)return;
    tHist.unshift(raw);tHI=-1;inp.value='';
    const parts=raw.split(' '),base=parts[0].toLowerCase();
    if(base==='nav'&&parts[1]){
      const sec=document.getElementById(parts[1]);
      if(sec){sec.scrollIntoView({behavior:'smooth'});ta(true,raw,`<div class="tdm">→ Scrolling to ${parts[1]}…</div>`);}
      else ta(true,raw,`<div class="ter">Section not found. Type 'sections'</div>`);
      return;
    }
    if(TC[base]){const r=TC[base].f();ta(true,raw,r);}
    else ta(true,raw,`<div class="ter">Unknown: '${raw}'. Type 'help'</div>`);
  } else if(e.key==='ArrowUp'){tHI=Math.min(tHI+1,tHist.length-1);inp.value=tHist[tHI]||''}
  else if(e.key==='ArrowDown'){tHI=Math.max(tHI-1,-1);inp.value=tHI>=0?tHist[tHI]:''}
}
function toggleTerm(){
  tOpen=!tOpen;
  document.getElementById('tw').classList.toggle('open',tOpen);
  if(tOpen&&!document.getElementById('tb2').innerHTML.trim()){
    setTimeout(()=>{
      ta(false,null,`<div class="tdm">Welcome to Prachi's Portfolio Terminal 🌸</div>`);
      ta(false,null,`<div class="tdm">Type <strong style="color:var(--rose)">help</strong> to get started.</div>`);
      ta(false,null,`<div class="tdm">──────────────────────────────</div>`);
    },80);
}
if(tOpen)setTimeout(()=>document.getElementById('ti').focus(),350);
}