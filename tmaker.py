from playwright.sync_api import sync_playwright
import pathlib, sys, json, subprocess
GAME='file://'+str(pathlib.Path('index.html').resolve())
MK='file://'+str(pathlib.Path('phat-hanh.html').resolve())
KEY='/home/claude/keys/private.json'
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
body='M0 -32C26 -32 46 -8 46 20C46 48 26 64 0 64C-26 64 -46 48 -46 20C-46 -8 -26 -32 0 -32Z'
ART=[{'kind':'pet','id':'bi-ngo','name':'Bí Ngô','body':body,'hue':28,'sat':86,'light':54,
      'back':[{'d':'M-4 -32L-3 -46Q2 -50 6 -46L4 -32Z','f':'#3f7a3a','s':'#233b2c','w':2}],
      'marks':[{'d':'M-16 -28Q-24 18 -16 62','f':'none','s':'#b8561a','w':3}]},
     {'kind':'fash','id':'mu','name':'Mũ phù thuỷ','slot':'hat','col':'#3a2a52','paths':[{'d':'M-34 -36L34 -36L2 -96Z','f':'#3a2a52','s':'#1a1226','w':2}]},
     {'kind':'frame','id':'khung','name':'Khung Halloween','edge':'#e07b2a','corner':[{'d':'M0 0L44 0Q20 8 0 44Z','f':'#e07b2a'}],'fall':{'paths':[{'d':'M8 0L16 8L8 16L0 8Z','f':'#3a2a52'}],'n':10,'dur':[6,11]}},
     {'kind':'boss','id':'vua','name':'Vua Bí Ngô','body':body,'hue':18,'sat':80,'light':40}]
PDA=subprocess.run(['node','artpack.js',json.dumps(ART,ensure_ascii=False)],capture_output=True,text=True).stdout
SEEN="S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};"
PLAY="(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;"+SEEN+"S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.coin=500;save();const e=document.getElementById('intro');if(e)e.remove();mount()})()"
with sync_playwright() as pw:
    b=pw.chromium.launch()
    mk=b.new_page(viewport={'width':1280,'height':900}); me=[]
    mk.on('pageerror',lambda e:me.append(str(e)[:140])); mk.on('dialog',lambda d:d.accept())
    mk.goto(MK); mk.wait_for_timeout(700)
    print('— công cụ: khoá —')
    ck('chưa có khoá: ba nút ký đều khoá', all(mk.locator(s).is_disabled() for s in ['#signEv','#signGift','#signKey']))
    mk.set_input_files('#keyfile',KEY); mk.wait_for_timeout(400)
    ck('nạp khoá: khớp với game', 'khớp với game' in mk.locator('#keyst').inner_text())
    print('— thẻ Sự kiện —')
    mk.fill('#name','Halloween ở quán')
    ck('mã định danh tự sinh', mk.input_value('#id')=='halloween-o-quan')
    _d=mk.evaluate("(Date.parse(document.getElementById('end').value)-Date.parse(document.getElementById('start').value))/864e5")
    ck('mặc định kéo dài 30 ngày', abs(_d-30)<0.01, f'{_d} ngày')
    mk.fill('#artin',PDA); mk.click('text=Thêm hình'); mk.wait_for_timeout(500)
    ck('dán mã hình: thêm 4 hình', mk.locator('#arts .art').count()==4, mk.locator('#artmsg').inner_text()[:80])
    ck('xem trước hình vẽ được', mk.locator('#arts .pv svg path').count()>=8)
    ck('pet chưa chọn tác dụng: chưa ký được', 'chưa chọn tác dụng' in mk.locator('#evMsg').inner_text())
    mk.select_option('[data-art="0"]','boxExtra'); mk.wait_for_timeout(200)
    mk.fill('[data-artl="0.join"]','Kẹo hay ghẹo?'); mk.wait_for_timeout(150)
    ck('ô thoại pet sự kiện ghi vào sự kiện', mk.evaluate("buildEv().art[0].lines.join")=='Kẹo hay ghẹo?')
    mk.locator('summary',has_text='Nhiệm vụ').click(); mk.click('text=Thêm nhiệm vụ')
    q=mk.locator('.item.quest').first; q.locator('[data-k="t"]').fill('Làm 1 việc'); q.locator('[data-k="n"]').fill('1')
    q.locator('[data-k="r.fash"]').select_option('mu')
    mk.locator('summary',has_text='Thang quà').click(); mk.click('text=Thêm mốc')
    m=mk.locator('.item.step1').first; m.locator('[data-k="at"]').fill('1'); m.locator('[data-k="m.pet"]').select_option('bi-ngo'); m.locator('[data-k="m.frame"]').select_option('khung')
    mk.fill('#setTitle','Phù thuỷ quán')
    mk.locator('summary',has_text='Boss').click(); mk.check('#bossOn'); mk.wait_for_timeout(100)
    mk.locator('#boss [data-k="name"]').fill('Vua Bí Ngô'); mk.locator('#boss [data-k="art"]').select_option('vua'); mk.locator('#boss [data-k="f.egg"]').select_option('rare')
    mk.wait_for_timeout(300)
    ck('phiếu tóm tắt đủ', all(x in mk.locator('#evSum').inner_text() for x in ['4 hình','Mốc 1','Phù thuỷ quán','Vua Bí Ngô']), mk.locator('#evSum').inner_text()[:90])
    ck('hợp lệ, nút ký mở', not mk.locator('#signEv').is_disabled(), mk.locator('#evMsg').inner_text()[:80])
    snap=mk.evaluate("JSON.stringify(buildEv())"); mk.evaluate("loadEv(JSON.parse(%s))" % json.dumps(snap)); mk.wait_for_timeout(300)
    ck('lưu rồi mở lại bản nháp: giữ nguyên hình và tác dụng', mk.evaluate("JSON.stringify(buildEv())")==snap)
    mk.click('#signEv'); mk.wait_for_timeout(1000); EVC=mk.input_value('#codeEv')
    ck('ký sự kiện', EVC.startswith('PDE'), f'{EVC[:4]} · {len(EVC)} ký tự')
    ck('con dấu', 'sealed' in mk.locator('#tkEv').get_attribute('class'))
    mk.screenshot(path='w_mk_ev.png')
    print('— thẻ Quà tặng —')
    mk.click('.tabs button[data-tab=gift]')
    mk.fill('#gName','Gói tân thủ'); mk.fill('[data-k="x.coin"]','200'); mk.select_option('[data-k="x.egg"]','common')
    mk.select_option('[data-k="x.seed"]','dao'); mk.fill('[data-k="x.seedN"]','5'); mk.wait_for_timeout(200)
    ck('phiếu quà: mã chung', 'Mã chung' in mk.locator('#gtKind').inner_text() and '200 xu' in mk.locator('#gtSum').inner_text())
    mk.click('#signGift'); mk.wait_for_timeout(800); GIFT=mk.input_value('#codeGift'); ck('ký mã quà', GIFT.startswith('PDG'))
    mk.fill('#gTo','abc'); mk.wait_for_timeout(200); ck('mã người chơi sai dạng: chặn ký', mk.locator('#signGift').is_disabled())
    mk.fill('#gTo',''); mk.wait_for_timeout(100)
    print('— thẻ Key —')
    mk.click('.tabs button[data-tab=key]')
    mk.fill('#kName','Lạnh Kaffee'); mk.fill('#kNote','Gói tư vấn 12 tháng'); mk.wait_for_timeout(200)
    ck('key mặc định dùng một năm', 'Dùng tới hết ngày' in mk.locator('#ktExp').inner_text())
    mk.click('#signKey'); mk.wait_for_timeout(800); KEYC=mk.input_value('#codeKey'); ck('ký key', KEYC.startswith('PDK'), f'{len(KEYC)} ký tự')
    ck('sổ key đã cấp ghi lại', 'Lạnh Kaffee' in mk.locator('#keylog').inner_text())
    mk.screenshot(path='w_mk_key.png')
    print('— kiểm mã trong công cụ —')
    for code,want in [(EVC,'Halloween'),(GIFT,'Gói tân thủ'),(KEYC,'Lạnh Kaffee')]:
        mk.fill('#vcode',code); mk.click('text=Kiểm mã'); mk.wait_for_timeout(500)
        ck(f'kiểm {code[:3]}: đọc đúng', want in mk.locator('#vres').inner_text())
    ck('công cụ không lỗi', not me, me[:2])

    print('— mang sang game —')
    pg=b.new_page(viewport={'width':390,'height':844}); ge=[]; pg.on('pageerror',lambda e:ge.append(str(e)[:140]))
    pg.add_init_script("localStorage.clear()"); pg.goto(GAME); pg.wait_for_timeout(1600)
    pg.fill('#lockin',KEYC); pg.click('#lockbtn'); pg.wait_for_timeout(1300)
    ck('key từ công cụ mở được game', pg.locator('#lockscr').count()==0 and pg.evaluate("S.lic.cname")=='Lạnh Kaffee')
    pg.evaluate(PLAY); pg.wait_for_timeout(600)
    r=pg.evaluate(f"(async()=>(await giftRedeem({json.dumps(GIFT)})).ok)()"); ck('mã quà từ công cụ nhận được', r and pg.evaluate("(S.eggs||[]).length")>=1)
    r=pg.evaluate(f"(async()=>(await evImport({json.dumps(EVC)})).ok)()"); ck('sự kiện từ công cụ nhập được', r)
    pg.evaluate("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S._qtab='d';go('quest')})()"); pg.wait_for_timeout(400)
    pg.locator('#v-quest .q').first.click(); pg.wait_for_timeout(500)
    pg.evaluate("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(500)
    for _ in range(6):
        bt=pg.locator('.evcard button:not([disabled])',has_text='Nhận')
        if not bt.count(): break
        bt.first.click(); pg.wait_for_timeout(450); pg.evaluate("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    ck('nhận mũ, khung và pet Bí Ngô', pg.evaluate("fashOwned('ev_halloween_o_quan_mu') && (S.owned||[]).includes('frame:ev_halloween_o_quan_khung') && S.stash.some(p=>p.evfx==='boxExtra')"))
    ck('đủ bộ (1 món): danh hiệu', pg.evaluate("(S.titles||[]).some(t=>t.t==='Phù thuỷ quán')"))
    ck('game không lỗi', not ge, ge[:2])
    print('— bố cục công cụ —')
    for w,h,n in [(390,844,'iPhone'),(820,1180,'iPad dọc'),(1180,820,'iPad ngang')]:
        p2=b.new_page(viewport={'width':w,'height':h}); p2.goto(MK); p2.wait_for_timeout(400)
        res=[]
        for t in ['ev','gift','key']:
            p2.click(f'.tabs button[data-tab={t}]'); p2.wait_for_timeout(100)
            res.append(p2.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
        ck(f'{n}: ba thẻ không tràn ngang', all(res), res); p2.close()
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
