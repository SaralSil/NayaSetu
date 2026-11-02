import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('wizSubmitBtn')
print(html[idx-100:idx+500])
