from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844})
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    pg.evaluate("""(()=>{S.onboarded=true;S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;S.frame='tet';
      S.pet.stage='evo';S.pet.level=32;refreshSkills(S.pet);
      sndInit();musicStart();save();const e=document.getElementById('intro');if(e)e.remove();go('home')})()""")
    pg.wait_for_timeout(1500)
    r=pg.evaluate("""(()=>new Promise(res=>{
      const t=[];let last=performance.now(),n=0;
      function tick(){const now=performance.now();t.push(now-last);last=now;n++;
        if(n<270)requestAnimationFrame(tick);
        else{t.sort((a,b)=>a-b);
          res({trungVi:+t[Math.floor(t.length/2)].toFixed(1),
               teNhat:+t[t.length-1].toFixed(1),
               rot:t.filter(x=>x>32).length})}}
      requestAnimationFrame(tick)}))""")
    print('hiệu năng (nhạc + khung lễ + hiệu ứng nền):', r)
    b.close()
