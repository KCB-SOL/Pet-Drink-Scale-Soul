from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1500)
    pg.evaluate("""(()=>{S.onboarded=true;S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;window.confirm=()=>true;
      S.stash=Array.from({length:4}).map((_,i)=>{const p=makePet();p.stage='adult';p.level=18;p.name='P'+i;return p});
      S.team=[];save();const e=document.getElementById('intro');if(e)e.remove();S._btab='team';go('battle')})()""")
    pg.wait_for_timeout(700)
    pg.evaluate("(()=>{toggleTeam(S.stash[0].id);toggleTeam(S.stash[1].id)})()"); pg.wait_for_timeout(300)
    print('bước 1 — xếp 2 pet phụ:')
    print('   S.team:', pg.evaluate("S.team.length"), '| teamPets():', pg.evaluate("teamPets().length"))
    print('bước 2 — đổi P0 lên làm pet chính (swapPet):')
    pg.evaluate("(()=>{const i=S.stash.findIndex(p=>p.name==='P0');swapPet(i)})()"); pg.wait_for_timeout(500)
    print('   S.team:', pg.evaluate("S.team.length"), '| teamPets():', pg.evaluate("teamPets().length"),
          '| pet chính:', pg.evaluate("S.pet.name"))
    print('   trần:', pg.evaluate("teamSize()"))
    print('bước 3 — thử thêm pet phụ nữa:')
    r=pg.evaluate("(()=>{const p=S.stash.find(x=>!S.team.includes(x.id)&&x.id!==S.pet.id);toggleTeam(p.id);return teamPets().length})()")
    pg.wait_for_timeout(300)
    print('   thêm được không:', 'KHÔNG' if r==1 else 'được', '| teamPets():', r)
    print('   => người chơi chỉ thấy', r, 'pet hỗ trợ dù trần là 2')
    b.close()
