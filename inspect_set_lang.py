import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx1 = html.find('function setLanguage(')
idx2 = html.find('// Connect language switcher buttons')
print(html[idx1:idx2])
