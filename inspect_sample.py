import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('not_sample_annapurna')
print("Found not_sample_annapurna at", idx)
if idx != -1:
    print(html[idx-100:idx+600])
