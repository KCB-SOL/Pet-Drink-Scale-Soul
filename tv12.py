from playwright.sync_api import sync_playwright
import pathlib, sys, json, collections
url='file://'+str(pathlib.Path('index.html').resolve())
F=[]
def ck(n,c,x=''):
    print(('  OK   ' if c else '  HỎNG ')+n+(' · '+str(x) if x!='' else ''))
    if not c: F.append(n)
SEEN="S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};"
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:140]))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    E=lambda j: pg.evaluate(j)
    E("(()=>{S.onboarded=true;S.qset={eod:0};S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;"+SEEN+"S.opsSeen=DB.opsCards.map(c=>c.id);S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];S.npc={met:true,revealed:true};S.tut.done=true;S.coin=9000;window.confirm=()=>true;save();const e=document.getElementById('intro');if(e)e.remove();go('home')})()")
    pg.wait_for_timeout(900)
    clean="(()=>{BANNER_Q=[];document.querySelectorAll('.bnr').forEach(x=>x.remove());try{closeSheet()}catch(e){}})()"

    print('— 1. thẻ mong muốn —')
    E("(()=>{S.pet.pers='curious';S.pet.care.hunger=30;S.wish={id:null,at:0};mount()})()"); pg.wait_for_timeout(700)
    ck('có dòng hành động, câu nói, chip', pg.locator('.wishcard .wact').count()==1 and pg.locator('.wishcard .wquote').count()==1 and pg.locator('.wishcard .wc').count()>=1)
    ck('hiện tính cách', 'tò mò' in pg.locator('.wishcard .wpers').inner_text().lower())
    print('   ', pg.locator('.wishcard .wact').inner_text(), '|', pg.locator('.wishcard .wquote').inner_text()[:50], '|', pg.evaluate("[...document.querySelectorAll('.wishcard .wc')].map(e=>e.textContent)"))
    pg.screenshot(path='w_wish.png', clip={'x':0,'y':pg.locator('.wishcard').bounding_box()['y']-8,'width':390,'height':pg.locator('.wishcard').bounding_box()['height']+16})
    # thưởng có thật: mong muốn ăn → cho ăn
    E("(()=>{S.wish={id:'w_feed',at:Date.now()};S.pet.care.hunger=30})()")
    b0=E("S.pet.bond"); l0=E("S.life.filter(e=>e.k==='wish').length"); c0=E("S.wish.count||0")
    E("(()=>{SC.busy=false;doAct('feed')})()")
    # pet đi bộ vào bếp: 2,3 giây nếu đứng sẵn ở bếp, gần 5 giây nếu ở khu xa — chờ tới khi xong
    for _ in range(60):
        pg.wait_for_timeout(200)
        if E("(S.wish.count||0)")>c0: break
    pg.wait_for_timeout(300)
    ck('ăn đúng mong muốn: được thưởng thật', E("S.wish.count||0")==c0+1 and E("S.pet.bond")-b0>=4 and E("S.life.filter(e=>e.k==='wish').length")==l0+1, f'gắn bó +{round(E("S.pet.bond")-b0,1)} (4 từ mong muốn + phần của bữa ăn)')
    ck('chip Kỷ niệm tắt khi hôm nay đã có', E("wishMemFresh()")==False)
    for key,wid,setup in [('now','w_sit','S.pet.bond=80;S.pet.care.happy=80'),('harvest','w_garden','0'),('egg','w_egg','0')]:
        E("(()=>{S.wish={id:null,at:0,capDay:today(),count:0}})()")
        E(f"(()=>{{{setup};S.wish.id='{wid}';S.wish.at=Date.now()}})()")
        b0=E("S.wish.count||0")
        if key=='now': E("acceptWish()")
        elif key=='harvest': E("(()=>{gardenState().slots[0]={seed:'arabica',start:Date.now()-99*36e5};harvest(0)})()")
        else: E("go('egg')")
        pg.wait_for_timeout(600); E(clean)
        ck(f'mong muốn {wid} hoàn thành bằng đúng việc', (E("S.wish.count||0")>b0), f'lần hoàn thành {b0}→{E("S.wish.count||0")}')
    E("(()=>{S.wish={id:null,at:0,capDay:today(),count:4}})()")
    ck('đủ 4 lần mỗi ngày thì thẻ nghỉ', E("currentWish()")==None)
    E("(()=>{S.wish={id:null,at:0,capDay:today(),count:0};go('home')})()")

    print('— 2. tính cách —')
    def dist(pers, setup):
        return E(f"""(()=>{{S.pet.pers='{pers}';{setup};const n={{}};for(let i=0;i<500;i++){{const w=pickWish();if(w)n[w.id]=(n[w.id]||0)+1}};return n}})()""")
    base="S.pet.care.hunger=80;S.pet.care.happy=80;S.pet.care.clean=80;S.pet.care.energy=80;S.pet.bond=80;towerState().tickets=5;advState().passes=3"
    d=dist('greedy', base+";") ; print('    tham ăn:', dict(sorted(d.items(),key=lambda x:-x[1])[:3]))
    E("(()=>{const h=new Date().getHours()})()")
    meal=E("[6,7,8,11,12,13,17,18,19].includes(new Date().getHours())")
    ck('tham ăn nhắc giờ ăn (nếu đang giờ ăn)', (not meal) or d.get('w_meal',0)>150, f'giờ ăn={meal}, w_meal={d.get("w_meal",0)}')
    d=dist('brave', base); ck('gan dạ muốn đánh boss', d.get('w_boss',0)>=max(d.values())*0.9, dict(sorted(d.items(),key=lambda x:-x[1])[:3]))
    d=dist('timid', base); ck('nhút nhát muốn bạn ở cạnh', d.get('w_hold',0)>=max(d.values())*0.9, dict(sorted(d.items(),key=lambda x:-x[1])[:3]))
    dc=dist('curious', base); dl=dist('lazy', base)
    ex=lambda d: sum(v for k,v in d.items() if k in ('w_trip','w_tower','w_garden','w_egg','w_boss'))
    ck('tò mò rủ khám phá nhiều hơn lười', ex(dc)>ex(dl)*2, f'tò mò {ex(dc)} · lười {ex(dl)}')
    # đo trực tiếp quyết định từ chối — một lượt rèn mất ~2,6 giây nên bấm dồn không đo được
    r=E("""(()=>{S.pet.pers='lazy';LAZY_LAST=false;const o=[];for(let i=0;i<400;i++)o.push(lazyRefuses('train'));return o})()""")
    two=any(r[i] and r[i+1] for i in range(len(r)-1))
    ck('lười thỉnh thoảng từ chối Rèn', 60<=sum(r)<=140, f'{sum(r)}/400 lần (~{round(sum(r)/4)}%)')
    ck('không bao giờ từ chối hai lần liền', not two)
    ck('lười không bao giờ từ chối ăn, tắm, ngủ, chơi', not any(E("(()=>{S.pet.pers='lazy';return ['feed','clean','sleep','play','explore'].map(k=>{let x=false;for(let i=0;i<50;i++)x=x||lazyRefuses(k);return x})})()")))
    ck('tính cách khác không từ chối Rèn', not any(E("(()=>{S.pet.pers='brave';const o=[];for(let i=0;i<100;i++)o.push(lazyRefuses('train'));return o})()")))
    # một lượt thật từ đầu tới cuối: bấm Rèn khi đang bị từ chối
    E("(()=>{S.pet.pers='lazy';LAZY_LAST=false;const _r=Math.random;Math.random=()=>0.01;window._r=_r})()")
    h0=E("S.pet.hist.train"); E("(()=>{SC.busy=false;doAct('train')})()"); pg.wait_for_timeout(500)
    E("(()=>{Math.random=window._r})()")
    ck('bấm Rèn thật: pet nói lý do, không trừ gì', E("S.pet.hist.train")==h0 and 'lười' in (E("[...document.querySelectorAll('.toast')].map(t=>t.textContent).pop()||''")).lower())
    E(clean)

    print('— 3. album —')
    E("""(()=>{S.life=[];const T=S.started;
      const at=(d,k,t)=>{S.life.push({k,d,at:T+d*864e5,t})};
      at(12,'born','Gặp '+S.pet.name);            // lỗi cũ: ghi ngày cài bản, không phải ngày gặp
      at(3,'trip','Đi Đồi trà'); at(5,'trip','Đi Cao nguyên đỏ'); at(6,'boss','Hạ được Hắc Tinh Ga');
      at(9,'bond','Gắn bó 75: x'); at(14,'bond','Gắn bó 100: y'); at(10,'evo','Tiến hoá thành Dạng Chăm Sóc');
      at(11,'child','Muối nở ra'); at(12,'quest',''); at(13,'wish','Cùng ăn');
      S.pet.born=S.started; save(); lifeFixBorn()})()""")
    ck('sửa ngày gặp nhau về ngày 1', E("S.life.find(e=>e.k==='born').d")==1, E("S.life.find(e=>e.k==='born').d"))
    P=E("albumPicks(10).map(x=>x.e.d+':'+x.A.t)")
    ck('album chọn lần đầu mỗi loại, gắn bó chỉ lấy mốc 100', P==['1:Gặp nhau','3:Chuyến đi đầu tiên','6:Thắng kẻ canh giữ đầu tiên','10:Tiến hoá','11:Có em bé','14:Gắn bó trọn vẹn'], P)
    E("(()=>{S._dtab='life';S._lifev='album';go('dex')})()"); pg.wait_for_timeout(700)
    ck('trang Cuốn đời mở bằng Album', pg.locator('.albc').count()==6)
    rec=set(E("(()=>{const s=new Set();for(let i=0;i<80;i++)s.add(lifeRecall());return [...s]})()"))
    ck('pet nhắc khoảnh khắc lớn', any('mới nở' in r for r in rec) and any('tiến hoá' in r for r in rec), f'{len(rec)} câu khác nhau')
    E("(()=>{S.life=[];for(let i=0;i<45;i++)S.life.push({k:'quest',d:2+i,at:i,t:''});S.life.unshift({k:'born',d:1,at:0,t:'Gặp X'});lifeAdd('craft','Pha thử',60)})()")
    ck('cuốn đời đầy vẫn giữ mốc Gặp nhau', E("S.life.some(e=>e.k==='born')") and E("S.life.length")<=40)

    print('— 4. con đường —')
    E("(()=>{S.pet.stage='adult';delete S.pet.form;S.pet.hist={feed:60,play:40,clean:10,sleep:5,pat:0,train:10,explore:3,win:2,lose:0,quest:10,trip:2};S.pet.bond=40;go('home')})()")
    pg.wait_for_timeout(700)
    E("openDetail&&openDetail()") if E("typeof openDetail==='function'") else None
    html=E("typeof lifePathHTML==='function'?lifePathHTML(S.pet):''")
    ck('sáu con đường, không có nhánh Ẩn', html.count('class="lpc')==6 and 'Ẩn' not in html)
    vals=E("DB.lifePath.map(L=>L.id+':'+Math.round(lpVal(L,S.pet)*100))"); print('   ', vals)
    ck('Chăm sóc giờ có thước đo thật', E("lpVal(DB.lifePath[0],S.pet)")>0.5)
    for setup,want in [("S.pet.hist.train=38;S.pet.hist.win=14","battle"),("S.pet.hist.feed=150;S.pet.hist.train=2;S.pet.hist.win=0","care"),("S.pet.hist.quest=59;S.pet.hist.feed=5","worker")]:
        got=E(f"(()=>{{{setup};return pickLifePath(S.pet,{{...S.pet,ageDays:20}})}})()")
        ck(f'nhánh cao nhất thắng → {want}', got==want, got)
    E("(()=>{S.pet.hist={feed:30,play:30,clean:30,sleep:30,pat:0,train:2,explore:2,win:0,lose:0,quest:3,trip:1};S.pet.bond=40;S.pet.stage='adult';S.pet.level=20;S.pet.born=Date.now()-11*864e5;delete S.pet.form;checkStage(S.pet)})()")
    ck('tiến hoá thật theo con đường cao nhất', E("S.pet.form")=='care', E("S.pet.form"))
    E("(()=>{S.pet.stash=null})()")

    print('— 5. nhà —')
    r=E("""(()=>{let n=0,same=0,labeled=0;
      for(let i=0;i<120;i++){
        const a=makePet({species:'beano'}),bb=makePet({species:'beano'});a.stage=bb.stage='adult';a.bond=bb.bond=80;
        const c=breedPair(a,bb); n++; if(c.house) labeled++; if(c.pers===DB.house[c.species].pers) same++;
      } return {n,labeled,same}})()""")
    ck('con đời 1 mang nhãn nhà', r['labeled']==r['n'], r)
    ck('khoảng một nửa nhận tính cách nhà', 45<=r['same']<=85, f"{r['same']}/{r['n']}")
    ck('nhãn hiển thị', 'Nhà Beano · Tò mò' in E("houseName(makePet({species:'beano'}))"))

    print('— thẻ chia sẻ và màn mở đầu —')
    E("(()=>{S.life=[];S.pet.born=S.started;lifeAdd('born','Gặp '+S.pet.name,1);S.life.push({k:'trip',d:3,at:1,t:'Đi Cao nguyên đỏ'},{k:'boss',d:6,at:2,t:'Hạ được Hắc Tinh Ga'},{k:'evo',d:10,at:3,t:'Tiến hoá thành Dạng Chăm Sóc'},{k:'child',d:13,at:4,t:'Miso ra đời'},{k:'bond',d:15,at:5,t:'Gắn bó 100: z'});S.pet.bond=100;save()})()")
    data=E("(async()=>{const b=await makeLifeCard();const r=new FileReader();return await new Promise(ok=>{r.onload=()=>ok(r.result);r.readAsDataURL(b)})})()")
    import base64; open('w_card12.png','wb').write(base64.b64decode(data.split(',')[1]))
    ck('không lỗi', not errs, errs[:3])
    pg2=b.new_page(viewport={'width':390,'height':844}); pg2.add_init_script("localStorage.clear()"); pg2.goto(url); pg2.wait_for_timeout(1500)
    ck('màn mở đầu không còn dòng tác giả', pg2.locator('#intro .icredit').count()==0 and 'Minh Đào' not in pg2.locator('#intro').inner_text())
    ck('chân màn mở đầu ghi v1.5', 'v1.5' in pg2.locator('#intro .ifoot').inner_text())
    b.close()
print('\n=== '+(f'{len(F)} HỎNG: {F}' if F else 'TOÀN BỘ ĐẠT')+' ===')
sys.exit(1 if F else 0)
