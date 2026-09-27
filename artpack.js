// đóng gói mã hình: node artpack.js '<json mảng hình>'
const fs=require('fs'); eval(fs.readFileSync(__dirname+'/evcore.js','utf8'));
evcArtPack(JSON.parse(process.argv[2])).then(c=>process.stdout.write(c));
