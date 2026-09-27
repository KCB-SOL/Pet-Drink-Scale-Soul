from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    pg.evaluate("""(()=>{S.onboarded=true;S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;window.confirm=()=>true;
      // pet chính đủ điều kiện
      S.pet.stage='adult';S.pet.bond=70;S.pet.species='beano';S.pet.name='Bơ';
      // chuồng: con ĐẦU MẢNG là pet non (không đủ), hai con sau đủ — đúng tình huống người dùng
      const non=makePet();non.stage='baby';non.bond=10;non.name='Nhóc';
      const m1=makePet({species:'matcha'});m1.stage='adult';m1.bond=72;m1.name='Trà';
      const m2=makePet({species:'milku'});m2.stage='evo';m2.form='care';m2.bond=88;m2.name='Sữa';
      const au=makePet({species:'automa'});au.model='am01';au.stage='adult';au.bond=90;au.name='AM-01';
      S.stash=[non,m1,m2,au];
      save();const e=document.getElementById('intro');if(e)e.remove();S._etab='barn';go('egg')})()""")
    pg.wait_for_timeout(900)
    print('tình huống: pet đầu mảng là pet non, hai con sau đủ điều kiện')
    pg.evaluate("breedUI()"); pg.wait_for_timeout(700)
    print('  bảng mở:', pg.locator('#sheet h3').first.inner_text() if pg.locator('#sheet').count() else 'KHÔNG MỞ')
    print('  chọn được:', pg.locator('#sheet .pickc').count(), 'bạn đời |',
          pg.evaluate("(()=>{return [...document.querySelectorAll('#sheet .pickc .pn')].map(e=>e.textContent)})()"))
    print('  nêu lý do cho con chưa đủ:', pg.evaluate("(()=>{return [...document.querySelectorAll('#sheet .kv')].map(e=>e.textContent.trim())})()"))
    n0=pg.evaluate("S.stash.length")
    pg.locator('#sheet .pickc').first.click(); pg.wait_for_timeout(1200)
    print('  sau khi lai:', pg.evaluate("S.stash.length"), '(trước', n0, ')')
    c=pg.evaluate("(()=>{const ch=S.stash[S.stash.length-1];return {ten:ch.name,doi:ch.gen,boMe:ch.parentNames,loai:DB.species[ch.species].name}})()")
    print('  con:', c)
    print('  khác loài vẫn lai được:', c['boMe'] is not None)
    print('LỖI:', errs[:3] if errs else 'không có')
    b.close()
