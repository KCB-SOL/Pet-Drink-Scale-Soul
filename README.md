# Pet Drink: Scale & Soul — v1.5

Mini game nuôi thú ảo offline, gắn vào công việc vận hành quán đồ uống.
Một file HTML chạy được ngoại tuyến, cài làm PWA được.

**Biểu tượng app:** pet loài Matcha — giọt trà xanh, hai lá trên đầu.


## PHÁT HÀNH BẢN MỚI — BẮT BUỘC
Mở `sw.js`, **tăng số `VER`** (ví dụ `1.1.0` → `1.1.1`). Nếu quên, máy đã cài game vẫn nhận
bản mới nhờ trang chính lấy mạng trước — nhưng ảnh và manifest sẽ giữ bản cũ.

Trước v1.1, `sw.js` dùng tên bộ đệm cố định `petpocket-v1` và lấy bộ đệm trước cho mọi file:
khi `sw.js` không đổi giữa hai bản, máy đã cài **cứ chạy bản cũ mãi**, không nhận bản sửa lỗi.

## Bản gọn cho điện thoại và iPad
`DB.lean = true` (trong `index.html`) ẩn: bong bóng và cửa sổ nổi ở trang Nhà, và 8 mục cài đặt
dành cho máy tính hoặc lúc phát triển. **Mã đo đạc vẫn chạy ngầm** để phiên ghép cầu nối có dữ
liệu so sánh. Đặt `DB.lean = false` để hiện lại toàn bộ.

## Mở dần theo ngày
Bảng `DB.unlockNav` (tab dưới) và `DB.unlockSub` (tab con trong Đấu). Mỗi mục mở theo ngày
**hoặc** theo tiến độ, cái nào tới trước. Người chơi cũ không bị khoá lại: lần đầu chạy bản mới,
mọi thứ đang mở được ghi là đã thấy, không bắn loạt thông báo.

## Thông báo xếp hàng
`showBanner()` không còn thay thông báo đang hiện. Cái mới vào hàng đợi `BANNER_Q`, hiện khi màn
hình trống (không thông báo, bảng hay hội thoại nào đang mở). **Khi viết test, đóng thông báo
bằng `closeBanner()` hoặc bấm nút — đừng xoá thẳng phần tử `.bnr`**, xoá thẳng sẽ giết luôn thông
báo mình đang muốn kiểm.


## Mong muốn — quy tắc khi thêm mong muốn mới
Mỗi mong muốn cần hai chỗ: một dòng trong `DB.wishes` (điều kiện, câu nói, câu khi đồng ý, câu khi
từ chối) và một dòng trong `DB.wishView` (biểu tượng, tên hành động, **`done`** — hành động nào hoàn
thành nó). Thiếu `done` thì thẻ hiện phần thưởng mà không bao giờ trả.

`fulfilWish()` xét **mong muốn người chơi đã nhận**, không gọi `currentWish()` — hàm đó kiểm lại điều
kiện, và chính việc làm đúng (cho ăn xong hết đói) sẽ làm mong muốn bị đổi trước khi kịp thưởng. Mong
muốn vừa bị thay được nhớ 60 giây vì nhiều hành động tự vẽ lại màn hình ở cuối.

## Con đường (Life Path)
`DB.lifePath` — mỗi con đường một hàm đo từ 0 tới 1, 100% bằng đúng ngưỡng cũ. Khi tiến hoá,
**con đường cao nhất thắng**. Nhánh Ẩn không hiện, vẫn được ưu tiên nếu đủ điều kiện.


## Hệ sự kiện
**KHOÁ BÍ MẬT KHÔNG BAO GIỜ ĐƯỢC NẰM TRONG THƯ MỤC NÀY.** `audit.py` dừng với mã lỗi nếu phát hiện
khoá trong `index.html`.

- Lõi dùng chung: `evcore.js` — chép **y hệt** vào `index.html` và vào trang tạo mã. Sửa một bên thì
  sửa cả bên kia, không thì trang tạo mã báo hợp lệ mà game từ chối.
- Khoá công khai: `DB.eventKeys` trong `index.html`. **Đổi khoá thì THÊM vào cuối danh sách, đừng
  xoá khoá cũ** — mã đã phát hành bằng khoá cũ vẫn được nhận.
- Mã: `PDE1.<dữ liệu>.<chữ ký>`, chữ ký ECDSA P-256 SHA-256 trên đúng các byte dữ liệu.
- Mã chỉ chứa dữ liệu theo danh sách định sẵn, không chứa lệnh. Muốn thêm loại nội dung mới thì
  sửa `evcValidate` trong lõi và phần nạp trong game.
- Công thức sự kiện **giữ mãi** sau khi sự kiện hết — sổ công thức tra theo mã công thức.


## v1.4 — mã hình, mã quà, key
- **Ba loại mã**, tiền tố `PDE` / `PDG` / `PDK`, số sau là 1 (thường) hoặc 2 (đã nén). **Loại mã nằm
  trong phần đã ký** (`t: event|gift|key`) — tiền tố không được ký, đổi tiền tố sẽ bị bắt.
- **Mã hình** `PDA…` chưa ký, chỉ để chuyển hình; hình đi qua `evcArt()` kiểm từng nét. Nét vẽ chỉ nhận
  chữ lệnh vẽ, số, dấu cách, phẩy, chấm, trừ. Màu chỉ nhận `#rgb`, `#rrggbb`, `none`.
- **Khuôn vẽ** (toạ độ theo thân pet, tâm 0,0): pet và boss vẽ thân quanh x −46…46, y −40…66; mũ trong
  x −50…50, y −104…−20; áo y 28…76; cầm tay x 22…78; khoác sau lưng x −62…62, y −40…72. Góc khung lễ
  trong ô 60×60, hạt rơi trong ô 16×16.
- **Pet sự kiện**: loài `ev_<sự kiện>_<hình>` đăng ký vào `DB.species` nhưng **không** vào
  `DB.speciesList` — trứng thường không nở ra. `p.evpet` chặn làm pet chính, lai tạo, tiến hoá.
- **Key**: `DB.license.required`. Người đã qua màn mở đầu từ bản trước được miễn (`S.lic.grand`).


## v1.5 — quy tắc thời gian thật
`DB.qrule`: việc cuối ngày (`eod`) ghi từ `eodHour()` giờ (mặc định 17, đổi ở Cài đặt, lưu `S.qset.eod`);
việc cuối tháng (`monthOpen`) mở từ ngày ghi trong bảng; việc tuần, tháng tối đa một lần mỗi ngày
(`S.questW.last`, `S.questM.last`).

**Bộ kiểm không kiểm giờ giấc phải đặt `S.qset={eod:0}`** — không thì kết quả tuỳ lúc chạy. Bài học
v1.5: các bộ cũ "đạt" chỉ vì máy thử đang ở 21 giờ; chạy lúc 9 giờ sáng thì ba bộ hỏng.

## Chạy kiểm trước mỗi lần đóng gói
```
python3 audit.py     # trùng tên class CSS, hàm JS, khoá trạng thái
python3 tsmoke.py    # 6 màn, 15 tab con, 12 hệ chính, 4 luồng chạy thật
python3 tfinal.py    # từng thao tác người chơi thật làm
python3 tunlock.py   # người mới ngày 1, người hăng hái, theo ngày, người cũ, bản gọn, thẻ chia sẻ
python3 tv12.py      # mong muốn có thưởng thật, tính cách, album, con đường, nhà
python3 tev.py       # mã ký bằng công cụ cũ v1.3 vẫn dùng được (cần file khoá)
python3 tv14.py      # key mở game, mã quà, sự kiện có hình, pet sự kiện (cần file khoá)
python3 tmaker.py    # công cụ ba thẻ → ký → game dùng được (cần file khoá)
python3 tv15.py      # việc theo giờ thật, chuồng/kho, hạt kinh nghiệm, trứng vàng
python3 thw.py       # chơi thử trọn sự kiện Halloween 2026 (cần file khoá)

# các bộ không kiểm giờ giấc phải đạt ở MỌI giờ — chạy lại lúc 9 giờ sáng:
python3 chay-buoi-sang.py tunlock.py   # tương tự cho tev, tv14, tsmoke, tfinal, tv12
python3 tmob.py      # bố cục ở 390 / 820 / 1440px
python3 tperf.py     # khung hình khi nhạc và hiệu ứng cùng chạy
```

**LƯU Ý:** từ v1.0 mã nằm trong **một file `index.html` duy nhất**. Các file module
(`data.js`, `v33.js`…) đã mất khi môi trường dựng bị dọn. Sửa trực tiếp trong `index.html`;
`audit.py` tự tách phần mã ra `_js.js` để soi.

## Chạy thử
Mở `index.html` bằng trình duyệt. Không cần server, không cần mạng.
Muốn cài như app trên điện thoại thì phải phục vụ qua HTTPS hoặc localhost (service worker yêu cầu vậy):

```
npx serve .
```

## File
| File | Vai trò |
|---|---|
| `index.html` | Toàn bộ game — dữ liệu, engine, hoạt cảnh, nội thất, tháp, dải quán, khung lễ, khu vườn, công thức, cài đặt, phiêu lưu, đo lường, cầu nối, hệ trạng thái pet, bóng dáng theo loài, trang bị, cốt truyện, Automa, kỷ niệm, hội thoại, âm thanh lofi, ghép trang bị, thời trang, tháp 110 tầng, Quán của chúng ta, sáu vị trí, di truyền, pet biết nhớ, mặt cắt quán, pet có ý muốn. 777 KB. |
| `sw.js` | Service worker, cache-first, chạy offline hoàn toàn. |
| `manifest.webmanifest` | Cài đặt PWA. |
| `icon.svg` | Biểu tượng. |

Tổng bộ: **856 KB** (gồm 68 KB hai font tiếng Việt nhúng sẵn), không phụ thuộc thư viện ngoài, không gọi mạng. Ngân sách 2–3 MB dư rất nhiều.

## Cấu trúc trong index.html
Ba khối, đọc từ trên xuống:

1. `DB` — toàn bộ hằng số cân bằng. Sửa ở đây là đổi game, không cần đụng logic.
2. Engine — di truyền, mô phỏng offline, bệnh, tiến hoá, đấu, dựng SVG.
3. Scene — đi lại, chớp mắt, ánh sáng theo giờ, chạm/giữ/kéo, 6 hoạt cảnh.
4. v2 — hình vẽ nội thất, hoạt cảnh trận đấu, chế độ nổi, thành tựu.
5. Zones — 7 khu, camera trượt ngang, điều hướng.
6. v6 — thiết bị F&B, nguyên liệu, khung lễ.
7. v7 — khu vườn, bàn chế biến, 24 công thức, ly buff.
8. v8 — màn khởi đầu, chủ đề màu, chế độ thử, sao lưu, mã pet.
9. v9 — 7 bản đồ phiêu lưu, chuyến đi, Pandora, tháp dọc.
10. v10 — ghi nhận sử dụng, cầu nối postMessage, hướng dẫn, hoạt cảnh tiến hoá.
11. v11 — hệ 14 trạng thái pet, thang khoảng cách 4 nấc.
12. v12 — sáu bóng dáng riêng theo loài, cờ `industrial` cho phe Công Nghiệp.
13. v13 — 4 ô trang bị, 20 món, 5 bậc chất liệu, hệ Rác.
14. v14 — chặng 4–5 (tầng 31–50), 5 mini boss, 10 thẻ cốt truyện.
15. v15 — Automa, điểm cốt, cây kỹ năng, trang bị mặc được, nền sàn đấu.
16. v16 — kỷ niệm, lời pet theo tính cách, sự kiện nở trứng, cốt truyện Quy mô đối Tâm hồn.
17. v17 — AM-00, hội thoại có chân dung, lớp trận đấu viết lại, nền ba lớp.
18. v18 — âm thanh tổng hợp lúc chạy, nhạc nền sinh theo thuật toán, ánh sáng và chuyển cảnh.
19. v19 — sửa lỗi mất hiệu ứng, hội thoại ra giữa, Nhà gọn, cây kỹ năng sơ đồ, 20 kiểu dáng trang bị.
20. v20 — cấp thân thiết vùng, 18 thẻ tri thức, 6 pet hoang, 6 boss vùng, bản đồ có nút.
21. v21 — nhạc lofi có vòng hoà thanh, bảng mô tả kỹ năng, quái theo phe Công Nghiệp, thả pet.
22. v22 — ghép và bán trang bị, 24 món thời trang, phòng thay đồ.
23. v23 — 12 kỳ ngộ, hộp bí ẩn ba hạng, hiệu ứng kỹ năng theo tên gọi.
24. v24 — tháp 110 tầng, 6 chặng mới, 12 thẻ cốt truyện, Bản Chuẩn và đoạn kết.
25. v25 — lịch sinh hoạt, khẩu vị theo loài, mốc gắn bó, tổng kết ngày, tuyến "Quán của chúng ta".
26. v26 — trần điểm cốt theo giai đoạn, 8 nông sản mới, sửa định lượng 24 công thức, sáu vị trí trong quán.
27. v27 — 9 khung thân boss, 12 chiêu riêng có hiệu ứng, cây gia phả và ký ức thừa hưởng.
28. v28 — pet tự bắt chuyện: 22 chủ đề, 75 câu, cộng ba phản ứng còn thiếu.
29. v29 — pet nhớ chuyện hôm qua, mốc gắn bó mở khoá, truyền thống dòng, nhiệm vụ kể kiểu pet nhờ, 8 đồ của pet.
30. v30 — Bản Chuẩn ba pha, gắn loài với vùng, 6 linh hồn vùng, chỉ báo ba mức trên UI tháp.
31. v31 — sửa lỗi chết tuyến "Quán ta", vẽ 22 nội thất, mặt cắt quán 6 pet, bán ly dư, lọc chuồng và kho.
31.1 — sửa bố cục màn rộng: thanh nav bám cột, dải tab xuống dòng thay vì cuộn ngang.
32. v32 — 9 hình nông sản, 18 công thức mới, nhạc chiptune, Automa tầng 30 + 3 mẫu khác loại, 25 thẻ quản trị quán.
33. v33 — mong muốn có thể từ chối, Cuốn đời theo ngày, nhánh Explorer, lời pet mọi trận, sửa hai lỗi ô vườn.
7. v4 — biểu tượng vật phẩm, sơ đồ lục giác, banner thắng, lời thoại, hành động nhàn rỗi.
6. Tower — sinh tầng, vé, tổ đội, phần thưởng, ngủ đông.
7. UI — trạng thái lưu, 6 màn hình, cầu nối nhiệm vụ.

### Sửa nội dung v4
| Muốn | Sửa |
|---|---|
| Đổi thưởng đấu giao hữu | `DB.quickBattle` |
| Thêm lời thoại | `DB.talk.pers` và `DB.talk.situ` |
| Thêm hành động nhàn rỗi | mảng `IDLE` + keyframes trong CSS |
| Đổi hình vật phẩm | `ITEM` trong khối v4 |
| Đổi vỏ trứng | `eggArt()` |
| Đổi huy hiệu thành tựu | `DB.achIcon` |

### Sửa dải quán
| Muốn | Sửa |
|---|---|
| Thêm hoặc bớt khu | `ZONES` + `zoneArt()`, cập nhật `.strip{width}` |
| Đổi khu cho một hành động | trường `act` trong `ZONES` |
| Đổi tốc độ đi bộ giữa khu | hàm `gotoZone()`, biến `dur` |
| Đổi độ cao pet khi nằm giường | class `.actor.onbed` |

### Sửa cửa hàng và khung lễ
| Muốn | Sửa |
|---|---|
| Thêm thiết bị F&B | `DB.furniture` + hình trong `FS` |
| Thêm nguyên liệu | `DB.mats` + hình trong `ITEM` |
| Thêm khung lễ | `DB.frames` + hình trong `FRAME_ART` |
| Đổi khoảng ngày gợi ý mùa | trường `window` trong `DB.frames` |
| Đổi hiệu ứng nội thất hoặc khung | trường `perk`, đọc bởi `activePerks()` |

### Sửa khu vườn và công thức
| Muốn | Sửa |
|---|---|
| Đổi thời gian trồng | trường `hours` trong `DB.seeds` |
| Đổi sản lượng mỗi ô | `DB.garden.yield` |
| Đổi số ô và giá mở | `DB.garden.freePlots`, `DB.garden.expand` |
| Thêm công thức | `DB.recipes` — nhớ điền cả `real` |
| Đổi mức khắc chế nhóm vị | `DB.weakBonusMult` |
| Thêm hiệu ứng buff mới | `DB.buffLabel` + hàm `drinkOpt()` |

### Cài đặt và font
| Muốn | Sửa |
|---|---|
| Bỏ chế độ thử khỏi bản chính thức | `DB.devMode.enabled = false` |
| Đổi câu mở khoá | `DB.devMode.phrase` |
| Thêm chủ đề màu | `DB.themes` |
| Đổi lời màn khởi đầu | `DB.intro` |
| Thay font tiêu đề | chuỗi base64 trong `@font-face` của `PP Serif` |

### Phiêu lưu và tháp dọc
| Muốn | Sửa |
|---|---|
| Thêm bản đồ | `DB.maps` + nhánh trong `mapPlant()` và `mapHorizon()` |
| Đổi thời lượng chuyến | `DB.adv.tripMinutes` |
| Đổi tỉ lệ nhận lượt đi | `DB.adv.pass` |
| Đổi mức phạt Pandora | `DB.adv.synthPenaltyPer`, `synthPenaltyCap`, `synthBuffMult` |
| Đổi số tầng hiện trong tháp dọc | hàm `verticalTower()` |
| Đổi tỉ lệ trứng khởi đầu | `DB.intro.dist` |

### Nhúng vào công cụ vận hành
Đặt game trong iframe rồi trao đổi bằng `postMessage`. Xem mã mẫu đầy đủ trong Cài đặt của game.

```js
// công cụ báo sang game
frame.contentWindow.postMessage({type:'pp:ops', quests:['open','pnl'],
  foodCost:'good', revenue:{actual, target}, checklistRate:0.97}, '*');

// game báo về công cụ, mỗi 60 giây
window.addEventListener('message', e => {
  if(e.data.type==='pp:status' && e.data.needsCare) showNhac(e.data.hint);
});
```
Trạng thái cũng ghi vào `localStorage['petpocket.status']` nếu không dùng iframe.

| Muốn | Sửa |
|---|---|
| Đổi mức thưởng khi food cost đẹp | `opsBuffMult()` |
| Thêm loại dữ liệu vận hành | `handleOps()` |
| Đổi các bước hướng dẫn | mảng `TUT` |
| Xem hoặc xoá số liệu đo | `S.tel`, hàm `telSummary()` |

### Vùng nguyên liệu
| Muốn | Sửa |
|---|---|
| Đổi tốc độ lên cấp vùng | `DB.region.tripsPerLevel` |
| Đổi tỉ lệ gặp pet hoang | `DB.region.petChance` |
| Thêm thẻ tri thức | `DB.knowCards` — ba thẻ mỗi vùng, mở ở cấp 2/3/5 |
| Thêm pet hoang | `DB.species` với cờ `wild:true` + `DB.wildOf` + `DB.evo[id]` |
| Đổi boss vùng | `DB.regionBoss` |
| Đổi vị trí nút bản đồ | `DB.mapNodes` — toạ độ phần trăm, giữ ở nửa trên để không đè tên vùng |

**Khi cân boss, đo kỹ năng trước.** Trong engine này bộ kỹ năng chi phối mạnh hơn cả hệ số `mult`
lẫn cơ chế đặc biệt: cùng một boss, đổi sang kỹ năng cơ bản thì người chơi thắng 100%, giữ bộ bốn
kỹ năng của loài thì thắng 2%. Công thức đang dùng: **một kỹ năng đặc trưng + hai kỹ năng thường**,
rồi dò `mult` bằng tìm kiếm nhị phân cho tỉ lệ thắng mục tiêu.

### Giảm chuyển động — ĐỪNG tắt tất cả
```css
/* SAI — đây là lỗi của v1 tới v18 */
@media(prefers-reduced-motion:reduce){ *{animation:none!important} }
```
Máy nào bật Giảm chuyển động là mất sạch cánh hoa rơi, bụi bay, pet thở. Quy tắc đúng:
tắt thứ **di chuyển tầm nhìn** (chuyển trang, camera trượt, xoay tít), giữ thứ **trang trí tại chỗ**.
Người dùng có công tắc riêng `body.nofx` trong Cài đặt, độc lập với hệ điều hành.

### Cây kỹ năng và trang bị
| Muốn | Sửa |
|---|---|
| Đổi nhánh mở sẵn | `S._topen` trong `skillTreeHTML()` |
| Thêm kiểu dáng trang bị | `GEAR_ART[<ô>][<bậc>]` trong v13 |
| Đổi dáng mặc trên người | `gearLayers()` trong engine — nhóm theo bậc bền |

### Âm thanh
Không có file nhạc nào. Toàn bộ tổng hợp bằng Web Audio, khoảng 13 KB mã.

| Muốn | Sửa |
|---|---|
| Thêm tiếng động | bảng `SFX` — mỗi mục là vài lần gọi `tone()` và `noise()` |
| Đổi vòng hoà thanh | `MUSIC.day.prog` / `MUSIC.night.prog` — mảng hợp âm, mỗi hợp âm là các quãng tính từ `root` |
| Đổi tốc độ chuyển hợp âm | `MUSIC.*.bars` (giây mỗi hợp âm) |
| Nhạc nghe chói | hạ `MUSIC.*.cut`, hoặc chỉnh hạ kệ `-14 dB` trong `musicStart()` |
| Đổi giờ chuyển ngày/đêm | `musicMood()` |
| Đổi độ vang | hệ số `wet.gain` trong `sndInit()` |

**iOS chỉ cho tạo âm sau một thao tác chạm thật** — `sndUnlockOnce()` lo việc này, đừng gọi
`musicStart()` lúc khởi động.

### Ánh sáng
`paintDust()`, `paintRay()`, `paintGlow()` trong scene. Chùm sáng chỉ hiện 6h–17h,
quầng ấm chỉ hiện 17h–7h. **Chỉ dùng transform và opacity** trong mọi keyframe.

### Hội thoại và AM-00
| Muốn | Sửa |
|---|---|
| Thêm cảnh hội thoại | `startDialogue([{who:'npc'|'pet'|'boss', text}], {after})` |
| Đổi lời AM-00 cho từng thẻ | `DB.npcLine` |
| Đổi lời chào khi mở app | `DB.greet` — xét theo thứ tự, câu đầu khớp thì dùng |
| Đổi cú lật AM-00 | `DB.npc.reveal` + `npcReveal()` |

### Lớp trận đấu
| Muốn | Sửa |
|---|---|
| Cỡ số sát thương | `.bpop` — 42px thường, `.small` 22px cho hiệu ứng phụ |
| Vị trí thanh máu | `.bhud` nằm trong `.bf`, `bottom:-28px` |
| Hiệu ứng trúng đòn | `.burst` / `bburst(side, crit)` |
| Biểu tượng hiệu ứng | `DB.buffIcon` + hàm `tags()` trong engine gửi `b1`/`b2` theo mỗi sự kiện |
| Nền sàn đấu | `ARENA_ART[<chặng>]` — ba hàm `far`, `mid`, `near` |

**Lưu ý khi test:** ba lớp phủ có thể nối tiếp nhau (banner → hội thoại → bảng kéo lên).
Kịch bản tự động phải đóng lặp nhiều lần, không đóng một lần rồi bấm ngay.

### Kỷ niệm và lời pet
| Muốn | Sửa |
|---|---|
| Thêm mốc kỷ niệm | `DB.memories` + điều kiện trong `scanMems()` |
| Thêm lời pet theo tính cách | `DB.opinion.<hoàn cảnh>` — **một câu ngắn cho mỗi tính cách**, không viết cả đoạn |
| Đổi lời thẻ hành động | `heroAction()` |
| Đổi chuỗi nở trứng | `hatchEvent()` / `paintHatch()` — dùng chung `introEggArt()` với màn khởi đầu |
| Đổi tên trạng thái | `DB.disease[].name` và `.cure` |

**Nguyên tắc ngôn từ:** không dùng thuật ngữ y khoa thật làm nhãn trạng thái pet, và không viết
lời khiến người chơi thấy mình là người chủ tồi. Pet không chết — ngủ đông hiện là "nghỉ cùng bạn".

**Nguyên tắc dung lượng cho nội dung theo tính cách:** một đoạn kể chung + một câu ngắn theo tính cách.
Viết cả đoạn cho từng tính cách sẽ nhân dung lượng lên mười lần.

### Automa, điểm cốt, trang bị mặc được
| Muốn | Sửa |
|---|---|
| Đổi số răng bánh răng của Automa | `cogPath(n, rOut, rIn, cy)` trong `BODY.automa` |
| Thêm dòng máy | `DB.automa.models` |
| Đổi mức đóng góp Automa | `DB.automa.share` |
| Đổi điểm cốt mỗi cấp / mỗi lần rèn | `DB.core.perLevel`, `perTrain`, `capPct` |
| Đổi hình trang bị mặc trên người | `gearLayers()` trong engine — neo vào tâm (0,20) |
| Thêm nền sàn đấu | `DB.arenaBg` + nhánh `kind` trong `arenaBg()` |

**Automa bị chặn ở bốn chỗ:** `swapPet` (không làm pet chính), `checkStage` (không tiến hoá),
`breedUI` (không lai tạo), và Gắn bó luôn bằng 0. Thêm loài đặc biệt mới thì phải chặn cả bốn.

### Tháp, mini boss và cốt truyện
| Muốn | Sửa |
|---|---|
| Mở chặng mới | `DB.tower.stages[].open = true` + `DB.tower.openStages` |
| Thêm mini boss | `DB.miniBoss[<số chặng>]` — đứng ở tầng 5 của chặng đó |
| Thêm cơ chế boss | nhánh `f.mech` trong `tick()` của engine + `mechP` trong data |
| Thêm thẻ cốt truyện | `DB.lore` + `DB.loreOrder` |
| Đổi thưởng mini | `DB.tower.reward.miniCoin`, `miniSeed` |

**Quy tắc khi vá mã:** mỗi phép thay thế phải kiểm tra khớp trước khi ghi. Ba lần trong dự án
này đã vá nhầm module và phép thay thế trượt im lặng — `verticalTower` ở v9 chứ không phải ui,
`ringHTML` ở v2 chứ không phải ui, `claimAch` ở v2 chứ không phải ui.

### Ba trục khắc chế — ĐỪNG THÊM TRỤC THỨ TƯ
| Trục | Quyết định | Dữ liệu |
|---|---|---|
| Loài | pet đấu pet | `DB.counter` |
| Nhóm vị | ly khắc chế boss | `DB.tasteGroups` + `boss.weak` |
| Vùng | pet hợp chặng tháp | `DB.regionSpecies` — DÙNG LẠI loài, không phải trục mới |

**Lợi thế vùng KHÔNG chồng với khắc chế loài** (`tm===1` mới áp dụng). Chồng cả hai thì
tầng 90 lên 100% thắng.

Khi mở tầng mới hoặc đổi cơ chế boss, đo lại **cả hai cột**: pet thường và pet hợp vùng.

### SỬA LỖI CHẠM: PHẢI KIỂM BẰNG CÚ CHẠM THẬT
v31 thêm nhánh xử lý ô đất khoá vào `tapPlot()` và test gọi thẳng `tapPlot(4)` — pass.
Nhưng ô khoá **không có `onclick`**, và dải chấm `.zdots` (z-index 11) còn đè lên ô đất (z-index 5).
Người chơi bấm mãi không được suốt hai bản.

**Khi sửa lỗi liên quan tới chạm, test phải `.click()` thật, không được gọi hàm trực tiếp.**
Dùng `document.elementFromPoint()` để biết thứ gì đang nằm trên.

Ngược lại: nếu `.click()` của Playwright hỏng mà `dispatch_event('click')` chạy được thì đó là
giới hạn công cụ test (phần tử chưa đứng yên vì camera đang trượt), **không phải lỗi sản phẩm**.

### TRÙNG TÊN — BỐN LẦN RỒI
| Lần | Tên | Hậu quả |
|---|---|---|
| v17 | `.bf` | đấu sĩ và dòng hiệu ứng công thức |
| v23 | `.fr` | thẻ khung lễ vỡ layout |
| v23 | `.dim` | tab Đấu trống trơn |
| v32 | `toggleFold()` + `S.fold` | nút gập gọi nhầm vào bảng biên lai |

Ba lần đầu là class CSS nên `audit.py` bắt được. **Lần thứ tư là tên hàm JS nên lọt.**
Bộ kiểm nay soi thêm: tên hàm JS khai báo ở nhiều module, và khoá `S.*` khởi tạo ở nhiều nơi.

**Chạy `python3 audit.py` trước mỗi lần đóng gói.** Nó trả mã lỗi khác 0 khi phát hiện.

### NHẠC — ĐỪNG THÊM NHIỄU NỀN
Bản v21 thêm lớp nhiễu giả tiếng đĩa than (bandpass 3200 Hz). Trên loa điện thoại nghe thành
**loa rè**. Đã bỏ hẳn. Nhạc hiện dùng sóng vuông cho giai điệu, tam giác cho bè trầm, cắt 2600 Hz
kèm hạ kệ −18 dB từ 3000 Hz.

| Muốn | Sửa |
|---|---|
| Đổi vòng hợp âm | `MUSIC.day.prog` / `MUSIC.night.prog` |
| Đổi mẫu giai điệu | `MUSIC.*.pat` (bậc trong hợp âm) và `MUSIC.*.oct` (quãng) |
| Đổi tốc độ | `MUSIC.*.tempo` — giây mỗi nốt |

### BỐ CỤC MÀN RỘNG
Cột nội dung là `.wrap{max-width:520px;margin:0 auto}`. **Mọi phần tử `position:fixed` phải bám cột
đó**, không bám viewport: `left:50%; transform:translateX(-50%); max-width:520px`. Bản v1 để
`.nav{left:0;right:0}` nên trên máy tính thanh điều hướng trải hết 1440px.

**Đừng dùng `overflow:auto` cho dải tab.** Trình duyệt tự trượt tới tab đang chọn và cắt mất tab
đầu; người chơi cũng không biết là còn tab để cuộn. Dùng `flex-wrap:wrap`.

Chạy `tmob.py` để kiểm bố cục ở 390 / 820 / 1440px trước khi đóng gói — bộ test chính chỉ chạy
ở 390 và 820 nên không bắt được lỗi màn rộng.

### BÀI HỌC: TEST KHÔNG ĐƯỢC VÔ HIỆU HOÁ THỨ NÓ KIỂM
Hai lần rồi:
- v17: bản vá đặt `npc.met=true` cho mọi kịch bản, kể cả kịch bản kiểm màn chào AM-00.
- v31: kịch bản đặt `S.ch.done` đầy để bỏ qua hội thoại — nên **không ai phát hiện tuyến
  "Quán ta" chết cứng suốt 6 bản** vì `S.stats.days` không tồn tại.

**Khi thêm bước bỏ qua vào test, phải có ÍT NHẤT một kịch bản không bỏ qua** và kiểm đúng
thứ đó từ trạng thái sạch.

### Vẽ vào cảnh quán
- `place(el, leftPct, bottomPx)` — `leftPct` là phần trăm trên **cả dải tám khu**, không phải
  trong từng khu. Quy đổi: `(zone + x/100) * (100/ZN)`.
- `paintProps()` xoá mọi `.prop` ở đầu hàm. Thứ gì mang class `prop` phải vẽ **SAU** dòng đó.
- `go('home')` phải gọi `paintProps()`, nếu không mua đồ ở Shop xong về Nhà sẽ không thấy.

### QUY TRÌNH VÁ MÃ — đọc trước khi viết kịch bản vá
Hàm `rep()` dùng `SystemExit` khi không khớp, nên **một phép vá lỗi làm dừng cả loạt phía sau**.
Ở v29 ba tính năng bị bỏ sót theo cách này và suýt được ghi là "đã làm".

**Khi vá nhiều chỗ trong một kịch bản: ghi lại chỗ lỗi rồi đi tiếp, đừng dừng.** Và luôn chạy
test xác nhận từng tính năng, đừng tin vào dòng "ok" của kịch bản vá.

### Pet biết nhớ
| Muốn | Sửa |
|---|---|
| Thêm loại sự kiện pet nhớ | `DB.recallKinds` + gọi `noteEvent(kind, x)` ở chỗ sự kiện xảy ra |
| Đổi cửa sổ nhắc | `DB.recallCfg.minAgeH` / `maxAgeH` — dưới 6 giờ thì nhắc lại thành ngớ ngẩn |
| Đổi mốc gắn bó mở khoá | `DB.bondUnlock` |
| Thêm truyền thống dòng | `DB.lineTraits` — điều kiện đọc từ `lineStats()` |
| Đổi lời nhờ của nhiệm vụ | `DB.questAsk` |
| Thêm đồ của pet | `DB.petDecor` + hình trong `decorArt()` + hiệu ứng trong `decorPerk()` |

### Pet tự bắt chuyện
| Muốn | Sửa |
|---|---|
| Thêm chủ đề | `DB.chatter` — mỗi mục có `when(ctx)`, trọng số `w`, và mảng câu |
| Thêm biến thay vào câu | `chatCtx()` trong v28 — mọi khoá của nó dùng được dạng `{ten}` |
| Đổi nhịp nói | `DB.chatterCfg.minGap` / `maxGap` |

**Trường `act` trong `DB.routine` là cụm mô tả, KHÔNG dùng được trong câu** — dùng `doing`.
Ghép nhầm ra "Mình đang đang ngủ đây".

Pet im lặng khi có bất kỳ lớp phủ nào đang mở (`#dlg`, `#sheet`, `.bnr`) — kiểm trong `chatTick()`.

### Boss: khung thân và chiêu riêng
| Muốn | Sửa |
|---|---|
| Đổi khung thân boss | `DB.indusShape[<tên boss>]` → khoá trong `BODY_INDUS_SET` |
| Thêm khung thân mới | `BODY_INDUS_SET` trong engine |
| Thêm chiêu riêng | `DB.bossSkills[<tên boss>]` — `every`, `eff`, `fx`, `col` |

**CHOÁNG là hiệu ứng nặng nhất.** Trận khoảng 20 lượt, mất 2–3 lượt là mất trận. Lần đầu thêm chiêu
làm ba boss tụt từ 30–60% xuống 5–9%. Chu kỳ choáng tối thiểu 5 lượt, và với boss đã có cơ chế mạnh
thì đừng dùng choáng — dùng giảm chỉ số.

### Di truyền
| Muốn | Sửa |
|---|---|
| Số ký ức truyền đời | `DB.lineage.memInherit` |
| Tỉ lệ truyền đặc điểm | `DB.lineage.traitChance` |
| Ưu thế mỗi đời | `DB.lineage.genPerk` — cộng vào trần tiềm năng |

**Sổ dòng dõi (`S.line.pets`) lưu riêng khỏi danh sách pet.** Thả pet không làm đứt cây gia phả —
cá thể đó mờ đi nhưng vẫn còn trong sổ.

### Điểm cốt và ngưỡng sức mạnh
| Muốn | Sửa |
|---|---|
| Đổi trần điểm cốt | `DB.core.capByStage` — theo giai đoạn, KHÔNG dùng `capPct` cố định |
| Đổi cách tiêu điểm dư | `DB.core.trade` |
| Thêm vị trí trong quán | `DB.shopRoles` — mỗi vị trí một `perk.type` nối vào cơ chế sẵn có |

**Điểm cốt cấp theo cấp là vô hạn, trần tiêu thì hữu hạn.** Nếu để trần cố định thì Lv60 dư 124
điểm. Trần phải tăng theo giai đoạn, và phần dư phải đổi được thành thứ khác.

**Ngưỡng phá đảo tầng 110:** đối thủ tương đương 2.446 PP. Pet người chơi tối đa 989 PP (Thần thoại
Lv60). Khoảng chênh bù bằng tổ đội, trang bị, ghép và ly đúng vị — cộng lại khoảng 1,9×, ra 30% thắng.

### Định lượng công thức
Ly có đá: nền lỏng **45–55%** tổng thể tích, đá 100–150g. Ly nóng: nền lỏng 85–90%, ghi rõ "ly nóng".
Bản v7 để nền lỏng tới 91% ở một số món — sai thực tế.

### Ba tuyến truyện — đừng lẫn
| Tuyến | Kể về | Dữ liệu |
|---|---|---|
| Tháp | thế giới bên ngoài, phe Công Nghiệp | `DB.lore` — 22 thẻ, mở theo tầng |
| Vùng nguyên liệu | nơi đồ uống sinh ra | `DB.knowCards` — 18 thẻ, mở theo cấp thân |
| **Quán của chúng ta** | chính cái quán của người chơi | `DB.chapters` — 8 chương, mở theo cột mốc quán |

Chương mở **tuần tự** và **theo cột mốc của quán**, không theo tầng tháp. Chương 6 chờ dữ liệu
doanh thu thật từ cầu nối — đó là chỗ tuyến truyện chạm vào công việc ngoài đời.

### Lịch sinh hoạt và khẩu vị
| Muốn | Sửa |
|---|---|
| Đổi thói quen theo giờ | `DB.routine` — mảng khung giờ, khu, dáng, lời |
| Đổi khẩu vị loài | `DB.speciesTaste` + hệ số `DB.tasteBond` |
| Thêm mốc gắn bó | `DB.bondEvents` |
| Đổi biểu tượng nhiệm vụ | `DB.questIcon` |

**Kho nông sản là `invCrop()`, không phải `invOf().crops`.** Và `g()` trong `applyAct` là hàm
cục bộ — ngoài đó dùng `perkOf('gain', <hành động>)`.

### Đường cong sức mạnh tháp — ĐỌC TRƯỚC KHI MỞ TẦNG MỚI
`tunePet` chỉ dựng nổi đối thủ tới khoảng **550 PP**; pet người chơi cũng chỉ đạt khoảng **770 PP**
dù lên cấp bao nhiêu. Đường cong mũ cũ đòi 6.991 PP ở tầng 110 nên mọi tầng trên 55 đều thắng 99%.

Cách đang dùng:
- `DB.tower.power(f)` — sức mạnh nền, **tuyến tính chậm** từ tầng 51: `704 + (f−50)×5,4`
- `DB.tower.pressure(f)` — **hệ số ép** nhân thẳng vào chỉ số: `1,14 + (f−50)×0,0115`

Mở tầng mới thì chỉnh `pressure`, **đừng chỉnh `power`** — hệ chỉ số không biểu diễn nổi.

### QUY TẮC ĐẶT TÊN CLASS — đọc trước khi thêm CSS
Ba lần trùng tên class đã gây lỗi hiển thị nặng:
- `.bf` — đấu sĩ trên sàn đấu **và** dòng hiệu ứng công thức (v17)
- `.fr` — thẻ khung lễ **và** hạt hiệu ứng vòng khí (v23)
- `.dim` — lớp phủ toàn màn **và** nhãn "chưa sở hữu" (v23)

**Mọi class mới phải có tiền tố theo module.** `pf` cho hiệu ứng kỹ năng, `g` cho trang bị,
`enc` cho kỳ ngộ, `fash` cho thời trang. Tên một hoặc hai chữ cái ở mức gốc là cấm.

Chạy `python3 audit.py` trước khi đóng gói — nó dừng nếu phát hiện lớp phủ toàn màn bị dùng
làm nhãn phụ, và liệt kê class khai báo trùng ở mức gốc.

### Kỳ ngộ, hộp bí ẩn, hiệu ứng kỹ năng
| Muốn | Sửa |
|---|---|
| Thêm kỳ ngộ | `DB.encounters` — mỗi mục có `fn()` đọc trạng thái và `goal` |
| Đổi lúc lộ gợi ý | `DB.encRevealAt` |
| Đổi nội dung hộp | `DB.box[<hạng>].pool` và `DB.boxAmt` |
| Thêm hiệu ứng kỹ năng | gán vào `DB.skillFx` một trong 10 khuôn ở `DB.fxKinds` |
| Thêm khuôn hiệu ứng mới | nhánh trong `playFx()` + CSS keyframe `fx<tên>` |

**Đừng thêm bậc chất liệu thứ sáu cho trang bị.** Hộp vàng thưởng bậc inox — bậc tốt nhất hiện có.
Thêm bậc trên inox sẽ phá cân bằng năm bậc và làm vô nghĩa đường cong ba tuần của v13.

### Ghép trang bị và thời trang
| Muốn | Sửa |
|---|---|
| Đổi trần ghép từng bậc | `DB.fuse.cap` |
| Đổi chi phí ghép | `DB.fuse.cost(lv)` |
| Đổi mức cộng mỗi cấp | `DB.fuse.bonusPerLv` |
| Đổi giá bán | `DB.fuse.sellBase`, `sellPerLv` |
| Thêm món thời trang | `DB.fashion` + dáng mặc trong `fashLayers()` |

**Trần ghép PHẢI khác nhau theo bậc.** Nhựa và giấy mua được bằng xu nên là nguồn vô hạn —
cho ghép ngang inox thì chúng lại mạnh tuyệt đối và đường cong ba tuần của v13 sụp.

**Khi vẽ lớp mặc lên pet:** khuôn mặt nằm quanh y = 6–20 trong hệ toạ độ thân. Mọi lớp áo phải
bắt đầu từ y = 34 trở xuống, nếu không sẽ che mất miệng.

### Trang bị và hệ Rác
| Muốn | Sửa |
|---|---|
| Đổi buff gốc từng ô | `DB.gearSlots[].buff` |
| Đổi cân bằng chất liệu | `DB.gearMats[].mult`, `uses`, `waste`, `spdPenalty` |
| Đổi thưởng bộ | `DB.gearSets` |
| Đổi tốc độ tích Rác | `DB.waste.perPoint`, `decayPerDay`, `cap` |
| Đổi tỉ lệ rơi đồ bền | `DB.gearDrop` |
| Đổi giá đời thật trên thẻ | `GEAR_REAL` trong data |

**Đường cong dự kiến:** ngày 1 mua bộ nhựa (mạnh nhất), ngày 7 Rác chạm trần −20%,
ngày 16 (trung vị) gom đủ bộ inox. Đổi `DB.gearDrop` là đổi cả ba mốc này.

### Bóng dáng theo loài
Bảng `BODY` trong engine: mỗi loài một `path`, một `belly`, một `face` (độ lệch cụm mắt miệng),
tuỳ chọn `join:'miter'` cho loài cần góc nhọn. `clipPath` dùng chính `path` đó nên hoa văn
không tràn ra ngoài thân.

| Muốn | Sửa |
|---|---|
| Đổi dáng một loài | `BODY.<loài>.path` — giữ trong khung tâm (0,20), rộng ~92, cao ~96 |
| Mặt bị lệch sau khi đổi dáng | `BODY.<loài>.face.y` |
| Thêm dáng cho quái Công Nghiệp | thêm mục vào `BODY`, gọi `renderPet(p,{industrial:1})` |

### Hệ trạng thái pet
14 trạng thái, tất cả keyframe mang tiền tố `pp-`, gom trong một khối CSS có chú thích.
Đổi tư thế bằng `setPose('tên')`. Gọi `setPose('idle')` thì hàm tự đổi sang `sad` hoặc `rest`
theo tâm trạng, nên chỗ gọi không cần biết pet đang buồn hay mệt.

| Muốn | Sửa |
|---|---|
| Thêm tư thế mới | `.actor.<tên> .in{animation:pp-<tên>}` + keyframe cùng khối + thêm vào `PET_STATES` |
| Đổi nhịp một tư thế | thời lượng trong khối `HỆ TRẠNG THÁI PET` |
| Đổi khoảng cách toàn app | biến `--s1` đến `--s4` |

**Chỉ dùng `transform` và `opacity` trong keyframe.** Mọi thuộc tính gây bố cục lại
(`filter`, `width`, `height`, `left`, `top`, `box-shadow`) đều làm rớt khung hình.

**Lưu ý về hiệu năng:** đừng thêm `backdrop-filter` hay `filter:blur()` vào phần tử nằm đè lên sân khấu — đó là nguyên nhân khựng hình ở bản v8. Đổi biểu cảm pet phải dùng `paintFace()`, chỉ dùng `paintPet()` khi đổi hẳn con pet.

**Lưu ý về font:** file nhúng sẵn DejaVu Serif Bold đã subset (430 ký tự, 29,8 KB WOFF) vì các font serif hệ thống như Georgia và Iowan Old Style thiếu khối Latin Extended Additional, làm dấu tiếng Việt bị tách rời. Đừng gỡ hai khối `@font-face` này. Có **hai** font nhúng: `PP Serif` cho tiêu đề (DejaVu Serif Bold, 29,8 KB) và `PP Mono` cho nhãn và số (Liberation Mono, 28,5 KB). Ba font hệ thống đã thử và trượt vì thiếu khối Latin Extended Additional: Georgia, Iowan Old Style, DejaVu Sans Mono.

### Sửa nội dung v3
| Muốn | Sửa |
|---|---|
| Đổi độ khó tháp | `DB.tower.power` |
| Thêm chặng / boss | `DB.tower.stages` (đặt `open:true`) |
| Đổi tỉ lệ vé | `DB.tower.ticket` |
| Đổi mức đóng góp pet phụ | `DB.team.statShare` |
| Thêm hạt mầm | `DB.seeds` |
| Cơ chế boss mới | nhánh `f.mech` trong `tick()` của engine |

### Sửa nội dung v2
| Muốn | Sửa |
|---|---|
| Thêm món nội thất | `DB.furniture` + hình trong `FS` |
| Đổi hiệu ứng nội thất | trường `perk`, đọc bởi `perkOf()` |
| Thêm mốc thành tựu | `DB.achievements[].tiers` |
| Đổi nhiệm vụ tuần/tháng | `DB.questsW`, `DB.questsM` |
| Đổi emoji kỹ năng | `DB.skillIcon` |
| Đổi nhịp hoạt cảnh đấu | hàm `playBattle()`, hằng `BD()` |

### Sửa hoạt cảnh
| Muốn | Sửa |
|---|---|
| Pet đi lại thưa hơn | `wanderTick()`, biến `delay` |
| Đổi diễn biến một hành động | đối tượng `SCENE` trong khối Scene |
| Đổi màu trời theo giờ | mảng `SKY` |
| Ngưỡng hiện vết bẩn | `messCount()` |
| Ngưỡng hiện bong bóng nhu cầu | `lowestNeed()`, hiện là < 32 |
| Thêm đồ trang trí trên quầy | `paintProps()` + `PROP` |

## Nhúng vào bộ công cụ quản lý

**Cách nhanh:** đặt `index.html` trong iframe ở một tab của app. Dữ liệu lưu ở localStorage khoá `petpocket.v1`, độc lập với dữ liệu vận hành.

**Cách đúng:** copy ba khối script vào bundle của bộ công cụ, rồi thay hàm `claim()`:

```js
// Bản demo: người dùng tự tick
function claim(id){ ... }

// Bản thật: nhiệm vụ tự sáng theo dữ liệu vận hành. Tuần/tháng dùng bumpQuest('W'|'M', id).
function syncQuests(ops){
  const map = {
    open:   ops.openChecklist.complete,
    pnl:    ops.pnl.lockedFor(today()),
    stock:  ops.inventory.countSavedToday,
    hr:     ops.attendance.completionRate === 1,
    target: ops.revenue.today >= ops.revenue.target,
    close:  ops.closeChecklist.complete
  };
  DB.quests.forEach(q => { if (map[q.id] && !S.quest.done.includes(q.id)) claim(q.id) });
}
```

Người dùng không tự tick được nữa. Đó là điểm khiến xu có giá trị.

## Sửa cân bằng thường gặp

| Muốn | Sửa |
|---|---|
| Pet đói chậm hơn | `DB.decay.hunger` |
| Vắng lâu không bị phạt nặng | `DB.decayRules.floor` |
| Trứng dễ ra đồ hiếm hơn | `DB.eggs[].dist` |
| Trận đấu dài hơn | `DB.battle.maxTurns`, hoặc hệ số HP×4 trong `mkFighter` |
| Quest cho nhiều xu hơn | `DB.quests[].coin` |
| Thêm loài thứ 7 | Thêm vào `DB.species`, `DB.evo`, `DB.counter`, và 6 kỹ năng vào `DB.skills` |

## Đã kiểm chứng bằng mô phỏng
- 3.000 lần tạo pet: phân bố độ hiếm khớp bảng thiết kế.
- 2.000 trận đấu: hai bên cân (51.2% / 48.8%); chênh PP > 15% thì bên mạnh thắng 96.5%.
- Đường cong hao hụt offline 6h/12h/24h/36h/72h: xem `pet-pocket-thiet-ke-v1.md` mục 7.
- 4 bảng xác suất trứng đều cộng đúng 100%.

## Chưa có trong v1.0
- Đấu với pet người thật (hiện là đối thủ sinh tự động khớp PP).
- Đồng bộ nhiều thiết bị (localStorage chỉ nằm trên một máy).
- Âm thanh.
- Nhiều phòng (hiện chỉ có một quầy; hệ nội thất đã sẵn để mở rộng).
- Tài khoản và đồng bộ đám mây.
- Đấu với pet của người thật.
