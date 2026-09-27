from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('index.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("localStorage.clear()")
    pg.goto(url); pg.wait_for_timeout(1600)
    print('1. màn mở đầu')
    print('   dòng tác giả dưới tên game:', 'đã bỏ đúng yêu cầu' if pg.locator('#intro .icredit').count()==0 else 'VẪN CÒN')
    print('   chân trang:', pg.locator('#intro .ifoot').inner_text().replace('\n',' / '))
    pg.screenshot(path='w_intro.png', clip={'x':0,'y':80,'width':390,'height':560})
    pg.evaluate("""(()=>{S.onboarded=true;S.lic=S.lic||{grand:true};(document.getElementById('lockscr')||{remove(){}}).remove();S.started=Date.now()-30*864e5;S.unl={seen:['n:battle','n:shop','n:egg','s:adv','s:team','s:gear','s:shop','s:fash']};S.opsSeen=DB.opsCards.map(c=>c.id);
      S.ch={done:DB.chapterAll.map(c=>c.id),cur:0};S.bondSeen=[25,50,75,90,100];
      S.npc={met:true,revealed:true};S.tut.done=true;
      save();const e=document.getElementById('intro');if(e)e.remove();S._dtab='set';go('dex')})()""")
    pg.wait_for_timeout(900)
    print('2. Cài đặt')
    print('   mục Về game:', pg.locator('.aboutbox').count(), '|', pg.locator('.aboutbox').inner_text().replace('\n',' · ')[:130])
    print('   mục Nhạc của bạn:', pg.locator('text=Nhạc của bạn').count())
    pg.locator('.aboutbox').scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    pg.screenshot(path='w_about.png', full_page=False)
    print('3. nhạc có sẵn')
    pg.evaluate("(()=>{sndInit();musicStart()})()"); pg.wait_for_timeout(1500)
    print('  ', pg.evaluate("({dangPhat:SND.playing, song:MUSIC[musicMood()].wave, nhip:Math.round(60/MUSIC[musicMood()].tempo/2)+' BPM', cat:MUSIC[musicMood()].cut, tram:MUSIC[musicMood()].bassGain})"))
    pg.evaluate("musicStop()")
    print('4. nhạc của bạn — nạp file thật')
    import base64
    data=base64.b64encode(open('nhac-video-demo.m4a','rb').read()).decode()
    r=pg.evaluate("""async (b64)=>{
      const bin=atob(b64); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i);
      const blob=new Blob([u],{type:'audio/mp4'});
      await mmPut({blob, name:'nhac-video-demo', at:Date.now()});
      await mmLoad(); const s=sndState(); s.mine=true; s.music=true; save();
      musicStop(); musicStart();
      await new Promise(r=>setTimeout(r,1500));
      return {daLuu:!!MYMUSIC.url, ten:MYMUSIC.name, dangDung:mmOn(),
              dangPhat:!MYMUSIC.el.paused, giay:+MYMUSIC.el.currentTime.toFixed(1), lap:MYMUSIC.el.loop}}""", data)
    print('  ', r)
    pg.evaluate("musicStop()"); pg.wait_for_timeout(300)
    print('   tắt nhạc thì dừng:', pg.evaluate("MYMUSIC.el.paused"))
    # nạp lại trang: file còn trong IndexedDB
    pg.reload(); pg.wait_for_timeout(2200)
    print('   nạp lại trang, file vẫn còn:', pg.evaluate("(async()=>{await mmLoad();return !!MYMUSIC.url && MYMUSIC.name})()"))
    print('LỖI:', errs[:3] if errs else 'không có')
    b.close()
