import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find("wizardForm.addEventListener('submit'")
print(html[idx+1800:idx+3000])
