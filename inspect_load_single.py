import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'async function loadSingleSchemeDetail' in l:
        start_line = i
        break

print("".join(lines[start_line+120:start_line+240]))
