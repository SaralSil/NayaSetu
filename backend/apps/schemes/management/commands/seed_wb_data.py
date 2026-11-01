from django.core.management.base import BaseCommand
from apps.schemes.models import Department, Scheme, SchemeEligibility, SchemeDocument, CommonRejectionReason
from apps.grievances.models import OfficialDirectory

class Command(BaseCommand):
    help = "Seed verified West Bengal Welfare Schemes, eligibility rules, and departments"

    def handle(self, *args, **options):
        self.stdout.write("Seeding West Bengal Departments...")

        # 1. Departments
        wcd, _ = Department.objects.get_or_create(
            code="wcd",
            defaults={
                "name_en": "Department of Women & Child Development and Social Welfare",
                "name_bn": "নারী ও শিশু বিকাশ এবং সমাজকল্যাণ দপ্তর",
                "name_hi": "महिला एवं बाल विकास और समाज कल्याण विभाग",
                "portal_url": "https://wb.gov.in",
                "helpline": "1800-345-5555"
            }
        )

        agri, _ = Department.objects.get_or_create(
            code="agri",
            defaults={
                "name_en": "Department of Agriculture",
                "name_bn": "কৃষি বিভাগ",
                "name_hi": "कृषि विभाग",
                "portal_url": "https://krishakbandhu.wb.gov.in",
                "helpline": "1800-103-3221"
            }
        )

        bcwd, _ = Department.objects.get_or_create(
            code="bcwd",
            defaults={
                "name_en": "Backward Classes Welfare Department",
                "name_bn": "অনগ্রসর শ্রেণী কল্যাণ দপ্তর",
                "name_hi": "पिछड़ा वर्ग कल्याण विभाग",
                "portal_url": "https://wbbcdev.gov.in",
                "helpline": "033-2321-2089"
            }
        )

        tribal, _ = Department.objects.get_or_create(
            code="tribal",
            defaults={
                "name_en": "Tribal Development Department",
                "name_bn": "আদিবাসী বিকাশ দপ্তর",
                "name_hi": "জনজাতীয় বিকাশ বিভাগ",
                "portal_url": "https://adibasikalyan.gov.in",
                "helpline": "033-2337-0205"
            }
        )

        health, _ = Department.objects.get_or_create(
            code="health",
            defaults={
                "name_en": "Health & Family Welfare Department",
                "name_bn": "স্বাস্থ্য ও পরিবার কল্যাণ দপ্তর",
                "name_hi": "स्वास्थ्य और परिवार कल्याण विभाग",
                "portal_url": "https://swasthyasathi.gov.in",
                "helpline": "1800-345-5384"
            }
        )

        minority, _ = Department.objects.get_or_create(
            code="minority",
            defaults={
                "name_en": "Minority Affairs & Madrasah Education Department",
                "name_bn": "সংখ্যালঘু বিষয়ক ও মাদ্রাসা শিক্ষা দপ্তর",
                "name_hi": "अल्पसंख्यक मामले और मदरसा शिक्षा विभाग",
                "portal_url": "https://wbmdfc.org",
                "helpline": "1800-120-2130"
            }
        )

        higher_edu, _ = Department.objects.get_or_create(
            code="higher_edu",
            defaults={
                "name_en": "Department of Higher Education",
                "name_bn": "উচ্চশিক্ষা দপ্তর",
                "name_hi": "उच्च शिक्षा विभाग",
                "portal_url": "https://wbscc.wb.gov.in",
                "helpline": "1800-102-8014"
            }
        )

        self.stdout.write("Seeding West Bengal Welfare Schemes...")

        # -------------------------------------------------------------
        # Scheme 1: Lakshmir Bhandar (লক্ষ্মীর ভাণ্ডার)
        # -------------------------------------------------------------
        lb, _ = Scheme.objects.get_or_create(
            slug="lakshmir-bhandar",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Lakshmir Bhandar",
                "name_bn": "লক্ষ্মীর ভাণ্ডার",
                "name_hi": "लक्ष्मी भंडार",
                "tagline_en": "Financial assistance for adult women in West Bengal",
                "tagline_bn": "পশ্চিমবঙ্গের মহিলাদের সার্বিক আর্থিক ক্ষমতায়নের জন্য মাসিক সহায়তা",
                "description_en": "Lakshmir Bhandar provides monthly financial assistance of Rs. 1,000 for General/OBC women and Rs. 1,200 for SC/ST women aged 25-60 years directly to their individual bank account.",
                "description_bn": "২৫ থেকে ৬০ বছর বয়সী সাধারণ ও ওবিসি পরিবারের মহিলাদের জন্য মাসিক ১,০০০ টাকা এবং তফশিলি জাতি/উপজাতির মহিলাদের জন্য মাসিক ১,২০০ টাকা সরাসরি নিজস্ব ব্যাংক অ্যাকাউন্টে প্রদান করা হয়।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000/month (General/OBC) | ₹1,200/month (SC/ST)",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা (সাধারণ/ওবিসি) | মাসিক ১,২০০ টাকা (তফসিলি জাতি/উপজাতি)",
                "application_channels": ["Duare Sarkar Camp", "BDO Office (Rural)", "SDO / Municipality Office (Urban)"],
                "official_portal_url": "https://wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=lb,
            defaults={
                "min_age": 25,
                "max_age": 60,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "requires_swasthya_sathi": True,
                "rules_summary_en": "Female resident of West Bengal aged 25-60. Must possess a Swasthya Sathi card and a single-operated bank account linked to Aadhaar (NPCI DBT active). Not eligible if receiving government job salary or government pension.",
                "rules_summary_bn": "বয়স ২৫ থেকে ৬০ বছর হতে হবে, স্বাস্থ্য সাথী কার্ড থাকা বাধ্যতামূলক এবং নিজস্ব একক (সিঙ্গেল) ব্যাংক অ্যাকাউন্ট থাকতে হবে। সরকারি চাকরিজীবী বা সরকারি পেনশন প্রাপকরা আবেদনযোগ্য নন।"
            }
        )
        lb_docs = [
            ("Swasthya Sathi Card", "স্বাস্থ্য সাথী কার্ড", True, "Card must have applicant woman's name listed"),
            ("Aadhaar Card", "আধার কার্ড", True, "Must be linked with mobile and bank account"),
            ("Single Bank Account Passbook", "একক (সিঙ্গেল) ব্যাংক পাসবুক", True, "Joint accounts are STRICTLY NOT ACCEPTED"),
            ("Caste Certificate (SC/ST)", "তফসিলি জাতি/উপজাতি সার্টিফিকেট", False, "Mandatory for receiving higher assistance of ₹1,200/month"),
            ("Passport Photo", "পাসপোর্ট সাইজ ছবি", True, "Recent colour photograph")
        ]
        for name_en, name_bn, is_mand, clar in lb_docs:
            SchemeDocument.objects.get_or_create(
                scheme=lb, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        CommonRejectionReason.objects.get_or_create(
            scheme=lb,
            code_or_phrase="Bank Account Validation Failed",
            defaults={
                "title_en": "Bank Account Validation / Single Account Mismatch",
                "title_bn": "ব্যাংক অ্যাকাউন্ট যাচাইকরণ ব্যর্থ / যৌথ অ্যাকাউন্ট সমস্যা",
                "explanation_en": "The bank account entered is either a joint account, has a name spelling mismatch with the Aadhaar card, or does not exist in active status.",
                "explanation_bn": "প্রদত্ত ব্যাংক অ্যাকাউন্টটি হয় যৌথ (জয়েন্ট) অ্যাকাউন্ট, অথবা আধারের নামের বানানের সাথে ব্যাংকের নামের গরমিল আছে।",
                "remedy_steps_en": [
                    "Open a fresh single savings account in your name at any nationalized or post office bank.",
                    "Ensure Aadhaar DBT mapping (NPCI) is active.",
                    "Submit bank passbook copy and Aadhaar copy at the BDO office or Duare Sarkar helpdesk."
                ],
                "remedy_steps_bn": [
                    "আপনার নিজস্ব নামে একটি নতুন সিঙ্গেল সেভিংস অ্যাকাউন্ট খুলুন।",
                    "ব্যাংকে গিয়ে আধার ডিবিটি (NPCI) ম্যাপিং নিশ্চিত করুন।",
                    "বিডিও অফিস বা দুয়ারে সরকার ডেস্কে নতুন পাসবুকের জেরক্স জমা দিন।"
                ],
                "responsible_authority": "Bank Branch & BDO Office"
            }
        )

        CommonRejectionReason.objects.get_or_create(
            scheme=lb,
            code_or_phrase="NPCI Inactive / Aadhaar De-linked",
            defaults={
                "title_en": "Aadhaar NPCI DBT Inactive in Bank Account",
                "title_bn": "ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) নিষ্ক্রিয়",
                "explanation_en": "Direct Benefit Transfer mandates that the bank account must be mapped with NPCI. Even if Aadhaar is linked for KYC, DBT mapping must be explicitly enabled.",
                "explanation_bn": "টাকা পাওয়ার জন্য ব্যাংক অ্যাকাউন্টে NPCI ম্যাপিং বাধ্যতামূলক। শুধুমাত্র আধার জমা দিলেই হয় না, ডিবিটি সক্রিয় থাকতে হয়।",
                "remedy_steps_en": [
                    "Visit your home bank branch.",
                    "Fill and submit the 'Aadhaar NPCI DBT Seeding Mandate' form.",
                    "Take a stamped receipt from the bank manager."
                ],
                "remedy_steps_bn": [
                    "আপনার মূল ব্যাংক শাখায় যান।",
                    "'আধার এনপিসিআই ডিবিটি ম্যান্ডেট' ফর্ম জমা দিন।",
                    "ব্যাংক ম্যানেজারের সিলযুক্ত কপি নিজের কাছে রাখুন।"
                ],
                "responsible_authority": "Bank Branch"
            }
        )

        # -------------------------------------------------------------
        # Scheme 2: Krishak Bandhu (Natun) (কৃষক বন্ধু - নতুন)
        # -------------------------------------------------------------
        kb, _ = Scheme.objects.get_or_create(
            slug="krishak-bandhu-natun",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Krishak Bandhu (Natun)",
                "name_bn": "কৃষক বন্ধু (নতুন)",
                "name_hi": "कृषक बंधु (नया)",
                "tagline_en": "Assured financial support and life death benefit for farmers in WB",
                "tagline_bn": "পশ্চিমবঙ্গের কৃষকদের জন্য নিশ্চিত আর্থিক অনুদান ও ২ লক্ষ টাকার জীবনাবসান সহায়তা",
                "description_en": "Financial assistance up to Rs. 10,000 per year (for 1 acre or more cultivable land) paid in 2 equal installments (Kharif and Rabi), with min Rs. 4,000 for small/marginal farmers, plus Rs. 2 Lakh death benefit for farmer families (age 18-60).",
                "description_bn": "১ একর বা তার বেশি চাষযোগ্য জমির জন্য বছরে সর্বাধিক ১০,০০০ টাকা (দুটি কিস্তিতে) এবং ক্ষুদ্র কৃষকদের ন্যূনতম ৪,০০০ টাকা সহায়তা, সাথে ১৮-৬০ বছর বয়সের মধ্যে কৃষকের স্বাভাবিক বা দুর্ঘটনায় মৃত্যুতে ২ লক্ষ টাকার পরিবার সহায়তা।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "₹4,000 to ₹10,000 / year + ₹2 Lakh Death Benefit",
                "benefit_amount_text_bn": "বছরে ৪,০০০ থেকে ১০,০০০ টাকা + ২ লক্ষ টাকা মৃত্যু সুবিধা",
                "application_channels": ["Duare Sarkar Camp", "Assistant Director of Agriculture (ADA) Office", "Krishak Bandhu Portal"],
                "official_portal_url": "https://krishakbandhu.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=kb,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "requires_land_record": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Farmer or recorded Bhagchasi (sharecropper) possessing cultivable land Record of Rights (RoR / Porcha) mutated in own name.",
                "rules_summary_bn": "পশ্চিমবঙ্গের কৃষক বা নথিবদ্ধ ভাগচাষী হতে হবে এবং নিজস্ব নামে চাষযোগ্য জমির সাম্প্রতিক রেকর্ড (পর্চা/খতিয়ান) থাকতে হবে।"
            }
        )
        kb_docs = [
            ("Land Record (RoR / Porcha)", "জমির সাম্প্রতিক রেকর্ড (পর্চা / খতিয়ান)", True, "Must be mutated in applicant's name"),
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory identification document"),
            ("Voter ID Card (EPIC)", "ভোটার কার্ড (EPIC)", True, "Mandatory for Krishak Bandhu verification"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "With clear IFSC and Account Number")
        ]
        for name_en, name_bn, is_mand, clar in kb_docs:
            SchemeDocument.objects.get_or_create(
                scheme=kb, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        CommonRejectionReason.objects.get_or_create(
            scheme=kb,
            code_or_phrase="Land Record Unverified / Porcha Mismatch",
            defaults={
                "title_en": "Land Record Mutation Pending or Porcha Not Updated",
                "title_bn": "জমির মিউটেশন অমীমাংসিত বা পর্চায় গরমিল",
                "explanation_en": "The submitted land Record of Rights (RoR) is either in ancestors' name (not mutated to applicant), or does not match Banglarbhumi land registry records.",
                "explanation_bn": "জমা দেওয়া পর্চাটি পূর্বপুরুষদের নামে রয়েছে (আবেদনকারীর নামে মিউটেশন হয়নি) অথবা বাংলারভূমি পোর্টালের রেকর্ডের সাথে মিলছে না।",
                "remedy_steps_en": [
                    "Apply for land mutation at the local BL&LRO (Block Land and Land Reforms Office).",
                    "Obtain the digitized Porcha from banglarbhumi.gov.in.",
                    "Submit updated Porcha with an application at the Assistant Director of Agriculture (ADA) office."
                ],
                "remedy_steps_bn": [
                    "স্থানীয় বিএলএলআরও (BL&LRO) অফিসে গিয়ে জমির মিউটেশনের আবেদন করুন।",
                    "বাংলারভূমি পোর্টাল থেকে ডিজিটাল পর্চা সংগ্রহ করুন।",
                    "সহকারী কৃষি অধিকর্তা (ADA) অফিসে নতুন পর্চাসহ আবেদন জমা দিন।"
                ],
                "responsible_authority": "BL&LRO & ADA Office"
            }
        )

        # -------------------------------------------------------------
        # Scheme 3: Kanyashree Prakalpa (কন্যাশ্রী প্রকল্প)
        # -------------------------------------------------------------
        kanya, _ = Scheme.objects.get_or_create(
            slug="kanyashree-prakalpa",
            defaults={
                "department": wcd,
                "category": "education",
                "name_en": "Kanyashree Prakalpa (K1 & K2)",
                "name_bn": "কন্যাশ্রী প্রকল্প (কে-১ ও কে-২)",
                "name_hi": "कन्याश्री प्रकल्प",
                "tagline_en": "Conditional cash transfer to promote girls' education and prevent early marriage",
                "tagline_bn": "মেয়েদের পড়াশোনা চালিয়ে যেতে এবং বাল্যবিবাহ রোধে বার্ষিক ও এককালীন অনুদান",
                "description_en": "K1 provides an annual scholarship of Rs. 1,000 for unmarried school girls aged 13-18 (Classes VIII-XII). K2 provides a one-time grant of Rs. 25,000 when the girl turns 18 and is continuing registered education while remaining unmarried.",
                "description_bn": "১৩ থেকে ১৮ বছর বয়সী অবিবাহিত ছাত্রীদের জন্য বার্ষিক ১,০০০ টাকা (K1) এবং ১৮ বছর বয়স পূর্ণ হলে অবিবাহিত অবস্থায় উচ্চশিক্ষা চালিয়ে যাওয়ার জন্য এককালীন ২৫,০০০ টাকা (K2) অনুদান।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "K1: ₹1,000 / year | K2: ₹25,000 (One-time grant)",
                "benefit_amount_text_bn": "কে-১: বার্ষিক ১,০০০ টাকা | কে-২: এককালীন ২৫,০০০ টাকা",
                "application_channels": ["Through School / College Institution", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbkanyashree.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=kanya,
            defaults={
                "min_age": 13,
                "max_age": 19,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Unmarried girl student residing in West Bengal, enrolled in class VIII or above in a recognized school/madrasah/college. K1: age 13-18. K2: age 18-19.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, অবিবাহিত ছাত্রী এবং কোনো স্বীকৃত বিদ্যালয়/মাদ্রাসা/কলেজে পাঠরত। কে-১ এর জন্য বয়স ১৩-১৮ এবং কে-২ এর জন্য বয়স ১৮-১৯ হতে হবে।"
            }
        )
        kanya_docs = [
            ("School Enrollment Certificate", "বিদ্যালয়ে ভর্তির প্রমাণপত্র", True, "Signed by Headmaster / Principal"),
            ("Unmarried Declaration", "অবিবাহিত থাকার ঘোষণাপত্র", True, "Self/Guardian declaration on prescribed form"),
            ("Aadhaar Card", "আধার কার্ড", True, "Student's own Aadhaar card"),
            ("Bank Passbook", "ছাত্রীর নিজস্ব ব্যাংক পাসবুক", True, "Must be single account in student's name"),
            ("Age Proof (Birth Certificate / Admit)", "জন্ম সার্টিফিকেট বা মাধ্যমিক অ্যাডমিট", True, "For age verification")
        ]
        for name_en, name_bn, is_mand, clar in kanya_docs:
            SchemeDocument.objects.get_or_create(
                scheme=kanya, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 4: Jai Johar (জয় জোহার)
        # -------------------------------------------------------------
        jj, _ = Scheme.objects.get_or_create(
            slug="jai-johar",
            defaults={
                "department": tribal,
                "category": "tribal_caste",
                "name_en": "Jai Johar (ST Old Age Pension)",
                "name_bn": "জয় জোহার (তফসিলি উপজাতি বার্ধক্য ভাতা)",
                "name_hi": "जय जोहार",
                "tagline_en": "Monthly pension for elderly Scheduled Tribe (ST) citizens",
                "tagline_bn": "পশ্চিমবঙ্গের ৬০ বছর বা তদূর্ধ্ব তফসিলি উপজাতি (ST) নাগরিকদের জন্য মাসিক পেনশন",
                "description_en": "Under Jai Johar, every Scheduled Tribe person aged 60 years or above receives a monthly pension of Rs. 1,000 directly into their bank account.",
                "description_bn": "জয় জোহার প্রকল্পের অধীনে ৬০ বছর বা তার বেশি বয়সী সকল তফসিলি উপজাতি (ST) ব্যক্তিকে মাসিক ১,০০০ টাকা করে সরাসরি ব্যাংক অ্যাকাউন্টে পেনশন দেওয়া হয়।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000 / month",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "SDO Office"],
                "official_portal_url": "https://adibasikalyan.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=jj,
            defaults={
                "min_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["ST"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Must belong to Scheduled Tribe (ST) category, age 60 years or above, permanent resident of West Bengal. Must not be receiving any other government pension.",
                "rules_summary_bn": "তফসিলি উপজাতি (ST) ভুক্ত হতে হবে, বয়স ৬০ বছর বা তার বেশি হতে হবে এবং অন্য কোনো সরকারি পেনশন প্রাপক হওয়া যাবে না।"
            }
        )
        jj_docs = [
            ("Digitized ST Caste Certificate", "ডিজিটাল তফসিলি উপজাতি (ST) সার্টিফিকেট", True, "Issued by SDO or competent authority"),
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory proof of identity and age"),
            ("Voter Card (EPIC)", "ভোটার কার্ড", True, "Address proof"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Linked with Aadhaar")
        ]
        for name_en, name_bn, is_mand, clar in jj_docs:
            SchemeDocument.objects.get_or_create(
                scheme=jj, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 5: Taposhili Bandhu (তপশিলী বন্ধু)
        # -------------------------------------------------------------
        tb, _ = Scheme.objects.get_or_create(
            slug="taposhili-bandhu",
            defaults={
                "department": bcwd,
                "category": "tribal_caste",
                "name_en": "Taposhili Bandhu (SC Old Age Pension)",
                "name_bn": "তপশিলী বন্ধু (তফসিলি জাতি বার্ধক্য ভাতা)",
                "name_hi": "तपशिली बंधु",
                "tagline_en": "Monthly pension for elderly Scheduled Caste (SC) citizens",
                "tagline_bn": "পশ্চিমবঙ্গের ৬০ বছর বা তদূর্ধ্ব তফসিলি জাতি (SC) প্রবীণ নাগরিকদের জন্য মাসিক পেনশন",
                "description_en": "Taposhili Bandhu provides a monthly pension of Rs. 1,000 to all Scheduled Caste (SC) persons aged 60 years or above who are not covered under any other pension scheme.",
                "description_bn": "তপশিলী বন্ধু প্রকল্পের অধীনে ৬০ বছর বা তদূর্ধ্ব সমস্ত তফসিলি জাতি (SC) ভুক্ত প্রবীণ নাগরিকদের মাসিক ১,০০০ টাকা হারে বার্ধক্য ভাতা প্রদান করা হয়।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000 / month",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "SDO Office"],
                "official_portal_url": "https://wbbcdev.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=tb,
            defaults={
                "min_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["SC"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Scheduled Caste (SC) citizen aged 60 years or above residing in West Bengal, not receiving any other old age or social security pension.",
                "rules_summary_bn": "তফসিলি জাতি (SC) ভুক্ত হতে হবে, বয়স ৬০ বছর বা তার বেশি হতে হবে এবং অন্য কোনো পেনশন প্রাপক হওয়া যাবে না।"
            }
        )
        tb_docs = [
            ("Digitized SC Certificate", "ডিজিটাল তফসিলি জাতি (SC) সার্টিফিকেট", True, "SDO issued certificate"),
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Aadhaar seeded savings account"),
            ("Voter ID Card", "ভোটার আইডি কার্ড", True, "Proof of residence in WB")
        ]
        for name_en, name_bn, is_mand, clar in tb_docs:
            SchemeDocument.objects.get_or_create(
                scheme=tb, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 6: Swasthya Sathi (স্বাস্থ্য সাথী)
        # -------------------------------------------------------------
        ss, _ = Scheme.objects.get_or_create(
            slug="swasthya-sathi",
            defaults={
                "department": health,
                "category": "health",
                "name_en": "Swasthya Sathi",
                "name_bn": "স্বাস্থ্য সাথী",
                "name_hi": "स्वास्थ्य साथी",
                "tagline_en": "Universal cashless secondary and tertiary healthcare coverage up to ₹5 Lakh/year",
                "tagline_bn": "পশ্চিমবঙ্গের প্রতিটি পরিবারের জন্য বার্ষিক ৫ লক্ষ টাকা পর্যন্ত ক্যাশলেস স্বাস্থ্য বীমা",
                "description_en": "Swasthya Sathi is West Bengal's flagship health scheme providing basic health cover up to Rs. 5 Lakh per annum per family on a floater basis. The smart card is issued in the name of the eldest female family member.",
                "description_bn": "পরিবার পিছু প্রতি বছর ৫ লক্ষ টাকা পর্যন্ত ক্যাশলেস চিকিৎসার সুবিধা। এই কার্ডটি পরিবারের বয়োজ্যেষ্ঠা মহিলার নামে ইস্যু করা হয় এবং পরিবারের সকল সদস্য এর আওতাভুক্ত থাকেন।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "Up to ₹5,00,000 / year (Cashless in empanelled hospitals)",
                "benefit_amount_text_bn": "পরিবার পিছু বছরে ৫,০০,০০০ টাকা পর্যন্ত ক্যাশলেস চিকিৎসা",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "Swasthya Sathi Kiosk at Sub-Division"],
                "official_portal_url": "https://swasthyasathi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ss,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "rules_summary_en": "All families in West Bengal not covered under any other comprehensive government/corporate medical allowance.",
                "rules_summary_bn": "পশ্চিমবঙ্গের সকল পরিবার, যারা অন্য কোনো সরকারি মেডিকেল ভাতা বা রিইমবার্সমেন্ট পান না।"
            }
        )
        ss_docs = [
            ("Aadhaar Card of all family members", "পরিবারের সকল সদস্যের আধার কার্ড", True, "For biometric enrollment"),
            ("Ration Card (Khadya Sathi)", "ডিজিটাল রেশন কার্ড", True, "Family composition proof"),
            ("Photo of Eldest Female Member", "পরিবারের বয়োজ্যেষ্ঠা মহিলার ছবি", True, "Card is issued in female head's name")
        ]
        for name_en, name_bn, is_mand, clar in ss_docs:
            SchemeDocument.objects.get_or_create(
                scheme=ss, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 7: Rupashree Prakalpa (রূপশ্রী প্রকল্প)
        # -------------------------------------------------------------
        rupa, _ = Scheme.objects.get_or_create(
            slug="rupashree-prakalpa",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Rupashree Prakalpa",
                "name_bn": "রূপশ্রী প্রকল্প",
                "name_hi": "रूपश्री प्रकल्प",
                "tagline_en": "One-time financial assistance of ₹25,000 for adult girl's marriage",
                "tagline_bn": "দরিদ্র পরিবারের প্রাপ্তবয়স্ক কন্যার বিয়ের খরচের জন্য এককালীন ২৫,০০০ টাকার সহায়তা",
                "description_en": "Rupashree Prakalpa provides a one-time financial grant of Rs. 25,000 to economically stressed families at the time of their adult daughter's marriage (annual family income up to Rs. 1.5 Lakh).",
                "description_bn": "যেসব পরিবারের বার্ষিক আয় ১.৫ লক্ষ টাকার কম, তাদের প্রাপ্তবয়স্ক কন্যার বিয়ের উদ্দেশ্যে এককালীন ২৫,০০০ টাকা সরাসরি কন্যার ব্যাংক অ্যাকাউন্টে জমা দেওয়া হয়।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "₹25,000 (One-time grant before marriage)",
                "benefit_amount_text_bn": "এককালীন ২৫,০০০ টাকা (বিয়ের পূর্বে)",
                "application_channels": ["BDO Office (Rural)", "SDO / Municipality Office (Urban)", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbrupashree.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=rupa,
            defaults={
                "min_age": 18,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "max_family_income": 150000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Applicant girl must be at least 18 years old, groom must be at least 21 years old. Annual family income must not exceed ₹1,50,000. Application must be submitted at least 30-60 days before the wedding date.",
                "rules_summary_bn": "কন্যার বয়স ন্যূনতম ১৮ এবং পাত্রের বয়স ন্যূনতম ২১ বছর হতে হবে। পারিবারিক বার্ষিক আয় ১.৫০ লক্ষ টাকার মধ্যে হতে হবে এবং বিয়ের তারিখের অন্তত ৩০-৬০ দিন আগে আবেদন জমা দিতে হবে।"
            }
        )
        rupa_docs = [
            ("Age Proof of Bride & Groom", "পাত্র ও পাত্রীর বয়সের প্রমাণপত্র", True, "Birth Certificate / Admit Card"),
            ("Wedding Invitation Card", "বিয়ের নিমন্ত্রণ পত্র", True, "Printed wedding card"),
            ("Income Certificate", "পারিবারিক আয়ের সার্টিফিকেট", True, "Issued by Pradhan / Councillor / SDO"),
            ("Bride's Single Bank Passbook", "কন্যার নিজস্ব ব্যাংক পাসবুক", True, "Payment is transferred directly to bride")
        ]
        for name_en, name_bn, is_mand, clar in rupa_docs:
            SchemeDocument.objects.get_or_create(
                scheme=rupa, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 8: West Bengal Student Credit Card (WBSCC)
        # -------------------------------------------------------------
        wbscc, _ = Scheme.objects.get_or_create(
            slug="wb-student-credit-card",
            defaults={
                "department": higher_edu,
                "category": "education",
                "name_en": "West Bengal Student Credit Card (WBSCC)",
                "name_bn": "স্টুডেন্ট ক্রেডিট কার্ড স্কিম",
                "name_hi": "स्टूडेंट क्रेडिट कार्ड",
                "tagline_en": "Concessional education loan up to ₹10 Lakh for higher studies",
                "tagline_bn": "উচ্চশিক্ষার জন্য ১০ লক্ষ টাকা পর্যন্ত স্বল্প সুদে শিক্ষা ঋণ সহায়তা",
                "description_en": "Offers education loans up to Rs. 10 Lakh at nominal 4% simple interest with state government guarantee for studying in India or abroad, repayable over 15 years.",
                "description_bn": "ভারত বা বিদেশে উচ্চশিক্ষার জন্য সর্বোচ্চ ১০ লক্ষ টাকা পর্যন্ত মাত্র ৪% সরল সুদে শিক্ষা ঋণ। রাজ্য সরকার এর গ্যারান্টার থাকে এবং কোর্স শেষ হওয়ার পর ১৫ বছর পর্যন্ত পরিশোধের সুযোগ থাকে।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Up to ₹10,00,000 Loan (4% simple interest)",
                "benefit_amount_text_bn": "১০,০০,০০০ টাকা পর্যন্ত শিক্ষা ঋণ (৪% সরল সুদ)",
                "application_channels": ["WBSCC Online Portal", "Higher Education Institutions", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbscc.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=wbscc,
            defaults={
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B"],
                "rules_summary_en": "Student must have resided in WB for at least 10 years, enrolled in Class 10/12/UG/PG/Professional courses, age up to 40 years.",
                "rules_summary_bn": "পশ্চিমবঙ্গে অন্তত ১০ বছর বসবাসকারী শিক্ষার্থী হতে হবে, বয়স সর্বোচ্চ ৪০ বছর এবং কোনো স্বীকৃত উচ্চশিক্ষা কোর্সে পাঠরত হতে হবে।"
            }
        )
        wbscc_docs = [
            ("Admission Proof / Course Fee Structure", "ভর্তির প্রমাণপত্র ও কোর্স ফি স্ট্রাকচার", True, "Issued by university/college"),
            ("Student & Co-borrower Aadhaar", "শিক্ষার্থী ও অভিভাবকের আধার কার্ড", True, "Identification"),
            ("PAN Card of Student / Guardian", "প্যান কার্ড", True, "Bank loan documentation"),
            ("Last Qualifying Marksheet", "সর্বশেষ পরীক্ষার মার্কশীট", True, "Academic record")
        ]
        for name_en, name_bn, is_mand, clar in wbscc_docs:
            SchemeDocument.objects.get_or_create(
                scheme=wbscc, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 9: Aikyashree Scholarship (ঐক্যশ্রী)
        # -------------------------------------------------------------
        aikya, _ = Scheme.objects.get_or_create(
            slug="aikyashree",
            defaults={
                "department": minority,
                "category": "education",
                "name_en": "Aikyashree (Minority Scholarship)",
                "name_bn": "ঐক্যশ্রী (সংখ্যালঘু বৃত্তি প্রকল্প)",
                "name_hi": "ऐक्यश्री",
                "tagline_en": "State scholarships for students belonging to minority communities",
                "tagline_bn": "সংখ্যালঘু সম্প্রদায়ের মেধাবী ছাত্রছাত্রীদের জন্য প্রাক-ম্যাট্রিক ও উত্তর-ম্যাট্রিক বৃত্তি",
                "description_en": "Aikyashree provides financial scholarships (Pre-matric, Post-matric, Merit-cum-Means, and SVMCM) to students belonging to minority communities (Muslim, Christian, Buddhist, Sikh, Jain, Parsi) in West Bengal.",
                "description_bn": "পশ্চিমবঙ্গের সংখ্যালঘু সম্প্রদায়ের (মুসলিম, খ্রিস্টান, বৌদ্ধ, শিখ, জৈন, পার্সি) শিক্ষার্থীদের প্রথম শ্রেণী থেকে পিএইচডি স্তর পর্যন্ত প্রাক-ম্যাট্রিক, উত্তর-ম্যাট্রিক ও মেধাবৃত্তি প্রদান করা হয়।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹1,100 to ₹33,000 / year (depending on course level)",
                "benefit_amount_text_bn": "কোর্স অনুযায়ী বছরে ১,১০০ থেকে ৩৩,০০০ টাকা",
                "application_channels": ["Aikyashree WBMDFC Portal", "School / College Verification"],
                "official_portal_url": "https://wbmdfc.org"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=aikya,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["Minority"],
                "max_family_income": 200000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Student belonging to religious minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) with at least 50% marks in previous exam and family income under ₹2 Lakh/year.",
                "rules_summary_bn": "ধর্মীয় সংখ্যালঘু সম্প্রদায়ের শিক্ষার্থী, পূর্ববর্তী পরীক্ষায় অন্তত ৫০% নম্বর এবং পারিবারিক বার্ষিক আয় ২ লক্ষ টাকার মধ্যে হতে হবে।"
            }
        )
        aikya_docs = [
            ("Previous Exam Marksheet", "পূর্ববর্তী পরীক্ষার মার্কশীট", True, "Minimum 50% marks"),
            ("Minority Community Declaration", "সংখ্যালঘু সম্প্রদায়ের স্বঘোষণাপত্র", True, "Self declaration"),
            ("Income Certificate", "বার্ষিক আয়ের প্রমাণপত্র", True, "Income below ₹2,00,000"),
            ("Bank Passbook", "ছাত্র/ছাত্রীর নিজস্ব ব্যাংক পাসবুক", True, "Aadhaar seeded single account")
        ]
        for name_en, name_bn, is_mand, clar in aikya_docs:
            SchemeDocument.objects.get_or_create(
                scheme=aikya, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Scheme 10: Sikshashree (শিক্ষাশ্রী)
        # -------------------------------------------------------------
        siksha, _ = Scheme.objects.get_or_create(
            slug="sikshashree",
            defaults={
                "department": bcwd,
                "category": "education",
                "name_en": "Sikshashree",
                "name_bn": "শিক্ষাশ্রী",
                "name_hi": "शिक्षाश्री",
                "tagline_en": "Assistance for SC/ST day-scholar students in Classes V to VIII",
                "tagline_bn": "পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত তফসিলি জাতি ও উপজাতির শিক্ষার্থীদের জন্য শিক্ষা সহায়তা",
                "description_en": "Provides an annual financial assistance of Rs. 800 to SC and ST day-scholar students studying in classes V to VIII in government or recognized schools to reduce dropout rates.",
                "description_bn": "স্কুলছুট কমাতে সরকারি ও সরকার পোষিত বিদ্যালয়ে পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত তফশিলি জাতি (SC) ও উপজাতি (ST) ছাত্রছাত্রীদের বার্ষিক ৮০০ টাকা সহায়তা প্রদান করা হয়।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹800 / year",
                "benefit_amount_text_bn": "বার্ষিক ৮০০ টাকা",
                "application_channels": ["Through School", "Oasis Portal"],
                "official_portal_url": "https://oasis.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=siksha,
            defaults={
                "min_age": 10,
                "max_age": 15,
                "gender_allowed": "all",
                "caste_categories": ["SC", "ST"],
                "max_family_income": 250000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "SC or ST day-scholar student studying in Class V to VIII, family income not exceeding ₹2.5 Lakh per year.",
                "rules_summary_bn": "তফসিলি জাতি বা উপজাতির শিক্ষার্থী, পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত এবং পারিবারিক বার্ষিক আয় ২.৫ লক্ষ টাকার মধ্যে হতে হবে।"
            }
        )
        siksha_docs = [
            ("Caste Certificate (SC/ST)", "তফসিলি জাতি/উপজাতি সার্টিফিকেট", True, "Issued by competent authority"),
            ("School Study Certificate", "বিদ্যালয়ের পাঠরত থাকার সার্টিফিকেট", True, "From Head of Institution"),
            ("Student Bank Passbook", "ছাত্রছাত্রীর ব্যাংক পাসবুক", True, "With IFSC details"),
            ("Income Certificate", "পারিবারিক আয়ের সার্টিফিকেট", True, "Under ₹2.5 Lakh")
        ]
        for name_en, name_bn, is_mand, clar in siksha_docs:
            SchemeDocument.objects.get_or_create(
                scheme=siksha, name_en=name_en,
                defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
            )

        # -------------------------------------------------------------
        # Official Directories & Grievance Offices
        # -------------------------------------------------------------
        OfficialDirectory.objects.get_or_create(
            office_type="cmo_cell",
            district="Statewide",
            defaults={
                "designation": "Chief Minister's Grievance Cell (Didi ke Bolo)",
                "office_address": "Nabanna, 325 Sarat Chatterjee Road, Howrah 711102",
                "contact_phone": "9137091370",
                "grievance_portal_url": "https://wb.gov.in"
            }
        )

        OfficialDirectory.objects.get_or_create(
            office_type="prd_portal",
            district="Statewide",
            defaults={
                "designation": "Panchayats & Rural Development Grievance Redressal",
                "office_address": "Joint Administrative Building, HC-7, Sector-III, Salt Lake, Kolkata 700106",
                "contact_phone": "1800-345-3200",
                "grievance_portal_url": "https://prd.wb.gov.in"
            }
        )

        OfficialDirectory.objects.get_or_create(
            office_type="duare_sarkar",
            district="Statewide",
            defaults={
                "designation": "Duare Sarkar State Monitoring Desk",
                "office_address": "State Secretariat Nabanna, Mandirtala, Shibpur, Howrah",
                "contact_phone": "033-2214-0152",
                "grievance_portal_url": "https://ds.wb.gov.in"
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded 10 core West Bengal schemes and departments!"))
