import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'কর্মশ্রী ৫০ দিন' in l or 'স্বাস্থ্য সাথী কার্ড' in l or 'সুশাসন সেবা শিবির' in l or 'কৃষক বন্ধু নমুনা' in l or 'id="grvLang"' in l:
        print(f"Line {i+1}: {l}")
