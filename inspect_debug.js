const fs = require('fs');

const home = fs.readFileSync('frontend/Home.html', 'utf8');

const modalStart = home.indexOf('id="modal-grievance"');
const modalEnd = home.indexOf('id="modal-schemes"');
console.log('modal-grievance length:', modalEnd - modalStart);
console.log(home.slice(modalStart, modalStart + 1500));
