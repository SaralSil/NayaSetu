with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('async function loadSingleSchemeDetail')
print(html[idx:idx+4500])
