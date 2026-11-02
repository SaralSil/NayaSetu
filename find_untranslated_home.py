import sys
import re
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

class BengaliFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.bengali_regex = re.compile(r'[\u0980-\u09FF]')
        self.untranslated = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        self.tag_stack.append((tag, attrs_dict))

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        if self.tag_stack and self.tag_stack[-1][0] == tag:
            self.tag_stack.pop()

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        text = data.strip()
        if text and self.bengali_regex.search(text):
            has_i18n = any('data-i18n' in attrs for _, attrs in self.tag_stack)
            if not has_i18n:
                curr_tag, curr_attrs = self.tag_stack[-1] if self.tag_stack else ('unknown', {})
                self.untranslated.append((curr_tag, curr_attrs.get('id', ''), curr_attrs.get('class', ''), text))

with open('frontend/Home.html', encoding='utf-8') as f:
    html = f.read()

parser = BengaliFinder()
parser.feed(html)

print("\nElements 51 to 150:")
for i, u in enumerate(parser.untranslated[50:150]):
    print(f"{i+51}. <{u[0]} id='{u[1]}'>: {u[3]}")
