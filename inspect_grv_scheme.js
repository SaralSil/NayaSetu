const fs = require('fs');
const html = fs.readFileSync('frontend/Landing.html', 'utf8');

const idx = html.indexOf('id="grvScheme"');
console.log(html.substring(idx, idx+1200));
