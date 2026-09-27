from playwright.sync_api import sync_playwright
import pathlib
url='file://'+str(pathlib.Path('trailer.html').resolve())
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':860}, device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url)
    marks=[(1.5,'s1'),(5.0,'s2'),(9.5,'s3'),(13.5,'s4'),(17.5,'s5'),(21.5,'s6'),(26.5,'s7'),(31.0,'s8')]
    last=0
    for t,name in marks:
        pg.wait_for_timeout(int((t-last)*1000)); last=t
        on=pg.evaluate("(()=>{const e=document.querySelector('.sc.on');return e?e.id:'-'})()")
        print(f'  {t:>4.1f}s  cảnh đang chiếu: {on}  {"OK" if on==name else "LỆCH (mong đợi "+name+")"}')
        pg.screenshot(path=f'tr_{name}.png', clip={'x':0,'y':0,'width':430,'height':790})
    print('LỖI:', errs[:3] if errs else 'không có')
    b.close()
