// công cụ ký cho bộ kiểm: node sign.js <E|G|K> '<json>'
const fs=require('fs'); eval(fs.readFileSync(__dirname+'/evcore.js','utf8'));
const k=JSON.parse(fs.readFileSync('/home/claude/keys/private.json')).jwk;
evcSign(JSON.parse(process.argv[3]),k,process.argv[2]).then(c=>process.stdout.write(c));
