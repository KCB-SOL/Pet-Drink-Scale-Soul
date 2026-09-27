from playwright.sync_api import sync_playwright
import pathlib, sys, json, subprocess, time, datetime
GAME='file://'+str(pathlib.Path('index.html').resolve())
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
def sign(T,obj): return subprocess.run(['node','sign.js',T,json.dumps(obj,ensure_ascii=False)],capture_output=True,text=True).stdout
VN=datetime.timezone(datetime.timedelta(hours=7))
iso=lambda d: (datetime.datetime.now(VN)+datetime.timedelta(days=d)).isoformat()
SEEN="S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};"
PLAY="(()=>{S.onboarded=true;S.qset={eod:0};S.started=Date.now()-30*864e5;"+SEEN+"S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.coin=2000;S.pet.stage='evo';S.pet.form='care';S.pet.level=30;refreshSkills(S.pet);window.confirm=()=>true;save();const e=document.getElementById('intro');if(e)e.remove();mount()})()"
KEY=sign('K',{'cid':'lanh-kaffee','cname':'Lạnh Kaffee','exp':iso(365),'iat':iso(0)})
KEY_OLD=sign('K',{'cid':'cu','cname':'Quán Cũ','exp':iso(-3),'iat':iso(-400)})
KEY_SOON=sign('K',{'cid':'sap-het','cname':'Quán Sắp Hết','exp':iso(3),'iat':iso(0)})
body='M0 -32C26 -32 46 -8 46 20C46 48 26 64 0 64C-26 64 -46 48 -46 20C-46 -8 -26 -32 0 -32Z'
EV={'id':'halloween-thu','rev':1,'name':'Halloween thử','start':iso(-1),'end':iso(29),
 'art':[{'kind':'pet','id':'bi-ngo','name':'Bí Ngô','body':body,'belly':{'cx':0,'cy':38,'rx':24,'ry':15},'faceY':12,'hue':28,'sat':86,'light':54,
         'back':[{'d':'M-4 -32L-3 -46Q2 -50 6 -46L4 -32Z','f':'#3f7a3a','s':'#233b2c','w':2}],
         'marks':[{'d':'M-16 -28Q-24 18 -16 62','f':'none','s':'#b8561a','w':3},{'d':'M16 -28Q24 18 16 62','f':'none','s':'#b8561a','w':3}],'fx':'boxExtra'},
        {'kind':'fash','id':'mu','name':'Mũ phù thuỷ','slot':'hat','col':'#3a2a52','paths':[{'d':'M-34 -36L34 -36L2 -96Z','f':'#3a2a52','s':'#1a1226','w':2}]},
        {'kind':'fash','id':'ao','name':'Áo choàng dơi','slot':'back','col':'#2a1e3a','paths':[{'d':'M-40 -10Q-58 30 -44 64L44 64Q58 30 40 -10Z','f':'#2a1e3a','s':'#120a1c','w':2}]},
        {'kind':'frame','id':'khung','name':'Khung Halloween','edge':'#e07b2a','corner':[{'d':'M0 0L44 0Q20 8 0 44Z','f':'#e07b2a'}],'fall':{'paths':[{'d':'M8 0L16 8L8 16L0 8Z','f':'#3a2a52'}],'n':10,'dur':[6,11]}},
        {'kind':'boss','id':'vua','name':'Vua Bí Ngô','body':body,'hue':18,'sat':80,'light':40}],
 'quests':[{'id':'q1','t':'Làm 1 việc','goal':{'type':'quest','n':1},'reward':{'coin':50}},
           {'id':'q2','t':'Làm 2 việc','goal':{'type':'quest','n':2},'reward':{'fash':'mu'}},
           {'id':'q3','t':'Làm 3 việc','goal':{'type':'quest','n':3},'reward':{'fash':'ao'}}],
 'ladder':[{'at':1,'reward':{'frame':'khung'}},{'at':3,'reward':{'pet':'bi-ngo'}}],
 'setTitle':'Phù thuỷ quán','gift':{'egg':'common','frame':'tet'},
 'boss':{'name':'Vua Bí Ngô','art':'vua','level':'easy','perDay':3,'first':{'coin':300},'win':{'coin':50}}}
EVCODE=sign('E',EV)
with sync_playwright() as pw:
    b=pw.chromium.launch()
    # ================= KEY =================
    print('— key mở game —')
    pg=b.new_page(viewport={'width':390,'height':844}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:140]))
    pg.add_init_script("localStorage.clear()"); pg.goto(GAME); pg.wait_for_timeout(1600)
    E=lambda j: pg.evaluate(j)
    ck('máy mới: hiện màn nhập key', pg.locator('#lockscr').count()==1)
    ck('logo pet Matcha trên màn key', pg.locator('#lockscr .ilogo svg').count()==1)
    def try_key(code):
        pg.fill('#lockin', code); pg.click('#lockbtn'); pg.wait_for_timeout(1200)
        return pg.locator('#lockerr').inner_text() if pg.locator('#lockscr').count() else 'ĐÃ MỞ'
    ck('gõ bậy: báo lỗi, không mở', 'không phải mã' in try_key('abc123').lower())
    ck('dán mã sự kiện vào ô key: báo đúng loại', 'mã sự kiện' in try_key(EVCODE))
    ck('dán key hết hạn: báo ngày hết hạn', 'hết hạn' in try_key(KEY_OLD))
    swapped=EVCODE.replace('PDE2','PDK2').replace('PDE1','PDK1')
    ck('đổi tiền tố mã sự kiện thành key: bị bắt', 'không khớp' in try_key(swapped))
    ck('key đúng: mở game', try_key(KEY)=='ĐÃ MỞ')
    ck('lưu tên khách hàng', E("S.lic.cname")=='Lạnh Kaffee')
    E(PLAY); pg.wait_for_timeout(700); saved=E("localStorage.getItem('petpocket.v1')")
    pg2=b.new_page(); pg2.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(saved)); pg2.goto(GAME); pg2.wait_for_timeout(2200)
    ck('mở lại: không hỏi key nữa', pg2.locator('#lockscr').count()==0)
    pg2.evaluate("(()=>{S._dtab='set';go('dex')})()"); pg2.wait_for_timeout(600)
    ck('Cài đặt ghi bản quyền', 'Lạnh Kaffee' in pg2.locator('#v-dex').inner_text())
    pg2.close()
    exp=json.loads(saved); exp['lic']={'code':KEY_OLD.strip(),'cid':'cu','cname':'Quán Cũ','exp':0,'at':0}
    pg3=b.new_page(); pg3.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(json.dumps(exp))); pg3.goto(GAME); pg3.wait_for_timeout(2400)
    ck('key hết hạn: khoá lại', pg3.locator('#lockscr').count()==1 and 'hết hạn' in pg3.locator('#lockscr').inner_text())
    ck('key hết hạn: tiến độ vẫn còn', pg3.evaluate("S.coin")==2000)
    pg3.fill('#lockin',KEY); pg3.click('#lockbtn'); pg3.wait_for_timeout(1300)
    ck('nhập key mới: chơi tiếp', pg3.locator('#lockscr').count()==0 and pg3.evaluate("S.coin")==2000); pg3.close()
    soon=json.loads(saved); soon['lic']={'code':KEY_SOON.strip(),'cid':'sap-het','cname':'Quán Sắp Hết','exp':0,'at':0}
    pg4=b.new_page(); pg4.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(json.dumps(soon))); pg4.goto(GAME); pg4.wait_for_timeout(3600)
    ck('sắp hết hạn: nhắc trước', any('hết hạn' in t for t in pg4.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent)")) or 'hết hạn' in pg4.evaluate("document.body.innerText")); pg4.close()
    old=json.loads(saved); old.pop('lic',None)
    pg5=b.new_page(); pg5.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(json.dumps(old))); pg5.goto(GAME); pg5.wait_for_timeout(2000)
    ck('người chơi từ bản trước: được miễn key', pg5.locator('#lockscr').count()==0 and pg5.evaluate("!!(S.lic&&S.lic.grand)")); pg5.close()

    # ================= MÃ QUÀ =================
    print('— mã quà —')
    pid=E("playerId()"); ck('mã người chơi dạng XXXX-XXXX', len(pid)==9 and pid[4]=='-', pid)
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    GIFT=sign('G',{'id':'tan-thu','name':'Gói tân thủ','reward':{'coin':200,'egg':'common','seeds':{'dao':5}}})
    c0,e0,s0=E("S.coin"),E("(S.eggs||[]).length"),E("invOf().seeds.dao||0")
    r=E(f"(async()=>{{const r=await giftRedeem({json.dumps(GIFT)});return {{ok:r.ok,msg:r.msg}}}})()")
    ck('gói tân thủ: 200 xu, 1 trứng, 5 hạt đào', r['ok'] and E("S.coin")-c0==200 and E("(S.eggs||[]).length")==e0+1 and E("invOf().seeds.dao||0")-s0==5, r.get('msg',''))
    r=E(f"(async()=>(await giftRedeem({json.dumps(GIFT)})).msg)()"); ck('nhận lần hai: bị chặn', 'rồi' in r, r)
    OTHER=sign('G',{'id':'rieng-1','name':'Quà riêng','to':'ABCD-EFGH','reward':{'coin':100}})
    r=E(f"(async()=>(await giftRedeem({json.dumps(OTHER)})).msg)()"); ck('quà riêng của người khác: bị chặn', 'người chơi khác' in r, r)
    MINE=sign('G',{'id':'rieng-2','name':'Quà riêng','to':pid,'reward':{'coin':100}})
    r=E(f"(async()=>(await giftRedeem({json.dumps(MINE)})).ok)()"); ck('quà riêng đúng người: nhận được', r)
    EXPG=sign('G',{'id':'het-han','name':'Quà cũ','until':iso(-1),'reward':{'coin':100}})
    r=E(f"(async()=>(await giftRedeem({json.dumps(EXPG)})).msg)()"); ck('quà hết hạn: bị chặn', 'hết hạn' in r, r)
    E("(()=>{S._dtab='set';go('dex')})()"); pg.wait_for_timeout(500)
    GIFT2=sign('G',{'id':'tang-ve','name':'Tặng vé','reward':{'tickets':2}})
    pg.locator('#v-dex .evinput').fill(GIFT2); pg.locator('#v-dex button',has_text='Nhập mã').click(); pg.wait_for_timeout(1500)
    ck('dán mã quà vào ô chung trong Cài đặt: nhận được', pg.locator('.bnr').count()==1 and 'Tặng vé' in pg.locator('.bnr').inner_text())
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")

    # ================= SỰ KIỆN CÓ HÌNH =================
    print('— sự kiện có hình —')
    import base64 as _b
    _raw=len(json.dumps(dict(EV,t='event'),ensure_ascii=False).encode())
    ck('nén đúng ngưỡng: dưới 2.500 byte không nén, trên thì nén', EVCODE.startswith('PDE2')==(_raw>2500), f'{_raw} byte → {EVCODE[:4]} · {len(EVCODE)} ký tự')
    r=E(f"(async()=>{{const r=await evImport({json.dumps(EVCODE)});return {{ok:r.ok,msg:r.msg}}}})()"); ck('nhập sự kiện có hình', r['ok'], r['msg'])
    sid='ev_halloween_thu_bi_ngo'
    ck('loài Bí Ngô được đăng ký', E(f"!!DB.species['{sid}'] && !!BODY['{sid}']"))
    ck('Bí Ngô không nằm trong danh sách nở trứng', E(f"!DB.speciesList.includes('{sid}')"))
    svg=E(f"(()=>{{const p=makePet({{species:'{sid}'}});p.dna.hue=28;return renderPet(p,{{static:1}})}})()")
    ck('vẽ Bí Ngô: có thân, gân, cuống', body.split('C')[0] in svg and '#b8561a' in svg and '#3f7a3a' in svg)
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    E("evGift('halloween-thu')"); pg.wait_for_timeout(400); E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    ck('sửa lỗi v1.3: nhận khung lễ là dùng được ngay', E("(S.owned||[]).includes('frame:tet')"))
    ck('đồ sự kiện chưa có: không hiện trong phòng thay đồ', E("(()=>{S._btab='fash';go('battle');return !document.getElementById('v-battle').innerHTML.includes('Mũ phù thuỷ')})()"))
    ck('không mua được đồ sự kiện', E("(()=>{const n=fashState().owned.length;buyFash('ev_halloween_thu_mu');return fashState().owned.length===n})()"))
    ck('hộp bí ẩn không bốc ra đồ sự kiện', E("!DB.fashion.filter(f=>!fashOwned(f.id)&&fashUnlocked(f)).some(f=>f.ev)"))
    ck('không mua được khung sự kiện', E("(()=>{const c=S.coin;buyFrame('ev_halloween_thu_khung');return S.coin===c && !(S.owned||[]).includes('frame:ev_halloween_thu_khung')})()"))
    E("(()=>{S._qtab='d';go('quest')})()"); pg.wait_for_timeout(400)
    for i in range(3): pg.locator('#v-quest .q').nth(i).click(); pg.wait_for_timeout(450)
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S._qtab='ev';go('quest')})()"); pg.wait_for_timeout(600)
    ck('thang quà hiện', pg.locator('.evlad .evrow').count()==2)
    for _ in range(8):
        btn=pg.locator('.evcard button:not([disabled])',has_text='Nhận')
        if not btn.count(): break
        btn.first.click(); pg.wait_for_timeout(450); E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove())})()")
    ck('nhận đủ: khung sự kiện dùng được', E("(S.owned||[]).includes('frame:ev_halloween_thu_khung')"))
    ck('nhận đủ: hai món thời trang', E("fashOwned('ev_halloween_thu_mu') && fashOwned('ev_halloween_thu_ao')"))
    ck('đủ bộ: có danh hiệu', E("(S.titles||[]).some(t=>t.t==='Phù thuỷ quán')"))
    ck('nhận pet Bí Ngô ở mốc cuối', E(f"(S.stash||[]).some(p=>p.species==='{sid}' && p.evpet)"))
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S._btab='fash';go('battle')})()"); pg.wait_for_timeout(500)
    ck('phòng thay đồ: hiện đồ sự kiện đã có và danh hiệu', 'Mũ phù thuỷ' in E("document.getElementById('v-battle').innerHTML") and 'Phù thuỷ quán' in pg.locator('#v-battle').inner_text())
    E("(()=>{fashState().equip.hat='ev_halloween_thu_mu';fashState().equip.back='ev_halloween_thu_ao';save();go('home')})()"); pg.wait_for_timeout(1200)
    pg.screenshot(path='w_hl_home.png', clip={'x':0,'y':100,'width':390,'height':260})
    print('— pet sự kiện —')
    i=E(f"(S.stash||[]).findIndex(p=>p.species==='{sid}')")
    ck('không làm pet chính được', E(f"(()=>{{const id=S.pet.id;swapPet({i});return S.pet.id===id}})()"))
    ck('không lai tạo được', 'không lai tạo' in (E(f"breedOk(S.stash[{i}])") or ''))
    ck('không tiến hoá', E(f"(()=>{{const p=S.stash[{i}];p.level=40;p.born=Date.now()-30*864e5;return checkStage(p)===null && !p.form}})()"))
    E(f"(()=>{{S.team=[S.stash[{i}].id];save()}})()")
    picks=E("(()=>{const before=DB.box.thuong.picks;const out=rollBox('thuong');return [before,out.length,DB.box.thuong.picks]})()")
    ck('tác dụng: hộp bí ẩn ra thêm một món', picks[1]==picks[0]+1 and picks[2]==picks[0], picks)
    wst=E("""(()=>{const a=makePet({species:'automa'});a.id='am6';a.model='am06';S.stash.push(a);
      const bp=S.stash.find(p=>p.evpet);bp.evfx='waste';S.team=['am6',bp.id];const v=automaPerk('waste');bp.evfx='boxExtra';return v})()""")
    ck('Automa + pet sự kiện cùng tác dụng: lấy mạnh nhất, không cộng dồn', abs(wst-0.30)<1e-9, wst)
    print('— boss có hình, nạp lại, mã cũ —')
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());S.team=[];setBSpeed&&setBSpeed(4);S.pet.care.energy=100})()")
    E("evBoss('halloween-thu')"); pg.wait_for_timeout(800)
    for _ in range(6):
        if pg.locator('#dlg').count(): pg.locator('#dlg').click(); pg.wait_for_timeout(350)
    for _ in range(80):
        pg.wait_for_timeout(250)
        if E("evState().list['halloween-thu'].boss.tries")>=1 and not E("SC.busy"): break
    ck('đấu boss có hình riêng: chạy, không lỗi', E("evState().list['halloween-thu'].boss.tries")==1 and not errs, errs[:2])
    E("(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());save()})()"); saved2=E("localStorage.getItem('petpocket.v1')")
    pg6=b.new_page(viewport={'width':390,'height':844}); e6=[]; pg6.on('pageerror',lambda e:e6.append(str(e)[:140]))
    pg6.add_init_script("localStorage.setItem('petpocket.v1', %s)" % json.dumps(saved2)); pg6.goto(GAME); pg6.wait_for_timeout(2200)
    ck('nạp lại: Bí Ngô vẽ được', pg6.evaluate(f"(()=>{{const p=S.stash.find(x=>x.species==='{sid}');return !!p && renderPet(p,{{static:1}}).includes('#b8561a')}})()"))
    ck('nạp lại: đồ sự kiện còn trong phòng thay đồ', pg6.evaluate("fashOwned('ev_halloween_thu_mu') && !!DB.fashById['ev_halloween_thu_mu']"))
    ck('nạp lại: khung sự kiện vẽ được', pg6.evaluate("(()=>{S.frame='ev_halloween_thu_khung';paintFrame();return !!document.querySelector('#stage .frm')})()"))
    ck('nạp lại: không lỗi', not e6, e6[:2]); pg6.close()
    old_code=open('ma-thu.txt').read()
    r=E(f"(async()=>(await evImport({json.dumps(old_code)})).ok)()"); ck('mã sự kiện v1.3 vẫn nhập được', r)
    ck('không lỗi suốt phiên', not errs, errs[:3])
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
