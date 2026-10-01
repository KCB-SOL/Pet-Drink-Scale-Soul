/* Pet Drink: Scale & Soul — service worker
   Bản cũ dùng tên bộ đệm cố định 'petpocket-v1' và lấy bộ đệm trước cho MỌI file.
   Khi sw.js không đổi giữa hai bản, máy đã cài cứ chạy bản cũ mãi, không nhận bản
   sửa lỗi mới. Nay:
   - tên bộ đệm gắn số phiên bản → đổi bản là bộ đệm cũ bị xoá
   - trang chính (index.html) lấy MẠNG TRƯỚC: có mạng thì luôn nhận bản mới nhất,
     mất mạng mới dùng bản trong bộ đệm — vẫn chạy offline được
   - ảnh, manifest vẫn lấy bộ đệm trước cho nhanh
   KHI PHÁT HÀNH BẢN MỚI: tăng VER dưới đây. */
const VER='1.1.2-b';
const C='petdrink-'+VER;
const ASSETS=['./','./index.html','./manifest.webmanifest','./icon.svg'];
self.addEventListener('install',e=>{
  // nhạc nền tải riêng: thiếu file (bản chỉ có một file HTML) thì không được làm hỏng cả bước cài
  e.waitUntil(caches.open(C).then(c=>c.addAll(ASSETS.map(u=>new Request(u,{cache:'reload'})))
      .then(()=>c.add(new Request('./nhac-nen.mp3',{cache:'reload'})).catch(()=>{})))
    .then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x))))
    .then(()=>self.clients.claim()));
});
function isPage(req){
  return req.mode==='navigate' || /\/(index\.html)?$/.test(new URL(req.url).pathname);
}
self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method!=='GET') return;
  // kênh sự kiện: LUÔN lấy mạng trước — không thì người chơi đọc mãi bản danh sách cũ.
  // Mất mạng mới dùng bản đã lưu (bỏ qua ?t= chống bộ nhớ đệm trình duyệt).
  const pn=new URL(req.url).pathname;
  if(pn.indexOf('/su-kien/')>=0 || /\/kenh\.txt$/.test(pn)){   // v1.1.2: cả kenh.txt ở thư mục gốc
    e.respondWith(fetch(req).then(res=>{ if(res.ok){ const cp=res.clone(); caches.open(C).then(c=>c.put(req.url.split('?')[0],cp)) } return res })
      .catch(()=>caches.match(req.url.split('?')[0])));
    return;
  }
  if(isPage(req)){
    // mạng trước cho trang chính
    e.respondWith(fetch(req).then(res=>{
      const cp=res.clone(); caches.open(C).then(c=>c.put('./index.html',cp)); return res;
    }).catch(()=>caches.match('./index.html').then(r=>r||caches.match('./'))));
    return;
  }
  // bộ đệm trước cho phần còn lại
  e.respondWith(caches.match(req).then(r=>r||fetch(req).then(res=>{
    const cp=res.clone(); caches.open(C).then(c=>c.put(req,cp)); return res;
  }).catch(()=>caches.match('./index.html'))));
});
