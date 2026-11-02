import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find("noticeForm.addEventListener('submit'")
print(html[idx+2500:idx+4500])
