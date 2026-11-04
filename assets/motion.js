() => {
 const root=document.querySelector('gradio-app')?.shadowRoot||document;
 const one=s=>root.querySelector(s), all=s=>[...root.querySelectorAll(s)];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let mounted=false;
 const setup=()=>{
  const room=one('.reading-room');
  if(!room||mounted)return;
  mounted=true;let position=0;const folios=all('[data-folio]');
  all('[data-folio-step]').forEach(b=>b.addEventListener('click',()=>{
   position=(position+Number(b.dataset.folioStep)+folios.length)%folios.length;
   folios.forEach((f,i)=>{f.hidden=i!==position;});
   one('.folio-position').textContent=['١','٢','٣'][position]+' / ٣';
  }));
  all('a[href^="#"]').forEach(a=>a.addEventListener('click',event=>{
   const target=one(a.getAttribute('href'));if(!target)return;
   event.preventDefault();target.scrollIntoView({behavior:reduced?'auto':'smooth',block:'start'});
   if(target.id==='search-start')setTimeout(()=>one('textarea')?.focus({preventScroll:true}),reduced?0:400);
  }));
 };
 setup();const observer=new MutationObserver(setup);observer.observe(root===document?document.body:root,{childList:true,subtree:true});
 if(reduced)return;
 const load=(url,key)=>new Promise((resolve,reject)=>{
  if(window[key])return resolve();
  const script=document.createElement('script');const timeout=setTimeout(reject,3500);
  script.src=url;script.async=true;script.onload=()=>{clearTimeout(timeout);resolve();};script.onerror=()=>{clearTimeout(timeout);reject();};document.head.appendChild(script);
 });
 load('https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js','gsap')
 .then(()=>load('https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js','ScrollTrigger'))
 .then(()=>{
  const gsap=window.gsap;gsap.registerPlugin(window.ScrollTrigger);
  const mm=gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)',()=>{
   const image=one('.hero-engraving'),hero=one('.taste-hero');
   if(image&&hero){
    gsap.fromTo(image,{scale:.8},{scale:1,ease:'none',scrollTrigger:{trigger:hero,start:'top bottom',end:'center center',scrub:.6}});
    gsap.to(image,{opacity:.2,ease:'none',scrollTrigger:{trigger:hero,start:'center top',end:'bottom top',scrub:.6}});
   }
   const room=one('.reading-room');
   all('.back-folio').forEach((card,i)=>gsap.fromTo(card,{y:50+(i*20),rotation:0},{y:0,rotation:i===0?3:-3,ease:'none',scrollTrigger:{trigger:room,start:'top 95%',end:'center 60%',scrub:.7}}));
  });
  addEventListener('pagehide',()=>{observer.disconnect();mm.revert();},{once:true});
 }).catch(()=>{});
}
