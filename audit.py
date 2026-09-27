# Kiểm trùng tên class giữa CSS và JS — chạy cùng bộ test để không lặp lại
# ba lỗi .bf (v17), .fr và .dim (v23).
import re, glob, sys
h=open('index.html').read()
css=h[h.index('<style>'):h.index('</style>')]

# tập selector class ở mức gốc (không có tổ tiên) -> dễ đụng nhất
root={}
for m in re.finditer(r'(^|\})\s*([^{}@]+)\{([^}]*)\}', css, re.S):
    decl=m.group(3)
    for sel in m.group(2).split(','):
        sel=sel.strip()
        mm=re.fullmatch(r'\.([a-zA-Z][\w-]*)', sel)
        if mm: root.setdefault(mm.group(1), []).append(decl.strip()[:70])

risky=[]
for name,decls in root.items():
    if len(decls)>1:
        risky.append((name, decls))

print('=== class gốc bị khai báo nhiều lần (nguy cơ trùng ý nghĩa) ===')
if risky:
    for n,d in sorted(risky):
        print(f'  .{n}')
        for x in d: print('      ', x)
else:
    print('  không có')

# class nào vừa là lớp phủ toàn màn vừa dùng như nhãn
overlay=[n for n,d in root.items() if any('position: absolute' in x and 'inset' in x for x in d)]
js=open('_js.js').read()
clash=[]
for n in overlay:
    # dùng như nhãn phụ: xuất hiện trong chuỗi class có nhiều tên
    for m in re.finditer(r'class="([^"]*\b'+re.escape(n)+r'\b[^"]*)"', js):
        if len(m.group(1).split())>1 or '${' in m.group(1):
            clash.append((n, m.group(1)[:60])); break
print()
print('=== lớp phủ toàn màn bị dùng làm nhãn phụ ===')
print('  ', clash if clash else 'không có')

# --- kiểm trùng tên hàm JS giữa các module ---
import collections
FILES=['_js.js']   # từ v1.0 mã nằm trong một file duy nhất, tách ra _js.js để soi
seen=collections.defaultdict(list)
for f in FILES:
    try: t=open(f).read()
    except: continue
    for m in re.finditer(r'^function\s+([A-Za-z_$][\w$]*)\s*\(', t, re.M):
        seen[m.group(1)].append(f)
dupfn=[(n,fs) for n,fs in seen.items() if len(fs)>1]
print()
print('=== hàm JS trùng tên giữa các module ===')
if dupfn:
    for n,fs in sorted(dupfn): print(f'   {n}()  ->  ' + ', '.join(fs))
else:
    print('   không có')

# --- kiểm trùng khoá trạng thái S.* giữa các module ---
skeys=collections.defaultdict(set)
for f in FILES:
    try: t=open(f).read()
    except: continue
    for m in re.finditer(r'S\.([a-zA-Z_$][\w$]*)\s*=\s*S\.\1\s*\|\|', t):
        skeys[m.group(1)].add(f)
dupk=[(k,fs) for k,fs in skeys.items() if len(fs)>1]
print()
print('=== khoá trạng thái khởi tạo ở nhiều nơi ===')
print('  ', [f'{k}: {sorted(fs)}' for k,fs in dupk] if dupk else 'không có')


# --- v1.3: khoá bí mật KHÔNG BAO GIỜ được nằm trong game ---
import re as _re
_h=open('index.html').read()
_priv=_re.search(r'"crv"\s*:\s*"P-256"[^}]{0,400}"d"\s*:\s*"[A-Za-z0-9_-]{20,}"|"d"\s*:\s*"[A-Za-z0-9_-]{40,}"[^}]{0,400}"crv"\s*:\s*"P-256"', _h)
print()
print('=== khoá bí mật trong game ===')
print('   !!! CÓ — GỠ NGAY, KHÔNG ĐƯỢC PHÁT HÀNH !!!' if _priv else '   không có')
if _priv: sys.exit(2)

sys.exit(1 if (clash or dupfn) else 0)
