with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="grvScheme"')
idx_end = text.find('</select>', idx)
with open('grv_scheme_snippet.html', 'w', encoding='utf-8') as out:
    out.write(text[idx-50:idx_end+10])
print("Grv snippet written")
