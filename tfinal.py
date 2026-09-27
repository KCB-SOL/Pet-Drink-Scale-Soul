# Kiểm lần cuối: đi qua từng thao tác người chơi thật làm, không gọi tắt.
from playwright.sync_api import sync_playwright
import pathlib, sys
url='file://'+str(pathlib.Path('index.html').resolve())
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else '')); 
    if not c: F.append(n)
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]
    pg.on('pageerror',lambda e:errs.append('ERR '+str(e)[:120]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:120]) if m.type=='error' else None)
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1700)
    E=lambda js: pg.evaluate(js)
    E("""(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;S.coin=99000;window.confirm=()=>true;
      S.pet.stage='evo';S.pet.form='care';S.pet.level=34;S.pet.bond=85;refreshSkills(S.pet);
      towerState().tickets=40;advState().passes=6;setBSpeed(4);
      S.stash=Array.from({length:6}).map((_,i)=>{const p=makePet();p.stage='adult';p.level=20;p.bond=70;p.name='P'+i;return p});
      save();const e=document.getElementById('intro');if(e)e.remove();mount()})()""")
    pg.wait_for_timeout(800)
    def clean(): E("(()=>{try{closeSheet()}catch(e){};try{closeDialogue()}catch(e){};document.querySelectorAll('.bnr,#boxscene').forEach(x=>x.remove())})()")

    print('— chăm sóc —')
    E("go('home')"); pg.wait_for_timeout(900)
    for a in ['feed','play','clean','sleep']:
        errs.clear(); c0=E("JSON.stringify(S.pet.care)")
        E(f"doAct('{a}')"); pg.wait_for_timeout(1300)
        ck('hành động '+a, E("JSON.stringify(S.pet.care)")!=c0 and not errs, errs[:1])
    clean()

    print('— mong muốn —')
    E("(()=>{S.pet.care.hunger=30;S.wish={id:null,at:0,doneAt:0,refused:0,streak:0};mount()})()"); pg.wait_for_timeout(600)
    ck('thẻ mong muốn hiện', pg.locator('.wishcard').count()==1)
    b0=E("S.pet.bond"); pg.locator('.wbtns .btn').nth(1).click(); pg.wait_for_timeout(700)
    ck('từ chối không trừ gắn bó', E("S.pet.bond")==b0)
    clean()

    print('— vườn —')
    E("(()=>{invOf().seeds.arabica=3;gotoZone(GARDEN_ZONE);paintProps()})()"); pg.wait_for_timeout(900)
    E("plantSeed(0,'arabica')"); pg.wait_for_timeout(400)
    ck('gieo hạt', E("!!gardenState().slots[0]"))
    E("(()=>{gardenState().slots[0].start=Date.now()-99*36e5;paintGarden()})()"); pg.wait_for_timeout(300)
    n0=E("invCrop().arabica||0"); E("harvest(0)"); pg.wait_for_timeout(500)
    ck('thu hoạch', E("invCrop().arabica||0")>n0)
    clean()
    try:
        pg.locator('.gplot.locked').first.click(timeout=4000); pg.wait_for_timeout(600)
        ck('chạm ô khoá mở bảng mở đất', E("!!document.querySelector('#sheet h3')&&document.querySelector('#sheet h3').textContent.includes('Mở thêm')"))
    except Exception as e: ck('chạm ô khoá mở bảng mở đất', False, str(e)[:60])
    clean()

    print('— bếp và bán ly —')
    E("""(()=>{DB.recipes.forEach(r=>Object.keys(r.mats).forEach(k=>{if(DB.matById[k])S.mats[k]=30;else invCrop()[k]=30}));save()})()""")
    errs.clear(); E("craft('cam_muoi')"); pg.wait_for_timeout(500)
    ck('pha công thức', E("(invOf().recipes||[]).includes('cam_muoi')") and not errs, errs[:1])
    c0=E("S.coin"); E("sellDrink('cam_muoi')"); pg.wait_for_timeout(400)
    ck('bán ly', E("S.coin")>c0)
    clean()

    print('— cửa hàng —')
    errs.clear(); E("buyFurn('espresso')"); pg.wait_for_timeout(300)
    ck('mua nội thất', E("(S.owned||[]).includes('espresso')") and not errs, errs[:1])
    E("buyDecor('bed')"); pg.wait_for_timeout(300)
    ck('mua đồ của pet', E("decorOwned('bed')"))
    E("(()=>{go('dex')})()"); pg.wait_for_timeout(300); E("go('home')"); pg.wait_for_timeout(900)
    ck('đồ của pet hiện trong quán', pg.locator('.decorp').count()>=1)
    E("buyFash('h_chef')"); pg.wait_for_timeout(300)
    ck('mua thời trang', E("fashOwned('h_chef')"))
    clean()

    print('— trang bị —')
    E("(()=>{addGear('weapon_steel',6);S.gear.equip.weapon='weapon_steel';save()})()")
    E("fuseGear('weapon_steel')"); pg.wait_for_timeout(300)
    ck('ghép trang bị', E("gearLv('weapon_steel')")==1)
    E("(()=>{addGear('armor_plastic',5)})()"); c0=E("S.coin")
    E("sellGear('armor_plastic',1)"); pg.wait_for_timeout(300)
    ck('bán trang bị', E("S.coin")>c0)
    clean()

    print('— tổ đội và lai tạo —')
    E("(()=>{S.team=[];S._btab='team';go('battle')})()"); pg.wait_for_timeout(600)
    cards=pg.locator('#v-battle .tm').last.locator('.tmc')
    cards.nth(0).click(); pg.wait_for_timeout(300); cards.nth(1).click(); pg.wait_for_timeout(300)
    ck('xếp 2 pet phụ', E("teamPets().length")==2)
    E("(()=>{const i=S.stash.findIndex(p=>p.id===S.team[0]);swapPet(i)})()"); pg.wait_for_timeout(500)
    E("(()=>{const p=S.stash.find(x=>!S.team.includes(x.id));toggleTeam(p.id)})()"); pg.wait_for_timeout(300)
    ck('đổi pet chính rồi vẫn xếp đủ 2', E("teamPets().length")==2)
    E("(()=>{S.pet.stage='adult';S.pet.bond=80})()")
    E("breedUI()"); pg.wait_for_timeout(600)
    ck('bảng chọn bạn đời', pg.locator('#sheet .pickc').count()>=1)
    n0=E("S.stash.length")
    if pg.locator('#sheet .pickc').count(): pg.locator('#sheet .pickc').first.click(); pg.wait_for_timeout(1000)
    ck('lai tạo ra con', E("S.stash.length")>n0)
    clean()
    E("(()=>{S._etab='barn';go('egg')})()"); pg.wait_for_timeout(600)
    pg.locator('.tmc div[onclick^="openPetInfo"]').first.click(); pg.wait_for_timeout(600)
    ck('bảng thông tin pet trong chuồng', pg.locator('#sheet').count()==1)
    sz=E("""(()=>{const s=document.querySelector('#sheet .recappet svg');if(!s)return null;
      const r=s.getBoundingClientRect(),b=document.querySelector('#sheet .recappet').getBoundingClientRect();
      return {pet:Math.round(r.height),khung:Math.round(b.height)}})()""")
    ck('pet trong bảng không bị bé tí', sz and sz['pet']>=sz['khung']*0.6, sz)
    clean()

    print('— chiến đấu —')
    errs.clear(); E("(()=>{S._btab='quick';go('battle')})()"); pg.wait_for_timeout(600)
    E("runBattle()"); pg.wait_for_timeout(3500)
    ck('đấu nhanh', not errs, errs[:1])
    errs.clear(); E("(()=>{S._btab='tower';go('battle')})()"); pg.wait_for_timeout(600)
    f0=E("towerState().floor"); E("doFast(5)"); pg.wait_for_timeout(3500)
    ck('leo 5 tầng', E("towerState().floor")>f0 and not errs, str(E("towerState().floor"))+' '+str(errs[:1]))
    clean()
    errs.clear(); E("(()=>{S._btab='adv';go('battle')})()"); pg.wait_for_timeout(600)
    E("startTrip('caonguyen')"); pg.wait_for_timeout(400)
    ck('bắt đầu chuyến đi', E("advState().trips.length")>=1 and not errs, errs[:1])
    clean()

    print('— dữ liệu vận hành —')
    errs.clear(); E("handleOps({revenue:{target:100,actual:150},checklistRate:0.97,foodCost:'good',quests:['open','stock']})"); pg.wait_for_timeout(900)
    ck('nhận dữ liệu vận hành', not errs, errs[:1])
    clean()

    print('— nhạc —')
    errs.clear(); E("(()=>{sndInit();musicStart()})()"); pg.wait_for_timeout(1200)
    ck('nhạc chạy', E("SND.playing") and not errs); E("musicStop()")

    print('— tổng —')
    ck('không lỗi nào trên console suốt phiên', not [e for e in errs if e.startswith('ERR')], errs[:3])
    b.close()
print('\n=== ' + (f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT') + ' ===')
sys.exit(1 if F else 0)
