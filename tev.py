# Kiểm hệ sự kiện từ đầu tới cuối: trang tạo mã → ký → game nhập → chơi.
from playwright.sync_api import sync_playwright
import pathlib, sys, json, subprocess, time
GAME='file://'+str(pathlib.Path('index.html').resolve())
MAKER='file://'+str(pathlib.Path('phat-hanh-su-kien.html').resolve())
KEY='/home/claude/keys/private.json'
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
SEEN="S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};"
SETUP="(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;"+SEEN+"S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.coin=1000;S.pet.stage='evo';S.pet.form='care';S.pet.level=30;refreshSkills(S.pet);window.confirm=()=>true;save();const e=document.getElementById('intro');if(e)e.remove();mount()})()"
def sign_node(obj):
    js=f"""const fs=require('fs');eval(fs.readFileSync('evcore.js','utf8'));
    const k=JSON.parse(fs.readFileSync('{KEY}')).jwk;
    evcSign({json.dumps(obj,ensure_ascii=False)},k).then(c=>process.stdout.write(c));"""
    return subprocess.run(['node','-e',js],capture_output=True,text=True,cwd='.').stdout
def iso(dt_ms): 
    import datetime; return datetime.datetime.fromtimestamp(dt_ms/1000, datetime.timezone(datetime.timedelta(hours=7))).isoformat()
now=time.time()*1000
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    # ================= trang tạo mã =================
    print('— trang tạo mã —')
    mk=b.new_page(viewport={'width':1280,'height':900})
    merr=[]; mk.on('pageerror',lambda e:merr.append(str(e)[:120]))
    mk.goto(MAKER); mk.wait_for_timeout(700)
    ck('chưa có khoá thì nút ký khoá', mk.locator('#signbtn').is_disabled())
    mk.set_input_files('#keyfile', KEY); mk.wait_for_timeout(500)
    ck('nạp khoá: báo khớp với game', 'khớp với game' in mk.locator('#keyst').inner_text(), mk.locator('#keyst').inner_text()[:60])
    mk.fill('#name','Trung Thu ở quán')
    ck('mã định danh tự sinh từ tên', mk.input_value('#id')=='trung-thu-o-quan', mk.input_value('#id'))
    mk.fill('#intro','Rước đèn cùng pet.')
    mk.fill('[data-k="g.coin"]','300'); mk.select_option('[data-k="g.box"]','hiem')
    mk.locator('summary',has_text='Nhiệm vụ sự kiện').click(); mk.locator('button',has_text='Thêm nhiệm vụ').click()
    q=mk.locator('.item.quest').first
    q.locator('[data-k="t"]').fill('Làm 2 việc ở quán'); q.locator('[data-k="n"]').fill('2'); q.locator('[data-k="r.coin"]').fill('200')
    mk.locator('button',has_text='Thêm nhiệm vụ').click()
    q2=mk.locator('.item.quest').nth(1)
    q2.locator('[data-k="t"]').fill('Cho pet ăn 1 lần'); q2.locator('[data-k="type"]').select_option('feed'); q2.locator('[data-k="n"]').fill('1'); q2.locator('[data-k="r.tickets"]').fill('2')
    mk.locator('summary',has_text='Pet muốn gì').click(); mk.locator('button',has_text='Thêm mong muốn').click()
    w=mk.locator('.item.wish').first
    w.locator('[data-k="t"]').fill('Đi rước đèn'); w.locator('[data-k="line"]').fill('Tối nay rước đèn nhé?'); w.locator('[data-k="done"]').select_option('now')
    mk.locator('summary',has_text='Câu pet tự nói').click(); mk.fill('#lines','Trăng hôm nay tròn ghê.\nMình muốn một cái lồng đèn.')
    mk.locator('summary',has_text='Công thức đồ uống').click(); mk.locator('button',has_text='Thêm công thức').click()
    r=mk.locator('.item.recipe').first
    r.locator('[data-k="name"]').fill('Trà Đào Trăng'); r.locator('[data-k="group"]').select_option('chua')
    r.locator('[data-k="m0"]').select_option('dao'); r.locator('[data-k="mn0"]').fill('2')
    r.locator('[data-k="bk"]').select_option('spd'); r.locator('[data-k="bv"]').fill('50')
    mk.locator('summary',has_text='Boss sự kiện').click(); mk.check('#bossOn')
    mk.locator('#boss [data-k="name"]').fill('Thỏ Ngọc Nướng'); mk.locator('#boss [data-k="quote"]').fill('Bánh của ta!')
    mk.locator('#boss [data-k="f.coin"]').fill('500'); mk.locator('#boss [data-k="level"]').select_option('easy')
    mk.wait_for_timeout(300)
    ck('phiếu xem trước cập nhật', 'Trung Thu ở quán' in mk.locator('#tk-name').inner_text() and 'Thỏ Ngọc' in mk.locator('#tk-sum').inner_text())
    ck('tăng 50% bị hạ về 20% và báo lại', 'đã hạ xuống' in mk.locator('#tk-msg').inner_text())
    ck('nút ký mở', not mk.locator('#signbtn').is_disabled())
    mk.locator('#signbtn').click(); mk.wait_for_timeout(1200)
    code=mk.input_value('#code')
    ck('ký ra mã', code.startswith('PDE1.'), f'{len(code)} ký tự')
    ck('con dấu hiện', 'sealed' in mk.locator('#ticket').get_attribute('class'))
    mk.fill('#base','https://vidu.droply.host/index.html'); mk.wait_for_timeout(200)
    link=mk.input_value('#link'); ck('tạo đường dẫn có mã', '#su-kien=PDE1.' in link)
    mk.screenshot(path='w_maker.png', full_page=False)
    mk.fill('#name',''); mk.wait_for_timeout(300)
    ck('xoá tên: báo lỗi, khoá nút ký', mk.locator('#signbtn').is_disabled() and 'Thiếu tên' in mk.locator('#tk-msg').inner_text())
    mk.fill('#name','Trung Thu ở quán'); mk.wait_for_timeout(200)
    mk.fill('#vcode', code); mk.locator('button',has_text='Kiểm mã').click(); mk.wait_for_timeout(700)
    ck('kiểm lại mã trong trang tạo mã', 'Trung Thu ở quán' in mk.locator('#vres').inner_text())
    ck('trang tạo mã không lỗi', not merr, merr[:2])

    # ================= game =================
    print('— game nhập mã —')
    pg=b.new_page(viewport={'width':390,'height':844}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:140]))
    pg.add_init_script("localStorage.clear()")
    pg.goto(GAME); pg.wait_for_timeout(1600)
    E=lambda j: pg.evaluate(j)
    E(SETUP); pg.wait_for_timeout(800)
    E("(()=>{S._dtab='set';go('dex')})()"); pg.wait_for_timeout(700)
    ck('Cài đặt có mục Sự kiện', pg.locator('#v-dex .evinput').count()==1)
    pg.locator('#v-dex .evinput').fill(code)
    pg.locator('#v-dex button',has_text='Nhập mã').click(); pg.wait_for_timeout(1800)
    ck('nhập thành công, có thông báo', pg.locator('.bnr').count()==1 and 'Trung Thu' in pg.locator('.bnr').inner_text())
    ck('sự kiện đang diễn ra', E("evLive().length")==1)
    pg.locator('.bnr .btn').click(); pg.wait_for_timeout(1200)
    ck('bấm thông báo mở tab Sự kiện', E("VIEW")=='quest' and pg.locator('.evcard').count()==1)
    pg.screenshot(path='w_evtab.png', clip={'x':0,'y':110,'width':390,'height':700})
    c0=E("S.coin"); b0=E("encState().boxes.length")
    pg.locator('.evcard .evrow').first.locator('button').click(); pg.wait_for_timeout(700)
    ck('nhận quà: +300 xu, +1 hộp bạc', E("S.coin")-c0==300 and E("encState().boxes.length")==b0+1)
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[]})()")
    ck('không nhận quà lần hai', E("(()=>{const c=S.coin;evGift('trung-thu-o-quan');return S.coin===c})()"))
    print('— chơi sự kiện bằng hành động thật —')
    E("(()=>{S._qtab='d';go('quest')})()"); pg.wait_for_timeout(500)
    for i in range(2): pg.locator('#v-quest .q').nth(i).click(); pg.wait_for_timeout(500)
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[]})()")
    ck('làm 2 việc vận hành → nhiệm vụ đủ', E("evState().list['trung-thu-o-quan'].prog.q1")==2)
    E("(()=>{go('home')})()"); pg.wait_for_timeout(700)
    E("(()=>{S.pet.care.hunger=30;SC.busy=false;doAct('feed')})()")
    for _ in range(40):
        pg.wait_for_timeout(200)
        if E("evState().list['trung-thu-o-quan'].prog.q2||0")>=1: break
    ck('cho ăn → nhiệm vụ thứ hai đủ', E("evState().list['trung-thu-o-quan'].prog.q2||0")==1)
    E("(()=>{S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(600)
    c0=E("S.coin"); t0=E("towerState().tickets")
    btns=pg.locator('.evcard .evrow button:not([disabled])')
    n=btns.count()
    for i in range(n): pg.locator('.evcard .evrow button:not([disabled])').first.click(); pg.wait_for_timeout(500); E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[]})()")
    ck('nhận thưởng nhiệm vụ: +200 xu, +2 vé', E("S.coin")-c0==200 and E("towerState().tickets")-t0==2, f'xu +{E("S.coin")-c0}, vé +{E("towerState().tickets")-t0}')
    ck('mong muốn sự kiện vào vòng chọn', E("DB.wishes.some(w=>w.id==='ev:trung-thu-o-quan:w1')"))
    ev_w=E("(()=>{let n=0;for(let i=0;i<300;i++){const w=pickWish();if(w&&w.kind==='event')n++}return n})()")
    ck('mong muốn sự kiện được ưu tiên', ev_w>60, f'{ev_w}/300')
    cl=E("(()=>{const s=new Set();for(let i=0;i<200;i++){const l=chatPick();if(l)s.add(l)}return [...s]})()")
    ck('pet nói câu sự kiện', 'Trăng hôm nay tròn ghê.' in cl)
    rid='ev_trung_thu_o_quan_r1'
    ck('công thức sự kiện có trong game', E(f"!!DB.recipeById['{rid}']"))
    ck('tăng tốc độ bị hạ về 20%', E(f"DB.recipeById['{rid}'].buff.spd")==1.2)
    E(f"(()=>{{invCrop().dao=10;craft('{rid}')}})()"); pg.wait_for_timeout(400)
    ck('pha được công thức sự kiện', E(f"(invOf().recipes||[]).includes('{rid}')"))
    print('— boss sự kiện —')
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[];setBSpeed&&setBSpeed(4);S.pet.care.energy=100;S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(500)
    ck('nút đấu boss 3/3', '3/3' in pg.locator('.evboss button').inner_text())
    E("evBoss('trung-thu-o-quan')"); pg.wait_for_timeout(800)
    for _ in range(6):
        if pg.locator('#dlg').count(): pg.locator('#dlg').click(); pg.wait_for_timeout(350)
    for _ in range(80):
        pg.wait_for_timeout(250)
        if E("evState().list['trung-thu-o-quan'].boss.tries")>=1 and not E("SC.busy"): break
    pg.wait_for_timeout(1500)
    ck('trận boss chạy, trừ một lượt', E("evState().list['trung-thu-o-quan'].boss.tries")==1)
    ck('không lỗi trong trận boss', not errs, errs[:2])
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[]})()")
    print('— nhập lại, cập nhật, giả mạo —')
    E("(()=>{S._dtab='set';go('dex')})()"); pg.wait_for_timeout(500)
    r=E(f"(async()=>await evImport({json.dumps(code)}))()"); ck('nhập lại cùng mã: báo đã có', not r['ok'] and 'đã có' in r['msg'])
    parts=code.split('.'); import base64
    raw=json.loads(base64.urlsafe_b64decode(parts[1]+'='*(-len(parts[1])%4)).decode())
    raw2=dict(raw); raw2['gift']={'coin':3000}
    forged=parts[0]+'.'+base64.urlsafe_b64encode(json.dumps(raw2,ensure_ascii=False).encode()).decode().rstrip('=')+'.'+parts[2]
    r=E(f"(async()=>await evImport({json.dumps(forged)}))()"); ck('sửa quà thành 3000 xu: bị từ chối', not r['ok'], r['msg'][:60])
    raw3=dict(raw); raw3['rev']=2; raw3['name']='Trung Thu ở quán (bản 2)'
    r=E(f"(async()=>await evImport({json.dumps(sign_node(raw3))}))()")
    ck('bản 2: cập nhật, giữ tiến độ', r['ok'] and E("evState().list['trung-thu-o-quan'].claimed.length")==2 and E("evState().list['trung-thu-o-quan'].gift")==True, r['msg'][:60])
    evil=dict(raw); evil['id']='xss-test'; evil['name']='<img src=x onerror="window.PWN=1">Lừa'; evil['intro']='<b>đậm</b>'
    r=E(f"(async()=>await evImport({json.dumps(sign_node(evil))}))()")
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[];S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(700)
    ck('chữ có thẻ HTML được thoát, không chạy', E("!window.PWN") and pg.locator('#v-quest img[src="x"]').count()==0 and '&lt;img' in E("document.getElementById('v-quest').innerHTML"))
    print('— thời gian —')
    soon=dict(raw); soon['id']='sap-toi'; soon['name']='Sắp tới'; soon['start']=iso(now+2*864e5); soon['end']=iso(now+5*864e5)
    over=dict(raw); over['id']='da-qua'; over['name']='Đã qua'; over['start']=iso(now-9*864e5); over['end']=iso(now-2*864e5)
    E(f"(async()=>{{await evImport({json.dumps(sign_node(soon))});await evImport({json.dumps(sign_node(over))})}})()"); pg.wait_for_timeout(300)
    E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove());BANNER_Q=[]})()")
    ck('sự kiện sắp tới: hiện đếm ngược', 'Bắt đầu sau' in E("evWhen(evState().list['sap-toi'].d)"), E("evWhen(evState().list['sap-toi'].d)"))
    ck('sự kiện sắp tới: chưa nhận quà được', E("(()=>{const c=S.coin;evGift('sap-toi');return S.coin===c})()"))
    E("(()=>{try{closeSheet()}catch(e){};BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S._qtab='d';go('quest')})()"); pg.wait_for_timeout(500)
    p0=E("JSON.stringify(evState().list['da-qua'].prog)")
    pg.locator('#v-quest .q').nth(3).click(); pg.wait_for_timeout(400)
    ck('sự kiện đã qua: không đếm tiến độ', E("JSON.stringify(evState().list['da-qua'].prog)")==p0)
    ck('sự kiện đã qua không hiện ở tab', E("!evShown().some(e=>e.d.id==='da-qua')"))
    print('— lưu và nạp lại —')
    E("save()"); saved=E("localStorage.getItem('petpocket.v1')")
    pg2=b.new_page(viewport={'width':390,'height':844}); e2=[]
    pg2.on('pageerror',lambda e:e2.append(str(e)[:140]))
    pg2.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(saved))
    pg2.goto(GAME); pg2.wait_for_timeout(2000)
    ck('nạp lại: sự kiện và tiến độ còn nguyên', pg2.evaluate("evState().list['trung-thu-o-quan'].claimed.length")==2)
    ck('nạp lại: công thức sự kiện vẫn tra được', pg2.evaluate(f"!!DB.recipeById['{rid}']"))
    ck('nạp lại: không lỗi', not e2, e2[:2])
    print('— mở bằng đường dẫn —')
    pg3=b.new_page(viewport={'width':390,'height':844}); e3=[]
    pg3.on('pageerror',lambda e:e3.append(str(e)[:140]))
    pg3.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(saved.replace('trung-thu-o-quan','khac-id')))
    pg3.goto(GAME+'#su-kien='+link.split('#su-kien=')[1]); pg3.wait_for_timeout(3500)
    ck('đường dẫn tự nhập mã', pg3.evaluate("!!evState().list['trung-thu-o-quan']"))
    ck('đường dẫn được xoá khỏi thanh địa chỉ', '#su-kien' not in pg3.url)
    ck('không lỗi', not e3, e3[:2])
    ck('game không lỗi suốt phiên', not [e for e in errs], errs[:3])
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
