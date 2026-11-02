const fs = require('fs');
const html = fs.readFileSync('frontend/Landing.html', 'utf8');

const idx = html.indexOf('data-i18n="c4_desc"');
console.log(html.substring(idx, idx+1500));
