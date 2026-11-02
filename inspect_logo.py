import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('brand_title')
print(html[idx-150:idx+350])
