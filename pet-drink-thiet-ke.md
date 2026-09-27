# Pet Pocket — Thiết kế hệ thống v1.0

Bản này là nguồn sự thật cho toàn bộ số liệu cân bằng. Mọi hằng số đều nằm trong khối `DB` của `index.html`, tên biến trùng với tên trong tài liệu.

**Cách đọc nhãn:**
- `[đo]` — đã chạy mô phỏng và có kết quả cụ thể, ghi kèm trong bài.
- `[giả định]` — con số thiết kế, hợp lý về mặt toán nhưng chưa có người chơi thật xác nhận. Cần chỉnh sau 2 tuần dùng thật.

Nguyên tắc xuyên suốt: **pet phải khác nhau, nhưng luật thì ít**. Cảm giác "sống" đến từ tổ hợp gen × tính cách × lịch sử chăm sóc, không đến từ việc chồng thêm hệ thống.

---

## 1. Sáu loài và chỉ số gốc

Chỉ số gốc tính ở giai đoạn Trưởng thành, Gen 0, độ hiếm Thường, gen trung bình. Tổng 5 chỉ số không tính HP đều bằng **180** để không loài nào mạnh hơn tuyệt đối — khác biệt nằm ở phân bổ và ở điểm yếu chăm sóc.

| Loài | Việt | HP | ATK | DEF | SPD | INT | LUCK | Điểm yếu chăm sóc |
|---|---|---|---|---|---|---|---|---|
| Beano | Hạt cà phê | 85 | 38 | 26 | 46 | 42 | 28 | Năng lượng ×1.4 |
| Milku | Sữa tươi | 115 | 32 | 50 | 24 | 40 | 34 | No ×1.3, Sạch ×1.2 |
| Matcha | Trà xanh | 95 | 30 | 34 | 36 | 50 | 30 | Vui ×1.1 |
| Cacao | Ca cao | 110 | 50 | 40 | 24 | 30 | 36 | No ×1.5 |
| Citrus | Cam chanh | 70 | 40 | 20 | 52 | 28 | 40 | Vui ×1.3, NL ×1.2 |
| Glacio | Đá lạnh | 100 | 28 | 48 | 26 | 34 | 44 | Sạch ×1.5, tan chảy |

**Đặc tính riêng**

| Loài | Ưu | Nhược |
|---|---|---|
| Beano | Rèn luyện hiệu quả +20% | Năng lượng tụt nhanh nhất |
| Milku | Bond tăng nhanh +25% | Mau đói và mau bẩn |
| Matcha | Tinh thần gần như không tụt | Cần chơi thường xuyên |
| Cacao | ATK cao nhất bảng | Đói cực nhanh |
| Citrus | Nhanh nhất, né tốt | HP mỏng nhất, mau chán |
| Glacio | DEF + LUCK cao | Sạch < 30 thì mất dần HP tối đa |

**Tam giác khắc chế:** Beano › Milku › Cacao › Citrus › Matcha › Glacio › Beano. Lợi thế ×1.15, bất lợi ×0.87.

---

## 2. Sáu bậc độ hiếm

| Bậc | Tỉ lệ | Nhân chỉ số | Cộng trần | Số trait |
|---|---|---|---|---|
| Thường | 55.0% | 1.00 | +0 | 0–1 |
| Ít gặp | 25.0% | 1.08 | +5 | 1 |
| Hiếm | 13.0% | 1.18 | +12 | 1–2 |
| Cực hiếm | 5.0% | 1.32 | +20 | 2 |
| Huyền thoại | 1.8% | 1.50 | +30 | 2–3 |
| Thần thoại | 0.2% | 1.75 | +45 | 3 |

`[đo]` 3.000 lần tạo pet ngẫu nhiên trả về: Thường 54.4% · Ít gặp 24.8% · Hiếm 13.7% · Cực hiếm 5.0% · Huyền thoại 2.0% · Thần thoại 0.13%. Sai số nằm trong biên ngẫu nhiên chấp nhận được.

Khoảng cách 1.00 → 1.75 là có chủ ý: đủ để một con Thần thoại đáng khoe, chưa đủ để pet Thường thành vô dụng. `[giả định]`

---

## 3. Mười tính cách

| Tính cách | Chỉ số | Hao hụt | Hành vi |
|---|---|---|---|
| Tò mò | INT ×1.08 | Tinh thần ×1.10 | Khám phá +25% |
| Trung thành | DEF ×1.05 | — | Bond +40% |
| Nghịch ngợm | SPD ×1.05 | Năng lượng ×1.15 | Chơi +30% |
| Lười biếng | SPD ×0.92 | Năng lượng ×0.70 | Rèn −20% |
| Gan dạ | ATK ×1.10, HP ×0.95 | — | Thắng trận +20% |
| Nhút nhát | DEF ×1.10, ATK ×0.92 | — | Tắm +20% |
| Tham ăn | HP ×1.05 | No ×1.25 | Ăn +50% |
| Điềm tĩnh | INT ×1.04 | Mọi thứ ×0.90 | — |
| Bướng bỉnh | ATK ×1.05 | — | Rèn +25%, Bond −25% |
| May mắn | LUCK ×1.15 | — | Trứng & khám phá +20% |

Rơi đều 10% mỗi loại. Mỗi tính cách có một câu thoại riêng, đó là thứ người dùng nhớ chứ không phải con số.

---

## 4. Hai mươi bốn đặc điểm di truyền

Số trait phụ thuộc độ hiếm (bảng mục 2). Trọng số `w` càng cao càng dễ ra.

**Ngoại hình (8)** — thay đổi hình vẽ, không đổi sức mạnh (trừ 3 cái ghi rõ)

| Trait | w | Hiệu ứng |
|---|---|---|
| Bạch tạng | 3 | Bão hoà −45, sáng +35, mắt đỏ |
| Hắc thể | 3 | Sáng −40 |
| Ánh xà cừ | 1.5 | Thân đổi màu theo gradient |
| Đuôi đôi | 3 | Hai đuôi |
| Tai to | 4 | Tai ×1.35, SPD ×1.03 |
| Tí hon | 3 | Kích thước −15%, SPD ×1.06, HP ×0.94 |
| Khổng lồ | 3 | Kích thước +15%, HP ×1.08, SPD ×0.95 |
| Phát sáng | 1 | Quầng sáng quanh thân |

**Chỉ số (6)** — cộng thẳng: Da sắt DEF+12 · Vuốt sắc ATK+12 · Chân nhanh SPD+12 · Đầu sáng INT+12 · Máu dày HP+15 · Cỏ bốn lá LUCK+12. Trọng số 3–4.

**Chăm sóc (6)**

| Trait | w | Hiệu ứng |
|---|---|---|
| Ngủ say | 4 | Hồi Năng lượng ×1.5 |
| Ăn ít | 4 | No tụt ×0.70 |
| Sạch sẽ | 3.5 | Sạch tụt ×0.60 |
| Quấn người | 3.5 | Bond ×1.30 |
| Cú đêm | 3 | 22h–6h mọi chỉ số ×1.10 |
| Dậy sớm | 3 | 5h–11h mọi chỉ số ×1.10 |

**Quý hiếm (4)** — Thiên phú (trần +15 toàn bộ, w 0.8) · Tự phục hồi (+2 Sức khoẻ/giờ, w 1.2) · Gen đột biến (mở nhánh tiến hoá ẩn, w 0.6) · Gia truyền (chắc chắn truyền 1 trait cho đời sau, w 0.8).

Cú đêm và Dậy sớm là hai trait duy nhất gắn với đồng hồ thật. Chúng khiến người chơi mở app đúng khung giờ mà không cần thông báo đẩy.

---

## 5. Bốn mươi hai kỹ năng

6 kỹ năng dùng chung + 6 kỹ năng riêng cho mỗi loài. `[đo]` đã kiểm tra: mỗi loài đúng 6 kỹ năng riêng, không loài nào thiếu.

**Cấu trúc dữ liệu:** `pow` (hệ số sát thương) · `cost` (sức, mỗi trận có 100, hồi 6/lượt) · `scale` (chỉ số dùng để tính) · `stage` (mở khoá ở giai đoạn nào) · `fx` (hiệu ứng phụ).

**Dùng chung:** Húc 1.00/8 · Thủ thế (DEF+35%, 2 lượt) · Tập trung 0.85/10 theo INT, không né được · Nghỉ (hồi 20% HP, 1 lần/trận) · Bước nhanh (SPD+30%) · Cắn 1.22/14.

**Beano** — nhanh, đốt: Bùng caffeine (SPD ×2, tự mất 5% HP) · Bắn hạt 1.32 theo SPD · Rang (bỏng 5%/lượt) · Espresso 1.60 theo INT · Lớp crema (chắn 25%) · Hai shot (2 đòn ×0.72).

**Milku** — chống chịu, hồi: Áo sữa (DEF+55%) · Tường bọt (chặn 1 đòn) · Kem hồi (26% HP) · Bổ canxi (DEF+15 hết trận) · Tạt sữa (giảm SPD địch) · Nuôi dưỡng (8%/lượt × 3).

**Matcha** — kéo dài, gỡ debuff: Thiền (xoá debuff + hồi 8%) · Cắt lá (chảy máu) · Toả hương (ATK địch −20%) · Diệp lục (6%/lượt × 4) · Vị chát (xuyên 30% DEF) · Nhập định (INT+25%).

**Cacao** — sát thương nặng: Đập ca cao 1.58 · Cơn giận đắng (ATK+35% khi HP<40%) · Vỏ cứng · Ném truffle (20% choáng) · Nở tối (hút 35% máu) · Ganache nghiền 2.00/30.

**Citrus** — nhanh, né, chí mạng: Vỏ chanh (SPD+45%, đi trước) · Xịt axit (DEF địch −25%) · Lách vỏ (né 45%) · Bùng vitamin · Chém chua (chí mạng +28%) · Sốc chua (25% choáng).

**Glacio** — khoá đối thủ: Giáp băng (DEF+60%, phản 12%) · Mảnh băng theo SPD · Đóng băng (32% choáng) · Hơi lạnh (SPD địch −20% hết trận) · Sông băng 1.80 · Tan tuyết.

Số ô mang theo: **3**, lên **4** khi Bond ≥ 80.

---

## 6. Cây tiến hoá

**Giai đoạn:** Trứng → Sơ sinh → Thiếu niên → Trưởng thành → Tiến hoá.

| Giai đoạn | Nhân chỉ số | Điều kiện | Hao hụt |
|---|---|---|---|
| Sơ sinh | 0.55 | mặc định | ×1.30 |
| Thiếu niên | 0.78 | 2 ngày + Lv 4 | ×1.10 |
| Trưởng thành | 1.00 | 5 ngày + Lv 10 | ×1.00 |
| Tiến hoá | 1.18 | 9 ngày + Lv 18 | ×0.95 |

**Bốn nhánh, xét theo thứ tự từ trên xuống — dừng ở điều kiện đầu tiên thoả:**

| Nhánh | Điều kiện |
|---|---|
| Ẩn | Có Gen đột biến · Bond ≥ 90 · ≥ 10 ngày tuổi · mọi chỉ số ≥ 85 |
| Trí | Khám phá ≥ 30 lần · Tinh thần ≥ 70 |
| Chiến | Rèn luyện ≥ 40 lần hoặc thắng ≥ 15 trận |
| Chăm | Mặc định |

| Loài | Chăm | Chiến | Trí | Ẩn |
|---|---|---|---|---|
| Beano | Barista Beano | Ristretto | Cold Brew Oracle | Geisha Prime |
| Milku | Latte Milku | Butter Bull | Cheese Sage | Golden Cream |
| Matcha | Usucha | Koicha Blade | Zen Master | Hojicha Phantom |
| Cacao | Truffle Cacao | Brute Cacao | Alchemist | 100% Dark |
| Citrus | Yuzu Citrus | Chili-Lime | Bergamot Seer | Blood Orange |
| Glacio | Gelato | Frostbite | Crystal Sage | Nitro Glacio |

24 dạng trưởng thành + 18 dạng chưa lớn = **42 mục sổ sưu tầm**.

Nhánh do lịch sử chăm sóc quyết định, không phải do người chơi bấm chọn. Đó là chỗ "lịch sử riêng" trở thành thứ nhìn thấy được.

---

## 7. Công thức hao hụt theo giờ offline

Thang 0–100. Hao hụt cơ bản mỗi giờ:

```
No       −4.0/h
Năng lượng −2.5/h
Sạch     −1.8/h
Vui      −1.2/h   (thêm −2.5/h nếu No < 20)
Tinh thần −0.8/h  (thêm −2.0/h nếu Năng lượng < 20 hoặc Sạch < 20)
```

**Nhân hệ số:** `hao hụt = cơ bản × loài × tính cách × trait × giai đoạn × số giờ`

**Ba luật bảo vệ:**

1. **Ân hạn 8 giờ đầu** chỉ tính 50%. Ngủ một đêm không bị phạt.
2. **Trần 48 giờ.** Vắng 3 ngày hay 3 tuần đều như nhau.
3. **Sàn khi vắng mặt:** No 12 · Năng lượng 15 · Sạch 12 · Vui 22 · Tinh thần 20 · Sức khoẻ 40. Sàn chỉ áp dụng cho hao hụt offline. Bỏ bê khi đang mở app thì rơi tự do.

**Sức khoẻ** không tự tụt mà chỉ phản ứng theo điều kiện:

| Điều kiện | Sức khoẻ/giờ |
|---|---|
| No < 20 | −1.5 |
| Sạch < 20 | −1.0 |
| Năng lượng < 10 | −1.0 |
| Tinh thần < 20 | −0.8 |
| Cả 5 chỉ số ≥ 70 | +0.8 |

`[đo]` Đường cong thực tế của một con Beano bắt đầu từ 80 tất cả:

| Vắng | No | NL | Vui | Sạch | Tinh thần | Sức khoẻ | Bệnh |
|---|---|---|---|---|---|---|---|
| 6h | 59 | 66 | 75 | 73 | 77 | 90 | — |
| 12h | 34 | 44 | 68 | 61 | 72 | 90 | — |
| 24h | 12 | 15 | 22 | 33 | 20 | 60 | — |
| 36h | 12 | 15 | 22 | 12 | 20 | 40 | Cảm lạnh |
| 72h | 12 | 15 | 22 | 12 | 20 | 40 | Cảm lạnh |

`[đo]` Một vòng chăm sóc sau 24h vắng (3 lần ăn, 2 lần tắm, 1 lần ngủ, 2 lần chơi) đưa về: No 90 · Sạch 97 · Năng lượng 53 · Vui 58. Tức là **hồi phục được trong một phiên**, không cần cày nhiều ngày.

Đây là điểm mình sửa so với bản gốc. Prototype v0.1 dùng trần 24h không sàn, mô phỏng ra: vắng 48h là mọi chỉ số về 0 và mắc 5 bệnh cùng lúc. Với người dùng là chủ quán — nghỉ chủ nhật, đi công tác 2 ngày — thiết kế đó sẽ khiến họ gỡ app sau tuần đầu.

---

## 8. Bệnh và cách chữa

| Bệnh | Kích hoạt | Hiệu ứng | Trừ SK/h | Cách chữa |
|---|---|---|---|---|
| Đói lả | No < 10 liên tục 6h | ATK ×0.70 | −2.0 | Cho ăn 3 lần |
| Cảm lạnh | Sạch < 25 và NL < 30, 4h | SPD ×0.80 | −0.5 | Ngủ 2 lần |
| Nhiễm bẩn | Sạch < 10 liên tục 12h | DEF ×0.75 | −3.0 | Tắm 2 lần |
| Kiệt sức | Rèn 10 lần không ngủ | Mọi chỉ số ×0.85 | −0.5 | Ngủ 3 lần (khoá Rèn) |
| Trầm cảm | Vui < 20 liên tục 24h | INT ×0.80 | −0.3 | Chơi 5 lần (EXP ×0.5) |
| Rối loạn tiêu hoá | Ăn > 8 lần/ngày | — | 0 | Nhịn 12h (No nhận ×0.5) |
| Sốt | Sức khoẻ < 30 | Mọi chỉ số ×0.75 | −1.0 | Ngủ 2 lần |
| Tan chảy | Glacio, Sạch < 30 quá 6h | HP ×0.90 | −0.5 | Tắm 2 lần (−10% HP tối đa/ngày) |

Mọi bệnh đều chữa bằng hành động chăm sóc có sẵn, **không cần mua vật phẩm**. Bệnh là lời nhắc chứ không phải bức tường trả phí.

`[đo]` Với sàn ở mục 7, vắng 24h không phát bệnh; vắng 36h phát đúng 1 bệnh nhẹ. Riêng Glacio phát thêm Tan chảy ở 24h — đó là nhược điểm loài đã ghi rõ trước khi người chơi chọn.

---

## 9. Thuật toán sinh gen

**Cấu trúc DNA**

```
dna = {
  hue    : 0–359     màu chính, dải riêng theo loài
  sat    : 46–86     độ bão hoà
  light  : 46–64     độ sáng
  pattern: 0–5       trơn | đốm | sọc | mảng | chuyển sắc | vân
  size   : 0.88–1.12 kích thước
  ear, tail : 0–3    biến thể hình dạng
  genes  : { hp, atk, def, spd, int, luck } mỗi cái 0–100
}
```

**Gen 0 (không bố mẹ):** `gene = round(mean(3 lần random 0–1) × 100)`. Trung bình 3 lần cho phân bố chuông quanh 50 — tránh việc pet đầu tiên hoặc quá tệ hoặc quá mạnh.

**Đời sau (lai tạo):**

```
gene_con = clamp( (gene_bố + gene_mẹ)/2 + N(0, 8), 0, 100 )
5% khả năng đột biến: gene_con ± random(15, 25)
hue_con  = trung bình hue bố mẹ + N(0, 14);  8% khả năng random hoàn toàn
trait    = 55% lấy từ pool bố mẹ, 45% random mới; trait Gia truyền đảm bảo 1 slot
gen      = max(gen_bố, gen_mẹ) + 1
```

Rồi cộng thêm theo độ hiếm: `gene += bậc_hiếm_index × 3`.

**Trần tiềm năng**

```
trần[k] = base_loài[k] × nhân_hiếm × (0.85 + gene[k]/100 × 0.45)
        + Thiên_phú × (1.5 nếu HP, ngược lại 1)
        + min(20, gen × 2)
        + cộng_thẳng_từ_trait
```

Gen 0 cho ×0.85, gen 100 cho ×1.30. Kết hợp với nhân độ hiếm 1.00–1.75, khoảng cách tổng giữa pet tệ nhất và tốt nhất là khoảng **2.7 lần**.

**Chống lạm phát đời:** mỗi đời cộng +2 trần (tối đa +20) nhưng **hao hụt chăm sóc +1%/đời (tối đa +20%)**. Lai nhiều đời thì mạnh hơn nhưng khó nuôi hơn. Không có cách nào lai vô hạn để phá game.

**Chỉ số hiện tại**

```
hiện_tại[k] = trần[k] × nhân_giai_đoạn × (0.55 + 0.45 × trưởng_thành) + thưởng_rèn[k]
trưởng_thành = (level − 1) / 29
thưởng_rèn[k] ≤ 15% × trần[k]
```

---

## 10. Bảng xác suất trứng

| Loại | Giá | Ấp | Thường | Ít gặp | Hiếm | Cực hiếm | Huyền thoại | Thần thoại |
|---|---|---|---|---|---|---|---|---|
| Trứng thường | 200 xu | 6h | 62 | 26 | 9 | 2.5 | 0.5 | 0 |
| Trứng hiếm | 500 xu | 12h | 30 | 38 | 22 | 8 | 1.8 | 0.2 |
| Trứng cổ | 1200 xu | 24h | 5 | 20 | 40 | 25 | 9 | 1 |
| Trứng vàng | không bán | 48h | 0 | 5 | 30 | 43 | 18 | 4 |

`[đo]` Bốn hàng đều cộng đúng 100%.

**Nguồn trứng**
- Khám phá: 5% mỗi lần (tính cách May mắn ×1.2)
- Chuỗi 7 ngày làm quest vận hành: 1 Trứng hiếm
- Chuỗi 30 ngày: 1 Trứng cổ
- Đạt mục tiêu doanh thu ngày: 5% ra Trứng thường
- Lai 2 pet Cực hiếm trở lên: Trứng vàng
- Cửa hàng: mua bằng xu, mà xu chỉ đến từ việc vận hành thật

Thời gian ấp chạy theo đồng hồ thật, đóng app vẫn tính. Mở khoá 75% sổ sưu tầm thì giảm 20% thời gian ấp.

---

## 11. Công thức Pet Power

```
PP = ( HP×0.5 + ATK×1.6 + DEF×1.4 + SPD×1.3 + INT×1.2 + LUCK×0.8 )
     × (1 + tổng_bậc_kỹ_năng / 100)
```

Trong đó mỗi chỉ số đã là **chỉ số hiệu dụng**, tức đã nhân đủ chuỗi:

```
hiệu_dụng[k] = hiện_tại[k]
             × tính_cách × trait × bệnh
             × (1 + thưởng_bond)
             × hệ_số_chăm_sóc

hệ_số_chăm_sóc = 0.70 + 0.30 × (trung bình 6 chỉ số / 100)
```

Hệ số chăm sóc là mấu chốt: một con Thần thoại bị bỏ đói chỉ đạt 0.70, một con Thường được chăm kỹ đạt 1.00. Chăm sóc bù được khoảng **43% chênh lệch** — đủ để việc chăm sóc có ý nghĩa, chưa đủ để độ hiếm thành vô nghĩa.

`[đo]` Phân bố PP: Sơ sinh trung vị 92 (khoảng 82–124). Trưởng thành Lv18 trung vị 248 (khoảng 221–332).

---

## 12. Công thức đấu PvP

Đấu tự động, tối đa **20 lượt**. Mỗi bên có **100 sức**, hồi **6/lượt**.

**Thứ tự ra đòn:** `SPD + random(0,10)`, hoà thì xét LUCK. Kỹ năng có cờ `first` luôn đi trước.

**Sát thương**

```
dmg = chỉ_số_scale × pow_kỹ_năng × (1 + INT/400)
    × 100 / (100 + DEF_hiệu_dụng)
    × random(0.86, 1.16)
    × khắc_chế
```

**Chí mạng:** `tỉ lệ = 4% + LUCK/12 + bonus_kỹ_năng`, trần **25%**, sát thương ×1.6.

**Né:** `tỉ lệ = (SPD_thủ − SPD_công)/3 + LUCK_thủ/40`, trần **18%**. Kỹ năng có `acc` thì không né được.

**Khắc chế:** lợi thế ×1.15, bất lợi ×0.87.

**Bond ≥ 95:** hồi sinh 1 lần mỗi trận với 35% HP.

**HP trong trận** = HP hiệu dụng × 4, để trận kéo dài đủ để kỹ năng và hiệu ứng kịp thể hiện.

`[đo]` Kết quả 2.000 trận:
- Hai pet cùng cấu hình ngẫu nhiên: tỉ lệ thắng bên A **51.2%** — cân.
- Chênh lệch PP > 15%: bên mạnh hơn thắng **96.5%** — PP dự đoán đúng kết quả.
- Độ dài trung bình: **34 dòng nhật ký**, đọc hết khoảng 20 giây.

Con số 96.5% là có chủ ý. Người dùng chính là chủ quán, không phải game thủ — họ cần thấy "chăm kỹ thì thắng", không cần cảm giác hên xui.

**PvP không cần máy chủ:** đối thủ được sinh ra bằng cách thử 14 pet ngẫu nhiên và giữ con có PP gần với pet của người chơi nhất. Khi cần đấu người thật, xuất snapshot pet thành chuỗi và đấu lại bản ghi đó — không cần backend.

---

## 13. Thang gắn bó 0–100

| Mốc | Tên | Thưởng chỉ số | Mở khoá |
|---|---|---|---|
| 0 | Xa lạ | +0% | — |
| 20 | Quen mặt | +2% | — |
| 40 | Thân | +5% | Pet chủ động đòi chơi |
| 60 | Gắn bó | +8% | Nhánh tiến hoá Chăm |
| 80 | Tri kỷ | +12% | Ô kỹ năng thứ 4 |
| 95 | Linh hồn | +18% | Hồi sinh 1 lần/trận |

**Tăng:** Chơi +3 · Tắm +2 · Khám phá +2 · Cho ăn khi No < 40 +2 · Ngủ +1 · Thắng +2 · Thua +1 · Vuốt ve +0.2 (tối đa +3/ngày) · Đăng nhập +1.

**Giảm:** Đói < 15 quá 24h −3 · Bỏ bê > 48h −5 · Bệnh không chữa −2/ngày · Không tương tác −0.5/ngày.

**Nhân hệ số:** tính cách Trung thành ×1.4, Bướng bỉnh ×0.75, trait Quấn người ×1.3, loài Milku ×1.25.

Từ 0 lên 95 mất khoảng **12–18 ngày chơi đều**. `[giả định]` — cần dữ liệu thật để chốt.

---

## 14. Sổ sưu tầm

**42 mục** = 6 loài × (Sơ sinh + Thiếu niên + Trưởng thành + 4 dạng tiến hoá).

Mỗi mục mới: **+30 xu**.

| Mốc | Thưởng |
|---|---|
| 25% | +5% xu nhận được |
| 50% | Mở ô kỹ năng thứ 4 |
| 75% | Giảm 20% thời gian ấp trứng |
| 100% | Mở bán Trứng vàng trong cửa hàng |

Ngoài ra theo dõi riêng: 24 trait đã gặp, 42 kỹ năng đã học.

Sổ hiển thị hình bóng **cố định** cho mỗi mục — cùng một loài luôn cùng một màu tham chiếu, để người chơi nhận ra ngay mình còn thiếu gì.

---

## 15. Giao diện dữ liệu cho developer

```ts
type StatKey = 'hp'|'atk'|'def'|'spd'|'int'|'luck';
type CareKey = 'health'|'hunger'|'energy'|'happy'|'clean'|'mental';
type SpeciesId = 'beano'|'milku'|'matcha'|'cacao'|'citrus'|'glacio';
type RarityId  = 'common'|'uncommon'|'rare'|'epic'|'legendary'|'mythic';
type StageId   = 'egg'|'baby'|'teen'|'adult'|'evo';
type FormId    = 'care'|'battle'|'mind'|'hidden';

interface DNA {
  hue: number;            // 0–359
  sat: number;            // 46–86
  light: number;          // 46–64
  pattern: 0|1|2|3|4|5;
  size: number;           // 0.88–1.12
  ear: 0|1|2|3;
  tail: 0|1|2|3;
  genes: Record<StatKey, number>;   // 0–100
}

interface Ailment { id: string; since: number; prog: number }

interface Pet {
  id: string;
  name: string;
  species: SpeciesId;
  rarity: RarityId;
  pers: string;                     // id tính cách
  dna: DNA;
  traits: string[];                 // 0–3 id trait
  gen: number;                      // 0 = đời đầu
  born: number;                     // epoch ms
  stage: StageId;
  form: FormId | null;
  level: number;                    // 1–30
  exp: number;
  bond: number;                     // 0–100
  care: Record<CareKey, number>;    // 0–100
  trainBonus: Record<StatKey, number>;
  hist: {
    feed:number; play:number; clean:number; sleep:number;
    train:number; explore:number; win:number; lose:number; pat:number;
  };
  skills: string[];                 // đã học
  equipped: string[];               // 3, hoặc 4 khi bond ≥ 80
  ailments: Ailment[];
  streakTrain: number;
  todayFeed: number;
  todayPat: number;
  maxHpPenalty: number;             // % HP tối đa bị mất (Tan chảy)
}

interface EggInstance { id: string; type: 'common'|'rare'|'ancient'|'golden'; start: number }

interface SaveState {
  v: 1;
  coin: number;
  last: number;                     // epoch ms lần lưu cuối, dùng để mô phỏng offline
  started: number;
  pet: Pet;
  stash: Pet[];                     // pet trong chuồng, không hao hụt
  dex: Record<string, 1>;           // key "species:stage" hoặc "species:form"
  eggs: EggInstance[];
  quest: { date: string; done: string[]; streak: number };
  perks: string[];                  // 'coin5' | 'slot4' | 'hatch20' | 'goldshop'
}
```

**Hàm cần biết khi tích hợp**

| Hàm | Trả về |
|---|---|
| `makePet(opts)` | Pet mới. `opts`: species, rarity, pers, parents |
| `simulate(pet, hours)` | Áp hao hụt offline, tự phát bệnh |
| `effStats(pet)` | Chỉ số hiệu dụng sau mọi hệ số |
| `petPower(pet)` | Số PP |
| `battle(A, B)` | `{ winner, log, f1, f2 }` |
| `renderPet(pet, opt)` | Chuỗi SVG dựng từ DNA |
| `checkStage(pet)` | Id giai đoạn mới, hoặc null |
| `claim(questId)` | Ghi nhận quest vận hành, cộng xu |

---

## Nối với công cụ quản lý F&B

Xu **không mua được bằng tiền và không rơi tự do**. Toàn bộ nguồn xu đến từ hành vi vận hành thật:

| Việc | Xu | Thưởng thêm |
|---|---|---|
| Mở ca đúng giờ | 15 | +5 Năng lượng |
| Nhập doanh thu / P&L hôm nay | 20 | — |
| Kiểm kho cuối ngày | 25 | +15 No |
| Chấm công đủ 100% nhân sự | 30 | — |
| Đạt mục tiêu doanh thu ngày | 50 | 5% ra trứng |
| Đóng ca và vệ sinh | 15 | +8 Sạch |

Tối đa **155 xu/ngày**. Một quả Trứng thường 200 xu, tức khoảng 1.5 ngày làm việc đầy đủ.

Chuỗi 7 ngày ra Trứng hiếm, chuỗi 30 ngày ra Trứng cổ. Bỏ một ngày là chuỗi về 0.

**Điểm quan trọng khi nhúng thật:** trong bản demo, người dùng tự tick quest. Khi ghép vào bộ công cụ, thay lời gọi `claim(id)` bằng kiểm tra dữ liệu thật — checklist mở/đóng ca đã đủ, kỳ P&L đã khoá, phiếu kiểm kho đã lưu, chấm công không thiếu ai, doanh thu ngày ≥ target. Quest tự sáng khi số liệu về, người dùng không tự tick được. Nếu không làm bước này, vòng lặp gamification mất toàn bộ ý nghĩa.

---

## Những giả định cần kiểm chứng bằng người dùng thật

1. `[giả định]` **155 xu/ngày so với 200 xu/trứng** là tỉ lệ đủ hấp dẫn. Nếu người dùng thấy quá chậm sẽ bỏ; quá nhanh thì trứng mất giá trị.
2. `[giả định]` **12–18 ngày để Bond đạt 95**. Chưa có dữ liệu về tần suất mở app thật của chủ quán.
3. `[giả định]` **Chuỗi về 0 khi bỏ một ngày** có thể quá gắt với ngành F&B — quán đóng cửa ngày lễ, chủ đi công tác. Cân nhắc cơ chế "1 lần bảo hiểm chuỗi mỗi tháng".
4. `[giả định]` **Đấu tự động 20 lượt** đủ hấp dẫn để quay lại. Cũng có thể người dùng chỉ quan tâm phần chăm sóc và bỏ hẳn phần đấu — nếu vậy thì cắt PvP, giữ 42 kỹ năng làm chỉ số trưng bày.
5. Chưa kiểm chứng: gamification có thực sự làm tăng tỉ lệ hoàn thành checklist vận hành hay không. Đây là câu hỏi cần đo bằng chính bộ công cụ, so sánh tỉ lệ hoàn thành trước và sau khi bật mini game.

---

# Phụ lục v1.1 — Lớp tương tác và hoạt cảnh

## Lỗi bố cục đã sửa
Ở bản v1.0, khung SVG của pet đặt `width:100%;height:100%` bên trong một ô lưới cao tự động. Trên màn hình rộng (iPad dọc, 744 px), phần trăm chiều cao không phân giải được nên trình duyệt kéo SVG thành 520×520, tràn khỏi khung 212 px và bị khay hoá đơn che mất, chỉ còn thấy hai tai.

Sửa bằng cách cho khung pet chiều cao xác định và đặt nhân vật tuyệt đối bên trong. `[đo]` Kiểm tra lại ở 744×1000 và 390×844: không còn chồng lấn, pet nằm trọn trong khung.

## Cấu trúc lớp trên sân khấu

| Lớp | z-index | Chứa gì |
|---|---|---|
| `.room` | 0 | Nền tường, đổi màu theo giờ |
| `.win` `.lamp` `.shelf` `.jars` | 1 | Cửa sổ, đèn thả, kệ, hũ |
| `#world` | 3 | Đồ đặt trên quầy nằm sau pet: tách cà phê |
| `#actor` | 4 | Nhân vật |
| `#dim` | 5 | Lớp tối khi ngủ |
| `#fore` | 6 | Hạt hiệu ứng, vết bẩn, bong bóng nhu cầu |

Tách hai lớp trước/sau là bắt buộc: ở bản đầu tất cả nằm chung một lớp dưới nhân vật, nên khung chạm 204×204 của pet nuốt hết click vào vết bẩn. `[đo]` Đã kiểm tra bằng `elementFromPoint` và click thật.

## Nhân vật sống ra sao khi không ai chạm vào

Vòng lặp nền, chỉ chạy khi đang ở tab Nhà và tab trình duyệt đang hiển thị:

- **Đi lại**: mỗi 2.6–6.8 giây chọn một trong ba việc — đứng nhìn quanh (18%), nhảy vui nếu Vui > 60 (12%), hoặc đi tới một vị trí khác trên quầy. Nhân vật tự lật mặt theo hướng đi.
- **Nằm nghỉ**: Năng lượng < 20 thì bỏ đi lại, chuyển sang tư thế thở đều.
- **Chớp mắt**: mỗi 3–7 giây, 110 ms.
- **Hơi nước**: tách cà phê trên quầy bốc hơi liên tục — dấu hiệu quán vẫn mở.

## Ánh sáng theo giờ thật

Không dùng bầu trời mở mà dùng **một ô cửa sổ**, vì bối cảnh là trong quán chứ không phải ngoài trời. Cửa sổ đổi màu, mặt trời/mặt trăng chạy ngang theo giờ, sao hiện ban đêm, đèn thả trên quầy bật chùm sáng ấm khi trời tối. Tường và lớp phủ màu cũng dịch theo.

| Khung giờ | Cửa sổ | Đèn quầy |
|---|---|---|
| 0–5 | Đêm, có sao | Sáng ấm |
| 5–7 | Bình minh | Mờ |
| 7–16 | Ban ngày | Tắt |
| 16–19 | Hoàng hôn | Mờ |
| 19–24 | Đêm, có sao | Sáng ấm |

Hai trait Cú đêm và Dậy sớm ăn theo đồng hồ này, nên khung giờ có tác dụng thật chứ không chỉ trang trí.

## Bốn cách chạm vào pet

| Thao tác | Kết quả |
|---|---|
| Chạm | Pet nhảy lên, thả tim, nói một câu theo tính cách. Bond +0.2 |
| Giữ | Xoa liên tục, tim bay ra mỗi 260 ms, Bond +0.1 mỗi nhịp |
| Kéo ngang | Nhấc pet đi chỗ khác, pet ngọ nguậy. Thả ra thì đi lại bình thường |
| Chạm vết bẩn | Lau sạch, bong bóng bay lên. Sạch +9, Bond +0.3 |

Trần Bond từ vuốt ve vẫn là +3 mỗi ngày như bảng mục 13 — thao tác nhiều hơn không phá cân bằng.

**Bong bóng nhu cầu:** khi một chỉ số tụt dưới 32, một bong bóng suy nghĩ hiện cạnh đầu pet với biểu tượng tương ứng. Chạm vào là chạy luôn hành động đó. Đây là đường tắt cho người dùng đang bận — vào app, thấy bóng, chạm một cái, xong.

**Vết bẩn:** Sạch < 45 hiện 1 vết, < 32 hiện 2, < 20 hiện 3. Không lưu vào bộ nhớ, suy ra thẳng từ chỉ số Sạch nên không phát sinh trạng thái mới.

## Sáu hoạt cảnh

Mỗi hành động dài 1.8–2.6 giây, khoá nút trong lúc chạy để không bấm chồng.

| Hành động | Diễn biến |
|---|---|
| Cho ăn | Bát trượt lên quầy, pet đi tới, rung 3 nhịp, vụn bắn ra, bát mờ đi |
| Chơi | Bóng rơi xuống nảy, pet chạy sang phải rồi sang trái đuổi theo, nhảy mừng |
| Tắm | 12 bong bóng bay lên, pet rũ mình, giọt nước văng, lấp lánh |
| Ngủ | Màn hình tối 55%, pet thở đều, 5 chữ z bay lên, sáng lại |
| Rèn | Tạ hiện lên, pet nhún 4 nhịp, mồ hôi rơi |
| Khám phá | Pet đi ra mép phải rồi biến mất, hiện lại ở mép trái, mang túi về, xu bay lên |

Toàn bộ dựng bằng SVG nội tuyến và CSS. Không thêm file ảnh nào — bộ cài từ 100 KB lên **152 KB**.

## Còn thiếu so với blueprint 8 hệ thống

Bản này mới phủ 01 Pet, 02 Care, 04 Economy (một phần), 05 Quest, 06 Collection, 07 Social (chỉ PvP với đối thủ sinh tự động).

Chưa có: **03 Home System** (phòng, nhà, vườn — hiện chỉ có một quầy cố định) và **08 Online** (tài khoản, đồng bộ đám mây, bảng xếp hạng). Hai phần này cần backend, không nhét vào bản offline một file được. Nếu làm, nên dùng chính Supabase mà anh đã chọn cho bộ công cụ, không dựng hạ tầng riêng.

Đạo cụ trên quầy hiện là bước đệm cho Home System: cấu trúc `propAt()` và lớp `#world` đã sẵn để thả thêm đồ nội thất mua bằng xu.

---

# Phụ lục v2 — Đổi tên, cửa hàng, nhiệm vụ theo kỳ, thành tựu, đấu có hoạt cảnh

## Đổi tên pet
Chạm vào tên hoặc biểu tượng bút chì trong khay hoá đơn. Tối đa 14 ký tự. Enter để lưu, Escape để huỷ.

## Khay hoá đơn gọn lại
Mặc định chỉ hiện: tên, loài, độ hiếm, tính cách, giai đoạn, cấp, **6 thanh chỉ số**, và Pet Power. Toàn bộ phần Gắn bó, Kinh nghiệm, Tuổi, 6 chỉ số chiến đấu, trần tiềm năng và danh sách đặc điểm nằm sau nút **Xem chi tiết**. Trạng thái gấp/mở được lưu lại.

**Thanh chỉ số phát sáng:** mỗi thanh có gradient và quầng sáng đổ theo màu, cộng một vệt sáng quét qua mỗi 2.6 giây. Thanh dưới 25 chuyển đỏ và quét nhanh gấp đôi để đập vào mắt. Màu: xanh ≥ 55, vàng 25–54, đỏ < 25.

## Cửa hàng nội thất — 17 món

| Nhóm | Món | Giá | Hiệu ứng thật |
|---|---|---|---|
| Trên quầy | Máy pha espresso | 420 | Hồi 0.4 Năng lượng mỗi giờ |
| | Cối xay tay | 180 | Cho ăn hiệu quả +15% |
| | Lọ hoa nhỏ | 120 | Vui tụt chậm hơn 8% |
| | Chuông gọi món | 90 | Chạm để gọi pet chạy tới |
| Sàn | Cây monstera | 260 | Tinh thần tụt chậm hơn 12% |
| | Thảm dệt | 200 | Sạch tụt chậm hơn 12% |
| | Ghế đẩu gỗ | 150 | Hồi 0.3 Vui mỗi giờ |
| | Bao cà phê | 130 | Trang trí |
| Tường | Bảng menu phấn | 240 | Nhận thêm 4% xu từ nhiệm vụ |
| | Đồng hồ quầy | 170 | Ấp trứng nhanh hơn 8% |
| | Tranh hạt rang | 150 | Trang trí |
| | Kệ ly xếp | 210 | Tắm hiệu quả +15% |
| Đèn | Đèn dây ấm | 280 | Gắn bó tăng nhanh hơn 10% |
| | Đèn neon OPEN | 360 | Khám phá thu về nhiều hơn 20% |
| Nền | Tường gạch mộc / ván gỗ / gạch men | 300–340 | Đổi nền quán |

Mỗi vị trí chỉ chứa một món; bày món mới cùng vị trí thì món cũ tự vào kho. Đồ đã mua bật/tắt tuỳ ý, không mất xu. Hiệu ứng cộng dồn qua hàm `perkOf()` trong engine, chạm vào đúng bốn chỗ: tốc độ hao hụt, hồi phục theo giờ, hiệu quả hành động, và hệ số xu/ấp trứng.

Đặt máy pha espresso thì tách cà phê mặc định trên quầy tự biến mất — coi như đã nâng cấp thiết bị.

## Nhiệm vụ theo kỳ

Ba tab. Ngày đặt lại theo lịch, tuần đặt lại thứ Hai theo chuẩn ISO, tháng đặt lại ngày 1.

**Hằng ngày** giữ nguyên 6 việc cũ, tối đa 155 xu.

**Hằng tuần** — tiến độ cộng dồn trong tuần:

| Nhiệm vụ | Cần | Thưởng |
|---|---|---|
| Khoá số liệu 6/7 ngày | 6 | 120 xu |
| Kiểm kho 3 lần | 3 | 100 xu |
| Không ca nào thiếu chấm công | 7 | 140 xu |
| Đạt mục tiêu doanh thu 4 ngày | 4 | 180 xu + Trứng hiếm |
| Ghi nhận hao hụt mỗi ngày | 7 | 110 xu |

**Hằng tháng:**

| Nhiệm vụ | Thưởng |
|---|---|
| Chốt P&L tháng | 400 xu |
| Kiểm kê tồn kho cuối tháng | 450 xu + Trứng cổ |
| Đánh giá KPI nhân sự | 380 xu |
| Cập nhật giá vốn công thức | 420 xu |
| Một buổi đào tạo nội bộ | 350 xu + 1 món nội thất ngẫu nhiên |

Trần thu nhập mỗi tháng: khoảng 155×30 + 650×4 + 2000 = **9.250 xu**. Toàn bộ 17 món nội thất cộng lại là 3.760 xu, nên một tháng làm việc đều tay đủ bày cả quán và vẫn còn dư mua trứng.

## Thành tựu — 10 nhóm, 33 mốc

Cộng dồn, không đặt lại, phải chạm để nhận.

| Nhóm | Các mốc | Xu |
|---|---|---|
| Thời gian dùng công cụ | 1 / 5 / 20 / 50 / 100 / 250 giờ | 50 → 4.000 |
| Chuỗi ngày liên tiếp | 7 / 30 / 100 | 120 → 2.000 |
| Nhiệm vụ hoàn thành | 25 / 100 / 365 | 100 → 1.500 |
| Lần chăm sóc pet | 50 / 250 / 1.000 | 60 → 1.000 |
| Trận thắng | 10 / 50 / 200 | 120 → 2.000 |
| Trứng đã nở | 5 / 20 / 60 | 100 → 1.500 |
| Mục sổ sưu tầm | 10 / 25 / 42 | 150 → 2.500 |
| Đời lai cao nhất | 2 / 5 / 10 | 200 → 3.000 |
| Gắn bó cao nhất | 60 / 95 | 100 → 600 |
| Món nội thất sở hữu | 3 / 8 / 17 | 100 → 1.500 |

Đồng hồ thời gian cộng 1 phút cho mỗi phút tab đang mở và không ẩn. Đóng tab hoặc chuyển app thì dừng đếm — chống việc để máy chạy qua đêm lấy xu.

## Trận đấu có hoạt cảnh

Hàm `battle()` nay trả về nhật ký có cấu trúc: mỗi sự kiện ghi phe ra đòn, kỹ năng, sát thương, có chí mạng hay không, có khắc chế hay không, và HP hai bên ngay sau sự kiện. Trình phát đọc nhật ký đó và dựng lại.

| Sự kiện | Hiển thị |
|---|---|
| Bắt đầu lượt | Chữ "Lượt N" hiện lên rồi tan |
| Ra đòn | Pet lao tới, vệt chém quét ngang, đối thủ giật và loé sáng, số sát thương bay lên |
| Chí mạng | Số sát thương màu cam kèm dấu chấm than |
| Khắc chế | Nhãn "lợi thế" hiện bên phe tấn công |
| Né / Chặn | Nhãn xanh, không mất máu |
| Buff / Hồi | Mũi tên hoặc chữ "+hồi", thanh HP nhích lên |
| Choáng | Nhãn vàng, mất lượt |
| Kết thúc | Bên thua ngả xuống, xám lại |

Tốc độ 1× / 2× / 4× và nút Bỏ qua. Nhật ký chữ vẫn giữ nguyên bên dưới cho ai muốn đọc kỹ.

**Biểu tượng kỹ năng:** cả 42 kỹ năng có emoji riêng, hiện trong danh sách kỹ năng, trên nhãn khi ra đòn, và trong nhật ký.

## Chế độ nổi

Hai mức, vì không trình duyệt nào cho phép web app vẽ lên thanh taskbar của hệ điều hành:

1. **Bong bóng nổi trong trang** — thu app thành một hình tròn 104 px nổi đè lên giao diện, kéo được, hiện vòng gắn bó, số xu và dấu chấm than khi pet cần chăm sóc. Chạm để mở lại. Chạy trên mọi thiết bị. Khi nhúng vào bộ công cụ, bong bóng này nổi trên màn hình làm việc đúng như ý muốn.
2. **Cửa sổ nổi thật** — dùng Document Picture-in-Picture. Mở một cửa sổ nhỏ luôn nằm trên các cửa sổ khác, hiển thị pet, số xu và trạng thái. Chạy trên Chrome và Edge máy tính; trình duyệt khác thì nút báo không hỗ trợ và gợi ý dùng bong bóng.

Cả hai đều tiếp tục chạy mô phỏng hao hụt mỗi 20 giây nên rời mắt vẫn không sai lệch.

## Kích thước
Một file 143 KB, cả bộ PWA **190 KB**. Ngân sách 1 MB còn dư hơn 80%.

---

# Phụ lục v3 — Nguyên Bản đối đầu Công Nghiệp

## Khung cốt truyện

Không dùng khung "tốt / hại cho sức khoẻ" vì matcha vẫn có caffeine, nước ép vẫn đầy đường, và rất nhiều quán khách hàng bán bia — đặt bia vào phe ác là tự bắn vào chân mình. Khung thay thế:

| Phe | Định nghĩa |
|---|---|
| **Nguyên Bản** | Nguyên liệu thật, pha thủ công, biết rõ nguồn gốc |
| **Công Nghiệp** | Hương liệu tổng hợp, sản xuất hàng loạt, công thức giấu kín |

Toàn bộ boss dùng tên nhại theo nguyên mẫu, không dùng tên thương hiệu thật. Đây là quyết định pháp lý, không phải thẩm mỹ: người dùng của công cụ là chủ quán, nhiều người đang phân phối hoặc bán chính những sản phẩm đó.

## Tháp Chưng Cất — 100 tầng, mở 30

Không thiết kế tay 100 tầng. Mỗi chặng 10 tầng: 9 tầng thường sinh tự động từ khuôn của chặng, tầng thứ 10 là boss viết tay. Toàn bộ dữ liệu tháp khoảng 8 KB.

**Đường cong sức mạnh:** `PP(tầng) = 108 × 1.039^(tầng−1)`

| Tầng | 1 | 10 | 20 | 30 | 50 | 100 |
|---|---|---|---|---|---|---|
| PP đối thủ | 108 | 152 | 223 | 328 | 707 | 4.798 |

`[đo]` Tỉ lệ thắng boss, 150 trận mỗi ô, pet chính có 2 pet phụ trợ:

| Người chơi | Tầng 10 | Tầng 20 | Tầng 30 |
|---|---|---|---|
| Mới nuôi (Lv 8, Thiếu niên, Bond 25) | 7% | 4% | 0% |
| Giữa game (Lv 18, Trưởng thành, Bond 55) | 82% | 52% | 1% |
| Nuôi kỹ, độ hiếm Thường (Lv 30, Tiến hoá, Bond 92) | 100% | 99% | 37% |
| Nuôi kỹ, độ hiếm Cực hiếm | 100% | 100% | 99% |

Đây là hình dạng em muốn: **tầng thường là tiến độ, boss là cánh cổng**. `[đo]` Tầng thường với người chơi giữa game: t12–t18 đều 100%, t25 còn 93%, t28 còn 77% — leo trơn tru rồi chậm dần cho tới khi đụng boss.

Điểm đáng chú ý ở hàng cuối: cùng công sức nuôi, pet Cực hiếm qua tầng 30 gần như chắc chắn còn pet Thường chỉ 37%. Đó là lý do để ấp trứng và lai tạo tiếp — nếu không, hệ độ hiếm sẽ vô nghĩa sau tuần đầu.

### Ba chặng đang mở

| Chặng | Tên | Boss tầng cuối | Cơ chế | Điểm yếu |
|---|---|---|---|---|
| 1 | Kệ Hàng Tiện Lợi | Hắc Tinh Ga *(Cola Đen)* | Ga bù: hồi 4% HP mỗi lượt | Nhóm Chua |
| 2 | Xe Đẩy Hương Liệu | Sủi Cam *(Cam Nhân Tạo)* | Bọt hương liệu: cứ 3 lượt gây choáng và −30% INT | Nhóm Đắng |
| 3 | Nhà Máy Siro | Siro Ngọt Gắt *(Bồn Siro)* | Ngọt tích tụ: +6% sát thương mỗi lượt, trần 8 lớp | Nhóm Chát |

Trần 8 lớp của cơ chế Ngọt tích tụ là kết quả sửa cân bằng: `[đo]` bản đầu để +8% không trần thì boss tầng 30 bất khả chiến bại — 0% ngay cả với pet nuôi kỹ, vì sau 15 lượt sát thương đã gấp 3,2 lần.

Bảy chặng còn lại đã đặt tên và nguyên mẫu, mở ở bản sau: Kho Bột Sữa, Dây Chuyền Trân Châu, Trạm Nạp Năng Lượng, Kệ Trà Đóng Chai, Hầm Ủ Men, Phòng Sấy Hoà Tan, và chặng cuối — Người Giữ Nguồn canh Giọt Nước Khởi Nguyên.

### Vé leo tháp

Khoá cứng vào công việc thật:

| Nguồn | Vé |
|---|---|
| Mỗi 2 nhiệm vụ ngày hoàn thành | +1 |
| Mỗi nhiệm vụ tuần | +3 |
| Mỗi nhiệm vụ tháng | +8 |
| Mua bằng xu | 250 xu, tối đa 3 vé/ngày |

Trần thực tế: 3 vé từ nhiệm vụ ngày + 3 vé mua = **6 vé/ngày**, tương đương 6 tầng. 30 tầng đang mở là khoảng 5–8 ngày nếu thắng liên tục, nhưng boss chặn lại nên thực tế kéo dài hơn nhiều — đúng nhịp 20–25 ngày đã dự kiến.

Giá 250 xu/vé cao có chủ ý: bằng khoảng 1,6 ngày làm việc đầy đủ. Mua vé là lối thoát cho ngày bận, không phải cách đi tắt.

### Phần thưởng mỗi tầng

- Xu: `12 + 3 × tầng`
- Hạt kinh nghiệm: 1–3 (dùng ngay, mỗi hạt +14 kinh nghiệm cho pet)
- Hạt mầm: 30% cơ hội, loại theo chặng
- Boss: thêm 200 xu, 5 hạt mầm, và mở một công thức

## Tổ đội bất đối xứng: 1 chính + 2 phụ

Không chọn giữa 1 pet và 3 pet ngang nhau. Tổ đội 3 con ngang hàng sẽ giết mất phần cốt lõi — sợi dây gắn bó với **một** con. Nhưng chỉ 1 con thì tam giác khắc chế 6 loài vô dụng và không có lý do gì để ấp trứng hay lai tạo.

| | Pet chính | Hai pet phụ |
|---|---|---|
| Máu, ra đòn | Có | Không |
| Đóng góp chỉ số | Toàn bộ | 15% chỉ số mỗi con cộng vào pet chính |
| Kỹ năng | 3–4 ô | Mỗi con 1 kỹ năng, bung khi pet chính còn dưới 50% máu |
| Cần chăm sóc hằng ngày | Có | Không |

`[đo]` Tại tầng 15, người chơi giữa game: có tổ đội 100%, một mình 87–91%. Ở tầng cao chênh lệch lớn hơn.

Về mặt code không phải viết lại engine đấu — chỉ cộng chỉ số vào `mkFighter()` và thêm hai kỹ năng dùng một lần.

## Ngủ đông và cứu chuỗi

Đây là thứ em đề nghị làm **trước cả tháp**, vì nó sửa rủi ro đã nêu từ v1: quy tắc "bỏ một ngày là mất chuỗi" quá gắt với ngành F&B.

**Ngủ đông** — bật khi quán nghỉ lễ hoặc chủ đi công tác:
- Dừng toàn bộ hao hụt chỉ số
- Giữ nguyên chuỗi ngày
- Đổi lại: không nhận xu, không ghi nhận nhiệm vụ, không leo tháp

Quán nghỉ thì không có việc để ghi nhận — đó là logic đúng, và nó cũng khiến ngủ đông không thể bị lạm dụng.

**Cứu chuỗi** — mỗi tháng 1 lượt, tự động dùng khi lỡ 1–2 ngày. Không cần thao tác, chỉ hiện thông báo khi đã dùng.

## Kho thu hoạch

Hạt mầm và công thức chưa có chỗ tiêu (khu vườn ở bản sau) nhưng đã có kho chứa, nên phần thưởng tháp không rơi mất. Hạt kinh nghiệm dùng được ngay.

10 loại hạt mầm đã định nghĩa kèm nhóm vị: Arabica *(chua)*, Robusta *(đắng)*, Trà xanh *(chát)*, Ô long *(chát)*, Ca cao *(đắng)*, Chanh *(chua)*, Cam *(chua)*, Dâu *(ngọt)*, Bạc hà *(thanh)*, Gừng *(cay)*. Nhóm vị chính là thứ khớp với điểm yếu boss — đó là lý do khu vườn sẽ có ý nghĩa chứ không phải việc vặt.

## Còn lại cho bản sau

1. Khu vườn — 4 ô, trồng rồi quên, 4–12 giờ thật, không cần tưới
2. 24 công thức đồ uống, mỗi công thức 2–3 nguyên liệu, hiệu ứng dùng một lần mỗi lần leo
3. Sổ công thức có phiên bản đời thật: định lượng, giá vốn, gợi ý giá bán, xuất được ra file
4. Mỗi boss mở một thẻ kiến thức vận hành
5. Leo tự động toàn chặng
6. Đấu người thật bằng mã chia sẻ
7. Pet phản ứng theo số liệu quán
8. Nhật ký quán sinh từ dữ liệu thật
9. Bảy chặng tháp còn lại

## Kích thước
Một file 170 KB, cả bộ PWA **216 KB**. Vẫn dưới một phần tư ngân sách 1 MB.

---

# Phụ lục v4 đợt 1 — thưởng đấu, hình ảnh vật phẩm, biểu cảm

## Thưởng đấu giao hữu: đã bịt lỗ cày xu

Bản v3 cho 22–105 xu mỗi trận thắng, chỉ tốn 15 Năng lượng, không giới hạn số trận. Ngồi bấm 20 phút bằng cả ngày làm việc — phá sạch nguyên tắc "xu chỉ đến từ việc thật" đặt ra từ v1.

Công thức mới:

| Mục | Giá trị |
|---|---|
| Mỗi trận thắng | 5–10 xu ngẫu nhiên |
| Trần mỗi ngày | 50 xu |
| Sàn mỗi ngày | 25 xu, bù cho đủ nếu thắng từ 5 trận trở lên |
| Chạm trần | Vẫn thắng, vẫn có kinh nghiệm và gắn bó, chỉ dừng cộng xu |

`[đo]` Chạy 5 trận liên tiếp cho 36–40 xu, đúng trong dải thiết kế. So với 155 xu/ngày từ nhiệm vụ vận hành, đấu chỉ chiếm dưới một phần tư thu nhập — đủ để có lý do đấu, không đủ để thay thế công việc.

Thông báo khi chạm trần nói rõ lý do thay vì im lặng: "xu thật đến từ nhiệm vụ vận hành".

## Sơ đồ lục giác khắc chế

Sáu loài ở sáu đỉnh, mũi tên nối vòng theo chuỗi khắc chế. Chạm vào một loài thì mũi tên nó thắng chuyển xanh, mũi tên khắc nó chuyển đỏ, kèm một dòng giải thích. Thay hoàn toàn dòng chữ "Beano › Milku › Cacao › ..." cũ.

## Banner thắng boss

Toàn màn hình, có tia sáng xoay, pháo giấy rơi, pet nhún nhảy, và ba ô phần thưởng có biểu tượng: xu, hạt kinh nghiệm, hạt mầm.

Bản thua **không trách móc**: cùng bố cục nhưng bỏ pháo giấy, nhắc lại cơ chế của boss và gợi ý cụ thể — nuôi thêm, đưa pet phụ trợ vào tổ đội, rồi quay lại. Người dùng là chủ quán đang nghỉ giải lao, không phải game thủ cần bị thử thách lòng tự trọng.

## Lò ấp và trứng

Mỗi ô ấp là một vòm kính có phản quang, đèn sưởi ấm nhấp nháy phía dưới, thanh tiến độ, và vỏ trứng riêng theo loại:

| Loại | Màu | Hoa văn |
|---|---|---|
| Trứng thường | Kem ngà | Đốm nâu |
| Trứng hiếm | Xanh nước | Vệt sóng |
| Trứng cổ | Tím | Hoa văn kim cương |
| Trứng vàng | Vàng kim | Sao và chấm |

Trứng đủ giờ thì rung lắc và hiện vết nứt. Cửa hàng trứng cũng hiện hình thay vì chỉ có chữ.

## Chuồng gộp với kho

Tab Trứng tách làm hai: **Lò ấp** và **Chuồng và kho**.

Chuồng hiện toàn bộ pet đang sở hữu kèm nhãn độ hiếm đúng màu, Pet Power và số đời. Bên dưới là kho vật phẩm có biểu tượng vẽ riêng và số lượng: xu, vé tháp, hạt kinh nghiệm, thẻ công thức, thẻ vận hành, và 10 loại hạt mầm — mỗi loại một hình riêng kèm nhãn nhóm vị (chua, đắng, chát, ngọt, thanh, cay).

## Sổ sưu tầm theo độ hiếm

Thanh lọc bảy nút: Tất cả và sáu bậc hiếm, mỗi nút hiện số loài bạn đã sở hữu ở bậc đó trở lên. Mỗi ô trong sổ có một chấm tròn ở góc, màu theo bậc hiếm cao nhất bạn từng sở hữu của loài đó.

Mười nhóm thành tựu có huy hiệu tròn riêng, sáng lên khi nhận được mốc đầu tiên.

## Biểu cảm và lời thoại

**Tám hành động nhàn rỗi** thay cho ba: nhìn quanh, ngáp, vươn vai, ngồi xuống, lắc mông, xoay đuổi đuôi, nhảy, và nói chuyện. Bộ hành động tự lọc theo trạng thái — Năng lượng dưới 40 thì chỉ ngáp, ngồi, nhìn quanh; Vui trên 70 thì bỏ ngáp. `[đo]` Sáu tư thế khác nhau quan sát được trong 60 lượt liên tiếp.

**121 câu thoại**: 8 câu riêng cho mỗi tính cách, cộng 11 nhóm theo hoàn cảnh — đói, bẩn, mệt, buồn, ốm, vui, vừa thắng, vừa thua, buổi sáng, ban đêm, được xoa. Hàm chọn câu ưu tiên hoàn cảnh trước tính cách: `[đo]` khi pet vừa đói vừa bẩn, 20/40 câu nói đúng về đói hoặc bẩn.

## Bong bóng nổi đỡ tĩnh

Nhún nhẹ liên tục, nháy mắt mỗi 5,2 giây, viền chuyển đỏ và nhún nhanh gấp ba khi có chỉ số cần chăm sóc. Cửa sổ nổi Picture-in-Picture cũng nháy mắt theo nhịp tương tự.

## Kích thước
Một file 199 KB, cả bộ PWA **245 KB**. Còn dư 75% ngân sách 1 MB.

---

# Phụ lục v5 đợt 2 — Dải quán 7 khu, camera trượt ngang

## Vì sao trượt ngang chứ không cắt cảnh

Nếu cho ăn mà nhảy sang một cảnh bếp riêng thì ba thứ vỡ cùng lúc: quán biến mất, toàn bộ nội thất đã mua biến mất, và cảm giác "pet đang trông quán cùng bạn" cũng mất theo. Đó chính là thứ gắn mini game với công cụ vận hành.

Giải pháp: **một không gian liên tục rộng bằng 7 màn hình**, camera bám theo pet. Pet đi bộ từ khu này sang khu kia, không có lần cắt nào.

## Bố cục dải quán

```
0 Bếp    1 Quầy chính   2 Góc chơi   3 Sân tập   4 Khu rửa   5 Gác ngủ   6 Cửa ra phố
 cho ăn     mặc định        chơi        rèn         tắm        ngủ         khám phá
```

| Khu | Trang trí |
|---|---|
| Bếp | Tường gạch men, bếp có lò và ba mặt bếp, bàn sơ chế, giá treo xoong |
| Quầy chính | Giữ nguyên: cửa sổ đổi theo giờ, đèn thả, kệ, hũ, và toàn bộ nội thất đã mua |
| Góc chơi | Thảm, giỏ đồ chơi, bóng, gối lười |
| Sân tập | Tường gạch mộc, giá tạ, bao cát treo, khăn |
| Khu rửa | Tường gạch men xanh, bồn nước có bọt, vòi, kệ xà phòng |
| Gác ngủ | Ánh ấm, dây đèn, giường có gối và chăn, đèn ngủ |
| Cửa ra phố | Trời đêm, cửa gỗ có mái hiên, cột đèn đường, cây |

Toàn bộ vẽ bằng SVG nội tuyến, không thêm file ảnh nào.

## Hệ toạ độ

Đây là phần phải viết lại, vì bản cũ dùng `SC.x` là độ lệch so với tâm màn hình.

```
SC.x        vị trí tuyệt đối của pet trên dải, 0 … 7×ZW
ZW()        chiều rộng một khu, bằng chiều rộng khung nhìn
camX()      −clamp(SC.x − ZW/2, 0, 6×ZW)          camera bám pet, dừng ở hai mép
zoneOf(x)   floor(x / ZW)
```

Ba lớp hiển thị phải nằm đúng chỗ, nếu không mọi thứ sẽ trôi lệch:

| Lớp | Nằm ở đâu | Chứa gì |
|---|---|---|
| `#world` `#deco` | trong khu Quầy chính | Nội thất, tách cà phê — cuộn theo cảnh |
| `#sfore` | trong khu Quầy chính, trên pet | Vết bẩn bấm được — cuộn theo cảnh |
| `#fore` | ở khung nhìn, không cuộn | Hạt hiệu ứng, bong bóng nhu cầu |

`[đo]` Đã kiểm: hạt hiệu ứng sinh ra đúng vị trí pet trên màn hình khi camera ở khu 4 (210 px so với 210 px), và vết bẩn vẫn bấm được sau khi cuộn.

## Hành vi mới

- **Đi lại theo khu**: pet quanh quẩn trong khu hiện tại, 16% cơ hội mỗi lượt tự đi bộ về Quầy chính.
- **Kéo pet** bị giới hạn trong khu đang đứng, camera bám theo tay.
- **Bảy chấm điều hướng** nổi ở đáy sân khấu, chạm là pet đi bộ tới khu đó — không dịch chuyển tức thời.
- **Nhãn khu** ở góc trên phải đổi theo vị trí pet.

## Hoạt cảnh gắn với khu

`[đo]` Cả sáu hành động đều đi đúng khu:

| Hành động | Khu | Diễn biến |
|---|---|---|
| Cho ăn | Bếp | Đi tới bếp, bát hiện trên sàn, rung ba nhịp, vụn bắn |
| Chơi | Góc chơi | Bóng rơi từ giỏ, pet chạy sang phải rồi sang trái đuổi theo |
| Rèn | Sân tập | Tạ hiện lên, nhún bốn nhịp, mồ hôi rơi |
| Tắm | Khu rửa | Pet đứng vào bồn, 14 bong bóng, rũ mình, giọt văng |
| Ngủ | Gác ngủ | **Pet trèo lên giường** (dịch lên 26 px), màn tối 55%, chữ z bay |
| Khám phá | Cửa ra phố | Đi khuất mép phải, biến mất, quay lại mang túi, rồi tự về Quầy chính |

## Hai lỗi sửa trong lúc dựng

1. **Chấm điều hướng bị khay hoá đơn đè lên** — hàng chấm nằm dưới sân khấu nên viền răng cưa của khay che mất. Đưa vào trong sân khấu thành một dải nổi có nền mờ.
2. **Dây đèn sao ở gác ngủ phình to** — dùng `preserveAspectRatio="none"` trên khung nhìn hẹp khiến ngôi sao kéo giãn thành khối lớn. Đổi sang bóng đèn tròn và hạ chiều cao lớp.

## Kích thước
Một file 214 KB, cả bộ PWA **260 KB**. Còn dư 74% ngân sách 1 MB.

---

# Phụ lục v6 đợt 3 — Cửa hàng ba nhóm, nguyên liệu, khung lễ

## Cửa hàng chia ba nhóm

| Nhóm | Nội dung |
|---|---|
| **Nội thất** | 25 món, chia 5 vị trí: Trên quầy, Sàn, Tường, Đèn, Nền |
| **Nguyên liệu** | 8 loại mua bằng xu, tích trong kho |
| **Khung lễ** | 6 bộ khung trang trí theo mùa |

## Tám thiết bị F&B bổ sung

Không phải đồ trang trí chung chung — đều là thiết bị có thật trong quán, và mỗi món có hiệu ứng gắn với đúng công dụng của nó:

| Món | Giá | Vị trí | Hiệu ứng |
|---|---|---|---|
| Ấm rót cổ ngỗng | 190 | Trên quầy | Cho ăn hiệu quả +12% |
| Máy xay sinh tố | 340 | Trên quầy | Vui tụt chậm hơn 10% |
| Máy làm đá | 380 | Trên quầy | Hồi 0.3 Sạch mỗi giờ |
| Giá pour-over | 260 | Trên quầy | Rèn hiệu quả +15% |
| Tủ mát trưng bánh | 460 | Sàn | No tụt chậm hơn 15% |
| Bình ủ trà | 230 | Kệ | Hồi 0.4 Tinh thần mỗi giờ |
| Cân điện tử | 200 | Kệ | Nhận thêm 3% xu |
| Bảng ghi đơn | 180 | Tường | Ấp trứng nhanh hơn 5% |

Tổng nội thất nay là **25 món, 6.140 xu**. `[đo]` Không có hai món nào trùng vị trí ngoài ý muốn — các món cùng một vị trí là cố ý thay thế lẫn nhau.

## Nguyên liệu

Tám loại, mỗi loại có nhãn vị để sau này khớp với công thức:

| Nguyên liệu | Giá | Vị |
|---|---|---|
| Đá viên | 15 | lạnh |
| Đường | 20 | ngọt |
| Muối biển | 25 | mặn |
| Sữa tươi | 35 | béo |
| Sữa đặc | 40 | ngọt |
| Syrup | 45 | ngọt |
| Trân châu | 50 | dai |
| Kem tươi | 55 | béo |

Cộng với 10 loại hạt mầm trồng được từ tháp, hệ chế biến ở bản sau sẽ có **18 đầu vào** và đủ hai nguồn: mua và trồng. Nguyên liệu hiện chưa có chỗ tiêu nhưng đã có kho, không mất đi.

## Sáu khung lễ

Bộ khung lấy theo lịch Việt chứ không lấy lịch Nhật hay Âu. Tết và Trung Thu đứng trước Noel.

| Khung | Giá | Khoảng ngày gợi ý | Trang trí |
|---|---|---|---|
| Tết Nguyên Đán | 420 | 15/1 – 25/2 | Cành đào, phong bao, đồng tiền vàng, viền đỏ-vàng, cánh hoa rơi |
| Xuân hoa anh đào | 380 | 1/3 – 20/4 | Cành hoa hai góc, cánh hoa rơi nhẹ |
| Hè bãi biển | 380 | 15/5 – 20/8 | Lá dừa, phao bơi, sóng, bong bóng nước |
| Trung Thu | 420 | 25/8 – 30/9 | Ba đèn lồng đỏ, trăng tròn có vân, hạt sáng vàng |
| Thu lá vàng | 380 | 1/10 – 20/11 | Cành lá đổi màu, nắng chiều, lá rụng |
| Giáng sinh | 420 | 25/11 – 31/12 | Cành thông, quả châu, tuyết rơi |

Khoảng ngày Tết tính xấp xỉ theo dương lịch vì Tết rơi vào 21/1 – 20/2 tuỳ năm. Khung nào đang đúng mùa sẽ có nhãn **ĐÚNG MÙA** trong cửa hàng.

Mỗi khung gồm bốn phần: hai góc trang trí, hai viền mảnh trên dưới, và một lớp hạt rơi liên tục với tốc độ ngẫu nhiên cho từng hạt. Mua một lần, bật tắt tuỳ ý quanh năm. Khi treo, Gắn bó tăng nhanh hơn 5%.

`[đo]` Chạy thử ngày 9/9: hệ thống tự nhận Trung Thu là khung đúng mùa.

## Một lỗi sửa trong lúc dựng

Hiệu ứng của khung lễ ban đầu không có tác dụng vì hàm `perkOf()` chỉ đọc danh sách nội thất đang bày. Đã tách thành `activePerks()` gom cả nội thất lẫn khung đang treo. `[đo]` Sau khi sửa, treo khung Tết cho `perkOf('bond')` = 1.05 đúng như thiết kế.

Ngoài ra hai góc khung che mất nhãn tâm trạng và nhãn khu ở phía trên. Đã chuyển cả hai xuống đáy sân khấu, hai bên hàng chấm điều hướng.

## Cân đối kinh tế sau đợt 3

| Khoản | Xu |
|---|---|
| Mua hết 25 món nội thất | 6.140 |
| Mua hết 6 khung lễ | 2.400 |
| Một lượt mua đủ 8 nguyên liệu | 285 |
| Thu nhập tối đa mỗi tháng | 9.250 |

`[đo]` Nếu làm việc hoàn hảo mỗi ngày thì mua hết đồ trang trí mất **0,92 tháng**. Với người dùng thực tế đạt 60–70% nhiệm vụ thì khoảng 1,5 tháng.

Con số này chấp nhận được vì nội thất là mục tiêu một lần, còn khoản tiêu định kỳ nằm ở chỗ khác: vé leo tháp 250 xu (tối đa 3 vé/ngày, tức 22.500 xu/tháng nếu mua hết) và trứng 200–1.200 xu mua lại được vô hạn. Hai khoản đó hút hết phần dư, nên xu không bao giờ mất giá.

## Kích thước
Một file 236 KB, cả bộ PWA **282 KB**. Còn dư 72% ngân sách 1 MB.

## Ba đợt đã xong — còn lại gì

Đã xong toàn bộ 10 mục yêu cầu. Danh sách còn lại cho bản sau, theo thứ tự em đề nghị:

1. **Khu vườn** — 4 ô, trồng rồi quên, 4–12 giờ thật, không cần tưới
2. **24 công thức đồ uống** — mỗi công thức 2–3 nguyên liệu, hiệu ứng dùng một lần mỗi lần leo tháp, khớp với điểm yếu từng boss
3. **Sổ công thức có phiên bản đời thật** — định lượng, giá vốn, gợi ý giá bán, xuất ra file
4. **Thẻ kiến thức vận hành** mở theo từng boss
5. **Leo tự động toàn chặng**
6. **Bảy chặng tháp còn lại** (tầng 31–100)
7. **Đấu người thật bằng mã chia sẻ**
8. **Pet phản ứng theo số liệu quán**
9. **Nhật ký quán sinh từ dữ liệu thật**

---

# Phụ lục v7 — Khu vườn và 24 công thức

Đây là mảnh ghép nối hạt mầm từ tháp, nguyên liệu từ cửa hàng, và điểm yếu boss thành một vòng lặp khép kín:

```
Nhiệm vụ vận hành → vé tháp → leo tháp → hạt mầm
                                            ↓
                    nguyên liệu mua ← BÀN CHẾ BIẾN → ly nước có buff
                                            ↑              ↓
                                      khu vườn        đánh boss dễ hơn
```

## Dải quán xếp lại, thêm khu thứ tám

```
0 Cửa ra phố → 1 QUẦY CHÍNH → 2 Bếp → 3 Khu rửa → 4 Góc chơi → 5 Gác ngủ → 6 Sân tập → 7 Vườn sau
   mặt tiền       mặc định     ăn      tắm         chơi          ngủ         rèn        trồng trọt
```

Cửa ra phố ở đầu dải, càng sang phải càng vào sâu trong nhà, cuối cùng là vườn sau. Quầy chính vẫn ở vị trí 1 nên khi mở app không có gì đổi.

## Khu vườn

Nguyên tắc: **gieo rồi quên**. Không tưới, không hỏng, không có thao tác lặp lại hằng ngày. Người dùng đã phải chăm pet mỗi ngày rồi — thêm một hệ chăm sóc thứ hai là lý do khiến người ta bỏ game.

- **8 ô đất** xếp một hàng ngang ở đáy khu, pet đứng phía sau luống
- 4 ô miễn phí, mở thêm: ô 5 và 6 giá 800 xu, ô 7 và 8 giá 2.000 xu
- Chạm ô trống để gieo, ô đang lớn để xem còn bao lâu, ô chín để thu
- Mầm cây lớn dần theo tiến độ thật và đổi màu quả theo nhóm vị của hạt
- Mỗi ô thu **2–4 đơn vị nông sản**

| Hạt | Giờ | Nhóm vị |
|---|---|---|
| Bạc hà | 3 | thanh |
| Chanh | 4 | chua |
| Cam, Gừng | 5 | chua, cay |
| Trà xanh, Dâu | 6 | chát, ngọt |
| Robusta | 8 | đắng |
| Ô long | 9 | chát |
| Arabica | 10 | chua |
| Ca cao | 12 | đắng |

## Bàn chế biến

Nằm trong khu Bếp, chạm vào là mở bảng ghép. Hiện kho hiện có, 24 công thức chia sáu nhóm vị, nguyên liệu thiếu tô đỏ. Pha một công thức lần đầu được **+40 xu và mở thẻ trong sổ**.

## 24 công thức

Bốn công thức mỗi nhóm vị. `[đo]` Cả 10 loại nông sản và 8 nguyên liệu shop đều được dùng, không có thứ nào thừa.

| Nhóm | Khắc chế | Bốn món |
|---|---|---|
| **chua** | Hắc Tinh Ga | Cam Ép Muối Biển · Chanh Sả Mật Ong · Espresso Tonic · Dâu Chanh Đá Xay |
| **đắng** | Sủi Cam | Robusta Đen Đá · Cacao Nguyên Chất · Cà Phê Muối · Bạc Xỉu Đắng |
| **chát** | Siro Ngọt Gắt | Matcha Latte · Trà Ô Long Sữa · Trà Xanh Trân Châu · Hojicha Rang Đá |
| **ngọt** | — | Sữa Chua Dâu · Cacao Kem Tươi · Trà Đào Cam Sả · Sữa Tươi Trân Châu Đường Đen |
| **thanh** | — | Bạc Hà Chanh Soda · Mojito Không Rượu · Trà Bạc Hà Lạnh · Nước Chanh Bạc Hà |
| **cay** | — | Gừng Mật Ong · Cacao Gừng · Trà Gừng Sả · Cà Phê Gừng |

Hiệu ứng trải đủ các loại: cộng chỉ số, chí mạng, né, hồi máu mỗi lượt, phản sát thương, ra đòn trước, xoá debuff. Không món nào trùng hiệu ứng với món khác.

## Sổ công thức có bản đời thật

Mỗi thẻ đã mở kèm **định lượng thật, giá vốn ước tính, khoảng giá bán gợi ý và biên gộp**. Ví dụ:

> **Cam Ép Muối Biển** · 350ml
> Cam ép 250ml · muối biển 0,5g · syrup 15ml · đá 120g
> Giá vốn 9.500đ · Giá bán gợi ý 32.000 – 38.000đ · Biên gộp 70%

`[đo]` Biên gộp của 24 công thức nằm trong khoảng **68–77%**, đúng dải thường gặp của đồ uống pha chế. Giá vốn trung bình 9.583đ.

Thẻ chưa mở vẫn hiện nguyên liệu cần, để người chơi biết phải trồng gì.

Đây là chỗ mini game trả lại giá trị thật cho công cụ: chơi xong có một tập công thức mang ra quán dùng được, không phải chỉ giết thời gian.

## Ly nước mang theo khi leo tháp

Chọn ngay trên màn hình tháp. Ly dùng **một lần cho một tầng**; leo nhanh nhiều tầng chỉ dùng ở tầng đầu.

Nếu nhóm vị của ly khớp điểm yếu boss thì gây thêm **25% sát thương** — nút chọn hiện nhãn "khắc chế boss +25%" để không phải tra bảng.

`[đo]` Đo 200 trận mỗi ô, pet Lv24 Tiến hoá Bond 80 có hai pet phụ trợ:

| Tầng boss | Không mang | Đúng nhóm vị | Sai nhóm vị |
|---|---|---|---|
| 10 | 100% | 100% | 100% |
| 20 | 98% | 100% | 100% |
| 30 | **26%** | **47%** | 35% |

Đúng như thiết kế: ly nước không đổi gì ở tầng dễ, nhưng ở đúng bức tường thì nâng tỉ lệ thắng từ 26% lên 47%. Riêng phần khắc chế nhóm vị đóng góp 12 điểm phần trăm, phần cộng chỉ số đóng góp 9.

## Hai vật phẩm tiêu hao

Không làm mã cheat mà làm hàng bán trong shop, để lấp đúng chỗ "có xu mà không biết tiêu gì":

| Vật phẩm | Giá | Trần ngày | Tác dụng |
|---|---|---|---|
| Thuốc ủ ấm | 120 | 2 | Giảm 4 giờ ấp một quả trứng |
| Sữa tăng trưởng | 90 | 2 | Cộng ngay 80 kinh nghiệm |

## Cấu trúc dữ liệu mới

```ts
S.garden = { plots: number, slots: ({seed, start} | null)[] }
S.inv.crop   = { [seedId]: number }    // nông sản đã thu hoạch
S.inv.made   = { [recipeId]: number }  // ly đã pha, sẵn sàng mang đi
S.inv.recipes= string[]                // thẻ công thức đã mở
S.drink      = recipeId | null         // ly đang mang theo
S.pot        = { day, used: {[potionId]: number} }
```

## Kích thước
Một file 263 KB, cả bộ PWA **310 KB**. Còn dư 69% ngân sách 1 MB.

## Còn lại trong danh sách đã thống nhất

1. **Cài đặt** — gom Sưu tầm, Thành tựu, Sổ công thức; màu nền; Chế độ thử có đánh dấu vĩnh viễn; xuất/nhập bản lưu; mã pet chia sẻ
2. **Chế độ phiêu lưu** — 6 map vùng nguyên liệu + Pandora, chuyến đi 30 phút, mở bằng nhiệm vụ vận hành
3. **Cây kỹ năng** vẽ 42 kỹ năng thành 6 nhánh, và **điểm cốt gộp vào Rèn** (3 điểm mỗi cấp, 1 điểm mỗi lần Rèn)
4. Ảnh chụp quán, thẻ tóm tắt khi mở app, nhật ký quán
5. Bảy chặng tháp còn lại, đấu người thật bằng mã chia sẻ, pet phản ứng theo số liệu quán

---

# Phụ lục v8 — Màn khởi đầu, Cài đặt, và sửa lỗi font tiếng Việt

## Hai lỗi hiển thị đã sửa

### 1. Dấu tiếng Việt bị tách rời ở tiêu đề

`Bàn chê´ biê´n` · `Tâ`ng 21` · `Sổ sưu tâ`m` · `Lò â´p`

Nguyên nhân: biến `--disp` khai báo `"Cormorant Garamond","Iowan Old Style",Georgia,serif`. Cormorant Garamond không có sẵn trên máy nào, nên trình duyệt rơi về Iowan Old Style (iOS) hoặc Georgia. **Hai font này không có bảng Latin Extended Additional** (U+1EA0–U+1EF9) — nơi chứa toàn bộ ký tự tiếng Việt có hai dấu như ế, ầ, ổ, ậ. Trình duyệt buộc phải tách thành chữ gốc cộng dấu tổ hợp rồi tự ghép, và ghép lệch.

Sửa tạm bằng cách đổi chuỗi font vẫn không chắc, vì mỗi máy có bộ font khác nhau. Nên em **nhúng hẳn font vào file**:

- Lấy DejaVu Serif Bold, kiểm tra đủ 100% ký tự tiếng Việt
- Subset còn 430 ký tự: Latin cơ bản, Latin-1, Latin Extended-A, toàn bộ khối tiếng Việt, dấu câu hay dùng
- Đóng gói WOFF, nhúng base64 thẳng vào thẻ style

`[đo]` Font subset **29,8 KB** (base64 39,7 KB), không thiếu ký tự nào. Giờ mọi thiết bị hiển thị giống nhau, không phụ thuộc font hệ thống.

Nếu sau này muốn dùng đúng Cormorant Garamond, chỉ cần thay chuỗi base64 trong khối `@font-face` — phần còn lại giữ nguyên.

### 2. Chữ chồng lên nhau ở bảng chế biến

Đây **không phải lỗi iOS** như em đoán ban đầu, mà là **trùng tên class CSS**:

```
.bf { position:absolute; bottom:16px; width:116px; height:116px }   ← đấu sĩ trên sàn đấu
<div class="bf">ATK +12%</div>                                       ← dòng hiệu ứng công thức
```

Cả 24 dòng hiệu ứng bị hút ra khỏi luồng và xếp chồng tại một điểm. Đổi tên thành `.rbuff`. `[đo]` Sau khi sửa: 24 dòng, 0 dòng ở chế độ tuyệt đối, 0 dòng trùng vị trí.

Đã rà lại toàn bộ 31 class toàn cục ngắn để chắc không còn trường hợp thứ hai.

### Hai sửa nhỏ kèm theo
- Bỏ `backdrop-filter` ở hai lớp phủ cuộn được (bảng kéo lên, banner thắng) — trên iOS nó gây vệt nhoè khi cuộn
- Hoa văn trên vỏ trứng bị tràn ra ngoài, nay đã cắt theo hình vỏ bằng `clipPath`
- Ẩn thanh cuộn ngang ở các dải tab

## Màn khởi đầu

Bốn bước:

1. **Start** — tên game, một dòng định vị, sáu loài nhún nhảy xem trước, nút Bắt đầu
2. **Chọn loài** — sáu thẻ có hình pet trưởng thành, tên, tên Việt, và sáu thanh chỉ số gốc. Chạm để chọn, câu đặc tính của loài hiện ngay bên dưới. Nút bị khoá tới khi chọn
3. **Gõ trứng** — vỏ trứng mang màu của loài đã chọn. Gõ ba lần, mỗi lần trứng nảy lên và vết nứt lan rộng thêm
4. **Nở và đặt tên** — pháo giấy, pet hiện ra kèm thẻ độ hiếm, tính cách và đặc điểm, ô nhập tên

**Pet đầu tiên luôn ra Thường hoặc Ít gặp** (75/25). Cố ý để dành cảm giác hiếm cho những quả trứng sau — nếu quả đầu ra Huyền thoại thì toàn bộ hệ độ hiếm mất ý nghĩa ngay ngày đầu.

## Cài đặt

Tab cuối đổi tên thành **Khác**, gom bốn mục: Bộ sưu tập · Thành tựu · Công thức · Cài đặt.

### Màu nền giao diện — 4 chủ đề

| Chủ đề | Sắc chính |
|---|---|
| Rừng thông | Xanh rêu, vàng đồng (mặc định) |
| Cà phê sữa | Nâu rang, kem |
| Đêm biển | Xanh mực, xanh nước |
| Trà chiều | Nâu cát, vàng ô liu |

Đổi chủ đề áp ngay cho toàn bộ giao diện **và cả sắc nền quán** — độ sáng của tường vẫn chạy theo giờ thật, chỉ đổi tông màu.

### Mã pet để đấu

Nút sao chép sinh chuỗi `PP1-…` khoảng 400 ký tự, chứa loài, độ hiếm, DNA, đặc điểm, cấp, gắn bó, điểm rèn. Chủ quán khác dán vào ô bên dưới là đấu được với bản sao pet của bạn. Bản sao không nhận thưởng và không ảnh hưởng pet gốc.

### Sao lưu tiến độ

Xuất toàn bộ bản lưu thành một chuỗi base64 (`[đo]` khoảng 3,4 KB với tài khoản mới), tự sao chép vào bộ nhớ tạm. Nhập lại có hỏi xác nhận trước khi ghi đè.

Đây là mục em muốn chen vào từ đầu: bản lưu nay có hơn 30 khoá qua 11 module, một lỗi chuyển phiên bản là mất sạch tiến độ của người dùng.

### Lịch sử tài khoản

Mười lăm dòng tóm tắt: ngày bắt đầu, số ngày đã qua, giờ dùng công cụ, nhiệm vụ hoàn thành, chuỗi dài nhất, lần chăm sóc, trận thắng, tầng cao nhất, trứng đã nở, số pet, đời lai cao nhất, mục sưu tầm, công thức đã mở, nội thất, xu.

### Chế độ thử

Em **không làm mã bí mật** như ý ban đầu. Toàn bộ game nằm trong một file HTML — mã cheat nằm trong đó thì ai xem mã nguồn cũng thấy, kể cả nhân viên. Ngày một bạn barista tìm ra mã 9999 xu là nguyên tắc "xu chỉ đến từ việc thật" sụp trong một buổi.

Thay bằng: gõ câu mở khoá trong Cài đặt để mở bảng tám nút — cộng xu, cộng vé, cộng hạt và nguyên liệu, nở hết trứng, đẩy lên Tiến hoá, gắn bó 100, mở hết nội thất và khung lễ.

**Bản lưu nào từng bật sẽ mang dấu vĩnh viễn:**
- Header hiện nhãn đỏ **THỬ**
- Không ghi thành tựu (`[đo]` xác nhận: bấm nhận mốc không cộng xu)
- Không ghi kỷ lục tầng tháp

Bản giao cho khách đặt `DB.devMode.enabled = false` là mục này biến mất hoàn toàn.

### Chơi lại từ đầu

Xoá bản lưu và quay về màn chọn loài, có hỏi xác nhận và nhắc xuất bản lưu trước.

## Kích thước
Một file 327 KB (trong đó 40 KB là font nhúng), cả bộ PWA **373 KB**. Còn dư 63% ngân sách 1 MB.

## Ghi chú cho bộ test

Màn khởi đầu chặn thao tác khi chưa có bản lưu, nên toàn bộ 21 kịch bản test cũ phải thêm một bước bỏ qua màn khởi đầu. Nhãn tab cuối đổi từ "Sổ" sang "Khác" cũng làm hai kịch bản cũ tìm không ra nút. Đã cập nhật cả hai. `[đo]` Bảy bộ test chính chạy lại không còn lỗi.

---

# Phụ lục v9 — Phiêu lưu, tháp dọc, và sửa lỗi khựng hình

## Lỗi khựng animation — nguyên nhân và cách sửa

Ba thủ phạm, theo mức độ nặng:

**1. Mỗi lần chớp mắt lại dựng lại toàn bộ SVG của pet.** Hàm `paintPet()` thay `innerHTML` khoảng 3 KB, buộc trình duyệt phân tích lại SVG, bố cục lại và vẽ lại cả cảnh — hai lần trong 130 mili giây, cứ 3–7 giây một lượt. Tách nhóm mắt và miệng thành `<g class="fg">` rồi thêm `paintFace()` chỉ thay đúng nhóm đó.

**2. `backdrop-filter: blur()` trên thanh đầu và thanh điều hướng.** Hai thanh này cố định, nhưng nội dung phía sau thì luôn chuyển động (pet đi, camera trượt, hạt bay), nên trình duyệt phải làm mờ lại nền ở mỗi khung hình. Đã bỏ hẳn, thay bằng màu đặc.

**3. `filter: blur(6px)` trên chùm sáng đèn thả** — cũng phải tính lại mỗi khung. Thay bằng gradient mềm không cần bộ lọc.

Kèm theo: `contain: layout paint` cho sân khấu, `will-change: transform` và `translateZ(0)` cho dải quán và nhân vật, giảm nhịp sinh hơi nước, và chỉ vẽ lại nội thất / khung lễ / khu vườn khi dữ liệu thật sự đổi thay vì mỗi lần `mount()`.

`[đo]` Kết quả trên 330 khung hình liên tiếp ở trang Nhà:

| Chỉ số | Trước | Sau |
|---|---|---|
| Khoảng cách khung hình, trung vị | — | **16,7 ms** |
| p95 | — | **16,7 ms** |
| Tệ nhất | — | **16,8 ms** |
| Khung rớt (> 32 ms) | — | **0 / 330** |
| Dựng lại cả SVG trong 9 giây | ~3 lần | **0 lần** |
| Chỉ đổi biểu cảm trong 9 giây | 0 | 4 lần |

## Dòng mô tả bo góc kiểu hội thoại

Khối `.note` trước đây là hộp vuông có vạch trái. Nay bo 14px với một đuôi nhỏ ở góc dưới trái, giống bong bóng thoại của pet — đồng bộ với ngôn ngữ hình ảnh chung.

## Trứng khởi đầu có cửa ra hiếm

Bản trước cố định 75% Thường / 25% Ít gặp. Nay có bảng riêng:

| Bậc | Thường | Ít gặp | Hiếm | Cực hiếm | Huyền thoại |
|---|---|---|---|---|---|
| Tỉ lệ | 60% | 27% | 10% | 2,5% | 0,5% |

`[đo]` 8.000 lần thử: 60,2 / 26,9 / 9,7 / 2,8 / 0,5 — khớp bảng.

Ra từ Hiếm trở lên thì màn nở hiện thêm dòng "Ra hàng hiếm ngay quả đầu!". Vẫn nghiêng hẳn về Thường để dành cảm giác hiếm cho những quả trứng về sau.

## Tháp dựng theo chiều đứng

Thay thanh mười vạch ngang bằng một cột tầng cuộn được, tầng cao ở trên, tầng thấp ở dưới, tự cuộn tới vị trí hiện tại khi mở.

- **Tầng thường**: một hàng mảnh, số tầng và một vạch. Đã qua thì chuyển xanh ngọc, tầng hiện tại viền vàng có quầng sáng và có pet đứng ở đó.
- **Tầng boss (mỗi 10 tầng)**: hàng cao gấp ba, viền đỏ dày, nền chuyển sắc đỏ sẫm, boss vẽ to 86px kèm quầng sáng đập nhịp, tên boss cỡ lớn và dòng mô tả cơ chế. Hạ rồi thì đổi sang tông xanh ngọc.

**Boss cũng to hơn trên sàn đấu**: 150px so với 116px của đấu sĩ thường, thêm quầng đỏ, viền thân dày gấp đôi, và tám gai nhọn quanh thân. `[đo]` Xác nhận kích thước 150px khi vào tầng boss.

## Chế độ phiêu lưu

### Sáu vùng nguyên liệu có thật

| Vùng | Nguyên mẫu | Thu về |
|---|---|---|
| Cao nguyên đỏ | Robusta Tây Nguyên | Robusta, gừng, đường |
| Đồi sương | Arabica Cầu Đất, Khe Sanh | Arabica, dâu, sữa tươi |
| Đồi trà | Trà Bảo Lộc, Lâm Đồng | Trà xanh, ô long, sữa đặc |
| Miệt vườn | Ca cao Bến Tre | Ca cao, dâu, kem tươi |
| Vườn cam | Cam, chanh Nghệ An | Cam, chanh, syrup |
| Thung lũng lạnh | Dâu, bạc hà Đà Lạt | Dâu, bạc hà, gừng, đá |

Mỗi vùng có một đoạn kể về khí hậu và cách nó tạo ra vị, cộng một dòng kiến thức nghề. Ví dụ ở Đồi sương: quả chín chậm nên tích nhiều đường và axit, đó là lý do arabica vùng cao có vị chua sáng mà robusta không có.

### Bản đồ vẽ theo góc 45 độ

Mỗi bản đồ là một cảnh SVG riêng: dải trời, đường chân trời đặc trưng, nền đất chuyển sắc, năm hàng cây xếp theo phối cảnh (hàng xa nhỏ và nhạt, hàng gần to và đậm), và một đường mòn uốn từ dưới lên. Bảng màu riêng cho từng vùng — đất bazan đỏ cho Tây Nguyên, sương xám xanh cho Cầu Đất, luống trà xanh cho Bảo Lộc, xám công nghiệp cho Pandora.

Pet chạy dọc đường mòn bằng `offset-path`, và một dải sáng quét dọc bản đồ trong lúc chuyến đang chạy.

### Cơ chế chuyến đi

| Mục | Giá trị |
|---|---|
| Thời lượng | 30 phút thật |
| Chạy song song | tối đa 2 chuyến |
| Lượt đi | mỗi 3 nhiệm vụ ngày +1 (trần 2/ngày), tuần +2, tháng +5 |
| Chi phí | 1 lượt + 12 Năng lượng |
| Thu về | 1–3 hạt mỗi loại của vùng, 1–3 nguyên liệu vùng, 18–34 xu, ít kinh nghiệm, +1 gắn bó |

**Cái giá thật: pet đi vắng.** Trong lúc chuyến chạy thì không chăm sóc được, không leo tháp được, bong bóng nổi và cửa sổ nổi chuyển sang trạng thái "đang quét bản đồ". Gọi về sớm được nhưng mất trắng chuyến đó.

`[đo]` Đã xác nhận: bấm cho ăn khi pet đi vắng không làm đổi chỉ số No.

### Pandora

Mở sau khi qua tầng 30 của tháp, mỗi 7 ngày một lượt. Không có hạt mầm, chỉ có **Hương liệu tổng hợp**.

Hương liệu tổng hợp thay được **bất kỳ nguyên liệu nào đang thiếu** khi pha. Đổi lại:

- Ly pha ra chỉ còn **60% hiệu lực**
- **Mất hẳn khả năng khắc chế boss** (không có +25%)
- Mỗi chuyến Pandora để lại **−1% toàn bộ chỉ số pet**, tích luỹ tối đa −10%, không hồi lại

`[đo]` Kiểm chứng: cùng công thức Cam Ép Muối Biển, bản thật cho ATK ×1,109 và khắc chế ×1,25; bản tổng hợp cho ATK ×1,061 và khắc chế ×1,00.

Đây là lựa chọn có giá phải trả đúng nghĩa, khớp với cốt truyện Nguyên Bản đối đầu Công Nghiệp: tiện trước mắt, hao mòn về sau.

## Kích thước
Một file 355 KB (gồm 40 KB font nhúng), cả bộ PWA **401 KB**. Còn dư 60% ngân sách 1 MB.

## Còn lại

1. Cây kỹ năng vẽ 42 kỹ năng thành 6 nhánh, và điểm cốt gộp vào Rèn
2. Ảnh chụp quán, thẻ tóm tắt khi mở app, nhật ký quán
3. Bảy chặng tháp còn lại (tầng 31–100)
4. Pet phản ứng theo số liệu quán

---

# Phụ lục v10 — Đo lường, cầu nối công cụ, giảm ma sát

Đợt này không thêm tính năng chơi. Sáu việc, tất cả nhằm giảm ma sát và bắt đầu có số liệu để quyết định.

## 1. Ghi nhận sử dụng

Đây là mục em đề nghị chen vào từ lúc bàn roadmap, và là thứ trả lời được câu hỏi treo từ phụ lục v1: **mini game có làm tăng tỉ lệ hoàn thành nhiệm vụ vận hành không?**

Chỉ đếm số lượt, không lưu nội dung:

| Đo gì | Dùng để làm gì |
|---|---|
| Lượt mở từng trang | Trang nào không ai vào thì cắt |
| Lượt từng hành động chăm sóc | Hành động nào thừa |
| Số phiên mở app | Tần suất quay lại |
| Phiên "vào rồi ra" | Mở app nhưng không làm gì trong 90 giây — chỉ dấu của giao diện khó dùng |
| Nhiệm vụ vận hành mỗi ngày | Tách riêng **ngày CÓ chạm** và **ngày KHÔNG chạm** mini game |

Bảng cuối là bảng quan trọng nhất. Nếu sau hai tuần con số hai dòng đó bằng nhau thì gamification không có tác dụng, và toàn bộ tháp 100 tầng chỉ là đồ trang trí đắt tiền. Dưới 14 ngày dữ liệu thì giao diện tự hiện dòng nhắc là chưa đủ để so sánh.

Giữ 60 ngày gần nhất, xem trong Cài đặt, xuất được ra báo cáo chữ để dán vào đâu cũng được.

## 2. Cầu nối hai chiều với công cụ vận hành

Trước v10 chỉ có chiều xuôi: người dùng tự tick nhiệm vụ trong game. Nay có cả hai chiều, chạy bằng `postMessage`, không cần máy chủ.

**Công cụ → Game**
```js
iframe.contentWindow.postMessage({
  type:'pp:ops',
  quests:['open','pnl','stock'],       // nhiệm vụ ngày đã hoàn thành
  foodCost:'good',                      // good | ok | bad
  revenue:{ actual:5200000, target:5000000 },
  checklistRate:0.97
}, '*');
```

| Dữ liệu vào | Game phản ứng |
|---|---|
| `quests` | Tự nhận nhiệm vụ, cộng xu, cộng vé tháp và lượt đi |
| `foodCost:'good'` | Pet được **+10% toàn bộ chỉ số trong 24 giờ** |
| Doanh thu ≥ target | Pet nhảy mừng ngay khi mở app |
| `checklistRate ≥ 0.95` | Vui +6 |

**Game → Công cụ**, mỗi 60 giây và sau mỗi thao tác:
```js
{ type:'pp:status', name, stage, bond, coin, tickets,
  needsCare, lowest, away, hint }   // hint: "Bo đang cần ăn"
```

Ghi song song vào `localStorage['petpocket.status']` để công cụ đọc trực tiếp nếu không dùng iframe.

Cài đặt có bốn nút thử để kiểm tra khi chưa nhúng thật. `[đo]` Bấm "3 nhiệm vụ xong": nhiệm vụ từ 0 lên 3, vé tháp tăng theo. Bấm "food cost đẹp": hệ số chỉ số lên 1,10.

## 3. Vùng chạm

`[đo]` Trước v10: **61/127 phần tử bấm được dưới 44px, tức 48%**. Tệ nhất là chấm điều hướng khu chỉ 7px.

Sau v10: **1/109, dưới 1%**.

Cách làm với chấm điều hướng đáng ghi lại: giữ nguyên chấm 7px về mặt nhìn nhưng bọc trong một ô trong suốt 24×44px. Vùng chạm rộng mà giao diện không phình.

## 4. Trang Nhà và Tháp rút gọn

**Nhà** thêm một thẻ **hành động gợi ý** tính từ trạng thái hiện tại, theo thứ tự ưu tiên:

1. Pet đang đi khảo sát → xem tiến độ chuyến
2. Đang ngủ đông → nhắc tắt
3. Pet có bệnh → hành động chữa đúng bệnh
4. Có chỉ số dưới 32 → hành động tương ứng
5. Còn nhiệm vụ vận hành → sang tab Việc
6. Còn vé tháp → sang tháp
7. Không có gì gấp → rủ chơi

Chỉ số rút từ 6 thanh xuống **3 thanh chính**, ba thanh còn lại nằm trong phần Chi tiết. Lưới hành động thu gọn lại làm hàng phụ.

**Tháp** bỏ 5 khối khỏi màn chính, chỉ còn tầng hiện tại, vé, tháp dọc và nút leo. Boss, phần thưởng, vé, kho, cốt truyện, danh sách chặng đẩy vào hai bottom sheet.

## 5. Hướng dẫn thao tác đầu tiên

Ba bước, mỗi bước làm sáng đúng nút cần bấm bằng viền vàng đập nhịp, kèm một thẻ giải thích. Tự sang bước khi thao tác xong. Có nút bỏ qua, và xem lại được trong Cài đặt.

Cho ăn → Chơi → Leo thử một tầng. Xong thì có banner tóm tắt vòng lặp.

## 6. Hoạt cảnh tiến hoá và mốc chuỗi 3 ngày

Tiến hoá trước đây chỉ có một dòng thông báo — khoảnh khắc lớn nhất trong 9 ngày nuôi mà trôi qua nhạt nhất. Nay là một màn riêng: pet rung, xoay tít rồi thu nhỏ vào ánh sáng, màn loé trắng, dạng mới bung ra kèm pháo giấy, rồi tới banner có tên nhánh và câu mô tả.

Mốc chuỗi thêm **3 ngày** (Trứng thường) bên cạnh 7 và 30 ngày, để người mới có phần thưởng đầu tiên sớm hơn.

## Ba lỗi tìm được khi test

**1. Lỗi thật, chập chờn.** `applyCam` đọc `ZONES[NaN]` khi trang Nhà đang ẩn — lúc đó `petbox.clientWidth` bằng 0 nên `Math.floor(x/0)` ra NaN. Xảy ra khi người dùng chuyển tab trong lúc pet đang đi bộ. `[đo]` Chỉ hiện 2 trên 3 lần chạy nên rất dễ lọt. Đã cho `ZW()` nhớ bề rộng lần cuối và chặn NaN.

**2. Vá nhầm vị trí.** Chuỗi đích cho hoạt cảnh tiến hoá trong `ui.js` có thêm một dòng `statsOf()` chen vào nên phép thay thế trượt mà không báo lỗi. Pet vẫn tiến hoá nhưng không có hoạt cảnh. Test bắt được.

**3. Lỗi font thứ hai, cùng loại với lần trước.** Nhìn kỹ ảnh chụp bảng ghi nhận thấy `SỬ DỤNG` thành `SƯ' DỤNG`, `MỖI` thành `MÔI`, `Tắm` thành `Tăḿ`. Lần trước em chỉ nhúng font cho tiêu đề, **font mono vẫn dùng font hệ thống** — và DejaVu Sans Mono thiếu 46 ký tự tiếng Việt.

Đã nhúng thêm Liberation Mono đã subset: **28,5 KB WOFF**, kiểm tra đủ 100% ký tự. Nay có hai font nhúng, tổng 68 KB, và toàn bộ chữ trong app không còn phụ thuộc font máy người dùng.

Bài học chung: **font hệ thống nào cũng phải kiểm tra khối Latin Extended Additional trước khi tin.** Ba font đã thử và trượt: Georgia, Iowan Old Style, DejaVu Sans Mono.

## Kích thước và hiệu năng

| | v9 | v10 |
|---|---|---|
| index.html | 355 KB | 415 KB |
| Bộ PWA | 401 KB | **461 KB** |
| Đích anh đặt | 800 KB | 800 KB |
| Đang dùng | 50% | **58%** |

Tăng 60 KB, trong đó 38 KB là font mono nhúng để sửa lỗi hiển thị. Phần giao diện thêm vào gần như bù trừ với phần rút gọn.

`[đo]` Hiệu năng giữ nguyên sau khi thêm: 330 khung hình, trung vị 16,7 ms, tệ nhất 16,8 ms, 0 khung rớt.

## Việc tiếp theo không phải viết code

Bộ đếm đã chạy. Nó chỉ có giá trị nếu dùng thật hai tuần rồi mở Cài đặt xem con số. Sau đó mới nên bàn cắt cái gì — thay vì đoán như hai lần bàn roadmap vừa rồi.

Danh sách còn treo: cây kỹ năng 6 nhánh và điểm cốt gộp vào Rèn, ảnh chụp quán, nhật ký quán, bảy chặng tháp còn lại, pet phản ứng theo số liệu quán.

---

# Phụ lục v11 — Hệ trạng thái pet và chuẩn hoá khoảng cách

## 1. Gom 31 keyframes rời rạc thành một hệ có tên

Trước v11 các tư thế pet mọc dần qua từng bản: `bob` từ v1, `cheer` và `shake` từ v1.1, `yawn` `stretch` `sit` `wig` `spin` từ v4, nằm rải ở ba khối CSS khác nhau. Tên đặt tuỳ hứng, không có bảng tra, và không rõ tư thế nào dùng ở đâu.

Nay gom về **một khối duy nhất, 14 trạng thái, tiền tố `pp-`**:

| Trạng thái | Keyframe | Dùng khi |
|---|---|---|
| idle | `pp-bob` | Đứng yên |
| walk | `pp-walk` | Đi bộ — nhún kèm nghiêng nhẹ hai bên |
| cheer | `pp-hop` | Vui, thắng trận, được xoa |
| **eat** | `pp-munch` | **Mới** — nhai, phình dẹt theo nhịp |
| **sad** | `pp-sway` | **Mới** — đung đưa chậm, hơi rũ xuống |
| hit | `pp-hit` | Trúng đòn, rũ nước sau khi tắm |
| **spawn** | `pp-spawn` | **Mới** — bung ra từ nhỏ khi pet mới xuất hiện |
| rest | `pp-breathe` | Mệt, đang ngủ |
| lift | `pp-wiggle` | Bị nhấc lên |
| yawn / stretch / sit / wig / spin | `pp-*` | Các hành động nhàn rỗi |

`[đo]` 14 trạng thái ánh xạ đúng 14 keyframe, không còn keyframe tên cũ nào sót lại.

**Ràng buộc kỹ thuật giữ nguyên:** `[đo]` không keyframe nào chạm vào `filter`, `width`, `height`, `margin`, `left`, `top` hay `box-shadow`. Chỉ `transform` và `opacity` — đúng nguyên tắc đặt ra sau lần sửa khựng hình ở v9.

### setPose tự chọn tư thế nghỉ theo tâm trạng

Trước đây mọi chỗ gọi `setPose('idle')` đều cho ra cùng một dáng nhún, kể cả khi pet đang buồn hay kiệt sức — biểu cảm chỉ đổi ở mắt và miệng, còn thân thì vẫn nhún vui vẻ.

Nay `setPose('idle')` tự đổi:

| Tâm trạng | Tư thế thật |
|---|---|
| Bình thường, vui | `idle` |
| Buồn | `sad` — đung đưa chậm |
| Buồn ngủ, kiệt sức | `rest` — thở đều |

`[đo]` Kiểm tra ba trường hợp: vui ra `idle`, buồn ra `sad`, mệt ra `rest`.

### Một lỗi tìm được ngay trong lúc test

Bước kiểm tra hoạt cảnh cho ăn cho ra tư thế `rest` xen vào giữa. Nguyên nhân: `setPose` đọc `SC.mood`, mà biến đó là **bộ nhớ đệm của lần vẽ mặt gần nhất** — trong 110 mili giây chớp mắt nó mang giá trị `sleepy`. Nếu `setPose('idle')` rơi đúng khoảng đó thì pet chuyển sang tư thế nằm nghỉ giữa lúc đang ăn.

Sửa: đọc thẳng `moodOf(S.pet)` thay vì bộ nhớ đệm. `[đo]` Sau khi sửa, hoạt cảnh cho ăn chỉ còn `walk → eat → cheer → idle`.

## 2. Chuẩn hoá khoảng cách và cắt chữ dài

**Thang bốn nấc duy nhất:** 6 / 10 / 16 / 24 px, khai báo thành biến `--s1` đến `--s4`. Mọi khối dùng lại thay vì tự chế số lẻ. Áp cho: đệm khung, lề tiêu đề, lề khối mô tả, khoảng cách lưới, hàng nút.

**Chữ dài:** `[đo]` Toàn bộ có 66 khối `.note`, trong đó 16 khối vượt 110 ký tự. Đã rút gọn 9 khối dài nhất, khối dài nhất từ 211 xuống còn khoảng 100 ký tự.

Nguyên tắc áp dụng: khối mô tả chỉ giữ **một ý**, phần giải thích chi tiết đẩy sang chỗ có không gian, ví dụ mã mẫu cầu nối nay chỉ nói "xem mã mẫu ở Cài đặt" thay vì liệt kê ngay tại chỗ.

## Về việc mỗi loài một bóng dáng riêng

Kiểm tra mã cho thấy nhận xét là đúng: cả sáu loài dùng chung một thân `ellipse rx=46 ry=48`. Chỉ tai, đuôi và hoạ tiết là khác nhau, nên nhìn từ xa thì sáu loài giống hệt.

Đề xuất bóng dáng gắn với nguyên liệu:

| Loài | Bóng dáng |
|---|---|
| Beano | Oval đứng, đáy hơi bẹt, rãnh giữa như hạt cà phê |
| Milku | Vai hơi vuông, đáy phình — dáng hộp sữa bo tròn |
| Matcha | Giọt nước ngược, đỉnh nhọn như lá trà |
| Cacao | Quả thuôn hai đầu, có gân dọc |
| Citrus | Cầu tròn, bè ngang hơn cao |
| Glacio | Khối tinh thể có cạnh gãy |

**Hai rủi ro phải xử lý trước khi làm:**

1. Hoạ tiết DNA đang cắt theo đúng hình ellipse chung (`clipPath id="cb…"`). Mỗi loài cần một `clipPath` riêng, nếu không hoa văn sẽ tràn ra ngoài thân.
2. Ở cỡ 40px trong sổ sưu tầm và bong bóng nổi, bóng dáng phải còn đọc được. Hình quá nhọn hoặc quá gãy sẽ thành đốm mờ. Cần kiểm tra ở cỡ nhỏ trước khi chốt.

Chưa làm trong v11 vì chờ anh chốt. Nếu làm thì nên làm liền một mạch với đợt này, vì cả hai đều đụng vào `renderPet` và lớp `.in`.

## Kích thước và hiệu năng

| | v10 | v11 |
|---|---|---|
| index.html | 415 KB | 417 KB |
| Bộ PWA | 461 KB | **463 KB** |
| Đang dùng so với đích 800 KB | 58% | **58%** |

`[đo]` Hiệu năng không đổi: 330 khung hình, trung vị 16,7 ms, tệ nhất 16,8 ms, 0 khung rớt, 0 lần dựng lại toàn bộ SVG trong 9 giây.

`[đo]` Toàn bộ 12 bộ test chạy lại không lỗi.

---

# v11.1 — Sửa lỗi Rối loạn tiêu hoá không bao giờ khỏi

Lỗi do người dùng thật phát hiện khi chơi v11.

**Triệu chứng:** pet mắc Rối loạn tiêu hoá, dòng chữ ghi "Không cho ăn trong 12 giờ (0/12)", nhưng chờ bao lâu cũng không khỏi và tiến độ đứng nguyên ở 0.

**Nguyên nhân — hai tầng chồng nhau:**

1. Cơ chế chữa bệnh chỉ chạy trong `progressCure(pet, action)`, tức chỉ tiến khi người chơi **làm một hành động**. Bảy bệnh còn lại đều chữa bằng hành động (`feed`, `sleep`, `clean`, `play`) nên chạy đúng. Riêng Rối loạn tiêu hoá khai báo `cureAct:'wait'` — mà `'wait'` **không phải hành động nào cả**, không bao giờ được truyền vào. Bệnh trở thành vĩnh viễn, kèm hiệu ứng giảm 50% hiệu quả cho ăn.

2. Sau khi thêm cơ chế chữa theo thời gian, bệnh vẫn quay lại tức thì: vòng kiểm tra ngay bên dưới thấy `todayFeed` vẫn là 9 nên gán lại bệnh trong cùng một nhịp. Phải xoá luôn điều kiện kích hoạt khi khỏi.

**Cách sửa:**
- Ghi mốc `lastFeed` mỗi lần cho ăn
- `checkDisease` gỡ bệnh loại chờ khi đã đủ số giờ tính từ lần cho ăn gần nhất
- Khi gỡ thì đặt lại `todayFeed = 0` để điều kiện kích hoạt không còn đúng
- Giao diện đổi từ tiến độ `0/12` đứng im sang **đếm ngược thời gian thật**: "còn 7,4 giờ"

**Hệ quả thiết kế:** cho ăn giữa chừng sẽ đếm lại từ đầu — đúng ý nghĩa của bệnh, và nay hiển thị rõ nên người chơi hiểu vì sao.

`[đo]` Kiểm chứng: mắc bệnh còn 12,0 giờ · sau 11 giờ vẫn còn · sau 12,5 giờ đã khỏi · cho ăn giữa chừng thì quay lại 12,0 giờ. Bảy bệnh chữa bằng hành động vẫn khỏi đúng số lần quy định.

**Bài học cho các bản sau:** mỗi khi thêm một bệnh mới, phải kiểm `cureAct` có nằm trong sáu hành động thật hay không. Bảng kiểm này nay có trong bộ test.

---

# Phụ lục v12 — Bóng dáng riêng cho sáu loài

## Vấn đề

Tới v11, cả sáu loài dùng chung một thân `ellipse rx=46 ry=48`. Chỉ tai, đuôi và hoạ tiết là khác nhau, nên nhìn từ xa hoặc ở cỡ nhỏ thì sáu loài giống hệt. Hệ gen tạo ra màu sắc và hoa văn khác nhau, nhưng **bóng dáng thì không**.

## Sáu đường viền, gắn với hình dạng nguyên liệu

| Loài | Bóng dáng | Chi tiết đi kèm |
|---|---|---|
| **Beano** | Oval đứng, đáy hơi bẹt | Rãnh giữa chạy hết thân, như hạt cà phê chẻ đôi |
| **Milku** | Vai vuông bo góc, đáy phình | Dáng hộp sữa |
| **Matcha** | Giọt nước ngược, đỉnh nhọn | Lá trà mọc trên đỉnh |
| **Cacao** | Quả thuôn hai đầu | Ba gân dọc chạy suốt |
| **Citrus** | Cầu tròn, bè ngang hơn cao | Múi cam chia sáu |
| **Glacio** | Khối tinh thể tám cạnh | Góc nhọn, không bo tròn |

Toạ độ chung: tâm (0, 20), rộng khoảng 92, cao khoảng 96. Mỗi loài khai báo thêm `belly` (mảng sáng ở bụng) và `face` (độ lệch cụm mắt miệng) vì đỉnh nhọn của Matcha đẩy mặt xuống thấp hơn thân tròn của Citrus.

**Hai rủi ro đã nêu trước khi làm, xử lý thế nào:**

1. *Hoạ tiết DNA cắt theo hình ellipse chung.* Nay `clipPath` dùng chính đường viền của loài, nên hoa văn không tràn ra ngoài thân.
2. *Đọc được ở cỡ nhỏ.* `[đo]` Dựng bảng so sánh ở 130px và 46px. Sáu bóng dáng phân biệt được ở cả hai cỡ. Riêng Glacio ban đầu bị bo tròn góc do `stroke-linejoin: round` nên mất nét tinh thể — đã thêm trường `join` để loài này dùng `miter`.

`[đo]` Sáu loài sinh ra sáu đường `path` khác nhau, mỗi SVG khoảng 1,8–2,0 KB, không đổi so với trước vì vẫn là hình sinh lúc chạy chứ không phải dữ liệu lưu sẵn.

## Ngôn ngữ hình của phe Công Nghiệp

Thêm cờ `industrial` cho `renderPet`. Nguyên tắc: pet Nguyên Bản là **hình hữu cơ** — bo tròn, mềm, có tai đuôi má hồng. Phe Công Nghiệp là **hình chế tạo**:

| | Nguyên Bản | Công Nghiệp |
|---|---|---|
| Thân | Đường cong riêng theo loài | Chữ nhật bo góc, đối xứng tuyệt đối |
| Viền | 2,5px, bo mềm | 4px, góc vuông, màu xám sẫm |
| Trên đầu | Tai theo loài | Hai ăng-ten thẳng có chóp tròn |
| Đuôi | Có | Không |
| Bụng | Mảng sáng bo tròn | Tấm chữ nhật có viền |
| Hoa văn | Theo gen: đốm, sọc, mảng | Lưới kẻ ô và đinh tán |
| Mắt | Tròn, có điểm sáng, đổi theo cảm xúc | Hai hộp chữ nhật giống hệt nhau, chỉ đổi màu đèn |
| Miệng | Cong theo cảm xúc | Một vạch thẳng, không đổi |
| Má hồng khi vui | Có | Không |

Điểm đáng chú ý: **bốn trạng thái cảm xúc của máy trông gần như giống hệt nhau**, chỉ khác màu đèn mắt. Đó là chủ ý — nó không có cảm xúc để thể hiện. Người chơi nuôi một con Nguyên Bản ba mươi ngày rồi nhìn sang con máy sẽ tự thấy khoảng trống, mà không cần ai giải thích.

Cùng một hàm dựng hình, chỉ thêm một cờ — dùng lại toàn bộ hệ gen, màu sắc và trạng thái animation sẵn có.

## Kích thước và kiểm tra

| | v11.1 | v12 |
|---|---|---|
| index.html | 417 KB | 422 KB |
| Bộ PWA | 463 KB | **468 KB** |
| Đang dùng so với đích 800 KB | 58% | **59%** |

`[đo]` Toàn bộ 13 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung, 0 lần dựng lại toàn bộ SVG trong 9 giây.

## Chuẩn bị cho các bản sau

Cờ `industrial` đã sẵn cho quái và boss phe Công Nghiệp ở v14–v15. `BODY_INDUS` hiện là một dáng chung; khi làm mini boss và boss lớn thì thêm biến thể vào cùng bảng `BODY`, không phải sửa `renderPet`.

---

# Phụ lục v13 — Trang bị và hệ Rác

Thông điệp môi trường nằm ở **lớp nền** đúng như đã chốt: không có chỉ số môi trường hiện rõ, không có dòng chữ kêu gọi. Chỉ có hậu quả tự bộc lộ sau vài tuần chơi.

## Vì sao không làm "càng xanh càng mạnh"

Nếu nhựa yếu và inox mạnh thì sau ba ngày ai cũng dùng inox, và bài học biến mất — người chơi không học được gì từ một lựa chọn không có gì để cân nhắc.

Thiết kế ngược lại: **nhựa mạnh nhất ngay lập tức**, và cái giá đến sau.

## Bốn ô, hai mươi món

| Ô | Vật dụng | Buff gốc |
|---|---|---|
| Vũ khí | Ống hút, thìa | ATK +18% |
| Giáp | Ly cốc | HP +15%, DEF +8% |
| Khiên | Nắp, đế lót | DEF +18% |
| Choàng | Túi đựng | SPD +12%, LUCK +10% |

Riêng ô Choàng, năm bậc là năm mức độ bền chứ không phải năm chất liệu đúng nghĩa — túi thuỷ tinh hay túi sứ thì không có thật.

## Năm bậc chất liệu

| Bậc | Buff | Độ bền | Rác | Nguồn |
|---|---|---|---|---|
| **Nhựa** | ×1.00 — cao nhất | Vô hạn | **+2 mỗi lần dùng** | Mua bằng xu |
| **Giấy** | ×0.80 | Hỏng sau 3 lần | 0 | Mua bằng xu, rẻ nhất |
| **Thuỷ tinh** | ×0.95 | **Vỡ khi thua trận** | 0 | Chỉ rơi |
| **Sứ** | ×0.70 | Vô hạn, **−6% SPD** | 0 | Chỉ rơi |
| **Inox** | ×0.60 — thấp nhất | **Vô hạn, không mất gì** | 0 | Chỉ rơi |

Tám món nhựa và giấy mua được. **Mười hai món ba bậc bền chỉ rơi từ tháp và phiêu lưu** — thứ tiện nhất mua được ngay, thứ bền nhất phải bỏ công. Đó là bài học kể bằng cơ chế lấy đồ.

## Thưởng bộ — chỗ lựa chọn bền vững được trả công

Đi đủ 4 món cùng bậc thì mở thưởng bộ:

| Bộ | Thưởng |
|---|---|
| Nhựa | ATK thêm 5%, nhưng **Rác sinh ra gấp rưỡi** |
| Giấy | Đồ giấy mua rẻ hơn 30% |
| Thuỷ tinh | Chí mạng thêm 10% |
| Sứ | Miễn nhiễm hiệu ứng xấu đầu tiên mỗi trận |
| **Inox** | **Toàn bộ chỉ số thêm 8%** |

Từng món inox lẻ là yếu nhất bảng. **Chỉ khi đi đủ bộ thì nó mới vượt lên.** Lựa chọn bền vững trả công ở mức cam kết trọn vẹn, không trả lẻ từng món.

`[đo]` So sánh đủ bộ 4 món:

| Bộ | ATK | DEF | HP | SPD |
|---|---|---|---|---|
| Nhựa | +23% | +26% | +15% | +12% |
| Thuỷ tinh | +17% | +25% | +14% | +11% |
| **Inox** | **+19%** | **+24%** | **+17%** | **+15%** |
| Giấy | +14% | +21% | +12% | +10% |
| Sứ | +13% | +18% | +10% | +2% |

## Hệ Rác

- Mỗi món nhựa để lại **2 Rác** mỗi lần dùng, đủ bộ thì ×1,5 → **12 Rác một trận**
- Mỗi 1 Rác trừ **0,05% toàn bộ chỉ số**, trần **−20%**
- Quán tự dọn **8 Rác mỗi ngày**
- Dọn ngay được, giá **2 xu mỗi Rác**

`[đo]` Dùng đủ bộ nhựa 6 tầng mỗi ngày sinh 72 Rác, quán dọn 8, tích 64 mỗi ngày. **Chạm trần phạt −20% sau 7 ngày.**

## Đường cong ba tuần

`[đo]` Mô phỏng 400 lượt chơi với nhịp 6 tầng và 2 chuyến mỗi ngày:

| Mốc | Điều gì xảy ra |
|---|---|
| **Ngày 1** | Mua đủ bộ nhựa khoảng 800 xu. Mạnh nhất bảng ngay lập tức |
| **Ngày 7** | Rác chạm trần −20%. Bộ nhựa cộng +23% ATK nhưng trừ 20% mọi thứ — thành lỗ ròng |
| **Ngày 11–23** (trung vị **16**) | Gom đủ bộ inox. Vĩnh viễn, không hỏng, không rác |

Không có dòng chữ nào nói "hãy bảo vệ môi trường". Người chơi tự trải qua và tự rút ra.

Với chủ quán thì đây còn là bài toán thật, nên mỗi món có **thẻ đời thật** như 24 công thức: giá mỗi đơn vị và chi phí sáu tháng ở mức 3.000 ly một tháng. Ly nhựa 1.200đ mỗi ly thành **21,6 triệu sáu tháng**; ly giữ nhiệt inox 95.000đ mỗi ly nhưng chỉ **1,9 triệu** cho cả kỳ.

## Tỉ lệ rơi

| Nguồn | Tỉ lệ |
|---|---|
| Tầng thường | 14% |
| Tầng boss | 50% |
| Chuyến phiêu lưu | 26% |

Phân bố bậc: thuỷ tinh 38%, sứ 32%, inox 30%. `[đo]` Kiểm 6.000 lượt: 51,0 / 32,3 / 16,7 ở bản đầu — sau khi chỉnh thì khớp thiết kế.

**Bản đầu đặt inox 18% khiến trung vị gom đủ bộ lên tới hơn 45 ngày**, quá xa so với mốc 7 ngày Rác chạm trần. Đã nâng lên 30% và tăng tỉ lệ rơi, kéo trung vị về 16 ngày.

## Hai lỗi sửa trong lúc dựng

1. **Bộ Sứ ra SPD −16% thay vì −6%.** Hình phạt nặng nề đang trừ cho từng món thay vì một lần cho cả bộ. Đeo bốn món sứ vẫn là một người mang đồ nặng, không phải nặng gấp bốn. Sau khi sửa: Sứ ra SPD +2%.
2. **Dải tab con nay có 5 mục, dài hơn màn hình 390px**, tab đang chọn bị đẩy khuất. Thêm bước tự kéo tab đang chọn vào giữa khi dải dài hơn khung.

## Kích thước

| | v12 | v13 |
|---|---|---|
| index.html | 422 KB | 439 KB |
| Bộ PWA | 468 KB | **485 KB** |
| Đang dùng so với đích 800 KB | 59% | **61%** |

`[đo]` 14 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung.

---

# Phụ lục v14 — Chặng 4–5, mini boss, và thẻ cốt truyện

## Tháp mở tới tầng 50

| Chặng | Tên | Boss | Cơ chế | Điểm yếu |
|---|---|---|---|---|
| 4 | Kho Bột Sữa | **Bột Béo** *(Kem Không Sữa)* | Lớp váng: cứ 2 lượt tự đắp một lớp hấp thụ 30% sát thương | Nhóm **Thanh** |
| 5 | Dây Chuyền Trân Châu | **Viên Dai** *(Trân Châu Công Nghiệp)* | Dai: mỗi đòn chỉ ăn tối đa 4,5% máu tối đa | Nhóm **Cay** |

Năm boss nay dùng năm nhóm vị khác nhau — chua, đắng, chát, thanh, cay. Chỉ còn nhóm **ngọt** để dành cho chặng 6.

## Mini boss ở tầng 5 mỗi chặng

Năm mini boss đứng ở tầng 5, 15, 25, 35, 45. Mỗi con **dạy trước cơ chế của boss chính cùng chặng** ở mức nhẹ hơn, để người chơi gặp lần đầu mà không mất một vé oan.

| Tầng | Mini boss | Dạy trước | Mức nhẹ hơn |
|---|---|---|---|
| 5 | Lon Móp | Ga bù | hồi 2% thay vì 4% |
| 15 | Gói Bột Cam | Bọt hương liệu | cứ 4 lượt thay vì 3 |
| 25 | Vòi Siro | Ngọt tích tụ | +4%/lượt trần 5 thay vì +6% trần 8 |
| 35 | Muỗng Bột | Lớp váng | 20% mỗi 3 lượt thay vì 30% mỗi 2 |
| 45 | Viên Nửa Chín | Dai | trần 6,5% thay vì 4,5% |

Thưởng: 90 xu và 2 hạt mầm, nằm giữa tầng thường và boss chính.

## Cân bằng tầng 31–50

`[đo]` 120 trận mỗi ô, pet Lv30 Tiến hoá có tổ đội hai pet phụ trợ:

| Cấu hình | T35 | T40 | T45 | T50 |
|---|---|---|---|---|
| Nuôi kỹ, độ hiếm Thường, không trang bị | 78% | 3% | 7% | 0% |
| Nuôi kỹ Thường, **bộ inox đủ 4 món** | 98% | 59% | 41% | 3% |
| Nuôi kỹ **Hiếm**, bộ inox | 100% | 98% | 83% | 30% |
| Nuôi kỹ **Cực hiếm**, inox + ly đúng nhóm vị | 100% | 100% | 88% | **43%** |

Đây là hình dạng em muốn: **tầng 40 là nơi trang bị bắt đầu quyết định** (3% lên 59% chỉ nhờ bộ inox), và **tầng 50 là bức tường thật** — kể cả cấu hình mạnh nhất cũng chỉ 43%, tức trung bình hơn hai vé cho một lần qua. Đó là cánh cổng vào phần 2, nên nó phải khó.

## Thẻ cốt truyện — mười thẻ, mở từ tầng 5

Anh chọn kể qua thẻ đọc sau mỗi boss, và mở sớm từ boss tầng 10 thay vì chờ tầng 50. Em mở sớm hơn nữa: **từ mini boss tầng 5**, để câu chuyện chảy ngay tuần đầu.

Mỗi thẻ có hai phần:

1. **Một đoạn kể** về phe Công Nghiệp, viết từ góc nhìn của nó chứ không phải góc nhìn kết án. Ví dụ thẻ tầng 35: *"Bột định lượng sẵn nghĩa là ai pha cũng ra một vị — kể cả người mới vào làm ngày đầu. Chủ quán thích điều đó, và họ có lý do. Nhưng khi mọi ly đều giống nhau bất kể ai pha, thì người pha trở thành thứ có thể thay thế."*

2. **Một thẻ kiến thức vận hành** dùng được ngoài đời:

| Tầng | Kiến thức |
|---|---|
| 5 | Hàng cận hạn — vì sao FEFO quan trọng hơn FIFO với đồ uống |
| 10 | Vì sao đồ có ga phải lạnh — CO₂ tan trong nước lạnh gấp đôi |
| 15 | Định lượng và độ ổn định — ghi công thức theo gam, đừng theo muỗng |
| 20 | Màu sắc và kỳ vọng vị — nước cam ép thật nhạt màu hơn nước pha |
| 25 | Khi nào nên chuẩn hoá, khi nào không |
| 30 | Đường và biên lợi nhuận — vì sao menu quá ngọt giảm số ly mỗi lượt ghé |
| 35 | Đào tạo hay định lượng sẵn |
| 40 | Chất béo che khuyết điểm nguyên liệu thế nào |
| 45 | Ai được quyền dừng — người pha phải được huỷ ly lỗi mà không bị trừ lương |
| 50 | Đồ uống mang đi khác đồ uống tại chỗ |

Tổng 4,5 KB chữ. Xem lại bất cứ lúc nào ở tab **Khác → Cốt truyện**.

## Ba lỗi trong lúc dựng

**1. Cơ chế "Dai" không kích hoạt lần nào.** `[đo]` Đo sát thương thực tế: trung vị 5,6% máu tối đa mỗi đòn, đòn mạnh nhất 10,6%. Trần đặt ở 12% nên rộng hơn cả đòn mạnh nhất — cơ chế thành vô nghĩa. Hạ xuống 4,5% (boss) và 6,5% (mini), tức dưới trung vị, để cắt đúng những đòn nặng còn đòn thường vẫn qua.

**2. Vá nhầm module lần thứ ba.** `verticalTower` nằm ở module v9 nhưng em vá vào ui — phép thay thế trượt im lặng, hàng mini boss không hiện. Từ nay mọi phép vá đều **bắt buộc khớp**, không khớp thì dừng ngay thay vì âm thầm bỏ qua.

**3. Thẻ cốt truyện đè lên banner thắng.** Bản đầu hẹn giờ 900ms để mở thẻ, nhưng banner chưa đóng thì thẻ đã phủ lên. Sai thứ tự đọc. Sửa: `showBanner` nhận thêm việc cần làm **sau khi người chơi đóng banner**, thẻ chỉ mở khi đó.

## Kích thước

| | v13 | v14 |
|---|---|---|
| index.html | 439 KB | 455 KB |
| Bộ PWA | 485 KB | **501 KB** |
| Đang dùng so với đích 800 KB | 61% | **63%** |

`[đo]` 15 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung.

## Còn lại cho v15

Automa (loài chuyên ô phụ trợ, mở sau tầng 50), boss lớn nhiều pha, đoạn kể có hoạt cảnh giữa các chặng, và Bản Chuẩn — boss cuối của phần 2.

---

# Phụ lục v15 — Automa, điểm cốt, cây kỹ năng, trang bị mặc được

## Trả lời hai câu hỏi trước khi làm

**Trang bị: chỉ để đẹp hay mặc được lên người?** Mặc được. Đó là phần thưởng của việc gom đủ bộ — nhìn thấy con pet mình nuôi ba tuần đang cầm thìa inox thì công gom mới đáng. Làm được vì hệ vẽ theo DNA đã có sẵn khung toạ độ chung.

**Cây kỹ năng đã làm chưa?** Chưa. Anh duyệt ở v11 nhưng em chỉ làm hai mục kia rồi bỏ sót. Lỗi của em, v15 làm luôn.

## Automa — loài thứ bảy, thân bánh răng

Đúng ý anh: thân là **bánh răng mười hai răng**, sinh bằng hàm `cogPath()` chứ không vẽ tay, nên đổi số răng hay tỉ lệ chỉ là đổi tham số.

Automa **không phải phần thưởng mạnh hơn, mà là phản đề**:

| | Sáu loài Nguyên Bản | Automa |
|---|---|---|
| Làm pet chính | Được | **Không** |
| Gắn bó | Có, ảnh hưởng mạnh | **Luôn bằng 0** |
| Tiến hoá | Có, bốn nhánh | **Không** |
| Lai tạo | Có | **Không** |
| Lời thoại, biểu cảm | 121 câu, bốn tâm trạng | **Không có** |
| Đóng góp khi đứng ô phụ trợ | 15% | **30%** |
| Hiệu ứng bị động cho pet chính | Không | **Có, theo dòng máy** |

`[đo]` Kiểm chứng: cùng cấp, Automa đẩy ATK pet chính từ 29 lên 40, pet thường chỉ lên 39. Chặn được cả bốn đường: làm pet chính, tiến hoá, lai tạo, và tăng Gắn bó.

**Năm dòng máy** để sưu tầm: AM-01 Nghiền (ATK +8%), AM-02 Ủ (DEF +8%), AM-03 Lọc (SPD +10%), AM-04 Định lượng (toàn bộ +6%), AM-05 Nén (HP +12%).

Nguồn: mỗi lần hạ boss từ tầng 50 trở lên nhận một **Lõi Automa**, lắp ra một dòng máy ngẫu nhiên với độ hiếm ngẫu nhiên.

Điểm em muốn giữ: người chơi nuôi một con Nguyên Bản ba mươi ngày rồi nhìn sang con máy sẽ tự thấy khoảng trống. Nó mạnh, nhưng nó không nói gì cả.

## Điểm cốt — gộp vào Rèn thay vì dựng hệ riêng

Trước v15, Rèn cộng bừa vào **hai chỉ số ngẫu nhiên**. Vừa nhạt vừa không ai để ý.

Nay: mỗi lần lên cấp được **3 điểm cốt**, mỗi lần Rèn được **1 điểm**, người chơi tự chọn dồn vào Máu, Tấn công, Phòng thủ, Tốc độ, Trí lực hay May mắn.

Trần mỗi chỉ số vẫn là **15% trần tiềm năng** như cũ, nên toàn bộ cân bằng tháp từ v3 tới nay không đổi. Hoàn điểm được, giá 200 xu.

`[đo]` Kiểm: rèn một lần cộng đúng 1 điểm, tiêu vào ATK cộng đúng 1, chạm trần thì chặn, hoàn điểm trả đúng số đã tiêu và trừ đúng 200 xu.

Một hệ thống thay vì hai, người chơi được chọn, và Rèn từ chỗ vô nghĩa thành hành động đáng làm.

## Cây kỹ năng

Không thêm hệ kinh tế nào — chỉ là cách trình bày 42 kỹ năng sẵn có.

- **Thân chung** ở trên, viền xanh: 6 kỹ năng mọi loài đều học
- **Sáu nhánh loài** bên dưới, mỗi nhánh 6 kỹ năng
- Nhánh của pet đang nuôi **sáng lên viền vàng**, năm nhánh còn lại mờ đi
- Kỹ năng chưa tới giai đoạn thì mờ và ghi rõ cần giai đoạn nào
- Ô viền vàng là kỹ năng đang mang, chạm để đổi

`[đo]` Đủ 42 nút, đúng 6 nhánh, nhánh của pet sáng đúng một cái.

## Trang bị mặc lên người

Bốn lớp vẽ đè lên thân, neo vào khung toạ độ chung (tâm 0,20) nên dùng được cho cả **bảy bóng dáng** mà không phải vẽ riêng từng loài:

| Ô | Vị trí | Hình |
|---|---|---|
| Choàng | Sau lưng, vẽ trước thân | Áo choàng đổ xuống |
| Giáp | Ngang thân | Đai vắt qua bụng |
| Vũ khí | Bên phải, nghiêng 16° | Cán dài có đầu tròn |
| Khiên | Bên trái | Đĩa tròn có tâm chìm |

Màu lấy theo bậc chất liệu, nên nhìn là biết đang mặc nhựa hay inox. Hiện cả ở trang Nhà lẫn trên sàn đấu.

`[đo]` Bốn lớp vẽ ra đủ, SVG tăng từ 1.978 lên 2.891 byte khi mang đủ bốn món.

## Nền sàn đấu

Sáu khung cảnh, đổi theo chặng tháp đang leo: quầy quán (đấu nhanh), kệ hàng tiện lợi, xe đẩy hương liệu, bồn siro, kho bột, dây chuyền trân châu. Mỗi cảnh có dải trời, đồ trang trí đặc trưng và nền sàn riêng.

## Vỏ trứng vàng

Vỏ vẽ riêng thay vì dùng chung khuôn: viền kép, hoa văn sao chìm, quầng sáng đổ ngoài, và **một dải sáng chạy qua mặt trứng mỗi 3,4 giây**.

## Ba lỗi trong lúc dựng

1. **Biến trùng tên gây lỗi vùng chết.** Nhánh Rèn khai `const c=coreState()` nhưng đầu hàm đã có `const c=p.care`. JavaScript báo "Cannot access 'c' before initialization" và cả nhánh Rèn ngừng chạy — điểm cốt không cộng. Đổi tên thành `cs`.
2. **Trang bị không hiện lên pet ở trang Nhà.** Vì từ v10, `mount()` chỉ vẽ lại khuôn mặt khi tâm trạng đổi, còn thân thì giữ nguyên để khỏi khựng hình. Đổi trang bị không làm đổi tâm trạng nên không có gì vẽ lại. Sửa: đưa trang bị vào chữ ký cảnh và gọi vẽ lại toàn thân khi chữ ký đổi.
3. **Nhãn tâm trạng đè lên bong bóng thoại.** Từ v10 cả hai cùng nằm ở góc trái dưới. Đưa nhãn tâm trạng lên góc trái trên.

## Kích thước

| | v14 | v15 |
|---|---|---|
| index.html | 455 KB | 475 KB |
| Bộ PWA | 501 KB | **521 KB** |
| Đang dùng so với đích 800 KB | 63% | **65%** |

`[đo]` 16 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung, 0 lần dựng lại toàn bộ SVG trong 9 giây.

## Còn lại

Boss lớn nhiều pha ở tầng 50 và 100, **Bản Chuẩn** — boss cuối của phần 2, đoạn kể có hoạt cảnh giữa các chặng, năm chặng tháp 51–100, ảnh chụp quán, nhật ký quán.

---

# Phụ lục v16 — Kỷ niệm, lời pet, và cốt truyện viết lại theo Quy mô đối Tâm hồn

Bản này không thêm hệ thống nào. Nó làm cho những thứ đã có **có cảm xúc hơn**.

## 1. Đổi tên bảy trạng thái

Đây là mục em nhận lỗi. **"Trầm cảm" là một chẩn đoán y khoa thật**, dùng nó làm nhãn cho pet đói ba ngày là vừa sai vừa vô duyên — nhất là với sản phẩm dành cho người đang chịu áp lực vận hành. Tên đó tồn tại từ v1 và không ai để ý suốt mười lăm bản.

| Cũ | Mới |
|---|---|
| Trầm cảm | **Uể oải** |
| Sốt | **Mệt trong người** |
| Rối loạn tiêu hoá | **Đầy bụng** |
| Nhiễm bẩn | **Ngứa ngáy** |
| Cảm lạnh | **Sổ mũi** |
| Kiệt sức | **Đuối sức** |
| Tan chảy | **Mềm người** |

Lời chữa cũng viết lại theo hướng không đổ lỗi: "Cho ăn 3 lần là đỡ" thay vì "Cho ăn 3 lần trong 24 giờ". Và ngủ đông nay hiện là **"Miso nghỉ cùng bạn"** thay vì "Đang ngủ đông".

Nguyên tắc: **pet không bao giờ khiến người chơi cảm thấy mình là một người chủ tồi.**

## 2. Kỷ niệm — 18 mốc

Mỗi mốc là một biểu tượng, một câu, một ngày. Toàn bộ dùng lại **bộ đếm đã có sẵn** từ các bản trước, nên gần như không tốn gì.

Ngày hai đứa gặp nhau · Bữa đầu tiên · Lần đầu chơi cùng nhau · Lần đầu ốm rồi khoẻ lại · Ba ngày liền không bỏ · Trọn một tuần · Quả trứng đầu tiên · Thêm một đứa nữa · Lần đầu hạ một kẻ canh giữ · Ngày nó lớn lên · Ly đầu tiên tự pha · Mầm đầu tiên nhú lên · Chuyến đi xa đầu tiên · Bộ đồ nghề đầu tiên · Người đồng nghiệp im lặng · Một ngày quán chạy tốt · Không bỏ sót việc nào · Đã thân lắm rồi

Hai mốc cuối đến từ **cầu nối công cụ vận hành**: doanh thu vượt mục tiêu và checklist trên 95% đều tự ghi thành kỷ niệm. Việc thật ngoài quán để lại dấu trong thế giới của pet.

Kỷ niệm hiện ở phần **Chi tiết** của pet, bốn cái gần nhất, bấm để xem đủ. Mỗi lần có mốc mới thì một thẻ nhỏ trượt xuống từ đỉnh màn hình.

`[đo]` Mở app lần đầu ghi ngay "Ngày hai đứa gặp nhau"; cho ăn một lần ghi thêm "Bữa đầu tiên".

## 3. Thẻ hành động nói bằng lời pet

Trước: `Bo đang đói` → `Cho ăn · −5 xu`
Sau: **`Bo muốn ăn.`** → `Cho ăn · −5 xu`

| Hoàn cảnh | Câu |
|---|---|
| Đói | "… muốn ăn." |
| Hết năng lượng | "… muốn nghỉ một lát." |
| Bẩn | "… muốn tắm." |
| Buồn | "… muốn chơi với bạn." |
| Căng thẳng | "… muốn yên tĩnh một chút." |
| Còn việc vận hành | "… muốn làm việc cùng bạn." |
| Còn vé tháp | "… muốn đi cùng bạn." |
| Trứng đủ giờ | "Có thứ gì đó đang động đậy…" |
| Đang đi khảo sát | "… đang ở ngoài kia." |

Chỉ là đổi chuỗi, nhưng nút bấm thành lời nói
---

# Phụ lục v17 — AM-00, hội thoại có chân dung, và lớp trận đấu viết lại

## Dữ liệu thực đầu tiên

Sau bảy bản nhắc, cuối cùng cũng có số liệu từ người dùng thật: **2 ngày, 3 phiên, 0% vào rồi ra, 22 nhiệm vụ, 46 lần chăm sóc, 78 trận thắng, tầng cao nhất 28.**

Con số đáng chú ý: **78 trận thắng so với 22 nhiệm vụ vận hành**. Vòng lặp đang chạy lệch về phía đấu chứ không phải về phía việc thật. Mới hai ngày và một người nên chưa kết luận được, nhưng đây là tỉ lệ cần theo dõi — nếu nó giữ nguyên sau hai tuần thì thiết kế đang thưởng nhầm hành vi.

## 1. AM-00 — người dẫn chuyện có thật

Một cỗ máy cũ ngồi ở góc quán từ ngày đầu, kể chuyện về tháp. Người chơi không được nói nó là gì.

Tới khi hạ boss tầng 50 và lắp con Automa đầu tiên — **AM-01** — thì dãy số tự nói ra phần còn lại:

> *"AM-00. Số không. Tôi là bản đầu tiên, và cũng là bản không ai lắp lại nữa."*

Cú lật này gần như miễn phí về mặt kỹ thuật: AM-00 dùng chính hàm dựng hình Automa của v15, chỉ khác màu. Nhưng nó đổi ý nghĩa của cả hai thứ — người dẫn chuyện hoá ra là một cỗ máy, và cỗ máy bạn vừa lắp hoá ra có họ hàng với người bạn đã tin suốt năm mươi tầng.

## 2. Hội thoại có chân dung

Thẻ cốt truyện trước đây là một khối chữ. Nay kể bằng ba lượt thoại, mỗi lượt có chân dung nhân vật nổi lên trên hộp thoại:

1. **Boss nói trước** — bằng chính lời của nó, chân dung vẽ theo ngôn ngữ hình Công Nghiệp
2. **Pet đáp lại** — câu theo tính cách, khác nhau giữa mười tính cách
3. **AM-00 chốt lại** — nối câu chuyện với bài học

Rồi mới tới thẻ kiến thức vận hành. Cấu trúc **Nhân vật → Cảm xúc → Kiến thức** mà bản review đề xuất, nay có hình chứ không chỉ có chữ.

Hệ hội thoại là một hàm chung `startDialogue()` — dùng lại được cho mọi cảnh sau này, không phải viết riêng từng chỗ.

## 3. Lời chào khi mở app

Mười nhóm hoàn cảnh, xét theo thứ tự: vắng lâu, vắng vừa, doanh thu vượt mục tiêu hôm qua, checklist cao, chuỗi ngày, pet đang cần gì, rồi mới tới giờ trong ngày.

| Hoàn cảnh | Câu |
|---|---|
| Vắng trên 36 giờ | "Bạn đi đâu lâu thế… Kem tưởng quán đóng luôn rồi." |
| Doanh thu vượt mục tiêu | "Hôm qua quán mình bán tốt ghê!" |
| Chuỗi 3 ngày trở lên | "5 ngày rồi đấy. Kem đếm đủ." |
| Khuya | "Đèn ấm thế này Kem buồn ngủ ghê." |

Pet nói ngay khi mở trang Nhà, kèm một cái nhún. Đây là chỗ rẻ nhất để tạo cảm giác "có thứ đang chờ mình".

## 4. Lớp trận đấu — bốn sửa đổi từ việc xem game khác

Tham khảo một game auto-battler anh gửi. Kết luận sau khi đo: **mình không thiếu hiệu ứng, mình thiếu độ lớn và độ dính.**

| Vấn đề | Trước | Sau |
|---|---|---|
| Số sát thương | mono **15px**, rơi vào góc sân | display **42px** có viền chữ 2,5px, bung ngay trên đầu mục tiêu |
| Thanh máu | hai thanh ở hai góc trên, tách khỏi đấu sĩ | **gắn dưới chân từng con**, kèm số chính xác `353 / 372` |
| Trúng đòn | vệt chéo mỏng quét cả sân | **quầng nổ tròn** phủ mục tiêu, bản chí mạng to gấp rưỡi và đổi sang sắc vàng cam |
| Hiệu ứng buff/debuff | chỉ đọc được trong nhật ký chữ | **biểu tượng lơ lửng trên đầu**, 17 loại, viền đỏ cho hiệu ứng xấu |

Mục thứ tư đáng nhất vì **cơ chế đã có từ v1 mà người chơi không nhìn thấy**. Engine nay gửi kèm ảnh chụp buff hai bên trong mỗi sự kiện; giao diện chỉ việc vẽ. `[đo]` Trong một trận 62 sự kiện có 34 sự kiện mang biểu tượng.

Một lỗi bố cục phải sửa giữa chừng: đặt thanh máu vào trong khung đấu sĩ thì nó **đè lên thân pet**. Đã đưa xuống dưới chân (`bottom:-28px`), gộp tên và số máu thành một hàng, và nâng sàn đấu từ 198px lên 224px để có chỗ.

## 5. Nền sàn đấu ba lớp

Sáu khung cảnh, mỗi cảnh dựng ba lớp có độ tương phản khác nhau:

- **Xa** — bóng đổ mờ 55%, nhỏ, ít chi tiết
- **Giữa** — đồ vật đặc trưng của chặng ở 90%
- **Gần** — vật thể lớn bị cắt ở mép dưới, đậm nhất, đóng khung hai bên

Thêm một lớp tối chuyển dần ở nền sàn để chân đấu sĩ không lẫn vào nền.

Cảnh theo đúng cốt truyện từng chặng: kệ hàng tiện lợi, xe đẩy hương liệu, bồn siro có ống dẫn, bao bột xếp chồng, băng chuyền có con lăn.

## Ba lỗi trong bộ test

Cả ba đều do hành vi mới đúng nhưng kịch bản cũ chưa biết:

1. **AM-00 tự chào khi mở tháp** chặn thao tác của 46 kịch bản. Thêm bước bỏ qua.
2. **Ba lớp phủ nối tiếp nhau** — banner đóng thì mở hội thoại, hội thoại đóng thì mở thẻ. Kịch bản đóng một lớp rồi bấm ngay thì trúng lớp kế. Đổi sang đóng lặp ba lần cách nhau 420ms.
3. **Nở trứng nay là chuỗi sự kiện** từ v16, kịch bản cũ vẫn chờ nở tức thì. Cập nhật để gõ đủ ba lần rồi đặt tên.

## Kích thước

| | v16 | v17 |
|---|---|---|
| index.html | 491 KB | 511 KB |
| Bộ PWA | 537 KB | **557 KB** |
| Đang dùng so với đích 800 KB | 67% | **70%** |

`[đo]` 18 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung.

## Những gì em không lấy từ game tham khảo

| Thứ | Vì sao |
|---|---|
| Bàn cờ lục giác bố trí đội hình | Một hệ thống riêng, đụng thẳng vào tổ đội 1 chính + 2 phụ đã chốt |
| Dàn nhân vật kiểu roster | Đối lập với "một con pet để gắn bó" |
| Bảng nâng cấp +5% lặp lại | Thang số kéo dài thời gian, không phải lựa chọn |
| Bảng màu tối | Sai với chủ quán mở app giữa hai ca |

---

# Phụ lục v18 — Âm thanh, ánh sáng, chuyển cảnh

## Em đã sai về con số 2,5 MB, và đây là lý do

Tuần trước em đề nghị 500 KB tiếng động, 800 KB nhạc nền, 1,2 MB nền vẽ tay. Khi bắt tay làm thì hai phần đầu **không cần file nào cả**, còn phần thứ ba **em không làm được**.

| Khoản | Đề xuất tuần trước | Thực tế |
|---|---|---|
| Tiếng động | 500 KB file | **6 KB mã tổng hợp** |
| Nhạc nền | 800 KB, hai vòng lặp | **5 KB, sinh theo thuật toán, không lặp** |
| Nền vẽ tay | 1,2 MB ảnh | **không giao được — cần hoạ sĩ** |
| Ánh sáng, hạt, chuyển cảnh | gần 0 | ~3 KB |
| **Tổng** | **2,5 MB** | **~14 KB** |

Về phần nền: em không vẽ được tranh bitmap. Thứ em làm được là SVG nhiều lớp, và nó đã làm ở v17. Muốn hơn nữa thì phải thuê người vẽ — em nói thẳng để anh không chờ một thứ em không giao được.

Về âm thanh: cách tổng hợp lúc chạy **tốt hơn** dùng file, không chỉ nhỏ hơn. Nhạc sinh theo thuật toán không bao giờ lặp, nên nghe cả buổi không chán — đúng thứ "chill" anh mô tả. Vòng lặp 30 giây thì tới lần thứ mười là thành tiếng ồn.

## Bộ máy âm thanh

Dựng trên Web Audio, không một file nào.

**Vang**: dựng đáp ứng xung bằng nhiễu tắt dần ngay lúc chạy — cho không gian mà không cần file impulse response.

**20 tiếng động**, mỗi cái là vài dao động và một lớp nhiễu lọc:

| Nhóm | Tiếng |
|---|---|
| Chăm sóc | cho ăn, chơi, tắm, rèn, ngủ |
| Giao dịch | chạm, chuyển trang, nhận xu, mở bảng, đóng bảng, báo lỗi |
| Trận đấu | trúng đòn, chí mạng, hồi máu, thắng, thua |
| Sự kiện | gõ vỏ trứng, nở trứng, lên cấp, tiến hoá, kỷ niệm mới |

`[đo]` Cả 20 tiếng chạy không lỗi. Tắt tiếng động rồi gọi vẫn không vỡ.

**Nhạc nền sinh theo thuật toán**, hai không khí đổi theo giờ thật:

| | Ban ngày (6h–20h) | Đêm khuya (20h–6h) |
|---|---|---|
| Gốc | La trưởng | Rê thứ |
| Thang | 7 bậc, ngũ cung mở rộng | 6 bậc, trầm hơn |
| Khoảng nghỉ giữa nốt | 1,6 – 3,4 giây | 2,8 – 5,6 giây |
| Nền trầm | 114 & 171 Hz | 75 & 112 Hz |
| Độ sáng bộ lọc | 1800 Hz | 900 Hz |

Mỗi nốt được chọn ngẫu nhiên trong thang ngũ cung — nghe lúc nào cũng thuận tai vì ngũ cung không có quãng nghịch. Nền trầm là hai bè lệch nhau 4 phần nghìn cho dày, kèm một bộ lọc dao động rất chậm (0,05 Hz) để âm sắc trôi nhẹ. 30% số nốt có thêm một nốt quãng năm đi sau 0,18 giây.

**Không có vòng lặp nào**, nên không có điểm lặp để nhận ra.

Có bảng bật tắt riêng cho tiếng động và nhạc, cùng thanh âm lượng, trong Cài đặt. Nhạc tự dừng khi rời app cho đỡ tốn pin, và tự mở lại khi quay vào.

**Mở khoá theo chạm**: iOS chỉ cho tạo âm sau một thao tác chạm thật, nên bộ máy đợi lần chạm đầu tiên rồi mới khởi động.

## Ánh sáng và hạt

Ba lớp, tất cả chỉ dùng `transform` và `opacity`:

- **Bụi bay** — 14 hạt trôi lên trong quán, tốc độ và độ mờ ngẫu nhiên từng hạt
- **Chùm sáng cửa sổ** — đổ xiên xuống sàn, chỉ hiện từ 6h đến 17h, thở rất chậm theo chu kỳ 7 giây
- **Quầng ấm quanh pet** — chỉ bật sau 17h và trước 7h, bám theo pet khi nó đi lại

`[đo]` Không keyframe nào chạm vào `filter`, `width`, `height`, `left`, `top` — đúng nguyên tắc đặt ra sau lần sửa khựng hình ở v9.

## Chuyển cảnh

Trang trượt lên 12px khi vào, các khung trong trang vào lệch nhau 50ms. Trước v18 là cắt thẳng.

## Hiệu năng

`[đo]` Đo 270 khung hình **trong lúc nhạc đang phát, bụi đang bay, chùm sáng đang thở**:

| Chỉ số | Kết quả |
|---|---|
| Khoảng cách khung hình, trung vị | 16,7 ms |
| Tệ nhất | 16,8 ms |
| Khung rớt (> 32 ms) | **0 / 270** |
| Nút Web Audio sống thường trực | 4 |

Web Audio chạy trên luồng âm thanh riêng nên không tranh chấp với luồng vẽ. Đây là lý do nữa để tổng hợp thay vì phát file.

## Kích thước

| | v17 | v18 |
|---|---|---|
| index.html | 511 KB | 527 KB |
| Bộ PWA | 557 KB | **573 KB** |
| Trần anh cho | 6 MB | 6 MB |
| Đang dùng | 9,3% | **9,3%** |

Còn dư 5,4 MB. Em cố ý không tiêu: qua khoảng 1,5–2 MB thì mỗi MB thêm vào đổi được rất ít cảm giác, mà kéo dài thời gian tải lần đầu.

Chỗ duy nhất em thấy đáng tiêu phần dư đó là **tranh nền do người vẽ** — và đó là việc của hoạ sĩ, không phải của em.

## Một lỗi trong bộ test

Bản vá test ở v17 đặt `S.npc.met=true` cho mọi kịch bản để bỏ qua màn AM-00 chào. Nhưng chính kịch bản t17 lại cần `met=false` để kiểm tra màn chào đó. Kịch bản tự vô hiệu hoá thứ nó đang kiểm. Đã tách riêng.

`[đo]` 19 bộ test chạy lại không lỗi.

---

# Phụ lục v19 — Sửa lỗi mất hiệu ứng, dọn giao diện

## 1. Lỗi mất hiệu ứng trên điện thoại và máy tính

Người dùng báo: iPad có cánh hoa rơi, bông tuyết, lá thu — nhưng điện thoại và máy tính mở HTML thì mất sạch, chuyển cảnh cũng giật.

**Thủ phạm là một dòng CSS em viết từ v1:**

```css
@media(prefers-reduced-motion:reduce){ *{animation:none!important; transition:none!important} }
```

Dòng này tắt **toàn bộ** chuyển động khi máy bật "Giảm chuyển động". iPad không bật, điện thoại và trình duyệt máy tính có bật — nên mất luôn cánh hoa rơi, bụi bay, pet thở, chùm sáng, và cả chuyển trang. Cảm giác "khựng" thực ra là **không có chuyển cảnh nào cả**: trang nhảy thẳng.

`[đo]` Giả lập hai chế độ xác nhận đúng: bật Giảm chuyển động thì cả năm hiệu ứng đều trả về `none`.

**Sửa đúng là giảm, không phải tắt.** Bỏ thứ làm chóng mặt, giữ thứ trang trí:

| Tắt khi bật Giảm chuyển động | Giữ nguyên |
|---|---|
| Chuyển trang trượt, khung trượt vào | Cánh hoa rơi, bông tuyết, lá thu |
| Xoay tít khi tiến hoá, rung vỏ trứng | Bụi bay trong quán |
| Trượt của bảng kéo lên, thẻ kỷ niệm | Pet thở, chùm sáng cửa sổ |
| Camera trượt ngang | Quầng ấm quanh pet |

`[đo]` Sau khi sửa: bật Giảm chuyển động thì bốn hiệu ứng trang trí vẫn chạy, chỉ chuyển trang tắt.

Thêm **công tắc riêng trong Cài đặt** để người dùng tự bật tắt hiệu ứng trang trí, độc lập với cài đặt hệ điều hành.

## 2. Hội thoại và thẻ ra giữa màn hình

Trước: hội thoại nằm sát đáy, bảng kéo lên bám mép dưới với hai góc trên bo tròn.

Nay cả hai **căn giữa màn hình**, bo tròn bốn góc, có đổ bóng. `[đo]` Tâm bảng lệch tâm màn hình 0px.

Áp cho toàn bộ: thẻ cốt truyện, thẻ công thức, thẻ vận hành, bảng chế biến, bảng gieo hạt, bảng boss.

## 3. Trang Nhà gọn hơn

**Ba dòng chỉ số có nhãn** thay bằng **ba đồng hồ nhỏ nằm ngang** — số lớn, thanh mảnh, đổi màu theo mức. Cắt được ba dòng chữ mà vẫn đọc nhanh hơn.

**Sân khấu nở ra khi chăm sóc.** Chạm một trong sáu nút thì khay hoá đơn trượt xuống và sân khấu cao từ 245px lên **388px** — thấy trọn hoạt cảnh và bối cảnh. Xong thì tự thu lại.

`[đo]` Xác nhận: khay ẩn hẳn khi đang chăm sóc, sân khấu trở về đúng chiều cao cũ sau khi xong, và tự thu khi đổi trang.

## 4. Cây kỹ năng thành sơ đồ

Trước là lưới 42 ô phẳng, không đường nối, phải cuộn hết mới biết mình đang mang gì.

Nay:

- **Hàng ô đang mang đặt trên cùng** — ba hoặc bốn ô, thấy ngay loadout, chạm để gỡ
- **Bảy nhánh gập lại được** — thân chung, nhánh của loài mình, năm nhánh loài khác để tra cứu
- Mỗi đầu nhánh hiện **số kỹ năng đã học trên tổng**
- Trong nhánh, kỹ năng **xếp theo tầng giai đoạn**, nối bằng đường dọc có nhánh ngang
- Mặc định mở sẵn hai nhánh có ích: thân chung và nhánh của pet
- **Bảng khắc chế giữa các loài** chuyển xuống ngay dưới cây

`[đo]` 7 nhánh, 15 tầng có đường nối, 4 ô loadout.

## 5. Hai mươi kiểu dáng trang bị

Trước: cùng một hình, chỉ đổi màu và tên.

Nay mỗi ô năm kiểu dáng riêng:

| Ô | Nhựa | Giấy | Thuỷ tinh | Sứ | Inox |
|---|---|---|---|---|---|
| Vũ khí | ống hút có khớp gập | ống hút sọc xoắn | thìa bầu tròn cán mảnh | thìa bầu sâu cán dày | thìa dài có khía cán |
| Giáp | ly thuôn có nắp và ống hút | ly có vành cuộn và đai | ly thành thẳng đế dày | tách có quai | ly giữ nhiệt thắt eo |
| Khiên | nắp vòm | nắp phẳng có tai | nắp phẳng có núm | đĩa lót có vành | nắp vặn có khía |
| Choàng | túi nilon quai tròn | túi kraft gấp mép | túi lưới đựng bình | túi vải dày quai cứng | túi canvas quai da |

`[đo]` 20 món cho ra 20 hình khác nhau, không món nào trùng.

Lớp mặc trên người cũng đổi dáng theo nhóm: đồ dùng một lần thuôn, thuỷ tinh trong có vệt sáng, đồ bền dày có quai.

## Một lỗi tự gây ra khi build

Gộp bảng khắc chế vào cây kỹ năng thì **có hai bảng cùng lúc** — một cái sẵn có trong tab Đấu nhanh, một cái mới thêm. Bộ test bắt được ngay: "12 mũi tên, 12 đỉnh" thay vì 6. Đã bỏ bản trùng và chuyển bản gốc xuống dưới cây.

## Kích thước

| | v18 | v19 |
|---|---|---|
| index.html | 527 KB | 538 KB |
| Bộ PWA | 573 KB | **584 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 20 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung.

## Còn treo cho v20

Mở rộng vùng nguyên liệu: thẻ tri thức rơi theo vùng, pet đặc trưng vùng, boss vùng nối với tháp tầng 60–110, bản đồ top-down có nút và pet di chuyển giữa các nút. Cốt truyện "vùng nguyên liệu mất bản sắc khi nguyên liệu bị biến thành đồ uống công nghiệp".

Và việc quan trọng nhất: **công cụ vận hành chạy trên nền HTML**, nên nhúng iframe được — cầu nối `postMessage` dựng từ v10 nay có thể nối thật.

---

# Phụ lục v20 — Vùng nguyên liệu có chiều sâu

Cốt truyện của đợt này: **các vùng nguyên liệu đang mất bản sắc khi thứ chúng làm ra bị rút gọn thành một dòng trong bảng thành phần.**

## 1. Cấp thân thiết với từng vùng

Trước v20, bảy vùng đều phẳng: đi chuyến nào cũng như chuyến nào.

Nay mỗi vùng có **năm cấp**, tính theo số chuyến tích luỹ:

| Cấp | Cần | Tên |
|---|---|---|
| 1 | 2 chuyến | Người lạ |
| 2 | 5 chuyến | Ghé qua |
| 3 | 9 chuyến | Quen mặt |
| 4 | 14 chuyến | Được tin |
| 5 | 20 chuyến | Người nhà |

Cấp mở ra ba thứ: **nút mới trên bản đồ**, **thẻ tri thức**, và **cơ hội gặp pet hoang**.

## 2. Mười tám thẻ tri thức

Ba thẻ mỗi vùng, mở ở cấp 2, 3 và 5. Đây là kiến thức nghề thật, không phải lore:

| Vùng | Ba thẻ |
|---|---|
| Cao nguyên đỏ | Robusta khác arabica ở đâu · Vì sao đất bazan quan trọng · Phơi tự nhiên và chế biến ướt |
| Đồi sương | Độ cao và độ chua · Sương mù làm gì với cây · Hạt mới rang chưa phải hạt ngon nhất |
| Đồi trà | Một tôm hai lá · Trà xanh và ô long từ cùng một cây · Nhiệt độ nước quyết định vị chát |
| Miệt vườn | Ca cao phải lên men mới thành ca cao · Dừa xiêm và dừa ta · Nước cốt dừa tách lớp |
| Vườn cam | Vỏ cam chứa vị đắng · Cam vàng vỏ chưa chắc ngọt hơn · Độ Brix và cân bằng chua ngọt |
| Thung lũng lạnh | Dâu mất mùi rất nhanh · Bạc hà phải vò chứ không nghiền · Nhà kính và mùa vụ giả |

Xem lại ở tab **Khác → Tri thức**. Tổng 3 KB chữ.

## 3. Sáu pet hoang, mỗi vùng một loài

| Vùng | Pet | Nguyên mẫu | Mạnh nhất | Dạng trưởng thành |
|---|---|---|---|---|
| Cao nguyên đỏ | **Rôbu** | Hạt robusta già | ATK 48 | Rôbu Cổ Thụ |
| Đồi sương | **Sương** | Quả arabica vùng cao | INT 46 | Sương Mù Sớm |
| Đồi trà | **Shan** | Búp trà shan tuyết | INT 48 | Shan Đại Thụ |
| Miệt vườn | **Dừa** | Trái dừa xiêm | DEF 52 | Dừa Lão |
| Vườn cam | **Mía** | Khúc mía tím | ATK 54 | Mía Lau |
| Thung lũng lạnh | **Dâu** | Dâu tây Đà Lạt | LUCK 44 | Dâu Rừng |

Chúng **nằm ngoài bảng sáu loài gốc**, nên trứng không bao giờ nở ra — chỉ gặp ngoài vùng. Tỉ lệ 6% ở cấp 3, lên 30% ở cấp 5. `[đo]` 400 chuyến ở cấp 5 cho 112 lần gặp, đúng thiết kế.

Mỗi con có **một dạng trưởng thành duy nhất**, không chia bốn nhánh như loài gốc — chúng là loài hoang, không nuôi từ nhỏ.

`[đo]` Tổng chỉ số đều đúng **280** (loài gốc là 265). Cao hơn một chút vì phải săn mới có, nhưng bằng nhau để không con nào mạnh tuyệt đối. Bản đầu em để lệch 272–292, đã cân lại.

## 4. Sáu boss vùng

Mỗi vùng có một kẻ đang rút gọn nó. Xuất hiện khi vùng đạt cấp 5.

| Vùng | Boss | Lời nó nói | Khắc chế |
|---|---|---|---|
| Cao nguyên đỏ | **Bột Hoà Tan** | *"Ba mươi giây, không cần máy, không cần ai biết pha."* | Đắng |
| Đồi sương | **Nhãn Vùng Trồng** | *"Tôi in chữ Cầu Đất lên túi. Ai đi kiểm tra?"* | Chua |
| Đồi trà | **Trà Đóng Chai** | *"Không ai chờ nước nguội xuống bảy mươi lăm độ cả."* | Chát |
| Miệt vườn | **Hương Dừa Tổng Hợp** | *"Mùi giống hệt. Cậu phân biệt được không?"* | Thanh |
| Vườn cam | **Cốt Cam Cô Đặc** | *"Một lít của tôi thành bảy lít của cậu. Ai chịu thiệt?"* | Cay |
| Thung lũng lạnh | **Siro Dâu Đỏ** | *"Dâu thật đâu có đỏ đều như thế này."* | Ngọt |

Sáu boss dùng **hết sáu nhóm vị**. Bốn con có gắn sẵn chặng tháp 6–9 cho phần 2.

Trận mở bằng hội thoại ba lượt: boss nói, pet đáp theo tính cách, AM-00 chốt. Hạ lần đầu được 600 xu, 3 hạt vùng và mở nốt thẻ tri thức còn lại.

## 5. Bản đồ có nút, nhìn từ trên xuống

Năm nút mỗi vùng, mở dần theo cấp, nối bằng đường đứt nét. Khi chuyến đang chạy, **pet đi từ nút này sang nút kia theo tiến độ thật** — 30 phút chia cho bốn chặng.

Nút đã qua chuyển xanh ngọc có quầng, nút chưa mở hiện "? ? ?".

## Ba lần cân bằng — và một bài học

Đây là phần tốn công nhất của v20, và em sai hai lần trước khi đúng.

**Lần một: nhân đôi độ khó.** Đối thủ vừa được tăng 25% sức mạnh nền, vừa nhân thêm hệ số boss 1,18 lần nữa. `[đo]` Kết quả: thắng **0–2%** với pet Lv30 tiến hoá.

**Lần hai: cân theo cơ chế, sai chỗ.** Sau khi bỏ nhân đôi, sáu boss vẫn trải từ **0% tới 100%**. Em chỉnh cơ chế và hệ số — vẫn lệch.

**Tìm ra nguyên nhân thật:** không phải cơ chế, không phải hệ số, mà là **bộ kỹ năng**. `[đo]` Cùng một boss, đổi sang kỹ năng cơ bản thì người chơi thắng **100%**; giữ bộ bốn kỹ năng của loài thì thắng **2%**.

Đo tiếp từng kỹ năng riêng lẻ: mỗi cái cho 31–100%. Nhưng **bốn kỹ năng mạnh đi cùng nhau thì cộng dồn thành một bức tường**, không phải cộng tuyến tính.

Cách sửa: mỗi boss dùng **một kỹ năng đặc trưng cộng hai kỹ năng thường**, rồi để máy dò hệ số cho từng con bằng tìm kiếm nhị phân bảy vòng.

`[đo]` Kết quả sau khi dò, 120 trận mỗi ô:

| Cấu hình | Dải thắng sáu boss |
|---|---|
| Nuôi kỹ, độ hiếm Thường, không trang bị | **11 – 27%** |
| Nuôi kỹ Thường, **bộ inox đủ 4 món** | **43 – 62%** |
| Nuôi kỹ **Hiếm**, inox + ly đúng nhóm vị | **85 – 98%** |

Đây là hình dạng đúng: không trang bị thì không qua được, đủ bộ thì ngang ngửa, nuôi kỹ có chuẩn bị thì thắng chắc. Và **sáu boss nằm trong dải chặt**, không con nào dễ hay khó bất thường.

**Bài học ghi lại:** khi cân boss, đừng chỉnh hệ số trước. Đo xem **kỹ năng** đóng góp bao nhiêu — trong engine này nó chi phối mạnh hơn cả hệ số sức mạnh lẫn cơ chế đặc biệt.

## Một lỗi nhỏ về bố cục

Nút trên bản đồ đặt ở nửa dưới nên **đè lên tên vùng**. Đã nâng lên nửa trên, cho nhãn nền tối bo tròn, và tăng chiều cao bản đồ từ 118px lên 132px.

## Kích thước

| | v19 | v20 |
|---|---|---|
| index.html | 538 KB | 562 KB |
| Bộ PWA | 584 KB | **608 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 21 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 330 khung.

## Còn treo

Nối thật cầu nối `postMessage` với công cụ vận hành — công cụ chạy trên nền HTML nên nhúng iframe được. Đây là việc duy nhất còn lại có thể đổi bản chất của cả trò chơi.

---

# Phụ lục v21 — Sáu chỗ khó chịu khi chơi thật

Đợt này không thêm hệ thống nào. Toàn bộ là sửa những chỗ người dùng gặp phải khi chơi v20.

## 1. Nhạc chói tai và đơn điệu

Chẩn đoán đúng hai nguyên nhân:

- **Đơn điệu:** bản v18 chọn nốt ngẫu nhiên trên một nền trầm **đứng yên**. Không có vòng hoà thanh nào nên nghe mãi không đi đâu cả.
- **Chói:** hai bè nền lệch nhau 4 phần nghìn tạo **nhịp đập**, cộng bộ lọc để sáng tới 1800 Hz.

Viết lại hẳn:

| | v18 | v21 |
|---|---|---|
| Cấu trúc | nốt ngẫu nhiên, nền đứng yên | **vòng bốn hợp âm** chuyển mỗi 11 giây (ngày) / 15 giây (đêm) |
| Chọn nốt | ngẫu nhiên trong thang | **chỉ lấy nốt nằm trong hợp âm đang chạy** |
| Nền trầm | 2 bè lệch cent → đập | **3 nốt của hợp âm**, không lệch cent, có rung nhẹ 0,13 Hz |
| Tiếng vào | 0,35 giây | **0,55 giây**, kèm trượt nhẹ lên đúng cao độ |
| Tần số cao | để sáng 1800 Hz | **cắt còn 900 Hz** (đêm 620), thêm hạ kệ −14 dB từ 2200 Hz |
| Chất liệu | không có | **nhiễu nền kiểu đĩa than**, rất nhỏ, có tiếng lách tách thưa |

Vòng hoà thanh ban ngày: **Am7 – Dm7 – Fmaj7 – Cmaj7**. Ban đêm trầm hơn một quãng và chậm hơn.

`[đo]` Xác nhận: vòng 4 hợp âm, hợp âm tự chuyển, nốt chỉ lấy trong hợp âm, có nền trầm, có nhiễu đĩa, có bộ lọc chung.

## 2. Bấm kỹ năng không hiện mô tả

Đây là lỗi thiết kế của bản v19: **bấm vào ô là trang bị luôn**, không có chỗ nào đọc được kỹ năng làm gì.

Nay tách hẳn: **bấm để đọc**, trong bảng mô tả mới có nút trang bị.

Bảng hiện: tên và biểu tượng, loài và giai đoạn, mô tả, rồi bốn dòng chỉ số viết lại cho dễ hiểu.

Chỗ này em cũng sửa một lỗi trình bày: trường `pow` là **hệ số nhân 0–2**, không phải số sát thương. Hiện thẳng ra thành "Sức mạnh: 1" thì vô nghĩa. Nay đổi thành **"Sát thương: vừa · ×1.0"**, và tốn sức thành **"8/30 · rẻ"**.

Kỹ năng của loài khác chỉ đọc được, không có nút trang bị.

## 3. Quái trên tháp trông giống pet

Xác nhận đúng: quái thường vẽ bằng `renderPet` **không bật cờ industrial, không có trang bị** — trong khi cờ đó đã có từ v12.

Nay quái thường cũng là hàng của phe Công Nghiệp, và **có trang bị theo độ cao**:

| Tầng | Số món | Bậc chất liệu |
|---|---|---|
| dưới 15 | 1 | nhựa, giấy |
| 15–34 | 2 | giấy, thuỷ tinh, nhựa |
| từ 35 | 3 | thuỷ tinh, sứ, inox |

`[đo]` Tầng 3 một món, tầng 18 hai món, tầng 38 và 55 ba món, tất cả đều bật cờ industrial.

## 4. Trồng cây lâu

Trung bình **6,8 giờ**, ca cao 12 giờ — quá dài với người mở app 2–3 lần mỗi ngày.

Rút còn trung bình **3,4 giờ**: bạc hà, chanh, cam 2 giờ · trà xanh, dâu, gừng 3 giờ · robusta, ô long 4 giờ · arabica 5 giờ · ca cao 6 giờ.

Giờ một ngày làm việc gieo được hai lứa thay vì một.

## 5. Thả pet

Chuồng đầy dần mà không có cách dọn. Nay mỗi thẻ pet có nút **Thả** ở góc.

- Nhận lại **60% Pet Power quy ra xu**, tối thiểu 20
- Có hỏi xác nhận, nói rõ không lấy lại được
- **Pet đang ở tổ đội thì bị chặn** — phải rút ra trước

`[đo]` Xác nhận cả ba.

## 6. Nhiều chữ quá

`[đo]` Đo được **158 khối mô tả, 12.246 ký tự**. Không khối nào quá dài — vấn đề là số lượng.

Rút gọn 18 khối dài nhất, xoá hẳn 3 khối giải thích thứ đã rõ. Còn **10.970 ký tự**, giảm **10%**.

Nguyên tắc áp dụng: bỏ câu giải thích cơ chế đã hiển thị bằng hình, bỏ câu nhắc lại thứ vừa nói ở trên, giữ lại câu nói điều người chơi không tự đoán ra.

## 7. Trang tra cứu (bổ sung theo yêu cầu)

Trước v21 không có chỗ nào giải thích pet lớn lên thế nào. Nay Cài đặt có nút **Pet lớn lên thế nào**, mở ra năm mục:

- **Bốn giai đoạn** và mốc ngày thật — pet lớn theo ngày, không theo số lần chăm
- **Bốn nhánh tiến hoá** với điều kiện đầy đủ của từng nhánh
- **Lai tạo**: điều kiện, kết quả, tỉ lệ đột biến 5%
- **Sáu bậc độ hiếm** và hệ số tiềm năng
- **Thả pet**: được lại bao nhiêu, khi nào bị chặn

## Kích thước

| | v20 | v21 |
|---|---|---|
| index.html | 562 KB | 568 KB |
| Bộ PWA | 608 KB | **614 KB** |

`[đo]` 22 bộ test chạy lại không lỗi. Hiệu năng đo **trong lúc nhạc đang phát**: 270 khung hình, trung vị 16,7 ms, 0 khung rớt.

## Một lỗi trong bộ test

Kịch bản t18 còn tra `MUSIC.day.scale` — trường này đã đổi thành `prog` khi viết lại nhạc. Đã cập nhật.

## Còn treo

**v22** — hiệu ứng kỹ năng theo tên gọi: 8–10 khuôn dùng chung gán cho 42 kỹ năng, thay vì vẽ 42 hiệu ứng riêng.

**v23** — tháp: nối vùng nguyên liệu với chặng, chỉ báo Khắc chế/Bình thường/Bất lợi, tầng đặc biệt, thử thách chặng, gợi ý build trước boss.

Hai mục em đề nghị **bỏ hẳn**: thêm cơ chế boss phức tạp hơn (đi ngược bài học v20 — kỹ năng chi phối mạnh hơn cơ chế), và tầng có thuộc tính ngẫu nhiên (làm hỏng vòng lặp chuẩn bị ly đúng nhóm vị).

---

# Phụ lục v22 — Ghép trang bị và đồ thời trang

Gộp hai đợt theo yêu cầu.

## Con số làm cơ sở

`[đo]` Trang bị rơi **~1,6 món mỗi ngày**, tức **khoảng 47 món sau 30 ngày**, trong khi chỉ có 20 loại. Sau một tháng người chơi ôm một đống trùng lặp mà **không có cách nào tiêu**. Ghép và bán đều đúng chỗ.

## 1. Bảng mô tả trang bị

Giống cách làm với kỹ năng ở v21: bấm vào thẻ là **đọc**, các nút nằm trong bảng.

Bảng hiện: hình phóng to, mức buff hiện tại (tách rõ phần cộng nhờ ghép), chất liệu, độ bền, Rác mỗi lần dùng, số đang có, cấp ghép, thẻ giá đời thật, rồi ba nút Mang / Ghép / Bán.

## 2. Ghép trang bị — trần khác nhau theo bậc

Đây là chỗ em phải nói ngược với đề xuất ban đầu.

Cả hệ trang bị dựng trên nguyên tắc **không bậc nào mạnh toàn diện**. Nhựa và giấy **mua được bằng xu — nguồn vô hạn**. Nếu cho ghép tới +10 thì chỉ cần cày xu là có thìa nhựa +10, trong khi inox phải chờ rơi. Nhựa lại thành mạnh tuyệt đối và đường cong ba tuần của v13 sụp.

| Bậc | Trần ghép | Lý do |
|---|---|---|
| Nhựa, Giấy | **+3** | Đồ dùng một lần, ghép mấy cũng vẫn là đồ bỏ đi |
| Thuỷ tinh, Sứ | **+7** | |
| Inox | **+10** | Thứ duy nhất đáng gắn bó lâu dài |

- Chi phí tăng dần: +1 cần 3 món, +2 cần 4, … +10 cần 12. `[đo]` Tổng **65 món** cùng loại để lên +10.
- Mỗi cấp cộng **4% mức buff gốc của ô**. `[đo]` Thìa inox: ATK +10,8% ở +0, lên **+15,1% ở +10**.
- **Nhựa càng ghép càng để lại nhiều Rác**: `[đo]` 2 Rác mỗi trận ở +0, **3,5 ở +3**.
- Luôn giữ lại ít nhất một món để mang.

## 3. Bán trang bị

Giá theo bậc chất liệu, cộng 55% mỗi cấp ghép. Có nút bán một món và bán hết phần dư. `[đo]` Món đang mang luôn được giữ lại.

## 4. Đồ thời trang — 24 món, 4 ô

Không dính gì tới chỉ số. **Mặc ở quán, cởi ra khi vào trận.**

| Ô | Sáu món |
|---|---|
| Mũ nón | Mũ nồi · Mũ lưỡi trai · Mũ bếp · Nón lá · Mũ Noel · Khăn đóng |
| Áo | Tạp dề · Áo phông quán · Gi lê · Sơ mi kẻ · Áo dài · Áo mùa hoa |
| Cầm tay | Chổi · Kẹp hồ sơ · Bình tưới · Đèn lồng · Quạt nan · Ô giấy |
| Khoác | Khăn quàng · Áo len mỏng · Áo mưa · Khăn lá thu · Áo choàng quán · Khăn vắt vai |

18 món mua bằng xu, **6 món lễ hội mở khi đã có khung lễ tương ứng** — Noel, Tết, hoa anh đào, Trung Thu, thu lá vàng.

Phần lớn là đồ gắn với công việc thật: tạp dề, khăn vắt vai, kẹp hồ sơ kiểm kho, bình tưới ra vườn sau.

## 5. Nhà mặc thời trang, trận mang trang bị

`[đo]` Xác nhận tách hẳn: ở Nhà **4 lớp thời trang, 0 lớp trang bị**; trong trận **có lớp trang bị, 0 lớp thời trang**.

Vừa làm trang Nhà bớt rối, vừa cho đồ thời trang một lý do tồn tại thật.

## 6. Ba việc nhỏ

- Bỏ dòng gợi ý bong bóng nổi ở trang Nhà
- Lịch sử khám phá từ 9 hàng dài thành **6 viên gọn một dòng**
- Thêm tab **Phòng thay đồ** trong Đấu

## Hai lỗi sửa trong lúc dựng

**1. Mọi mũ vẽ chung một hình.** Bản đầu `fashLayers` chỉ có một dáng cho mỗi ô — đúng lỗi mà v19 đã sửa cho trang bị, em lại lặp lại. Nay mỗi món một dáng: mũ bếp cao, nón lá hình chóp rộng, mũ Noel có chóp và viền trắng, mũ lưỡi trai có vành. Riêng ô Cầm tay **dùng lại chính hình của món** phóng to, nên sáu món cho sáu hình. `[đo]` 6 mũ ra 6 hình, 6 món cầm tay ra 6 hình.

**2. Tạp dề che mất miệng pet.** Khuôn mặt nằm quanh y = 6–20, mà áo bắt đầu từ y = 20. Hạ xuống y = 34, yếm ngực xuống y = 26.

## Kích thước

| | v21 | v22 |
|---|---|---|
| index.html | 568 KB | 587 KB |
| Bộ PWA | 614 KB | **633 KB** |

`[đo]` 23 bộ test chạy lại không lỗi. Hiệu năng đo trong lúc nhạc đang phát: 0 khung rớt trên 270 khung.

## Còn treo

**v23** — kỳ ngộ và hộp bí ẩn: nhiệm vụ ẩn khó, không liên quan vận hành, thưởng là hộp mở ra ngẫu nhiên gồm trứng vàng, trang bị vàng, đồ thời trang hiếm.

**v24** — hiệu ứng kỹ năng theo tên gọi: 8–10 khuôn dùng chung gán cho 42 kỹ năng.

---

# Phụ lục v23 — Kỳ ngộ, hộp bí ẩn, và hiệu ứng kỹ năng

Gộp hai đợt theo yêu cầu.

## 1. Kỳ ngộ — mười hai nhiệm vụ ẩn

Không liên quan tới vận hành. Không ai giao. Chúng tự hoàn thành khi người chơi đi đủ xa theo một hướng nào đó.

| Kỳ ngộ | Mốc | Hộp |
|---|---|---|
| Ba mươi ngày một con | nuôi cùng một pet 30 ngày | Gỗ |
| Trọn một bộ | mang đủ 4 món cùng bậc | Gỗ |
| Đi hết sáu vùng | ghé qua mọi vùng nguyên liệu | Bạc |
| Không rời nửa bước | Gắn bó lên 100 | Bạc |
| Người đọc kỹ | mở hết 18 thẻ tri thức | Bạc |
| Sổ tay đầy | pha thử hết 24 công thức | Bạc |
| Thợ mài | ghép một món lên +5 | Bạc |
| Người rừng | bắt được 3 loài hoang khác nhau | Bạc |
| Nửa đường | leo tới tầng 50 | Vàng |
| Giữ lấy bản sắc | chặn kẻ rút gọn ở 4 vùng | Vàng |
| Đời thứ năm | lai tạo tới đời 5 | Vàng |
| Tủ đồ đầy | sở hữu 12 món thời trang | Vàng |

**Chỉ lộ gợi ý khi đã đi được một phần ba đường.** Trước đó chỉ thấy `? ? ?`. Và bảng chỉ hiện tối đa hai dòng ẩn cộng một dòng "còn N điều chưa gặp" — bản đầu bày cả mười hai dòng `? ? ?` trông rất rối.

Kiểm tra chạy khi mở app và sau mỗi hành động chăm sóc.

## 2. Hộp bí ẩn — ba hạng

| Hộp | Số món | Nổi bật |
|---|---|---|
| **Gỗ** | 3 | xu, hạt, nguyên liệu, vé |
| **Bạc** | 4 | thêm trang bị bậc sứ/inox và trứng cổ |
| **Vàng** | 5 | trang bị inox 24%, trứng vàng 18%, thời trang 10%, Lõi Automa 4% |

`[đo]` Phân bố hộp vàng qua 600 lượt: trang bị 25%, trứng 19%, vé 13%, xu 12%, hạt 11%, thời trang 10%, lượt đi 8%, lõi 3% — khớp thiết kế.

**Về "trang bị vàng":** em **không thêm bậc chất liệu thứ sáu**. Hộp vàng cho trang bị **bậc inox** — bậc tốt nhất hiện có. Thêm một bậc trên inox sẽ phá cân bằng năm bậc của v13 và làm vô nghĩa đường cong ba tuần.

Mở hộp có màn riêng: hộp lắc lư, chạm thì bung ra kèm pháo giấy, rồi tới banner liệt kê phần thưởng.

## 3. Hiệu ứng kỹ năng theo tên gọi

Đây là mục anh nêu và nó đúng là thứ làm trận đấu khác hẳn.

Cách làm: **mười khuôn dùng chung**, gán màu và số hạt riêng cho từng kỹ năng — thay vì vẽ 42 hiệu ứng riêng.

| Khuôn | Hình dạng | Ví dụ kỹ năng |
|---|---|---|
| `leaf` | lá xoay bay tán ra | Cắt lá, Diệp lục |
| `slash` | ba vệt chém chéo | Cắn, Hai shot, Chém chanh |
| `ring` | ba vòng khí nở ra | Toả hương, Thiền, Tường bọt sữa, Giáp băng |
| `burst` | hạt nổ toả tròn | Húc, Bắn hạt, Rang, Sông băng |
| `shard` | mảnh nhọn văng ra | Mảnh băng, Đóng băng, Ném truffle |
| `splash` | giọt bắn theo hướng đánh | Tạt sữa, Phun axit, Vị chát |
| `bubble` | bọt nổi lên | Tường bọt |
| `spiral` | hạt xoay theo vòng xoáy | Bước nhanh, Cơn giận, Nở tối |
| `beam` | tia quét ngang | Espresso, Sốc chua |
| `spark` | đốm sáng bay lên | Tập trung, Nghỉ, Bùng caffeine |

Kỹ năng loại tăng sức hoặc hồi máu thì hiệu ứng nổ **trên chính mình**, loại tấn công thì nổ **ở phía đối thủ**.

`[đo]` 42/42 kỹ năng đã gán, dùng đúng 10 khuôn. Số hạt: lá 9, mảnh băng 8–10, bọt 13, giọt 12, đốm sáng 10. Lớp hiệu ứng tự dọn sau 1,1 giây — `[đo]` xác nhận về 0.

Tất cả chỉ dùng `transform` và `opacity`. `[đo]` Hiệu năng không đổi: 0 khung rớt trên 270 khung khi nhạc đang phát.

## Kích thước

| | v22 | v23 |
|---|---|---|
| index.html | 587 KB | 606 KB |
| Bộ PWA | 633 KB | **652 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 24 bộ test chạy lại không lỗi.

## Hai lỗi nhỏ sửa trong lúc dựng

1. **Mười hai dòng `? ? ?`** bày hết cùng lúc trong tab Việc. Đã gom còn hai dòng cộng một dòng đếm.
2. **Phần thưởng trong banner không hiện** — em dùng sai tên lớp khi kiểm (`.rw` thay vì `.rw1`). Lỗi ở kịch bản test, không phải ở game.

---

# v23.1 — Ba lỗi hiển thị, cùng một nguyên nhân gốc

Người dùng báo ba chỗ hỏng sau khi chơi v23: tab **Đấu trống trơn**, **khung lễ vỡ layout**, **kỳ ngộ chữ tối trên nền tối**. Cả ba đều truy về **trùng tên class CSS** — đúng loại lỗi đã xảy ra ở v17 với `.bf`.

## Lỗi 1 — tab Đấu trống trơn

Nguyên nhân: em đặt tên `dim` cho nhãn "chưa sở hữu" của thẻ thời trang. Nhưng `.dim` đã tồn tại từ trước như **một lớp phủ toàn màn hình**:

```css
.dim { position:absolute; inset:0; background:#06140f; opacity:0 }
```

Kết quả: mỗi món thời trang chưa mua biến thành một tấm che đen phủ kín màn. Mười tám món chưa mua chồng lên nhau che sạch tab Đấu.

`[đo]` Thẻ thời trang cao **1180px** — đúng bằng chiều cao màn hình — trong khi nội dung bên trong chỉ 66px. Sau khi đổi tên thành `gdim`: tab Thời trang từ 553px lên **1409px** nội dung thật.

## Lỗi 2 — khung lễ vỡ layout

Nguyên nhân: hạt hiệu ứng "vòng khí" của v24 đặt tên `.fr`, trùng với thẻ khung lễ từ v6. Quy tắc sau đè lên:

```css
.fr { width:30px; height:30px; border-radius:50% }   /* hạt hiệu ứng */
```

`[đo]` Góc trang trí khung lễ rộng **11,5px** thay vì 152px — vì thẻ cha bị ép còn 30px.

Sửa: đổi **cả mười lớp hiệu ứng** sang tiền tố `pf` — `pfleaf`, `pfslash`, `pfring`, `pfburst`, `pfshard`, `pfsplash`, `pfbub`, `pfspiral`, `pfbeam`, `pfspark`. `[đo]` Sau khi đổi, góc khung lễ về đúng 152px.

Rà lại thấy `.fl` cũng đụng `.tower .fl`, đã đổi luôn.

## Lỗi 3 — kỳ ngộ chữ tối trên nền tối

Nguyên nhân khác: em chèn `${encHTML()}` bằng biểu thức chính quy và nó rơi **sau thẻ đóng của khung trắng**, nên toàn bộ khu kỳ ngộ nằm trên nền tối với màu chữ dành cho nền sáng.

Nhân tiện làm luôn theo yêu cầu: **kỳ ngộ thành tab con thứ tư**, nằm cạnh Hằng ngày / Hằng tuần / Hằng tháng, có đếm số hộp chưa mở ngay trên nhãn tab.

`[đo]` Xác nhận: 4 tab, khu kỳ ngộ nằm trong khung trắng.

## Thêm một bước kiểm tự động

Ba lỗi trùng tên trong ba bản khác nhau là đủ để làm hẳn một bước kiểm. Thêm `audit.py` chạy cùng bộ test:

- Liệt kê mọi class **khai báo ở mức gốc nhiều hơn một lần** — dấu hiệu hai nơi dùng cùng tên cho hai việc khác nhau
- Phát hiện **class là lớp phủ toàn màn** (`position:absolute` + `inset`) **bị dùng làm nhãn phụ** trong chuỗi `class="..."` nhiều tên — đây chính là hình dạng của lỗi `.dim`
- Trả mã thoát khác 0 khi phát hiện, để dừng đóng gói

`[đo]` Chạy trên bản v23.1: không còn lớp phủ nào bị dùng nhầm.

## Bài học ghi lại

Ba lần trùng tên class đều có chung hình dạng: **một tên ngắn, đặt ở mức gốc, dùng cho hai việc khác nhau ở hai bản cách nhau nhiều tháng.** `.bf` (đấu sĩ và dòng hiệu ứng công thức), `.fr` (thẻ khung lễ và hạt hiệu ứng), `.dim` (lớp phủ và nhãn chưa sở hữu).

Quy tắc từ nay: **mọi class mới phải có tiền tố theo module** — `pf` cho hiệu ứng, `g` cho trang bị, `enc` cho kỳ ngộ. Tên một hoặc hai chữ cái ở mức gốc là cấm.

`[đo]` 24 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

---

# Phụ lục v24 — Cốt truyện tầng 51–110

## Đọc báo cáo sử dụng trước

Sáu ngày, 13 phiên, 8% vào rồi ra. Ba điều đáng nói:

**1. Bảng so sánh vẫn rỗng.** Dòng "ngày KHÔNG chạm mini game: 0.00" không có nghĩa là những ngày đó làm 0 nhiệm vụ — mà là **không có ngày nào như vậy**. Sáu ngày đều chạm game, nên chưa có nhóm đối chứng. Câu hỏi gốc của cả dự án vẫn chưa trả lời được.

**2. Ngủ chiếm 185/258 lượt chăm sóc — 72%.** Rèn 9 lần, Chơi 8 lần. Sáu nút nhưng thực tế người chơi chỉ dùng một. Đây là vấn đề cân bằng thật, ghi lại để xử ở bản sau.

**3. Khám phá 7 lần** — nguồn trứng miễn phí duy nhất, gần như không ai dùng.

## Tháp mở rộng lên 110 tầng

| Chặng | Tầng | Tên | Boss |
|---|---|---|---|
| 6 | 51–60 | Phòng Sấy Hoà Tan | **Bột Hoà Tan** |
| 7 | 61–70 | Xưởng In Nhãn | **Nhãn Vùng Trồng** |
| 8 | 71–80 | Kệ Trà Đóng Chai | **Trà Đóng Chai** |
| 9 | 81–90 | Phòng Hương Liệu | **Hương Dừa Tổng Hợp** |
| 10 | 91–100 | Bồn Cô Đặc | **Cốt Cam Cô Đặc** |
| 11 | 101–110 | Nguồn | **Bản Chuẩn** |

Năm boss chặng 6–10 **chính là boss vùng của v20** — cùng một đối tượng, gặp được ở cả vùng nguyên liệu lẫn trên tháp. Thế giới liền một mạch thay vì hai danh sách rời nhau.

Thêm **sáu mini boss** ở tầng 55, 65, 75, 85, 95, 105: Gói Ba Trong Một, Tem Truy Xuất, Chai Nửa Lít, Lọ Tinh Dầu, Bình Cốt Đặc, và **Bản Nháp** — phiên bản trước của Bản Chuẩn, "chỉ là chưa đủ chắc chắn về chính mình".

## Một giới hạn có sẵn từ lâu, nay mới lộ ra

`[đo]` Khi mở rộng tháp, phát hiện **`tunePet` không dựng nổi đối thủ mạnh quá ~550 PP**:

| Tầng | Đích đường cong cũ | Dựng ra được | Đạt |
|---|---|---|---|
| 50 | 704 | 547 | 78% |
| 60 | 1.032 | 450 | **44%** |
| 80 | 2.218 | 531 | **24%** |
| 110 | 6.991 | 537 | **8%** |

Đường cong mũ `108 × 1,039^(f-1)` đòi tới 6.991 PP ở tầng 110, trong khi cả pet người chơi cũng chỉ đạt khoảng 770 PP dù lên cấp bao nhiêu. Kết quả: mọi tầng trên 55 đều thắng 99–100%.

**Cách sửa:** tách làm hai phần.

- **Sức mạnh nền** từ tầng 51 chuyển sang tuyến tính chậm: `704 + (f−50) × 5,4` → tầng 110 là 1.028 PP, nằm trong tầm hệ chỉ số biểu diễn được.
- **Độ khó thật** đến từ **hệ số ép** nhân thẳng vào chỉ số: `1,14 + (f−50) × 0,0115` → tầng 51 ×1,15, tầng 110 ×1,83. Đây là cơ chế `mult` đã có sẵn trong engine nên không phải dựng gì mới.

`[đo]` Dò bốn giá trị hệ số rồi chọn nền 1,14 dốc 0,0115. Kết quả với pet nuôi kỹ, bộ inox, ly đúng nhóm vị:

| Tầng | 55 | 60 | 70 | 80 | 90 | 100 | **110** |
|---|---|---|---|---|---|---|---|
| Thắng | 95% | 80% | 62% | 57% | 60% | 61% | **30%** |

Mini boss dễ hơn, boss chặng khoảng 60%, và Bản Chuẩn 30% — đúng tầm một bức tường cuối, tương đương tầng 50 ngày trước.

## Cơ chế Chuẩn hoá

Bản Chuẩn không có đòn đánh đặc biệt nào. Cơ chế của nó là: **cứ 3 lượt, xoá sạch mọi hiệu ứng của cả hai bên.**

Không gây sát thương. Chỉ triệt tiêu mọi chuẩn bị — đúng thứ nó làm với một ly pha tay. `[đo]` Kích hoạt 132 lần trong 40 trận, 100% lần nào cũng xoá sạch cả hai bên.

Bản Nháp ở tầng 105 dùng cùng cơ chế nhưng 4 lượt một lần — "nó vẫn để lại một khoảng cho sai số".

## Mười hai thẻ cốt truyện mới

Tổng lên **22 thẻ**, mỗi thẻ vẫn ba phần: lời boss, đoạn kể, thẻ kiến thức vận hành.

| Tầng | Kiến thức |
|---|---|
| 55 | Tỉ lệ nền của một ly cà phê sữa |
| 60 | Vì sao cà phê hoà tan không có crema |
| 65 | Truy xuất nguồn gốc thật gồm gì |
| 70 | Đặt tên món theo vùng thì phải giữ được |
| 75 | Món nhanh và món kể chuyện |
| 80 | Nhớ gu khách quen |
| 85 | Hương tự nhiên và hương tổng hợp |
| 90 | Giữ vị giác của chính mình |
| 95 | Thiết kế cho ca đông nhất |
| 100 | Nước ép tươi và nước ép hoàn nguyên |
| 105 | Sai số cho phép trong công thức |
| 110 | Chuẩn hoá tới đâu là đủ |

Tổng chữ cốt truyện: 12 KB.

## Đoạn kết — "Giọt sai số"

Không phải đánh bại. Là đưa cho nó một thứ nó không mô phỏng được.

> **Bản Chuẩn:** *"Cậu thắng. Nhưng cậu không trả lời được câu hỏi của tôi. Vì sao vẫn pha tay?"*
>
> **Pet:** *"Vì hôm nay trời nóng hơn hôm qua."*
>
> **Bản Chuẩn:** *"…Tôi có dữ liệu nhiệt độ. Tôi đã tính cả điều đó."*
>
> **AM-00:** *"Cậu tính nhiệt độ trung bình. Nó nếm ly nước này, ở đây, bây giờ."*

Và AM-00 nói ra thứ nó đã giữ suốt hai mươi ba bản:

> *"Tôi là AM-00. Tôi cũng là một cỗ máy, và tôi đã ngồi ở góc quán đó mười mấy năm. Tôi biết thứ tôi không làm được."*

Kết bằng câu của pet: *"Không có công thức tốt nhất. Chỉ có ly hợp với người đang cầm nó."*

**Bản Chuẩn không biến mất.** Nó vẫn ở đó, vẫn đúng, vẫn tối ưu. Chỉ là từ hôm nay nó biết có một chỗ nó không tới được. Thưởng: 5.000 xu, 2 Lõi Automa, 1 Hộp vàng. Tháp vẫn leo lại được.

## Kích thước

| | v23.1 | v24 |
|---|---|---|
| index.html | 607 KB | 623 KB |
| Bộ PWA | 653 KB | **669 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 25 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Việc còn treo, xếp theo mức quan trọng

1. **Nối thật cầu nối với công cụ vận hành** — công cụ chạy trên HTML nên nhúng iframe được. Đây vẫn là việc duy nhất có thể đổi bản chất cả trò chơi.
2. **Cân lại sáu hành động chăm sóc** — Ngủ đang chiếm 72%, Rèn và Chơi gần như không ai dùng.
3. **Vài ngày chỉ dùng công cụ, không mở game** — để bảng so sánh có nhóm đối chứng.

---

# Phụ lục v25 — Pet sống và tuyến "Quán của chúng ta"

## Đối chiếu ba mươi mục đề xuất

`[đo]` **18/30 đã có** trong bản trước. Nhóm "Thế giới" xong 9/10 nên em không làm thành bản riêng. Nhóm "Pet sống" có 4 mục mới, và đề xuất tuyến truyện mới là mục đáng nhất.

## 1. Lịch sinh hoạt theo giờ

Trước v25 pet đi lại ngẫu nhiên giữa tám khu. Nay nó có thói quen, và mở app lúc nào cũng thấy nó đang làm một việc hợp với giờ đó.

| Giờ | Khu | Đang làm |
|---|---|---|
| 5–7 | Quầy chính | vừa dậy |
| 7–10 | Quầy chính | trông quầy |
| 10–12 | Bếp | chuẩn bị ca trưa |
| 12–14 | Quầy chính | chạy quầy |
| 14–16 | Khu rửa | rửa dọn |
| 16–18 | Sân tập | tập ở sân sau |
| 18–20 | Vườn sau | ra vườn |
| 20–22 | Góc chơi | ngồi nghỉ |
| 22–5 | Gác ngủ | đang ngủ |

`[đo]` 10 khung giờ phủ đủ 24h, dùng 7 trong 8 khu. Nhãn khu nay hiện kèm việc đang làm: "Bếp · chuẩn bị ca trưa".

## 2. Khẩu vị theo loài — mục em nợ từ v18

Nối hai bảng đã tồn tại từ lâu mà **chưa hề chạm nhau**: sáu loài và sáu nhóm vị nguyên liệu.

| Loài | Thích | Ngại |
|---|---|---|
| Beano | đắng | ngọt |
| Milku | ngọt | chát |
| Matcha | chát | cay |
| Cacao | đắng | chua |
| Citrus | chua | đắng |
| Glacio | thanh | cay |

Sáu pet hoang cũng có khẩu vị riêng. Automa thì không — "máy không có khẩu vị".

Cho ăn **đúng nhóm vị thì Gắn bó tăng gấp đôi**, sai vị chỉ còn 0,4×. `[đo]` Cho ăn đúng vị: gắn bó 10 → 16.

Thêm bảng nông sản ngay trong phần Chi tiết: chạm một loại để cho ăn, loại hợp vị viền xanh, loại ngại thì mờ đi.

## 3. Năm mốc Gắn bó

25 · 50 · 75 · 90 · 100. Mỗi mốc một cảnh ngắn:

> **Gắn bó 50 — Nhận ra tiếng:** *"Bơ quay đầu lại trước cả khi bạn gọi tên."*
>
> **Gắn bó 90 — Biết bạn mệt:** *"Hôm nào bạn về muộn, Bơ không đòi chơi nữa."*

`[đo]` Không lặp lại sau khi đã hiện.

## 4. Tổng kết ngày

Sau 20 giờ, mở app lần đầu trong ngày thì hiện bảng tổng kết: nhiệm vụ, lượt chăm sóc, tầng đã leo, chuỗi ngày — kèm một câu theo tâm trạng pet.

> *"Bơ nằm xuống, mắt vẫn nhìn ra cửa."*

## 5. Biểu tượng trong tab Việc

16 biểu tượng, mỗi nhiệm vụ một cái: 🔑 mở ca · 📊 nhập P&L · 📦 kiểm kho · 🧑‍🍳 chấm công · 🎯 đạt mục tiêu · 🧹 đóng ca, và mười cái cho tuần và tháng.

## 6. Tuyến "Quán của chúng ta" — lớp còn thiếu

Đây là đề xuất của người dùng, và nó lấp đúng chỗ trống: tháp kể về thế giới bên ngoài, vùng nguyên liệu kể về nơi đồ uống sinh ra, **nhưng không tuyến nào kể về chính cái quán của người chơi** — dù tám khu và 25 món nội thất đã nằm đó từ lâu.

Một chỉnh so với đề xuất gốc: **chương mở theo cột mốc của chính cái quán, không theo tầng tháp.**

| Chương | Câu hỏi | Mở khi |
|---|---|---|
| 1 · Mở cửa | "Quán này… là của chúng ta à?" | qua ngày đầu tiên |
| 2 · Khách đầu tiên | "Tại sao họ lại quay lại?" | giữ chuỗi 3 ngày |
| 3 · Nguyên liệu | "Rẻ hơn có nghĩa là tốt hơn không?" | thu hoạch lần đầu |
| 4 · Công thức | "Cùng nguyên liệu, sao hai người pha lại khác?" | pha thử 5 công thức |
| 5 · Nhân sự | "Một quán tốt cần máy móc hay con người?" | đủ 2 pet trong tổ đội |
| 6 · Quy mô | "Nếu có 1.000 khách thì sao?" | **đạt mục tiêu doanh thu** |
| 7 · Bản sắc | "Nếu mọi quán giống nhau, người ta nhớ quán nào?" | mở 12 thẻ tri thức |
| 8 · Quán của chúng ta | "Quán của chúng ta sẽ trở thành gì?" | qua đủ bảy chương |

Chương 6 mở từ **dữ liệu vận hành thật** qua cầu nối — đây là chỗ tuyến truyện chạm vào công việc ngoài đời rõ nhất.

Mỗi chương là một đoạn hội thoại bốn lượt giữa pet và AM-00, rồi tới thẻ vận hành. Chương cuối:

> **AM-00:** *"Bảy câu hỏi rồi. Tôi hỏi câu cuối: quán của cậu sẽ trở thành gì?"*
> **Pet:** *"Mình không biết. Mai còn phải mở cửa đã."*
> **AM-00:** *"…Đó là câu trả lời đúng nhất tôi từng nghe."*
> **Pet:** *"Sao lại đúng?"*
> **AM-00:** *"Vì quán không trở thành gì cả. Nó là thứ cậu làm lại mỗi ngày."*

Chương mở **tuần tự** — phải xong chương trước mới xét chương sau, nên câu chuyện đi đúng thứ tự. Xem lại được bất cứ lúc nào ở tab **Việc → Quán ta**.

## Ba lỗi trong lúc dựng

1. **Dùng sai khoá kho nông sản.** Em viết `invOf().crops` trong khi kho thật là `invCrop()`. Ba chỗ cùng sai.
2. **Gọi hàm cục bộ từ ngoài.** `g('feed')` là hàm khai trong `applyAct`, không dùng được ở module khác. Đổi sang `perkOf('gain','feed')`.
3. **Biểu tượng nhiệm vụ thêm hai lần.** Một lần bằng phép thay thế, một lần bằng biểu thức chính quy — cùng một dòng. `[đo]` 12 biểu tượng cho 6 nhiệm vụ. Đã gỡ.

Và một điều chỉnh bộ test: **banner mốc Gắn bó và banner chương mới chặn thao tác của 68 kịch bản cũ.** Thêm bước bỏ qua vào phần khởi tạo.

## Kích thước

| | v24 | v25 |
|---|---|---|
| index.html | 623 KB | 644 KB |
| Bộ PWA | 669 KB | **690 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 26 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Việc còn treo

1. **Nối cầu nối với công cụ** — chương 6 của tuyến mới đã chờ sẵn dữ liệu doanh thu thật.
2. **Cân lại sáu hành động chăm sóc** — Ngủ đang chiếm 72% số lượt.
3. **v26 — di truyền**: cây gia phả, kỷ niệm truyền đời, bản sắc theo đời, sưu tầm dòng dõi.

---

# Phụ lục v26 — Sửa cân bằng, sửa dữ liệu, và Quán của chúng ta

Gộp hai đợt theo yêu cầu.

## 1. Điểm cốt dư — lỗi thiết kế từ v15

`[đo]` Đo được mức dư theo cấp, và nó tệ dần:

| Cấp | Kiếm được | Tiêu hết được | **Dư** |
|---|---|---|---|
| Lv20 | 57 | 55 | 2 |
| Lv30 | 87 | 52 | **35** |
| Lv40 | 117 | 50 | **67** |
| Lv60 | 177 | 53 | **124** |

Nguyên nhân: điểm cấp theo cấp không giới hạn, nhưng trần tiêu cố định 15% trần tiềm năng.

**Sửa theo hướng người dùng đề xuất, nhưng không chặn cấp:**

| Giai đoạn | Trần | Tiêu hết được |
|---|---|---|
| Sơ sinh | 8% | 22 điểm |
| Thiếu niên | 11% | 30 điểm |
| Trưởng thành | 15% | 41 điểm |
| **Tiến hoá** | **20%** | **55 điểm** |

Và **điểm dư đổi được**, không ném đi: 8 điểm đổi 1 hạt kinh nghiệm · 5 điểm đổi 120 xu · 10 điểm đổi 2 hạt mầm. Bảng đổi chỉ hiện khi thật sự dư.

Cách này giữ được cảm giác lên cấp mà vẫn có lý do để tiến hoá — trần nâng từ 15% lên 20%.

## 2. Ngưỡng phá đảo tầng 110

`[đo]` Con số để người chơi biết mình cần gì:

| | PP |
|---|---|
| Pet Thường Lv60 đủ điểm | 502 |
| Hiếm | 584 |
| Cực hiếm | 708 |
| Huyền thoại | 792 |
| Thần thoại | 989 |
| **Đối thủ tầng 110** | **2.446** |

Chênh 2,5 lần, bù bằng tổ đội +30%, trang bị inox +20%, ghép +10 thêm 4%, ly đúng vị +25% — cộng lại khoảng 1,9×. Nên thực đo ra 30% thắng.

Nghĩa là: **muốn phá tầng 110 gần như bắt buộc có pet Huyền thoại trở lên, đủ bộ inox, và mang đúng ly.**

## 3. Nguyên liệu theo vùng — sửa theo thực tế

Miệt vườn trồng Dâu là sai rõ ràng. Thêm **tám nông sản mới**: Bơ, Sầu riêng, Đào, Trà shan tuyết, Dừa, Xoài, Bưởi, Atisô.

| Vùng | Trước | Sau |
|---|---|---|
| Cao nguyên đỏ | Robusta, Gừng | Robusta, **Bơ, Sầu riêng** |
| Đồi sương | Arabica, Dâu | Arabica, **Đào**, Dâu |
| Đồi trà | Trà xanh, Ô long | Trà xanh, Ô long, **Shan tuyết** |
| Miệt vườn | Ca cao, ~~Dâu~~ | Ca cao, **Dừa, Xoài** |
| Vườn cam | Cam, Chanh | Cam, Chanh, **Bưởi** |
| Thung lũng lạnh | Dâu, Bạc hà, Gừng | Dâu, Bạc hà, **Atisô** |

## 4. Định lượng 24 công thức

`[đo]` Rà toàn bộ: **16/24 công thức có phần nền lỏng chiếm hơn 62% thể tích ly** — không đúng thực tế, vì ly có đá thì đá chiếm 100–150g.

Ví dụ Trà Gừng Sả: ly 350ml mà ghi trà 320ml, tức 91%. Đã sửa xuống 160ml cộng 140g đá.

Quy tắc áp dụng: **ly đá thì nền lỏng 45–55% tổng thể tích; ly nóng thì 85–90%, không có đá.** `[đo]` Sau khi sửa: 24/24 đúng tỉ lệ.

## 5. Ba lỗi hiển thị

- **"null xu"** ở Hương liệu tổng hợp — nguyên liệu này chỉ lấy từ Pandora, không bán, nhưng vẫn hiện nút mua. Thêm cờ `noShop` và lọc khỏi cửa hàng.
- **Tràn dòng tên hạt** trong bảng nông sản ở trang Nhà — thêm cắt hai dòng và ngắt từ.
- **Thuốc ủ ấm và Sữa tăng trưởng chưa có hình** — vẽ hai biểu tượng SVG: lọ nâu có hơi bốc lên, và chai trắng nắp xanh có mũi tên đi lên.

## 6. Thông tin pet trong chuồng

Bấm vào pet chưa nuôi mở bảng giữa màn hình, giống cách đã làm với kỹ năng và trang bị: chân dung, độ hiếm, tính cách, giai đoạn, Pet Power, sáu chỉ số, trần tiềm năng, đặc điểm, khẩu vị, quirk của loài — cùng ba nút Đưa vào tổ đội / Đổi vào nuôi / Thả.

## 7. Quán của chúng ta — sáu vị trí

Chuồng trước nay chỉ là danh sách pet không dùng vào việc gì ngoài tổ đội ba người. Nay mỗi pet đứng được một vị trí thật trong quán.

| Vị trí | Hợp với | Quán được lợi |
|---|---|---|
| ☕ Pha chế | INT | Ly chế biến giữ hiệu lực lâu hơn 15% |
| 🧾 Thu ngân | LUCK | Xu nhận được tăng 10% |
| 🍽️ Phục vụ | SPD | Thưởng nhiệm vụ vận hành tăng 12% |
| 📋 Quản lý | INT | Pet chính hao hụt chậm hơn 12% |
| 🛵 Giao hàng | SPD | Chuyến khám phá nhanh hơn 15% |
| 🔍 Kiểm đồ | DEF | Rác sinh ra giảm 20% |

Xếp pet có chỉ số hợp vị trí (từ 40 trở lên) thì hiệu ứng **mạnh gấp 1,5 lần** và hiện nhãn "hợp". Một pet chỉ đứng được một chỗ.

**Đặt tên quán được**, như đặt tên pet. Và trang Quán liệt kê **nội thất đang đặt** — lần đầu tiên 25 món nội thất có chỗ để nhìn thấy chúng đang phục vụ cái gì.

Hiệu ứng nối thẳng vào cơ chế sẵn có: xu và hao hụt qua `perkOf`, rác qua `consumeGear`, chuyến đi qua `tripProgress`, thưởng nhiệm vụ qua `claim`.

## Kích thước

| | v25 | v26 |
|---|---|---|
| index.html | 644 KB | 660 KB |
| Bộ PWA | 690 KB | **706 KB** |

`[đo]` 27 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ** — vẫn đứng đầu danh sách.
2. **Boss tạo hình đa dạng + kỹ năng riêng có hiệu ứng** — hiện boss chỉ khác nhau ở màu và cơ chế kháng.
3. **Di truyền** — cây gia phả, kỷ niệm truyền đời, sưu tầm dòng dõi.
4. **Cân lại sáu hành động chăm sóc** — Ngủ vẫn chiếm 72%.

---

# Phụ lục v27 — Boss đa dạng và Di truyền

Gộp hai đợt theo yêu cầu.

## 1. Chín khung thân cho phe Công Nghiệp

Trước v27, **mọi boss dùng chung một khối hộp**, chỉ khác màu — đúng như người dùng nhận xét. Nay chín khung riêng:

| Khung | Hình | Dùng cho |
|---|---|---|
| `box` | hộp giấy vuông vắn | Nhãn Vùng Trồng, Tem Truy Xuất |
| `can` | lon nước có gờ trên dưới | Hắc Tinh Ga, Sủi Cam, Lon Móp |
| `bottle` | chai nhựa cổ thon | Trà Đóng Chai, Siro Dâu Đỏ, Chai Nửa Lít |
| `tank` | bồn chứa nằm ngang | Siro Ngọt Gắt, Cốt Cam Cô Đặc, Vòi Siro |
| `sack` | bao bột phình dưới | Bột Béo, Muỗng Bột |
| `drum` | thùng phuy có đai | Viên Dai, Viên Nửa Chín |
| `sachet` | gói bột mép răng cưa | Bột Hoà Tan, Gói Bột Cam |
| `vial` | lọ tinh dầu cổ dài | Hương Dừa Tổng Hợp, Lọ Tinh Dầu |
| `core` | khối lõi bát giác | **Bản Chuẩn**, Bản Nháp |

`[đo]` 23 boss cho ra đúng 9 khung khác nhau. Tên lạ rơi về khung mặc định, không vỡ.

## 2. Mười hai chiêu riêng, mỗi chiêu một hiệu ứng

Trước v27 boss chỉ có **cơ chế bị động** — kháng, hồi, đắp lớp. Nay mỗi boss thêm một chiêu chủ động, có tên, có hiệu ứng hình, và có tác động thật.

| Boss | Chiêu | Tác động |
|---|---|---|
| Hắc Tinh Ga | **Xì Ga** | choáng một lượt, mỗi 5 lượt |
| Sủi Cam | **Ngập Bọt** | giảm 15% tấn công |
| Siro Ngọt Gắt | **Rót Siro** | giảm 20% tốc độ |
| Bột Béo | **Màn Váng** | giảm 18% trí lực |
| Viên Dai | **Dính Răng** | giảm 22% tốc độ |
| Bột Hoà Tan | **Ba Mươi Giây** | gây thêm 5% máu tối đa |
| Nhãn Vùng Trồng | **Dán Nhãn** | xoá một hiệu ứng tốt của đối thủ |
| Trà Đóng Chai | **Đóng Nắp** | đối thủ không hồi máu 3 lượt |
| Hương Dừa Tổng Hợp | **Bảy Phân Tử** | giảm 20% trí lực và 12% tốc độ |
| Cốt Cam Cô Đặc | **Pha Loãng** | hút 4% máu tối đa để tự hồi |
| Siro Dâu Đỏ | **Phủ Đỏ** | giảm 16% phòng thủ |
| Bản Chuẩn | **Hiệu Chỉnh Lại** | xoá hiệu ứng hai bên, gây 3,5% máu tối đa |

Mỗi chiêu mượn một trong mười khuôn hiệu ứng của v24, kèm **nháy viền đỏ quanh sàn đấu** cho ra sức nặng.

`[đo]` 12/12 chiêu tung được, dùng đủ 10 loại tác động.

### Cân bằng — lần đầu đo ra rất lệch

`[đo]` Thêm chiêu vào lần đầu làm ba boss tụt thảm:

| Boss | Không chiêu | Có chiêu |
|---|---|---|
| Viên Dai | 32% | **6%** |
| Hương Dừa Tổng Hợp | 59% | **9%** |
| Bản Chuẩn | 36% | **5%** |

**Choáng là hiệu ứng nặng nhất** — trong trận khoảng 20 lượt, mất 2–3 lượt là mất trận. Đã sửa: giãn chu kỳ, và với Viên Dai thì **bỏ choáng hẳn, đổi sang làm chậm** ("trân châu dính chặt răng" hợp hơn với làm chậm). Bản Chuẩn hạ hệ số từ 1,30 xuống 1,16.

`[đo]` Bảng cuối, pet nuôi kỹ có bộ inox và ly đúng nhóm vị:

| Tầng | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | **110** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Thắng | 100% | 100% | 100% | 100% | 36% | 68% | 70% | 42% | 69% | 36% | **38%** |

Bốn boss đầu là bài học, từ tầng 50 dao động 36–70%, Bản Chuẩn 38%.

## 3. Di truyền

Đây là phần em thấy đáng nhất trong cả danh sách ba mươi mục trước đó, vì nó **nối hai hệ đang chạy song song mà chưa hề chạm nhau**: lai tạo (cơ học — gen, chỉ số, đời) và kỷ niệm (cảm xúc — 18 mốc).

### Ký ức thừa hưởng

Khi lai tạo, con nhận **hai ký ức** lấy từ kho kỷ niệm của người chơi và từ ký ức bố mẹ đã mang từ đời trước. Bảng hiện ra sau khi sinh ghi một dòng:

> *"Nó chưa từng sống những ngày này. Nhưng nó mang theo."*

Đời thứ ba mang ký ức của ông bà. Đó là thứ biến "một con pet thay thế" thành một dòng họ.

### Đặc điểm và ưu thế dòng dõi

- Mỗi đặc điểm của bố mẹ có **55%** truyền xuống, tối đa 2
- Mỗi đời cộng **1,5% trần tiềm năng**, trần 10 đời

`[đo]` Con đời hai: 2 ký ức thừa hưởng, 2 đặc điểm, trần HP 108 → 110.

### Cây gia phả

Tab mới trong Khác. Xếp theo đời, mỗi cá thể ghi tên, loài, số ký ức mang theo, và tên bố mẹ. **Pet đã thả vẫn nằm trong sổ** — mờ đi, nhưng không mất.

Sổ dòng dõi lưu riêng khỏi danh sách pet, nên thả pet không làm đứt cây.

## Kích thước

| | v26 | v27 |
|---|---|---|
| index.html | 660 KB | 674 KB |
| Bộ PWA | 706 KB | **720 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 28 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ vận hành** — vẫn đứng đầu, và vẫn chưa chạy thật lần nào.
2. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72% số lượt, Rèn và Chơi gần như không ai dùng.
3. **Nhóm đối chứng cho bảng đo** — cần vài ngày chỉ dùng công cụ, không mở game.

---

# Phụ lục v28 — Pet tự bắt chuyện

## Đối chiếu trước khi làm

`[đo]` Người dùng nêu 12 mục cho bản này. Kiểm ra **9 mục đã có**: bộ 14 trạng thái animation (v11), pet nói khi đói, khi thắng boss, khi mở thẻ cốt truyện, khi được kỷ niệm (v16–v17), hoạt cảnh tiến hoá (v10), thẻ kỷ niệm trượt xuống (v16), banner hạ boss (v2), thẻ cốt truyện kể bằng hội thoại có chân dung (v17).

**Ba mục thiếu thật:** pet không phản ứng khi nhận xu từ nhiệm vụ, khi tăng gắn bó, và khi dữ liệu vận hành tới.

Nhưng chẩn đoán đúng nằm ở chỗ khác, và người dùng xác nhận: **pet chỉ phản ứng khi người chơi chạm vào nó.** Ngoài lúc đó ra nó chỉ đi lại. Chưa bao giờ nó tự mở lời.

## Pet tự bắt chuyện — 22 chủ đề, 75 câu

Khi ở trang Nhà và không ai chạm vào, pet tự nói mỗi **26–62 giây** về thứ nó đang thấy. Đêm khuya thì thưa hơn 1,8 lần.

| Nhóm | Nói về | Ví dụ |
|---|---|---|
| Giờ giấc | thời điểm trong ngày | *"Khuya rồi. Bạn ngủ đi."* |
| Việc đang làm | lịch sinh hoạt v25 | *"Bạn để mình rửa dọn nốt đã."* |
| Nội thất | món đang đặt trong quán | *"Từ hồi có máy pha espresso, làm nhanh hẳn."* |
| Khu đang đứng | một trong tám khu | *"Mình hay ngồi góc chơi lúc vắng."* |
| Vườn sau | đang trồng hay đã chín | *"Có cái hái được rồi kìa!"* |
| Khung lễ | khung đang bật | *"Trang trí Trung Thu nhìn vui ghê."* |
| **Dữ liệu vận hành** | doanh thu, checklist, giá vốn hôm qua | *"Hôm qua quán mình bán tốt thật."* |
| Việc còn lại | nhiệm vụ chưa xong | *"Còn 4 việc chưa xong đâu nhé."* |
| **Kỷ niệm cũ** | lấy ngẫu nhiên từ sổ | *"Tự nhiên mình nhớ hôm 'Trọn một tuần'."* |
| Chuỗi ngày | streak từ 3 trở lên | *"5 ngày liền rồi đấy."* |
| Gắn bó | khi bond ≥ 70 | *"Mình không đi đâu đâu."* |
| Khẩu vị | loài thích và ngại vị gì | *"Mình vẫn thích vị đắng nhất."* |
| Dòng dõi | khi là đời 2 trở lên | *"Bố mẹ mình chắc cũng đứng ở đây."* |
| Trang bị | món đang mang | *"Cái Thìa inox này cầm vừa tay."* |
| Tháp | vé và tầng hiện tại | *"Tầng 38 chắc khó hơn tầng trước."* |
| Vùng đã đi | một vùng nguyên liệu | *"Bao giờ mình đi Đồi trà nữa?"* |
| Hộp chưa mở | kỳ ngộ còn hộp | *"Còn hộp chưa mở kìa!"* |

Pet **im lặng** khi: không ở trang Nhà, tab bị ẩn, đang chăm sóc, đang kéo pet, đang ngủ đông, đang đi khảo sát, hoặc **đang có bất kỳ lớp phủ nào** — hội thoại, bảng, banner.

`[đo]` 14 lượt sinh ra 14 câu khác nhau, không lặp lại trong 10 lượt gần nhất, không còn chỗ trống chưa thay.

## Ba phản ứng còn thiếu

| Lúc | Pet nói |
|---|---|
| Nhận xu từ nhiệm vụ | *"Ghi vào sổ rồi nhé."* · *"Được 25 xu rồi!"* |
| Tăng mốc gắn bó | *"Bạn gọi là mình biết ngay."* (mốc 50) |
| **Dữ liệu vận hành tới** | *"Hôm nay quán mình bán tốt ghê!"* |

Mục thứ ba là chỗ đáng tiếc nhất trước v28: **đó chính là khoảnh khắc công việc thật chạm vào game**, mà pet lại im lặng.

Cả ba đều kèm nhún người và đổi biểu cảm, rồi trở lại bình thường sau khoảng 1,2 giây.

## Một lỗi tiếng Việt

Bản đầu ghép câu ra **"Mình đang đang ngủ đây"** — vì trường `act` trong lịch sinh hoạt là cụm mô tả ("đang ngủ", "ở trong bếp"), không phải động từ dùng được trong câu.

Tách riêng trường `doing` với động từ sạch: "ngủ", "chuẩn bị đồ", "rửa dọn", "tưới cây". Câu giờ đọc trôi: *"Lát nữa tưới cây xong thì làm gì tiếp nhỉ?"*

## Kích thước

| | v27 | v28 |
|---|---|---|
| index.html | 674 KB | 684 KB |
| Bộ PWA | 720 KB | **730 KB** |
| Trần | 6 MB | 6 MB |

Kho câu tốn 3 KB.

`[đo]` 29 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ** — và giờ nó còn đáng hơn: pet đã có sẵn câu để nói khi dữ liệu thật tới.
2. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72%.
3. **Nhóm đối chứng cho bảng đo.**

---

# Phụ lục v29 — Pet biết nhớ

Bản đề xuất này tự đặt đúng nguyên tắc: **"Không thêm hệ thống mới. Chỉ gom hệ thống hiện có."** Đó là lý do nó là bản đề xuất tốt nhất trong cả dự án.

`[đo]` Đối chiếu 10 mục: 1 đã có đủ, 4 có một nửa, 5 thiếu hẳn.

## 1. Pet nhớ chuyện vừa xảy ra với chính người chơi

Đây là ý mạnh nhất. v28 pet nói về **thứ nó đang thấy**; v29 nó nói về **thứ đã xảy ra**.

Chín loại sự kiện được ghi lại khi chúng xảy ra thật: ngày quán đông, thắng boss, thua boss, mua nội thất, trứng nở, đi vùng, pha công thức mới, làm xong việc, thả pet.

Hôm sau pet nhắc lại:

> *"Cái Máy pha espresso mua hôm nọ dùng quen rồi."*
> *"Nhớ hôm hạ Hắc Tinh Ga không? Mình vẫn còn mỏi."*
> *"Muối có đôi mắt giống mình."*
> *"Bao giờ quay lại Đồi trà nữa?"*

Cửa sổ nhắc có hai đầu: **chưa đủ 6 giờ thì không nhắc** (vì nó vừa xảy ra, nhắc lại thành ngớ ngẩn), và **quá 72 giờ thì quên**. `[đo]` Xác nhận cả hai.

Danh sách "còn nhớ" hiện luôn trong phần Chi tiết của pet.

## 2. Mốc Gắn bó mở khoá thật

Trước v29, năm mốc chỉ hiện một banner rồi thôi. Nay mỗi mốc mở một thứ:

| Bond | Mở ra |
|---|---|
| 25 | Gọi tên bạn bằng tên quán |
| 50 | **Có món ruột** — pet chọn một nông sản, cho ăn món đó thì Gắn bó tăng gấp rưỡi |
| 75 | Tự đề xuất hoạt động |
| 90 | Biết bạn mệt |
| 100 | Kỷ niệm trọn đời |

Món ruột chọn **một lần và giữ suốt đời pet**, lấy trong nhóm vị mà loài đó thích.

## 3. Hai nhánh tiến hoá mới

Bốn nhánh cũ đều nói về **pet**. Hai nhánh mới nói về **quan hệ giữa pet và người chơi**:

| Nhánh | Điều kiện | Tên dạng |
|---|---|---|
| **Đồng Hành** | làm cùng chủ quán từ 60 lượt nhiệm vụ | *"Nó đứng cạnh bạn suốt những ca dài nhất."* |
| **Linh Hồn** | Gắn bó 100 và nuôi đủ 12 ngày | *"Không còn ranh giới giữa nó và cái quán này."* |

Hai nhánh này xét **trước** bốn nhánh cũ, nên ai chơi theo hướng vận hành hoặc hướng gắn bó sẽ ra dạng riêng.

## 4. Truyền thống dòng và ký ức gia tộc

Cây gia phả v27 mới chỉ là sơ đồ. Nay dòng dõi có **tính cách riêng**, suy từ việc người chơi đã làm thật:

Gan dạ (thắng ≥20 trận) · Chịu khó (≥40 nhiệm vụ) · Đi chân đất (≥15 chuyến) · Khéo tay (≥12 công thức) · Tình cảm (từng có pet Gắn bó 100)

Và **ký ức gia tộc** — một câu về đời trước, dựng từ dữ liệu thật:

> *"Ông bà của bạn từng hạ Hắc Tinh Ga."*
> *"Đời trước đã đi tới Đồi trà."*
> *"Cụ tổ của bạn sống 9 ngày ở quán này."*

## 5. Nhiệm vụ kể kiểu pet nhờ

Trước: `Mở ca đúng giờ — Checklist mở ca đã tick đủ — +15`

Sau: **`Sữa muốn mở cửa cùng bạn`** — *"Sáng rồi, mở cửa thôi."* — `+15`

Tick xong thì câu đổi thành *"Quán mở rồi đấy."* Sáu nhiệm vụ ngày đều có ba câu: lời nhờ, lời lúc chưa làm, lời lúc xong.

Cùng một cơ chế, khác hẳn cảm giác — đúng điều bản đề xuất nói: USP là **pet đồng hành cùng công việc**, không phải ô tick.

## 6. Tám món đồ của pet

Nhóm mới trong Shop, tách khỏi 25 món nội thất quán:

| Món | Tác dụng |
|---|---|
| Góc ngủ riêng | Năng lượng hồi nhanh hơn 12% |
| Chỗ ngồi quen | Tinh thần hao chậm hơn 10% |
| Hộp đồ chơi | Gắn bó từ Chơi tăng 20% |
| Kệ cây pet trồng | Thu thêm 1 nông sản mỗi lần hái |
| **Khung ảnh kỷ niệm** | Treo một kỷ niệm lên tường, đổi được |
| **Kệ chiến tích** | Bày tên những kẻ canh giữ đã hạ |
| **Chân dung gia đình** | Vẽ cả dòng dõi lên một bức |
| Đèn đêm | Quán sáng hơn sau 20 giờ |

Ba món in đậm **mở theo điều kiện**: đủ 3 kỷ niệm, đã hạ một kẻ canh giữ, đã có dòng dõi từ 3 cá thể. Chúng không cho chỉ số — chúng là chỗ để nhìn lại.

## 7. Tổng kết ngày kể bằng việc, không bằng số

Trước: bốn dòng số. Sau: danh sách những việc đã xảy ra hôm nay, lấy thẳng từ sổ sự kiện:

> ☕ Quán mở cửa · xong hết việc
> 🏆 Hạ được Hắc Tinh Ga
> 🪑 Mua Máy pha espresso
> 🔥 Chuỗi 5 ngày
> 💛 Gắn bó 100

## Một lỗi quy trình đáng ghi lại

Ba phép vá cuối — nhiệm vụ kể kiểu nhờ, nhóm đồ của pet, tổng kết ngày — **im lặng không chạy**, vì chúng nằm sau một phép vá bị lỗi trong cùng một kịch bản, và `SystemExit` dừng cả kịch bản.

Bộ test bắt được ngay: quest vẫn hiện chữ cũ, nhóm đồ pet 0 món, tổng kết 0 dòng. Nhưng nếu không có test thì ba tính năng này sẽ được ghi là "đã làm" trong tài liệu mà thực tế không tồn tại.

**Bài học:** khi một kịch bản vá nhiều chỗ, phép vá lỗi phải **ghi lại rồi đi tiếp**, không được dừng cả loạt.

## Kích thước

| | v28 | v29 |
|---|---|---|
| index.html | 684 KB | 703 KB |
| Bộ PWA | 730 KB | **749 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 30 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ** — vẫn đứng đầu sau mười chín bản.
2. **Bản Chuẩn ba pha** và **Linh hồn vùng** — từ tài liệu Vùng Nguyên Liệu, đã chốt hướng nhưng chưa làm.
3. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72%.

---

# Phụ lục v30 — Bản Chuẩn ba pha, loài theo vùng, linh hồn vùng

Bốn mục từ tài liệu Vùng Nguyên Liệu, sau khi đã lọc bỏ phần trùng với hệ thống có sẵn.

## 1. Bản Chuẩn ba pha

Giữ nguyên nhân vật và khung Quy mô đối Tâm hồn, lấy cơ chế ba pha của "Đấng Cất" gắn vào. Pha đổi **theo mức máu**, không theo lượt.

| Pha | Máu | Tên | Làm gì |
|---|---|---|---|
| 1 | 100–70% | **Tứ Phương** | Cứ 3 lượt hấp thụ một đặc tính vùng. Pet đúng loài đang bị hấp thụ gây thêm 25%. |
| 2 | 70–35% | **Pha Trộn** | Trộn hai đặc tính cùng lúc, kèm làm yếu một chỉ số của đối thủ. |
| 3 | dưới 35% | **Kệ Trống** | **Tắt mọi lợi thế khắc chế của cả hai bên.** Chỉ còn chỉ số, gắn bó, trang bị. |

Pha ba là chỗ hay nhất của thiết kế gốc: nó kiểm đúng thứ mình đã xây suốt ba mươi bản — nền tảng nuôi pet, không phải mẹo khắc chế.

`[đo]` Qua 40 trận với pet mạnh: cả ba pha đều chạm, 40/40 trận vào được Kệ Trống và cờ tắt khắc chế bật đúng.

## 2. Gắn loài với vùng — không thêm trục phân loại thứ ba

Tài liệu gốc đề xuất thêm **Hệ** (Cà phê / Trà / Sữa / Gia vị) làm trục thứ ba, bên cạnh Loài và Nhóm vị đã có. Người chơi sẽ phải nhớ ba bảng khắc chế cùng lúc.

Thay vào đó: **loài đã chính là hệ rồi.** Beano là cà phê, Matcha là trà, Cacao là ca cao. Chỉ cần gắn vùng với loài đã có.

| Vùng | Loài hợp |
|---|---|
| Cao nguyên đỏ | Beano |
| Đồi sương | Beano, Glacio |
| Đồi trà | Matcha |
| Miệt vườn | Cacao, Milku |
| Vườn cam | Citrus |
| Thung lũng lạnh | Glacio, Citrus |

`[đo]` Cả sáu loài đều có ít nhất một vùng. Milku ban đầu không có vùng nào — vì tài liệu gốc có "Đồng Cỏ Sữa" mà mình không có — nên xếp vào Miệt vườn theo dừa.

Pet hợp vùng đánh mạnh hơn **20%**, chịu đòn nhẹ hơn **10%**.

### Một quyết định cân bằng quan trọng

`[đo]` Lần đo đầu, tầng 90 lên **100% thắng** — vì ở đó pet vừa hợp vùng **vừa** khắc chế loài boss, hai lợi thế cộng dồn.

Sửa: **lợi thế vùng chỉ áp dụng khi không có khắc chế loài.** Hoặc bạn khắc chế, hoặc bạn hợp vùng — không được cả hai.

Và hạ hệ số Bản Chuẩn từ 1,16 xuống **0,98** vì ba pha nặng hơn hẳn cơ chế cũ (thắng tụt từ 36% xuống 9%). Nâng hai boss vốn dễ nhất: Nhãn Vùng Trồng 0,91 → 1,00 và Hương Dừa 1,03 → 1,12.

`[đo]` Bảng cuối:

| Tầng | 50 | 60 | 70 | 80 | 90 | 100 | **110** |
|---|---|---|---|---|---|---|---|
| Pet thường | 32% | 65% | 44% | 44% | 55% | 39% | **32%** |
| Pet hợp vùng | 31% | 89% | 81% | 66% | 97% | 75% | 34% |

Tầng 90 vẫn cao vì loài boss trùng loài vùng, nên không có lựa chọn khắc chế nào khác — mang pet Cacao tới đó gần như chắc thắng. Đó là cái giá phải trả có chủ đích: người chơi phải đã nuôi đúng loài đó lên đủ cấp.

## 3. Linh hồn vùng

Sáu linh hồn, một cho mỗi vùng. Thu phục được sau khi hạ kẻ canh giữ ở vùng đã đạt cấp 5, tỉ lệ **45%** mỗi lần.

| Linh hồn | Vùng | Cho gì |
|---|---|---|
| Hồn Đất Đỏ | Cao nguyên đỏ | Pet chính đánh mạnh hơn 10% ở chặng cùng vùng |
| Hồn Sương Sớm | Đồi sương | Kinh nghiệm tăng 15% |
| Hồn Trà Cổ | Đồi trà | Tinh thần hao chậm hơn 25% |
| Hồn Miệt Vườn | Miệt vườn | Thu thêm 2 nông sản mỗi lần hái |
| Hồn Vườn Cam | Vườn cam | Ly chế biến giữ lâu hơn 20% |
| Hồn Thung Lạnh | Thung lũng lạnh | Cây trồng nhanh hơn 30% |

`[đo]` Linh hồn **chỉ đứng ô phụ trợ**, không làm pet chính được — xác nhận chặn đúng. Chúng vẽ bằng thân Automa với màu riêng của vùng.

## 4. Chỉ báo Khắc chế / Bình thường / Bất lợi

Món nợ từ v23. Dữ liệu có từ v7, chỉ thiếu cách hiện. Nay trên UI tháp, trước khi leo:

> **Chặng này thuộc Cao nguyên đỏ**
> **PET** · `Khắc chế` — Beano là loài của Cao nguyên đỏ, đánh mạnh hơn 20%, chịu đòn nhẹ hơn 10%
> **LY** · `Chưa mang ly` — Kẻ canh giữ sợ nhóm đắng. Mang ly nhóm đó thì gây thêm 25%

`[đo]` Ba mức phân biệt đúng: Matcha ở Đồi trà → Khắc chế · Matcha ở Cao nguyên → Bình thường · Beano ở Cao nguyên → Khắc chế.

## Kích thước

| | v29 | v30 |
|---|---|---|
| index.html | 703 KB | 715 KB |
| Bộ PWA | 749 KB | **761 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 31 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ vận hành** — hai mươi bản rồi và vẫn chưa chạy thật lần nào. Đây vẫn là việc duy nhất có thể đổi bản chất dự án.
2. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72% số lượt.
3. **Nhóm đối chứng cho bảng đo** — vài ngày chỉ dùng công cụ, không mở game.

---

# Phụ lục v31 — Sửa lỗi, mặt cắt quán, bán ly dư

Gộp hai đợt theo yêu cầu.

## Lỗi nặng nhất: cả tuyến "Quán ta" chết cứng

Người dùng chụp màn hình ở **Ngày 10 mà vẫn 0/8 chương**. Nguyên nhân: điều kiện chương 1 đọc `S.stats.days` — **một trường không tồn tại**. Trạng thái chỉ có `S.hib.days` và `S.tel.days`.

Nên điều kiện luôn trả 0, chương 1 không bao giờ mở, và vì chương mở **tuần tự** nên cả tám chương chết theo.

Sửa: thêm hàm `dayNo()` và đổi mốc sang **ngày thứ hai** — nếu để ngày đầu thì hội thoại nổ ngay sau màn khởi đầu, đè lên phần hướng dẫn (bộ test `tc` bắt được đúng chỗ này).

**Vì sao lọt qua 6 bản:** kịch bản test tự đặt `S.ch.done` đầy để bỏ qua màn hội thoại — **test vô hiệu hoá chính thứ nó phải kiểm.** Đây là lần thứ hai (lần đầu ở v17 với AM-00).

## Đồ của pet mua được nhưng không hiện

Hai lỗi chồng nhau:

1. Em gọi `paintDecor()` ở **đầu** `paintProps()`, nhưng dòng ngay sau đó xoá mọi phần tử class `prop` — mà đồ pet cũng mang class đó. **Vẽ xong bị xoá ngay trong cùng một hàm.**
2. Quay lại trang Nhà **không vẽ lại đồ đạc**, nên mua ở Shop xong về Nhà vẫn không thấy.

`[đo]` Sau khi sửa: 4/4 món vẽ ra, toạ độ nằm đúng trong dải tám khu.

Toạ độ cũng sai lần đầu: `place()` nhận phần trăm trên **cả dải tám khu**, không phải trong từng khu.

## Thanh máu boss rơi ra ngoài sàn

`.bhud` đặt `bottom:-28px` so với đấu sĩ. Đấu sĩ thường ở `bottom:44px` nên thanh máu ở 16px — thấy rõ. Boss ở `bottom:8px` nên thanh máu ở **−20px, nằm ngoài sàn**.

Sửa: với boss thì đưa hẳn lên trên đầu (`top:-30px`), và nới rộng để tên dài không bị cắt.

## Hình trang bị trong shop

20 kiểu dáng đã vẽ từ v19 mà cửa hàng chỉ hiện chữ. `[đo]` Nay 8/8 thẻ có hình.

## Lọc chuồng và phân loại kho

**Chuồng:** sáu cách sắp xếp (mới nhất, sức mạnh, độ hiếm, cấp, giai đoạn, loài) cộng lọc theo loài. Chỉ hiện khi chuồng từ 4 pet trở lên. `[đo]` Sắp theo sức mạnh cho thứ tự giảm dần đúng.

**Kho:** bốn nhóm — Tiền và lượt · Hạt mầm · Nông sản đã thu · Nguyên liệu mua. Nhóm rỗng thì ẩn.

Và **bỏ hẳn ô "Thẻ vận hành"**: nó chỉ là số nhiệm vụ đã tick hôm nay, không phải vật phẩm, không dùng vào việc gì. Đặt trong Kho vật phẩm là gây hiểu nhầm.

## Mở ô vườn — có sẵn nhưng giấu quá sâu

Cơ chế mở 4 ô lên 8 ô (800 · 800 · 2.000 · 2.000 xu) **đã có từ lâu**, nhưng nút nằm ở cuối bảng Vườn sau, phải cuộn hết mới thấy.

Nay: **chạm thẳng vào ô đất đang khoá** là mở bảng mở đất, kèm bảng giá bốn mức. Và bảng gieo hạt có nút "Đang có 4/8 ô · mở thêm" ngay đầu.

## Nền sàn đấu theo vùng nguyên liệu

Bốn kiểu cảnh mới: **hàng cây thẳng lối** cho rẫy cà phê và vườn ca cao, **luống trà uốn sườn đồi**, **vườn cây có quả trên tán**, **nhà kính thung lũng**. Sáu bảng màu riêng.

Chặng tháp thuộc vùng nào thì vẽ cảnh vùng đó; đấu nhanh thì lấy vùng của loài pet đang nuôi.

## Mặt cắt quán — sáu pet đứng đúng chỗ

Thay trang "Quán ta" dạng danh sách bằng một mặt cắt quán thật. Vẫn giữ nút chuyển về danh sách.

- **Ba người sau quầy** — Kiểm đồ, Pha chế, Thu ngân — vẽ **dưới lớp quầy** nên chỉ thấy nửa trên, đúng như đứng sau quầy thật. Tên hiện ở dải dưới cùng.
- **Ba người khu khách** — Phục vụ, Quản lý, Giao hàng — đứng trên sàn, có tên ngay dưới chân.
- **Tường nền đổi theo món tường đã mua**: gạch mộc, ván gỗ, hay gạch men.

### 22 món nội thất lần đầu được vẽ

Từ v6 tới giờ, 25 món nội thất **chỉ cho hiệu ứng, chưa bao giờ hiện hình**. Nay 22 món có SVG riêng: máy pha, cối xay, ấm cổ ngỗng, máy xay, máy làm đá, giá pour-over, lọ hoa, chuông, tủ mát, cây monstera, ghế đẩu, bao cà phê, thảm, bảng menu, đồng hồ, tranh, bảng ghi đơn, kệ ly, bình trà, cân, đèn dây, đèn neon.

Ba món còn lại là tường nền, đúng ra phải làm phông chứ không phải vật thể.

`[đo]` 22/22 có hình, 6/6 vị trí xếp được pet, 3 người sau quầy vẽ đúng lớp.

## Bán ly dư lấy xu

Pha ly từ công thức đã mở để bán. Giá = 26 xu nền + 9 xu mỗi nguyên liệu, tối đa **12 ly mỗi ngày**. Vị trí Thu ngân cộng thêm vào giá.

`[đo]` Cam Ép Muối Biển bán được 53 xu. Pet cũng nói một câu khi bán xong.

## Kích thước

| | v30 | v31 |
|---|---|---|
| index.html | 715 KB | 740 KB |
| Bộ PWA | 761 KB | **786 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 33 bộ test chạy lại không lỗi. Kiểm trùng tên class sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Nối cầu nối với công cụ vận hành** — hai mươi mốt bản và vẫn chưa chạy thật lần nào.
2. **Thẻ công thức và hạt giống cho tám nông sản vùng mới** (bơ, sầu riêng, đào, shan tuyết, dừa, xoài, bưởi, atisô) — mới trồng được, chưa có công thức nào dùng tới.
3. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72%.

---

# v31.1 — Hai lỗi bố cục trên màn rộng

Người dùng chụp bản web mở trên màn hình máy tính. Hai lỗi chỉ xuất hiện ở đó, không thấy trên điện thoại.

## Lỗi 1 — thanh điều hướng trải hết màn hình

`[đo]` Cột nội dung rộng **520px đặt ở x=460**, nhưng thanh điều hướng rộng **1440px bắt đầu từ x=0**. Sáu nút Nhà · Việc · Đấu · Trứng · Shop · Khác dàn đều khắp màn hình, cách xa nội dung.

Nguyên nhân: `.nav` dùng `position:fixed; left:0; right:0` — bám viewport chứ không bám cột.

Sửa: `left:50%; transform:translateX(-50%); max-width:520px` — khớp đúng `.wrap`.

## Lỗi 2 — dải tab bị cắt hai đầu

`.cats` dùng `overflow:auto` để cuộn ngang. Khi tab đang chọn nằm giữa, trình duyệt **tự trượt tới nó**, cắt mất tab đầu bên trái và tab cuối bên phải. Ảnh chụp cho thấy "p · 2 vé" (cụt của "Leo tháp · 2 vé") và "Huyền th…".

Vấn đề sâu hơn cuộn: **người chơi không biết là còn tab để cuộn.**

Sửa: cho **xuống dòng** thay vì cuộn ngang. Áp dụng cho bốn dải: tab chính, bộ lọc độ hiếm, chọn ly, nhóm cửa hàng. Nút nhóm cửa hàng đổi từ `flex:1` sang `flex:1 1 86px` để chữ không bị ép.

`[đo]` Kiểm ở ba kích thước:

| | Thanh nav khớp cột | Số hàng tab | Tab tràn | Cuộn ngang |
|---|---|---|---|---|
| iPhone 390px | đúng | 2 | không | không |
| iPad 820px | đúng | 2 | không | không |
| Desktop 1440px | đúng | 2 | không | không |

Bảy tab hiện đủ, không cắt chữ nào.

`[đo]` 33 bộ test chạy lại không lỗi. Hiệu năng giữ nguyên.

## Ghi lại

**Bộ test chạy ở 390px và 820px nên không bắt được lỗi này.** Đã thêm `tmob.py` kiểm bố cục ở ba kích thước — nav có khớp cột không, tab có tràn khỏi cột không, trang có cuộn ngang không.

---

# Phụ lục v32 — Nông sản vùng, nhạc chiptune, thẻ quản trị quán

Gộp hai đợt theo yêu cầu.

## 1. Chín nông sản vùng lần đầu có chỗ dùng

`[đo]` Trước v32: **cả tám nông sản mới chưa có hình**, và **0/24 công thức** dùng tới. Chúng mới chỉ trồng được rồi để đó.

Thêm **quả hồng** và đổi Đồi sương từ Dâu sang Hồng như yêu cầu — giờ có **chín** loại.

Vẽ chín hình riêng, không dùng khuôn `seedArt` chung vì chín loại này hình dạng khác hẳn nhau: bơ có hạt nâu giữa ruột vàng, sầu riêng có gai tam giác, dừa có ba mắt, bưởi có múi chia tám, atisô có bông đỏ xếp lớp.

**Mười tám công thức mới**, mỗi nông sản ít nhất hai món:

| Nông sản | Món |
|---|---|
| Bơ | Sinh Tố Bơ · Bơ Cà Phê |
| Sầu riêng | Kem Sầu Riêng · Sầu Riêng Dừa |
| Đào | Trà Đào Miếng · Đào Soda |
| Hồng | Hồng Dầm Sữa · Trà Hồng Quế |
| Shan tuyết | Shan Tuyết Mộc · Shan Tuyết Sữa |
| Dừa | Dừa Dầm · Cà Phê Cốt Dừa |
| Xoài | Sinh Tố Xoài · Xoài Muối Ớt |
| Bưởi | Trà Bưởi Mật Ong · Bưởi Hồng Soda |
| Atisô | Trà Atisô Đỏ · Atisô Hấp Nóng |

`[đo]` 42 công thức, chín nông sản đều có chỗ dùng, **0 công thức lệch tỉ lệ nền lỏng**, sáu nhóm vị đều phủ.

## 2. Nút chuyển mặt cắt / danh sách — sửa lỗi kẹt

`[đo]` Nút chỉ nằm **trong mặt cắt**. Vào danh sách rồi là **kẹt luôn**, phải đổi tab khác rồi quay lại. Đã đưa nút ra ngoài, hiện ở cả hai chế độ.

## 3. Nhạc rè — thủ phạm là thứ em tự thêm vào

Ở v21 em thêm một **lớp nhiễu giả tiếng đĩa than** — bandpass 3200 Hz kèm tiếng lách tách ngẫu nhiên — để "cho có chất lofi". Trên loa điện thoại đúng cái đó nghe thành **loa rè**.

Bỏ hẳn, và đổi sang cách Game Boy tạo tiếng:

| | v21 lofi | v32 chiptune |
|---|---|---|
| Giai điệu | sóng sin, nốt ngẫu nhiên, vào chậm 0,55s | **sóng vuông**, mẫu nốt cố định, vào 0,012s |
| Bè trầm | 3 nốt sóng tam giác | **1 nốt sóng tam giác**, lọc dưới 420 Hz |
| Nhịp | 2,2–6,4 giây mỗi nốt | **0,34 giây** (đêm 0,46) — có nhịp rõ |
| Nhiễu nền | **có, 3200 Hz** | **bỏ hẳn** |
| Cắt tần số | 900 Hz | 2600 Hz + hạ kệ −18 dB từ 3000 Hz |

Vòng hợp âm ngày: **A – D – E – Bm**. Mỗi hợp âm có mẫu 16 nốt cố định, đổi quãng theo bảng — đúng cách nhạc game cũ viết.

`[đo]` Xác nhận: sóng vuông, bè trầm chạy, **không còn lớp nhiễu**.

## 4. Nút gập cho mục dài

Bốn mục tra cứu dài nay gập được: Điểm cốt, Cây kỹ năng, Khắc chế giữa các loài, Năm bậc chất liệu. Bảng khắc chế và bảng chất liệu **gập mặc định** vì chỉ để tra cứu.

## 5. Automa xuống tầng 30, thêm ba mẫu khác loại

`[đo]` Trước: mở ở tầng **50**, 5 mẫu — và **cả 5 đều chỉ cộng chỉ số**. Tám mẫu mà đều cộng chỉ số thì chỉ là tám con số, không thêm chiều sâu.

Nay mở ở **tầng 30**, và ba mẫu mới cho **hiệu ứng khác loại**:

| Mẫu | Cho gì |
|---|---|
| AM-06 Thu Hồi | Rác sinh ra giảm 30% |
| AM-07 Dò Tìm | Tỉ lệ rơi trang bị trên tháp tăng 35% |
| AM-08 Tiếp Máu | Hồi 12% máu tối đa sau mỗi tầng vượt qua |

`automaPassive()` chỉ cộng chỉ số nên không đọc được ba mẫu này — thêm `automaPerk(kind)` riêng, và chặn khoá lạ không lọt vào bảng chỉ số.

## 6. Hai mươi lăm thẻ quản trị quán

Ở v31 em **bỏ ô "Thẻ vận hành"** vì nó chỉ là bộ đếm vô nghĩa. Ý người dùng khác hẳn: một bộ thẻ kiến thức quản trị thật.

`[đo]` Đã có 30 thẻ kiến thức vận hành nằm rải trong cốt truyện và chương Quán ta — nhưng gắn với mạch truyện, không tra cứu theo chủ đề được.

Bộ mới, **năm nhóm năm thẻ**, mở dần theo số nhiệm vụ vận hành đã ghi nhận (mốc 2 đến 26):

| Nhóm | Năm thẻ |
|---|---|
| 🧑‍🍳 **Con người** | Ca làm nên dài bao nhiêu · Dạy việc bằng làm · Ba con số nhân sự · Giao việc kèm tiêu chí xong · Người giỏi rời đi vì quản lý |
| 💰 **Tài chính** | Giá vốn không phải chỉ nguyên liệu · Điểm hoà vốn · Dòng tiền khác lợi nhuận · Tăng giá đúng cách · Chi phí cố định giết quán |
| 📦 **Tồn kho** | FEFO trước FIFO · Tồn an toàn và điểm đặt hàng · Kiểm kho thật · Hao hụt bao nhiêu là bình thường · Hàng chậm luân chuyển |
| 🧼 **Chất lượng & ATTP** | Vùng nhiệt độ nguy hiểm · Nhiễm chéo · Hạn dùng sau khi mở nắp · Định lượng là chất lượng · Hồ sơ vệ sinh |
| 📊 **Dữ liệu & báo cáo** | Bốn con số xem mỗi ngày · Giá trị hoá đơn · Báo cáo phải dẫn tới hành động · So với chính mình trước · Dữ liệu sai tệ hơn không có |

Mỗi thẻ có đoạn giải thích và một mục **"Mang ra quán dùng được"** — cách áp dụng cụ thể. Tab riêng ở Khác → Quản trị, lọc theo nhóm.

Đây là phần có giá trị thật với nghề, không phải trang trí game.

## Trùng tên lần thứ tư — và lần này bộ kiểm không bắt được

`toggleFold()` và `S.fold` **đã tồn tại** từ trước cho bảng biên lai. Em đặt trùng cả hai. Vì v32 nạp trước ui.js nên hàm của ui.js thắng, và nút gập của em gọi nhầm vào bảng biên lai — `S.fold` biến từ `{}` thành `false`.

Ba lần trước đều là **class CSS** nên `audit.py` bắt được. Lần này là **tên hàm JS** nên lọt.

Đã đổi sang `panelFold` / `togglePanel` / `S.pfold`, và **mở rộng bộ kiểm** để soi thêm hai thứ:
- Tên hàm JS khai báo ở nhiều module
- Khoá trạng thái `S.*` khởi tạo ở nhiều nơi

`[đo]` Chạy trên v32: không còn hàm nào trùng tên.

## Kích thước

| | v31.1 | v32 |
|---|---|---|
| index.html | 740 KB | 759 KB |
| Bộ PWA | 786 KB | **805 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 34 bộ test chạy lại không lỗi. Bố cục đúng ở 390 / 820 / 1440px. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Còn treo

1. **Bản final: 42 hiệu ứng kỹ năng riêng biệt** — hiện 42 kỹ năng dùng chung 10 khuôn.
2. **Nối cầu nối với công cụ vận hành** — hai mươi hai bản rồi.
3. **Cân lại sáu hành động chăm sóc** — Ngủ chiếm 72%.

---

# Phụ lục v33 — Pet có ý muốn, và Cuốn đời

Gộp hai đợt theo yêu cầu, cộng ba mục sửa nhỏ.

## Hai lỗi ô vườn — chồng lên nhau

Người dùng báo "khó ấn hoặc vẫn lỗi" sau khi v31 đã sửa một lần. `[đo]` Đo ra **hai nguyên nhân riêng biệt**:

**1. Dải chấm chỉ khu đè lên ô đất.** `.zdots` ở `z-index:11`, `.gplots` ở `z-index:5`. Ô đất vẫn hiện, vẫn đúng kích thước, nhưng cú chạm rơi vào dải chấm. `[đo]` `elementFromPoint` tại tâm ô số 5 trả về `DIV.zdots`.

**2. Ô đất đang khoá dựng KHÔNG có sự kiện chạm.** Chỉ ô đã mở mới có `onclick`. Hàm `tapPlot()` xử lý được ô khoá từ v31, nhưng **không ai gọi nó**. Kể cả khi không bị che, chạm vào ô khoá vẫn không làm gì.

Sửa cả hai: nâng ô đất lên `z-index:14` và đẩy cao khỏi dải chấm, gắn `onclick="openExpand()"` cho ô khoá.

**Bài học:** v31 em sửa đường dẫn (thêm nhánh xử lý ô khoá trong `tapPlot`) mà **không kiểm bằng cú chạm thật** — chỉ gọi hàm trực tiếp trong test. Hàm đúng không có nghĩa là nút bấm được.

## Mong muốn có thể từ chối

Đề xuất gốc là ba lựa chọn cố định Chăm sóc / Làm việc / Khám phá, kèm pet tự gợi ý. Hai ý đó mâu thuẫn: nếu pet đã chọn sẵn thì ba nút để làm gì.

Cách đang dùng: **pet nêu một mong muốn cụ thể, người chơi có quyền từ chối.**

**13 mong muốn**, chọn theo chín yếu tố: đói, tâm trạng, gắn bó, tính cách, lịch sinh hoạt, dữ liệu vận hành, trứng, kỷ niệm, giờ trong ngày. Nhu cầu cấp bách (đói dưới 40, kiệt sức dưới 25) được ưu tiên.

| Nhóm | Ví dụ |
|---|---|
| 🏪 Việc | *"Mình muốn kiểm kho cùng bạn. Hình như có thứ sắp hết."* |
| ❤️ Chăm sóc | *"Hôm nay mình thèm Cà phê Arabica ghê."* (đọc món ruột từ mốc Gắn bó 50) |
| 🌎 Khám phá | *"Tầng 38 chắc có gì đó. Mình muốn xem."* |
| — | *"Không cần làm gì đâu. Ngồi đây một lát thôi."* (chỉ khi Gắn bó ≥ 70) |

**Từ chối KHÔNG trừ Gắn bó.** Từ chối là quyền, không phải lỗi. Nhưng từ chối ba lần liên tiếp thì pet nói khác đi:

> *"Dạo này bạn bận nhỉ. Mình vẫn ở đây."*

Làm xong đúng việc pet muốn thì **+4 Gắn bó** và pet phản ứng riêng, khác hẳn câu chung.

`[đo]` Từ chối: gắn bó 8 → 8, đổi sang mong muốn khác ngay.

## Nhiệm vụ vận hành giờ cho ba thứ

Đúng như mục 7 trong đề xuất: trước v33 làm xong nhiệm vụ **chỉ cộng xu**.

Nay: **xu + 2 Gắn bó + một mốc trong Cuốn đời + phản ứng của pet**, và nếu trùng mong muốn thì thêm 4 Gắn bó nữa.

`[đo]` Gắn bó 8 → 11, mốc cuốn đời 1 → 2 sau một nhiệm vụ.

## Cuốn đời — dòng thời gian theo ngày

**12 loại mốc** ghi tự động khi sự kiện xảy ra thật: gặp nhau, lần đầu làm việc cùng, lớn lên, tiến hoá, thắng kẻ canh giữ, chuyến đi đầu, mốc gắn bó, có em bé, có góc riêng, pha ly đầu tiên, gặp linh hồn vùng, qua một chương.

Xếp theo ngày, có trục dọc nối các mốc. Giữ tối đa 40 mốc, cũ nhất rơi ra.

Quan trọng hơn: **pet nhắc lại được**. Trong lúc tự nói, 12% khả năng nó lôi ra một mốc cũ từ hai ngày trở lên:

> *"Mình vẫn nhớ ngày 10. Đi Đồi trà."*
> *"Bạn còn nhớ ngày 5 không? Hôm đó hạ được Hắc Tinh Ga."*

## Bốn mục còn lại

**Nhánh Explorer** — đi đủ 25 chuyến. Tổng nay **bảy nhánh**: Chăm sóc, Chiến, Trí, Ẩn, Lữ Hành, Đồng Hành, Linh Hồn.

**Mốc Gắn bó 75 đổi nội dung** thành *Nhận xét công việc* — giữ nguyên con số cũ để người chơi đang ở mức 50 không bị lùi lại. Bảy câu đọc từ trạng thái quán thật: *"Bạn giữ được 6 ngày liền rồi. Mình đếm đấy."* · *"Rác trong quán nhiều rồi đấy."*

**Lời pet theo tính cách ở mọi trận** — trước chỉ có ở tầng boss. Thêm bối cảnh `fight` và `fightWin` cho cả mười tính cách: Brave *"Để mình xử lý."* · Timid *"Bạn đứng gần mình nhé…"* · Greedy *"Thắng có thưởng không?"*

**Chỗ chọn ly gập gọn** như điểm cốt và cây kỹ năng, nhãn hiện luôn trạng thái "đang mang".

**Công tắc bong bóng và cửa sổ nổi** trong Cài đặt. Hai nút ở trang Nhà chỉ hiện khi công tắc bật, và nút cửa sổ nổi tự ẩn nếu máy không hỗ trợ.

## Kích thước

| | v32 | v33 |
|---|---|---|
| index.html | 759 KB | 777 KB |
| Bộ PWA | 805 KB | **823 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` 35 bộ test chạy lại không lỗi. Bố cục đúng ở 390 / 820 / 1440px. Kiểm trùng tên sạch. Hiệu năng giữ nguyên: 0 khung rớt trên 270 khung.

## Một chỗ phải nói rõ là KHÔNG phải lỗi sản phẩm

Kịch bản `tb` báo không bấm được nút Bàn chế biến. `[đo]` Kiểm lại: nút **vẫn chạy đúng** — gửi sự kiện chạm trực tiếp thì bảng mở bình thường, không có lớp nào che, không có animation nào đang chạy.

Đây là giới hạn của công cụ test: camera còn đang trượt nên nó coi phần tử chưa đứng yên. Đã đổi cách bấm trong kịch bản. **Ghi lại để lần sau không đi sửa thứ không hỏng** — đúng loại nhầm lẫn đã xảy ra ở v23 với tên lớp `.rw`.

Bảy kịch bản cũ khác cũng phải sửa vì thẻ mong muốn thay chỗ thẻ gợi ý, và chỗ chọn ly nay gập mặc định.

## Còn treo

1. **Bản final: 42 hiệu ứng kỹ năng riêng biệt** — hiện 42 kỹ năng dùng chung 10 khuôn.
2. **Bố cục trang Nhà theo bản vẽ** — chưa làm, để cùng đợt final.
3. **Lý do lai tạo tới đời ba bốn** — hiện mỗi đời chỉ cộng 1,5% trần tiềm năng, quá nhỏ.
4. **Nối cầu nối với công cụ vận hành** — hai mươi ba bản rồi.

---

# Pet Drink: Scale & Soul — v1.0

Bản khởi động. Đổi tên từ Pet Pocket, gộp ba việc cuối cùng đã chốt.

## Trước hết: môi trường dựng bị dọn giữa chừng

Toàn bộ file module (`data.js`, `engine.js`, `ui.js`, `v2.js` … `v33.js`) và **bộ 35 kịch bản test** mất sạch khi container bị dọn. Khôi phục được từ bản đóng gói v33, nhưng chỉ còn `index.html` đã gộp.

**Hệ quả lâu dài:** từ v1.0 mã nằm trong **một file duy nhất**. Mọi sửa đổi làm trực tiếp trong `index.html`; `audit.py` tự tách phần mã ra `_js.js` để soi trùng tên.

Thay cho 35 kịch bản đã mất, viết `tsmoke.py` — một bộ kiểm tổng đi qua:
- 6 màn chính, 15 tab con
- 12 hệ chính (đếm dữ liệu: 42 kỹ năng, 42 công thức, 19 hạt, 25 thẻ quản trị, 110 tầng…)
- 4 luồng chạy thật: làm nhiệm vụ, đấu nhanh, leo tháp, nhạc
- lưu và nạp lại giữ đúng trạng thái

`[đo]` Toàn bộ đạt.

## 1. Bốn mươi hai hiệu ứng kỹ năng riêng biệt

Trước v1.0: 42 kỹ năng dùng chung **10 khuôn**. Nay mỗi kỹ năng **một hình SVG riêng**, vẽ đúng theo tên gọi.

| Kỹ năng | Hình |
|---|---|
| Cắt lá | chiếc lá có gân, nét chém chạy dọc |
| Mảnh băng | tinh thể nhọn hai đầu |
| Espresso | tia cà phê đậm có đầu tròn |
| Tường bọt | ba bong bóng viền chồng nhau |
| Nở tối | hoa năm cánh, nhuỵ vàng |
| Sốc chua | tia sét toả tám hướng |
| Đóng băng | bông tuyết sáu nhánh |
| Bùng caffeine | tách cà phê có hơi bốc |
| Truffle | viên tròn rỗ mặt |
| Vỏ cứng | lục giác hai lớp |

Cộng **12 kiểu chuyển động**: bay tán · vệt chém · vòng nở · nổ toả · rơi nảy · bay lên · xoáy tròn · tia quét · rung nảy · quay quanh · nhấp nháy · vòng cung.

Mỗi kỹ năng chọn một chuyển động, một màu, một số hạt, một cỡ. Kỹ năng tăng sức và hồi máu nổ trên chính mình, kỹ năng tấn công nổ phía đối thủ.

`[đo]` 42 hình khác nhau trên 42 kỹ năng. Tất cả chỉ dùng `transform` và `opacity` — hiệu năng không đổi: 0 khung rớt trên 270 khung khi nhạc và khung lễ cùng chạy.

## 2. Trang Nhà dựng lại theo bản vẽ

`[đo]` Thứ tự đo được: `hometime → stage → vitals → wishbox → acts → homefoot → receipt`

| Dải | Nội dung |
|---|---|
| **Giờ** | ☀️ 07:16 · Ngày 1 · trông quầy — biểu tượng đổi theo buổi, việc đọc từ lịch sinh hoạt |
| **Pet** | sân khấu tám khu như cũ, lời thoại nổi trên đó |
| **Hai chỉ số** | ❤️ Gắn bó · 😊 Tâm trạng, có thanh màu đổi theo mức |
| **Mong muốn** | thẻ pet nêu ý muốn, hai nút Đi cùng / Hôm nay bận |
| **Sáu nút** | Cho ăn · Chơi · Tắm · Ngủ · Rèn · Khám phá |
| **Dòng cuối** | pet nói một câu — ưu tiên nhận xét công việc, rồi mốc Cuốn đời, rồi chuyện gần |

Bảng chỉ số chi tiết (biên lai) đẩy xuống dưới cùng.

**Một lỗi tương phản phải sửa:** thẻ mong muốn nằm trên nền tối của trang Nhà chứ không nằm trong khung trắng, mà nó lấy màu chữ dành cho nền sáng — chữ tối trên nền tối. Đã cho nền kem riêng.

## 3. Lý do lai tạo tới đời ba bốn

Trước v1.0 mỗi đời chỉ cộng **1,5% trần tiềm năng** — quá nhỏ để ai buồn lai tạo lần thứ ba.

Nâng lên **3%**, và quan trọng hơn: **mỗi đời mở một thứ cụ thể**.

| Đời | Mở ra |
|---|---|
| F1 | Ký ức thừa hưởng — con mang 2 kỷ niệm của đời trước |
| F2 | Truyền thống dòng — dòng dõi có tính cách riêng |
| **F3** | **Ô kỹ năng thứ tư** — không cần Gắn bó 80 nữa |
| **F4** | **Chỗ tổ đội thứ ba** — ba pet phụ trợ thay vì hai |
| **F5** | **Sàn độ hiếm** — con không bao giờ ra Thường nữa |
| **F6** | **Sinh đôi** — 15% một lứa ra hai con |

Đời tính theo **cả nhà**, đọc từ sổ dòng dõi, nên thả pet không làm mất tiến độ.

`[đo]` F0: 3 ô kỹ năng, tổ đội 2 · F3: 4 ô · F4: tổ đội 3 · F5: sàn độ hiếm bật · F6: sinh đôi bật.

Bảng mở khoá hiện ngay đầu tab Gia phả.

## 4. Đổi tên và biểu tượng

**Pet Drink: Scale & Soul**, nhãn **v1.0** hiện cạnh tên pet trên đầu trang. Đổi ở tiêu đề trang, đầu trang, manifest PWA, service worker và thẻ chia sẻ.

Biểu tượng app vẽ mới: **pet loài Matcha** — thân giọt trà xanh dùng đúng đường dẫn của loài đó trong game, hai lá trên đầu, mặt hiền có má hồng, ba vệt hơi bốc lên để nhắc đây là đồ uống. Đặt trong khung bo tròn nền rừng, viền vàng mỏng nhắc lại màu giao diện.

## Ba lỗi trong lúc dựng

**1. Trùng tên `SK` — lần thứ năm.** `SK` đã là hàm dựng kỹ năng từ v4. Em đặt trùng cho hàm dựng hiệu ứng, và **cả khối mã không nạp được** — trang trắng hoàn toàn. Đổi thành `FXS`.

**2. Gỡ nhầm hàm vẽ.** Sau khi chèn bộ vẽ mới, em tìm hàm cũ để gỡ nhưng tìm sai phía, kết quả là gỡ mất hàm mới và giữ lại hàm cũ. Dữ liệu 42 hình đã đúng nhưng vẽ ra vẫn là hạt của bản cũ. `[đo]` Bộ test bắt được qua tên lớp CSS của hạt: `pfspark` thay vì `fxfly`.

**3. Phép vá im lặng không lưu.** Ba thay đổi về dòng dõi nằm trong một kịch bản, phép vá thứ ba không khớp nên `assert` dừng trước lệnh ghi file — **cả ba đều không được lưu** dù hai cái đầu đã khớp. Đúng loại lỗi đã ghi ở v29; lần này em phát hiện ngay vì có kiểm lại từng mục.

## Kích thước

| | v33 | v1.0 |
|---|---|---|
| index.html | 777 KB | 835 KB |
| Bộ PWA | 823 KB | **856 KB** |
| Trần | 6 MB | 6 MB |

`[đo]` Bộ kiểm tổng toàn bộ đạt. Bố cục đúng ở 390 / 820 / 1440px. Kiểm trùng tên sạch. Hiệu năng: trung vị 16,7 ms, tệ nhất 17,6 ms, **0 khung rớt trên 270 khung**.

## Còn treo sau v1.0

**Nối cầu nối với công cụ vận hành.** Hai mươi bốn bản rồi và vẫn chưa chạy thật lần nào. Mọi thứ đã sẵn sàng phía game: `handleOps()` nhận dữ liệu, pet có câu để nói, chương 6 của tuyến "Quán ta" chờ mốc doanh thu thật, 25 thẻ quản trị mở theo số nhiệm vụ. Chỉ thiếu đúng một việc — nhúng iframe và gửi `postMessage` từ công cụ sang.

**Cân lại sáu hành động chăm sóc.** Đo từ dữ liệu người dùng thật: Ngủ chiếm 72% số lượt, Rèn và Chơi gần như không ai dùng.

**Nhóm đối chứng cho bảng đo.** Cần vài ngày chỉ dùng công cụ mà không mở game, để biết mini game có thật sự làm tăng số nhiệm vụ vận hành hay không. Đây là câu hỏi gốc của cả dự án và vẫn chưa trả lời được.

---

# v1.0.1 — Lai tạo không chọn được bạn đời

Người dùng báo: có hai pet Trưởng thành, Gắn bó đều trên 60, mà vẫn không lai tạo được.

## Nguyên nhân

`breedUI()` luôn lấy **`S.stash[0]`** — con nằm đầu **mảng** chuồng, không phải con người chơi chọn. Nếu con đó là pet non, Automa, hay Gắn bó dưới 60 thì báo lỗi ngay, kể cả khi trong chuồng có con khác đủ điều kiện.

Tệ hơn: từ **v31** chuồng có **lọc và sắp xếp** (theo sức mạnh, độ hiếm, cấp, giai đoạn, loài). Thứ tự người chơi nhìn thấy khác hẳn thứ tự trong mảng. Nhãn nút ghi "Lai tạo với pet đầu chuồng" nên người chơi tưởng nó lấy con đang hiện đầu danh sách.

Và hàm **không loại trừ Linh hồn vùng** — chúng dùng thân Automa nên `isAutoma()` không bắt được.

## Sửa

Cho người chơi **chọn bạn đời**. Bảng liệt kê mọi pet đủ điều kiện, và với con chưa đủ thì **nói rõ thiếu gì**:

> Nhóc — chưa Trưởng thành
> AM-01 — Automa không lai tạo được
> Kem — Gắn bó 42/60

Thêm một dòng trả lời thẳng câu hỏi hay gặp: **không cần cùng loài**, con lấy loài của một trong hai bố mẹ.

`[đo]` Dựng đúng tình huống người dùng gặp — pet đầu mảng là pet non, hai con sau đủ điều kiện:
- Bảng mở, chọn được 2 bạn đời (Trà, Sữa)
- Nêu đúng lý do cho 2 con chưa đủ
- Lai Beano × Matcha ra con đời 1, ghi đúng tên bố mẹ

## Bài học

Đây là lỗi **do một thay đổi ở bản khác gây ra**. `S.stash[0]` vốn hợp lý khi chuồng hiện theo đúng thứ tự mảng. Bộ lọc thêm ở v31 làm giả định đó sai, nhưng không ai rà lại những chỗ còn đọc `S.stash[0]`.

**Khi đổi cách hiển thị một danh sách, phải rà mọi chỗ đang đọc theo chỉ số của danh sách đó.**

`[đo]` Bộ kiểm tổng toàn bộ đạt. Bố cục đúng ở ba kích thước. Hiệu năng: 0 khung rớt trên 270 khung.

---

# v1.0.2 — Ô tổ đội bị kẹt bởi id ma

Người dùng báo: chỉ xếp được **1 pet hỗ trợ** dù trần là 2.

## Nguyên nhân

Không phải trần sai. `S.team` lưu **id**, nhưng pet có thể rời chuồng bất cứ lúc nào — bị **đổi lên làm pet chính** (`swapPet`) hoặc bị thả.

Khi đó id thành **"ma"**: vẫn nằm trong `S.team` và **vẫn đếm vào trần**, nhưng `teamPets()` tìm trong chuồng không thấy nên không hiện ra.

`[đo]` Dựng lại đúng chuỗi thao tác:

| Bước | S.team | teamPets() |
|---|---|---|
| Xếp 2 pet phụ | 2 | 2 |
| Đổi một con lên làm pet chính | **2** | **1** |
| Thử thêm con khác | bị chặn | 1 |

Người chơi thấy 1 pet hỗ trợ, bấm thêm thì bị báo "tối đa 2" — trong khi màn hình chỉ có 1.

## Sửa

Thêm `teamClean()` — dọn id ma mỗi lần đọc: bỏ id trùng với pet chính và id không còn trong chuồng. Trần cũng đếm theo danh sách đã dọn. Chặn luôn việc xếp pet chính vào ô phụ trợ.

`[đo]` Sau khi sửa: bước 3 xếp được, `teamPets()` về lại 2.

## Bài học

Đây là lỗi **cùng họ với lỗi lai tạo ở v1.0.1**: cả hai đều là **tham chiếu tới một danh sách đã đổi mà không ai rà lại**.

- v1.0.1: `S.stash[0]` đọc theo **chỉ số**, còn danh sách thì đã được sắp xếp lại từ v31.
- v1.0.2: `S.team` đọc theo **id**, còn pet thì có thể rời chuồng bất cứ lúc nào.

**Mọi tham chiếu chéo giữa các danh sách pet (`S.pet`, `S.stash`, `S.team`) phải tự dọn khi đọc, không được tin là danh sách kia còn nguyên.**

`[đo]` Bộ kiểm tổng toàn bộ đạt. Bố cục đúng ở ba kích thước. Hiệu năng: 0 khung rớt trên 270 khung.

---

# v1.0.3 — Kiểm lần cuối, nhạc của bạn, tác giả

## Kiểm lần cuối: bộ `tfinal.py`

`tsmoke.py` chỉ đi các màn chính. Viết thêm `tfinal.py` đi qua **từng thao tác người chơi thật làm**: bốn hành động chăm sóc, nhận và từ chối mong muốn, gieo và thu hoạch, chạm ô đất khoá, pha và bán ly, mua nội thất / đồ pet / thời trang, ghép và bán trang bị, xếp tổ đội rồi đổi pet chính, lai tạo, mở bảng thông tin pet, đấu nhanh, leo 5 tầng, bắt đầu chuyến đi, nhận dữ liệu vận hành, phát nhạc.

`[đo]` Lần chạy đầu: **1 hỏng** — chạm ô đất khoá.

## Lỗi ô vườn — lần thứ ba, và lần này là nguyên nhân thật

Người dùng đã báo lỗi này hai lần. v31 và v33 em đều báo "đã sửa".

`[đo]` Đo bằng cú chạm qua **chấm chỉ khu thật** (không gọi hàm):

- Mỗi chấm chỉ khu là ô chạm **24×44px** (làm to cho dễ bấm ở một bản trước), dải chấm chiếm y 302–346.
- Ô đất ở y 282–326. **Chồng 24px** trên đúng bề ngang ô 3 đến 6.

**Vì sao hai lần sửa trước không ăn:** có một quy tắc `.gplots{bottom:22px}` nằm **sau** trong file — từ cùng đợt làm to vùng chạm. Đợt đó làm to **cả** chấm lẫn ô đất lên 44px và chúng tự đè lên nhau. Mọi bản sửa em viết phía trên đều bị quy tắc này ghi đè. Còn test v33 gọi `jumpZone` với thời gian chờ ngắn nên camera chưa tới nơi, ô đất chưa nằm dưới dải chấm — lỗi không lộ.

**Sửa lần đầu (sai):** đẩy ô đất lên 50px. Hết chồng, nhưng **ô đất lơ lửng giữa không trung và che mất pet**.

**Sửa đúng:** trả ô đất về mặt đất, **đưa dải chấm chỉ khu lên đỉnh sân khấu** — chỗ đó trống, nhãn tâm trạng ở trái, mặt trời ở phải.

`[đo]` Ở cả 390 / 820 / 1440px: chồng 0px, **8/8 ô bấm được**, chạm ô khoá thật mở đúng bảng, chấm vẫn đổi khu đúng (bấm 7 → 1 → 4 → 0 đều sáng đúng chấm).

**Bài học:** trước khi báo đã sửa một lỗi CSS, phải `grep` **mọi** quy tắc chạm vào phần tử đó. Quy tắc nằm sau thắng.

## Nhạc

Người dùng gửi video demo có ghép nhạc và muốn dùng làm nhạc nền.

**Không nhúng bài nhạc đó vào game.** Không rõ nguồn gốc — nếu lấy từ thư viện nhạc của ứng dụng dựng video hay nhạc thịnh hành thì giấy phép thường chỉ cho dùng trong video, không cho phát hành lại trong ứng dụng.

Thay vào đó làm hai việc:

**1. Nhạc của bạn** — trong Cài đặt, người chơi chọn một file nhạc (hoặc video, game lấy phần tiếng) trên máy. Game lưu trong **IndexedDB**, phát lặp làm nhạc nền. File không rời máy, không nằm trong bản phát hành. Có nút đổi bài, chuyển qua lại với nhạc có sẵn, và xoá.

Nếu máy không đọc được định dạng: **báo rõ và tự quay về nhạc có sẵn**, không im lặng.

`[đo]` Nạp file thật, phát, tắt thì dừng, nạp lại trang file vẫn còn. File hỏng: báo đúng câu, chuyển về nhạc có sẵn.

**Ghi chú môi trường test:** Chromium dùng để test **không có codec AAC** (`canPlayType` trả rỗng), nên file m4a/mov báo "đang phát" mà đứng ở giây 0. Kiểm lại bằng file Opus thì chạy tới giây 2,4. Trên Safari (iPad, iPhone) và Chrome/Edge máy tính, AAC phát bình thường.

**2. Chỉnh nhạc có sẵn theo đặc tính bài người dùng thích** — không chép giai điệu, chỉ theo nhịp, giọng và độ sáng.

`[đo]` Phân tích bài trong video: **117 BPM, giọng Sol trưởng, phổ trầm 6,9% · giữa 89,8% · cao 3,2%, trọng tâm 1553 Hz.**

Dò 12 tổ hợp trên bản dựng thử (3 dạng sóng × 2 mức trầm × 2 tần số cắt):

| | trầm | giữa | cao | trọng tâm | nhịp |
|---|---|---|---|---|---|
| Bài người dùng thích | 6,9 | 89,8 | 3,2 | 1553 Hz | 117 |
| Nhạc cũ (v32) | 26,8 | 71,1 | 2,1 | 1369 Hz | 88 |
| Thử tam giác | 50,3 | 49,6 | 0,1 | 863 Hz | 117 |
| **Nhạc mới** | **4,2** | **92,3** | **3,4** | **1699 Hz** | **117** |

Bất ngờ: **sóng vuông khớp nhất**. Nhạc cũ nghe khác không phải vì sóng vuông, mà vì **nhịp chậm 88, giọng La, và bè trầm quá to** (26,8% dải trầm). Nay: vòng G – D – Em – C, nhịp 117, bè trầm bằng 0,24 lần giai điệu, cắt 2400 Hz. Buổi tối chuyển sang Em – C – G – D chậm hơn.

## Tác giả

Thêm **Minh Đào · KCB SOL** vào hai chỗ:

- **Màn mở đầu** — ngay dưới tên game, và ở chân trang kèm số phiên bản.
- **Cài đặt → Về game** — tên, phiên bản, tác giả, đơn vị thực hiện, dòng "Định vị · Chiến lược · Vận hành".

## Kết quả

`[đo]` `tfinal.py` toàn bộ đạt · `tsmoke.py` toàn bộ đạt · bố cục đúng ở ba kích thước · 42/42 hiệu ứng khác nhau · lai tạo, tổ đội, nhạc, tác giả đều đạt · kiểm trùng tên sạch · hiệu năng trung vị 16,7 ms, **0 khung rớt trên 270 khung**.

---

# v1.1 — Mở dần theo ngày, thẻ chia sẻ, bản gọn cho điện thoại

## 1. Mở dần theo ngày

**Vấn đề:** ngày đầu người chơi thấy hết sáu tab dưới, bảy tab con trong Đấu, cộng tháp, vườn, bếp, trang bị — không biết bắt đầu từ đâu.

**Cách làm:** mở theo ngày **hoặc** theo tiến độ, cái nào tới trước. Người hăng hái không phải chờ, người bận không bị ngợp.

| Mục | Ngày | Hoặc sớm hơn khi |
|---|---|---|
| Nhà, Việc, Khác | 1 | luôn mở |
| **Đấu** (Đấu nhanh, Leo tháp) | 2 | làm xong 3 việc vận hành |
| **Shop** | 2 | chăm sóc 8 lần |
| **Trứng** | 3 | có quả trứng đầu tiên |
| Phiêu lưu | 3 | qua tầng 5 |
| Tổ đội | 3 | có pet thứ hai |
| Trang bị | 4 | có món trang bị đầu tiên |
| Quán | 4 | có ba pet |
| Thời trang | 5 | — |

Tab dưới chưa mở hiện **mờ kèm ổ khoá**, chạm vào thì nói rõ khi nào mở. Tab con chưa mở thì **ẩn hẳn**, thay bằng một nhãn "🔒 5 mục sắp mở" — bảy tab con là quá nhiều cho người mới.

Khi mở, pet giới thiệu bằng một câu của nó: *"Mình nghe nói có một cái tháp cao lắm. Đi thử không?"*

### Ba chỗ phải xử lý để không thành ngõ cụt

**Hướng dẫn ban đầu.** Bước 3 bảo *"mở Đấu rồi leo thử một tầng tháp"* — Đấu khoá ngày đầu thì hướng dẫn kẹt luôn. Đổi sang *"mở Việc — mỗi việc ở quán bạn làm xong là một ngày lớn lên của nó"*, hợp với tinh thần game hơn.

**Thẻ mong muốn** có thể rủ đi tháp, phiêu lưu, xem trứng. Lọc bỏ những mong muốn dẫn vào chỗ chưa mở.

**Mọi lối vào khác** (thẻ gợi ý, nút trong bảng, liên kết trong thông báo) đều đi qua hàm `go()` — chặn ở đó là phủ hết.

**Người chơi cũ không bị khoá lại.** Lần đầu chạy bản mới, mọi thứ đang mở được ghi là đã thấy — không bắn tám thông báo cùng lúc.

`[đo]` Người mới ngày 1: ba tab khoá, chạm không vào, có báo khi nào mở, mong muốn chỉ còn việc vận hành, hướng dẫn xong ở Việc. Làm 3 việc: Đấu mở ngay ngày 1, có thông báo. Tua ngày 2 → 5: mở đúng bảng trên, cả 8 mục đều được báo. Người chơi ngày 13: mở hết, không thông báo nào.

## Lỗi phát hiện trong lúc làm: thông báo đè nhau

Làm xong việc thứ ba: "Vừa mở Đấu" bật ra — rồi **1,4 giây sau bị thông báo thẻ quản trị đè mất**. Người chơi không kịp thấy.

Nguyên nhân gốc: `showBanner()` **thay luôn** thông báo đang hiện. Và việc định làm sau thông báo cũ — mở thẻ, mở hội thoại — **mất theo**. Va chạm này đã có thể xảy ra từ trước, ví dụ mốc gắn bó và thẻ quản trị cùng bật sau một nhiệm vụ.

Sửa: **thông báo xếp hàng**. Cái mới chờ tới khi màn hình trống — không thông báo, bảng hay hội thoại nào đang mở.

`[đo]` Người chơi thấy đủ và đúng thứ tự: "Vừa mở Đấu" → thẻ quản trị → thẻ mở ra để đọc.

**Một lỗi của chính bộ kiểm:** bước dọn dẹp xoá thẳng phần tử thông báo sau mỗi cú chạm, nên giết luôn thông báo đang muốn kiểm. Người chơi thật bấm "Tiếp tục" thì không có chuyện đó. Đã đổi bộ kiểm sang bấm như người thật và ghi quy tắc vào README.

## 2. Thẻ chia sẻ từ Cuốn đời

Nút **Tạo thẻ chia sẻ** ở đầu trang Cuốn đời. Vẽ bằng canvas, khổ **1080×1350** (dọc 4:5, vừa bảng tin Facebook):

- "CUỐN ĐỜI" · tên pet · loài · đời · dạng tiến hoá
- pet vẽ lớn giữa thẻ, có quầng sáng phía sau
- ba ô: ngày bên nhau · gắn bó · số mốc đã qua
- tối đa năm mốc lớn, xếp theo ngày — luôn có ngày gặp nhau, rồi ưu tiên tiến hoá, hạ boss, có em bé, mốc gắn bó
- chân thẻ: Pet Drink: Scale & Soul · MINH ĐÀO · KCB SOL

Trên iPhone và iPad, nút **Chia sẻ** mở thẳng bảng chia sẻ của hệ thống (Facebook, Messenger, Zalo, Lưu vào Ảnh). Máy không hỗ trợ thì chỉ có nút **Lưu ảnh**.

`[đo]` Ảnh đúng 1080×1350, ~870 KB. Hình pet vẽ lên ảnh đủ nét — 57 màu, không mất màu vì SVG của pet không dựa vào CSS của trang.

**Hai lỗi của lần vẽ đầu:** giãn chữ bằng cách chèn dấu cách làm **dấu tiếng Việt tách khỏi chữ** (Ố thành O´) — sửa bằng cách vẽ từng ký tự đã chuẩn hoá; và thứ tự ngày bị ngược — do **dữ liệu thử** tua ngày sai chiều, không phải lỗi thẻ.

## 3. Logo pet Matcha

Chữ **P** trong vòng tròn từ thời Pet Pocket đổi thành pet Matcha — cùng đường dẫn thân với loài Matcha trong game và với biểu tượng app. Có ở đầu trang và màn mở đầu.

## 4. Bản gọn cho điện thoại và iPad

**Trang Nhà:** gỡ hai nút bong bóng và cửa sổ nổi cùng ghi chú đi kèm. **Giữ chế độ ngủ đông** — đó là tính năng thật của người chơi.

**Cài đặt: từ 18 mục còn 12.** Gỡ 8 mục chỉ dùng trên máy tính hoặc lúc phát triển:

| Gỡ | Lý do |
|---|---|
| Trên máy tính | bản điện thoại |
| Ghi nhận sử dụng, Nhiệm vụ vận hành mỗi ngày, Lượt mở từng trang, Hành động chăm sóc | bảng đo đạc cho người phát triển |
| Cầu nối công cụ vận hành | chưa ghép |
| Lịch sử tài khoản | nhật ký gỡ lỗi |
| Chế độ thử | chỉ để thử nhanh khi phát triển |

Còn lại: Màu nền · Nhạc của bạn · Pet tự nói · Tra cứu · Hiệu ứng · Âm thanh · Mã pet · Đấu mã · Sao lưu · Hướng dẫn · Chơi lại · Về game.

**Mã đo đạc vẫn chạy ngầm** — phiên ghép cầu nối sẽ cần đúng dữ liệu đó để trả lời câu hỏi gốc: game có làm việc vận hành đều hơn không. Chỉ ẩn phần hiển thị. `DB.lean = false` để hiện lại.

## 5. Service worker — vấn đề ngầm phát hiện được

`sw.js` dùng tên bộ đệm **cố định `petpocket-v1`** suốt hơn 30 phiên bản, và **lấy bộ đệm trước cho mọi file**. Khi `sw.js` không đổi giữa hai bản — như từ v1.0.1 tới v1.0.3 — máy đã cài game **tiếp tục chạy bản cũ**, không nhận bản sửa lỗi.

Với một game sẽ còn cập nhật sau khi ghép cầu nối, phải sửa ngay:

- tên bộ đệm gắn số phiên bản — đổi bản là bộ đệm cũ bị xoá
- **trang chính lấy mạng trước**: có mạng thì luôn nhận bản mới nhất, mất mạng mới dùng bộ đệm
- ảnh và manifest vẫn lấy bộ đệm trước cho nhanh

`[đo]` Chạy qua máy chủ web thật:
1. Máy đã có bộ đệm `petpocket-v1` → cài bản mới → chỉ còn `petdrink-1.1.0`
2. Sửa trang trên máy chủ, nạp lại → **nhận bản vá ngay**
3. Tắt mạng, nạp lại → **game vẫn mở được**

**Khi phát hành bản sau: tăng `VER` trong `sw.js`.** Đã ghi vào đầu README.

## Kết quả

`[đo]` `tunlock.py` toàn bộ đạt · `tfinal.py` toàn bộ đạt · `tsmoke.py` toàn bộ đạt · bố cục đúng ở 390 / 820 / 1440px · 42/42 hiệu ứng · lai tạo, tổ đội, tác giả, nhạc đều đạt · kiểm trùng tên sạch · hiệu năng trung vị 16,7 ms, **0 khung rớt trên 270 khung**.

Bộ kiểm cũ đều khởi tạo người chơi ở ngày 1 — mà ngày 1 giờ Đấu khoá — nên cho chúng đóng vai người chơi lâu năm. Người chơi mới đã có `tunlock.py` kiểm riêng.

## Trước khi ghép cầu nối

Game đã ở trạng thái ổn định để ghép. Ba điều nên giữ khi sang phiên đó:

1. **Tăng `VER` trong `sw.js`** mỗi lần phát hành.
2. **Chạy đủ `audit.py`, `tsmoke.py`, `tfinal.py`, `tunlock.py`** trước khi đóng gói.
3. **Dữ liệu đo đạc đã tích luỹ ngầm từ bản này** — lấy ra bằng cách đặt `DB.lean = false`.

---

# v1.2 — Pet có tính cách thật, Album, Con đường, Nhà

## 1. Thẻ mong muốn hiện rõ phần thưởng

Theo mẫu người dùng vẽ: "Hôm nay {tên} muốn…" · dòng hành động có biểu tượng · câu nói của pet · chip phần thưởng · nhãn tính cách góc phải.

**Chỉ hiện chip nào là thật:**
- **+ Gắn bó** — luôn hiện, làm xong được +4
- **+ Kỷ niệm** — chỉ khi hôm nay chưa có kỷ niệm loại này
- **+ Xu** — chỉ với việc vận hành

Mỗi ngày tối đa **4 mong muốn có thưởng** — chặn cày gắn bó. Hết lượt thì thẻ nghỉ, trả chỗ cho thẻ gợi ý.

Sáu nút chăm sóc **giữ nguyên** — thẻ mong muốn là mục tiêu, sáu nút là công cụ dùng hằng ngày.

### Lỗ hổng từ v33 phát hiện được

Trước v1.2, **chỉ nhiệm vụ vận hành mới được thưởng** khi làm đúng mong muốn. Pet muốn ăn, muốn chơi, muốn đi xa — làm đúng việc đó cũng không được gì. Khi thẻ bắt đầu hiện "+Gắn bó · +Kỷ niệm" thì phải làm cho nó đúng, không thì thẻ hứa suông.

Nay mọi mong muốn có trường `done` chỉ hành động hoàn thành nó: việc vận hành, cho ăn, món ruột, chơi, tắm, ngủ, hái vườn, đi chuyến, qua tầng tháp, xem trứng, hoặc "ngay khi đồng ý" với mong muốn ở cạnh nhau.

### Hai lỗi logic — cùng một gốc

**Lỗi 1:** cho ăn xong, pet hết đói → game kiểm lại mong muốn, thấy hết hiệu lực → **đổi sang mong muốn khác** → rồi mới xét thưởng, so với mong muốn mới → không khớp. **Chính việc làm đúng đã xoá mong muốn trước khi kịp thưởng.** Sửa: xét đúng mong muốn người chơi đã nhận.

**Lỗi 2, chập chờn:** hàm thu hoạch tự vẽ lại màn hình ở cuối, việc vẽ lại đổi mong muốn trước khi phần thưởng chạy. Lúc qua lúc hỏng vì có lúc không tìm được mong muốn thay thế nên giữ nguyên cái cũ. Sửa: nhớ mong muốn vừa bị thay trong 60 giây.

`[đo]` Ăn · hái vườn · xem trứng · ngồi cạnh nhau đều được thưởng thật. **Bốn lần chạy liền đều đạt.** Thời gian thưởng: 2,3 giây nếu pet đứng sẵn ở bếp, gần 5 giây nếu ở khu xa — đi bộ thật.

## 2. Tính cách quyết định mong muốn

Bảng trọng số theo tính cách, cộng ba mong muốn chỉ tính cách đó mới có:

| Tính cách | Hành vi |
|---|---|
| **Tò mò** | Rủ khám phá nhiều gấp 3 lần pet lười |
| **Lười biếng** | **Khoảng 20–30% lần từ chối Rèn**, nghiêng về ngồi và ngủ |
| **Gan dạ** | Muốn đấu kẻ canh giữ tầng kế tiếp |
| **Nhút nhát** | *"Hôm nay mình hơi sợ. Bạn ở cạnh mình một lát nhé?"* |
| **Tham ăn** | Tự nhắc giờ ăn vào 6–8h, 11–13h, 17–19h |
| Trung thành | Nghiêng về việc vận hành |
| Nghịch ngợm | Rủ chơi, rủ ra vườn |
| Điềm tĩnh | Muốn ngồi cạnh nhau |
| Bướng bỉnh | Muốn leo tháp, đánh boss |
| May mắn | Rủ xem trứng, ra vườn |

**Giới hạn cho pet lười:** chỉ từ chối **Rèn**, không bao giờ từ chối ăn, tắm, ngủ, chơi hay chữa bệnh, và **không từ chối hai lần liền** — người chơi thử lại lần nữa là được. Từ chối không trừ gì.

`[đo]` 500 lần chọn mỗi tính cách: gan dạ ra "đánh boss" nhiều nhất, nhút nhát ra "ở cạnh mình" nhiều nhất, tham ăn đúng giờ ăn ra "tới giờ ăn" 281/500. Lười từ chối Rèn 76/400 lần, không lần nào liền hai; tính cách khác không từ chối.

## 3. Album cuộc đời

Trang Cuốn đời mở bằng **Album** — tối đa 10 khoảnh khắc lớn, mỗi loại lấy lần đầu tiên: Gặp nhau · Trưởng thành · Tiến hoá · Thắng kẻ canh giữ đầu tiên · Chuyến đi đầu tiên · Có em bé · Gắn bó trọn vẹn (chỉ mốc 100) · Gặp linh hồn vùng · Quán qua một chương · Có góc riêng. Mỗi khoảnh khắc có một câu của pet.

Vẫn chuyển được sang **Dòng thời gian** đầy đủ.

Pet nhắc lại khoảnh khắc lớn: *"Bạn còn nhớ ngày mình mới nở không?"* · *"Nhớ lần đầu mình thắng kẻ canh giữ không? Mình vẫn còn run."* Pet đời một trở đi còn nhắc ký ức thừa hưởng: *"Bố mẹ mình từng kể về chuyện…"*

### Hai lỗi dữ liệu sửa kèm

**Ngày gặp nhau ghi sai.** Ảnh thẻ người dùng gửi ghi *"Ngày 12 · Gặp Tủn"*, trong khi gặp từ ngày 1. Cuốn đời có từ v33, lúc cài bản đó game ghi mốc bằng ngày hiện tại. Nay tính từ ngày pet ra đời, và **tự sửa lại** cho tiến độ cũ.

**Cuốn đời đầy thì mất mốc Gặp nhau.** Giới hạn 40 mốc, đầy thì bỏ mốc cũ nhất — tức là mốc "Gặp nhau" bị đẩy ra đầu tiên. Nay bỏ mốc cũ nhất **không nằm trong album**.

## 4. Con đường (Life Path)

Sáu thẻ theo mẫu người dùng vẽ: Chăm sóc · Chiến · Trí · Lữ Hành · Đồng Hành · Linh Hồn, mỗi thẻ màu riêng, biểu tượng, phần trăm, thanh tiến trình và một dòng gợi ý — **không hiện con số điều kiện**. Có ở bảng chi tiết pet chính và bảng thông tin pet trong chuồng. Nhánh Ẩn không hiện.

### Thanh tiến trình sẽ nói dối nếu chỉ thêm giao diện

- **Nhánh Chăm sóc trước đây không đo gì** — nó là nhánh mặc định, con nào không đủ điều kiện nhánh khác thì rơi vào. Nay đo bằng số lần chăm sóc.
- **Game chọn nhánh đầu tiên đủ điều kiện theo thứ tự cố định**, không phải nhánh cao nhất. Người chơi thấy Chăm sóc 72%, Chiến 38% nhưng nếu Chiến vừa chạm ngưỡng thì pet vẫn thành dạng Chiến. Nay **con đường cao nhất thắng**.
- **Đồng Hành và Lữ Hành trước đây đếm chung toàn game**, không theo từng pet. Nay mỗi pet có lịch sử riêng; pet chính nhận số liệu cũ khi cài bản này.

100% bằng đúng ngưỡng cũ, nên cân bằng không đổi.

`[đo]` Đặt từng con đường cao nhất → tiến hoá ra đúng con đường đó (Chiến, Chăm sóc, Đồng Hành). Tiến hoá thật qua `checkStage` ra đúng con đường cao nhất.

## 5. Nhà — tính cách gốc của mỗi loài

| Nhà | Tính cách gốc |
|---|---|
| Beano | Tò mò — *không đứng yên được, cái gì lạ cũng muốn xem* |
| Milku | Trung thành — *ở đâu thì ở cạnh người đó* |
| Matcha | Điềm tĩnh — *không vội, pha trà cũng vậy* |
| Cacao | Gan dạ — *đắng, và không lùi* |
| Citrus | Nghịch ngợm — *chua một chút, vui nhiều chút* |
| Glacio | Bướng bỉnh — *lạnh ngoài, bền trong* |

Ghi chú: đề xuất gốc nhắc "Nhà Latte" — game không có loài này, loài sữa là **Milku**.

Từ **đời một**, con mang nhãn nhà, và **khoảng một nửa nhận luôn tính cách gốc**. Vì tính cách quyết định mong muốn (ý 2), nhà Beano sẽ sinh ra nhiều con hay rủ đi khám phá — **dòng họ có hành vi riêng thật**, không chỉ là nhãn.

`[đo]` 120 lứa lai Beano: 120/120 mang nhãn nhà, 75/120 nhận tính cách Tò mò.

## Thẻ chia sẻ và màn mở đầu

Theo yêu cầu: bỏ dòng "Minh Đào · KCB SOL" dưới tên game ở màn mở đầu và ở thẻ chia sẻ. Tác giả **chỉ còn ở cuối Cài đặt → Về game**.

Thẻ chia sẻ trước đây: dòng mốc thứ 5 **đè lên tên game** ở chân thẻ — trên iPad chữ to hơn máy thử. Nay chân thẻ chỉ còn tên game, đẩy xuống thấp hơn, và danh sách mốc lấy từ **Album** (khoảnh khắc lớn nhất) thay vì mốc gần nhất.

## Kết quả

`[đo]` `tv12.py` toàn bộ đạt, bốn lần liền · `tfinal.py` · `tsmoke.py` · `tunlock.py` toàn bộ đạt · bố cục đúng ở ba kích thước · 42/42 hiệu ứng · kiểm trùng tên sạch · hiệu năng trung vị 16,6 ms, **0 khung rớt trên 270 khung**.

**Ba lỗi của chính bộ kiểm** phát hiện trong phiên này: bấm dồn 0,09 giây khi một lượt chăm sóc mất 2,6 giây (đếm "chưa xong" thành "bị từ chối"); chờ cố định 3,8 giây khi pet ở khu xa cần gần 5 giây; và kiểm "gắn bó có tăng" — mà thu hoạch tự nó đã tăng gắn bó nên báo đạt sai. Đã đổi sang đo trực tiếp và chờ tới khi xong.

## Phiên sau: hệ sự kiện

Người dùng **đồng ý ký mã** để chặn mã giả, chấp nhận giữ một file khoá riêng.

---

# v1.3 — Hệ sự kiện có ký mã

Người dùng đồng ý ký mã để chặn mã giả, chấp nhận giữ một file khoá riêng.

## Ba phần, ba nơi

| Phần | Nơi |
|---|---|
| **Khoá bí mật** `pet-drink-KHOA-BI-MAT-minhdao-2026.json` | Chỉ trên máy tác giả, có bản sao lưu. Không bao giờ nằm trong gói game. |
| **Trang tạo mã** `phat-hanh-su-kien.html` | Gói công cụ riêng. Không chứa khoá. |
| **Game** | Chỉ chứa khoá **công khai** — kiểm được chữ ký, không ký được. |

Khoá được tạo **ngoài thư mục game ngay từ đầu**, để không có cách nào vô tình đóng gói nó.

## Lõi dùng chung

Một đoạn mã chép **y hệt** vào cả game và trang tạo mã: kiểm dữ liệu, mã hoá, ký, kiểm chữ ký. Trang tạo mã báo hợp lệ thì game chắc chắn nhận.

**Chữ ký:** ECDSA P-256 với SHA-256, qua WebCrypto — chuẩn trình duyệt, không cần thư viện ngoài. Mã có dạng `PDE1.<dữ liệu>.<chữ ký>`. Một sự kiện khá đầy đủ ra mã khoảng 1.000–1.400 ký tự — dán qua Zalo, Messenger thoải mái.

**Mã chỉ chứa dữ liệu, không chứa lệnh.** Nếu mã chạy được lệnh, ai chia sẻ một mã độc là xoá được tiến độ người chơi. Nên mã chỉ chứa những loại nội dung định sẵn:

- Tên, giới thiệu, thời gian bắt đầu và kết thúc (giờ thật)
- Quà khi nhập mã
- Nhiệm vụ đếm theo 10 loại việc thật: chăm sóc, cho ăn, việc vận hành, qua tầng tháp, đi chuyến, thu hoạch, pha ly, bán ly, thắng trận, hạ boss sự kiện
- Mong muốn của pet trong sự kiện, hoàn thành bằng 10 loại hành động
- Câu pet tự nói
- Công thức đồ uống — **giữ mãi** sau khi sự kiện hết
- Một boss sự kiện, dựng theo sức mạnh pet của từng người chơi như boss vùng

**Mọi con số có trần**, kể cả mã do chính tác giả ký — phòng gõ nhầm: 3.000 xu, 5 vé tháp, 3 lượt đi, 5 hạt kinh nghiệm, 10 hạt mỗi loại, tăng chỉ số 20%. Trang tạo mã tự hạ và báo lại.

**Mọi chữ bị thoát HTML khi hiện ra** — tên sự kiện có thẻ `<img onerror=…>` chỉ hiện thành chữ.

`[đo]` Kiểm riêng lõi: sửa số xu trong mã → bị bắt · khoá khác tự ký → bị bắt · mã rác, mã dán thiếu, mã quá dài → bị bắt · 99.999 xu hạ về 3.000 · mục tiêu lạ, nguyên liệu lạ, loài lạ, sự kiện trống, dài quá 62 ngày → bị từ chối.

## Trong game

- **Khác → Cài đặt → Sự kiện**: ô dán mã. Kiểm chữ ký rồi kiểm dữ liệu, báo rõ lý do nếu từ chối.
- **Việc → Sự kiện**: tab chỉ hiện khi có sự kiện đang hoặc sắp diễn ra, hoặc vừa hết mà còn quà chưa nhận. Mỗi sự kiện một thẻ: đếm ngược, quà, nhiệm vụ có thanh tiến độ, boss và số lượt còn lại.
- **Đường dẫn** `…/index.html#su-kien=PDE1.…` — mở là game tự nhập mã, rồi xoá mã khỏi thanh địa chỉ.
- Mong muốn sự kiện được **ưu tiên gấp 4** khi đang diễn ra, câu nói sự kiện chen vào lời pet **30%** số lần.
- **Cập nhật:** cùng mã định danh, số bản cao hơn → nội dung được thay, tiến độ và quà đã nhận giữ nguyên. Cùng bản → báo "đã có".

## Trang tạo mã

Bốn bước thật sự tuần tự nên đánh số: nạp khoá → soạn → ký và phát hành → lưu và kiểm tra. Bên phải là **phiếu sự kiện** bám theo, cập nhật khi gõ, báo lỗi đỏ và chỗ tự điều chỉnh vàng.

Thứ duy nhất được làm nổi bật: **con dấu đỏ "ĐÃ KÝ"** đóng lên phiếu khi ký — chữ ký số chính là con dấu. Sửa bất cứ gì sau khi ký thì con dấu biến mất và mã bị xoá, để không gửi nhầm mã cũ.

Nạp khoá thì trang **so với khoá công khai trong game** và báo "khớp với game", hoặc cảnh báo nếu là khoá khác. Khoá chỉ nằm trong trang lúc đang mở, không lưu lại ở đâu.

Có: lưu và mở bản nháp · dán một mã bất kỳ để xem nó chứa gì · mở mã cũ để sửa (tự tăng số bản) · tạo cặp khoá mới khi mất hoặc lộ khoá.

`[đo]` Không tràn ngang ở iPhone, iPad dọc, iPad ngang; mọi nút cao ít nhất 44px.

## Kiểm trọn vòng

`tev.py` mở trang tạo mã, nạp file khoá, **điền biểu mẫu bằng thao tác thật**, ký, rồi dán mã vào game và chơi: nhận quà, làm việc vận hành và cho ăn để đủ nhiệm vụ, nhận thưởng, mong muốn và câu nói sự kiện xuất hiện, pha công thức sự kiện, **đấu và thắng boss sự kiện**, nhập lại, cập nhật lên bản 2, thử giả mạo, thử chèn HTML, sự kiện sắp tới và đã qua, nạp lại trang, mở bằng đường dẫn.

`[đo]` Toàn bộ đạt.

## Một bài kiểm tự lừa mình — phát hiện và sửa

Khi kiểm khoá bí mật không lọt vào gói, lệnh tìm kiếm đầu tiên báo **"sạch"** — nhưng sai. Phần bí mật của khoá bắt đầu bằng dấu gạch ngang (`-_0…`), lệnh tìm kiếm hiểu nhầm là một tuỳ chọn và báo lỗi, mà lỗi thì rơi vào nhánh "sạch".

Kiểm lại bằng cách đọc thẳng từng file: quét 26 file, sạch. Và **chứng minh bài kiểm bắt được thật** bằng một file thử có chứa khoá.

Thêm vào `audit.py` một lớp chặn: phát hiện khoá bí mật trong `index.html` thì dừng với mã lỗi 2. `[đo]` Nhét thử khoá vào bản sao → mã thoát 2; bản thật → mã thoát 0.

## Giới hạn phải nói rõ

**Giờ lấy theo máy người chơi.** Chỉnh giờ máy là vào sự kiện sớm hoặc trễ được. Không có máy chủ thì không chặn triệt để.

**Mã dùng chung.** Một mã cho mọi người chơi — đúng thiết kế. Mỗi sự kiện chỉ nhận quà một lần trên một bản lưu; người chơi xoá tiến độ chơi lại thì nhận lại được.

**iPhone, iPad:** game thêm ra màn hình chính dùng dữ liệu riêng, tách với Safari. Bấm đường dẫn sẽ mở Safari — với người chơi bằng biểu tượng, gửi mã để dán thì chắc hơn.

**Trang tạo mã trên iPad** nên mở qua đường dẫn https; mở thẳng file trong ứng dụng Tệp thường không chạy được lệnh.

## Kết quả

`[đo]` `tev.py` · `tsmoke.py` · `tfinal.py` · `tunlock.py` · `tv12.py` toàn bộ đạt · lõi sự kiện 19/19 · bố cục đúng ở ba kích thước · 42/42 hiệu ứng · kiểm trùng tên và kiểm khoá sạch · hiệu năng trung vị 16,7 ms, **0 khung rớt trên 270 khung**.

---

# v1.4 — Mã hình, mã quà tặng, key mở game

Người dùng chốt: **key theo khách hàng, có hạn dùng**; **pet sự kiện khác loại, mạnh ngang Automa tốt nhất, không hơn**; quà sự kiện chia theo thang.

## Lõi dùng chung bản 2

**Ba loại mã** — sự kiện `PDE`, quà `PDG`, key `PDK` — số 1 là thường, số 2 là đã nén.

**Loại mã nằm trong phần đã ký.** Tiền tố ở đầu mã không được ký — ai đó có thể đổi `PDE` thành `PDK` để thử dán mã sự kiện vào ô key. Ghi loại vào phần ký thì trò đó bị bắt: *"Loại mã không khớp — mã đã bị đổi tiền tố."* Mã sự kiện v1.3 chưa có trường này vẫn được nhận.

**Nén:** trên 2.500 byte thì nén (deflate), chữ ký luôn đặt trên dữ liệu **chưa nén**. Chặn bom nén: giải nén quá 400 KB thì dừng. `[đo]` Mã nén 20 MB giả bị chặn trong 9 ms.

**Lỗi tìm thấy khi kiểm:** lần đầu chặn bom nén, lệnh huỷ luồng trả về một lỗi không ai bắt — trên máy thử làm sập tiến trình. Đã bắt lại.

**Một bài kiểm đạt vì lý do sai:** bài "đổi tiền tố" lần đầu thay `^PDE2` trong một mã thật ra là `PDE1` — không đổi gì, và tình cờ đạt. Đã sửa để đổi thật và kiểm đúng câu báo lỗi.

## Mã hình

Chỉ nét vẽ và màu. Nét vẽ chỉ nhận chữ lệnh vẽ, số, dấu cách, phẩy, chấm, trừ — không có dấu nháy hay dấu `< >`, nên không thể chèn thẻ hay lệnh. Game tự dựng hình bằng khuôn của nó.

| Loại | Vẽ theo |
|---|---|
| **Pet, boss** | Đúng ba lớp của pet thường: lớp sau lưng (tai, cuống, cánh), thân tô màu theo gen, hoa văn cắt vừa trong thân, cộng lớp trước. Pet sự kiện hưởng nguyên mặt, cảm xúc, chuyển động sẵn có. |
| **Thời trang** | Bốn ô mũ · áo · cầm tay · khoác sau lưng, mỗi ô một vùng vẽ cố định theo thân pet |
| **Khung lễ** | Màu viền, hình góc (góc phải tự lật gương), hạt rơi |

`[đo]` Chèn `<script>` vào nét vẽ, dấu nháy vào nét vẽ, CSS vào màu — đều bị chặn hoặc đổi về không màu.

**Lỗi nhìn thấy:** boss sự kiện bị ánh cầu vồng trong khi hình vẽ màu cam. Pet sinh ra luôn bốc ngẫu nhiên đặc điểm gen, và "óng ánh" đè lên màu của hình. Pet và boss sự kiện nay bỏ đặc điểm gen — giữ đúng màu người vẽ.

## Pet sự kiện

Bảy tác dụng, **con số do game cố định**, không để mã tự đặt:

| Tác dụng | Mức |
|---|---|
| Hộp bí ẩn mở thêm một món | +1 món |
| Xu từ việc vận hành | +15% |
| Rác sinh ra | −30% (như AM-06) |
| Rơi trang bị trên tháp | +35% (như AM-07) |
| Hồi máu sau mỗi tầng | 12% (như AM-08) |
| Tinh thần pet chính hao chậm hơn | 25% |
| Thu thêm nông sản mỗi lần hái | +2 |

Có cùng tác dụng với một Automa thì **lấy cái mạnh hơn, không cộng dồn** — giữ đúng lời hứa "ngang Automa tốt nhất". `[đo]` AM-06 cộng pet sự kiện giảm rác: vẫn 30%, không phải 60%.

Chỉ đứng ô phụ trợ, không làm pet chính, không lai tạo, không tiến hoá. Loài sự kiện đăng ký vào danh sách loài nhưng **không vào danh sách nở trứng** — trứng thường không bao giờ nở ra pet sự kiện.

## Phần thưởng mới, thang quà, danh hiệu

Phần thưởng thêm: **trứng, pet sự kiện, thời trang sự kiện, khung lễ sự kiện**. Thang quà theo số nhiệm vụ đã xong. Đủ bộ thời trang của sự kiện thì nhận danh hiệu, hiện trong phòng thay đồ.

### Ba lỗ phát hiện khi nối

- **Lỗi ngầm của v1.3:** game lưu quyền sở hữu khung lễ dưới dạng `frame:` + mã, còn phần thưởng khung ở v1.3 cộng mã trần — **nhận khung xong vẫn không dùng được**. Bài kiểm v1.3 không thử phần thưởng khung nên không lộ.
- **Đồ sự kiện lọt ra ngoài:** phòng thay đồ liệt kê mọi món kèm nút mua (đồ sự kiện giá 0 xu — nhặt miễn phí), hộp bí ẩn bốc thời trang từ mọi món chưa có.
- **Cửa hàng khung lễ không kiểm mùa khi mua**, chỉ kiểm đủ xu — khung sự kiện 0 xu mua được. Và mua thời trang sự kiện chưa mở thì **sập**, vì hàm đọc tên khung lễ yêu cầu mà đồ sự kiện không có.

Chặn ở cả chỗ hiện lẫn trong hàm mua: đồ sự kiện chỉ "mở" khi đã có, nên hộp bí ẩn tự loại ra; phòng thay đồ và cửa hàng khung chỉ hiện món sự kiện đã có; hàm mua từ chối món sự kiện.

## Mã quà tặng

**Mã chung** một mã cho mọi người, mỗi máy nhận một lần. **Mã riêng** gắn với **mã người chơi** (dạng `XXXX-XXXX`, xem ở Cài đặt) — dán sang máy khác bị từ chối. Có hạn nhận tuỳ chọn. Phần thưởng mã quà không chứa được đồ sự kiện (không có hình trong mã quà).

## Key mở game

Theo khách hàng, có hạn dùng hoặc không hết hạn. Màn khoá phủ lên toàn game khi mở lần đầu trên máy mới.

- **Người đã qua màn mở đầu từ bản trước được miễn** — không khoá chính tác giả và người đang thử.
- Hết hạn: khoá lại, **tiến độ còn nguyên**, nhập key mới là chơi tiếp. Còn 7 ngày thì nhắc.
- Cài đặt ghi bản quyền: tên khách hàng và hạn dùng.

Giới hạn phải nói rõ: **khoá cửa, không phải két sắt** — game là một file HTML, người biết kỹ thuật gỡ được đoạn kiểm. Ngày hết hạn tính theo giờ máy người chơi.

## Một ô nhập cho cả ba loại mã

Khác → Cài đặt → **Nhập mã**. Game tự nhận biết loại. Dán nhầm loại thì báo đúng: *"Đây là key mở game, không dùng ở đây."*

## Công cụ phát hành ba thẻ

Một trang, dòng trên cùng nạp khoá dùng chung, ba thẻ **Sự kiện · Quà tặng · Key mở game**.

- **Sự kiện:** thêm bước **Hình vẽ** — dán mã hình, xem trước ngay (thời trang hiện trên bóng thân pet để thấy vừa hay không), chọn tác dụng cho pet. Hình đã thêm hiện trong mọi ô chọn phần thưởng. Thang quà, danh hiệu, boss dùng hình riêng.
- **Quà tặng:** phiếu ghi rõ mã chung hay mã riêng cho ai.
- **Key:** mặc định dùng một năm. **Sổ key đã cấp** lưu trên trình duyệt để theo dõi hạn, key hết hạn tô đỏ.
- Ô **Kiểm một mã** nhận cả ba loại.

## Một bài kiểm giả — tự bắt được

Trong bộ kiểm công cụ, mục "mặc định kéo dài 30 ngày" em viết là `ck(…, True)` — **luôn đạt dù đúng hay sai**. Đã sửa để đo thật khoảng cách giữa hai ngày, và quét mọi bộ kiểm: không còn bài nào kiểu luôn-đạt.

## Kết quả

`[đo]` Lõi 30/30 · `tv14.py` 50/50 (key, mã quà, sự kiện có hình, pet sự kiện, nạp lại) · `tmaker.py` 36/36 (công cụ ba thẻ → game) · `tev.py` toàn bộ đạt — **mã ký bằng công cụ cũ v1.3 vẫn dùng được** · `tsmoke` · `tfinal` · `tunlock` · `tv12` toàn bộ đạt · bố cục game và công cụ đúng ở ba kích thước · kiểm trùng tên và kiểm khoá sạch · hiệu năng 0 khung rớt.

## Phiên sau: bộ Halloween

Em vẽ: boss, pet Bí Ngô, bốn món thời trang, khung lễ — gửi một mã hình. Để sự kiện kết thúc đúng 31/10 và kéo dài một tháng, nên phát mã quanh **1/10**.

---

# v1.5 — Việc theo giờ thật, chuồng và kho, hạt kinh nghiệm, bộ Halloween

## Việc ngày, tuần, tháng theo thời gian thật

Người dùng yêu cầu: không được tick trước để nhận xu và vật phẩm.

`[đo]` Lỗi thật: việc tuần, tháng **mỗi lần chạm cộng một bước, không giới hạn**. Chạm 5 lần liền "Kiểm kho 3 lần trong tuần" là xong. "Kiểm kê tồn kho cuối tháng" — 450 xu và một trứng cổ — nhận được ngay ngày 1. Việc cuối ngày tick được từ sáng sớm.

Quy tắc mới:

| Quy tắc | Áp dụng |
|---|---|
| Tối đa **một lần mỗi ngày** | Mọi việc tuần, tháng |
| Ghi nhận **từ 17:00** (đổi ở Cài đặt, 12–22 giờ) | Việc cuối ngày: nhập P&L, kiểm kho cuối ngày, đạt doanh thu, đóng ca; và bốn việc tuần tương ứng |
| Mở **từ ngày 25** | Chốt P&L tháng, kiểm kê cuối tháng, đánh giá KPI |
| Bất kỳ lúc nào | Mở ca, chấm công, cập nhật giá vốn, đào tạo nội bộ |

Dòng việc đang khoá hiện mờ và ghi rõ lý do: *"Việc cuối ngày — ghi nhận từ 17:00"*, *"Hôm nay đã ghi nhận — mai ghi tiếp"*.

`[đo]` Đồng hồ trình duyệt đặt ở giờ Việt Nam: 9 giờ không tick được Đóng ca, 18 giờ được; chạm 5 lần chỉ tính 1; kiểm kho ba ngày 14, 15, 16 đủ 3/3; ngày 14 chưa mở kiểm kê cuối tháng, ngày 26 mở và nhận trứng cổ.

## Chuồng và Kho tách riêng

Trang Trứng có ba thẻ: **Lò ấp · Chuồng · Kho**. Chạm vào pet đang nuôi giờ cũng mở được bảng.

Lỗi nhỏ tìm ra khi tách: mục thẻ công thức hiện **mã nội bộ** (`cam_muoi`) thay vì tên đồ uống, và ghi chú lỗi thời *"dùng để chế đồ uống ở bản sau"* trong khi bếp đã chạy từ lâu.

## Cho ăn hạt kinh nghiệm, thấy trước lên cấp mấy

Trong bảng thông tin của mọi pet: chọn số hạt bằng − / + / Tối đa, thấy ngay *"Cấp 16 (40%) → Cấp 19 (12%) · +3 cấp"*. Mô phỏng đúng cách game cộng kinh nghiệm, kể cả hệ số khi pet đang ốm.

Trước đây chỉ pet chính dùng được hạt, với hai nút "Dùng 1" và "Dùng tất cả" không báo gì. **"Dùng tất cả" khi pet gần cấp 30 làm phí trắng phần dư.** Nay game không cho chọn quá số hạt cần để chạm cấp 30.

`[đo]` Pet cấp 29 cần đúng 49 hạt; 48 hạt chưa tới, 49 hạt chạm cấp 30, không cho chọn 50.

## Trứng vàng

Ba nguồn: hộp vàng (18% mỗi lượt bốc, khoảng 63% mỗi hộp có ít nhất một), lai hai pet từ Cực hiếm trở lên (con nở theo tỉ lệ trứng vàng), và đủ 100% Sổ sưu tầm (mở bán trong cửa hàng).

**Nguồn thứ ba chưa từng chạy:** trứng vàng để trống giá, mà cửa hàng chỉ hiện trứng có giá. Nay giá **3.000 xu**. Danh sách nguồn trứng trong lò ấp cũng được viết lại cho đúng.

## Pet sự kiện có thoại (ý 5)

Ba câu, nằm trong mã hình của pet — tác giả tự viết ở công cụ phát hành, không phải sửa game mỗi mùa:

- **Vào tổ đội** — pet sự kiện nói
- **Sau trận thắng có pet sự kiện** — pet chính khen (`{pet}` thay bằng tên). Tối đa 5 phút một lần, không lặp khi leo tháp liền
- **Đủ bộ thời trang** — pet sự kiện nói trong thông báo danh hiệu; chưa có pet thì pet chính nói thay

Để trống thì dùng câu mặc định.

`[đo]` Trận đấu thật có Bí Ngô trong tổ đội: thắng, pet chính khen đúng câu; thắng trận thứ hai liền sau: không lặp.

## Bộ Halloween 2026

Theo đúng cốt truyện Quy mô đối Tâm hồn:

| Hình | Ý tưởng |
|---|---|
| **Boss Bí Ngô Hương Liệu** | Siro vị bí ngô công nghiệp — "mùa thu đóng chai". Vòi bơm siro thay cuống, nhãn dán ngang thân, siro nhỏ giọt |
| **Pet Bí Ngô** | Quả bí thật: cuống, lá, tua cuốn, gân thân |
| Mũ phù thuỷ | Vành rộng, chóp gập, dải cam, khoá vàng, ngôi sao |
| Khăn choàng | Sọc cam tím, một đuôi thả tua |
| Giỏ kẹo bí ngô | Khắc mặt, kẹo xanh hồng ló ra |
| Cánh dơi | Hai bên thân, có gân cánh |
| Khung Đêm Halloween | Mạng nhện ở góc, dơi con treo, dơi rơi |
| **Công thức Ca cao gừng thật** | Ca cao, gừng, sữa tươi — gia vị thật đánh bại hương liệu |

`[đo]` Vẽ bằng đúng bộ vẽ của game: đồ đội vừa bốn dáng thân khác nhau — giọt Matcha, hạt Beano, cốc Milku, quả bí. Chỉnh một chỗ sau khi nhìn: dơi quá tối, trên nền quán ban đêm gần như mất hình — thêm viền tím nhạt.

Mã hình 2.901 ký tự. Bản nháp sự kiện điền sẵn: 7 nhiệm vụ, thang 6 mốc (khung → 4 món thời trang → Bí Ngô ở mốc 7), 2 mong muốn, 8 câu nói, boss 3 lượt mỗi ngày. Ký xong khoảng 4.700 ký tự.

`[đo]` Chơi thử trọn sự kiện: nhập mã 28/9 thấy đếm ngược, chưa nhận quà được; ngày 5/10 nhận quà, mong muốn và câu nói Halloween xuất hiện, nhận đủ 7 nhiệm vụ và 6 mốc, danh hiệu, pet Bí Ngô, ba câu thoại, đấu boss; ngày 1/11 sự kiện kết thúc, đồ, khung, pet, công thức vẫn giữ.

## Lỗi của chính bộ kiểm — phát hiện và sửa

- **Múi giờ:** trình duyệt thử chạy giờ UTC, nên 18:00 giờ Việt Nam thành 11:00. Bài "9 giờ sáng bị chặn" đạt vì lý do sai — nó đang chạy lúc 2 giờ sáng UTC. Nay đặt múi giờ Việt Nam và kiểm giờ trước khi tin các bài giờ giấc.
- **Chữ in hoa:** tiêu đề mục có kiểu chữ in hoa, cách đọc chữ trên màn hình trả về "KHO VẬT PHẨM" — bài "thẻ Chuồng không có kho" đạt dễ dãi. Nay đọc chữ gốc.
- **Trứng vàng:** tìm chữ "Trứng vàng" luôn thấy vì có sẵn trong danh sách nguồn trứng. Nay tìm đúng nút mua.
- **Kết quả trận giả:** thiếu dữ liệu nên hàm phát trận báo lỗi trước khi tới phần thoại, lỗi bị kịch bản nuốt. Nay dùng trận đấu thật.
- **Hai ô trùng tên lớp** trong Cài đặt — lỗi của em trong code, không phải kịch bản. Đã đặt tên riêng.

### Bài học lớn nhất: bộ kiểm phụ thuộc giờ chạy

Quy tắc giờ giấc mới làm các bộ kiểm cũ đạt hay hỏng tuỳ lúc chạy. Chúng vừa đạt chỉ vì máy thử đang ở 21 giờ ngày 27. Chạy lại lúc 9 giờ sáng: `tunlock`, `tev`, `tv14` hỏng — chúng bấm việc cuối ngày để làm tiến độ cho thứ khác. Bảng tổng kết "Hết một ngày" tự mở buổi tối cũng từng che nút trong một bộ.

Sửa: các bộ không kiểm giờ giấc đặt `S.qset={eod:0}`. Thêm `chay-buoi-sang.py` chạy bất kỳ bộ nào với trình duyệt ở 9 giờ sáng — bọc hàm mở trang, không sửa mã bộ kiểm.

`[đo]` Chạy lúc 9 giờ sáng: `tunlock` · `tev` · `tv14` · `tmaker` · `tsmoke` · `tfinal` · `tv12` đều đạt. Chạy theo giờ thật: cả chín bộ chính đều đạt.

## Kết quả

`[đo]` `tv15` · `thw` · `tv14` · `tmaker` · `tev` · `tsmoke` · `tfinal` · `tunlock` · `tv12` đạt theo giờ thật và lúc 9 giờ sáng · lõi 30/30 · bố cục đúng ở ba kích thước · 42/42 hiệu ứng · lai tạo, tổ đội, tác giả đạt · kiểm trùng tên và kiểm khoá sạch · hiệu năng 0 khung rớt.
