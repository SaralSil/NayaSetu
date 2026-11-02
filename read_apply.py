import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('apply_full_multilingual.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
for i in range(0, len(lines), 50):
    print(f"--- Line {i} ---")
    print("".join(lines[i:i+30]))
