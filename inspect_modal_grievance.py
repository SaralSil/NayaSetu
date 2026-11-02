import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Home.html', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="modal-grievance"')
end = html.find('id="modal-schemes"')
print(html[start+3500:end])
