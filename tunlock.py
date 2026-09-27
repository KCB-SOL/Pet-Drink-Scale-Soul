from playwright.sync_api import sync_playwright
import pathlib, sys
url='file://'+str(pathlib.Path('index.html').resolve())
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
with sync_playwright() as pw:
    b=pw.chromium.launch()
    # ---------- người chơi MỚI, đi qua màn mở đầu thật ----------
    pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    E=lambda j: pg.evaluate(j)
    print('— người chơi mới, ngày 1 —')
    ck('máy mới gặp màn key trước', E("!!document.getElementById('lockscr')"))
    E("(()=>{S.lic={grand:true};document.getElementById('lockscr').remove()})()")
    ck('logo màn mở đầu là pet Matcha', pg.locator('#intro .ilogo svg').count()==1)
    # đi qua màn mở đầu bằng thao tác thật
    for _ in range(12):
        if not pg.locator('#intro').count(): break
        btn=pg.locator('#intro .btn, #intro .pk, #intro .spk, #intro [onclick]').first
        try: btn.click(timeout=1500)
        except Exception: pass
        pg.wait_for_timeout(500)
    if pg.locator('#intro').count():   # còn kẹt thì hoàn tất bằng mã, ghi nhận lại
        E("(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();save();document.getElementById('intro').remove();mount()})()")
        print('  (màn mở đầu hoàn tất bằng mã)')
    pg.wait_for_timeout(900)
    ck('ngày 1', E("dayNo()")==1)
    ck('logo đầu trang là pet Matcha', pg.locator('#brandmark svg').count()==1)
    locked=E("[...document.querySelectorAll('#nav button')].map(b=>b.classList.contains('navlock')?'🔒'+b.textContent.trim():b.textContent.trim())")
    ck('Nhà, Việc, Khác mở · Đấu, Trứng, Shop khoá', locked==['Nhà','Việc','🔒Đấu','🔒Trứng','🔒Shop','Khác'] or all(x.startswith('🔒')==(x.strip('🔒') in ['Đấu','Trứng','Shop']) for x in locked), locked)
    E("go('battle')"); pg.wait_for_timeout(400)
    ck('chạm Đấu khi khoá: không vào', E("VIEW")!='battle', E("VIEW"))
    ck('và có báo khi nào mở', 'ngày 2' in (E("[...document.querySelectorAll('.toast')].map(t=>t.textContent).pop()||''")), E("[...document.querySelectorAll('.toast')].map(t=>t.textContent).pop()||''"))
    E("(()=>{S.wish={id:null,at:0,doneAt:0,refused:0,streak:0};towerState().tickets=5;advState().passes=3})()")
    w=E("(()=>{const out=new Set();for(let i=0;i<60;i++){const x=pickWish();if(x)out.add(x.go)}return [...out]})()")
    ck('mong muốn không dẫn vào tháp, phiêu lưu, trứng', not any(g in w for g in ['tower','adv','egg']), w)
    print('— hướng dẫn —')
    E("(()=>{S.tut={step:2,done:false};save();go('home')})()"); pg.wait_for_timeout(900)
    ck('bước 3 trỏ vào Việc', 'Việc' in (E("(document.getElementById('tutcard')||{}).textContent||''")), (E("(document.getElementById('tutcard')||{}).textContent||''"))[:60])
    pg.locator('#nav button').nth(1).click(); pg.wait_for_timeout(1200)
    ck('mở Việc thì xong hướng dẫn', E("S.tut.done")==True)
    E("(()=>{try{closeSheet()}catch(e){};document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    print('— người hăng hái: làm 3 việc ngay ngày 1 —')
    E("(()=>{S.qset={eod:0};save()})()")  # bộ này không kiểm giờ cuối ngày
    E("go('quest')"); pg.wait_for_timeout(500)
    # bấm như người thật: KHÔNG xoá thông báo bằng mã — xoá thẳng sẽ giết luôn
    # thông báo mình đang muốn kiểm (bài học của chính bộ kiểm này)
    for i in range(3):
        pg.locator('#v-quest .q').nth(i).click(); pg.wait_for_timeout(500)
    pg.wait_for_timeout(300)
    ck('Đấu mở sau 3 việc dù vẫn ngày 1', not E("navLocked('battle')"))
    pg.wait_for_timeout(2400)
    seen_unlock=False
    for _ in range(5):
        if not pg.locator('.bnr').count(): pg.wait_for_timeout(900)
        if not pg.locator('.bnr').count(): break
        if 'VỪA MỞ' in pg.locator('.bnr').inner_text().upper(): seen_unlock=True; break
        pg.locator('.bnr .btn').click(); pg.wait_for_timeout(600)
        E("(()=>{try{closeSheet()}catch(e){}})()"); pg.wait_for_timeout(700)
    ck('có thông báo vừa mở Đấu, không bị đè', seen_unlock)
    pg.screenshot(path='w_unlock.png', clip={'x':0,'y':150,'width':390,'height':520})
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    E("(()=>{S._btab='quick';go('battle')})()"); pg.wait_for_timeout(600)
    tabs=E("[...document.querySelectorAll('#v-battle .cats button')].map(b=>b.textContent.trim())")
    ck('Đấu chỉ hiện Đấu nhanh, Leo tháp + nhãn sắp mở', len(tabs)==3 and '🔒' in tabs[-1], tabs)
    E("(()=>{S._btab='gear';mount()})()"); pg.wait_for_timeout(400)
    ck('tab con khoá thì tự về Đấu nhanh', E("S._btab")=='quick')
    ck('không lỗi', not errs, errs[:2])
    pg.close()

    # ---------- theo ngày ----------
    print('— theo ngày —')
    pg=b.new_page(viewport={'width':390,'height':844}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1500)
    E=lambda j: pg.evaluate(j)
    E("(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.unl={seen:null};unlInit();save();const e=document.getElementById('intro');if(e)e.remove();mount()})()")
    for d in [2,3,4,5]:
        E(f"(()=>{{S.started=Date.now()-{d-1}*864e5-6e4;mount()}})()"); pg.wait_for_timeout(200)
        nav=E("['battle','egg','shop'].filter(v=>!navLocked(v))")
        sub=E("Object.keys(DB.unlockSub).filter(k=>!subLocked(k))")
        print(f'   ngày {d}: mở {nav} · tab con {sub}')
    ck('ngày 5 mở hết', E("['battle','egg','shop'].every(v=>!navLocked(v)) && Object.keys(DB.unlockSub).every(k=>!subLocked(k))"))
    # thông báo lần lượt, không chồng
    shown=[]
    for _ in range(12):
        E("(()=>{document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
        E("unlCheck()"); pg.wait_for_timeout(250)
        n=pg.locator('.bnr').count()
        if not n: break
        shown.append(pg.locator('.bnr').inner_text().split('\n')[1] if '\n' in pg.locator('.bnr').inner_text() else '?')
    ck('cả 8 mục đều được báo, không sót', len(E("S.unl.seen"))==8, f'{len(E("S.unl.seen"))} mục · hiện trong vòng: {len(shown)}')
    pg.close()

    # ---------- người chơi CŨ (ngày 13) ----------
    print('— người chơi cũ, ngày 13 —')
    tmp=b.new_page(); tmp.add_init_script("localStorage.clear()"); tmp.goto(url); tmp.wait_for_timeout(1400)
    save=tmp.evaluate("""(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};
      S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.started=Date.now()-12*864e5;
      delete S.unl;save();return localStorage.getItem('petpocket.v1')})()""")
    tmp.close()
    import json
    pg=b.new_page(viewport={'width':390,'height':844}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
    pg.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(save))
    pg.goto(url); pg.wait_for_timeout(2400)
    E=lambda j: pg.evaluate(j)
    ck('ngày 13', E("dayNo()")==13, E("dayNo()"))
    ck('mọi thứ mở', E("['battle','egg','shop'].every(v=>!navLocked(v)) && Object.keys(DB.unlockSub).every(k=>!subLocked(k))"))
    ck('không bắn loạt thông báo', pg.locator('.bnr').count()==0 and E("BANNER_Q.length")==0)
    ck('không lỗi', not errs, errs[:2])

    print('— bản gọn —')
    E("go('home')"); pg.wait_for_timeout(900)
    ck('trang Nhà không còn nút bong bóng', pg.locator('#deskRow .btn').count()==0)
    ck('không còn ghi chú cửa sổ nổi', 'Cửa sổ nổi tách hẳn' not in E("document.getElementById('v-home').innerHTML"))
    ck('chế độ ngủ đông vẫn còn', pg.locator('#hibRow').count()==1)
    E("(()=>{S._dtab='set';go('dex')})()"); pg.wait_for_timeout(800)
    secs=E("[...document.querySelectorAll('#v-dex h3.sec')].map(h=>h.textContent.trim())")
    print('   mục còn lại:', secs)
    ck('đã gỡ 8 mục', not any(s in secs for s in ['Trên máy tính','Ghi nhận sử dụng','Nhiệm vụ vận hành mỗi ngày','Lượt mở từng trang','Hành động chăm sóc','Cầu nối công cụ vận hành','Lịch sử tài khoản','Chế độ thử']))
    ck('giữ Nhạc của bạn, Sao lưu, Về game', all(s in secs for s in ['Nhạc của bạn','Sao lưu tiến độ','Về game']))
    ck('mã đo đạc vẫn chạy ngầm', E("!!S.tel && typeof S.tel.sessions==='number'"))

    print('— thẻ chia sẻ —')
    # ghi mốc theo đúng trình tự thời gian: ngày gặp nhau là ngày 1
    E("(()=>{S.life=[];const T0=Date.now()-12*864e5;S.started=T0;S.started=Date.now();lifeAdd('born','Gặp '+S.pet.name);S.started=Date.now()-3*864e5;lifeAdd('boss','Hạ được Hắc Tinh Ga');S.started=Date.now()-7*864e5;lifeAdd('evo','Tiến hoá thành Dạng Linh Hồn');S.started=Date.now()-10*864e5;lifeAdd('child','Muối nở ra');S.started=T0;S.pet.bond=88;save();S._dtab='life';go('dex')})()")
    pg.wait_for_timeout(800)
    ck('nút Tạo thẻ chia sẻ', pg.locator('text=Tạo thẻ chia sẻ').count()==1)
    E("(()=>{try{closeSheet()}catch(e){};BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")  # bảng "Hết một ngày" tự mở buổi tối
    pg.locator('text=Tạo thẻ chia sẻ').click(); pg.wait_for_timeout(2500)
    ck('bảng xem trước', pg.locator('#sheet .sharepv').count()==1)
    dim=E("(()=>{const i=document.querySelector('#sheet .sharepv');return i?[i.naturalWidth,i.naturalHeight]:null})()")
    ck('ảnh 1080×1350', dim==[1080,1350], dim)
    ck('dung lượng hợp lý', 50_000 < E("SHARE.blob.size") < 3_000_000, str(round(E("SHARE.blob.size")/1024))+' KB')
    data=E("(async()=>{const r=new FileReader();return await new Promise(ok=>{r.onload=()=>ok(r.result);r.readAsDataURL(SHARE.blob)})})()")
    import base64
    open('w_card.png','wb').write(base64.b64decode(data.split(',')[1]))
    ck('không lỗi', not errs, errs[:2])
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
