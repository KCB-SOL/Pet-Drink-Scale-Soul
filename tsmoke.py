# Bộ kiểm tổng cho bản v1.0 — thay cho 35 kịch bản đã mất cùng container.
# Đi qua mọi màn, mọi hệ chính, và bắt lỗi trên console.
from playwright.sync_api import sync_playwright
import pathlib, sys
url='file://'+str(pathlib.Path('index.html').resolve())
FAIL=[]
def ck(name, cond, extra=''):
    print(('  OK   ' if cond else '  HỎNG ')+name+(' · '+str(extra) if extra else ''))
    if not cond: FAIL.append(name)

with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]
    pg.on('pageerror',lambda e:errs.append('ERR '+str(e)[:110]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:110]) if m.type=='error' else None)
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    ck('nạp không lỗi', len(errs)==0, errs[:2])

    print('\n— khởi động —')
    ck('màn giới thiệu hiện', pg.locator('#intro').count()==1)
    pg.evaluate("""(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;S.coin=99000;
      S.pet.stage='evo';S.pet.level=32;S.pet.bond=82;refreshSkills(S.pet);
      towerState().tickets=30;advState().passes=4;
      window.confirm=()=>true;save();const e=document.getElementById('intro');if(e)e.remove();mount()})()""")
    pg.wait_for_timeout(900)

    print('\n— sáu màn chính —')
    for v,label in [('home','Nhà'),('quest','Việc'),('battle','Đấu'),('egg','Trứng'),('shop','Shop'),('dex','Khác')]:
        errs.clear()
        pg.evaluate(f"go('{v}')"); pg.wait_for_timeout(700)
        n=pg.evaluate(f"document.getElementById('v-{v}').innerHTML.length")
        ck(f'màn {label}', n>400 and not errs, f'{n} ký tự {errs[:1] if errs else ""}')

    print('\n— tab con —')
    for tab,label in [('quick','Đấu nhanh'),('tower','Leo tháp'),('adv','Phiêu lưu'),
                      ('gear','Trang bị'),('fash','Thời trang'),('team','Tổ đội'),('shop','Quán')]:
        errs.clear()
        pg.evaluate(f"(()=>{{S._btab='{tab}';go('battle')}})()"); pg.wait_for_timeout(600)
        n=pg.evaluate("document.getElementById('v-battle').innerHTML.length")
        ck(label, n>400 and not errs, f'{n} {errs[:1] if errs else ""}')
    for tab,label in [('d','Hằng ngày'),('e','Kỳ ngộ'),('c','Quán ta')]:
        errs.clear()
        pg.evaluate(f"(()=>{{S._qtab='{tab}';go('quest')}})()"); pg.wait_for_timeout(500)
        ck('Việc · '+label, pg.evaluate("document.getElementById('v-quest').innerHTML.length")>400 and not errs)
    for tab,label in [('life','Cuốn đời'),('ops','Quản trị'),('tree','Gia phả'),('know','Tri thức'),('set','Cài đặt')]:
        errs.clear()
        pg.evaluate(f"(()=>{{S._dtab='{tab}';go('dex')}})()"); pg.wait_for_timeout(500)
        ck('Khác · '+label, pg.evaluate("document.getElementById('v-dex').innerHTML.length")>300 and not errs, errs[:1])

    print('\n— hệ chính —')
    errs.clear()
    ck('42 kỹ năng có hiệu ứng riêng',
       pg.evaluate("DB.skills.every(s=>FXG[s.id]&&DB.skillFx[s.id]&&DB.skillFx[s.id].m)"),
       pg.evaluate("new Set(DB.skills.map(s=>FXG[s.id](DB.skillFx[s.id].c))).size")+'/42' if False else pg.evaluate("String(new Set(DB.skills.map(s=>FXG[s.id](DB.skillFx[s.id].c))).size)+'/42'"))
    ck('42 công thức', pg.evaluate("DB.recipes.length")==42)
    ck('19 hạt mầm đủ hình', pg.evaluate("DB.seeds.every(s=>(itemIcon(s.id)||'').includes('<svg'))"))
    ck('25 thẻ quản trị', pg.evaluate("DB.opsCards.length")==25)
    ck('22 thẻ cốt truyện', pg.evaluate("DB.loreOrder.length")==22)
    ck('8 chương Quán ta', pg.evaluate("DB.chapterAll.length")==8)
    ck('tháp 110 tầng', pg.evaluate("DB.tower.floors")==110)
    ck('7 nhánh tiến hoá', pg.evaluate("DB.evoRules.length+DB.evoExtra.length")==7)
    ck('6 linh hồn vùng', pg.evaluate("DB.spirits.length")==6)
    ck('8 mẫu Automa', pg.evaluate("DB.automa.models.length")==8)
    ck('16 mong muốn (13 + 3 theo tính cách)', pg.evaluate("DB.wishes.length")==16)
    ck('6 mốc mở khoá đời', pg.evaluate("Object.keys(DB.lineage.unlocks).length")==6)

    print('\n— chạy thật —')
    errs.clear()
    pg.evaluate("(()=>{S._qtab='d';go('quest')})()"); pg.wait_for_timeout(500)
    c0=pg.evaluate("S.coin"); b0=pg.evaluate("S.pet.bond"); l0=pg.evaluate("S.life.length")
    pg.locator('#v-quest .q').first.click(); pg.wait_for_timeout(900)
    ck('làm nhiệm vụ: xu + gắn bó + mốc đời',
       pg.evaluate("S.coin")>c0 and pg.evaluate("S.pet.bond")>b0 and pg.evaluate("S.life.length")>l0)
    errs.clear()
    pg.evaluate("(()=>{setBSpeed(4);S._btab='quick';go('battle')})()"); pg.wait_for_timeout(600)
    pg.evaluate("runBattle()"); pg.wait_for_timeout(3000)
    ck('đấu nhanh chạy xong', pg.evaluate("!SC.busy") and not errs, errs[:1])
    errs.clear()
    pg.evaluate("(()=>{S._btab='tower';go('battle')})()"); pg.wait_for_timeout(600)
    f0=pg.evaluate("towerState().floor")
    pg.evaluate("doFast(3)"); pg.wait_for_timeout(2500)
    ck('leo tháp chạy', pg.evaluate("towerState().floor")>=f0 and not errs, errs[:1])
    errs.clear()
    pg.evaluate("(()=>{sndInit();musicStart()})()"); pg.wait_for_timeout(1200)
    ck('nhạc chạy, không còn lớp nhiễu', pg.evaluate("SND.playing && !SND.vinyl"))
    pg.evaluate("musicStop()")

    print('\n— lưu và nạp lại —')
    pg.evaluate("save()")
    saved=pg.evaluate("localStorage.getItem('petpocket.v1')")
    ck('ghi được bộ nhớ', bool(saved) and len(saved)>500, str(len(saved or ''))+' ký tự')
    # nạp lại mà KHÔNG xoá bộ nhớ: gỡ init script bằng cách mở trang mới cùng bối cảnh
    pg2=b.new_page(viewport={'width':390,'height':844})
    errs2=[]
    pg2.on('pageerror',lambda e:errs2.append('ERR '+str(e)[:110]))
    pg2.add_init_script("localStorage.setItem('petpocket.v1', %s)" % __import__('json').dumps(saved))
    pg2.goto(url); pg2.wait_for_timeout(1900)
    ck('nạp lại giữ trạng thái', pg2.evaluate("S.onboarded===true && S.coin>0"),
       'xu='+str(pg2.evaluate("S.coin")))
    ck('không lỗi sau nạp lại', not errs2, errs2[:2])
    ck('nhãn phiên bản', 'v1.5' in pg2.evaluate("document.getElementById('hdrsub').textContent"),
       pg2.evaluate("document.getElementById('hdrsub').textContent"))
    pg2.close()

    print('\n— tên và biểu tượng —')
    ck('tiêu đề', pg.title()=='Pet Drink — Scale & Soul', pg.title())
    ck('đầu trang', pg.locator('.hdr h1').inner_text()=='Pet Drink')
    b.close()

print('\n=== KẾT QUẢ: ' + (f'{len(FAIL)} mục HỎNG: {FAIL}' if FAIL else 'toàn bộ đạt') + ' ===')
sys.exit(1 if FAIL else 0)
