import sys
import re
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Home.html', encoding='utf-8') as f:
    lines = f.readlines()

bengali_regex = re.compile(r'[\u0980-\u09FF]')

untranslated_lines = []
in_script = False
in_style = False

for idx, line in enumerate(lines):
    stripped = line.strip()
    if '<script' in stripped:
        in_script = True
    if '</script>' in stripped:
        in_script = False
        continue
    if '<style' in stripped:
        in_style = True
    if '</style>' in stripped:
        in_style = False
        continue
    if in_script or in_style:
        continue

    if bengali_regex.search(stripped) and 'data-i18n' not in stripped:
        untranslated_lines.append((idx + 1, stripped))

print(f"Total lines with untranslated Bengali: {len(untranslated_lines)}")
with open('untranslated_lines.txt', 'w', encoding='utf-8') as out:
    for num, l in untranslated_lines:
        out.write(f"Line {num}: {l}\n")

print("Written to untranslated_lines.txt")
