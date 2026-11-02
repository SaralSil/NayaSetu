from django.core.management.base import BaseCommand
from apps.schemes.models import Department, Scheme, SchemeEligibility, SchemeDocument, CommonRejectionReason
from apps.grievances.models import OfficialDirectory

class Command(BaseCommand):
    help = "Seed verified 2026 West Bengal Welfare Schemes, eligibility rules, and departments"

    def handle(self, *args, **options):
        self.stdout.write("Seeding West Bengal Departments...")

        # -------------------------------------------------------------
        # 1. Departments
        # -------------------------------------------------------------
        wcd, _ = Department.objects.get_or_create(
            code="wcd",
            defaults={
                "name_en": "Department of Women & Child Development and Social Welfare",
                "name_bn": "নারী ও শিশু বিকাশ এবং সমাজকল্যাণ দপ্তর",
                "name_hi": "महिला एवं बाल विकास और समाज कल्याण विभाग",
                "portal_url": "https://socialsecurity.wb.gov.in",
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
                "name_hi": "जनजातीय विकास विभाग",
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

        nha, _ = Department.objects.get_or_create(
            code="nha",
            defaults={
                "name_en": "National Health Authority (Ayushman Bharat)",
                "name_bn": "জাতীয় স্বাস্থ্য কর্তৃপক্ষ (আয়ুষ্মান ভারত)",
                "name_hi": "राष्ट्रीय स्वास्थ्य प्राधिकरण (आयुष्मान भारत)",
                "portal_url": "https://beneficiary.nha.gov.in",
                "helpline": "14555"
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

        school_edu, _ = Department.objects.get_or_create(
            code="school_edu",
            defaults={
                "name_en": "School Education Department",
                "name_bn": "বিদ্যালয় শিক্ষা দপ্তর",
                "name_hi": "स्कूल शिक्षा विभाग",
                "portal_url": "https://school.banglarshiksha.gov.in",
                "helpline": "033-2337-8311"
            }
        )

        youth_dept, _ = Department.objects.get_or_create(
            code="youth",
            defaults={
                "name_en": "Department of Youth Services and Sports",
                "name_bn": "যুব কল্যাণ ও ক্রীড়া দপ্তর",
                "name_hi": "युवा सेवा एवं खेल विभाग",
                "portal_url": "https://yubasathi.wb.gov.in",
                "helpline": "1800-345-8243"
            }
        )

        prd, _ = Department.objects.get_or_create(
            code="prd",
            defaults={
                "name_en": "Panchayat & Rural Development Department",
                "name_bn": "পঞ্চায়েত ও গ্রামোন্নয়ন দপ্তর",
                "name_hi": "पंचायत और ग्रामीण विकास विभाग",
                "portal_url": "https://wbprd.gov.in",
                "helpline": "1800-345-3200"
            }
        )

        msme, _ = Department.objects.get_or_create(
            code="msme",
            defaults={
                "name_en": "Micro, Small & Medium Enterprises and Textiles Department",
                "name_bn": "ক্ষুদ্র, ছোট ও মাঝারি শিল্প দপ্তর",
                "name_hi": "सूक्ष्म, लघु एवं मध्यम उद्यम विभाग",
                "portal_url": "https://bccs.wb.gov.in",
                "helpline": "033-2214-5555"
            }
        )

        fisheries, _ = Department.objects.get_or_create(
            code="fisheries",
            defaults={
                "name_en": "Department of Fisheries",
                "name_bn": "মৎস্য বিভাগ",
                "name_hi": "मत्स्य विभाग",
                "portal_url": "https://wbfisheries.gov.in",
                "helpline": "033-2357-0077"
            }
        )

        food, _ = Department.objects.get_or_create(
            code="food",
            defaults={
                "name_en": "Food and Supplies Department",
                "name_bn": "খাদ্য ও সরবরাহ দপ্তর",
                "name_hi": "खाद्य एवं आपूर्ति विभाग",
                "portal_url": "https://food.wb.gov.in",
                "helpline": "1800-345-5505"
            }
        )

        self.stdout.write("Seeding Active 2026 West Bengal Welfare Schemes...")

        # Helper function for adding scheme documents
        def set_docs(scheme_obj, docs_list):
            for name_en, name_bn, is_mand, clar in docs_list:
                SchemeDocument.objects.update_or_create(
                    scheme=scheme_obj, name_en=name_en,
                    defaults={"name_bn": name_bn, "is_mandatory": is_mand, "clarification_en": clar}
                )

        # -------------------------------------------------------------
        # Scheme 1: Annapurna Bhandar / Lakshmir Bhandar (2026 Active)
        # -------------------------------------------------------------
        lb, _ = Scheme.objects.update_or_create(
            slug="lakshmir-bhandar",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Annapurna Bhandar / Lakshmir Bhandar",
                "name_bn": "অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার",
                "name_hi": "अन्नपूर्णा भंडार / लक्ष्मी भंडार",
                "tagline_en": "Universal monthly financial grant of ₹3,000 for adult women in West Bengal",
                "tagline_bn": "পশ্চিমবঙ্গের মহিলাদের সার্বিক আর্থিক ক্ষমতায়নের জন্য মাসিক ৩,০০০ টাকা সহায়তা ও বিনামূল্যে বাস যাত্রা",
                "tagline_hi": "पश्चिम बंगाल की वयस्क महिलाओं के लिए ₹3,000 मासिक वित्तीय सहायता और मुफ्त बस यात्रा",
                "description_en": "Annapurna Bhandar (evolved from Lakshmir Bhandar) provides a monthly direct financial transfer of Rs. 3,000 directly into the individual bank accounts of resident women aged 25-60 years, along with free transport in state buses.",
                "description_bn": "২৫ থেকে ৬০ বছর বয়সী মহিলাদের জন্য মাসিক ৩,০০০ টাকা সরাসরি নিজস্ব একক ব্যাংক অ্যাকাউন্টে ডিবিটি মারফত প্রদান করা হয় এবং সরকারি বাসে বিনামূল্যে ভ্রমণের সুযোগ প্রদান করা হয়।",
                "description_hi": "25 से 60 वर्ष की महिलाओं को ₹3,000 प्रति माह सीधे उनके एकल बैंक खाते में डीबीटी के माध्यम से दिया जाता है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹3,000 / month (Direct DBT) + Free State Bus Travel",
                "benefit_amount_text_bn": "মাসিক ৩,০০০ টাকা (সরাসরি ব্যাঙ্ক DBT) + বিনামূল্যে বাস ভ্রমণ",
                "application_channels": ["Duare Sarkar Camp", "BDO Office (Rural)", "SDO / Municipality Office (Urban)"],
                "official_portal_url": "https://socialsecurity.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=lb,
            defaults={
                "min_age": 25,
                "max_age": 60,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 1200000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "requires_swasthya_sathi": True,
                "rules_summary_en": "Female resident of West Bengal aged 25-60. Personal monthly income ≤ ₹10,000; family annual income ≤ ₹12 Lakh. Must possess Swasthya Sathi card and single-operated bank account linked to Aadhaar NPCI. Non-taxpayer; not a permanent government employee.",
                "rules_summary_bn": "পশ্চিমবঙ্গের ২৫ থেকে ৬০ বছর বয়সী স্থায়ী মহিলা বাসিন্দা। নিজস্ব একক (সিঙ্গেল) সেভিংস ব্যাঙ্ক অ্যাকাউন্ট ও আধার ডিবিটি বাধ্যতামূলক। সরকারি চাকরিজীবী ও আয়করদাতারা ব্যতিত।"
            }
        )
        set_docs(lb, [
            ("Aadhaar Card", "আধার কার্ড", True, "Must be linked with mobile and bank account"),
            ("Swasthya Sathi Card", "স্বাস্থ্য সাথী কার্ড", True, "Card listing applicant woman's name"),
            ("Single Bank Account Passbook", "একক (সিঙ্গেল) ব্যাংক পাসবুক", True, "Joint accounts are STRICTLY NOT ACCEPTED"),
            ("Active Aadhaar-NPCI DBT Mandate", "ব্যাঙ্ক ডিবিটি সক্রিয় প্রমাণ", True, "NPCI seeding active in core banking"),
            ("Passport Photo", "পাসপোর্ট সাইজ ছবি", True, "Recent colour photograph")
        ])

        # -------------------------------------------------------------
        # Scheme 2: West Bengal Yuva Shakti Yojana (2026 Active)
        # -------------------------------------------------------------
        ys, _ = Scheme.objects.update_or_create(
            slug="wb-yuva-shakti",
            defaults={
                "department": youth_dept,
                "category": "youth",
                "name_en": "West Bengal Yuva Shakti Yojana (Yuva Shakti Bharosa Card)",
                "name_bn": "পশ্চিমবঙ্গ যুব শক্তি প্রকল্প (যুব শক্তি ভরসা কার্ড)",
                "name_hi": "पश्चिम बंगाल युवा शक्ति योजना (युवा शक्ति भरोसा कार्ड)",
                "tagline_en": "Monthly allowance of ₹2,000 to ₹3,000 for unemployed educated youth",
                "tagline_bn": "পশ্চিমবঙ্গের শিক্ষিত বেকার যুবক-যুবতীদের জন্য মাসিক ₹২,০০০ থেকে ₹৩,০০০ টাকার ভাতা",
                "tagline_hi": "शिक्षित बेरोजगार युवाओं के लिए ₹2,000 से ₹3,000 मासिक बेरोजगारी भत्ता व कौशल प्रशिक्षण",
                "description_en": "Yuva Shakti provides monthly unemployment and skill-enhancement allowance: Rs. 3,000/month for graduates/post-graduates and Rs. 2,000/month for Madhyamik/HS passed youth aged 21-45 for up to 5 years.",
                "description_bn": "২১ থেকে ৪৫ বছর বয়সী বেকার যুবক-যুবতীদের চাকরির প্রস্তুতি ও দক্ষতার জন্য মাসিক ভাতা: স্নাতকদের ₹৩,০০০ এবং মাধ্যমিক/উচ্চমাধ্যমিক উত্তীর্ণদের ₹২,০০০ টাকা প্রদান করা হয়।",
                "description_hi": "स्नातक युवाओं को ₹3,000/माह और 10वीं/12वीं पास युवाओं को ₹2,000/माह 5 वर्षों तक दिया जाता है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹3,000/mo (Graduates) | ₹2,000/mo (Class 10/12 Pass)",
                "benefit_amount_text_bn": "মাসিক ₹৩,০০০ (স্নাতক) | মাসিক ₹২,০০০ (মাধ্যমিক/উচ্চমাধ্যমিক)",
                "application_channels": ["Yuva Shakti Portal", "Employment Bank", "Duare Sarkar Camp"],
                "official_portal_url": "https://yubasathi.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ys,
            defaults={
                "min_age": 21,
                "max_age": 45,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 100000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Permanent resident of WB aged 21-45, completely unemployed, passed at least Madhyamik. Annual family income below ₹1,00,000.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, বয়স ২১ থেকে ৪৫ বছর, সম্পূর্ণ বেকার এবং পারিবারিক বার্ষিক আয় ১ লক্ষ টাকার নিচে।"
            }
        )
        set_docs(ys, [
            ("Aadhaar Card", "আধার কার্ড", True, "Identity and address proof"),
            ("Educational Certificates / Marksheet", "শিক্ষাগত যোগ্যতার মার্কশিট ও সার্টিফিকেট", True, "Madhyamik/HS/Degree pass certificate"),
            ("Family Income Certificate", "পারিবারিক আয়ের শংসাপত্র", True, "Annual income under ₹1 Lakh"),
            ("Bank Passbook with Aadhaar Seeding", "আধার সংযুক্ত ব্যাংক পাসবই", True, "For direct monthly transfer"),
            ("Employment Exchange / Yuvashree Card", "এমপ্লয়মেন্ট এক্সচেঞ্জ নথিভুক্তি", False, "If already enrolled")
        ])

        # -------------------------------------------------------------
        # Scheme 3: Ayushman Bharat (AB-PMJAY) - Healthcare
        # -------------------------------------------------------------
        ab, _ = Scheme.objects.update_or_create(
            slug="ayushman-bharat",
            defaults={
                "department": nha,
                "category": "health",
                "name_en": "Ayushman Bharat (AB-PMJAY) & Vay Vandana 70+",
                "name_bn": "আয়ুষ্মান ভারত (পিএম-জেএওয়াই) ও ৭৫+ প্রবীণ স্বাস্থ্য সুরক্ষা",
                "name_hi": "आयुष्मान भारत (PM-JAY) एवं 70+ वरिष्ठ नागरिक सुरक्षा",
                "tagline_en": "₹5 Lakh family cashless hospitalization + dedicated ₹5 Lakh for seniors 70+",
                "tagline_bn": "প্রতি পরিবারে বার্ষিক ₹৫ লক্ষ টাকার ক্যাশলেস চিকিৎসা এবং ৭০+ প্রবীণদের জন্য অতিরিক্ত ₹৫ লক্ষ",
                "tagline_hi": "प्रति परिवार प्रति वर्ष ₹5 लाख कैशलेस इलाज एवं 70 वर्ष से अधिक के बुजुर्गों हेतु अतिरिक्त ₹5 लाख",
                "description_en": "Ayushman Bharat PM-JAY provides ₹5,00,000 cashless secondary and tertiary hospital care per family per year, valid across 28,000+ hospitals in India. Every senior citizen aged 70+ receives an additional dedicated ₹5 Lakh cover regardless of income.",
                "description_bn": "সমগ্র ভারতের ২৮,০০০+ হাসপাতালে প্রতি পরিবারের জন্য বছরে ৫ লক্ষ টাকা ক্যাশলেস চিকিৎসা। ৭০ বছর বা তার বেশি বয়সী সকল প্রবীণ নাগরিক পারিবারিক আয়ের কোনো শর্ত ছাড়াই ব্যক্তিগত অতিরিক্ত ৫ লক্ষ টাকার সুবিধা পান।",
                "description_hi": "देश भर के 28,000+ अस्पतालों में ₹5 लाख तक का मुफ्त इलाज। 70 वर्ष से अधिक आयु के सभी नागरिकों को बिना किसी आय सीमा के अलग से ₹5 लाख का कवर।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "₹5,00,000 / family / year (+ Dedicated ₹5 Lakh for Seniors 70+)",
                "benefit_amount_text_bn": "পরিবার পিছু বছরে ₹৫,০০,০০০ (এবং ৭০+ প্রবীণদের জন্য পৃথক ₹৫ লক্ষ)",
                "application_channels": ["Ayushman App", "NHA Beneficiary Portal", "CSC Center", "Hospital Ayushman Mitra Desk"],
                "official_portal_url": "https://beneficiary.nha.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ab,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Families identified under SECC / NFSA ration databases. For Senior Citizens (70+ years), coverage is universal with no income bar.",
                "rules_summary_bn": "জাতীয় খাদ্য সুরক্ষা (NFSA) রেশন কার্ড ও আর্থ-সামাজিক তালিকাভুক্ত পরিবার। ৭০ বা তার বেশি বয়সী প্রবীণদের জন্য সম্পূর্ণ সার্বজনীন।"
            }
        )
        set_docs(ab, [
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory for demographic and biometric e-KYC"),
            ("Active Mobile Number", "সক্রিয় মোবাইল নম্বর", True, "For Aadhaar OTP authentication"),
            ("Digital Ration Card / Family Proof", "ডিজিটাল রেশন কার্ড", True, "To match family membership records")
        ])

        # -------------------------------------------------------------
        # Scheme 4: Swasthya Sathi (স্বাস্থ্য সাথী)
        # -------------------------------------------------------------
        ss, _ = Scheme.objects.update_or_create(
            slug="swasthya-sathi",
            defaults={
                "department": health,
                "category": "health",
                "name_en": "Swasthya Sathi",
                "name_bn": "স্বাস্থ্য সাথী",
                "name_hi": "स्वास्थ्य साथी",
                "tagline_en": "Universal cashless hospital cover up to ₹5 Lakh/year per family",
                "tagline_bn": "পশ্চিমবঙ্গের প্রতিটি পরিবারের জন্য বার্ষিক ৫ লক্ষ টাকা পর্যন্ত ক্যাশলেস স্বাস্থ্য বীমা",
                "tagline_hi": "राज्य के सभी परिवारों के लिए ₹5 लाख तक का कैशलेस स्वास्थ्य सुरक्षा स्मार्ट कार्ड",
                "description_en": "Swasthya Sathi provides cashless hospital coverage up to Rs. 5 Lakh per annum per family on a floater basis. The smart card is issued strictly in the name of the eldest female family member.",
                "description_bn": "পরিবার পিছু প্রতি বছর ৫ লক্ষ টাকা পর্যন্ত ক্যাশলেস চিকিৎসার সুবিধা। এই কার্ডটি পরিবারের বয়োজ্যেষ্ঠা মহিলার নামে ইস্যু করা হয়।",
                "description_hi": "परिवार की वरिष्ठ महिला के नाम पर ₹5 लाख प्रति वर्ष तक कैशलेस इलाज।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "Up to ₹5,00,000 / year (Cashless Family Cover)",
                "benefit_amount_text_bn": "পরিবার পিছু বছরে ৫,০০,০০০ টাকা পর্যন্ত ক্যাশলেস চিকিৎসা",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "Swasthya Sathi Kiosks"],
                "official_portal_url": "https://swasthyasathi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ss,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "All resident families of West Bengal not covered under corporate or central government medical reimbursements.",
                "rules_summary_bn": "পশ্চিমবঙ্গের সমস্ত স্থায়ী পরিবার যারা অন্য কোনো সরকারি রিইমবার্সমেন্ট পান না।"
            }
        )
        set_docs(ss, [
            ("Aadhaar Card of all members", "পরিবারের সকলের আধার কার্ড", True, "For biometric enrollment"),
            ("Digital Ration Card", "ডিজিটাল রেশন কার্ড", True, "Family composition proof"),
            ("Photo of Eldest Female Member", "পরিবারের বয়োজ্যেষ্ঠা মহিলার ছবি", True, "Card issued in her name")
        ])

        # -------------------------------------------------------------
        # Scheme 5: Karmashree (কর্মশ্রী) - 50 Days Rural Work
        # -------------------------------------------------------------
        karm, _ = Scheme.objects.update_or_create(
            slug="karmashree",
            defaults={
                "department": prd,
                "category": "agriculture",
                "name_en": "Karmashree (50-Day Guaranteed Wage Employment)",
                "name_bn": "কর্মশ্রী প্রকল্প (৫০ দিনের নিশ্চিত গ্রামীণ কর্মসংস্থান)",
                "name_hi": "कर्मश्री योजना (50 दिन की गारंटीकृत ग्रामीण मजदूरी)",
                "tagline_en": "State-guaranteed 50 days of manual wage employment for rural Job Card holders",
                "tagline_bn": "গ্রামীণ জব কার্ডধারীদের জন্য রাজ্য সরকারের নিজস্ব ৫০ দিনের নিশ্চিত মজুরি কাজ",
                "tagline_hi": "ग्रामीण जॉब कार्ड धारकों के लिए न्यूनतम 50 दिन का गारंटीकृत रोजगार व मजदूरी",
                "description_en": "Karmashree guarantees at least 50 days of manual wage work for registered rural Job Card holders across West Bengal, funded 100% by the State Government, with direct wage crediting into bank accounts.",
                "description_bn": "পশ্চিমবঙ্গের গ্রামীণ জব কার্ডধারী শ্রমিকদের জন্য বছরে অন্তত ৫০ দিনের নিশ্চিত কাজের সুযোগ। রাজ্য সরকারের নিজস্ব তহবিল থেকে সরাসরি মজুরির টাকা ব্যাংকে জমা হয়।",
                "description_hi": "ग्रामीण परिवारों को प्रति वर्ष 50 दिन का काम और सीधे बैंक खाते में वैधानिक मजदूरी भुगतान।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "50 Days Guaranteed Wage Work per Household",
                "benefit_amount_text_bn": "পরিবার পিছু ৫০ দিনের নিশ্চিত মজুরিসহ কাজ",
                "application_channels": ["Gram Panchayat Office", "BDO Office", "Duare Sarkar Camp"],
                "official_portal_url": "https://karmashree.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=karm,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Rural households holding active Job Cards willing to undertake unskilled manual labor.",
                "rules_summary_bn": "পশ্চিমবঙ্গের গ্রামীণ জব কার্ডধারী প্রাপ্তবয়স্ক ব্যক্তি যারা কায়িক শ্রম করতে ইচ্ছুক।"
            }
        )
        set_docs(karm, [
            ("Rural Job Card", "গ্রামীণ জব কার্ড", True, "Must be valid and active"),
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar authentication"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Account linked with Job Card for wage payment")
        ])

        # -------------------------------------------------------------
        # Scheme 6: Krishak Bandhu (Natun) + PM-Kisan
        # -------------------------------------------------------------
        kb, _ = Scheme.objects.update_or_create(
            slug="krishak-bandhu-natun",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Krishak Bandhu (Natun) & PM-Kisan",
                "name_bn": "কৃষক বন্ধু (নতুন) ও পিএম-কিষাণ সমন্বয়",
                "name_hi": "कृषक बंधु (नया) एवं पीएम-किसान",
                "tagline_en": "Assured farm aid up to ₹16,000/yr + ₹2 Lakh death insurance for farmers",
                "tagline_bn": "কৃষকদের জন্য বছরে ১৬,০০০ টাকা পর্যন্ত অনুদান ও ২ লক্ষ টাকার জীবনাবসান সহায়তা",
                "tagline_hi": "किसानों को प्रति वर्ष ₹16,000 तक की सहायता और ₹2 लाख का जीवन बीमा लाभ",
                "description_en": "Under Krishak Bandhu, farmers receive up to Rs. 10,000/year (minimum Rs. 4,000) in two equal installments, plus Rs. 2,00,000 death benefit for farmer families (aged 18-60). Synchronized PM-Kisan provides an additional Rs. 6,000/year.",
                "description_bn": "১ একর বা বেশি চাষযোগ্য জমির জন্য বছরে ১০,০০০ টাকা (ক্ষুদ্র কৃষকদের ন্যূনতম ৪,০০০ টাকা) এবং কৃষকের স্বাভাবিক বা দুর্ঘটনায় মৃত্যুতে ২ লক্ষ টাকার পরিবার সহায়তা। পিএম-কিষাণ সহ মোট ১৬,০০০ টাকা পর্যন্ত সুবিধা।",
                "description_hi": "1 एकड़ या अधिक भूमि पर ₹10,000/वर्ष (न्यूनतम ₹4,000) तथा ₹2 लाख मृत्यु सहायता।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Up to ₹10,000/yr (Krishak Bandhu) + ₹6,000 (PM-Kisan) + ₹2 Lakh Death Benefit",
                "benefit_amount_text_bn": "বছরে ১০,০০০ টাকা পর্যন্ত (+ ৬,০০০ পিএম-কিষাণ) + ২ লক্ষ টাকা মৃত্যু সুবিধা",
                "application_channels": ["Assistant Director of Agriculture (ADA) Office", "Duare Sarkar Camp", "Portal"],
                "official_portal_url": "https://krishakbandhu.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=kb,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Farmer or recorded bargadar (sharecropper) possessing cultivable land Porcha/RoR mutated in own name.",
                "rules_summary_bn": "পশ্চিমবঙ্গের কৃষক বা নথিবদ্ধ ভাগচাষী এবং নিজস্ব নামে চাষযোগ্য জমির সাম্প্রতিক রেকর্ড (পর্চা) থাকতে হবে।"
            }
        )
        set_docs(kb, [
            ("Land Record (RoR / Porcha)", "জমির সাম্প্রতিক রেকর্ড (পর্চা / খতিয়ান)", True, "Mutated in applicant's name"),
            ("Voter ID Card (EPIC)", "ভোটার কার্ড (EPIC)", True, "Mandatory for Krishak Bandhu verification"),
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory identification"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Clear IFSC and Account number")
        ])

        # -------------------------------------------------------------
        # Scheme 7: Bangla Shasya Bima (BSB) - 100% Free Crop Insurance
        # -------------------------------------------------------------
        bsb, _ = Scheme.objects.update_or_create(
            slug="bangla-shasya-bima",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Bangla Shasya Bima (BSB)",
                "name_bn": "বাংলা শস্য বীমা (১০০% বিনামূল্যে ফসল সুরক্ষা)",
                "name_hi": "बांग्ला शस्य बीमा (BSB - 100% मुफ्त फसल बीमा)",
                "tagline_en": "100% state-paid comprehensive crop loss insurance against natural disasters",
                "tagline_bn": "প্রাকৃতিক দুর্যোগে ফসল নষ্ট হলে ক্ষতিপূরণ — কৃষকদের কোনো প্রিমিয়াম দিতে হয় না",
                "tagline_hi": "सूखा, बाढ़ या कीटों से फसल नुकसान पर शत-प्रतिशत मुआवजा — किसानों के लिए प्रीमियम बिल्कुल मुफ्त",
                "description_en": "Bangla Shasya Bima is West Bengal's crop insurance where the state government pays 100% of the insurance premium on behalf of farmers for all notified crops (paddy, potato, jute, oilseeds, wheat).",
                "description_bn": "পশ্চিমবঙ্গ সরকার কৃষকদের পক্ষ থেকে শস্য বীমার সম্পূর্ণ প্রিমিয়াম পরিশোধ করে। খরা, বন্যা বা শিলাবৃষ্টিতে ফসল নষ্ট হলে কৃষকদের সরাসরি ব্যাংক অ্যাকাউন্টে ক্ষতিপূরণ প্রদান করা হয়।",
                "description_hi": "फसल बीमा का पूरा प्रीमियम राज्य सरकार भरती है। फसल नुकसान होने पर सीधे बैंक खाते में मुआवजा।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "100% Free Crop Loss Compensation (Zero Premium for Farmers)",
                "benefit_amount_text_bn": "১০০% ক্ষতিপূরণ (কৃষকদের প্রিমিয়াম সম্পূর্ণ বিনামূল্যে)",
                "application_channels": ["ADA Office", "Duare Sarkar Camp", "BSB Portal"],
                "official_portal_url": "https://banglashasyabima.net"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=bsb,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "All cultivating farmers (owner cultivators, tenant farmers, and sharecroppers) growing notified seasonal crops.",
                "rules_summary_bn": "পশ্চিমবঙ্গের সমস্ত চাষী ও ভাগচাষী যারা নির্দিষ্ট মরশুমি ফসল চাষ করছেন।"
            }
        )
        set_docs(bsb, [
            ("Land Porcha / Khatian / Rent Receipt", "জমির পর্চা বা খাজনার রসিদ", True, "Proof of land cultivation"),
            ("Crop Sowing Certificate", "ফসল বপন শংসাপত্র", True, "Certified by Gram Panchayat Pradhan or ADA"),
            ("Aadhaar Card & Voter ID", "আধার ও ভোটার কার্ড", True, "Identification"),
            ("Bank Passbook Copy", "ব্যাংক পাসবুকের জেরক্স", True, "For compensation credit")
        ])

        # -------------------------------------------------------------
        # Scheme 8: Bhabishyat Credit Card Scheme (WBBCCS)
        # -------------------------------------------------------------
        bccs, _ = Scheme.objects.update_or_create(
            slug="bhabishyat-credit-card",
            defaults={
                "department": msme,
                "category": "youth",
                "name_en": "Bhabishyat Credit Card Scheme (WBBCCS)",
                "name_bn": "ভবিষ্যৎ ক্রেডিট কার্ড স্কিম",
                "name_hi": "भविष्य क्रेडिट कार्ड योजना (WBBCCS)",
                "tagline_en": "Collateral-free micro-enterprise business loans up to ₹5 Lakh with 10% subsidy",
                "tagline_bn": "ব্যবসা বা উদ্যোগ শুরুর জন্য ৫ লক্ষ টাকা পর্যন্ত জামানতহীন সহজ ঋণ ও ১০% সরকারি অনুদান",
                "tagline_hi": "युवाओं को नया व्यवसाय शुरू करने के लिए ₹5 लाख तक का गारंटी-मुक्त ऋण व 10% सब्सिडी",
                "description_en": "Provides collateral-free bank loans up to Rs. 5 Lakh for youth aged 18-45 to set up manufacturing, trading, or service enterprises. State provides 10% margin money subsidy (up to ₹25,000) and 85% credit guarantee.",
                "description_bn": "১৮ থেকে ৪৫ বছর বয়সী যুবক-যুবতীদের ব্যবসা, দোকান বা ক্ষুদ্র শিল্প স্থাপনের জন্য কোনো সম্পত্তি বন্ধক ছাড়াই ৫ লক্ষ টাকা পর্যন্ত ব্যাংক ঋণ, সাথে ১০% সরকারি ভর্তুকি।",
                "description_hi": "बिना किसी गारंटी के ₹5 लाख तक का बैंक ऋण, 10% सरकारी सब्सिडी और 85% राज्य गारंटी।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Up to ₹5,00,000 Loan (10% subsidy up to ₹25,000 + 85% guarantee)",
                "benefit_amount_text_bn": "৫,০০,০০০ টাকা পর্যন্ত ঋণ (১০% অনুদান ও ৮৫% রাজ্য গ্যারান্টি)",
                "application_channels": ["BCCS Online Portal", "DIC Office", "Duare Sarkar Camp"],
                "official_portal_url": "https://bccs.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=bccs,
            defaults={
                "min_age": 18,
                "max_age": 45,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Resident of WB for at least 5 years, aged 18-45, minimum Class 8 pass. Setting up a new micro-business.",
                "rules_summary_bn": "পশ্চিমবঙ্গে অন্তত ৫ বছর বসবাসকারী, বয়স ১৮-৪৫ বছর, ন্যূনতম অষ্টম শ্রেণী উত্তীর্ণ এবং নতুন ব্যবসা শুরু করতে ইচ্ছুক।"
            }
        )
        set_docs(bccs, [
            ("Detailed Project Report (DPR)", "প্রজেক্ট রিপোর্ট বা ব্যবসার পরিকল্পনা", True, "Business cost and profit projection"),
            ("Aadhaar Card", "আধার কার্ড", True, "Proof of identity"),
            ("Residential Proof", "আবাসিক প্রমাণপত্র", True, "Voter ID / Ration card"),
            ("Proof of Business Address", "ব্যবসার ঠিকানার প্রমাণ", True, "Trade license / rent agreement / ownership document"),
            ("Educational Certificate", "শিক্ষাগত যোগ্যতার প্রমাণ", True, "Minimum Class 8 pass")
        ])

        # -------------------------------------------------------------
        # Scheme 9: Banglar Awas Yojana / Paschim Banga Awas
        # -------------------------------------------------------------
        bay, _ = Scheme.objects.update_or_create(
            slug="banglar-awas-yojana",
            defaults={
                "department": prd,
                "category": "social_security",
                "name_en": "Banglar Awas Yojana / Paschim Banga Awas",
                "name_bn": "বাংলার আবাস যোজনা / পশ্চিমবঙ্গ আবাস যোজনা",
                "name_hi": "बांग्लार आवास योजना / पश्चिम बंगाल आवास योजना",
                "tagline_en": "Direct financial aid of ₹1,20,000 to construct durable rural pucca houses",
                "tagline_bn": "কাঁচা বাড়ির বাসিন্দাদের পাকা বাড়ি তৈরির জন্য ১,২০,০০০ টাকার সরাসরি আর্থিক অনুদান",
                "tagline_hi": "ग्रामीण गरीबों को पक्का मकान बनाने हेतु ₹1,20,000 की सीधी आर्थिक सहायता",
                "description_en": "Banglar Awas Yojana provides financial assistance of Rs. 1,20,000 in 3 milestone installments directly into the beneficiary's bank account to construct a permanent pucca house with sanitary toilet.",
                "description_bn": "গৃহহীন এবং কাঁচা মাটির বা ভাঙাচোরা বাড়িতে বসবাসকারী গ্রামীণ পরিবারের নিজস্ব পাকা ঘর নির্মাণের জন্য তিন কিস্তিতে মোট ১,২০,০০০ টাকা প্রদান করা হয়।",
                "description_hi": "ग्रामीण आवासहीन व कच्चे मकानों में रहने वाले परिवारों को पक्का घर बनाने हेतु ₹1.20 लाख की सहायता।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "₹1,20,000 Cash Grant (in 3 installments: ₹60k + ₹50k + ₹10k)",
                "benefit_amount_text_bn": "১,২০,০০০ টাকা অনুদান (৩ কিস্তিতে: ৬০হাজার + ৫০হাজার + ১০হাজার)",
                "application_channels": ["Gram Panchayat Verification", "BDO Office Survey", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbprd.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=bay,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Houseless families or households residing in temporary, kutcha or dilapidated structures with no pucca house in family.",
                "rules_summary_bn": "পরিবারে কোনো পাকা বাড়ি নেই এবং গ্রামীণ কাঁচা মাটির ঘরে বসবাসকারী গৃহহীন পরিবার।"
            }
        )
        set_docs(bay, [
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory verification"),
            ("Digital Ration Card", "ডিজিটাল রেশন কার্ড", True, "Family unit identification"),
            ("Bank Account Passbook", "ব্যাংক পাসবুক", True, "Must be linked to Aadhaar for direct DBT transfer"),
            ("Geo-tagged Photo of Kutcha House", "বিদ্যমান কাঁচা বাড়ির ছবি", True, "Inspected by BDO surveyor")
        ])

        # -------------------------------------------------------------
        # Scheme 10: Taruner Swapno (তরুণের স্বপ্ন)
        # -------------------------------------------------------------
        ts, _ = Scheme.objects.update_or_create(
            slug="taruner-swapno",
            defaults={
                "department": school_edu,
                "category": "education",
                "name_en": "Taruner Swapno",
                "name_bn": "তরুণের স্বপ্ন (ট্যাব ও স্মার্টফোন অনুদান)",
                "name_hi": "तरुणेर स्वप्न (टैबलेट/स्मार्टफोन अनुदान)",
                "tagline_en": "One-time DBT grant of ₹10,000 to Class 11 students for digital learning devices",
                "tagline_bn": "একাদশ শ্রেণীর ছাত্রছাত্রীদের ট্যাব বা স্মার্টফোন কেনার জন্য এককালীন ১০,০০০ টাকার অনুদান",
                "tagline_hi": "11वीं कक्षा के छात्रों को टैबलेट या स्मार्टफोन खरीदने हेतु ₹10,000 का एकमुश्त अनुदान",
                "description_en": "Taruner Swapno provides a one-time grant of Rs. 10,000 transferred via DBT directly into the bank accounts of Class 11 students across all government and aided schools for digital learning.",
                "description_bn": "ডিজিটাল শিক্ষার প্রসারে রাজ্যের সমস্ত সরকারি ও সরকার পোষিত বিদ্যালয় এবং মাদ্রাসার একাদশ শ্রেণীর শিক্ষার্থীদের নিজস্ব স্মার্টফোন বা ট্যাব কেনার জন্য এককালীন ১০,০০০ টাকা দেওয়া হয়।",
                "description_hi": "कक्षा 11 के सभी छात्रों को ऑनलाइन पढ़ाई के लिए ₹10,000 की सहायता सीधे बैंक खाते में।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹10,000 (One-time DBT for Tablet / Phone)",
                "benefit_amount_text_bn": "এককালীন ১০,০০০ টাকা (ডিজিটাল ডিভাইস কিনতে)",
                "application_channels": ["Through School (Banglar Shiksha Portal)"],
                "official_portal_url": "https://school.banglarshiksha.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ts,
            defaults={
                "min_age": 15,
                "max_age": 19,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Enrolled regular student in Class 11 in government, aided, or recognized madrasahs in West Bengal.",
                "rules_summary_bn": "পশ্চিমবঙ্গের সরকারি বা সরকার পোষিত বিদ্যালয় ও মাদ্রাসায় একাদশ শ্রেণীতে নিয়মিত পাঠরত শিক্ষার্থী।"
            }
        )
        set_docs(ts, [
            ("School Admission / Enrollment ID", "বিদ্যালয়ে ভর্তির প্রমাণ (Student ID)", True, "Banglar Shiksha student code"),
            ("Student Aadhaar Card", "শিক্ষার্থীর আধার কার্ড", True, "Mandatory"),
            ("Student Single Bank Passbook", "ছাত্রছাত্রীর নিজস্ব ব্যাংক পাসবই", True, "Single account in student's own name")
        ])

        # -------------------------------------------------------------
        # Scheme 11: West Bengal Student Credit Card (WBSCC)
        # -------------------------------------------------------------
        wbscc, _ = Scheme.objects.update_or_create(
            slug="wb-student-credit-card",
            defaults={
                "department": higher_edu,
                "category": "education",
                "name_en": "West Bengal Student Credit Card (WBSCC)",
                "name_bn": "স্টুডেন্ট ক্রেডিট কার্ড স্কিম",
                "name_hi": "स्टूडेंट क्रेडिट कार्ड योजना",
                "tagline_en": "Higher education loans up to ₹10 Lakh at nominal 4% simple interest",
                "tagline_bn": "উচ্চশিক্ষার জন্য ১০ লক্ষ টাকা পর্যন্ত স্বল্প সুদে শিক্ষা ঋণ সহায়তা",
                "tagline_hi": "उच्च शिक्षा के लिए राज्य सरकार की गारंटी पर ₹10 लाख तक का शिक्षा ऋण (4% ब्याज)",
                "description_en": "Provides collateral-free education loans up to Rs. 10 Lakh at 4% simple interest with 100% state government guarantee for pursuing higher education in India or abroad, repayable over 15 years.",
                "description_bn": "ভারত বা বিদেশে উচ্চশিক্ষার জন্য সর্বোচ্চ ১০ লক্ষ টাকা পর্যন্ত মাত্র ৪% সরল সুদে শিক্ষা ঋণ। কোর্স শেষ হওয়ার পর ১৫ বছর পরিশোধের সুযোগ।",
                "description_hi": "भारत या विदेश में उच्च शिक्षा हेतु ₹10 लाख तक का ऋण, 15 साल की आसान वापसी अवधि।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Up to ₹10,00,000 Loan (4% simple interest, 15-year tenure)",
                "benefit_amount_text_bn": "১০,০০,০০০ টাকা পর্যন্ত শিক্ষা ঋণ (৪% সরল সুদ)",
                "application_channels": ["WBSCC Online Portal", "College Desk", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbscc.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=wbscc,
            defaults={
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Student residing in WB for at least 10 years, enrolled in Class 10/12/UG/PG/Professional courses, age up to 40 years.",
                "rules_summary_bn": "পশ্চিমবঙ্গে অন্তত ১০ বছর বসবাসকারী শিক্ষার্থী, বয়স সর্বোচ্চ ৪০ বছর এবং উচ্চশিক্ষায় পাঠরত।"
            }
        )
        set_docs(wbscc, [
            ("Admission Proof & Fee Structure", "ভর্তির প্রমাণপত্র ও কোর্স ফি তালিকা", True, "From college/university"),
            ("Student & Co-borrower Aadhaar & PAN", "আধার কার্ড ও প্যান কার্ড", True, "Mandatory KYC"),
            ("Last Qualifying Marksheet", "সর্বশেষ পরীক্ষার মার্কশিট", True, "Academic pass record")
        ])

        # -------------------------------------------------------------
        # Scheme 12: Swami Vivekananda Merit-cum-Means (SVMCM)
        # -------------------------------------------------------------
        svmcm, _ = Scheme.objects.update_or_create(
            slug="svmcm-scholarship",
            defaults={
                "department": higher_edu,
                "category": "education",
                "name_en": "Swami Vivekananda Merit-cum-Means Scholarship (SVMCM)",
                "name_bn": "স্বামী বিবেকানন্দ মেরিট-কাম-মিনস স্কলারশিপ (বিকাশ ভবন)",
                "name_hi": "स्वामी विवेकानंद मेरिट-कम-मीन्स स्कॉलरशिप (SVMCM)",
                "tagline_en": "High-value merit scholarship from ₹1,000 to ₹5,000/month for HS, UG, and PG students",
                "tagline_bn": "উচ্চমাধ্যমিক, স্নাতক ও স্নাতকোত্তর শিক্ষার্থীদের জন্য মাসিক ₹১,০০০ থেকে ₹৫,০০০ টাকার স্কলারশিপ",
                "tagline_hi": "मेधावी छात्र-छात्राओं के लिए ₹1,000 से ₹5,000 मासिक उच्च शिक्षा छात्रवृत्ति",
                "description_en": "SVMCM provides financial assistance from ₹1,000 to ₹5,000 per month for regular students studying in Class 11, 12, UG, PG, Engineering, and Medical courses with at least 60% marks and family income ≤ ₹2.5 Lakh.",
                "description_bn": "মাধ্যমিক বা পূর্ববর্তী পরীক্ষায় ন্যূনতম ৬০% নম্বর এবং পারিবারিক বার্ষিক আয় ২.৫ লক্ষ টাকার মধ্যে থাকা মেধাবী শিক্ষার্থীদের মাসিক ₹১,০০০ থেকে ₹৫,০০০ পর্যন্ত বৃত্তি প্রদান করা হয়।",
                "description_hi": "कक्षा 11 से लेकर पीजी, इंजीनियरिंग व मेडिकल छात्रों के लिए ₹1,000 से ₹5,000 मासिक छात्रवृत्ति (न्यूनतम 60% अंक)।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹1,000 to ₹5,000 / month (Course level dependent)",
                "benefit_amount_text_bn": "মাসিক ₹১,০০০ থেকে ₹৫,০০০ টাকা",
                "application_channels": ["SVMCM Online Portal (svmcm.wbhed.gov.in)"],
                "official_portal_url": "https://svmcm.wbhed.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=svmcm,
            defaults={
                "min_age": 14,
                "max_age": 35,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 250000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Resident of WB with at least 60% marks in qualifying exam and family income ≤ ₹2.5 Lakh/year.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, পূর্ববর্তী পরীক্ষায় ৬০% বা তার বেশি নম্বর এবং পরিবারের বার্ষিক আয় সর্বোচ্চ ২.৫ লক্ষ টাকা।"
            }
        )
        set_docs(svmcm, [
            ("Marksheet of Qualifying Exam", "শেষ পরীক্ষার মার্কশিট (উভয় পিঠ)", True, "Minimum 60% marks"),
            ("Current Course Admission Receipt", "ভর্তির রশিদ ও ফি স্লিপ", True, "Institutional proof"),
            ("Family Income Certificate", "পারিবারিক আয়ের শংসাপত্র (BDO/SDO দ্বারা)", True, "Income under ₹2.5 Lakh"),
            ("Student Bank Passbook", "ছাত্রছাত্রীর নিজস্ব ব্যাংক পাসবই", True, "Aadhaar seeded single account")
        ])

        # -------------------------------------------------------------
        # Scheme 13: Kanyashree Prakalpa (K1, K2 & K3)
        # -------------------------------------------------------------
        kanya, _ = Scheme.objects.update_or_create(
            slug="kanyashree-prakalpa",
            defaults={
                "department": wcd,
                "category": "education",
                "name_en": "Kanyashree Prakalpa (K1, K2 & K3)",
                "name_bn": "কন্যাশ্রী প্রকল্প (কে-১, কে-২ ও কে-৩)",
                "name_hi": "कन्याश्री प्रकल्प (K1, K2 एवं K3)",
                "tagline_en": "Annual scholarship of ₹1,000 and one-time grant of ₹25,000 for girls' education",
                "tagline_bn": "মেয়েদের পড়াশোনা চালিয়ে যেতে বার্ষিক ₹১,০০০ এবং ১৮ বছর বয়সে এককালীন ₹২৫,০০০ অনুদান",
                "tagline_hi": "बालिकाओं की शिक्षा जारी रखने हेतु ₹1,000 वार्षिक और 18 वर्ष पर ₹25,000 का एकमुश्त अनुदान",
                "description_en": "K1 provides an annual scholarship of Rs. 1,000 for unmarried girls aged 13-18 (Classes 8-12). K2 provides a one-time grant of Rs. 25,000 when turning 18 while continuing education unmarried. K3 supports post-graduate university studies.",
                "description_bn": "১৩-১৮ বছর বয়সী অবিবাহিত ছাত্রীদের বার্ষিক ১,০০০ টাকা (K1) এবং ১৮ বছর পূর্ণ হলে অবিবাহিত অবস্থায় পড়াশোনা চালিয়ে যাওয়ার জন্য এককালীন ২৫,০০০ টাকা (K2)।",
                "description_hi": "अविवाहित छात्राओं को सालाना ₹1,000 और 18 वर्ष पूर्ण होने पर ₹25,000 की प्रोत्साहन राशि।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "K1: ₹1,000/yr | K2: ₹25,000 one-time | K3: ₹2,000-₹2,500/mo",
                "benefit_amount_text_bn": "কে-১: বার্ষিক ১,০০০ টাকা | কে-২: এককালীন ২৫,০০০ টাকা",
                "application_channels": ["Through School / College", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbkanyashree.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=kanya,
            defaults={
                "min_age": 13,
                "max_age": 25,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Unmarried girl student residing in West Bengal, enrolled in recognized school/college. K1: age 13-18. K2: age 18-19.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, অবিবাহিত ছাত্রী এবং কোনো স্বীকৃত বিদ্যালয়/কলেজে পাঠরত।"
            }
        )
        set_docs(kanya, [
            ("School Enrollment Certificate", "বিদ্যালয়ে ভর্তির প্রমাণপত্র", True, "Signed by Headmaster/Principal"),
            ("Unmarried Declaration", "অবিবাহিত থাকার ঘোষণাপত্র", True, "Signed by student & guardian"),
            ("Aadhaar Card", "আধার কার্ড", True, "Student's own Aadhaar"),
            ("Single Bank Passbook", "ছাত্রীর নিজস্ব ব্যাংক পাসবুক", True, "Single account in student's name")
        ])

        # -------------------------------------------------------------
        # Scheme 14: Rupashree Prakalpa (রূপশ্রী প্রকল্প)
        # -------------------------------------------------------------
        rupa, _ = Scheme.objects.update_or_create(
            slug="rupashree-prakalpa",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Rupashree Prakalpa",
                "name_bn": "রূপশ্রী প্রকল্প",
                "name_hi": "रूपश्री प्रकल्प",
                "tagline_en": "One-time financial grant of ₹25,000 for adult girl's marriage in low-income families",
                "tagline_bn": "দরিদ্র পরিবারের প্রাপ্তবয়স্ক কন্যার বিয়ের খরচের জন্য এককালীন ২৫,০০০ টাকার সহায়তা",
                "tagline_hi": "कम आय वाले परिवारों की बेटियों के विवाह हेतु ₹25,000 का एकमुश्त आर्थिक अनुदान",
                "description_en": "Rupashree Prakalpa provides a one-time grant of Rs. 25,000 directly into the bride's bank account before her marriage (family annual income up to Rs. 1.5 Lakh).",
                "description_bn": "যেসব পরিবারের বার্ষিক আয় ১.৫ লক্ষ টাকার কম, তাদের প্রাপ্তবয়স্ক কন্যার বিয়ের উদ্দেশ্যে এককালীন ২৫,০০০ টাকা সরাসরি কন্যার ব্যাংক অ্যাকাউন্টে জমা দেওয়া হয়।",
                "description_hi": "18 वर्ष से अधिक आयु की युवती के विवाह पूर्व ₹25,000 सीधे बैंक खाते में जमा।",
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
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 150000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Bride age ≥ 18 years, groom age ≥ 21 years. Family annual income ≤ ₹1,50,000. Apply 30-60 days before wedding.",
                "rules_summary_bn": "কন্যার বয়স ন্যূনতম ১৮ ও পাত্রের বয়স ন্যূনতম ২১ বছর। পারিবারিক বার্ষিক আয় ১.৫০ লক্ষ টাকার মধ্যে হতে হবে।"
            }
        )
        set_docs(rupa, [
            ("Age Proof of Bride & Groom", "পাত্র ও পাত্রীর বয়সের প্রমাণপত্র", True, "Birth Certificate / Admit Card"),
            ("Wedding Invitation Card", "বিয়ের নিমন্ত্রণ পত্র", True, "Printed wedding card"),
            ("Income Certificate", "পারিবারিক আয়ের শংসাপত্র", True, "Income under ₹1,50,000"),
            ("Bride's Single Bank Passbook", "কন্যার নিজস্ব ব্যাংক পাসবই", True, "Payment transferred directly to bride")
        ])

        # -------------------------------------------------------------
        # Scheme 15: Medhashree (মেধাশ্রী) - OBC Scholarship
        # -------------------------------------------------------------
        medha, _ = Scheme.objects.update_or_create(
            slug="medhashree",
            defaults={
                "department": bcwd,
                "category": "education",
                "name_en": "Medhashree (OBC Pre-Matric Scholarship)",
                "name_bn": "মেধাশ্রী (ওবিসি প্রি-ম্যাট্রিক স্কলারশিপ)",
                "name_hi": "मेधाश्री (OBC प्री-मैट्रिक छात्रवृत्ति)",
                "tagline_en": "Annual scholarship of ₹800 for OBC students studying in Classes V to VIII",
                "tagline_bn": "পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত ওবিসি ছাত্রছাত্রীদের জন্য বার্ষিক ৮০০ টাকার বৃত্তি",
                "tagline_hi": "कक्षा 5 से 8 में पढ़ने वाले अन्य पिछड़ा वर्ग (OBC) के छात्रों हेतु ₹800 वार्षिक छात्रवृत्ति",
                "description_en": "Medhashree is a 100% state-funded pre-matric scholarship providing Rs. 800 per year directly to OBC students in classes 5 to 8 with family income up to Rs. 2.5 Lakh.",
                "description_bn": "কেন্দ্রীয় বৃত্তি বন্ধের পর রাজ্য সরকারের নিজস্ব তহবিল থেকে পঞ্চম থেকে অষ্টম শ্রেণীর ওবিসি শিক্ষার্থীদের পড়াশোনা এগিয়ে নিতে বার্ষিক ৮০০ টাকা সরাসরি অ্যাকাউন্টে দেওয়া হয়।",
                "description_hi": "OBC वर्ग के छात्रों को कक्षा 5 से 8 तक सालाना ₹800 की छात्रवृत्ति।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹800 / year (Pre-Matric OBC)",
                "benefit_amount_text_bn": "বার্ষিক ৮০০ টাকা",
                "application_channels": ["OASIS Portal (oasis.wb.gov.in)", "Through School"],
                "official_portal_url": "https://oasis.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=medha,
            defaults={
                "min_age": 10,
                "max_age": 16,
                "gender_allowed": "all",
                "caste_categories": ["OBC-A", "OBC-B"],
                "max_family_income": 250000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "OBC student studying in Class 5 to 8 in recognized school; family income ≤ ₹2.5 Lakh/year.",
                "rules_summary_bn": "পশ্চিমবঙ্গের কোনো স্বীকৃত বিদ্যালয়ে ৫ম থেকে ৮ম শ্রেণীতে পাঠরত ওবিসি শিক্ষার্থী, পারিবারিক বার্ষিক আয় ২.৫ লক্ষের কম।"
            }
        )
        set_docs(medha, [
            ("OBC Caste Certificate", "অনলাইন ওবিসি শংসাপত্র", True, "Issued by SDO/competent authority"),
            ("School Study Certificate", "বিদ্যালয়ে পাঠরত থাকার প্রমাণপত্র", True, "From Head of Institution"),
            ("Student Bank Passbook", "ছাত্রছাত্রীর ব্যাংক পাসবুক", True, "Aadhaar linked"),
            ("Family Income Certificate", "পারিবারিক আয়ের শংসাপত্র", True, "Under ₹2.5 Lakh")
        ])

        # -------------------------------------------------------------
        # Scheme 16: Yogyasree (যোগ্যশ্রী) - Free Coaching
        # -------------------------------------------------------------
        yogya, _ = Scheme.objects.update_or_create(
            slug="yogyasree",
            defaults={
                "department": bcwd,
                "category": "education",
                "name_en": "Yogyasree (Free Competitive Exam Coaching)",
                "name_bn": "যোগ্যশ্রী (বিনামূল্যে প্রবেশিকা ও সরকারি চাকরির প্রস্তুতি)",
                "name_hi": "योग्यश्री (मुफ्त कोचिंग योजना - JEE/NEET/WBCS/Police)",
                "tagline_en": "100% free residential coaching & study materials for JEE, NEET, WBCS, Banking, and Police exams",
                "tagline_bn": "এসসি, এসটি ও ওবিসি শিক্ষার্থীদের জন্য মেডিকেল, ইঞ্জিনিয়ারিং ও সরকারি চাকরির ১০০% বিনামূল্যে প্রশিক্ষণ",
                "tagline_hi": "SC/ST/OBC एवं अल्पसंख्यक युवाओं के लिए मेडिकल, इंजीनियरिंग, WBCS एवं पुलिस भर्ती की मुफ्त कोचिंग",
                "description_en": "Yogyasree provides comprehensive, free residential and non-residential coaching along with hostel lodging and books for SC, ST, OBC, and minority youth preparing for JEE, NEET, WBCS, Railways, Banking, and Police Constable/SI exams.",
                "description_bn": "পশ্চিমবঙ্গের সমস্ত জেলায় এসসি, এসটি, ওবিসি ও সংখ্যালঘু শিক্ষার্থীদের ইঞ্জিনিয়ারিং (JEE), মেডিকেল (NEET), ডব্লিউবিসিএস, পুলিশ ও ব্যাংকিং পরীক্ষার জন্য সম্পূর্ণ বিনামূল্যে সেরা শিক্ষকদের মাধ্যমে প্রশিক্ষণ।",
                "description_hi": "प्रवेश परीक्षाओं और सरकारी नौकरियों की तैयारी हेतु आवासीय व गैर-आवासीय मुफ्त कोचिंग सुविधा।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "100% Free Coaching, Hostel Stay & Books",
                "benefit_amount_text_bn": "১০০% বিনামূল্যে প্রশিক্ষণ, হোস্টেল ও বইপত্র",
                "application_channels": ["WBCSTRWDC Portal", "BCW Department Portal", "District Welfare Office"],
                "official_portal_url": "https://www.wbcstrwdc.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=yogya,
            defaults={
                "min_age": 16,
                "max_age": 35,
                "gender_allowed": "all",
                "caste_categories": ["SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Candidates from SC, ST, OBC, or Minority communities appearing in or passed Class 10/12/Graduation.",
                "rules_summary_bn": "পশ্চিমবঙ্গের তফসিলি জাতি, উপজাতি, ওবিসি ও সংখ্যালঘু তরুণ-তরুণী যারা প্রবেশিকা বা সরকারি চাকরির প্রস্তুতি নিচ্ছেন।"
            }
        )
        set_docs(yogya, [
            ("Caste Certificate", "ডিজিটাল জাতিগত শংসাপত্র (SC/ST/OBC)", True, "Issued by SDO"),
            ("Academic Marksheets", "মাধ্যমিক বা উচ্চমাধ্যমিকের মার্কশিট", True, "Proof of qualification"),
            ("Aadhaar Card", "আধার কার্ড", True, "Identity proof")
        ])

        # -------------------------------------------------------------
        # Scheme 17: Sishu Sathi (শিশু সাথী) - Pediatric Surgeries
        # -------------------------------------------------------------
        sishu, _ = Scheme.objects.update_or_create(
            slug="sishu-sathi",
            defaults={
                "department": health,
                "category": "health",
                "name_en": "Sishu Sathi (Free Pediatric Cardiac & Critical Surgery)",
                "name_bn": "শিশু সাথী প্রকল্প (শিশুদের বিনামূল্যে হার্ট ও জটিল অস্ত্রোপচার)",
                "name_hi": "शिशु साथी योजना (बच्चों की मुफ्त हार्ट व गंभीर सर्जरी)",
                "tagline_en": "100% free cardiac and critical surgeries for children aged 0 to 18 with zero income bar",
                "tagline_bn": "১৮ বছর পর্যন্ত শিশুদের জন্মগত হৃদরোগ ও জটিল রোগের ১০০% বিনামূল্যে সম্পূর্ণ চিকিৎসা ও অপারেশন",
                "tagline_hi": "0 से 18 वर्ष के बच्चों के जन्मजात हृदय रोग एवं गंभीर बीमारियों की 100% मुफ्त सर्जरी",
                "description_en": "Sishu Sathi provides completely free-of-cost surgeries and post-operative care for children aged 0 to 18 suffering from congenital heart disease, neurosurgical conditions, and eye ailments, regardless of family income.",
                "description_bn": "পশ্চিমবঙ্গের ১৮ বছর বয়স পর্যন্ত শিশুদের জন্মগত হার্টের ফুটো বা ত্রুটি, নিউরো ও চোখের জটিল অস্ত্রোপচার সম্পূর্ণ বিনামূল্যে রাজ্য ও শীর্ষস্থানীয় বেসরকারি হাসপাতালে সম্পন্ন হয়। কোনো আয়ের শর্ত নেই।",
                "description_hi": "बिना किसी आय सीमा के 18 वर्ष तक के बच्चों की हृदय व अन्य गंभीर सर्जरी सरकारी व एम्पैनल्ड अस्पतालों में मुफ्त।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "100% Free Surgeries, ICU & Medicines (Zero Income Bar)",
                "benefit_amount_text_bn": "১০০% বিনামূল্যে জটিল অস্ত্রোপচার ও ওষুধপত্র",
                "application_channels": ["District CMOH Office", "Govt Medical Colleges (SSKM/BC Roy)", "Swasthya Bhawan"],
                "official_portal_url": "https://wbhealth.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=sishu,
            defaults={
                "min_age": 0,
                "max_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Any child aged 0 to 18 years residing in West Bengal suffering from covered conditions. Absolutely NO income bar.",
                "rules_summary_bn": "পশ্চিমবঙ্গের ০ থেকে ১৮ বছর বয়সী যেকোনো শিশু। কোনো পারিবারিক আয়ের ঊর্ধ্বসীমা নেই।"
            }
        )
        set_docs(sishu, [
            ("Child's Birth Certificate", "শিশুর জন্ম শংসাপত্র", True, "Proof of age"),
            ("Doctor's Diagnosis & Medical Reports", "ডাক্তারি রিপোর্ট ও ইকোকার্ডিওগ্রাফি", True, "Diagnosis of condition"),
            ("Parent's Aadhaar & Ration Card", "অভিভাবকের আধার ও রেশন কার্ড", True, "Residence proof")
        ])

        # -------------------------------------------------------------
        # Scheme 18: Chokher Alo (চোখের আলো) - Free Eye Care
        # -------------------------------------------------------------
        chokher, _ = Scheme.objects.update_or_create(
            slug="chokher-alo",
            defaults={
                "department": health,
                "category": "health",
                "name_en": "Chokher Alo (Universal Eye Care & Cataract Surgery)",
                "name_bn": "চোখের আলো (বিনামূল্যে চোখের চিকিৎসা ও ছানি অপারেশন)",
                "name_hi": "चोखेर आलो (मुफ्त नेत्र जांच, चश्मा एवं मोतियाबिंद ऑपरेशन)",
                "tagline_en": "Free eye screening, free spectacles, and 100% free cataract surgeries with IOL lenses",
                "tagline_bn": "বিনামূল্যে চোখের পরীক্ষা, চশমা বিতরণ এবং আধুনিক ছানি অপারেশন",
                "tagline_hi": "राज्य भर में मुफ्त नेत्र जांच, मुफ्त चश्मा वितरण एवं अत्याधुनिक मोतियाबिंद सर्जरी",
                "description_en": "Chokher Alo offers mass eye testing, distribution of free corrective eyeglasses for school students and senior citizens, and 100% free cataract surgeries with intraocular lens (IOL) implants across all blocks.",
                "description_bn": "অন্ধত্ব দূরীকরণে রাজ্যের প্রতিটি ব্লকে বিনামূল্যে চক্ষু পরীক্ষা, পড়ুয়া ও প্রবীণদের চশমা প্রদান এবং সরকারি হাসপাতালে সম্পূর্ণ বিনামূল্যে ছানি অপারেশন ও লেন্স প্রতিস্থাপন করা হয়।",
                "description_hi": "सभी नागरिकों के लिए मुफ्त नेत्र जांच, विद्यार्थियों व बुजुर्गों को मुफ्त चश्मा एवं मोतियाबिंद का मुफ्त ऑपरेशन।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "Free Eye Checkup, Spectacles & Free Cataract Surgery",
                "benefit_amount_text_bn": "বিনামূল্যে চোখের পরীক্ষা, চশমা ও ছানি অপারেশন",
                "application_channels": ["Block Eye Camps", "Sub-Division / District Hospital Eye OPD", "Duare Sarkar"],
                "official_portal_url": "https://wbhealth.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=chokher,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "All citizens residing in West Bengal, specifically focusing on school students and senior citizens (60+ years).",
                "rules_summary_bn": "পশ্চিমবঙ্গের সমস্ত নাগরিক, বিশেষ করে স্কুল শিক্ষার্থী ও ৬০+ প্রবীণ ব্যক্তিরা।"
            }
        )
        set_docs(chokher, [
            ("Aadhaar Card / Voter ID", "আধার কার্ড বা ভোটার কার্ড", True, "Identification"),
            ("Doctor's Prescription", "প্রেসক্রিপশন", False, "If already examined")
        ])

        # -------------------------------------------------------------
        # Scheme 19: Taposhili Bandhu (তপশিলী বন্ধু) - SC Pension
        # -------------------------------------------------------------
        tb, _ = Scheme.objects.update_or_create(
            slug="taposhili-bandhu",
            defaults={
                "department": bcwd,
                "category": "tribal_caste",
                "name_en": "Taposhili Bandhu (SC Old Age Pension)",
                "name_bn": "তপশিলী বন্ধু (তফসিলি জাতি বার্ধক্য ভাতা)",
                "name_hi": "तपशिली बंधु (SC वृद्धावस्था पेंशन)",
                "tagline_en": "Monthly pension of ₹1,000 for elderly Scheduled Caste (SC) citizens aged 60+",
                "tagline_bn": "পশ্চিমবঙ্গের ৬০ বছর বা তদূর্ধ্ব তফসিলি জাতি (SC) প্রবীণ নাগরিকদের জন্য মাসিক পেনশন",
                "tagline_hi": "60 वर्ष से अधिक आयु के अनुसूचित जाति (SC) के बुजुर्गों हेतु ₹1,000 मासिक पेंशन",
                "description_en": "Taposhili Bandhu provides a lifelong monthly pension of Rs. 1,000 directly to all Scheduled Caste (SC) persons aged 60 years or above who are not covered under other government pensions.",
                "description_bn": "তপশিলী বন্ধু প্রকল্পের অধীনে ৬০ বছর বা তদূর্ধ্ব সমস্ত তফসিলি জাতি (SC) প্রবীণ নাগরিকদের মাসিক ১,০০০ টাকা হারে সরাসরি ব্যাংক অ্যাকাউন্টে পেনশন দেওয়া হয়।",
                "description_hi": "60 वर्ष से अधिक SC नागरिकों को हर महीने ₹1,000 की वृद्धावस्था पेंशन।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000 / month (Lifelong Pension)",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা (আজীবন পেনশন)",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "SDO Office", "Jai Bangla Portal"],
                "official_portal_url": "https://jaibangla.wb.gov.in"
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
                "rules_summary_bn": "তফসিলি জাতি (SC) ভুক্ত হতে হবে, বয়স ৬০ বছর বা তার বেশি এবং অন্য কোনো পেনশন প্রাপক হওয়া যাবে না।"
            }
        )
        set_docs(tb, [
            ("Digitized SC Certificate", "ডিজিটাল তফসিলি জাতি (SC) সার্টিফিকেট", True, "SDO issued certificate"),
            ("Aadhaar Card", "আধার কার্ড", True, "Proof of age and identity"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Aadhaar seeded savings account"),
            ("Voter ID Card", "ভোটার আইডি কার্ড", True, "Proof of residence")
        ])

        # -------------------------------------------------------------
        # Scheme 20: Jai Johar (জয় জোহার) - ST Pension
        # -------------------------------------------------------------
        jj, _ = Scheme.objects.update_or_create(
            slug="jai-johar",
            defaults={
                "department": tribal,
                "category": "tribal_caste",
                "name_en": "Jai Johar (ST Old Age Pension)",
                "name_bn": "জয় জোহার (তফসিলি উপজাতি বার্ধক্য ভাতা)",
                "name_hi": "जय जोहार (ST वृद्धावस्था पेंशन)",
                "tagline_en": "Monthly pension of ₹1,000 for elderly Scheduled Tribe (ST) citizens aged 60+",
                "tagline_bn": "পশ্চিমবঙ্গের ৬০ বছর বা তদূর্ধ্ব তফসিলি উপজাতি (ST) নাগরিকদের জন্য মাসিক পেনশন",
                "tagline_hi": "60 वर्ष से अधिक आयु के अनुसूचित जनजाति (ST) के बुजुर्गों हेतु ₹1,000 मासिक पेंशन",
                "description_en": "Jai Johar provides a monthly pension of Rs. 1,000 directly into the bank accounts of all Scheduled Tribe persons aged 60 years or above.",
                "description_bn": "৬০ বছর বা তার বেশি বয়সী সকল তফসিলি উপজাতি (ST) প্রবীণ নাগরিকদের মাসিক ১,০০০ টাকা করে সরাসরি ব্যাংক অ্যাকাউন্টে পেনশন দেওয়া হয়।",
                "description_hi": "60 वर्ष से अधिक ST नागरिकों को हर महीने ₹1,000 की वृद्धावस्था पेंशन सीधे बैंक खाते में।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000 / month (Lifelong Pension)",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা (আজীবন পেনশন)",
                "application_channels": ["Duare Sarkar Camp", "BDO Office", "SDO Office", "Jai Bangla Portal"],
                "official_portal_url": "https://jaibangla.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=jj,
            defaults={
                "min_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["ST"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Must belong to Scheduled Tribe (ST) category, age 60 years or above, permanent resident of West Bengal. Not receiving another pension.",
                "rules_summary_bn": "তফসিলি উপজাতি (ST) ভুক্ত হতে হবে, বয়স ৬০ বছর বা তার বেশি এবং অন্য কোনো পেনশন প্রাপক হওয়া যাবে না।"
            }
        )
        set_docs(jj, [
            ("Digitized ST Certificate", "ডিজিটাল তফসিলি উপজাতি (ST) সার্টিফিকেট", True, "Issued by SDO"),
            ("Aadhaar Card", "আধার কার্ড", True, "Proof of age and identity"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Aadhaar seeded savings account")
        ])

        # -------------------------------------------------------------
        # Scheme 21: Manabik Pension (মানবিক পেনশন) - Disability
        # -------------------------------------------------------------
        mana, _ = Scheme.objects.update_or_create(
            slug="manabik-pension",
            defaults={
                "department": wcd,
                "category": "social_security",
                "name_en": "Manabik Pension (Disability Assistance)",
                "name_bn": "মানবিক পেনশন (প্রতিবন্ধী ভাতা)",
                "name_hi": "मानविक पेंशन (दिव्यांग सहायता योजना)",
                "tagline_en": "Monthly pension of ₹1,000 for Persons with Disabilities (40% or higher)",
                "tagline_bn": "৪০% বা তার বেশি প্রতিবন্ধী ব্যক্তিদের জন্য মাসিক ১,০০০ টাকার আর্থিক সুরক্ষা",
                "tagline_hi": "40% या अधिक दिव्यांगता वाले नागरिकों हेतु ₹1,000 मासिक जीवन सुरक्षा पेंशन",
                "description_en": "Manabik scheme provides a monthly pension of Rs. 1,000 to persons with disabilities of 40% or higher as certified by a competent government medical authority.",
                "description_bn": "সরকারি মেডিকেল বোর্ড কর্তৃক ৪০% বা তার অধিক প্রতিবন্ধী হিসেবে প্রত্যায়িত ব্যক্তিদের আজীবন মাসিক ১,০০০ টাকা ভাতা প্রদান করা হয়।",
                "description_hi": "सरकारी मेडिकल बोर्ड द्वारा 40% या अधिक दिव्यांग प्रमाणित व्यक्तियों को ₹1,000 मासिक पेंशन।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,000 / month (Lifelong Pension)",
                "benefit_amount_text_bn": "মাসিক ১,০০০ টাকা (আজীবন পেনশন)",
                "application_channels": ["BDO Office", "SDO Office", "Duare Sarkar Camp", "Jai Bangla Portal"],
                "official_portal_url": "https://jaibangla.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=mana,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 100000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Resident of WB with certified disability of 40% or higher; family income not exceeding ₹1,00,000 per year.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, সরকারি মেডিকেল সার্টিফিকেট অনুযায়ী প্রতিবন্ধকতার মাত্রা অন্তত ৪০% এবং পারিবারিক আয় বছরে ১ লক্ষ টাকার কম।"
            }
        )
        set_docs(mana, [
            ("Disability Certificate / UDID Card", "প্রতিবন্ধী শংসাপত্র বা UDID কার্ড", True, "Certified by Govt Medical Board (40%+ disability)"),
            ("Aadhaar Card", "আধার কার্ড", True, "Identity proof"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Aadhaar seeded bank account"),
            ("Income Certificate", "আয়ের শংসাপত্র", True, "Under ₹1 Lakh/year")
        ])

        # -------------------------------------------------------------
        # Scheme 22: Matsyajeebi Bandhu (মৎস্যজীবী বন্ধু)
        # -------------------------------------------------------------
        matsya, _ = Scheme.objects.update_or_create(
            slug="matsyajeebi-bandhu",
            defaults={
                "department": fisheries,
                "category": "agriculture",
                "name_en": "Matsyajeebi Bandhu (Fishermen Welfare Scheme)",
                "name_bn": "মৎস্যজীবী বন্ধু প্রকল্প",
                "name_hi": "मत्स्यजीवी बंधु योजना (मछुआरों के लिए कल्याण योजना)",
                "tagline_en": "Financial aid of ₹5,000 during fishing ban + ₹2 Lakh accidental death cover",
                "tagline_bn": "মাছ ধরা নিষেধাজ্ঞার সময় ৫,০০০ টাকা অনুদান ও ২ লক্ষ টাকার দুর্ঘটনাকালীন ক্ষতিপূরণ",
                "tagline_hi": "मछली पकड़ने पर रोक के समय ₹5,000 की सहायता और ₹2 लाख का दुर्घटना बीमा",
                "description_en": "Matsyajeebi Bandhu provides livelihood assistance of Rs. 5,000 during annual fish breeding ban periods, and a one-time relief of Rs. 2,00,000 to the families of fishermen who die accidentally while fishing.",
                "description_bn": "মাছের প্রজনন মরশুমে সমুদ্রে ও নদীতে মাছ ধরার নিষেধাজ্ঞার সময় নিবন্ধিত মৎস্যজীবীদের ৫,০০০ টাকা আর্থিক অনুদান এবং মাছ ধরতে গিয়ে দুর্ঘটনায় মৃত্যুতে ২ লক্ষ টাকার সহায়তা প্রদান করা হয়।",
                "description_hi": "मछुआरों को मछली पकड़ने के प्रतिबंध काल में ₹5,000 की सहायता तथा दुर्घटना में मृत्यु पर ₹2 लाख की आर्थिक सहायता।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "₹5,000 Fishing Ban Relief + ₹2 Lakh Accidental Death Relief",
                "benefit_amount_text_bn": "৫,০০০ টাকা নিষেদ্ধকালীন অনুদান + ২ লক্ষ টাকা মৃত্যু সুবিধা",
                "application_channels": ["Block Fishery Extension Officer (BFEO)", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbfisheries.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=matsya,
            defaults={
                "min_age": 18,
                "max_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Active traditional fisherman holding a Biometric Fisherman Identity Card issued by the Fisheries Department.",
                "rules_summary_bn": "মৎস্য দপ্তর কর্তৃক প্রদত্ত বায়োমেট্রিক মৎস্যজীবী পরিচয়পত্রধারী সক্রিয় ঐতিহ্যবাহী মৎস্যজীবী।"
            }
        )
        set_docs(matsya, [
            ("Biometric Fisherman ID Card", "বায়োমেট্রিক মৎস্যজীবী পরিচয়পত্র", True, "Issued by Fisheries Dept"),
            ("Aadhaar Card", "আধার কার্ড", True, "Identity proof"),
            ("Bank Passbook", "ব্যাংক পাসবুক", True, "Aadhaar seeded bank account")
        ])

        # -------------------------------------------------------------
        # Scheme 23: Khadya Sathi & Duare Ration (খাদ্য সাথী ও দুয়ারে রেশন)
        # -------------------------------------------------------------
        khadya, _ = Scheme.objects.update_or_create(
            slug="khadya-sathi",
            defaults={
                "department": food,
                "category": "social_security",
                "name_en": "Khadya Sathi & Duare Ration",
                "name_bn": "খাদ্য সাথী ও দুয়ারে রেশন",
                "name_hi": "खाद्य साथी एवं दुआरे राशन (मुफ्त राशन वितरण)",
                "tagline_en": "100% free monthly food grains (rice & wheat) delivered at doorsteps / fair price shops",
                "tagline_bn": "ডিজিটাল রেশন কার্ডধারীদের জন্য বিনামূল্যে মাসিক খাদ্যশস্য (চাল ও গম/আটা) সরবরাহ",
                "tagline_hi": "राज्य के सभी डिजिटल राशन कार्ड धारकों को हर महीने मुफ्त चावल व गेहूं का वितरण",
                "description_en": "Khadya Sathi provides 100% free monthly food grains to over 9 crore citizens in West Bengal through doorstep ration delivery vans (Duare Ration) and fair price dealers.",
                "description_bn": "পশ্চিমবঙ্গের ৯ কোটিরও বেশি মানুষের কাছে বিনামূল্যে প্রতি মাসে নির্ধারিত চাল ও আটা সরবরাহ করা হয়। দুয়ারে রেশন প্রকল্পের মাধ্যমে পাড়ায় পাড়ায় গাড়ি পৌঁছে রেশন দেওয়া হয়।",
                "description_hi": "डिजिटल राशन कार्ड धारक परिवारों को हर महीने निश्चित मात्रा में मुफ्त चावल व गेहूं घर के पास उपलब्ध कराया जाता है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "100% Free Monthly Food Grains (Rice & Wheat)",
                "benefit_amount_text_bn": "সম্পূর্ণ বিনামূল্যে মাসিক চাল ও গম/আটা",
                "application_channels": ["Fair Price Ration Shops", "Food & Supplies Portal", "Duare Sarkar Camp"],
                "official_portal_url": "https://food.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=khadya,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "All citizens holding an active Digital Ration Card (AAY, SPHH, PHH, RKSY-I, RKSY-II).",
                "rules_summary_bn": "পশ্চিমবঙ্গের যেসকল নাগরিকের বৈধ ডিজিটাল রেশন কার্ড রয়েছে।"
            }
        )
        set_docs(khadya, [
            ("Digital Ration Card", "ডিজিটাল রেশন কার্ড", True, "For biometric e-POS distribution"),
            ("Aadhaar Card", "আধার কার্ড", True, "Linked with Ration Card")
        ])

        # -------------------------------------------------------------
        # Official Directories & Grievance Offices
        # -------------------------------------------------------------
        OfficialDirectory.objects.update_or_create(
            office_type="cmo_cell",
            district="Statewide",
            defaults={
                "designation": "Chief Minister's Grievance Cell (Didi ke Bolo)",
                "office_address": "Nabanna, 325 Sarat Chatterjee Road, Howrah 711102",
                "contact_phone": "9137091370",
                "grievance_portal_url": "https://wb.gov.in"
            }
        )

        OfficialDirectory.objects.update_or_create(
            office_type="prd_portal",
            district="Statewide",
            defaults={
                "designation": "Panchayats & Rural Development Grievance Redressal",
                "office_address": "Joint Administrative Building, HC-7, Sector-III, Salt Lake, Kolkata 700106",
                "contact_phone": "1800-345-3200",
                "grievance_portal_url": "https://prd.wb.gov.in"
            }
        )

        OfficialDirectory.objects.update_or_create(
            office_type="duare_sarkar",
            district="Statewide",
            defaults={
                "designation": "Duare Sarkar State Monitoring Desk",
                "office_address": "State Secretariat Nabanna, Mandirtala, Shibpur, Howrah",
                "contact_phone": "033-2214-0152",
                "grievance_portal_url": "https://ds.wb.gov.in"
            }
        )

        OfficialDirectory.objects.update_or_create(
            office_type="nha_desk",
            district="Statewide",
            defaults={
                "designation": "Ayushman Bharat PM-JAY State Operations Desk",
                "office_address": "Swasthya Bhawan, GN-29, Sector-V, Salt Lake, Kolkata 700091",
                "contact_phone": "14555",
                "grievance_portal_url": "https://beneficiary.nha.gov.in"
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded comprehensive 2026 West Bengal schemes!"))
