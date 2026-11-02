import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function renderWizardResults')
print(html[idx+2000:idx+4500])
