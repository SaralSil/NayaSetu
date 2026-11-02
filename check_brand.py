import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'data-i18n=["\']brand_title["\']', html)
print("data-i18n=brand_title found at:", m.start() if m else None)
if m:
    print(html[m.start()-100:m.start()+150])
