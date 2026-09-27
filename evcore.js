/* ==========================================================
   LÕI SỰ KIỆN — DÙNG CHUNG cho game và trang tạo mã.
   Hai nơi chép Y HỆT đoạn này, nên trang tạo mã báo hợp lệ thì
   game chắc chắn nhận.

   An toàn:
   - Mã chỉ chứa DỮ LIỆU theo danh sách định sẵn, không chứa lệnh.
   - Có chữ ký ECDSA P-256: không có khoá bí mật thì không chế được mã.
   - Mọi con số bị giới hạn, mọi chữ bị cắt độ dài và thoát HTML khi
     hiện ra — kể cả mã do chính tác giả ký (phòng gõ nhầm).
   ========================================================== */
const EVC = {
  PREFIX:'PDE1', MAX_CODE:80000, MAX_DAYS:62,
  GOALS:{ care:'Chăm sóc pet', feed:'Cho ăn', quest:'Làm việc vận hành', tower:'Qua tầng tháp',
    trip:'Đi chuyến khám phá', harvest:'Thu hoạch vườn', craft:'Pha ly', sell:'Bán ly',
    win:'Thắng trận', boss:'Hạ boss sự kiện' },
  DONES:{ quest:'Làm một việc vận hành', feed:'Cho ăn', play:'Chơi', clean:'Tắm', sleep:'Ngủ',
    trip:'Đi chuyến khám phá', tower:'Qua một tầng tháp', harvest:'Thu hoạch', egg:'Xem trứng',
    now:'Ngay khi đồng ý' },
  BUFFS:{ hp:'Máu', atk:'Tấn công', def:'Phòng thủ', spd:'Tốc độ', int:'Trí', luck:'May mắn', crit:'Chí mạng' },
  LEVEL:{ easy:0.85, normal:1, hard:1.15 },
  LIM:{ coin:3000, tickets:5, passes:3, expSeed:5, seedEach:10, seedKinds:5,
    quests:8, wishes:6, lines:30, recipes:4, goalN:200, perDay:5,
    arts:10, pathsPerArt:16, pathLen:3000, ladder:6 },
  /* v1.4: tác dụng của pet sự kiện — KHÁC LOẠI, mạnh ngang Automa tốt nhất,
     con số do game cố định chứ không để mã tự đặt */
  PETFX:{
    boxExtra: { name:'Hộp bí ẩn mở ra thêm một món', v:1 },
    questCoin:{ name:'Xu từ việc vận hành tăng 15%', v:0.15 },
    waste:    { name:'Rác sinh ra giảm 30%', v:0.30 },
    drop:     { name:'Rơi trang bị trên tháp tăng 35%', v:0.35 },
    heal:     { name:'Hồi 12% máu sau mỗi tầng tháp', v:0.12 },
    mental:   { name:'Tinh thần pet chính hao chậm hơn 25%', v:0.25 },
    crop:     { name:'Thu thêm 2 nông sản mỗi lần hái', v:2 }
  },
  ARTKIND:{ pet:'Pet sự kiện', boss:'Boss', fash:'Thời trang', frame:'Khung lễ' },
  SLOTS:{ hat:'Mũ', wear:'Áo', hand:'Cầm tay', back:'Khoác sau lưng' },
  TYPE:{ E:'event', G:'gift', K:'key' }
};
function evcStr(v,max){ return (typeof v==='string') ? v.replace(/\s+/g,' ').trim().slice(0,max) : '' }
function evcNum(v,min,max){ v=+v; return isFinite(v) ? Math.max(min,Math.min(max,v)) : min }
function evcInt(v,min,max){ return Math.round(evcNum(v,min,max)) }
function evcSlug(v){ return (typeof v==='string') ? v.trim().toLowerCase() : '' }
function evcOkSlug(s){ return /^[a-z0-9][a-z0-9-]{1,39}$/.test(s) }
function evcEsc(s){ return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) }
/* phần thưởng: bỏ thứ không biết, hạ con số vượt trần và báo lại */
function evcReward(r, REF, E, W, where, ART){
  const out={}; if(!r || typeof r!=='object') return out;
  const cap=(k,v,lim,label)=>{ const n=evcInt(v,0,1e9); if(n>lim) W.push(`${where}: ${label} tối đa ${lim} — đã hạ xuống.`); return Math.min(n,lim) };
  if(r.coin)    out.coin   =cap('coin',r.coin,EVC.LIM.coin,'xu');
  if(r.tickets) out.tickets=cap('t',r.tickets,EVC.LIM.tickets,'vé tháp');
  if(r.passes)  out.passes =cap('p',r.passes,EVC.LIM.passes,'lượt đi');
  if(r.expSeed) out.expSeed=cap('e',r.expSeed,EVC.LIM.expSeed,'hạt kinh nghiệm');
  if(r.seeds && typeof r.seeds==='object'){
    const ks=Object.keys(r.seeds).filter(k=>REF.seeds.includes(k));
    Object.keys(r.seeds).filter(k=>!REF.seeds.includes(k)).forEach(k=>E.push(`${where}: không có hạt “${k}”.`));
    if(ks.length>EVC.LIM.seedKinds) W.push(`${where}: tối đa ${EVC.LIM.seedKinds} loại hạt — bỏ bớt.`);
    const s={}; ks.slice(0,EVC.LIM.seedKinds).forEach(k=>{ const n=cap('s',r.seeds[k],EVC.LIM.seedEach,'mỗi loại hạt'); if(n>0) s[k]=n });
    if(Object.keys(s).length) out.seeds=s;
  }
  if(r.box){ if(REF.boxes.includes(r.box)) out.box=r.box; else E.push(`${where}: không có loại hộp “${r.box}”.`) }
  if(r.frame){ const a=ART&&ART[r.frame];
    if(REF.frames.includes(r.frame) || (a && a.kind==='frame')) out.frame=r.frame;
    else E.push(`${where}: không có khung lễ “${r.frame}”.`) }
  if(r.egg){ if(REF.eggs && REF.eggs.includes(r.egg)) out.egg=r.egg; else E.push(`${where}: không có loại trứng “${r.egg}”.`) }
  if(r.pet){ const a=ART&&ART[r.pet]; if(a && a.kind==='pet') out.pet=r.pet; else E.push(`${where}: không có hình pet “${r.pet}” trong sự kiện.`) }
  if(r.fash){ const a=ART&&ART[r.fash]; if(a && a.kind==='fash') out.fash=r.fash; else E.push(`${where}: không có món thời trang “${r.fash}” trong sự kiện.`) }
  return out;
}

/* ==========================================================
   v1.4 — MÃ HÌNH: chỉ nét vẽ và màu, không gì khác.
   Nét vẽ chỉ được chứa chữ lệnh vẽ, số, dấu cách, phẩy, chấm, trừ —
   không có dấu nháy hay dấu < > nên không thể chèn thẻ hay lệnh.
   Game tự dựng hình bằng khuôn của nó từ các nét đã kiểm.
   ========================================================== */
const EVC_D=/^[MmLlHhVvCcSsQqTtAaZz0-9\s,.\-]+$/;
const EVC_C=/^(none|#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6})$/;
function evcD(d, E, where){ d=(typeof d==='string')?d.trim():'';
  if(!d || d.length>EVC.LIM.pathLen || !EVC_D.test(d)){ E.push(`${where}: nét vẽ không hợp lệ.`); return null } return d }
function evcCol(c, dft){ return (typeof c==='string' && EVC_C.test(c.trim())) ? c.trim() : dft }
function evcPaint(list, E, where){
  if(list==null) return [];
  if(!Array.isArray(list)){ E.push(`${where}: phải là danh sách nét.`); return [] }
  return list.slice(0,EVC.LIM.pathsPerArt).map((x,i)=>{ const d=evcD(x&&x.d,E,`${where} nét ${i+1}`); if(!d) return null;
    return { d, f:evcCol(x.f,'none'), s:evcCol(x.s,'none'), w:evcNum(x.w||0,0,8), o:evcNum(x.o==null?1:x.o,0,1) } }).filter(Boolean);
}
/* dựng SVG từ nét đã kiểm — dùng chung cho game và trang tạo mã */
function evcPaths(list){ return (list||[]).map(p=>`<path d="${p.d}" fill="${p.f}" stroke="${p.s}" stroke-width="${p.w}" opacity="${p.o}" stroke-linejoin="round" stroke-linecap="round"/>`).join('') }
function evcArt(a, E, W, i){
  const where=`Hình ${i+1}`, out={};
  if(!a || typeof a!=='object'){ E.push(`${where}: hỏng.`); return null }
  out.kind=a.kind; if(!EVC.ARTKIND[a.kind]){ E.push(`${where}: loại hình “${a.kind}” không có.`); return null }
  out.id=evcSlug(a.id); if(!evcOkSlug(out.id)) E.push(`${where}: mã hình sai.`);
  out.name=evcStr(a.name,40)||EVC.ARTKIND[a.kind];
  if(a.kind==='pet' || a.kind==='boss'){
    out.body=evcD(a.body,E,`${where} thân`);
    const b=a.belly||{}; out.belly={ cx:evcNum(b.cx||0,-60,60), cy:evcNum(b.cy||40,-60,80), rx:evcNum(b.rx||22,0,60), ry:evcNum(b.ry||16,0,60) };
    out.faceY=evcNum(a.faceY==null?12:a.faceY,-40,60);
    out.hue=evcInt(a.hue||0,0,359); out.sat=evcInt(a.sat==null?60:a.sat,0,100); out.light=evcInt(a.light==null?55:a.light,15,85);
    out.back=evcPaint(a.back,E,`${where} lớp sau`); out.marks=evcPaint(a.marks,E,`${where} hoa văn`); out.front=evcPaint(a.front,E,`${where} lớp trước`);
    if(a.kind==='pet'){ out.fx=a.fx; if(a.fx!=null && !EVC.PETFX[a.fx]) E.push(`${where}: tác dụng “${a.fx}” không có.`);
      // v1.5: thoại của pet sự kiện — vào tổ đội, sau trận thắng, khi đủ bộ thời trang
      const L=(a.lines && typeof a.lines==='object') ? a.lines : {};
      out.lines={ join:evcStr(L.join,140), win:evcStr(L.win,140), set:evcStr(L.set,140) } }
    out.note=evcStr(a.note,160);
  } else if(a.kind==='fash'){
    out.slot=a.slot; if(!EVC.SLOTS[a.slot]) E.push(`${where}: ô “${a.slot}” không có.`);
    out.col=evcCol(a.col,'#c8973f'); out.paths=evcPaint(a.paths,E,where);
    if(!out.paths.length) E.push(`${where}: cần ít nhất một nét.`);
    out.note=evcStr(a.note,120);
  } else if(a.kind==='frame'){
    out.edge=evcCol(a.edge,'#c8973f'); out.corner=evcPaint(a.corner,E,`${where} góc`);
    const f=a.fall||{}; out.fall={ paths:evcPaint(f.paths,E,`${where} hạt rơi`), n:evcInt(f.n||12,0,24),
      dur:[evcNum((f.dur||[])[0]||7,3,20), evcNum((f.dur||[])[1]||12,3,24)] };
    if(!out.corner.length) E.push(`${where}: khung cần hình ở góc.`);
    out.note=evcStr(a.note,160);
  }
  const n=['back','marks','front','paths','corner'].reduce((t,k)=>t+((out[k]||[]).length),0)+((out.fall&&out.fall.paths.length)||0);
  if(n>EVC.LIM.pathsPerArt*3) E.push(`${where}: quá nhiều nét.`);
  return out;
}

function evcValidate(o, REF){
  const E=[], W=[], d={v:1};
  if(!o || typeof o!=='object' || Array.isArray(o)) return {ok:false, errors:['Không phải dữ liệu sự kiện.'], warnings:[], data:null};
  d.id=evcSlug(o.id);
  if(!evcOkSlug(d.id)) E.push('Mã định danh chỉ gồm chữ thường không dấu, số, gạch ngang — 2 đến 40 ký tự.');
  d.rev=evcInt(o.rev||1,1,9999);
  d.name=evcStr(o.name,60); if(!d.name) E.push('Thiếu tên sự kiện.');
  d.intro=evcStr(o.intro,400);
  const s=Date.parse(o.start), e=Date.parse(o.end);
  if(!isFinite(s) || !isFinite(e)) E.push('Ngày bắt đầu hoặc kết thúc không hợp lệ.');
  else if(e<=s) E.push('Ngày kết thúc phải sau ngày bắt đầu.');
  else if(e-s > EVC.MAX_DAYS*864e5) E.push(`Một sự kiện dài tối đa ${EVC.MAX_DAYS} ngày.`);
  d.start=String(o.start||''); d.end=String(o.end||''); d.startT=s; d.endT=e;
  // hình vẽ trước — phần thưởng và boss tham chiếu tới hình
  d.art=[]; const ART={};
  if(o.art!=null){ if(!Array.isArray(o.art)) E.push('Hình vẽ phải là danh sách.');
    else { if(o.art.length>EVC.LIM.arts) W.push(`Hình vẽ: tối đa ${EVC.LIM.arts} — bỏ bớt.`);
      o.art.slice(0,EVC.LIM.arts).forEach((a,i)=>{ const x=evcArt(a,E,W,i); if(!x) return;
        if(ART[x.id]) E.push(`Hình ${i+1}: trùng mã “${x.id}”.`); ART[x.id]=x; d.art.push(x) }) } }
  d.gift=evcReward(o.gift, REF, E, W, 'Quà khi nhập mã', ART);
  const list=(a,max,label)=>{ if(a==null) return []; if(!Array.isArray(a)){ E.push(`${label} phải là danh sách.`); return [] }
    if(a.length>max) W.push(`${label}: tối đa ${max} — bỏ bớt phần sau.`); return a.slice(0,max) };
  const seen=new Set();
  d.quests=list(o.quests,EVC.LIM.quests,'Nhiệm vụ').map((q,i)=>{
    const w=`Nhiệm vụ ${i+1}`, id=evcSlug(q&&q.id)||('q'+(i+1));
    if(!evcOkSlug(id) || seen.has('q:'+id)) E.push(`${w}: mã nhiệm vụ trùng hoặc sai.`); seen.add('q:'+id);
    const t=evcStr(q&&q.t,60); if(!t) E.push(`${w}: thiếu tên.`);
    const g=q&&q.goal||{}; if(!EVC.GOALS[g.type]) E.push(`${w}: loại mục tiêu “${g.type}” không có.`);
    return { id, t, hint:evcStr(q&&q.hint,120), goal:{ type:g.type, n:evcInt(g.n||1,1,EVC.LIM.goalN) },
      reward:evcReward(q&&q.reward, REF, E, W, w, ART) };
  });
  d.wishes=list(o.wishes,EVC.LIM.wishes,'Mong muốn').map((x,i)=>{
    const w=`Mong muốn ${i+1}`, id=evcSlug(x&&x.id)||('w'+(i+1));
    if(!evcOkSlug(id) || seen.has('w:'+id)) E.push(`${w}: mã trùng hoặc sai.`); seen.add('w:'+id);
    const t=evcStr(x&&x.t,60), line=evcStr(x&&x.line,140);
    if(!t || !line) E.push(`${w}: cần tên việc và câu pet nói.`);
    if(!EVC.DONES[x&&x.done]) E.push(`${w}: cách hoàn thành “${x&&x.done}” không có.`);
    return { id, ic:evcStr(x&&x.ic,4)||'🎉', t, line, yes:evcStr(x&&x.yes,140)||'Vui quá!',
      no:evcStr(x&&x.no,140)||'Ừ, hôm khác nhé.', done:x&&x.done };
  });
  d.lines=list(o.lines,EVC.LIM.lines,'Câu pet nói').map(x=>evcStr(x,140)).filter(Boolean);
  d.recipes=list(o.recipes,EVC.LIM.recipes,'Công thức').map((r,i)=>{
    const w=`Công thức ${i+1}`, id=evcSlug(r&&r.id)||('r'+(i+1));
    if(!evcOkSlug(id) || seen.has('r:'+id)) E.push(`${w}: mã trùng hoặc sai.`); seen.add('r:'+id);
    const name=evcStr(r&&r.name,40); if(!name) E.push(`${w}: thiếu tên.`);
    if(!REF.groups.includes(r&&r.group)) E.push(`${w}: nhóm vị “${r&&r.group}” không có.`);
    const mats={}; Object.entries((r&&r.mats)||{}).slice(0,4).forEach(([k,n])=>{
      if(!REF.mats.includes(k)) E.push(`${w}: không có nguyên liệu “${k}”.`); else mats[k]=evcInt(n,1,5) });
    if(!Object.keys(mats).length) E.push(`${w}: cần ít nhất một nguyên liệu.`);
    const buff={}; Object.entries((r&&r.buff)||{}).forEach(([k,v])=>{
      if(!EVC.BUFFS[k]) return E.push(`${w}: chỉ số “${k}” không có.`);
      if(k==='crit'){ buff[k]=evcNum(v,0,0.15) } else { const n=evcNum(v,1,1.2); if(+v>1.2) W.push(`${w}: tăng chỉ số tối đa 20% — đã hạ xuống.`); buff[k]=n }
    });
    return { id, name, group:r&&r.group, mats, buff, note:evcStr(r&&r.note,160) };
  });
  if(o.boss){
    const b=o.boss, w='Boss';
    const name=evcStr(b.name,40); if(!name) E.push('Boss: thiếu tên.');
    if(!b.art && !REF.species.includes(b.species)) E.push(`Boss: không có loài “${b.species}”.`);
    if(!EVC.LEVEL[b.level||'normal']) E.push(`Boss: độ khó “${b.level}” không có.`);
    d.boss={ name, species:b.species, hue:evcInt(b.hue||0,0,359), level:b.level||'normal',
      quote:evcStr(b.quote,140)||'Thử xem.', perDay:evcInt(b.perDay||3,1,EVC.LIM.perDay),
      first:evcReward(b.first,REF,E,W,'Boss · lần đầu thắng',ART), win:evcReward(b.win,REF,E,W,'Boss · mỗi lần thắng',ART) };
    if(b.art){ const a=ART[b.art]; if(a && a.kind==='boss') d.boss.art=b.art; else E.push(`Boss: không có hình boss “${b.art}” trong sự kiện.`) }
  } else d.boss=null;
  d.ladder=list(o.ladder,EVC.LIM.ladder,'Thang mốc').map((m,i)=>({
    at:evcInt(m&&m.at||1,1,Math.max(1,d.quests.length)), reward:evcReward(m&&m.reward,REF,E,W,`Mốc ${i+1}`,ART) }))
    .sort((a,b)=>a.at-b.at);
  if(d.ladder.length && !d.quests.length) E.push('Thang mốc cần có nhiệm vụ để đếm.');
  d.setTitle=evcStr(o.setTitle,30);
  // pet từ mã hình phải có tác dụng — không có tác dụng thì chỉ là hình
  d.art.filter(a=>a.kind==='pet' && !a.fx).forEach(a=>E.push(`Pet “${a.name}”: chưa chọn tác dụng.`));
  if(!d.quests.length && !d.wishes.length && !d.lines.length && !d.recipes.length && !d.boss && !Object.keys(d.gift).length)
    E.push('Sự kiện trống — cần ít nhất một thứ: quà, nhiệm vụ, mong muốn, câu nói, công thức hoặc boss.');
  return { ok:E.length===0, errors:E, warnings:W, data:E.length?null:d };
}

/* ---------- v1.4: MÃ QUÀ TẶNG ---------- */
const EVC_PID=/^[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$/;
function evcValidateGift(o, REF){
  const E=[], W=[], d={t:'gift'};
  if(!o || typeof o!=='object') return {ok:false, errors:['Không phải mã quà.'], warnings:[], data:null};
  d.id=evcSlug(o.id); if(!evcOkSlug(d.id)) E.push('Mã quà: mã định danh sai.');
  d.name=evcStr(o.name,60); if(!d.name) E.push('Mã quà: thiếu tên.');
  d.reward=evcReward(o.reward,REF,E,W,'Quà');
  if(!Object.keys(d.reward).length) E.push('Mã quà: chưa có món quà nào.');
  d.to=''; if(o.to){ const p=String(o.to).trim().toUpperCase(); if(EVC_PID.test(p)) d.to=p; else E.push('Mã người chơi phải có dạng XXXX-XXXX.') }
  d.until=0; if(o.until){ const u=Date.parse(o.until); if(isFinite(u)) d.until=u; else E.push('Hạn nhận quà không hợp lệ.') }
  return {ok:!E.length, errors:E, warnings:W, data:E.length?null:d};
}
/* ---------- v1.4: KEY MỞ GAME — theo khách hàng, có hạn dùng ---------- */
function evcValidateKey(o){
  const E=[], d={t:'key'};
  if(!o || typeof o!=='object') return {ok:false, errors:['Không phải key.'], warnings:[], data:null};
  d.cid=evcSlug(o.cid); if(!evcOkSlug(d.cid)) E.push('Key: mã khách hàng sai.');
  d.cname=evcStr(o.cname,60); if(!d.cname) E.push('Key: thiếu tên khách hàng.');
  d.exp=0; if(o.exp){ const x=Date.parse(o.exp); if(isFinite(x)) d.exp=x; else E.push('Key: ngày hết hạn không hợp lệ.') }
  d.iat=Date.parse(o.iat)||0; d.note=evcStr(o.note,80);
  return {ok:!E.length, errors:E, warnings:[], data:E.length?null:d};
}

/* ---- mã hoá, ký, kiểm chữ ký ---- */
function evcB64u(bytes){ let s=''; for(let i=0;i<bytes.length;i++) s+=String.fromCharCode(bytes[i]);
  return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'') }
function evcUnB64u(str){ str=str.replace(/-/g,'+').replace(/_/g,'/'); while(str.length%4) str+='=';
  const bin=atob(str), u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return u }
function evcCrypto(){ const c=(typeof crypto!=='undefined') && crypto.subtle; return c||null }
/* nén: mã có hình vẽ dài 15–20 nghìn ký tự, nén còn khoảng một phần ba */
function evcCanZip(){ return typeof CompressionStream!=='undefined' && typeof DecompressionStream!=='undefined' }
async function evcZip(bytes){ const cs=new CompressionStream('deflate'); const w=cs.writable.getWriter();
  w.write(bytes).catch(()=>{}); w.close().catch(()=>{}); return new Uint8Array(await new Response(cs.readable).arrayBuffer()) }
async function evcUnzip(bytes, max){ // chặn bom nén: dừng khi vượt trần
  const ds=new DecompressionStream('deflate'); const w=ds.writable.getWriter();
  w.write(bytes).catch(()=>{}); w.close().catch(()=>{});   // huỷ giữa chừng sẽ làm hai lệnh này báo lỗi — bắt lại
  const rd=ds.readable.getReader(), parts=[]; let n=0;
  for(;;){ const {done,value}=await rd.read(); if(done) break; n+=value.length;
    if(n>max){ rd.cancel().catch(()=>{}); throw new Error('quá lớn') } parts.push(value) }
  const out=new Uint8Array(n); let o=0; parts.forEach(p=>{ out.set(p,o); o+=p.length }); return out }
/* ký: chữ ký luôn đặt trên dữ liệu CHƯA nén, và loại mã nằm trong phần được ký */
async function evcSign(obj, privJwk, T){
  T=T||'E';
  const sub=evcCrypto(); if(!sub) throw new Error('Trình duyệt này không có bộ ký an toàn — mở qua https hoặc Chrome/Safari mới.');
  const body=Object.assign({}, obj, {t:EVC.TYPE[T]});
  const bytes=new TextEncoder().encode(JSON.stringify(body));
  const key=await sub.importKey('jwk',{kty:'EC',crv:'P-256',x:privJwk.x,y:privJwk.y,d:privJwk.d},{name:'ECDSA',namedCurve:'P-256'},false,['sign']);
  const sig=new Uint8Array(await sub.sign({name:'ECDSA',hash:'SHA-256'},key,bytes));
  const zip = bytes.length>2500 && evcCanZip();
  const payload = zip ? await evcZip(bytes) : bytes;
  return 'PD'+T+(zip?'2':'1')+'.'+evcB64u(payload)+'.'+evcB64u(sig);
}
async function evcVerify(code, keys, T){
  T=T||'E';
  const sub=evcCrypto(); if(!sub) return {ok:false, err:'Trình duyệt này không kiểm được chữ ký — cần mở game qua https.'};
  code=String(code||'').replace(/\s+/g,'');
  if(code.length>EVC.MAX_CODE) return {ok:false, err:'Mã quá dài.'};
  const p=code.split('.'), m=/^PD([EGK])([12])$/.exec(p[0]||'');
  if(p.length!==3 || !m) return {ok:false, err:'Đây không phải mã Pet Drink.'};
  if(m[1]!==T) return {ok:false, err:({E:'Đây là mã sự kiện',G:'Đây là mã quà tặng',K:'Đây là key mở game'})[m[1]]+', không dùng ở đây.'};
  let bytes, sig;
  try{ const raw=evcUnB64u(p[1]); sig=evcUnB64u(p[2]);
    if(m[2]==='2'){ if(!evcCanZip()) return {ok:false, err:'Trình duyệt này không giải nén được mã — cập nhật Safari hoặc Chrome.'};
      bytes=await evcUnzip(raw, 400000) } else bytes=raw;
  }catch(e){ return {ok:false, err:'Mã bị hỏng — có thể dán thiếu.'} }
  for(const k of keys){
    try{
      const key=await sub.importKey('jwk',{kty:'EC',crv:'P-256',x:k.jwk.x,y:k.jwk.y},{name:'ECDSA',namedCurve:'P-256'},false,['verify']);
      if(await sub.verify({name:'ECDSA',hash:'SHA-256'},key,sig,bytes)){
        let obj; try{ obj=JSON.parse(new TextDecoder().decode(bytes)) }catch(e){ return {ok:false, err:'Nội dung mã hỏng.'} }
        // loại mã phải khớp với loại ghi trong phần ĐÃ KÝ; mã sự kiện v1.3 chưa có trường này
        const want=EVC.TYPE[T];
        if(!(obj.t===want || (T==='E' && m[2]==='1' && obj.t===undefined)))
          return {ok:false, err:'Loại mã không khớp — mã đã bị đổi tiền tố.'};
        return {ok:true, obj, kid:k.kid};
      }
    }catch(e){}
  }
  return {ok:false, err:'Chữ ký không đúng — mã này không do tác giả phát hành, hoặc đã bị sửa.'};
}
/* ---------- mã hình: em vẽ xong gửi tác giả bằng dạng này ----------
   CHƯA KÝ — chỉ để chuyển hình. Chữ ký đặt lúc tác giả phát hành sự kiện,
   và hình vẫn đi qua evcArt() kiểm từng nét trước khi dùng. */
async function evcArtPack(list){
  const bytes=new TextEncoder().encode(JSON.stringify(list));
  const zip=bytes.length>1500 && evcCanZip();
  return 'PDA'+(zip?'2':'1')+'.'+evcB64u(zip ? await evcZip(bytes) : bytes);
}
async function evcArtUnpack(code){
  code=String(code||'').replace(/\s+/g,'');
  const m=/^PDA([12])\.([A-Za-z0-9_-]+)$/.exec(code);
  if(!m) throw new Error('Đây không phải mã hình (mã hình bắt đầu bằng PDA).');
  let b=evcUnB64u(m[2]);
  if(m[1]==='2'){ if(!evcCanZip()) throw new Error('Trình duyệt này không giải nén được.'); b=await evcUnzip(b, 400000) }
  const o=JSON.parse(new TextDecoder().decode(b));
  return Array.isArray(o) ? o : [o];
}
