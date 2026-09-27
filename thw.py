# Chơi thử trọn sự kiện Halloween 2026, gồm thoại pet sự kiện (ý 5)
from playwright.sync_api import sync_playwright
import pathlib, sys, json, subprocess, datetime
GAME='file://'+str(pathlib.Path('index.html').resolve())
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
draft=json.load(open('nhap-halloween-2026.json'))
CODE=subprocess.run(['node','sign.js','E',json.dumps(draft,ensure_ascii=False)],capture_output=True,text=True).stdout
VN=datetime.timezone(datetime.timedelta(hours=7))
SEEN="S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};"
SETUP="(()=>{S.onboarded=true;S.lic={grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;"+SEEN+"S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.coin=500;S.pet.stage='evo';S.pet.form='care';S.pet.level=30;refreshSkills(S.pet);window.confirm=()=>true;save();const e=document.getElementById('intro');if(e)e.remove();mount()})()"
clean="(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());try{closeSheet()}catch(e){}})()"
toasts="[...document.querySelectorAll('.toast')].map(t=>t.textContent)"
with sync_playwright() as pw:
    b=pw.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},timezone_id='Asia/Ho_Chi_Minh')
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:140]))
    pg.clock.install(time=datetime.datetime(2026,9,28,10,0,tzinfo=VN))
    pg.add_init_script("localStorage.clear()"); pg.goto(GAME); pg.wait_for_timeout(1500)
    E=lambda j: pg.evaluate(j); E(SETUP); pg.wait_for_timeout(500)
    print('— trước 1/10 —')
    r=E(f"(async()=>(await evImport({json.dumps(CODE)})).ok)()"); ck('nhập mã Halloween', r)
    E(clean); ck('ngày 28/9: hiện đếm ngược', 'Bắt đầu sau' in E("evWhen(evState().list['halloween-2026'].d)"), E("evWhen(evState().list['halloween-2026'].d)"))
    ck('chưa nhận quà được', E("(()=>{const c=S.coin;evGift('halloween-2026');return S.coin===c})()"))
    print('— ngày 5/10 —')
    pg.clock.set_fixed_time(datetime.datetime(2026,10,5,19,0,tzinfo=VN)); E("mount()")
    ck('đang diễn ra, còn khoảng 26 ngày', 'Còn 26 ngày' in E("evWhen(evState().list['halloween-2026'].d)"), E("evWhen(evState().list['halloween-2026'].d)"))
    E("evGift('halloween-2026')"); E(clean)
    ck('quà: 150 xu, 1 trứng', E("S.coin")==650 and E("(S.eggs||[]).length")>=1)
    ck('mong muốn Halloween vào vòng chọn', E("(()=>{let n=0;for(let i=0;i<200;i++){const w=pickWish();if(w&&String(w.id).startsWith('ev:halloween-2026'))n++}return n})()")>40)
    ck('pet nói câu Halloween', E("(()=>{const s=new Set();for(let i=0;i<300;i++)s.add(chatPick());return [...s].some(x=>/bí ngô|kẹo|Dơi/.test(x||''))})()"))
    rid='ev_halloween_2026_r1'
    ck('công thức Ca cao gừng thật', E(f"DB.recipeById['{rid}'] && DB.recipeById['{rid}'].name")=='Ca cao gừng thật')
    print('— thang quà —')
    E("(()=>{const e=evState().list['halloween-2026'];e.d.quests.forEach(q=>e.prog[q.id]=q.goal.n);save();S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(500)
    got=0
    for _ in range(16):
        bt=pg.locator('.evcard button:not([disabled])',has_text='Nhận')
        if not bt.count(): break
        bt.first.click(); got+=1; pg.wait_for_timeout(450)
        if pg.locator('.bnr').count() and 'Danh hiệu' in pg.locator('.bnr').inner_text():
            SETNOTE=pg.locator('.bnr').inner_text()
        E(clean)
    ck('nhận đủ 7 nhiệm vụ + 6 mốc', got==13, got)
    ck('khung Đêm Halloween dùng được', E("(S.owned||[]).includes('frame:ev_halloween_2026_dem_halloween')"))
    ck('đủ 4 món thời trang', E("['mu_phu_thuy','khan_choang','gio_keo','canh_doi'].every(k=>fashOwned('ev_halloween_2026_'+k))"))
    ck('danh hiệu Phù thuỷ quán', E("(S.titles||[]).some(t=>t.t==='Phù thuỷ quán')"))
    bn=E("(S.stash||[]).findIndex(p=>p.evpet && p.evpet.aid==='bi-ngo')")
    ck('nhận pet Bí Ngô', bn>=0)
    print('— thoại Bí Ngô (ý 5) —')
    E("(()=>{S.team=[];S._btab='team';go('battle')})()"); pg.wait_for_timeout(400)
    E(f"toggleTeam(S.stash[{bn}].id)"); pg.wait_for_timeout(600)
    ck('vào tổ đội: Bí Ngô nói', any('Kẹo hay ghẹo? Mình theo bạn!' in t for t in E(toasts)), E(toasts)[-1:] )
    # trận thật: pet chính cấp 30 đấu một đối thủ yếu, Bí Ngô trong tổ đội
    E("(()=>{EV_WIN_AT=0;setBSpeed&&setBSpeed(4);S.pet.care.energy=100})()")
    REAL="(async()=>{const foe=tunePet(60,{species:'beano'});foe.name='Đối thủ tập';S._btab='quick';go('battle');const r=battle(S.pet,foe,{team:teamPets()},{});await playBattle(r);return r.winner})()"
    w=E(REAL); pg.wait_for_timeout(1400)
    ck('trận thật có Bí Ngô trong tổ đội: thắng', w=='A', w)
    ck('thắng trận có Bí Ngô: pet chính khen', any('Bí Ngô ném kẹo trúng phóc luôn.' in t for t in E(toasts)), E(toasts)[-2:])
    E(REAL); pg.wait_for_timeout(1400)
    ck('thắng liền trận nữa: không lặp câu khen', sum('ném kẹo' in t for t in E(toasts))<=1)
    ck('đủ bộ: Bí Ngô nói trong thông báo danh hiệu', E("evPetLine(S.stash.find(p=>p.evpet),'set')")=='Đội mũ vào nhìn bạn giống phù thuỷ thật đó!')
    print('— boss Bí Ngô Hương Liệu —')
    E(clean); E("(()=>{S.team=[];setBSpeed&&setBSpeed(4);S.pet.care.energy=100;S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(400)
    E("evBoss('halloween-2026')"); pg.wait_for_timeout(800)
    ck('boss nói câu của nó', 'Mùa thu đóng chai' in (pg.locator('#dlg').inner_text() if pg.locator('#dlg').count() else ''))
    for _ in range(6):
        if pg.locator('#dlg').count(): pg.locator('#dlg').click(); pg.wait_for_timeout(350)
    for _ in range(80):
        pg.wait_for_timeout(250)
        if E("evState().list['halloween-2026'].boss.tries")>=1 and not E("SC.busy"): break
    ck('trận boss chạy xong', E("evState().list['halloween-2026'].boss.tries")==1)
    print('— hết sự kiện —')
    pg.clock.set_fixed_time(datetime.datetime(2026,11,1,9,0,tzinfo=VN)); E(clean); E("mount()")
    ck('1/11: sự kiện đã kết thúc', E("evWhen(evState().list['halloween-2026'].d)")=='Đã kết thúc')
    ck('đồ, khung, pet, công thức vẫn giữ', E(f"fashOwned('ev_halloween_2026_mu_phu_thuy') && (S.owned||[]).includes('frame:ev_halloween_2026_dem_halloween') && S.stash.some(p=>p.evpet) && !!DB.recipeById['{rid}']"))
    ck('không lỗi', not errs, errs[:3])
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
