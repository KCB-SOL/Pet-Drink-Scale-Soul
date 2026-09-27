from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w,h,name in [(390,844,'iPhone'),(820,1180,'iPad'),(1440,900,'Desktop')]:
        pg=b.new_page(viewport={'width':w,'height':h})
        pg.add_init_script("localStorage.clear()")
        pg.goto(url); pg.wait_for_timeout(1300)
        pg.evaluate("""(()=>{S.onboarded=true;S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};
          S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};
          save();const e=document.getElementById('intro');if(e)e.remove();S._btab='tower';go('battle')})()""")
        pg.wait_for_timeout(700)
        r=pg.evaluate("""(()=>{
          const nav=document.querySelector('.nav').getBoundingClientRect();
          const wrap=document.querySelector('.wrap').getBoundingClientRect();
          const cats=document.querySelector('.cats');
          const bs=[...cats.querySelectorAll('button')];
          const rows=new Set(bs.map(b=>Math.round(b.getBoundingClientRect().top))).size;
          const tran = bs.some(b=>{const r=b.getBoundingClientRect();
            return r.left < wrap.left-1 || r.right > wrap.right+1});
          return {navKhopCot: Math.abs(nav.left-wrap.left)<2 && Math.abs(nav.width-wrap.width)<2,
                  tabHang:rows, tabTran:tran,
                  cuonNgang: document.documentElement.scrollWidth > innerWidth+1}})()""")
        print(f'{name:8s} {r}')
        pg.close()
    b.close()
