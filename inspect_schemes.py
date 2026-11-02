import re

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Endpoints:")
for ep in set(re.findall(r'/api/[a-zA-Z0-9_\-/]+', html)):
    if 'scheme' in ep:
        print(ep)

print("\nFunctions matching scheme detail:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*scheme[a-zA-Z0-9_]*)\s*\(', html, re.IGNORECASE):
    print(m.group(1))

print("\nLook for modal or render functions:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*detail[a-zA-Z0-9_]*|[a-zA-Z0-9_]*modal[a-zA-Z0-9_]*)\s*\(', html, re.IGNORECASE):
    print(m.group(1))
