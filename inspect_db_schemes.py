import os, sys
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.schemes.models import Scheme

schemes = Scheme.objects.all()
print(f"Total schemes in DB: {schemes.count()}")
for s in schemes:
    print("---")
    print("Slug:", s.slug)
    print("Name BN:", s.name_bn)
    print("Name EN:", s.name_en)
    print("Desc EN:", s.description_en[:50] if s.description_en else "EMPTY")
    print("Benefit EN:", s.benefit_amount_text_en)
    print("Rules Summary EN:", s.eligibility.rules_summary_en if hasattr(s, 'eligibility') and s.eligibility else "NO ELIG")
