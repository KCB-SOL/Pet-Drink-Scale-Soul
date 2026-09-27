from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    pg.evaluate("""(()=>{S.onboarded=true;S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;
      S.stash=Array.from({length:5}).map((_,i)=>{const p=makePet();p.stage='adult';p.level=18;p.name='P'+i;return p});
      S.team=[];save();const e=document.getElementById('intro');if(e)e.remove();
      S._btab='team';go('battle')})()""")
    pg.wait_for_timeout(900)
    print('trần tổ đội:', pg.evaluate("teamSize()"), '| DB.team.size:', pg.evaluate("DB.team.size"))
    print('nút Dùng trên màn:', pg.evaluate("(()=>{return [...document.querySelectorAll('#v-battle button')].filter(b=>/Dùng|Thêm|Rút/.test(b.textContent)).length})()"))
    for i in range(3):
        pg.evaluate(f"(()=>{{toggleTeam(S.stash[{i}].id)}})()"); pg.wait_for_timeout(300)
        print(f'  thêm P{i} -> tổ đội:', pg.evaluate("S.team.length"))
    print('teamPets() trả về:', pg.evaluate("teamPets().length"), 'pet')
    print('ô tổ đội vẽ ra:', pg.evaluate("(()=>{const n=document.querySelectorAll('#v-battle .tslot, #v-battle .tmslot');return n.length})()"))
    html=pg.evaluate("document.getElementById('v-battle').innerHTML")
    import re
    print('có chữ "tối đa":', [x for x in re.findall(r'tối đa[^<]{0,40}', html)][:2])
    # bấm thật trên giao diện, không gọi hàm
    pg.evaluate("(()=>{S.team=[];mount()})()"); pg.wait_for_timeout(600)
    cards=pg.locator('#v-battle .tm').last.locator('.tmc')
    print('thẻ trong mục Chuồng:', cards.count())
    for i in range(min(3,cards.count())):
        try:
            cards.nth(i).click(timeout=3000); pg.wait_for_timeout(400)
            print(f'  bấm thẻ {i} -> tổ đội:', pg.evaluate("S.team.length"))
        except Exception as e:
            print(f'  bấm thẻ {i} THẤT BẠI:', str(e)[:80])
    print('LỖI:', errs[:3] if errs else 'không có')
    b.close()
