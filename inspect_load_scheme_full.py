import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('async function loadSingleSchemeDetail')
idx_end = html.find('// Bind filter category buttons', idx)
print(html[idx:idx_end])
