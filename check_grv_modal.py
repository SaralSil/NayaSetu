with open('frontend/Home.html', encoding='utf-8') as f:
    html = f.read()
import re
start = html.find('id="modal-grievance"')
end = html.find('id="modal-schemes"')
modal_html = html[start:end]

data_paths = re.findall(r'data-path="[^"]*"', modal_html)
print('data-paths in modal-grievance:', data_paths)

close_modals = re.findall(r'close-modal', modal_html)
print('close-modal count in modal-grievance:', len(close_modals))
