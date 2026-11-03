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
        mca, _ = Department.objects.get_or_create(
            code="mca",
            defaults={
                "name_en": "Ministry of Corporate Affairs (Central Government)",
                "name_bn": "কর্পোরেট বিষয়ক মন্ত্রক",
                "name_hi": "कॉर्पोरेट कार्य मंत्रालय",
                "portal_url": "https://pminternship.mca.gov.in",
                "helpline": "1800-111-555"
            }
        )

        pbssd, _ = Department.objects.get_or_create(
            code="pbssd",
            defaults={
                "name_en": "Technical Education, Training & Skill Development (PBSSD)",
                "name_bn": "কারিগরি শিক্ষা, প্রশিক্ষণ ও দক্ষতা উন্নয়ন দপ্তর (PBSSD)",
                "name_hi": "तकनीकी शिक्षा, प्रशिक्षण एवं कौशल विकास विभाग (PBSSD)",
                "portal_url": "https://pbssd.gov.in",
                "helpline": "1800-102-8014"
            }
        )

        udma, _ = Department.objects.get_or_create(
            code="udma",
            defaults={
                "name_en": "Urban Development & Municipal Affairs Department",
                "name_bn": "নগর উন্নয়ন ও পুর বিষয়ক দপ্তর",
                "name_hi": "नगर विकास और नगरपालिका मामले विभाग",
                "portal_url": "https://wbudma.gov.in",
                "helpline": "033-2334-9394"
            }
        )

        labour, _ = Department.objects.get_or_create(
            code="labour",
            defaults={
                "name_en": "Labour Department",
                "name_bn": "শ্রম দপ্তর",
                "name_hi": "श्रम विभाग",
                "portal_url": "https://karmasathi.wb.gov.in",
                "helpline": "1800-103-0009"
            }
        )

        uidai, _ = Department.objects.get_or_create(
            code="uidai",
            defaults={
                "name_en": "Unique Identification Authority of India (UIDAI)",
                "name_bn": "ইউআইডিএআই (ভারতীয় স্বতন্ত্র পরিচয় কর্তৃপক্ষ)",
                "name_hi": "भारतीय विशिष्ट पहचान प्राधिकरण (UIDAI)",
                "portal_url": "https://uidai.gov.in",
                "helpline": "1947"
            }
        )

        land, _ = Department.objects.get_or_create(
            code="land",
            defaults={
                "name_en": "Land & Land Reforms and Refugee Relief & Rehabilitation Department",
                "name_bn": "ভূমি ও ভূমি সংস্কার এবং উদ্বাস্তু ত্রাণ ও পুনর্বাসন দপ্তর",
                "name_hi": "भूमि एवं भूमि सुधार तथा शरणार्थी राहत और पुनर्वास विभाग",
                "portal_url": "https://banglarbhumi.gov.in",
                "helpline": "1800-345-5555"
            }
        )

        moa, _ = Department.objects.get_or_create(
            code="moa",
            defaults={
                "name_en": "Ministry of Agriculture & Farmers Welfare",
                "name_bn": "কৃষি ও কৃষক কল্যাণ মন্ত্রক",
                "name_hi": "कृषि एवं किसान कल्याण मंत्रालय",
                "portal_url": "https://agriinfra.dac.gov.in",
                "helpline": "1800-180-1551"
            }
        )

        dfs, _ = Department.objects.get_or_create(
            code="dfs",
            defaults={
                "name_en": "Department of Financial Services / PFRDA",
                "name_bn": "আর্থিক পরিষেবা বিভাগ (PFRDA)",
                "name_hi": "वित्तीय सेवाएं विभाग / पीएफआरडीए",
                "portal_url": "https://npai.pfrda.org.in",
                "helpline": "1800-110-069"
            }
        )

        mha, _ = Department.objects.get_or_create(
            code="mha",
            defaults={
                "name_en": "Ministry of Home Affairs (Citizenship Division)",
                "name_bn": "স্বরাষ্ট্র মন্ত্রক (নাগরিকত্ব শাখা)",
                "name_hi": "गृह मंत्रालय (नागरिकता प्रभाग)",
                "portal_url": "https://indiancitizenshiponline.nic.in",
                "helpline": "011-2309-2011"
            }
        )

        mord, _ = Department.objects.get_or_create(
            code="mord",
            defaults={
                "name_en": "Ministry of Rural Development & Anandadhara (WBSRLM)",
                "name_bn": "গ্রামীণ উন্নয়ন মন্ত্রক ও আনন্দধারা (WBSRLM)",
                "name_hi": "ग्रामीण विकास मंत्रालय एवं आनंदधारा (WBSRLM)",
                "portal_url": "https://nrlm.gov.in",
                "helpline": "1800-345-3200"
            }
        )

        mole, _ = Department.objects.get_or_create(
            code="mole",
            defaults={
                "name_en": "Ministry of Labour & Employment",
                "name_bn": "শ্রম ও কর্মসংস্থান মন্ত্রক",
                "name_hi": "श्रम एवं रोजगार मंत्रालय",
                "portal_url": "https://eshram.gov.in",
                "helpline": "14434"
            }
        )

        msde, _ = Department.objects.get_or_create(
            code="msde",
            defaults={
                "name_en": "Ministry of Skill Development and Entrepreneurship",
                "name_bn": "দক্ষতা উন্নয়ন ও উদ্যোক্তা মন্ত্রক",
                "name_hi": "कौशल विकास और उद्यमिता मंत्रालय",
                "portal_url": "https://www.apprenticeshipindia.gov.in",
                "helpline": "011-2345-6789"
            }
        )

        moe, _ = Department.objects.get_or_create(
            code="moe",
            defaults={
                "name_en": "Ministry of Education (NATS / BOAT)",
                "name_bn": "শিক্ষা মন্ত্রক (NATS / BOAT)",
                "name_hi": "शिक्षा मंत्रालय (NATS / BOAT)",
                "portal_url": "https://nats.education.gov.in",
                "helpline": "1800-425-2239"
            }
        )

        mnre, _ = Department.objects.get_or_create(
            code="mnre",
            defaults={
                "name_en": "Ministry of New and Renewable Energy (MNRE) / WBSEDCL",
                "name_bn": "নতুন ও পুনর্নবীকরণযোগ্য শক্তি মন্ত্রক (MNRE) / বিদ্যুৎ বণ্টন",
                "name_hi": "नवीन और नवीकरणीय ऊर्जा मंत्रालय (MNRE) / विद्युत वितरण",
                "portal_url": "https://pmsuryaghar.gov.in",
                "helpline": "15555"
            }
        )

        mopng, _ = Department.objects.get_or_create(
            code="mopng",
            defaults={
                "name_en": "Ministry of Petroleum and Natural Gas (MoPNG)",
                "name_bn": "পেট্রোলিয়াম ও প্রাকৃতিক গ্যাস মন্ত্রক",
                "name_hi": "पेट्रोलियम एवं प्राकृतिक गैस मंत्रालय",
                "portal_url": "https://www.pmuy.gov.in",
                "helpline": "1800-266-6696"
            }
        )

        self.stdout.write("Seeding Active 2026 West Bengal Welfare Schemes...")

        # Helper function for adding scheme documents
        def set_docs(scheme_obj, docs_list):
            current_names = [d[0] for d in docs_list]
            SchemeDocument.objects.filter(scheme=scheme_obj).exclude(name_en__in=current_names).delete()
            for name_en, name_bn, is_mand, clar in docs_list:
                doc = SchemeDocument.objects.filter(scheme=scheme_obj, name_en=name_en).first()
                if doc:
                    doc.name_bn = name_bn
                    doc.is_mandatory = is_mand
                    doc.clarification_en = clar
                    doc.save()
                else:
                    SchemeDocument.objects.create(
                        scheme=scheme_obj, name_en=name_en, name_bn=name_bn,
                        is_mandatory=is_mand, clarification_en=clar
                    )

        # -------------------------------------------------------------
        # Scheme 1: Ayushman Bharat (AB-PMJAY)
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
                "rules_summary_en": "Automatically determined through socio-economic deprivation and occupational criteria based on SECC 2011 and NFSA registries. Rural families lacking permanent shelter, living in single-room kucha houses, landless manual labour households, and SC/ST households; urban informal workers (ragpickers, domestic helpers, street vendors, transport drivers, construction labourers); and all senior citizens aged 70 and above, regardless of income.",
                "rules_summary_bn": "জাতীয় খাদ্য সুরক্ষা (NFSA) রেশন কার্ড ও আর্থ-সামাজিক তালিকাভুক্ত পরিবার। ৭০ বা তার বেশি বয়সী প্রবীণদের জন্য সম্পূর্ণ সার্বজনীন।"
            }
        )
        set_docs(ab, [
            ("Aadhaar Card (Mandatory for e-KYC)", "আধার কার্ড (ই-কেওয়াইসি বাধ্যতামূলক)", True, "Aadhaar card (mandatory for e-KYC and biometric authentication)"),
            ("Digital Ration Card / NFSA Ration Card", "ডিজিটাল রেশন কার্ড / এনএফএসএ কার্ড", True, "Digital Ration Card / NFSA Ration Card matching family entitlement records"),
            ("Proof of Identity (Voter ID, Driving Licence)", "পরিচয়পত্র (ভোটার কার্ড বা ড্রাইভিং লাইসেন্স)", True, "Proof of identity (Voter ID, driving licence, or other officially valid document)"),
            ("Active Mobile Number", "সক্রিয় মোবাইল নম্বর", True, "Active mobile number linked with Aadhaar for OTP verification")
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
                "official_portal_url": "https://wbmsmet.gov.in/schemes_of_msmet"
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
                "official_portal_url": "https://www.govtschemes.in/west-bengal-yogyashree-scheme"
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
                "rules_summary_en": "Permanent resident of West Bengal belonging to Scheduled Tribe (ST) community, aged 60 years or above. Must not receive any other monthly social welfare pension or regular government salary/pension.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, তফসিলি উপজাতি (ST) ভুক্ত, বয়স ৬০ বছর বা তার বেশি এবং অন্য কোনো সামাজিক নিরাপত্তা পেনশন বা নিয়মিত সরকারি বেতন প্রাপক হওয়া যাবে না।"
            }
        )
        set_docs(jj, [
            ("Formal ST Caste/Tribe Certificate", "ডিজিটাল তফসিলি উপজাতি (ST) সার্টিফিকেট", True, "Formal ST Caste/Tribe certificate issued by a competent authority (or paternal relative certificate with undertaking)"),
            ("Proof of Age & Address: Aadhaar Card", "আধার কার্ড (বয়স ও ঠিকানার প্রমাণ)", True, "Aadhaar card of applicant proving age and identity"),
            ("Proof of Residence: Voter ID (EPIC)", "ভোটার আইডি কার্ড (ঠিকানার প্রমাণ)", True, "Voter identity card (EPIC) proving West Bengal domicile"),
            ("Digital Ration Card", "ডিজিটাল রেশন কার্ড", True, "Digital ration card of the applicant"),
            ("Aadhaar-Linked CBS Bank Passbook Copy", "আধার সংযুক্ত সিবিএস ব্যাংক পাসবুক", True, "Aadhaar-linked CBS bank passbook copy showing account number & IFSC"),
            ("Recent Passport-Size Photographs", "সাম্প্রতিক পাসপোর্ট সাইজ রঙিন ছবি", True, "Recent colour passport-size photographs")
        ])

        # -------------------------------------------------------------
        # Scheme 21: Manabik Pension (মানবিক পেনশন) - Disability
        # -------------------------------------------------------------
        pmis, _ = Scheme.objects.update_or_create(
            slug="prime-minister-internship-scheme",
            defaults={
                "department": mca,
                "category": "youth",
                "name_en": "Prime Minister Internship Scheme (PMIS)",
                "name_bn": "প্রধানমন্ত্রী ইন্টার্নশিপ প্রকল্প (PMIS)",
                "name_hi": "प्रधानमंत्री इंटर्नशिप योजना (PMIS)",
                "tagline_en": "12-month paid internship with top Indian companies with ₹5,000/month stipend and ₹6,000 one-time grant",
                "tagline_bn": "শীর্ষস্থানীয় ভারতীয় কোম্পানিতে ১২ মাসের পেইড ইন্টার্নশিপ ও মাসিক ₹৫,০০০ অনুদান",
                "tagline_hi": "शीर्ष भारतीय कंपनियों में 12 महीने की सशुल्क इंटर्नशिप व ₹5,000/माह वजीफा",
                "description_en": "Prime Minister Internship Scheme (PMIS) provides a 12-month real-world corporate internship experience in top 500 companies in India for youth aged 21-24 years. Interns receive ₹5,000/month stipend plus ₹6,000 one-time grant for incidental expenses.",
                "description_bn": "২১ থেকে ২৪ বছর বয়সী ভারতীয় তরুণ-তরুণীদের জন্য ভারতের শীর্ষ ৫০০ সংস্থায় ১২ মাসের ইন্টার্নশিপ। মাসিক ₹৫,০০০ অনুদান এবং এককালীন ₹৬,০০০ টাকার আর্থিক সাহায্য।",
                "description_hi": "21 से 24 वर्ष के युवाओं को भारत की शीर्ष 500 कंपनियों में 12 महीने की इंटर्नशिप, ₹5,000 मासिक सहायता और ₹6,000 एकमुश्त सहायता दी जाती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹5,000 / month Stipend + ₹6,000 One-time Grant",
                "benefit_amount_text_bn": "মাসিক ₹৫,০০০ স্টাইপেন্ড + এককালীন ₹৬,০০০ অনুদান",
                "application_channels": ["Online Portal (pminternship.mca.gov.in)"],
                "official_portal_url": "https://pminternship.mca.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmis,
            defaults={
                "min_age": 21,
                "max_age": 24,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 800000,
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian citizen aged 21-24. Passed Class 10/12, ITI, Polytechnic Diploma, or Undergraduate degrees. Family annual income ≤ ₹8,00,000. Not in full-time employment or full-time higher education.",
                "rules_summary_bn": "২১-২৪ বছর বয়সী ভারতীয় নাগরিক। মাধ্যমিক, উচ্চমাধ্যমিক, আইটিআই, ডিপ্লোমা বা স্নাতক পাস। বার্ষিক আয় ৮ লাখ টাকার মধ্যে।"
            }
        )
        set_docs(pmis, [
            ("Aadhaar Card", "আধার কার্ড", True, "Mandatory for e-KYC"),
            ("Educational Certificates and Marksheets", "শিক্ষাগত যোগ্যতার সার্টিফিকেট ও মার্কশিট", True, "10th/12th/ITI/Diploma/Degree pass documents"),
            ("Proof of Age", "বয়সের প্রমাণপত্র", True, "Birth Certificate / School Leaving / Admit Card"),
            ("Aadhaar-Seeded Bank Account Passbook", "আধার-সিডেড ব্যাঙ্ক পাসবই", True, "Active Aadhaar-NPCI DBT seeded account"),
            ("Recent Passport-Size Photograph", "পাসপোর্ট সাইজ ছবি", True, "Recent colour passport photograph")
        ])

        # -------------------------------------------------------------
        # Scheme 27: Rajya Khadya Suraksha Yojana (RKSY / Food Security Scheme)
        # -------------------------------------------------------------
        rksy, _ = Scheme.objects.update_or_create(
            slug="rajya-khadya-suraksha-yojana",
            defaults={
                "department": food,
                "category": "health",
                "name_en": "Rajya Khadya Suraksha Yojana (RKSY / Food Security Scheme)",
                "name_bn": "রাজ্য খাদ্য সুরক্ষা যোজনা (RKSY / খাদ্য সাথী)",
                "name_hi": "राज्य खाद्य सुरक्षा योजना (RKSY / खाद्य सुरक्षा)",
                "tagline_en": "Subsidized and free food grains (Rice & Wheat) for all eligible beneficiary families under RKSY-I and RKSY-II",
                "tagline_bn": "পশ্চিমবঙ্গের সমস্ত যোগ্য পরিবারের জন্য বিনামূল্যে ও ভর্তুকিযুক্ত খাদ্যশস্য (চাল ও গম) সরবরাহ",
                "tagline_hi": "सभी पात्र परिवारों के लिए रियायती और मुफ्त खाद्यान्न (चावल व गेहूं)",
                "description_en": "Rajya Khadya Suraksha Yojana (RKSY) ensures food security across West Bengal. Eligible families receive digital ration cards categorized under RKSY-I and RKSY-II to receive monthly food grains directly from fair price ration shops and Duare Ration delivery.",
                "description_bn": "খাদ্য ও সরবরাহ দপ্তর পরিচালিত রাজ্য খাদ্য সুরক্ষা যোজনার মাধ্যমে পশ্চিমবঙ্গের অর্থনৈতিকভাবে পিছিয়ে থাকা পরিবারগুলিকে প্রতি মাসে বিনামূল্যে চাল ও গম প্রদান করা হয়।",
                "description_hi": "राज्य खाद्य सुरक्षा योजना के तहत गरीब परिवारों को डिजिटल राशन कार्ड के माध्यम से हर महीने मुफ्त व रियायती चावल-गेहूं प्रदान किया जाता है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "Free / Subsidized Monthly Food Grains (5kg/head/month)",
                "benefit_amount_text_bn": "বিনামূল্যে মাসিক মাথাপিছু ৫ কেজি খাদ্যশস্য (চাল ও গম)",
                "application_channels": ["Duare Sarkar Camp", "Food & Supplies Inspector Office", "Online Portal (food.wb.gov.in)"],
                "official_portal_url": "https://food.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=rksy,
            defaults={
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 150000,
                "rules_summary_en": "Permanent resident of West Bengal belonging to BPL, Antyodaya Anna Yojana (AAY), or Priority Household (PHH) categories. Must not have duplicating central quotas.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা। বিপিএল, অন্ত্যোদয় বা অগ্রাধিকারপ্রাপ্ত (PHH) পরিবারভুক্ত।"
            }
        )
        set_docs(rksy, [
            ("Aadhaar Cards of All Family Members", "পরিবারের সকল সদস্যের আধার কার্ড", True, "Mandatory for biometric seeding"),
            ("Existing Ration Card / Family Card", "বর্তমান রেশন কার্ড / ফ্যামিলি কার্ড", False, "Required if updating or migrating category"),
            ("Proof of Residence", "বাসস্থানের প্রমাণপত্র", True, "Voter ID (EPIC) / Electricity Bill"),
            ("Income Certificate / BPL Certificate", "বার্ষিক আয় / বিপিএল সার্টিফিকেট", True, "Issued by competent local authority"),
            ("Active Mobile Number and Passport Photo of Head of Family", "মোবাইল নম্বর ও পরিবারের প্রধানের ছবি", True, "Linked with digital ration card profile")
        ])

        # -------------------------------------------------------------
        # Scheme 28: Rojgar Seva Portal (PBSSD / Employment Services)
        # -------------------------------------------------------------
        rojgar, _ = Scheme.objects.update_or_create(
            slug="rojgar-seva-portal",
            defaults={
                "department": pbssd,
                "category": "youth",
                "name_en": "Rojgar Seva Portal (PBSSD / Employment Services)",
                "name_bn": "রোজগার সেবা পোর্টাল (PBSSD / এমপ্লয়মেন্ট ব্যাঙ্ক)",
                "name_hi": "रोजगार सेवा पोर्टल (PBSSD / रोजगार सेवाएं)",
                "tagline_en": "Statewide job search, vocational placement, and apprentice matching for West Bengal job seekers",
                "tagline_bn": "পশ্চিমবঙ্গের চাকরিপ্রার্থীদের জন্য রাজ্যভিত্তিক কর্মসংস্থান ও শিক্ষানবিশী সহায়তা পোর্টাল",
                "tagline_hi": "पश्चिम बंगाल के नौकरी चाहने वालों के लिए राज्यव्यापी नौकरी व शिक्षुता पोर्टल",
                "description_en": "Rojgar Seva Portal connects resident job seekers of West Bengal with registered employers, micro-enterprises, and skill-based apprenticeship opportunities matching their education and trade skills.",
                "description_bn": "পশ্চিমবঙ্গের চাকরিপ্রার্থীদের সরকারি ও বেসরকারি ক্ষেত্রে কাজের সুযোগ, শিক্ষানবিশী প্রশিক্ষণ ও কর্মসংস্থানের সুযোগ করে দেওয়ার কেন্দ্রীয় পোর্টাল।",
                "description_hi": "पश्चिम बंगाल के युवाओं को रोजगार के अवसर, निजी व सरकारी नौकरियों और अप्रेंटिसशिप से जोड़ने वाला राज्य पोर्टल।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Free Job Matching & Skill Apprenticeship",
                "benefit_amount_text_bn": "বিনামূল্যে চাকরি ও বৃত্তিমূলক প্রশিক্ষণ সংযোগ",
                "application_channels": ["Online Portal (employmentbankwb.gov.in)", "District Employment Exchange"],
                "official_portal_url": "https://employmentbankwb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=rojgar,
            defaults={
                "min_age": 18,
                "max_age": 45,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Resident job seekers of West Bengal looking for employment, apprenticeships, or vocational placement. Minimum age 18 years.",
                "rules_summary_bn": "পশ্চিমবঙ্গের বাসিন্দা কর্মপ্রার্থী। সর্বনিম্ন বয়স ১৮ বছর।"
            }
        )
        set_docs(rojgar, [
            ("Aadhaar Card / Voter ID (EPIC)", "আধার কার্ড / ভোটার কার্ড", True, "Mandatory proof of identity and West Bengal residence"),
            ("Academic Certificates and Trade Pass Diplomas", "শিক্ষাগত শংসাপত্র ও মার্কশিট", True, "Class 8th/10th/12th/ITI/Diploma/Degree pass documents"),
            ("Resume / Curriculum Vitae (CV)", "বায়োডাটা / জীবনবৃত্তান্ত (CV)", True, "Updated resume showing skills and experience"),
            ("Caste & Disability Certificate (if applicable)", "জাতিগত ও প্রতিবন্ধী শংসাপত্র", False, "Applicable for reserved vacancies and concessions"),
            ("Active Mobile Number and Valid Email Address", "সক্রিয় মোবাইল নম্বর ও ইমেল", True, "For employer call letters and interview notices")
        ])

        # -------------------------------------------------------------
        # Scheme 29: Soil Health Card Scheme
        # -------------------------------------------------------------
        soil, _ = Scheme.objects.update_or_create(
            slug="soil-health-card-scheme",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Soil Health Card Scheme",
                "name_bn": "মৃত্তিকা স্বাস্থ্য কার্ড প্রকল্প (Soil Health Card)",
                "name_hi": "मृदा स्वास्थ्य कार्ड योजना (Soil Health Card)",
                "tagline_en": "Free laboratory soil testing and customized crop nutrient recommendations for farmers",
                "tagline_bn": "চাষীদের জন্য বিনামূল্যে মাটির গুণমান পরীক্ষা ও সুনির্দিষ্ট সার ব্যবহারের পরামর্শ",
                "tagline_hi": "किसानों के लिए मुफ्त मिट्टी परीक्षण व पोषक तत्व परामर्श कार्ड",
                "description_en": "Soil Health Card Scheme issues comprehensive soil nutrient status cards to farmers every 3 years. It reports 12 key soil health parameters and provides tailored chemical and organic fertilizer dosages.",
                "description_bn": "কৃষি দপ্তরের এই প্রকল্পে কৃষকদের জমির মাটি বিনামূল্যে পরীক্ষাগারে পরীক্ষা করে ১২টি উপাদানের মাত্রা ও সারের সঠিক পরিমাণযুক্ত স্বাস্থ্য কার্ড প্রদান করা হয়।",
                "description_hi": "इस योजना के तहत किसानों की कृषि भूमि की मिट्टी की मुफ्त जांच करके 12 पोषक तत्वों की स्थिति का कार्ड दिया जाता है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Free Soil Testing & Scientific Advisory every 3 Years",
                "benefit_amount_text_bn": "বিনামূল্যে মাটির স্বাস্থ্য পরীক্ষা ও সার প্রয়োগ নির্দেশিকা",
                "application_channels": ["Block ADA Office", "Krishi Vigyan Kendra (KVK)", "Duare Sarkar Camp"],
                "official_portal_url": "https://soilhealth.dac.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=soil,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "All Indian farmers cultivating or holding agricultural land in West Bengal. Open to owner farmers, tenant farmers, and sharecroppers.",
                "rules_summary_bn": "পশ্চিমবঙ্গের সমস্ত জমির মালিক কৃষক, ক্ষুদ্র-প্রান্তিক চাষী ও বর্গাদার।"
            }
        )
        set_docs(soil, [
            ("Aadhaar Card", "আধার কার্ড", True, "Proof of identity of the farmer"),
            ("Land Record Documents (RoR / Khatian / Porcha)", "জমির পরচা বা খতিয়ান", True, "Mandatory proof of agricultural land holding"),
            ("Tenancy or Lease Agreement (for Sharecroppers)", "বর্গাদার বা ইজারা চুক্তিপত্র", False, "Required for tenant farmers and bargadars"),
            ("Bank Account Passbook Copy", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "Bank details of the farmer"),
            ("Contact Mobile Number", "যোগাযোগের মোবাইল নম্বর", True, "For SMS notifications of soil test results")
        ])

        # -------------------------------------------------------------
        # Scheme 30: Sukanya Samriddhi Yojana (SSY)
        # -------------------------------------------------------------
        ssy, _ = Scheme.objects.update_or_create(
            slug="sukanya-samriddhi-yojana",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Sukanya Samriddhi Yojana (SSY)",
                "name_bn": "সুকন্যা সমৃদ্ধি যোজনা (SSY)",
                "name_hi": "सुकन्या समृद्धि योजना (SSY)",
                "tagline_en": "High-interest, tax-free small savings scheme dedicated to the education and marriage of the girl child",
                "tagline_bn": "কন্যা সন্তানের উচ্চশিক্ষা ও ভবিষ্যতের জন্য সর্বোচ্চ সুদের করমুক্ত সরকারি সঞ্চয় প্রকল্প",
                "tagline_hi": "बालिका की शिक्षा व भविष्य हेतु उच्च ब्याज दर वाली कर-मुक्त बचत योजना",
                "description_en": "Sukanya Samriddhi Yojana (SSY) is a government-backed savings scheme for girl children offering attractive sovereign interest rates (8.2%+) with Triple Tax Exemption (EEE) under Section 80C.",
                "description_bn": "কন্যা সন্তানের ভবিষ্যতের জন্য একটি অত্যন্ত লাভজনক সরকারি সঞ্চয় যোজনা। সর্বনিম্ন ২৫০ টাকা দিয়ে পোস্ট অফিস বা ব্যাংকে অ্যাকাউন্ট খোলা যায়।",
                "description_hi": "बेटियों के भविष्य को सुरक्षित करने के लिए उच्च ब्याज वाली योजना। 10 वर्ष से कम आयु की बालिकाओं के लिए न्यूनतम ₹250 में खाता खोला जा सकता है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "High Sovereign Interest (8.2% p.a.) + 100% Tax-Free Maturity",
                "benefit_amount_text_bn": "বার্ষিক ৮.২% সরকারি সুদ + সম্পূর্ণ করমুক্ত সঞ্চিত তহবিল",
                "application_channels": ["Post Office Branches", "Authorized Commercial Banks"],
                "official_portal_url": "https://www.indiapost.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ssy,
            defaults={
                "min_age": 0,
                "max_age": 10,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Account opened in the name of girl child under 10 years by parents/guardians. Max 2 accounts per family (triplet/twin exceptions permitted). Minimum deposit ₹250/year.",
                "rules_summary_bn": "কন্যা সন্তানের বয়স ১০ বছরের কম হতে হবে। পরিবারে সর্বাধিক ২ জন কন্যা সন্তানের জন্য অ্যাকাউন্ট খোলা সম্ভব।"
            }
        )
        set_docs(ssy, [
            ("Birth Certificate of the Girl Child", "কন্যা সন্তানের জন্ম শংসাপত্র", True, "Mandatory original birth certificate"),
            ("Identity Proof of Parent / Guardian", "অভিভাবকের পরিচয়পত্র (আধার/প্যান)", True, "Aadhaar Card or PAN Card of the parent/guardian"),
            ("Address Proof of Parent / Guardian", "অভিভাবকের ঠিকানার প্রমাণপত্র", True, "Voter ID / Utility Electricity Bill / Passport"),
            ("Passport-Size Photographs of Child and Guardian", "সন্তান ও অভিভাবকের পাসপোর্ট ছবি", True, "Recent colour passport-size photos"),
            ("Medical Certificate (for Twins/Triplets)", "যমজ সন্তানের মেডিকেল সার্টিফিকেট", False, "Required if opening accounts for twin/triplet daughters")
        ])

        # -------------------------------------------------------------
        # Scheme 31: Swachh Bharat Mission (SBM - Urban / General)
        # -------------------------------------------------------------
        sbm_urban, _ = Scheme.objects.update_or_create(
            slug="swachh-bharat-mission-urban",
            defaults={
                "department": udma,
                "category": "health",
                "name_en": "Swachh Bharat Mission (SBM - Urban / General)",
                "name_bn": "স্বচ্ছ ভারত মিশন (শহরাঞ্চল / সাধারণ)",
                "name_hi": "स्वच्छ भारत मिशन (शहरी / सामान्य)",
                "tagline_en": "Urban sanitation, municipal waste management, and community sanitation infrastructure development",
                "tagline_bn": "পৌর এলাকার নিকাশি, কঠিন বর্জ্য ব্যবস্থাপনা ও সার্বিক স্বাস্থ্যবিধির উন্নয়ন",
                "tagline_hi": "शहरी स्वच्छता, ठोस अपशिष्ट प्रबंधन व सामुदायिक शौचालय अवसंरचना",
                "description_en": "Swachh Bharat Mission (Urban) focuses on achieving 100% open defecation-free (ODF) status and municipal solid waste management across all statutory towns in West Bengal through community sanitation units and waste processing.",
                "description_bn": "পশ্চিমবঙ্গের সমস্ত পৌর এলাকায় স্বাস্থ্যসম্মত শৌচাগার নির্মাণ, বর্জ্য নিষ্কাশন ও নাগরিক স্বাস্থ্য সুরক্ষায় আর্থিক অনুদান প্রদানকারী প্রকল্প।",
                "description_hi": "शहरी क्षेत्रों में खुले में शौच से मुक्ति, सामुदायिक स्वच्छता व ठोस कचरा प्रबंधन हेतु बुनियादी ढांचा व सहायता योजना।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Individual & Community Sanitation Grants",
                "benefit_amount_text_bn": "শহুরে স্বাস্থ্যসম্মত শৌচাগার ও কঠিন বর্জ্য ব্যবস্থাপনা অনুদান",
                "application_channels": ["Municipality Office", "Online Portal (sbmurban.org)"],
                "official_portal_url": "https://sbmurban.org"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=sbm_urban,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Urban households lacking individual sanitation access, as well as ULBs and community groups implementing sanitation.",
                "rules_summary_bn": "পৌর এলাকায় বসবাসকারী পরিবার যাদের বাড়িতে স্বাস্থ্যসম্মত শৌচাগার নেই।"
            }
        )
        set_docs(sbm_urban, [
            ("Proof of Identity and Address (Aadhaar / Voter ID)", "আধার কার্ড / ভোটার কার্ড", True, "Mandatory proof of residence within municipal ward"),
            ("Municipal Ward & Property Details / Rent Verification", "পৌর ওয়ার্ড ও হোল্ডিং ট্যাক্স রসিদ", True, "Property assessment tax slip or municipal residence verification"),
            ("Bank Passbook Details", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "For direct benefit transfer with IFSC code")
        ])

        # -------------------------------------------------------------
        # Scheme 32: Swachh Bharat Mission (Grameen) - IHHL
        # -------------------------------------------------------------
        sbm_grameen, _ = Scheme.objects.update_or_create(
            slug="swachh-bharat-mission-grameen",
            defaults={
                "department": prd,
                "category": "health",
                "name_en": "Swachh Bharat Mission (Grameen) - Individual Household Latrine (IHHL)",
                "name_bn": "স্বচ্ছ ভারত মিশন (গ্রামীণ) — মিশন নির্মল বাংলা শৌচাগার অনুদান (IHHL)",
                "name_hi": "स्वच्छ भारत मिशन (ग्रामीण) — व्यक्तिगत घरेलू शौचालय (IHHL)",
                "tagline_en": "Direct financial incentive of ₹12,000 for construction of individual sanitary toilets in rural households",
                "tagline_bn": "গ্রামীণ পরিবারে স্বাস্থ্যসম্মত শৌচাগার নির্মাণের জন্য সরাসরি ₹১২,০০০ আর্থিক সহায়তা",
                "tagline_hi": "ग्रामीण परिवारों में शौचालय निर्माण हेतु सीधे ₹12,000 की वित्तीय सहायता",
                "description_en": "Under Swachh Bharat Mission (Grameen) / Mission Nirmal Bangla, eligible rural households without functional sanitary toilets receive a direct financial incentive of ₹12,000 into their bank account to construct a twin-pit sanitary toilet.",
                "description_bn": "মিশন নির্মল বাংলা / স্বচ্ছ ভারত মিশন গ্রামীণ প্রকল্পের আওতায় গ্রামীণ পরিবারে স্বাস্থ্যসম্মত পাকা শৌচাগার তৈরির জন্য সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ₹১২,০০০ অনুদান দেওয়া হয়।",
                "description_hi": "ग्रामीण क्षेत्रों में स्वच्छ शौचालय निर्माण के लिए पात्र परिवारों को सीधे बैंक खाते में ₹12,000 की प्रोत्साहन राशि दी जाती है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "₹12,000 One-time Direct Financial Incentive",
                "benefit_amount_text_bn": "শৌচাগার নির্মাণের জন্য এককালীন ₹১২,০০০ আর্থিক অনুদান",
                "application_channels": ["Gram Panchayat Office", "BDO Office", "Online Portal (sbm.gov.in)"],
                "official_portal_url": "https://sbm.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=sbm_grameen,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_single_bank_account": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Rural households in West Bengal without a functional sanitary toilet. Priority given to BPL and identified APL (SC/ST, small/marginal farmers, female-headed). Must not have received prior toilet subsidies.",
                "rules_summary_bn": "পশ্চিমবঙ্গের গ্রামীণ এলাকার পরিবার যাদের পাকা শৌচাগার নেই। পূর্বে কোনো সরকারি শৌচাগার অনুদান না পেয়ে থাকা আবশ্যক।"
            }
        )
        set_docs(sbm_grameen, [
            ("Aadhaar Card of Applicant (Head of Household)", "আবেদনকারীর আধার কার্ড", True, "Mandatory Aadhaar card for e-KYC and DBT transfer"),
            ("Bank Passbook Details Linked with Aadhaar", "আধার লিঙ্ক করা ব্যাঙ্ক পাসবই", True, "Showing Account Number, IFSC, and active NPCI DBT status"),
            ("Ration Card / BPL Card", "রেশন কার্ড / বিপিএল কার্ড", True, "Digital ration card or official BPL family survey listing"),
            ("Active Mobile Number", "সক্রিয় মোবাইল নম্বর", True, "For status updates and survey verification"),
            ("Geo-Tagged Photographs of Toilet Construction Site", "শৌচাগার নির্মাণের স্থান ও সমাপ্তির ছবি", True, "Pre-construction and post-construction geo-tagged photographs")
        ])

        # -------------------------------------------------------------
        # Scheme 33: Udyam Registration (MSME)
        # -------------------------------------------------------------
        udyam, _ = Scheme.objects.update_or_create(
            slug="udyam-registration-msme",
            defaults={
                "department": msme,
                "category": "youth",
                "name_en": "Udyam Registration (MSME)",
                "name_bn": "উদ্যম রেজিস্ট্রেশন (MSME)",
                "name_hi": "उद्यम पंजीकरण (MSME)",
                "tagline_en": "Official paperless government registration for Micro, Small, and Medium Enterprises with priority lending and subsidies",
                "tagline_bn": "ক্ষুদ্র ও মাঝারি শিল্পের জন্য সরকারি উদ্যম রেজিস্ট্রেশন ও কম সুদে ঋণ সুবিধা",
                "tagline_hi": "सूक्ष्म, लघु व मध्यम उद्यमों हेतु आधिकारिक सरकारी पंजीकरण व सब्सिडी लाभ",
                "description_en": "Udyam Registration is the official, zero-fee, paperless recognition granted to MSMEs in India. It enables enterprises in West Bengal to access government subsidies, collateral-free credit under CGTMSE, priority sector bank lending, and protection against delayed payments.",
                "description_bn": "ক্ষুদ্র, ছোট ও মাঝারি শিল্পোদ্যোগীদের জন্য কেন্দ্রীয় ও রাজ্য সরকারের আনুষ্ঠানিক সার্টিফিকেট। এর মাধ্যমে ব্যাঙ্ক ঋণ, সরকারি টেন্ডারে অগ্রাধিকার ও বিদ্যুৎ বিলে ভর্তুকি মেলে।",
                "description_hi": "एमएसएमई के लिए आधिकारिक शून्य-शुल्क ऑनलाइन पंजीकरण। इसके तहत बैंकों से सस्ता लोन, सरकारी टेंडर में प्राथमिकता और सरकारी सब्सिडी मिलती है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Official MSME Recognition + Collateral-Free Loans",
                "benefit_amount_text_bn": "সরকারি শিল্প স্বীকৃতি + জামানতমুক্ত ঋণ ও সরকারি ভর্তুকি",
                "application_channels": ["Online Portal (udyamregistration.gov.in)", "District Industries Centre (DIC)"],
                "official_portal_url": "https://udyamregistration.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=udyam,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Any individual, enterprise, proprietorship, partnership, LLP, or private company operating as Micro (Investment ≤ ₹1 Cr & Turnover ≤ ₹5 Cr), Small (Investment ≤ ₹10 Cr & Turnover ≤ ₹50 Cr), or Medium (Investment ≤ ₹50 Cr & Turnover ≤ ₹250 Cr).",
                "rules_summary_bn": "যেকোনো নতুন বা বিদ্যমান ব্যবসা বা কারখানা।"
            }
        )
        set_docs(udyam, [
            ("Aadhaar Card of Proprietor / Partner / Director", "মালিকের আধার কার্ড (মোবাইল লিঙ্ক)", True, "Linked with mobile for OTP verification"),
            ("PAN Card (Proprietor or Business Entity)", "প্যান কার্ড", True, "Mandatory PAN card for verification"),
            ("GSTIN (if applicable under GST laws)", "জিএসটিআইএন (যদি প্রযোজ্য হয়)", False, "Mandatory only if business turnover exceeds statutory threshold"),
            ("Business Address Proof & Bank Details (Account & IFSC)", "ব্যবসার ঠিকানার প্রমাণ ও ব্যাঙ্ক অ্যাকাউন্ট", True, "Bank account passbook and electricity/rental deed"),
            ("National Industrial Classification (NIC) Code", "শিল্পের কাজের ধরন বা এনআইসি কোড", True, "Determined based on manufactured product or service description")
        ])

        # -------------------------------------------------------------
        # Scheme 34: Utkarsh Bangla (PBSSD)
        # -------------------------------------------------------------
        utkarsh, _ = Scheme.objects.update_or_create(
            slug="utkarsh-bangla",
            defaults={
                "department": pbssd,
                "category": "youth",
                "name_en": "Utkarsh Bangla (PBSSD)",
                "name_bn": "উৎকর্ষ বাংলা (PBSSD)",
                "name_hi": "उत्कर्ष बांग्ला (PBSSD)",
                "tagline_en": "Flagship free vocational training and skill development program across all sub-divisions of West Bengal",
                "tagline_bn": "পশ্চিমবঙ্গের যুবক-যুবতীদের জন্য সম্পূর্ণ বিনামূল্যে কর্মমুখী বৃত্তিমূলক প্রশিক্ষণ",
                "tagline_hi": "युवाओं के लिए पूर्णतः निःशुल्क व्यावसायिक कौशल विकास व रोजगार प्रशिक्षण",
                "description_en": "Utkarsh Bangla provides completely non-priced vocational training to school dropouts and unemployed youth in modern industry sectors (IT, electronics, healthcare, automotive, hospitality) with certified job placement assistance.",
                "description_bn": "পশ্চিমবঙ্গ সরকারের সম্পূর্ণ বিনামূল্যে কারিগরি ও বৃত্তিমূলক প্রশিক্ষণ প্রকল্প। বিভিন্ন আধুনিক ট্রেডে প্রশিক্ষণ শেষে সরকারি শংসাপত্র ও চাকরির সুযোগ প্রদান করা হয়।",
                "description_hi": "पश्चिम बंगाल के युवाओं को निःशुल्क वोकेशनल ट्रेनिंग देने वाली योजना। ट्रेनिंग पूरी होने पर प्रमाणित प्रमाण पत्र व जॉब प्लेसमेंट दिया जाता है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "100% Free Vocational Skill Course + Placement",
                "benefit_amount_text_bn": "সম্পূর্ণ বিনামূল্যে বৃত্তিমূলক কোর্স ও চাকরির সুযোগ",
                "application_channels": ["Online Portal (pbssd.gov.in)", "District ITI / Vocational Training Centre"],
                "official_portal_url": "https://pbssd.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=utkarsh,
            defaults={
                "min_age": 18,
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Permanent resident of West Bengal aged 18 to 40 years. School dropouts, Class 8th/10th pass, or higher depending on the course trade.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা। বয়স ১৮ থেকে ৪০ বছর।"
            }
        )
        set_docs(utkarsh, [
            ("Aadhaar Card and Voter ID (EPIC)", "আধার কার্ড ও ভোটার কার্ড", True, "Mandatory proof of residence in West Bengal"),
            ("Academic Marksheets of Highest Qualification", "সর্বোচ্চ শিক্ষাগত যোগ্যতার মার্কশিট", True, "Class 8th / 10th / 12th marksheets or transfer certificate"),
            ("Domicile Certificate / Address Proof", "আবাসিক শংসাপত্র", True, "Issued by Pradhan, Councilor, or BDO/SDO"),
            ("Bank Passbook Copy", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "Student's single bank passbook with IFSC code"),
            ("Passport-Size Photographs", "পাসপোর্ট সাইজ ছবি", True, "Recent colour passport photographs"),
            ("Caste Certificate (if applicable)", "জাতিগত শংসাপত্র (প্রযোজ্য ক্ষেত্রে)", False, "For availing reserved quota seats")
        ])

        # -------------------------------------------------------------
        # Scheme 35: West Bengal Migrant Worker Welfare Scheme (Shramashree / Karmasathi)
        # -------------------------------------------------------------
        migrant, _ = Scheme.objects.update_or_create(
            slug="wb-migrant-worker-welfare",
            defaults={
                "department": labour,
                "category": "social_security",
                "name_en": "West Bengal Migrant Worker Welfare Scheme (Shramashree / Karmasathi)",
                "name_bn": "পশ্চিমবঙ্গ পরিযায়ী শ্রমিক কল্যাণ প্রকল্প (শ্রমশ্রী / কর্মসাথী পরিযায়ী)",
                "name_hi": "पश्चिम बंगाल प्रवासी श्रमिक कल्याण योजना (श्रमश्री / कर्मसाथी)",
                "tagline_en": "Comprehensive social security, ₹2 Lakh accidental insurance, emergency relief, and rehabilitation assistance for migrant workers",
                "tagline_bn": "পরিযায়ী শ্রমিকদের জন্য সামাজিক সুরক্ষা, ২ লাখ টাকার দুর্ঘটনা বীমা ও জরুরি অনুদান",
                "tagline_hi": "प्रवासी श्रमिकों हेतु सामाजिक सुरक्षा, ₹2 लाख दुर्घटना बीमा व पुनर्वास सहायता",
                "description_en": "West Bengal Migrant Worker Welfare Scheme provides registered unorganized migrant workers with ₹2,00,000 accidental death benefit, ₹50,000 permanent disability coverage, ₹30,000 transportation cost for repatriation of dead body, and emergency food and medical assistance during distress.",
                "description_bn": "অন্য রাজ্য বা বিদেশে কর্মরত পশ্চিমবঙ্গের পরিযায়ী শ্রমিকদের জন্য রাজ্য সরকারের সার্বিক সুরক্ষা প্রকল্প। দুর্ঘটনায় মৃত্যুতে ২ লক্ষ টাকা, অঙ্গহানিতে ৫০,০০০ টাকা ও জরুরি অবস্থায় আর্থিক সহায়তা দেওয়া হয়।",
                "description_hi": "अन्य राज्यों में काम करने वाले पश्चिम बंगाल के श्रमिकों के लिए ₹2 लाख दुर्घटना बीमा, आपातकालीन वित्तीय सहायता और पुनर्वास योजना।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "₹2 Lakh Accidental Death Cover + ₹50,000 Disability + Emergency Aid",
                "benefit_amount_text_bn": "২ লক্ষ টাকা দুর্ঘটনা বীমা + ৫০,০০০ টাকা অঙ্গহানি ক্ষতিপূরণ + জরুরি সাহায্য",
                "application_channels": ["Duare Sarkar Camp", "Online Portal (karmasathi.wb.gov.in)", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://karmasathi.wb.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=migrant,
            defaults={
                "min_age": 18,
                "max_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Permanent resident of West Bengal who has migrated or intends to migrate to other states or abroad for work, registered on Karmasathi / Shramashree portal.",
                "rules_summary_bn": "ভিনরাজ্যে বা বিদেশে কর্মরত পশ্চিমবঙ্গের স্থায়ী বাসিন্দা এবং কর্মসাথী পোর্টালে নথিভুক্ত পরিযায়ী শ্রমিক।"
            }
        )
        set_docs(migrant, [
            ("Aadhaar Card and Voter ID (EPIC)", "আধার কার্ড ও ভোটার কার্ড", True, "Proof of identity and West Bengal residence"),
            ("Household Ration Card", "পারিবারিক রেশন কার্ড", True, "Digital ration card copy of the family"),
            ("Migrant Worker Identification Number (MWIN/MWINP Receipt)", "পরিযায়ী শ্রমিক রেজিস্ট্রেশন নম্বর (MWIN)", True, "Registration acknowledgment slip from karmasathi.wb.gov.in"),
            ("Bank Passbook Copy", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "Active savings bank passbook with IFSC code for emergency DBT"),
            ("Passport and Valid Work Visa (for Overseas Workers)", "পাসপোর্ট ও কাজের ভিসা (বিদেশে কর্মরতদের জন্য)", False, "Mandatory only if working in a foreign nation"),
            ("Details & Mobile Number of Employer / Contractor", "নিয়োগকর্তা বা ঠিকাদারের মোবাইল নম্বর ও বিবরণ", True, "Contact details of workplace employer or contractor outside Bengal")
        ])

        # -------------------------------------------------------------
        # Scheme 34: Aadhaar Enrolment and Seeding
        # -------------------------------------------------------------
        aadhaar_sc, _ = Scheme.objects.update_or_create(
            slug="aadhaar-enrolment-seeding",
            defaults={
                "department": uidai,
                "category": "social_security",
                "name_en": "Aadhaar Enrolment and Seeding",
                "name_bn": "আধার নথিভুক্তি ও ব্যাঙ্ক সিডিং",
                "name_hi": "आधार नामांकन एवं बैंक सीडिंग",
                "tagline_en": "Universal biometric digital identity and NPCI-DBT bank account seeding",
                "tagline_bn": "সার্বজনীন ডিজিটাল পরিচয়পত্র এবং সরকারি সুযোগ-সুবিধার জন্য আধার-ডিবিটি ব্যাঙ্ক সিডিং",
                "tagline_hi": "सार्वभौमिक डिजिटल पहचान नामांकन और डीबीटी लाभ प्राप्ति हेतु आधार-बैंक सीडिंग",
                "description_en": "Aadhaar provides a unique 12-digit biometric identity for all residents of India. Aadhaar bank seeding links this unique identity to active bank accounts, ration cards, and social welfare programs to facilitate seamless Direct Benefit Transfer (DBT).",
                "description_bn": "আধার নথিভুক্তি ভারতের সকল নাগরিককে একটি ১২ সংখ্যার অনন্য ডিজিটাল পরিচয় প্রদান করে। আধার ব্যাঙ্ক সিডিংয়ের মাধ্যমে ব্যাংক অ্যাকাউন্ট ও রেশন কার্ডে আধার যুক্ত হয়, যার ফলে সমস্ত সরকারি আর্থিক সুবিধা সরাসরি ডিবিটি-র মাধ্যমে পৌঁছায়।",
                "description_hi": "आधार नामांकन सभी भारतीय निवासियों को 12 अंकों की विशिष्ट पहचान प्रदान करता है। बैंक सीडिंग के माध्यम से इसे सक्रिय बैंक खातों और योजनाओं से जोड़ा जाता है जिससे डीबीटी सहायता मिलती है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Universal 12-digit Identity + Direct Benefit Transfer (DBT) Seeding",
                "benefit_amount_text_bn": "১২ সংখ্যার ডিজিটাল আধার পরিচয় + সরকারি প্রকল্পের ডিবিটি সুবিধা সক্রিয়করণ",
                "application_channels": ["Aadhaar Enrolment Centre", "Post Office / Bank Branch", "Duare Sarkar Camp", "UIDAI Portal (m-Aadhaar)"],
                "official_portal_url": "https://uidai.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=aadhaar_sc,
            defaults={
                "min_age": None,
                "max_age": None,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Enrolment: Any individual resident of India residing for 182 days or more in the preceding 12 months, regardless of age or gender. Seeding: Any citizen holding an active bank account, ration card, LPG connection, or voter identity card seeking DBT/government benefit delivery.",
                "rules_summary_bn": "নথিভুক্তি: বিগত ১২ মাসে ১৮২ দিন বা তার বেশি ভারতে বসবাসকারী যে কোনো ভারতীয় বাসিন্দা (বয়স বা লিঙ্গ নির্বিশেষে)। সিডিং: ডিবিটি বা সরকারি সুবিধা পেতে যে কোনো নাগরিকের সক্রিয় ব্যাঙ্ক অ্যাকাউন্ট, রেশন কার্ড, এলপিজি সংযোগ বা ভোটার কার্ড থাকা আবশ্যক।"
            }
        )
        set_docs(aadhaar_sc, [
            ("Proof of Identity (PoI)", "পরিচয়ের প্রমাণপত্র (PoI)", True, "Passport, PAN Card, Voter ID, Driving Licence, or Government photo ID"),
            ("Proof of Address (PoA)", "ঠিকানার প্রমাণপত্র (PoA)", True, "Electricity/water/gas bill (last 3 months), bank/post office passbook, or registered rent agreement"),
            ("Proof of Date of Birth (DoB)", "জন্ম তারিখের প্রমাণপত্র (DoB)", True, "Birth certificate, SSLC/10th admit card, or marksheet"),
            ("Documents for Minors (Baal Aadhaar)", "নাবালকদের নথি (বাল আধার)", False, "Birth certificate of the child and Aadhaar card of either parent (with biometric consent)"),
            ("Bank Seeding / NPCI Mapping Mandate Form", "আধার সিডিং / এনপিসিআই সম্মতি ফর্ম", True, "Completed Aadhaar Seeding / NPCI Mapping consent mandate form along with a bank passbook copy")
        ])

        # -------------------------------------------------------------
        # Scheme 35: Agriculture Infrastructure Fund (AIF)
        # -------------------------------------------------------------
        aif_sc, _ = Scheme.objects.update_or_create(
            slug="agriculture-infrastructure-fund",
            defaults={
                "department": moa,
                "category": "agriculture",
                "name_en": "Agriculture Infrastructure Fund (AIF)",
                "name_bn": "কৃষি পরিকাঠামো তহবিল (AIF)",
                "name_hi": "कृषि अवसंरचना कोष (AIF)",
                "tagline_en": "Medium-long term debt financing facility with 3% interest subvention for post-harvest agri-infrastructure",
                "tagline_bn": "ফসলোত্তর পরিকাঠামো এবং আধুনিক খামার ব্যবস্থার জন্য ৩% সুদ রেয়াতি ঋণ সহায়তা",
                "tagline_hi": "फसल कटाई बाद प्रबंधन व आधुनिक कृषि संपत्तियों के निर्माण हेतु 3% ब्याज छूट पर बैंक ऋण",
                "description_en": "Agriculture Infrastructure Fund (AIF) provides medium to long-term debt financing for post-harvest management infrastructure (cold storages, warehouses, silos, pack houses) and community farming assets with a 3% interest subvention up to ₹2 Crore and credit guarantee coverage.",
                "description_bn": "কৃষি পরিকাঠামো তহবিল (AIF) হল একটি বিশেষ ঋণ প্রকল্প যা কোল্ড স্টোরেজ, গুদাম, সাইলো, প্যাকিং ইউনিট এবং আধুনিক খামার পরিকাঠামো গড়ার জন্য ৩% বার্ষিক সুদের ছাড় ও ক্রেডিট গ্যারান্টি সুবিধা প্রদান করে।",
                "description_hi": "कृषि अवसंरचना कोष (AIF) फसल कटाई के बाद गोदाम, कोल्ड स्टोरेज, साइलो और सामुदायिक कृषि परिसंपत्तियों के निर्माण के लिए 3% वार्षिक ब्याज छूट और बैंक गारंटी के साथ आसान ऋण प्रदान करता है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Up to ₹2 Crore Loan with 3% Interest Subvention (up to 7 years) + Credit Guarantee",
                "benefit_amount_text_bn": "২ কোটি টাকা পর্যন্ত ঋণে ৩% সুদের ছাড় (৭ বছর) + ক্রেডিট গ্যারান্টি সুরক্ষা",
                "application_channels": ["AIF Online Portal (agriinfra.dac.gov.in)", "Scheduled Commercial Banks", "State Cooperative Banks", "NABARD"],
                "official_portal_url": "https://agriinfra.dac.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=aif_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "Primary Agricultural Credit Societies (PACS), Marketing Cooperative Societies, FPOs, SHGs, JLGs, Multipurpose Cooperative Societies, Agri-entrepreneurs, and startups. Investment must be directed toward post-harvest management infrastructure or community farming assets.",
                "rules_summary_bn": "যোগ্য আবেদনকারী: প্রাথমিক কৃষি ঋণ সমিতি (PACS), সমবায় বিপণন সমিতি, FPO, স্বনির্ভর দল (SHG), যৌথ দায়বদ্ধতা দল (JLG), কৃষি-উদ্যোক্তা এবং স্টার্টআপ। বিনিয়োগ অবশ্যই ফসলোত্তর পরিকাঠামো বা কৃষি সম্পদের জন্য হতে হবে।"
            }
        )
        set_docs(aif_sc, [
            ("KYC Documents of Promoter / Directors", "প্রবর্তকের কেওয়াইসি নথি (আধার ও প্যান)", True, "KYC documents of the promoter/partners/directors (Aadhaar, PAN card)"),
            ("Business Registration / Incorporation Certificate", "ব্যবসায়িক নিবন্ধন প্রশংসাপত্র", True, "Business registration/incorporation certificate, partnership deed, or society bylaws"),
            ("Detailed Project Report (DPR)", "বিস্তারিত প্রকল্প রিপোর্ট (DPR)", True, "Detailed Project Report (DPR) detailing project costs, financial viability, and capacity"),
            ("Land Ownership Documents (RoR) / Lease Deed", "জমির মালিকানা রেকর্ড বা লিজ চুক্তি", True, "Land ownership documents (RoR/Khatian) or registered long-term lease agreement"),
            ("Bank Statements & Audited Financials / ITR", "ব্যাঙ্ক স্টেটমেন্ট ও অডিট রিপোর্ট / আইটিআর", True, "Bank statements (last 1 year) and audited financials / ITR (last 3 years, if applicable)"),
            ("Statutory Sanctions & Clearance Approvals", "স্থানীয় পঞ্চায়েত/পৌরসভার অনুমোদন ও ক্লিয়ারেন্স", True, "Local municipal/Panchayat sanctions and statutory clearance approvals")
        ])

        # -------------------------------------------------------------
        # Scheme 36: Annapurna Bhandar / Annapurna Yojana (West Bengal Social Registry)
        # -------------------------------------------------------------
        annapurna_sc, _ = Scheme.objects.update_or_create(
            slug="annapurna-senior-food-security",
            defaults={
                "department": food,
                "category": "social_security",
                "name_en": "Annapurna Bhandar / Annapurna Yojana (WB Social Registry & Food Security)",
                "name_bn": "অন্নপূর্ণা ভাণ্ডার / অন্নপূর্ণা যোজনা (পশ্চিমবঙ্গ সামাজিক রেজিস্ট্রি ও খাদ্য সুরক্ষা)",
                "name_hi": "अन्नपूर्णा भंडार / अन्नपूर्णा योजना (पश्चिम बंगाल सामाजिक रजिस्ट्री एवं खाद्य सुरक्षा)",
                "tagline_en": "10 kg free foodgrains monthly for indigent senior citizens aged 65+ and vulnerable female welfare assistance",
                "tagline_bn": "৬৫+ অসহায় প্রবীণ নাগরিকদের জন্য মাসিক ১০ কেজি বিনামূল্যে খাদ্যশস্য ও প্রান্তিক মহিলাদের আর্থিক সুরক্ষা",
                "tagline_hi": "65+ निराश्रित बुजुर्गों को मासिक 10 किग्रा मुफ्त खाद्यान्न एवं पात्र महिलाओं को सामाजिक सुरक्षा",
                "description_en": "Annapurna Bhandar / Annapurna Yojana provides social security benefits alongside monthly foodgrains assistance to indigent senior citizens and vulnerable households via the West Bengal Social Registry.",
                "description_bn": "অন্নপূর্ণা ভাণ্ডার / অন্নপূর্ণা যোজনার আওতায় পশ্চিমবঙ্গ সামাজিক রেজিস্ট্রির মাধ্যমে অসহায় প্রবীণ নাগরিক ও আর্থিকভাবে অনগ্রসর পরিবারগুলোকে সামাজিক সুরক্ষা এবং খাদ্য সহায়তা প্রদান করা হয়।",
                "description_hi": "अन्नपूर्णा भंडार / अन्नपूर्णा योजना के अंतर्गत पश्चिम बंगाल सामाजिक रजिस्ट्री के माध्यम से पात्र वरिष्ठ नागरिकों और कमजोर परिवारों को सामाजिक सुरक्षा व खाद्यान्न सहायता प्रदान की जाती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "10 kg Free Foodgrains (Rice/Wheat) per Month + Social Welfare Assistance",
                "benefit_amount_text_bn": "প্রতি মাসে ১০ কেজি বিনামূল্যে খাদ্যশস্য (চাল/গম) + সামাজিক কল্যাণ সহায়তা",
                "application_channels": ["West Bengal Social Registry Portal (socialregistry.wb.gov.in)", "Gram Panchayat / BDO Office", "Municipality / SDO Office", "Duare Sarkar Camp"],
                "official_portal_url": "https://socialregistry.wb.gov.in/"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=annapurna_sc,
            defaults={
                "min_age": 65,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 1200000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "National / PDS Framework: Indigent senior citizens aged 65 years or above who are eligible for NOAPS but not receiving any regular pension or government financial assistance. State Special Framework: Female residents from economically vulnerable households with personal monthly income under ₹10,000 and total family annual income within prescribed limits (under ₹12 lakh), not employed in regular government service.",
                "rules_summary_bn": "জাতীয়/পিডিএস কাঠামো: ৬৫ বা তার বেশি বয়সী অসহায় প্রবীণ নাগরিক যারা কোনো নিয়মিত পেনশন বা সরকারি সাহায্য পাচ্ছেন না। রাজ্য বিশেষ কাঠামো: মাসিক ₹১০,০০০-এর কম ব্যক্তিগত আয় এবং বাৎসরিক ₹১২ লাখের কম পারিবারিক আয়ের মহিলারা।"
            }
        )
        set_docs(annapurna_sc, [
            ("Aadhaar Card of Applicant", "আবেদনকারীর আধার কার্ড", True, "Aadhaar card of the applicant"),
            ("Digital Ration Card / Food Security Card", "ডিজিটাল রেশন কার্ড / খাদ্য সুরক্ষা কার্ড", True, "Digital Ration Card / Food Security card"),
            ("Voter ID Card (EPIC) & Residential Proof", "ভোটার কার্ড ও বসবাসের প্রমাণপত্র", True, "Voter ID card (EPIC) and residential proof"),
            ("Age Proof Document", "বয়সের প্রমাণপত্র", True, "Age proof (admit card, school leaving certificate, or birth record)"),
            ("Bank Passbook Copy (Aadhaar-Seeded)", "আধার সিডেড ব্যাঙ্ক পাসবুক", True, "Bank account passbook copy (Aadhaar-seeded for DBT)"),
            ("Non-Receipt of Pension Declaration / Income Certificate", "পেনশন না-পাওয়ার ঘোষণাপত্র বা আয় শংসাপত্র", True, "Non-receipt of pension declaration / Income certificate issued by BDO/SDO")
        ])

        # -------------------------------------------------------------
        # Scheme 37: Atal Pension Yojana (APY)
        # -------------------------------------------------------------
        apy_sc, _ = Scheme.objects.update_or_create(
            slug="atal-pension-yojana",
            defaults={
                "department": dfs,
                "category": "social_security",
                "name_en": "Atal Pension Yojana (APY)",
                "name_bn": "অটল পেনশন যোজনা (APY)",
                "name_hi": "अटल पेंशन योजना (APY)",
                "tagline_en": "Guaranteed monthly pension of ₹1,000 to ₹5,000 after age 60 for unorganized workers",
                "tagline_bn": "৬০ বছর বয়সের পর থেকে আজীবন মাসিক ₹১,০০০ থেকে ₹৫,০০০ নিশ্চিত সরকারি পেনশন",
                "tagline_hi": "60 वर्ष की आयु के बाद ₹1,000 से ₹5,000 की आजीवन मासिक पेंशन",
                "description_en": "Atal Pension Yojana (APY) provides a guaranteed minimum monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000 or ₹5,000 to subscribers starting at the age of 60 based on modest periodic contributions made between ages 18 and 40.",
                "description_bn": "অটল পেনশন যোজনা (APY) হলো ভারত সরকারের একটি পেনশন প্রকল্প যা অসংগঠিত ক্ষেত্রের কর্মীদের জন্য পরিকল্পিত। ১৮ থেকে ৪০ বছর বয়সে যোগ দিয়ে ৬০ বছর বয়স থেকে প্রতি মাসে ১,০০০ থেকে ৫,০০০ টাকা নিশ্চিত পেনশন পাওয়া যায়।",
                "description_hi": "अटल पेंशन योजना (APY) असंगठित क्षेत्र के कामगारों के लिए सरकार समर्थित योजना है जिसमें 60 वर्ष की आयु के बाद ₹1,000 से ₹5,000 की आजीवन मासिक पेंशन मिलती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "Guaranteed ₹1,000 to ₹5,000 / month Pension + Spouse Pension & Corpus to Nominee",
                "benefit_amount_text_bn": "৬০ বছর পর নিশ্চিত মাসিক ₹১,০০০-₹৫,০০০ পেনশন + পত্নী পেনশন ও নমিনিকে এককালীন তহবিল",
                "application_channels": ["Bank Branch (Savings Account Branch)", "Post Office", "Net Banking / Mobile Banking App", "Duare Sarkar Banking Desk"],
                "official_portal_url": "https://npai.pfrda.org.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=apy_sc,
            defaults={
                "min_age": 18,
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Any Indian citizen aged between 18 and 40 years holding an active individual savings bank account or post office savings account. Must not be an income tax payer (individuals who have been income tax assessees are ineligible for fresh enrolment). Auto-debit consent required for periodic contributions up to age 60.",
                "rules_summary_bn": "১৮ থেকে ৪০ বছর বয়সী ভারতীয় নাগরিক, যাঁর সক্রিয় সেভিংস ব্যাংক বা পোস্ট অফিস অ্যাকাউন্ট আছে। আয়করদাতা হলে চলবে না। ৬০ বছর পর্যন্ত নিয়মিত অবদানের অটো-ডেবিট সম্মতি দিতে হবে।"
            }
        )
        set_docs(apy_sc, [
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar card"),
            ("Savings Bank Account Passbook / Cheque", "সেভিংস ব্যাংক পাসবুক বা চেক", True, "Savings bank account number and IFSC code (passbook copy/cheque)"),
            ("Completed APY Application & Auto-Debit Mandate Form", "আবেদন ও অটো-ডেবিট ম্যান্ডেট ফর্ম", True, "Completed APY application-cum-auto-debit mandate form"),
            ("Nominee and Spouse Details", "নমিনি ও জীবনসঙ্গীর বিবরণ", True, "Nominee and spouse details"),
            ("Active Mobile Number", "সক্রিয় মোবাইল নম্বর", True, "Active mobile number")
        ])

        # -------------------------------------------------------------
        # Scheme 38: Beti Bachao Beti Padhao (BBBP) Yojana
        # -------------------------------------------------------------
        bbbp_sc, _ = Scheme.objects.update_or_create(
            slug="beti-bachao-beti-padhao",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Beti Bachao Beti Padhao (BBBP) Yojana",
                "name_bn": "বেটি বাঁচাও বেটি পড়াও যোজনা",
                "name_hi": "बेटी बचाओ बेटी पढ़ाओ (BBBP) योजना",
                "tagline_en": "Inter-ministerial national initiative ensuring survival, institutional health, and education of girl children",
                "tagline_bn": "কন্যা সন্তানের সুরক্ষা, প্রাতিষ্ঠানিক স্বাস্থ্যসেবা ও সর্বজনীন শিক্ষার সর্বভারতীয় উদ্যোগ",
                "tagline_hi": "बालिकाओं के संरक्षण, स्वास्थ्य एवं गुणवत्तापूर्ण शिक्षा सुनिश्चित करने हेतु राष्ट्रीय अभियान",
                "description_en": "Beti Bachao Beti Padhao (BBBP) is an inter-ministerial national advocacy and institutional access campaign ensuring the survival, protection, institutional healthcare (MCP tracking), and secondary education of the girl child, linked with financial tools like Sukanya Samriddhi Yojana (SSY).",
                "description_bn": "বেটি বাঁচাও বেটি পড়াও একটি আন্তঃমন্ত্রণালয় জাতীয় উদ্যোগ যা কন্যা সন্তানের জন্ম হার বৃদ্ধি, স্বাস্থ্য কার্ড (MCP কার্ড) ও শিক্ষা নিশ্চিত করে এবং সুকন্যা সমৃদ্ধি যোজনার মতো আর্থিক প্রকল্পের সাথে যুক্ত করে।",
                "description_hi": "बेटी बचाओ बेटी पढ़ाओ (BBBP) बालिकाओं की सुरक्षा, स्वास्थ्य ट्रैकिंग और शिक्षा को बढ़ावा देने वाला राष्ट्रीय अभियान है, जो सुकन्या समृद्धि योजना (SSY) जैसी बचत योजनाओं से सीधा जुड़ता है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Institutional Healthcare & Education Entitlements + SSY / Kanyashree Linkage",
                "benefit_amount_text_bn": "প্রাতিষ্ঠানিক স্বাস্থ্য ও শিক্ষা সহায়তা + সুকন্যা সমৃদ্ধি ও কন্যাশ্রী প্রকল্পের সংযোগ",
                "application_channels": ["Anganwadi Centres (ICDS)", "Gram Panchayat / Block Office", "Primary Health Centres (PHC)", "Local Schools"],
                "official_portal_url": "https://wcd.gov.in/women/beti-bachao-beti-padhao"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=bbbp_sc,
            defaults={
                "min_age": 0,
                "max_age": 18,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Targets every Indian family with a girl child. Eligibility focuses on institutional access: pregnant and lactating mothers registering their pregnancy (MCP card) and newborn girl children accessing institutional healthcare and education. Links directly with financial tools like Sukanya Samriddhi Yojana (SSY).",
                "rules_summary_bn": "কন্যা সন্তান রয়েছে এমন সমস্ত ভারতীয় পরিবার। প্রাতিষ্ঠানিক সহায়তা: গর্ভবতী মায়েদের রেজিস্ট্রেশন (MCP কার্ড) এবং নবজাতক কন্যার স্বাস্থ্যসেবা ও বিদ্যালয়ে ভর্তি নিশ্চিতকরণ।"
            }
        )
        set_docs(bbbp_sc, [
            ("Mother and Child Protection (MCP) Card", "মা ও শিশু সুরক্ষা (MCP) কার্ড", True, "Mother and Child Protection (MCP) card"),
            ("Birth Certificate of the Girl Child", "কন্যা সন্তানের জন্ম শংসাপত্র", True, "Birth Certificate of the girl child"),
            ("Aadhaar Cards of Parents / Guardians", "পিতা-মাতার আধার কার্ড", True, "Aadhaar cards of the parents/guardians"),
            ("School Enrollment / Bonafide Certificate", "বিদ্যালয়ে ভর্তির প্রশংসাপত্র", True, "School enrollment/bonafide certificate for secondary educational tracking")
        ])

        # -------------------------------------------------------------
        # Scheme 39: Bina Mulya Samajik Suraksha Yojana (BMSSY - West Bengal)
        # -------------------------------------------------------------
        bmssy_sc, _ = Scheme.objects.update_or_create(
            slug="bmssy-west-bengal",
            defaults={
                "department": labour,
                "category": "social_security",
                "name_en": "Bina Mulya Samajik Suraksha Yojana (BMSSY)",
                "name_bn": "বিনা মূল্যে সামাজিক সুরক্ষা যোজনা (BMSSY)",
                "name_hi": "बिना मूल्य सामाजिक सुरक्षा योजना (BMSSY)",
                "tagline_en": "State-funded social security, provident fund, and accident insurance for unorganized workers in West Bengal",
                "tagline_bn": "পশ্চিমবঙ্গের অসংগঠিত শ্রমিকদের জন্য সম্পূর্ণ বিনামূল্যে প্রভিডেন্ট ফান্ড ও দুর্ঘটনা বীমা সুরক্ষা",
                "tagline_hi": "पश्चिम बंगाल के असंगठित कामगारों के लिए 100% राज्य प्रायोजित सामाजिक सुरक्षा व भविष्य निधि",
                "description_en": "Bina Mulya Samajik Suraksha Yojana (BMSSY) integrates social security for unorganized workers across 46 industries and 15 self-employed occupations in West Bengal, providing full state contribution to provident funds, accidental death relief of ₹2,00,000, and education stipends.",
                "description_bn": "পশ্চিমবঙ্গের শ্রম দপ্তরের বিনা মূল্যে সামাজিক সুরক্ষা যোজনায় (BMSSY) ৪৬টি অসংগঠিত শিল্প এবং ১৫টি স্বনিযুক্ত পেশার শ্রমিকদের সম্পূর্ণ সরকারি খরচে প্রভিডেন্ট ফান্ড, মৃত্যু বা দুর্ঘটনাজনিত ক্ষতিপূরণ এবং সন্তানদের শিক্ষার অনুদান দেওয়া হয়।",
                "description_hi": "बीना मूल्य सामाजिक सुरक्षा योजना (BMSSY) पश्चिम बंगाल के 46 असंगठित उद्योगों और 15 स्वरोजगार व्यवसायों के कामगारों को पूर्णतः मुफ्त भविष्य निधि, ₹2 लाख तक का दुर्घटना बीमा और चिकित्सा सहायता प्रदान करती है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Free State PF Contribution + ₹2,00,000 Accidental Death Cover + Educational Grants",
                "benefit_amount_text_bn": "বিনামূল্যে সরকারি পিএফ অনুদান + ₹২,০০,০০০ দুর্ঘটনা বীমা + সন্তানদের শিক্ষাবৃত্তি",
                "application_channels": ["Duare Sarkar Camp", "Regional Labour Office (RLO)", "Labour Welfare Facilitation Centre (LWFC)", "BMSSY Online Portal"],
                "official_portal_url": "https://bmssy.wblabour.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=bmssy_sc,
            defaults={
                "min_age": 18,
                "max_age": 60,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 78000,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Permanent resident of West Bengal aged between 18 and 60 years engaged in notified unorganized industries (46 sectors) or self-employed categories (15 occupations, such as carpenters, barbers, street hawkers, rickshaw pullers). Monthly family income must not exceed ₹6,500 (no income cap applies to building/construction and transport workers).",
                "rules_summary_bn": "পশ্চিমবঙ্গের ১৮ থেকে ৬০ বছর বয়সী অসংগঠিত শ্রমিক (৪৬টি শিল্প ও ১৫টি পেশা)। মাসিক পারিবারিক আয় অনূর্ধ্ব ₹৬,৫০০ (নির্মাণ ও পরিবহন শ্রমিকদের আয়ের কোনো ঊর্ধ্বসীমা নেই)।"
            }
        )
        set_docs(bmssy_sc, [
            ("Aadhaar Card and Voter ID (EPIC)", "আধার কার্ড ও ভোটার কার্ড", True, "Aadhaar card and Voter ID (EPIC)"),
            ("Digital Ration Card", "ডিজিটাল রেশন কার্ড", True, "Digital Ration Card"),
            ("Bank Passbook Copy (Aadhaar Seeded)", "আধার লিঙ্কড ব্যাঙ্ক পাসবুক", True, "Bank passbook copy (showing IFSC and Aadhaar seeding)"),
            ("Passport-Size Photographs & Specimen Signature", "পাসপোর্ট সাইজ ছবি ও স্বাক্ষর", True, "Passport-size photographs and specimen signature"),
            ("Self-Declaration / Trade Proof", "পেশার স্ব-ঘোষণাপত্র / প্রত্যয়ন", True, "Self-declaration / Trade or unorganized profession proof certified by a local councillor or Panchayat representative")
        ])

        # -------------------------------------------------------------
        # Scheme 40: Citizenship Amendment Act (CAA - 2019)
        # -------------------------------------------------------------
        caa_sc, _ = Scheme.objects.update_or_create(
            slug="citizenship-amendment-act",
            defaults={
                "department": mha,
                "category": "social_security",
                "name_en": "Citizenship Amendment Act (CAA - 2019)",
                "name_bn": "নাগরিকত্ব সংশোধনী আইন (CAA - ২০১৯)",
                "name_hi": "नागरिकता संशोधन अधिनियम (CAA - 2019)",
                "tagline_en": "Statutory citizenship registration portal for minority migrants entering India on or before 31.12.2014",
                "tagline_bn": "৩১ ডিসেম্বর ২০১৪-এর পূর্বে ভারতে আগত ধর্মীয় সংখ্যালঘু শরণার্থীদের ভারতীয় নাগরিকত্ব প্রদান",
                "tagline_hi": "31 दिसंबर 2014 से पूर्व भारत आए प्रताड़ित अल्पसंख्यक प्रवासियों हेतु भारतीय नागरिकता",
                "description_en": "Citizenship Amendment Act (CAA - 2019) enables persecuted minority migrants (Hindus, Sikhs, Buddhists, Jains, Parsis, Christians) from Pakistan, Bangladesh, and Afghanistan who entered India on or before December 31, 2014 to apply for and obtain Indian citizenship via the statutory online portal.",
                "description_bn": "নাগরিকত্ব সংশোধনী আইনের (CAA) আওতায় বাংলাদেশ, পাকিস্তান ও আফগানিস্তান থেকে ধর্মীয় নিপীড়নের কারণে ৩১ ডিসেম্বর ২০১৪ এর পূর্বে ভারতে প্রবেশ করা ৬টি সংখ্যালঘু সম্প্রদায়ের মানুষদের ভারতীয় নাগরিকত্বের জন্য আবেদনের সুযোগ দেওয়া হয়।",
                "description_hi": "नागरिकता संशोधन अधिनियम (CAA - 2019) के तहत पाकिस्तान, बांग्लादेश व अफगानिस्तान से 31 दिसंबर 2014 से पहले भारत आए 6 अल्पसंख्यक समुदायों के प्रवासियों को भारतीय नागरिकता प्रदान करने का प्रावधान है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Certificate of Naturalization / Indian Citizenship under Section 6B",
                "benefit_amount_text_bn": "ধারা ৬বি অনুযায়ী ভারতীয় নাগরিকত্ব শংসাপত্র ও যাবতীয় নাগরিক অধিকার লাভ",
                "application_channels": ["Indian Citizenship Online Portal (indiancitizenshiponline.nic.in)", "District Empowered Committee", "Post Office Portal Helpdesk"],
                "official_portal_url": "https://indiancitizenshiponline.nic.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=caa_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Migrants belonging to six minority religious communities: Hindus, Sikhs, Buddhists, Jains, Parsis, or Christians originating from Pakistan, Bangladesh, or Afghanistan who entered India on or before December 31, 2014. Not residing in Sixth Schedule tribal areas or ILP states.",
                "rules_summary_bn": "পাকিস্তান, বাংলাদেশ বা আফগানিস্তান থেকে ৩১ ডিসেম্বর ২০১৪ এর মধ্যে ভারতে আসা হিন্দু, শিখ, বৌদ্ধ, জৈন, পার্সি বা খ্রিস্টান সম্প্রদায়ের ব্যক্তিরা। ষষ্ঠ তফসিল বা আইএলপি এলাকার বাইরে অবস্থানকারী।"
            }
        )
        set_docs(caa_sc, [
            ("Proof of Nationality of Origin", "উৎপত্তিস্থল দেশের নাগরিকত্বের প্রমাণ", True, "Passport, birth certificate, school/college certificate, tenancy records, or national ID issued by authorities in Pakistan/Bangladesh/Afghanistan"),
            ("Proof of Entry into India on/before 31.12.2014", "৩১.১২.২০১৪-এর পূর্বে ভারতে প্রবেশের প্রমাণ", True, "Visa stamp, FRRO permit, Indian census slip, driving licence, school certificate, or land tenancy deed in India"),
            ("Affidavit & Eligibility Certificate from Community Institution", "যোগ্যতার হলফনামা ও কমিউনিটি প্রত্যয়ন", True, "Affidavit verifying eligibility under the CAA rules and an eligibility certificate from a locally recognized community institution")
        ])

        # -------------------------------------------------------------
        # Scheme 41: Credit Linkage to Self-Help Groups (SHGs)
        # -------------------------------------------------------------
        shg_credit_sc, _ = Scheme.objects.update_or_create(
            slug="credit-linkage-shg",
            defaults={
                "department": mord,
                "category": "women",
                "name_en": "Credit Linkage to Self-Help Groups (SHGs)",
                "name_bn": "স্বনির্ভর দলের (SHG) জন্য ব্যাঙ্ক ক্রেডিট লিঙ্কেজ",
                "name_hi": "स्वयं सहायता समूह (SHG) बैंक क्रेडिट लिंकेज",
                "tagline_en": "Collateral-free institutional subsidized bank loans up to ₹20 Lakh for rural women SHGs",
                "tagline_bn": "গ্রামীণ মহিলা স্বনির্ভর দলগুলির জন্য ২০ লক্ষ টাকা পর্যন্ত জামানতবিহীন স্বল্পসুদে ব্যাঙ্ক ঋণ",
                "tagline_hi": "ग्रामीण महिला स्वयं सहायता समूहों को ₹20 लाख तक का संपार्श्विक-मुक्त रियायती बैंक ऋण",
                "description_en": "Credit Linkage to Self-Help Groups (SHGs) under DAY-NRLM / Anandadhara provides collateral-free institutional credit to women's groups adhering to Panchasutra principles, offering interest subvention down to 7% (or 4% on prompt repayment).",
                "description_bn": "আনন্দধারা (WBSRLM) ও DAY-NRLM-এর অধীনে পঞ্চসূত্র মেনে চলা সক্রিয় মহিলা স্বনির্ভর দলগুলিকে সহজে ব্যবসা ও জীবিকার প্রসারের জন্য জামানতবিহীন প্রাতিষ্ঠানিক ব্যাঙ্ক ঋণ ও সুদের ছাড় দেওয়া হয়।",
                "description_hi": "DAY-NRLM व आनंदधारा के तहत पंचसूत्र का पालन करने वाले सक्रिय महिला SHG समूहों को आसान ब्याज दर पर ₹20 लाख तक का बिना गारंटी का बैंक ऋण उपलब्ध कराया जाता है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Collateral-free Bank Credit from ₹1.5 Lakh up to ₹20 Lakh with Interest Subvention (7% / 4%)",
                "benefit_amount_text_bn": "১.৫ লক্ষ থেকে ২০ লক্ষ টাকা পর্যন্ত জামানতহীন ব্যাঙ্ক ঋণ ও সুদের ছাড়",
                "application_channels": ["Gram Panchayat Sangh / Sangha Co-operative", "Local Bank Branch", "BDO Office (Anandadhara Cell)", "Duare Sarkar Camp"],
                "official_portal_url": "https://nrlm.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=shg_credit_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "The SHG must be in active existence for at least 6 months with updated books of account. Adherence to 'Panchasutra' principles: Regular meetings, regular savings, regular internal lending, timely recovery, and proper maintenance of books. Qualified under grading norms prescribed by NABARD / State Rural Livelihood Mission. Minimum 70% of members must be from poor households (for DAY-NRLM groups).",
                "rules_summary_bn": "স্বনির্ভর দলটির বয়স ন্যূনতম ৬ মাস হতে হবে এবং হিসাবের খাতা আপডেট থাকতে হবে। 'পঞ্চসূত্র' নীতি পালন বাধ্যতামূলক। নাবার্ড/এনআরএলএম গ্রেডিংয়ে উত্তীর্ণ হতে হবে। অন্তত ৭০% সদস্য দরিদ্র পরিবারের হতে হবে।"
            }
        )
        set_docs(shg_credit_sc, [
            ("Loan Application Form with Approved MCP", "ঋণ আবেদন ফর্ম ও মাইক্রো-ক্রেডিট প্ল্যান (MCP)", True, "Loan application form along with the group's approved Micro-Credit Plan (MCP)"),
            ("SHG Loan Resolution Signed by All Members", "সকল সদস্যের স্বাক্ষরিত দলীয় রেজোলিউশন", True, "Resolution of the SHG to apply for a bank loan, signed by all group members"),
            ("KYC Documents of Office Bearers and Members", "কর্মকর্তা ও সকল সদস্যের কেওয়াইসি", True, "KYC documents (Aadhaar, PAN/Form 60, photos) of authorized office bearers (President, Secretary, Cashier) and all members"),
            ("SHG Grading Sheet / Appraisal Score", "স্বনির্ভর দলের গ্রেডিং মূল্যায়ন পত্র", True, "SHG grading sheet / appraisal score from NRLM/Sponsoring agency"),
            ("Savings Bank Passbook & Account Audit Statement", "ব্যাঙ্ক পাসবুক ও অডিট রিপোর্ট", True, "Existing savings bank passbook and account audit/statement")
        ])

        # -------------------------------------------------------------
        # Scheme 42: Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)
        # -------------------------------------------------------------
        ddugky_sc, _ = Scheme.objects.update_or_create(
            slug="ddu-gky",
            defaults={
                "department": pbssd,
                "category": "youth",
                "name_en": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
                "name_bn": "দীন দয়াল উপাধ্যায় গ্রামীণ কৌশল্য যোজনা (DDU-GKY)",
                "name_hi": "दीन दयाल उपाध्याय ग्रामीण कौशल्य योजना (DDU-GKY)",
                "tagline_en": "Free residential vocational placement-linked skill training for rural poor youth aged 15-35",
                "tagline_bn": "১৫-৩৫ বছর বয়সী গ্রামীণ যুবক-যুবতীদের জন্য বিনামূল্যে থাকা-খাওয়াসহ নিশ্চিত কর্মসংস্থানমুখী প্রশিক্ষণ",
                "tagline_hi": "15-35 वर्ष के ग्रामीण युवाओं के लिए निःशुल्क आवासीय कौशल प्रशिक्षण व रोजगार गारंटी",
                "description_en": "DDU-GKY is a placement-linked skill training initiative under the Ministry of Rural Development for rural poor youth, guaranteeing at least 70% job placement, free boarding, lodging, uniform, tablets, and post-placement stipend support.",
                "description_bn": "গ্রামীণ উন্নয়ন মন্ত্রকের অধীনে ডিডিইউ-জিকেওয়াই (DDU-GKY) প্রকল্পের মাধ্যমে গ্রামীণ দারিদ্র্যসীমার নিচের যুবক-যুবতীদের সম্পূর্ণ বিনামূল্যে আধুনিক কারিগরি ও বৃত্তিমূলক প্রশিক্ষণ দিয়ে নিশ্চিত চাকরির সুযোগ করে দেওয়া হয়।",
                "description_hi": "DDU-GKY ग्रामीण विकास मंत्रालय द्वारा संचालित कौशल विकास योजना है, जिसमें ग्रामीण निर्धन युवाओं को मुफ्त आवासीय प्रशिक्षण और कम से कम 70% सुनिश्चित प्लेसमेंट (नौकरी) की गारंटी दी जाती है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "100% Free Residential Skill Training + Guaranteed Job Placement + Post-Placement Support",
                "benefit_amount_text_bn": "বিনামূল্যে আবাসিক প্রশিক্ষণ + নিশ্চিত চাকরি (ন্যূনতম ₹৬,০০০-₹১৫,০০০/মাস) + স্টাইপেন্ড",
                "application_channels": ["Gram Panchayat Office", "District PBSSD / DDU-GKY Center", "Kaushal Panjee Portal", "Duare Sarkar Camp"],
                "official_portal_url": "https://ddugky.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=ddugky_sc,
            defaults={
                "min_age": 15,
                "max_age": 35,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Rural youth aged between 15 and 35 years (upper age relaxed up to 45 years for women, PwDs, and Special Groups like PVTGs). Household must belong to economically poor backgrounds verified through: BPL card, AAY card, active MGNREGA household (with at least 15 days of work in the previous financial year), or members of NRLM SHGs.",
                "rules_summary_bn": "১৫ থেকে ৩৫ বছর বয়সী গ্রামীণ যুবক-যুবতী (মহিলা, বিশেষভাবে সক্ষম ও বিশেষ আদিবাসীদের ক্ষেত্রে ৪৫ বছর পর্যন্ত শিথিলযোগ্য)। বিপিএল/এএওয়াই কার্ড, একশো দিনের কাজের জব কার্ড (১৫ দিনের কাজ) অথবা স্বনির্ভর দলের সদস্য পরিবার।"
            }
        )
        set_docs(ddugky_sc, [
            ("Aadhaar Card or Voter ID", "আধার কার্ড বা ভোটার কার্ড", True, "Aadhaar card or Voter ID (proof of identity and age)"),
            ("Proof of Rural Residence", "গ্রামীণ আবাসিক প্রশংসাপত্র", True, "Proof of rural residence (Panchayat domicile certificate / Ration Card)"),
            ("Proof of Poverty Entitlement (BPL / AAY / MGNREGA)", "দারিদ্র্যসীমার প্রমাণপত্র (BPL/AAY/NREGA)", True, "Proof of poverty entitlement: BPL card, Antyodaya Anna Yojana (AAY) card, or MGNREGA Job Card"),
            ("Educational Certificates and Marksheets", "শিক্ষাগত যোগ্যতার সার্টিফিকেট ও মার্কশিট", True, "Educational certificates and mark sheets (Class 8, 10, or 12)"),
            ("Caste / PwD Certificate (if applicable)", "জাতিগত বা প্রতিবন্ধী শংসাপত্র (প্রযোজ্য ক্ষেত্রে)", False, "Caste certificate / PwD certificate (if applicable)"),
            ("Aadhaar-Linked Bank Passbook", "আধার লিঙ্ক করা ব্যাঙ্ক পাসবুক", True, "Aadhaar-linked bank passbook")
        ])

        # -------------------------------------------------------------
        # Scheme 43: Deen Dayal Upadhyaya National Rural Livelihoods Mission (DAY-NRLM / Anandadhara)
        # -------------------------------------------------------------
        day_nrlm_sc, _ = Scheme.objects.update_or_create(
            slug="day-nrlm-anandadhara",
            defaults={
                "department": prd,
                "category": "women",
                "name_en": "DAY-NRLM / Anandadhara (State Rural Livelihoods Mission)",
                "name_bn": "আনন্দধারা / ডে-এনআরএলএম (রাজ্য গ্রামীণ জীবিকা মিশন)",
                "name_hi": "डे-एनआरएलएम / आनंदधारा (राज्य ग्रामीण आजीविका मिशन)",
                "tagline_en": "Mobilizing rural women into Self-Help Groups with revolving funds, community investment, and livelihood support",
                "tagline_bn": "গ্রামীণ মহিলাদের স্বনির্ভর গোষ্ঠীতে অন্তর্ভুক্তি, রিভলভিং ফান্ড ও বহুমুখী জীবিকা সহায়তা",
                "tagline_hi": "ग्रामीण निर्धन महिलाओं को SHG से जोड़कर रिवाल्विंग फंड व आजीविका प्रोत्साहन",
                "description_en": "Deen Dayal Upadhyaya National Rural Livelihoods Mission (DAY-NRLM / Anandadhara) organizes poor rural women into affinity-based Self-Help Groups, providing Revolving Funds (RF), Community Investment Funds (CIF), and livelihood support.",
                "description_bn": "আনন্দধারা (DAY-NRLM) প্রকল্পের মাধ্যমে পশ্চিমবঙ্গের গ্রামীণ দরিদ্র পরিবারের মহিলাদের স্বনির্ভর দল (SHG)-এ একত্রিত করে রিভলভিং ফান্ড (RF), ভিলেজ অর্গানাইজেশন সিআইএফ ফান্ড এবং বিকল্প জীবিকার প্রশিক্ষণ প্রদান করা হয়।",
                "description_hi": "DAY-NRLM (पश्चिम बंगाल में 'आनंदधारा') के तहत ग्रामीण महिलाओं को स्वयं सहायता समूहों में संगठित कर रिवॉल्विंग फंड, सामुदायिक निवेश फंड (CIF) और आजीविका सहायता दी जाती है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "₹15,000 Revolving Fund + ₹1.5 Lakh CIF per SHG + Sustainable Livelihood Support",
                "benefit_amount_text_bn": "প্রতি দলে ₹১৫,০০০ রিভলভিং ফান্ড + ₹১.৫ লক্ষ সিআইএফ অনুদান + জীবিকা সহায়তা",
                "application_channels": ["Gram Panchayat Office", "BDO Office (Anandadhara Cell)", "Sangha Co-operative / VO Desk", "Duare Sarkar Camp"],
                "official_portal_url": "https://wbprd.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=day_nrlm_sc,
            defaults={
                "min_age": 18,
                "max_age": 65,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Rural women belonging to poor and vulnerable households identified via the Participatory Identification of the Poor (PIP) process. One female member per identified household is brought into an affinity-based Self-Help Group (10–20 women). Special priority given to manual scavengers, bonded labourers, PVTGs, and single-women households.",
                "rules_summary_bn": "অংশগ্রহণমূলক দারিদ্র্য চিহ্নিতকরণ (PIP) প্রক্রিয়ার মাধ্যমে নির্বাচিত গ্রামীণ দরিদ্র পরিবারের মহিলারা। প্রতি পরিবার থেকে একজন মহিলা সদস্য ১০-২০ জনের স্বনির্ভর দলে অন্তর্ভুক্ত হবেন।"
            }
        )
        set_docs(day_nrlm_sc, [
            ("Aadhaar Card and Voter ID of Applicant", "আবেদনকারীর আধার কার্ড ও ভোটার কার্ড", True, "Aadhaar card and Voter ID of the applicant"),
            ("Proof of Residence in Gram Panchayat", "গ্রাম পঞ্চায়েতে বসবাসের প্রমাণপত্র", True, "Proof of residence in the Gram Panchayat"),
            ("BPL Ration Card / PIP Survey Confirmation", "বিপিএল রেশন কার্ড বা পিআইপি তালিকাভুক্তির প্রমাণ", True, "BPL Ration Card / PIP survey confirmation"),
            ("Bank Savings Account Passbook", "ব্যাংক সেভিংস অ্যাকাউন্ট পাসবুক", True, "Bank savings account passbook"),
            ("Passport-Size Photograph", "পাসপোর্ট সাইজ ছবি", True, "Passport-size photograph")
        ])

        # -------------------------------------------------------------
        # Scheme 44: E-Shram Card (NDUW)
        # -------------------------------------------------------------
        eshram_sc, _ = Scheme.objects.update_or_create(
            slug="e-shram-card",
            defaults={
                "department": mole,
                "category": "social_security",
                "name_en": "E-Shram Card (NDUW)",
                "name_bn": "ই-শ্রম কার্ড (জাতীয় অসংগঠিত শ্রমিক ডেটাবেস)",
                "name_hi": "ई-श्रम कार्ड (राष्ट्रीय असंगठित कर्मकार डेटाबेस)",
                "tagline_en": "12-digit Universal Account Number (UAN) with ₹2 Lakh accidental insurance and national welfare access",
                "tagline_bn": "১২ সংখ্যার ইউনিভার্সাল অ্যাকাউন্ট নম্বর (UAN), ২ লক্ষ টাকার দুর্ঘটনা বীমা ও সামাজিক সুরক্ষা",
                "tagline_hi": "12 अंकों का यूनिवर्सल अकाउंट नंबर (UAN) व ₹2 लाख का मुफ्त दुर्घटना बीमा",
                "description_en": "E-Shram Card is issued by the Ministry of Labour & Employment under the National Database of Unorganized Workers (NDUW). It provides a 12-digit UAN number, ₹2,00,000 accidental death/permanent disability cover under PMSBY, and seamless access to central/state welfare schemes.",
                "description_bn": "ই-শ্রম প্রকল্পের মাধ্যমে ভারতের সমস্ত অসংগঠিত শ্রমিকদের (নির্মাণ কর্মী, পরিযায়ী শ্রমিক, গৃহকর্মী, গিগ কর্মী ইত্যাদি) একটি জাতীয় ১২ সংখ্যার UAN কার্ড দেওয়া হয়, যার সাথে ২ লক্ষ টাকার দুর্ঘটনা বীমা এবং নানা সামাজিক সহায়তা যুক্ত।",
                "description_hi": "ई-श्रम कार्ड असंगठित क्षेत्र के सभी कामगारों (मजदूर, रेहड़ी-पटरी, गिग वर्कर्स आदि) को 12 अंकों का UAN नंबर, ₹2 लाख तक का दुर्घटना बीमा और सामाजिक सुरक्षा योजनाओं का सीधा लाभ प्रदान करता है।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "12-Digit UAN Card + ₹2,00,000 Accidental Death / Permanent Disability Cover",
                "benefit_amount_text_bn": "১২ সংখ্যার UAN কার্ড + ২ লক্ষ টাকার দুর্ঘটনা বীমা + জাতীয় কল্যাণ প্রকল্প সুবিধা",
                "application_channels": ["Self Registration Portal (eshram.gov.in)", "Common Service Centres (CSC)", "Duare Sarkar Camps", "Post Office / Seva Kendra"],
                "official_portal_url": "https://eshram.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=eshram_sc,
            defaults={
                "min_age": 16,
                "max_age": 59,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Unorganized worker (agricultural labourer, gig worker, construction worker, domestic help, rickshaw driver, etc.). Age: Between 16 and 59 years. Must not be an active member of EPFO, ESIC, or NPS (government-sponsored). Must not be an income tax assessee.",
                "rules_summary_bn": "১৬ থেকে ৫৯ বছর বয়সী অসংগঠিত ক্ষেত্রের শ্রমিক। EPFO, ESIC বা সরকারি এনপিএস-এর সক্রিয় সদস্য হওয়া চলবে না এবং আয়করদাতা হওয়া চলবে না।"
            }
        )
        set_docs(eshram_sc, [
            ("Aadhaar Card (Mandatory with Mobile Linked)", "মোবাইল লিঙ্কড আধার কার্ড", True, "Aadhaar card (mandatory with mobile number linked for OTP/e-KYC)"),
            ("Active Aadhaar-Seeded Bank Account Passbook", "আধার সিডেড সক্রিয় ব্যাঙ্ক অ্যাকাউন্ট", True, "Active Aadhaar-seeded bank account number with IFSC code"),
            ("Occupational / Trade Details", "পেশা ও কাজের বিবরণ", True, "Occupational/trade details"),
            ("Nominee Details", "নমিনির বিবরণ", True, "Nominee details")
        ])

        # -------------------------------------------------------------
        # Scheme 45: Job Cards under VB-G RAM-G Scheme / MGNREGS
        # -------------------------------------------------------------
        mgnregs_sc, _ = Scheme.objects.update_or_create(
            slug="job-cards-mgnregs",
            defaults={
                "department": prd,
                "category": "social_security",
                "name_en": "Job Cards under VB-G RAM-G Scheme / MGNREGS",
                "name_bn": "১০০ দিনের কাজের জব কার্ড (VB-G RAM-G / MGNREGS)",
                "name_hi": "जॉब कार्ड योजना (VB-G RAM-G / मनरेगा MGNREGS)",
                "tagline_en": "Statutory 100 to 125 days wage employment guarantee for rural adult household members",
                "tagline_bn": "গ্রামীণ পরিবারের জন্য ১০০-১২৫ দিনের নিশ্চিত কর্মসংস্থান এবং সংবিধিবদ্ধ দৈনিক মজুরি",
                "tagline_hi": "प्रत्येक ग्रामीण परिवार को 100 से 125 दिनों का गारंटीकृत वैधानिक अकुशल रोजगार",
                "description_en": "Job Cards under VB-G RAM-G / MGNREGS provide rural households with a statutory legal guarantee of 100 to 125 days of unskilled wage employment per financial year at statutory wages disbursed directly to bank accounts.",
                "description_bn": "মহাত্মা গান্ধী জাতীয় গ্রামীণ কর্মসংস্থান নিশ্চয়তা প্রকল্প ও ভিবি-জি রাম-জি কাঠামোর অধীনে প্রতিটি গ্রামীণ প্রাপ্তবয়স্ক আবেদনকারী পরিবারকে ১০০ থেকে ১২৫ দিনের কাজের অধিকার ও জব কার্ড প্রদান করা হয়।",
                "description_hi": "मनरेगा (MGNREGS) और VB-G RAM-G योजना के तहत ग्रामीण वयस्क परिवारों को प्रति वित्तीय वर्ष 100 से 125 दिनों के वैधानिक अकुशल शारीरिक रोजगार की कानूनी गारंटी दी जाती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "100-125 Days Guaranteed Work per Year at Statutory Daily Wages (Direct Bank DBT)",
                "benefit_amount_text_bn": "বছরে ১০০-১২৫ দিনের নিশ্চিত কাজ ও সরাসরি ব্যাঙ্ক অ্যাকাউন্টে দৈনিক মজুরি",
                "application_channels": ["Gram Panchayat Office (Gram Rozgar Sahayak)", "BDO Office", "Duare Sarkar Camp", "NREGA Portal"],
                "official_portal_url": "https://nrega.nic.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=mgnregs_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Adult members of rural households (aged 18 years and above) residing within the Gram Panchayat area. Must be willing to perform unskilled manual labour. Family must apply as a household unit to receive statutory work guarantees (100–125 days).",
                "rules_summary_bn": "গ্রাম পঞ্চায়েত এলাকার স্থায়ী বাসিন্দা ১৮ বছর বা তার বেশি বয়সী প্রাপ্তবয়স্ক গ্রামীণ নাগরিক, যারা অদক্ষ কায়িক শ্রম করতে ইচ্ছুক। পরিবার হিসেবে যৌথ জব কার্ড ইস্যু করা হয়।"
            }
        )
        set_docs(mgnregs_sc, [
            ("Aadhaar Cards of All Adult Members", "পরিবারের সকল প্রাপ্তবয়স্ক সদস্যের আধার কার্ড", True, "Aadhaar cards of all adult household members applying for work"),
            ("Proof of Residence in Gram Panchayat", "গ্রাম পঞ্চায়েতে বসবাসের প্রমাণপত্র", True, "Proof of residence within the Gram Panchayat jurisdiction (Voter ID, Ration Card)"),
            ("Aadhaar-Seeded Bank / Post Office Passbook", "আধার সিডেড ব্যাঙ্ক বা পোস্ট অফিস পাসবুক", True, "Individual/joint Aadhaar-seeded bank/post office passbook details"),
            ("Passport-Size Photos of All Applicants", "সকল প্রাপ্তবয়স্ক সদস্যের পাসপোর্ট ছবি", True, "Passport-size photos of all adult applicants")
        ])

        # -------------------------------------------------------------
        # Scheme 46: Kisan Credit Card (KCC)
        # -------------------------------------------------------------
        kcc_sc, _ = Scheme.objects.update_or_create(
            slug="kisan-credit-card",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Kisan Credit Card (KCC)",
                "name_bn": "কিসান ক্রেডিট কার্ড (KCC)",
                "name_hi": "किसान क्रेडिट कार्ड (KCC)",
                "tagline_en": "Concessional institutional crop and working capital credit up to ₹3 Lakh at 4% interest rate",
                "tagline_bn": "কৃষক ও ভাগচাষীদের জন্য ৪% কার্যকরী সুদে ৩ লক্ষ টাকা পর্যন্ত সহজ কৃষি ঋণ",
                "tagline_hi": "किसानों व बटाईदारों को 4% प्रभावी ब्याज पर ₹3 लाख तक का आसान कृषि बैंक लोन",
                "description_en": "Kisan Credit Card (KCC) scheme provides cost-effective and timely institutional credit to farmers, tenant cultivators, and sharecroppers for agricultural production, post-harvest expenses, animal husbandry, and fisheries at 4% effective interest.",
                "description_bn": "কিসান ক্রেডিট কার্ড (KCC) প্রকল্পের মাধ্যমে কৃষক, বর্গাদার ও মৎস্যজীবীদের চাষের খরচ, সার-বীজ ক্রয় এবং পশুপালনের জন্য ৩ লক্ষ টাকা পর্যন্ত মাত্র ৪% কার্যকর বার্ষিক সুদে প্রাতিষ্ঠানিক ব্যাঙ্ক ঋণ দেওয়া হয়।",
                "description_hi": "किसान क्रेडिट कार्ड (KCC) किसानों, पट्टेदारों और पशुपालकों को बीज, खाद व खेती की जरूरतों के लिए ₹3 लाख तक का बैंक ऋण मात्र 4% रियायती ब्याज दर पर प्रदान करता है।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Up to ₹3,00,000 Revolving Credit at 4% Effective Interest (with 3% Prompt Repayment Subvention)",
                "benefit_amount_text_bn": "মাত্র ৪% কার্যকর সুদে ৩,০০,০০০ টাকা পর্যন্ত ফসল ঋণ সুবিধা",
                "application_channels": ["Commercial Bank / Regional Rural Bank / Cooperative Bank", "Duare Sarkar Camps", "Krishi Vigyan Kendra", "Agriculture Department Field Office"],
                "official_portal_url": "https://agricoop.nic.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=kcc_sc,
            defaults={
                "min_age": 18,
                "max_age": 75,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "Individual or joint owner-cultivators owning agricultural land, tenant farmers, oral lessees, and sharecroppers cultivating leased land. SHGs or Joint Liability Groups (JLGs) of farmers, including animal husbandry and fisheries practitioners. Age: 18 to 75 years (borrowers over 60 require a major co-borrower/legal heir).",
                "rules_summary_bn": "কৃষিজমির মালিক, বর্গাদার, ভাগচাষী, মৎস্যচাষী বা পশুপালক (১৮ থেকে ৭৫ বছর বয়সী)। ৬০ বছরের বেশি বয়সীদের ক্ষেত্রে একজন প্রাপ্তবয়স্ক সহ-আবেদনকারী প্রয়োজন।"
            }
        )
        set_docs(kcc_sc, [
            ("Duly Filled KCC Application Form", "যথাযথ পূরণকৃত কেসিসি আবেদন ফর্ম", True, "Duly filled KCC application form"),
            ("Identity and Address Proof (Aadhaar / Voter ID / PAN)", "পরিচয় ও ঠিকানার প্রমাণপত্র", True, "Identity and address proof: Aadhaar card, Voter ID, or PAN card"),
            ("Land Title and Record Documents (RoR / Khatian / Porcha)", "জমির পরচা ও খতিয়ান রেকর্ড (RoR/Porcha)", True, "Land title and record documents: RoR / Khatian / Porcha / 7/12 extract showing cultivable holding"),
            ("Crop Cultivation Proof / Tenancy Agreement", "ফসল চাষ বা ভাগচাষের চুক্তিপত্র", True, "Crop cultivation proof / tenancy agreement (for sharecroppers/tenants)"),
            ("Bank No-Dues Certificate / Non-Encumbrance Declaration", "ব্যাঙ্কের নো-ডিউস বা দায়মুক্তির ঘোষণাপত্র", True, "Bank-approved 'No Dues' certificate / declaration of non-encumbrance from nearby credit institutions")
        ])

        # -------------------------------------------------------------
        # Scheme 47: Mission for Integrated Development of Horticulture (MIDH)
        # -------------------------------------------------------------
        midh_sc, _ = Scheme.objects.update_or_create(
            slug="midh-horticulture",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Mission for Integrated Development of Horticulture (MIDH)",
                "name_bn": "সমন্বিত উদ্যানপালন বিকাশ মিশন (MIDH)",
                "name_hi": "एकीकृत बागवानी विकास मिशन (MIDH)",
                "tagline_en": "Up to 50% capital subsidy for polyhouses, cold chain storages, high-density orchards, and nurseries",
                "tagline_bn": "পলিহাউস, ফল-সবজি বাগান, কোল্ড স্টোরেজ ও মাশরুম চাষে ৫০% পর্যন্ত সরকারি অনুদান",
                "tagline_hi": "पॉलीहाउस, कोल्ड स्टोरेज, फल-फूल की बागवानी व आधुनिक नर्सरी हेतु 50% तक पूंजीगत सब्सिडी",
                "description_en": "Mission for Integrated Development of Horticulture (MIDH) is a Centrally Sponsored Scheme promoting holistic growth of the horticulture sector including fruits, vegetables, root crops, spices, flowers, polyhouse protected cultivation, and post-harvest management.",
                "description_bn": "সমন্বিত উদ্যানপালন বিকাশ মিশন (MIDH) ফল, ফুল, শাকসবজি, মশলা এবং পলিহাউস ও শেডনেট চাষের জন্য ৩৫% থেকে ৫০% পর্যন্ত আর্থিক ভরতুকি ও প্রযুক্তিগত সহায়তা প্রদান করে।",
                "description_hi": "एकीकृत बागवानी विकास मिशन (MIDH) फलों, सब्जियों, फूलों, मसालों, पॉलीहाउस संरक्षित खेती और कोल्ड चेन के निर्माण हेतु 35% से 50% तक की भारी पूंजीगत सब्सिडी उपलब्ध कराता है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "35% to 50% Direct Capital Investment Subsidy on Infrastructure Cost",
                "benefit_amount_text_bn": "পরিকাঠামো তৈরিতে ৩৫% থেকে ৫০% সরাসরি মূলধনী ভরতুকি",
                "application_channels": ["District Horticulture Office / DOH", "State Horticulture Mission Portal", "Duare Sarkar Camps", "NABARD"],
                "official_portal_url": "https://midh.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=midh_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "Individual farmers, small and marginal growers, FPOs, registered cooperatives, SHGs, and agribusiness entrepreneurs. Must own or hold registered long-term leasehold land suitable for horticultural crops (fruits, vegetables, spices, flowers, polyhouse cultivation, or nursery production).",
                "rules_summary_bn": "ব্যক্তিগত কৃষক, ক্ষুদ্র ও প্রান্তিক চাষী, এফপিও, নিবন্ধিত সমবায় সমিতি ও স্বনির্ভর দল যাদের নিজস্ব বা নিবন্ধিত লিজকৃত উপযুক্ত উদ্যানপালন জমি রয়েছে।"
            }
        )
        set_docs(midh_sc, [
            ("Land Record Documents (RoR / Registered Lease Deed)", "জমির খতিয়ান বা নিবন্ধিত লিজ দলিল", True, "Land record documents (RoR / Khatian / registered lease deed)"),
            ("Aadhaar Card and PAN Card", "আধার কার্ড ও প্যান কার্ড", True, "Aadhaar card and PAN card"),
            ("Detailed Project Report (DPR) / Technical Blueprint", "বিস্তারিত প্রকল্প রিপোর্ট (DPR) ও ব্লুপ্রিন্ট", True, "Detailed Project Report (DPR) / Technical blueprint (for cold rooms, polyhouses, protected shade nets)"),
            ("Cost Estimation / Invoice Quotations", "খরচের প্রাক্কলন ও অনুমোদিত বিক্রেতার কোটেশন", True, "Cost estimation/invoice quotations from approved empanelled vendors"),
            ("Bank Account Details & Credit Sanction Letter", "ব্যাংক বিবরণ ও ঋণ মঞ্জুরি পত্র", True, "Bank account details and credit sanction letter (for bank-appraised credit-linked capital subsidies)")
        ])

        # -------------------------------------------------------------
        # Scheme 48: Minor Correction of Land Records (West Bengal - Banglarbhumi)
        # -------------------------------------------------------------
        minor_corr_sc, _ = Scheme.objects.update_or_create(
            slug="minor-correction-land-records",
            defaults={
                "department": land,
                "category": "agriculture",
                "name_en": "Minor Correction of Land Records (West Bengal - Banglarbhumi)",
                "name_bn": "জমির রেকর্ডের ছোটখাটো সংশোধন (বাংলারভূমি)",
                "name_hi": "भू-अभिलेखों का लघु संशोधन (पश्चिम बंगाल - बांगलारभूमि)",
                "tagline_en": "Online rectification of clerical, spelling, and share errors in computerized RoR (Khatian/Porcha)",
                "tagline_bn": "কম্পিউটারাইজড খতিয়ান বা পরচায় নাম, বানান ও অংশের করণিক ভুল সংশোধন",
                "tagline_hi": "कंप्यूटरीकृत खतियान/पर्चे में नाम, वर्तनी या अंश की लिपिकीय त्रुटियों का त्वरित सुधार",
                "description_en": "Minor Correction of Land Records under Banglarbhumi allows recorded raiyats or their legal heirs to correct clerical, spelling, typography, or typographical area/share errors in their computerized Record of Rights (CLR/Khatian/Parcha).",
                "description_bn": "বাংলারভূমি পোর্টালে জমির রেকর্ডে (খতিয়ান/পর্চা) নাম বা বাবার নামের বানান ভুল, অংশ বা দাগের টাইপোগ্রাফিক্যাল করণিক ত্রুটি দ্রুত সংশোধনের আইনি নাগরিক পরিষেবা।",
                "description_hi": "बांगलारभूमि पोर्टल के माध्यम से खतियान/पर्चे में नाम की वर्तनी, पिता के नाम अथवा हिस्से की लिपिकीय गलतियों को आधिकारिक रूप से सुधारने की कानूनी प्रक्रिया।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Updated & Error-Free Computerized Record of Rights (Digitally Corrected Khatian/Porcha)",
                "benefit_amount_text_bn": "সংশোধিত ডিজিটাল খতিয়ান ও পর্চা প্রদান",
                "application_channels": ["Banglarbhumi Portal (banglarbhumi.gov.in)", "Office of the BL&LRO", "Duare Sarkar Camps", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://banglarbhumi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=minor_corr_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "Recorded raiyat (landholder) or their legitimate legal heirs possessing registered legal title. Applies to clerical, spelling, typography, or typographical area/share errors in the current computerized Record of Rights (CLR/Khatian/Parcha).",
                "rules_summary_bn": "রেকর্ডকৃত রায়ত বা তাদের বৈধ উত্তরাধিকারী। বর্তমান কম্পিউটারাইজড রেকর্ড অফ রাইটস (খতিয়ান/পর্চা)-তে নাম, বানান, অংশ বা ক্ষেত্রফলের করণিক ত্রুটি সংশোধনের জন্য প্রযোজ্য।"
            }
        )
        set_docs(minor_corr_sc, [
            ("Certified Copy of Current Khatian / RoR", "বর্তমান ভুল খতিয়ান / পরচার সার্টিফাইড কপি", True, "Certified copy of current Khatian / Record of Rights (RoR) displaying the clerical error"),
            ("Original and Chain Deeds", "মূল দলিলের কপি ও বায়া দলিল", True, "Original and chain deeds: Registered Sale Deed, Gift Deed, or Partition Deed establishing the correct names/shares"),
            ("Notarized Legal Affidavit", "নোটারি পাবলিক স্বাক্ষরিত হলফনামা", True, "Notarized legal affidavit sworn before a Magistrate/Notary Public detailing the discrepancy"),
            ("Aadhaar Card / Voter ID of Recorded Owner", "মালিকের আধার কার্ড বা ভোটার কার্ড", True, "Aadhaar Card / Voter ID of the recorded owner (for identity verification)"),
            ("Up-to-Date Land Revenue (Khajna) Payment Receipt", "হালনাগাদ জমির খাজনা রসিদ", True, "Up-to-date Land Revenue (Khajna) payment receipt")
        ])

        # -------------------------------------------------------------
        # Scheme 49: Mutation of Land Records (West Bengal - Banglarbhumi)
        # -------------------------------------------------------------
        mutation_sc, _ = Scheme.objects.update_or_create(
            slug="mutation-land-records",
            defaults={
                "department": land,
                "category": "agriculture",
                "name_en": "Mutation of Land Records (West Bengal - Banglarbhumi)",
                "name_bn": "জমির মিউটেশন ও খতিয়ান তৈরি (বাংলারভূমি)",
                "name_hi": "जमीन म्यूटेशन / नामांतरण (पश्चिम बंगाल - बांगलारभूमि)",
                "tagline_en": "Legal recording of title transfer in computerized Record of Rights under Section 50 of WBLR Act",
                "tagline_bn": "পশ্চিমবঙ্গ ভূমি সংস্কার আইন অনুযায়ী জমির মালিকানা স্থানান্তর ও পৃথক ডিজিটাল খতিয়ান প্রাপ্তি",
                "tagline_hi": "पश्चिम बंगाल भूमि सुधार अधिनियम की धारा 50 के अंतर्गत जमीन का आधिकारिक नामांतरण",
                "description_en": "Mutation of Land Records legally establishes and records ownership transfer through registered purchase, gift, exchange, or inheritance under Section 50 of the West Bengal Land Reforms Act, issuing an independent digital Khatian.",
                "description_bn": "পশ্চিমবঙ্গ ভূমি সংস্কার আইনের ৫০ নম্বর ধারা অনুযায়ী ক্রয়, দানপত্র বা উত্তরাধিকার সূত্রে প্রাপ্ত জমির আইনি মালিকানা স্থানান্তর ও রাজস্ব রেকর্ডে নতুন খতিয়ান ভুক্ত করার সার্বিক পরিষেবা।",
                "description_hi": "पश्चिम बंगाल भूमि सुधार अधिनियम के तहत क्रय, उपहार या पैतृक उत्तराधिकार द्वारा प्राप्त जमीन का स्वामित्व राजस्व रिकॉर्ड में दर्ज कराने व नया खतियान प्राप्त करने की प्रक्रिया।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Digitally Signed Mutation Certificate & New Computerized Khatian",
                "benefit_amount_text_bn": "ডিজিটালি স্বাক্ষরিত মিউটেশন শংসাপত্র ও নিজস্ব কম্পিউটারাইজড খতিয়ান",
                "application_channels": ["Banglarbhumi Online Portal", "Office of the BL&LRO", "Duare Sarkar Camps", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://banglarbhumi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=mutation_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "rules_summary_en": "Any person who has acquired legal ownership of land through registered purchase, gift, exchange, court decree, or ancestral inheritance (succession) under Section 50 of the West Bengal Land Reforms Act. The seller/predecessor must hold a valid chain of title without unrecorded intervening encumbrances.",
                "rules_summary_bn": "যে কোনো ব্যক্তি যিনি রেজিস্টার্ড ক্রয়, দানপত্র, বিনিময়, আদালতের ডিক্রি বা পৈতৃক উত্তরাধিকার সূত্রে জমির বৈধ মালিকানা অর্জন করেছেন। বিক্রেতার বৈধ স্বত্ব থাকতে হবে।"
            }
        )
        set_docs(mutation_sc, [
            ("Registered Deed of Transfer", "রেজিস্টার্ড দলিল (ক্রয়/হেবানামা/দানপত্র)", True, "Registered deed of transfer (Sale Deed, Gift Deed, Exchange Deed)"),
            ("Legal Heir Certificate & Death Certificate", "ওয়ারিশন সার্টিফিকেট ও মৃত্যু শংসাপত্র", False, "For inheritance cases: Death Certificate and Legal Heir Certificate (issued by SDO/BDO/Court)"),
            ("Previous Recorded Khatian / Porcha of Transferor", "বিক্রেতা বা পূর্বসূরীর পূর্ববর্তী রেকর্ডকৃত খতিয়ান/পর্চা", True, "Previous recorded Khatian/Parcha of the transferor"),
            ("Up-to-Date Land Tax (Khajna) / Property Clearance Receipt", "আপ-টু-ডেট জমির খাজনা বা পুরসভার ট্যাক্স রসিদ", True, "Up-to-date Land Tax (Khajna) / municipal property tax clearance receipt"),
            ("Aadhaar Card and PAN Card of Buyer & Seller", "ক্রেতা-বিক্রেতার আধার ও প্যান কার্ড", True, "Aadhaar card and PAN card of the buyer and seller/donor"),
            ("Boundary Sketch Map & Land Ceiling Affidavit", "সীমানা নকশা ও সিলিং ঘোষণাপত্র", True, "Boundary sketch map and self-declaration affidavit regarding land ceilings")
        ])

        # -------------------------------------------------------------
        # Scheme 50: National Apprenticeship Promotion Scheme (NAPS)
        # -------------------------------------------------------------
        naps_sc, _ = Scheme.objects.update_or_create(
            slug="national-apprenticeship-promotion-scheme",
            defaults={
                "department": msde,
                "category": "youth",
                "name_en": "National Apprenticeship Promotion Scheme (NAPS)",
                "name_bn": "জাতীয় শিক্ষানবিশি প্রচার যোজনা (NAPS)",
                "name_hi": "राष्ट्रीय शिक्षुता संवर्धन योजना (NAPS)",
                "tagline_en": "Industry apprenticeship with 25% stipend support (up to ₹1,500/month) directly via DBT",
                "tagline_bn": "শিল্প প্রতিষ্ঠানে হাতে-কলমে শিক্ষানবিশি প্রশিক্ষণ এবং প্রতি মাসে সরাসরি সরকারি স্টাইপেন্ড",
                "tagline_hi": "उद्योगों में ऑन-द-जॉब अप्रेंटिसशिप प्रशिक्षण व ₹1,500 प्रति माह तक प्रत्यक्ष डीबीटी वजीफा",
                "description_en": "National Apprenticeship Promotion Scheme (NAPS) promotes apprenticeship training across establishments by reimbursing up to 25% of stipend (up to ₹1,500 per month) directly to trainees via DBT, awarding National Apprenticeship Certificates upon completion.",
                "description_bn": "জাতীয় শিক্ষানবিশি প্রচার যোজনা (NAPS) যুবক-যুবতীদের বিভিন্ন শিল্প প্রতিষ্ঠানে কাজ শেখার সুযোগ দেয়, যেখানে সরকার সরাসরি প্রার্থীর অ্যাকাউন্টে ২৫% পর্যন্ত (সর্বোচ্চ ₹১,৫০০/মাস) স্টাইপেন্ড প্রদান করে।",
                "description_hi": "राष्ट्रीय शिक्षुता संवर्धन योजना (NAPS) युवाओं को कंपनियों में व्यावहारिक अप्रेंटिसशिप प्रशिक्षण प्रदान करती है जिसमें सरकार वजीफे का 25% (अधिकतम ₹1,500/माह) सीधे प्रशिक्षु के खाते में DBT करती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "Government Direct Stipend Support (25% up to ₹1,500/month DBT) + Industry Certification",
                "benefit_amount_text_bn": "সরকারি স্টাইপেন্ড (২৫% সর্বোচ্চ ₹১,৫০০/মাস ডিবিটি) + জাতীয় শিক্ষানবিশি শংসাপত্র",
                "application_channels": ["Apprenticeship India Portal (apprenticeshipindia.gov.in)", "District Skill Development Office", "ITIs & Vocational Institutes", "Duare Sarkar Camps"],
                "official_portal_url": "https://www.apprenticeshipindia.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=naps_sc,
            defaults={
                "min_age": 14,
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Trainee must have completed at least 14 years of age (18 years for designated hazardous industries). Educational qualification: Class 5, 8, 10, or 12 pass, or ITI certificate holder (depending on the designated or optional trade). Must be registered on the Apprenticeship India Portal (apprenticeshipindia.gov.in).",
                "rules_summary_bn": "প্রার্থীর বয়স ন্যূনতম ১৪ বছর হতে হবে (বিপজ্জনক শিল্পের জন্য ১৮ বছর)। শিক্ষাগত যোগ্যতা: ৫ম, ৮ম, ১০ম, ১২শ শ্রেণি উত্তীর্ণ অথবা আইটিআই (ITI) পাস। পোর্টাল রেজিস্ট্রেশন বাধ্যতামূলক।"
            }
        )
        set_docs(naps_sc, [
            ("Aadhaar Card (Mandatory for e-KYC)", "আধার কার্ড (ই-কেওয়াইসির জন্য বাধ্যতামূলক)", True, "Aadhaar card (mandatory for e-KYC)"),
            ("Educational Qualification Marksheets / ITI NTC", "শিক্ষাগত যোগ্যতার মার্কশিট বা আইটিআই এনটিসি", True, "Educational qualification mark sheets / ITI National Trade Certificate (NTC)"),
            ("Aadhaar-Seeded Bank Passbook / Cancelled Cheque", "আধার সিডেড ব্যাঙ্ক পাসবুক বা বাতিল চেক", True, "Aadhaar-seeded bank account passbook / cancelled cheque (for direct DBT stipend sharing)"),
            ("Passport-Size Photograph", "পাসপোর্ট সাইজ ছবি", True, "Passport-size photograph")
        ])

        # -------------------------------------------------------------
        # Scheme 51: National Apprenticeship Training Scheme (NATS)
        # -------------------------------------------------------------
        nats_sc, _ = Scheme.objects.update_or_create(
            slug="national-apprenticeship-training-scheme",
            defaults={
                "department": moe,
                "category": "youth",
                "name_en": "National Apprenticeship Training Scheme (NATS)",
                "name_bn": "জাতীয় শিক্ষানবিশি প্রশিক্ষণ যোজনা (NATS 2.0)",
                "name_hi": "राष्ट्रीय शिक्षुता प्रशिक्षण योजना (NATS 2.0)",
                "tagline_en": "1-year practical on-the-job training with government stipend for Engineering, Diploma, and Degree graduates",
                "tagline_bn": "গ্র্যাজুয়েট ও ডিপ্লোমাধারীদের জন্য ১ বছরের অর্থসহ বাস্তব শিল্প প্রশিক্ষণ ও স্টাইপেন্ড",
                "tagline_hi": "डिप्लोमा और ग्रेजुएट युवाओं के लिए 1 वर्षीय सवैतनिक व्यावहारिक औद्योगिक प्रशिक्षण",
                "description_en": "National Apprenticeship Training Scheme (NATS 2.0) is a flagship 1-year practical training program by the Ministry of Education for Degree and Diploma holders in Engineering, Technology, and General streams (BA, BSc, BCom, BBA, BCA) with direct central monthly stipend support.",
                "description_bn": "শিক্ষা মন্ত্রকের অধীনে NATS 2.0 প্রকল্প ইঞ্জিনিয়ারিং, ডিপ্লোমা এবং সাধারণ স্নাতকদের (BA, BSc, BCom, BCA ইত্যাদি) ভারতের শীর্ষস্থানীয় শিল্প প্রতিষ্ঠানে ১ বছরের জন্য নিশ্চিত স্টাইপেন্ড সহ শিক্ষানবিশি প্রশিক্ষণ প্রদান করে।",
                "description_hi": "NATS 2.0 शिक्षा मंत्रालय का प्रमुख कार्यक्रम है जिसके तहत इंजीनियरिंग, डिप्लोमा व सामान्य स्नातक (BA/BSc/BCom/BCA) युवाओं को कंपनियों में 1 वर्ष का व्यावहारिक प्रशिक्षण व सीधा मासिक वजीफा मिलता है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "Monthly Stipend (₹8,000 to ₹9,000+ / month DBT) + Certificate of Proficiency by Gov of India",
                "benefit_amount_text_bn": "মাসিক স্টাইপেন্ড (₹৮,০০০-₹৯,০০০+/মাস সরাসরি ডিবিটি) + কেন্দ্রীয় সরকারি দক্ষতা শংসাপত্র",
                "application_channels": ["NATS 2.0 Portal (nats.education.gov.in)", "Board of Apprenticeship Training (BOAT Eastern Region)", "College Placement Cell"],
                "official_portal_url": "https://nats.education.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=nats_sc,
            defaults={
                "min_age": 16,
                "max_age": 35,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Citizen of India aged 16 years or above holding a recognized Degree or Diploma in Engineering/Technology or general graduate degree (BA, B.Sc, B.Com, BBA, BCA, etc.) graduated within the last 3 to 5 years. Must not have prior formal work experience or apprenticeship training for 1 year or more.",
                "rules_summary_bn": "১৬ বছর বা তার বেশি বয়সী ভারতীয় নাগরিক যিনি স্বীকৃত বিশ্ববিদ্যালয়/বোর্ড থেকে ইঞ্জিনিয়ারিং, ডিপ্লোমা বা সাধারণ ডিগ্রি (বিএ, বিএসসি, বিকম ইত্যাদি) পাস করেছেন (বিগত ৩-৫ বছরের মধ্যে)। পূর্বে ১ বছর বা তার বেশি কাজের অভিজ্ঞতা থাকা চলবে না।"
            }
        )
        set_docs(nats_sc, [
            ("Degree / Diploma Passing Certificate or Final Marksheet", "ডিগ্রি বা ডিপ্লোমা পাসের সার্টিফিকেট / মার্কশিট", True, "Degree / Diploma passing certificate or consolidated final mark sheet"),
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar card"),
            ("Aadhaar-Linked Active Bank Passbook", "আধার লিঙ্কড সক্রিয় ব্যাঙ্ক পাসবুক", True, "Aadhaar-linked active bank account passbook"),
            ("Institutional Student ID / Bonafide Certificate", "কলেজের স্টুডেন্ট আইডি বা প্রত্যয়ন পত্র", True, "Institutional student ID / Bonafide certificate"),
            ("Active Email Address and Mobile Number", "সক্রিয় ইমেল ও মোবাইল নম্বর", True, "Active email address and mobile number registered on the NATS 2.0 portal")
        ])

        # -------------------------------------------------------------
        # Scheme 52: Patta Application (Settlement of Vested Land - West Bengal)
        # -------------------------------------------------------------
        patta_sc, _ = Scheme.objects.update_or_create(
            slug="patta-application-vested-land",
            defaults={
                "department": land,
                "category": "agriculture",
                "name_en": "Patta Application (Settlement of Vested Land - West Bengal)",
                "name_bn": "পাট্টা আবেদন (সরকার খাস/ভেস্টেড খাসজমির বন্দোবস্ত)",
                "name_hi": "पट्टा आवेदन (सरकारी निहित/वेस्टेड कृषि व आवासीय भूमि बंदोबस्त)",
                "tagline_en": "Permanent legal land rights and Patta deeds for landless rural poor and marginal agricultural families",
                "tagline_bn": "ভূমিহীন গ্রামীণ দরিদ্র, কৃষক ও কারিগরদের জন্য সরকারি ভেস্টেড জমির স্থায়ী অধিকার ও পাট্টা প্রদান",
                "tagline_hi": "भूमिहीन ग्रामीण निर्धन परिवारों व किसानों को सरकारी निहित भूमि का स्थायी कानूनी पट्टा",
                "description_en": "Patta Application allows landless rural poor, agricultural labourers, and village artisans in West Bengal to obtain permanent, heritable settlement of government-vested (khas) land for agricultural or homestead use up to 1 acre free of cost.",
                "description_bn": "পশ্চিমবঙ্গের ভূমি ও ভূমি সংস্কার দপ্তরের মাধ্যমে বাস্তুহীন এবং কৃষিজমিহীন প্রান্তিক দরিদ্র পরিবার, তফসিলি জাতি ও উপজাতিদের সরকারি খাসজমির স্থায়ী মালিকানা ও পাট্টা দলিল প্রদান করা হয়।",
                "description_hi": "पश्चिम बंगाल सरकार द्वारा भूमिहीन ग्रामीण निर्धनों, खेतिहर मजदूरों, अनुसूचित जाति/जनजाति और असहाय परिवारों को कृषि अथवा घर बनाने हेतु सरकारी निहित भूमि का स्थायी पट्टा निःशुल्क दिया जाता है।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Permanent Heritable Land Patta Deed (up to 1 Acre) + Revenue Exemption",
                "benefit_amount_text_bn": "স্থায়ী উত্তরাধিকারযোগ্য পাট্টা দলিল (১ একর পর্যন্ত) + রাজস্ব ছাড়",
                "application_channels": ["Office of the Block Land & Land Reforms Officer (BL&LRO)", "Duare Sarkar Camps", "Gram Panchayat Office", "Banglarbhumi Portal"],
                "official_portal_url": "https://banglarbhumi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=patta_sc,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 100000,
                "rules_summary_en": "Landless rural poor, agricultural labourers, marginal farmers, or village artisans permanently residing in West Bengal. Priority given to Scheduled Castes (SC), Scheduled Tribes (ST), women-headed households, and families lacking any agricultural or homestead land physically occupying or cultivating government-vested land.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা ভূমিহীন গ্রামীণ দরিদ্র, প্রান্তিক চাষী, কৃষি শ্রমিক বা গ্রামীণ কারিগর। এসসি, এসটি ও মহিলা চালিত পরিবার অগ্রাধিকার পাবে। সরকারি খাসজমিতে বাস্তব দখল থাকতে হবে।"
            }
        )
        set_docs(patta_sc, [
            ("Prescribed Patta Application Form (Form 1)", "নির্ধারিত পাট্টা আবেদন ফর্ম (ফর্ম ১)", True, "Prescribed Patta application form (Form 1) submitted to the Block Land & Land Reforms Officer (BL&LRO)"),
            ("Identity Proof (Aadhaar Card and Voter ID)", "আধার কার্ড ও ভোটার কার্ড", True, "Identity proof: Aadhaar card and Voter ID (EPIC)"),
            ("Proof of Permanent Residence and GP Domicile", "স্থায়ী বাসস্থান ও পঞ্চায়েতের ডোমিসাইল প্রমাণ", True, "Proof of permanent residence and local Gram Panchayat domicile"),
            ("Digital Ration Card / BPL Certificate", "ডিজিটাল রেশন কার্ড বা বিপিএল সার্টিফিকেট", True, "Digital Ration Card / BPL certificate"),
            ("Family Income Certificate from BDO / GP Pradhan", "পারিবারিক আয় শংসাপত্র (বিডিও বা প্রধান)", True, "Family income certificate from BDO/Gram Panchayat Pradhan"),
            ("Possession Certificate / RI Verification Report", "জমির বাস্তব দখল শংসাপত্র বা আরআই রিপোর্ট", True, "Possession certificate / verification report from the local Revenue Inspector proving physical possession of the vested plot")
        ])


        # -------------------------------------------------------------
        # Scheme 53: PM Surya Ghar Muft Bijli Yojana
        # -------------------------------------------------------------
        pm_surya, _ = Scheme.objects.update_or_create(
            slug="pm-surya-ghar",
            defaults={
                "department": mnre,
                "category": "social_security",
                "name_en": "PM Surya Ghar: Muft Bijli Yojana",
                "name_bn": "প্রধানমন্ত্রী সূর্য ঘর: বিনামূল্যে বিদ্যুৎ যোজনা",
                "name_hi": "पीएम सूर्य घर: मुफ्त बिजली योजना",
                "tagline_en": "Free rooftop solar electricity up to 300 units/month with up to ₹78,000 central government subsidy",
                "tagline_bn": "ছাদে সৌরবিদ্যুৎ প্যানেল বসিয়ে প্রতি মাসে ৩০০ ইউনিট পর্যন্ত বিনামূল্যে বিদ্যুৎ ও ৭৮,০০০ টাকা পর্যন্ত সরকারি ভর্তুকি",
                "tagline_hi": "छत पर सोलर पैनल लगाकर 300 यूनिट तक मुफ्त बिजली और ₹78,000 तक की केंद्रीय वित्तीय सब्सिडी",
                "description_en": "PM Surya Ghar: Muft Bijli Yojana provides rooftop solar systems for residential households with up to 300 units of free electricity every month and direct financial subsidy (CFA) up to ₹78,000 credited directly to bank accounts.",
                "description_bn": "আবাসিক গৃহস্থালির ছাদে রুফটপ সোলার প্যানেল স্থাপনের মাধ্যমে প্রতি মাসে ৩০০ ইউনিট পর্যন্ত বিনামূল্যে বিদ্যুৎ এবং সরাসরি ব্যাংক অ্যাকাউন্টে ৭৮,০০০ টাকা পর্যন্ত কেন্দ্রীয় সরকারি ভর্তুকি প্রদান করা হয়।",
                "description_hi": "आवासीय घरों की छत पर सौर ऊर्जा संयंत्र स्थापित करने हेतु प्रति माह 300 यूनिट तक मुफ्त बिजली और ₹78,000 तक की सीधी बैंक सब्सिडी।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Up to ₹78,000 Direct Subsidy (CFA) + 300 Units/Month Free Solar Electricity",
                "benefit_amount_text_bn": "৭৮,০০০ টাকা পর্যন্ত সরকারি ভর্তুকি (CFA) + প্রতি মাসে ৩০০ ইউনিট বিনামূল্যে সৌরবিদ্যুৎ",
                "application_channels": ["National Portal for Rooftop Solar (pmsuryaghar.gov.in)", "DISCOM Consumer Portal", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://pmsuryaghar.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_surya,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Must be an Indian citizen and head/member of the household owning a residential property suitable for rooftop solar installation. Must have a valid, active grid-connected domestic electricity connection in their name with the local DISCOM (WBSEDCL/CESC). Must not have availed of any other central/state financial assistance or subsidy for rooftop solar previously.",
                "rules_summary_bn": "ভারতীয় নাগরিক এবং ছাদসহ নিজস্ব আবাসিক বাসগৃহের মালিক। স্থানীয় বিদ্যুৎ বণ্টন কোম্পানির (WBSEDCL/CESC) বৈধ ও সক্রিয় গার্হস্থ্য বিদ্যুৎ সংযোগ আবেদনকারীর নামে থাকতে হবে এবং পূর্বে কোনো কেন্দ্রীয়/রাজ্য সোলার ভর্তুকি নেননি।"
            }
        )
        set_docs(pm_surya, [
            ("Aadhaar Card (Aadhaar-Linked Mobile Verification)", "আধার কার্ড (আধার লিঙ্কযুক্ত মোবাইল যাচাইকরণ)", True, "Aadhaar card with linked mobile number for OTP/biometric verification"),
            ("Latest Domestic Electricity Bill", "সাম্প্রতিক গার্হস্থ্য বিদ্যুৎ বিল", True, "Latest domestic electricity bill issued within the last 90 days"),
            ("Proof of Roof / Property Ownership", "ছাদ বা সম্পত্তির মালিকানার প্রমাণপত্র", True, "Proof of roof/property ownership (registered sale deed, property tax receipt, or municipal assessment)"),
            ("Aadhaar-Seeded Bank Passbook Copy or Cancelled Cheque", "আধার সংযুক্ত ব্যাঙ্ক পাসবই বা বাতিল চেক", True, "Aadhaar-seeded bank account passbook copy or cancelled cheque (for direct CFA release)"),
            ("PAN Card", "প্যান কার্ড", True, "Permanent Account Number (PAN) card of the applicant")
        ])

        # -------------------------------------------------------------
        # Scheme 54: PM SVANidhi (Pradhan Mantri Street Vendor’s AtmaNirbhar Nidhi)
        # -------------------------------------------------------------
        pm_svanidhi, _ = Scheme.objects.update_or_create(
            slug="pm-svanidhi",
            defaults={
                "department": udma,
                "category": "youth",
                "name_en": "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
                "name_bn": "পিএম স্বনিধি (রাস্তার হকারদের আত্মনির্ভর তহবিল)",
                "name_hi": "पीएम स्वनिधि (प्रधानमंत्री स्ट्रीट वेंडर्स आत्मनिर्भर निधि)",
                "tagline_en": "Collateral-free working capital loan up to ₹50,000 with 7% interest subsidy for street vendors and hawkers",
                "tagline_bn": "পথবিক্রেতা ও হকারদের জন্য বন্ধকমুক্ত ₹১০,০০০ থেকে ₹৫০,০০০ পর্যন্ত কার্যকরী মূলধন ঋণ ও ৭% সুদ ভর্তুকি",
                "tagline_hi": "स्ट्रीट वेंडर्स और रेहड़ी-पटरी वालों के लिए ₹50,000 तक का बिना गारंटी कार्यशील पूंजी ऋण और 7% ब्याज सब्सिडी",
                "description_en": "PM SVANidhi empowers urban and peri-urban street vendors with collateral-free micro-credit loans in tranches of ₹10,000, ₹20,000, and ₹50,000, along with a 7% interest subsidy on timely repayment and digital cashback incentives up to ₹1,200/year.",
                "description_bn": "শহরের ও শহরতলির রাস্তার হকার ও ক্ষুদ্র বিক্রেতাদের জামানতমুক্ত ঋণ সুবিধা (প্রথম কিস্তিতে ₹১০,০০০, দ্বিতীয়তে ₹২০,০০০ এবং তৃতীয়তে ₹৫০,০০০), সময়মতো ঋণ পরিশোধে ৭% সুদের ভর্তুকি এবং ডিজিটাল লেনদেনে ক্যাশব্যাক প্রদান করা হয়।",
                "description_hi": "शहरी और अर्ध-शहरी रेहड़ी-पटरी विक्रेताओं के लिए ₹10,000 से ₹50,000 तक का आसान लोन, समय पर भुगतान पर 7% ब्याज छूट और डिजिटल कैशबैक।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Collateral-free working capital loan: ₹10,000 (1st), ₹20,000 (2nd), ₹50,000 (3rd) + 7% interest subsidy + UPI cashback",
                "benefit_amount_text_bn": "জামানতমুক্ত কার্যকরী ঋণ: ₹১০,০০০ (১ম), ₹২০,০০০ (২য়), ₹৫০,০০০ (৩য়) + ৭% সুদ ভর্তুকি + ইউপিআই ক্যাশব্যাক",
                "application_channels": ["PM SVANidhi Portal / Mobile App", "Urban Local Body (ULB) / Municipality Office", "Common Service Centres (CSC)", "Microfinance / Bank Branches"],
                "official_portal_url": "https://pmsvanidhi.mohua.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_svanidhi,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Street vendors, hawkers, and informal service providers operating in urban, peri-urban, or rural surrounding areas. Must be at least 18 years of age. Possessing a Certificate of Vending (CoV), Vendor ID card, or a Letter of Recommendation (LoR) issued by the Town Vending Committee (TVC), Urban Local Body (ULB), or Block Development Officer (BDO).",
                "rules_summary_bn": "শহর ও শহরতলির রাস্তার হকার, ক্ষুদ্র ব্যবসায়ী ও সেবা প্রদানকারী। বয়স ন্যূনতম ১৮ বছর। টাউন ভেন্ডিং কমিটি (TVC), পুরসভা (ULB) বা BDO কর্তৃক প্রদত্ত ভেন্ডিং সার্টিফিকেট (CoV), ভেন্ডর আইডি কার্ড বা সুপারিশপত্র (LoR) থাকতে হবে।"
            }
        )
        set_docs(pm_svanidhi, [
            ("Certificate of Vending (CoV) / Vendor ID Card / Letter of Recommendation (LoR)", "ভেন্ডিং সার্টিফিকেট (CoV) / ভেন্ডর আইডি কার্ড / সুপারিশপত্র (LoR)", True, "Certificate of Vending (CoV), Vendor ID Card, or Letter of Recommendation (LoR) issued by TVC/ULB/BDO"),
            ("Aadhaar Card (or Voter ID for Assam/Meghalaya)", "আধার কার্ড (বা ভোটার কার্ড)", True, "Aadhaar card (or Voter ID for Assam/Meghalaya)"),
            ("Bank Account Passbook / Statement", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই / স্টেটমেন্ট", True, "Active bank account passbook or statement"),
            ("Active Mobile Number Linked to Aadhaar and a UPI Handle", "আধার ও ইউপিআই সংযুক্ত সক্রিয় মোবাইল নম্বর", True, "Active mobile number linked to Aadhaar and a UPI handle")
        ])

        # -------------------------------------------------------------
        # Scheme 55: Post Matric Scholarship Scheme
        # -------------------------------------------------------------
        post_matric, _ = Scheme.objects.update_or_create(
            slug="post-matric-scholarship",
            defaults={
                "department": bcwd,
                "category": "education",
                "name_en": "Post Matric Scholarship Scheme",
                "name_bn": "পোস্ট-ম্যাট্রিক স্কলারশিপ যোজনা (এসসি, এসটি, ওবিসি ও ইডব্লিউএস)",
                "name_hi": "पोस्ट-मैट्रिक स्कॉलरशिप योजना (SC, ST, OBC एवं EWS)",
                "tagline_en": "Centrally sponsored post-matric scholarship for SC, ST, OBC, and EWS students in Class 11, 12, ITI, Diploma, UG, PG, and Ph.D.",
                "tagline_bn": "একাদশ, দ্বাদশ, আইটিআই, ডিপ্লোমা, স্নাতক, স্নাতকোত্তর ও পিএইচডি পড়ুয়া এসসি, এসটি, ওবিসি ও ইডব্লিউএস শিক্ষার্থীদের উচ্চশিক্ষা বৃত্তি",
                "tagline_hi": "11वीं, 12वीं, आईटीआई, डिप्लोमा, यूजी, पीजी व पीएचडी के एससी, एसटी, ओबीसी और ईडब्ल्यूएस छात्रों हेतु पोस्ट-मैट्रिक छात्रवृत्ति",
                "description_en": "Centrally Sponsored Post Matric Scholarship provides financial assistance covering compulsory non-refundable fees and annual maintenance allowances to eligible SC, ST, OBC, and EWS students studying post-secondary courses in recognized institutions.",
                "description_bn": "স্বীকৃত শিক্ষা প্রতিষ্ঠানে একাদশ, দ্বাদশ শ্রেণি, আইটিআই, পলিটেকনিক, ডিপ্লোমা, ডিগ্রি, পোস্ট-গ্র্যাজুয়েট ও পিএইচডি স্তরে অধ্যয়নরত যোগ্য এসসি, এসটি, ওবিসি এবং ইডব্লিউএস শিক্ষার্থীদের টিউশন ফি ও রক্ষণাবেক্ষণ অনুদান প্রদান করা হয়।",
                "description_hi": "मान्यता प्राप्त संस्थानों में 11वीं, 12वीं, आईटीआई, पॉलिटेक्निक, स्नातक, स्नातकोत्तर और पीएचडी में पढ़ रहे एससी, एसटी, ओबीसी और ईडब्ल्यूएस विद्यार्थियों को छात्रवृत्ति।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Full Compulsory Course Fee Reimbursement + Annual Maintenance Allowance (₹2,500 to ₹13,500/yr DBT)",
                "benefit_amount_text_bn": "সম্পূর্ণ কোর্স ফি ফেরত + বার্ষিক রক্ষণাবেক্ষণ ভাতা (২,৫০০ থেকে ১৩,৫০০ টাকা/বছর সরাসরি ডিবিটি)",
                "application_channels": ["National Scholarship Portal (NSP - scholarships.gov.in)", "State Scholarship Portal (OASIS - oasis.gov.in)", "Institutional Nodal Officer"],
                "official_portal_url": "https://scholarships.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=post_matric,
            defaults={
                "min_age": 15,
                "gender_allowed": "all",
                "caste_categories": ["SC", "ST", "OBC-A", "OBC-B", "EWS"],
                "max_family_income": 250000.00,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian students belonging to eligible socio-economic categories (SC, ST, OBC, or EWS). Enrolled in post-secondary/post-matric courses (Class 11, Class 12, ITI, Polytechnic, Diploma, Undergraduate, Postgraduate, or Ph.D.) at recognized government or accredited private institutions. Must have passed the previous qualifying examination without backlogs. Annual family income must not exceed the prescribed threshold (typically up to ₹2.50 lakh for SC/ST and ₹1.50–2.50 lakh for OBC/EWS, depending on specific state guidelines).",
                "rules_summary_bn": "এসসি, এসটি, ওবিসি বা ইডব্লিউএস শ্রেণিভুক্ত ভারতীয় শিক্ষার্থী। স্বীকৃত প্রতিষ্ঠানে পোস্ট-ম্যাট্রিক কোর্সে পাঠরত এবং পূর্ববর্তী পরীক্ষায় ব্যাকলগ ছাড়া উত্তীর্ণ। বার্ষিক পারিবারিক আয় ২.৫০ লক্ষ টাকার মধ্যে হতে হবে।"
            }
        )
        set_docs(post_matric, [
            ("Aadhaar Card of the Applicant", "আবেদনকারীর আধার কার্ড", True, "Aadhaar card of the applicant student"),
            ("Valid Caste / Category Certificate", "বৈধ জাতিগত / ক্যাটাগরি শংসাপত্র", True, "Valid Caste/Category certificate issued by a competent authority"),
            ("Valid Family Income Certificate", "পারিবারিক আয়ের শংসাপত্র", True, "Valid Family Income Certificate (issued by SDO/BDO/Tehsildar)"),
            ("Mark Sheet / Certificate of Last Qualifying Examination", "পূর্ববর্তী উত্তীর্ণ পরীক্ষার মার্কশিট / শংসাপত্র", True, "Mark sheet/certificate of the last qualifying examination passed without backlogs"),
            ("Current Course Admission Fee Receipt & Bonafide Certificate", "কোর্সে ভর্তির ফি রশিদ ও ইনস্টিটিউশনাল বনফাইড শংসাপত্র", True, "Current course admission fee receipt and Bonafide Certificate / Institutional Verification"),
            ("Student’s Active Aadhaar-Seeded Bank Passbook Copy", "শিক্ষার্থীর নিজস্ব আধার-সংযুক্ত ব্যাঙ্ক পাসবই", True, "Student's active Aadhaar-seeded bank passbook copy for DBT disbursement")
        ])

        # -------------------------------------------------------------
        # Scheme 56: Pradhan Mantri Awas Yojana (Urban) – PMAY-U
        # -------------------------------------------------------------
        pmay_u, _ = Scheme.objects.update_or_create(
            slug="pmay-urban",
            defaults={
                "department": udma,
                "category": "social_security",
                "name_en": "Pradhan Mantri Awas Yojana (Urban) – PMAY-U",
                "name_bn": "প্রধানমন্ত্রী আবাস যোজনা (শহরাঞ্চল) – পিএমএওয়াই-ইউ",
                "name_hi": "प्रधानमंत्री आवास योजना (शहरी) – पीएमएवाई-यू",
                "tagline_en": "Pucca housing assistance and interest subsidy up to ₹2.50 Lakh for urban homeless, EWS, and LIG families",
                "tagline_bn": "শহরাঞ্চলের গৃহহীন, ইডব্লিউএস ও এলআইজি পরিবারের জন্য পাকা বাড়ি নির্মাণে ₹২.৫০ লক্ষ পর্যন্ত সরকারি অনুদান",
                "tagline_hi": "शहरी बेघर, ईडब्ल्यूएस और एलआईजी परिवारों के लिए पक्का मकान बनाने हेतु ₹2.50 लाख तक की वित्तीय सहायता",
                "description_en": "Pradhan Mantri Awas Yojana - Urban (PMAY-U / Housing for All) addresses urban housing shortage among EWS, LIG, and MIG families by providing central financial assistance up to ₹2.50 Lakh for Beneficiary-Led Construction, Affordable Housing in Partnership, or Credit Linked Interest Subsidy.",
                "description_bn": "শহরের গৃহহীন এবং কাঁচা বাড়িতে বসবাসকারী আর্থিকভাবে দুর্বল (EWS) ও নিম্ন আয়ের (LIG) পরিবারগুলির পাকা বাড়ি নির্মাণের জন্য সরাসরি আধার-সংযুক্ত ব্যাংক অ্যাকাউন্টে কিস্তিতে অনুদান প্রদান করা হয়।",
                "description_hi": "शहरी क्षेत्र के आर्थिक रूप से कमजोर (EWS) और कम आय वर्ग (LIG) के परिवारों को पक्का मकान बनाने के लिए ₹2.50 लाख तक का अनुदान।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Up to ₹2.50 Lakh Financial Grant / Interest Subsidy up to 6.5% for Pucca House",
                "benefit_amount_text_bn": "পাকা বাড়ি নির্মাণে ₹২.৫০ লক্ষ পর্যন্ত অনুদান / গৃহঋণে ৬.৫% পর্যন্ত সুদ ভর্তুকি",
                "application_channels": ["PMAY Urban Portal (pmaymis.gov.in)", "Urban Local Body (Municipality / Municipal Corporation)", "Common Service Centre (CSC)"],
                "official_portal_url": "https://pmay-urban.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmay_u,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority", "EWS"],
                "max_family_income": 600000.00,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian citizen and head of household. The beneficiary family must not own a pucca (permanent) house in their name or in any family member's name anywhere in India. Must not have received central/state housing assistance under any previous government scheme. Must fall within designated income brackets: Economically Weaker Section (EWS: annual income up to ₹3 lakh), Lower Income Group (LIG: ₹3–6 lakh), or Middle Income Group (MIG). Houses are preferably owned or co-owned by female family members.",
                "rules_summary_bn": "ভারতীয় নাগরিক ও পরিবারের প্রধান। ভারতে পরিবারের কোনো সদস্যের নামে পাকা বাড়ি থাকতে পারবে না। অতীতে কোনো সরকারি আবাসন প্রকল্পের সুবিধা নেননি। বার্ষিক পারিবারিক আয় EWS (৩ লক্ষ পর্যন্ত) বা LIG (৩-৬ লক্ষ)। গৃহস্বত্বে পরিবারের প্রাপ্তবয়স্ক নারী সদস্যের নাম অগ্রাধিকারযোগ্য।"
            }
        )
        set_docs(pmay_u, [
            ("Aadhaar Card and Voter ID (EPIC) of All Family Members", "পরিবারের সকল সদস্যের আধার কার্ড ও ভোটার কার্ড", True, "Aadhaar card and Voter ID (EPIC) of all family members"),
            ("Income Certificate / ITR Acknowledgement / Salary Slips", "আয়ের শংসাপত্র / আইটিআর প্রাপ্তিস্বীকার / বেতন রশিদ", True, "Income certificate / ITR acknowledgement / salary slips proving EWS/LIG income category"),
            ("Self-Declaration / Affidavit of Not Owning a Pucca House in India", "ভারতে কোথাও পাকা বাড়ি না থাকার স্বঘোষিত হলফনামা", True, "Self-declaration/affidavit of not owning a pucca house in India"),
            ("Land Title, Sale Deed, or Property Registration Documents", "জমির দলিল, পর্চা বা রেজিস্ট্রিকৃত স্বত্বের প্রমাণপত্র", True, "Land title, sale deed, or property registration documents (for Beneficiary-Led Construction)"),
            ("Bank Account Passbook (Aadhaar-Linked)", "আধার-সংযুক্ত ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "Bank account passbook (Aadhaar-linked)")
        ])

        # -------------------------------------------------------------
        # Scheme 57: PM-FME (Micro Food Processing Enterprises)
        # -------------------------------------------------------------
        pm_fme, _ = Scheme.objects.update_or_create(
            slug="pm-fme",
            defaults={
                "department": msme,
                "category": "youth",
                "name_en": "PM Formalisation of Micro Food Processing Enterprises (PM-FME)",
                "name_bn": "প্রধানমন্ত্রী ক্ষুদ্র খাদ্য প্রক্রিয়াকরণ শিল্প সহায়তা যোজনা (PM-FME)",
                "name_hi": "पीएम सूक्ष्म खाद्य उद्योग उन्नयन योजना (PM-FME)",
                "tagline_en": "35% credit-linked subsidy up to ₹10 Lakh for upgrading or setting up micro-food processing enterprises under ODOP",
                "tagline_bn": "খাদ্য প্রক্রিয়াকরণ ক্ষুদ্র উদ্যোগ স্থাপন ও আধুনিকীকরণে ৩৫% (সর্বোচ্চ ১০ লক্ষ টাকা) মূলধনী ভর্তুকি ও প্রশিক্ষণ",
                "tagline_hi": "सूक्ष्म खाद्य प्रसंस्करण उद्यमों को आधुनिक बनाने व नए उद्योग हेतु 35% (अधिकतम ₹10 लाख) क्रेडिट-लिंक्ड सब्सिडी",
                "description_en": "PM-FME (under Atmanirbhar Bharat) provides financial, technical, and business support for the upgradation of existing micro-food processing enterprises, offering 35% credit-linked capital subsidy up to ₹10 Lakh, ODOP cluster integration, and quality certification support.",
                "description_bn": "ক্ষুদ্র খাদ্য প্রক্রিয়াকরণ ইউনিট, স্বনির্ভর দল (SHG) এবং কৃষক উৎপাদক সংস্থাগুলিকে (FPO) আধুনিক যন্ত্রপাতি স্থাপন ও ব্যবসায়িক মানোন্নয়নে ৩৫% মূলধনী অনুদান এবং কারিগরি সহায়তা প্রদান করা হয়।",
                "description_hi": "माइक्रो फूड प्रोसेसिंग उद्यमियों और स्वयं सहायता समूहों को आधुनिक मशीनरी खरीदने हेतु 35% सब्सिडी (₹10 लाख तक) और कौशल प्रशिक्षण।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "35% Credit-Linked Capital Subsidy up to ₹10 Lakh + ₹40,000 Seed Capital for SHG members",
                "benefit_amount_text_bn": "৩৫% ঋণ-সংযুক্ত মূলধনী ভর্তুকি (সর্বোচ্চ ১০ লক্ষ টাকা) + স্বনির্ভর দলের সদস্যদের ৪০,০০০ টাকা বীজ মূলধন",
                "application_channels": ["PM-FME National Portal (pmfme.mofpi.gov.in)", "District Resource Person (DRP) / DIC Office", "MSME Development Institute"],
                "official_portal_url": "https://pmfme.mofpi.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_fme,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Existing or aspiring individual micro-food processing units, SHGs, Farmer Producer Organizations (FPOs), or Producer Cooperatives. The individual applicant must be at least 18 years old and have studied up to at least Class 8. Existing micro-enterprises must have formal or informal operations; priority is given to enterprises aligned with the district's 'One District One Product' (ODOP) focus. Enterprise ownership must be proprietary or partnership-based with willingness to contribute at least 10% of the project cost as equity.",
                "rules_summary_bn": "বিদ্যমান বা নতুন ক্ষুদ্র খাদ্য প্রক্রিয়াকরণ উদ্যোক্তা, এসএইচজি বা এফপিও। আবেদনকারীর বয়স কমপক্ষে ১৮ বছর এবং ন্যূনতম অষ্টম শ্রেণি উত্তীর্ণ। জেলার 'এক জেলা এক পণ্য' (ODOP) অন্তর্ভুক্ত উদ্যোগে অগ্রাধিকার। প্রকল্পের ব্যয়ের কমপক্ষে ১০% নিজস্ব মূলধন বিনিয়োগে সম্মত থাকতে হবে।"
            }
        )
        set_docs(pm_fme, [
            ("Aadhaar Card and PAN Card of the Promoter/Proprietor", "উদ্যোক্তা/প্রোপ্রাইটরের আধার কার্ড ও প্যান কার্ড", True, "Aadhaar card and PAN card of the promoter/proprietor"),
            ("Educational Qualification Certificate (Class 8 Pass or Higher)", "শিক্ষাগত যোগ্যতার শংসাপত্র (ন্যূনতম অষ্টম শ্রেণি পাস)", True, "Educational qualification certificate (Class 8 pass or higher)"),
            ("Udyam Registration Certificate (or Trade License / Electricity Bill)", "উদ্যম রেজিস্ট্রেশন শংসাপত্র (বা ট্রেড লাইসেন্স / বিদ্যুৎ বিল)", True, "Udyam Registration Certificate (or electricity connection proof/local trade license)"),
            ("Bank Account Statements for the Last 6 Months", "বিগত ৬ মাসের ব্যাঙ্ক স্টেটমেন্ট", True, "Bank account statements for the last 6 months"),
            ("Detailed Project Report (DPR) / Machinery Quotations", "বিশদ প্রকল্প রিপোর্ট (DPR) ও যন্ত্রপাতির কোটেশন", True, "Detailed Project Report (DPR) / Quotation for proposed machinery and civil work"),
            ("Proof of Business Premises (Ownership Deed or Lease Agreement)", "ব্যবসায়িক প্রাঙ্গনের প্রামাণ্য নথি (দলিল বা ভাড়াপত্র)", True, "Proof of business premises (ownership deed or rent/lease agreement)")
        ])

        # -------------------------------------------------------------
        # Scheme 58: Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY)
        # -------------------------------------------------------------
        pmgkay, _ = Scheme.objects.update_or_create(
            slug="pmgkay",
            defaults={
                "department": food,
                "category": "social_security",
                "name_en": "Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY)",
                "name_bn": "প্রধানমন্ত্রী গরীব কল্যাণ অন্ন যোজনা (PMGKAY)",
                "name_hi": "प्रधानमंत्री गरीब कल्याण अन्न योजना (PMGKAY)",
                "tagline_en": "100% free food grains (rice/wheat) for Antyodaya (AAY) and Priority Household (PHH) ration cardholders under NFSA",
                "tagline_bn": "অন্ত্যোদয় (AAY) ও প্রায়োরিটি গৃহস্থালী (PHH) রেশন কার্ডধারী পরিবারগুলির জন্য সম্পূর্ণ বিনামূল্যে মাসিক খাদ্যশস্য বণ্টন",
                "tagline_hi": "अंत्योदय (AAY) और प्राथमिकता (PHH) राशन कार्ड धारकों को प्रति माह प्रति व्यक्ति 5 किलो मुफ्त राशन वितरण",
                "description_en": "PMGKAY provides 100% free foodgrains to approximately 81.35 crore beneficiaries under the National Food Security Act (NFSA), ensuring 5 kg free grains per person per month to Priority Households (PHH) and 35 kg per family per month to Antyodaya Anna Yojana (AAY) families.",
                "description_bn": "জাতীয় খাদ্য সুরক্ষা আইনের (NFSA) আওতায় অন্ত্যোদয় অন্ন যোজনা (AAY) এবং অগ্রাধিকারপ্রাপ্ত গৃহস্থালি (PHH) কার্ডধারী পরিবারের সকল সদস্যকে ন্যায্যমূল্যের রেশন ডিলারদের মাধ্যমে বিনামূল্যে চাল ও গম প্রদান করা হয়।",
                "description_hi": "राष्ट्रीय खाद्य सुरक्षा अधिनियम (NFSA) के अंतर्गत AAY और PHH राशन कार्ड धारक गरीब परिवारों को हर महीने 100% मुफ्त खाद्यान्न।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "100% Free Foodgrains: 5 kg/person/month for PHH; 35 kg/family/month for Antyodaya (AAY)",
                "benefit_amount_text_bn": "সম্পূর্ণ বিনামূল্যে খাদ্যশস্য: PHH কার্ডে প্রতি মাসে মাথাপিছু ৫ কেজি; অন্ত্যোদয় (AAY) কার্ডে পরিবার পিছু ৩৫ কেজি চাল ও গম",
                "application_channels": ["Fair Price Ration Shops (FPS)", "State Food & Supplies Portal", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://nfsa.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmgkay,
            defaults={
                "min_age": 0,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Families and individuals holding valid Antyodaya Anna Yojana (AAY) cards. Families holding valid Priority Household (PHH) ration cards recognized under the National Food Security Act (NFSA).",
                "rules_summary_bn": "জাতীয় খাদ্য সুরক্ষা আইন (NFSA)-এর অধীন অন্ত্যোদয় অন্ন যোজনা (AAY) কার্ডধারী পরিবার অথবা প্রায়োরিটি হাউসহোল্ড (PHH / SPHH) রেশন কার্ডধারী ব্যক্তিবর্গ।"
            }
        )
        set_docs(pmgkay, [
            ("Active Digital Ration Card (AAY / PHH / State-Equivalent Category)", "সক্রিয় ডিজিটাল রেশন কার্ড (AAY / PHH)", True, "Active Digital Ration Card (AAY / PHH / state-equivalent category)"),
            ("Aadhaar Card of Each Family Member (Linked to Ration Card)", "পরিবারের সকল সদস্যের আধার কার্ড (রেশনের সাথে যুক্ত)", True, "Aadhaar card of each family member (must be linked to the ration card/PDS e-PoS)")
        ])

        # -------------------------------------------------------------
        # Scheme 59: Pradhan Mantri Jan Dhan Yojana (PMJDY)
        # -------------------------------------------------------------
        pmjdy, _ = Scheme.objects.update_or_create(
            slug="pmjdy",
            defaults={
                "department": dfs,
                "category": "social_security",
                "name_en": "Pradhan Mantri Jan Dhan Yojana (PMJDY)",
                "name_bn": "প্রধানমন্ত্রী জন ধন যোজনা (PMJDY)",
                "name_hi": "प्रधानमंत्री जन धन योजना (PMJDY)",
                "tagline_en": "Universal zero-balance savings bank account with free ₹2 Lakh RuPay accidental insurance and ₹10,000 overdraft facility",
                "tagline_bn": "শূন্য জমার ব্যাঙ্ক অ্যাকাউন্ট, ২ লক্ষ টাকার বিনামূল্যে RuPay দুর্ঘটনা বীমা ও ১০,০০০ টাকার ওভারড্রাফট সুবিধা",
                "tagline_hi": "शून्य बैलेंस बचत बैंक खाता, ₹2 लाख का मुफ्त रुपे दुर्घटना बीमा और ₹10,000 की ओवरड्राफ्ट सुविधा",
                "description_en": "PMJDY is India's premier National Mission for Financial Inclusion, ensuring access to financial services like zero minimum balance basic savings accounts, direct access to government DBT welfare payments, a free RuPay Debit Card with ₹2 Lakh accidental insurance cover, and an overdraft facility of up to ₹10,000.",
                "description_bn": "দেশের সকল নাগরিককে ব্যাংকিং পরিষেবায় যুক্ত করতে কোনো ন্যূনতম জমা ছাড়াই (Zero Balance) সেভিংস অ্যাকাউন্ট খোলার সুযোগ, বিনামূল্যে RuPay ডেবিট কার্ডে ২ লক্ষ টাকার দুর্ঘটনা বীমা এবং ১০,০০০ টাকা ওভারড্রাফট সুবিধা প্রদান করা হয়।",
                "description_hi": "प्रत्येक परिवार को बैंकिंग प्रणाली से जोड़ने हेतु शून्य बैलेंस खाता, ₹2 लाख दुर्घटना बीमा युक्त रुपे कार्ड और ₹10,000 तक ओवरड्राफ्ट सुविधा।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Zero Balance Basic Savings Account + Free ₹2 Lakh RuPay Accidental Cover + ₹10,000 Overdraft Facility",
                "benefit_amount_text_bn": "জিরো ব্যালেন্স সেভিংস অ্যাকাউন্ট + বিনামূল্যে ২ লক্ষ টাকার RuPay দুর্ঘটনা বীমা + ১০,০০০ টাকা ওভারড্রাফট",
                "application_channels": ["Any Commercial Bank Branch", "Regional Rural Bank (RRB)", "Post Office / IPPB Branch", "Bank Mitra / Business Correspondent (BC) Point"],
                "official_portal_url": "https://pmjdy.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmjdy,
            defaults={
                "min_age": 10,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Any Indian citizen aged 10 years or older. Must not possess an existing basic savings bank deposit account (BSBDA) in the same bank.",
                "rules_summary_bn": "১০ বছর বা তদূর্ধ্ব বয়সের যেকোনো ভারতীয় নাগরিক। সংশ্লিষ্ট ব্যাংকে পূর্বে কোনো সক্রিয় মৌলিক সঞ্চয়ী ব্যাংক আমানত হিসাব (BSBDA) থাকা চলবে না।"
            }
        )
        set_docs(pmjdy, [
            ("Aadhaar Card (Proof of Identity and Address)", "আধার কার্ড (পরিচয় ও ঠিকানার প্রমাণপত্র)", True, "Aadhaar card (serves as proof of both identity and address)"),
            ("Alternative Officially Valid Documents (OVD)", "বিকল্প সরকারি পরিচয়পত্র (ভোটার/প্যান/ডিএল/মনরেগা)", False, "Alternative: Officially Valid Documents (OVD) if Aadhaar is missing: Voter ID, PAN card, Driving Licence, Passport, or NREGA job card"),
            ("Two Passport-Sized Photographs", "দুটি পাসপোর্ট সাইজের রঙিন ছবি", True, "Two passport-sized photographs")
        ])

        # -------------------------------------------------------------
        # Scheme 60: Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)
        # -------------------------------------------------------------
        pmjjby, _ = Scheme.objects.update_or_create(
            slug="pmjjby",
            defaults={
                "department": dfs,
                "category": "social_security",
                "name_en": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
                "name_bn": "প্রধানমন্ত্রী জীবন জ্যোতি বীমা যোজনা (PMJJBY)",
                "name_hi": "प्रधानमंत्री जीवन ज्योति बीमा योजना (PMJJBY)",
                "tagline_en": "Low-cost ₹2 Lakh renewable term life insurance cover for annual premium of ₹436 (auto-debited)",
                "tagline_bn": "বার্ষিক মাত্র ৪৩৬ টাকা প্রিমিয়ামে ২ লক্ষ টাকার নিশ্চিত জীবন বীমা কভারেজ (যেকোনো কারণে মৃত্যুতে প্রযোজ্য)",
                "tagline_hi": "मात्र ₹436 वार्षिक प्रीमियम पर ₹2 लाख का नवीकरणीय जीवन बीमा कवर (किसी भी कारण से मृत्यु पर देय)",
                "description_en": "PMJJBY offers a one-year renewable term life insurance cover of ₹2,00,000 in case of death of the insured due to any cause, available to individuals aged 18 to 50 years holding an active bank or post office savings account with auto-debit consent.",
                "description_bn": "১৮ থেকে ৫০ বছর বয়সী যেকোনো সঞ্চয়ী ব্যাংক অ্যাকাউন্টধারীর জন্য মাত্র ৪৩৬ টাকা বার্ষিক প্রিমিয়ামে ২ লক্ষ টাকার লাইফ ইনস্যুরেন্স কভার, যা প্রাকৃতিক বা যেকোনো কারণে মৃত্যুতে মনোনীত ব্যক্তিকে (Nominee) প্রদান করা হয়।",
                "description_hi": "18 से 50 वर्ष के नागरिकों के लिए मात्र ₹436 सालाना प्रीमियम में ₹2 लाख का टर्म लाइफ इंश्योरेंस।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "₹2,00,000 Life Insurance Cover Payable to Nominee on Death Due to Any Cause (Annual Premium ₹436)",
                "benefit_amount_text_bn": "যেকোনো কারণে মৃত্যুতে মনোনীত ব্যক্তিকে ₹২,০০,০০০ নিশ্চিত জীবন বীমা কভারেজ (বার্ষিক প্রিমিয়াম মাত্র ₹৪৩৬)",
                "application_channels": ["Savings Bank Branch", "Post Office Savings Bank / IPPB", "Net Banking / Mobile Banking App", "Bank Mitra / CSP"],
                "official_portal_url": "https://financialservices.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmjjby,
            defaults={
                "min_age": 18,
                "max_age": 50,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian citizen aged between 18 and 50 years. Must hold an active individual or joint savings bank/post office account. Must give consent to enable the auto-debit facility for the annual premium (cover continues up to age 55 provided timely renewals occur).",
                "rules_summary_bn": "১৮ থেকে ৫০ বছর বয়সী ভারতীয় নাগরিক। সক্রিয় একক বা যৌথ ব্যাঙ্ক/ডাকঘর সঞ্চয়ী অ্যাকাউন্ট থাকতে হবে এবং বার্ষিক প্রিমিয়াম অটো-ডেবিটের সম্মতি দিতে হবে (নিয়মিত নবায়নে ৫৫ বছর বয়স পর্যন্ত সুরক্ষা বজায় থাকে)।"
            }
        )
        set_docs(pmjjby, [
            ("Aadhaar Card (Primary KYC)", "আধার কার্ড (প্রাথমিক কেওয়াইসি)", True, "Aadhaar card (primary KYC)"),
            ("Bank Passbook / Account Statement", "ব্যাঙ্ক পাসবই বা অ্যাকাউন্ট স্টেটমেন্ট", True, "Bank passbook or account statement showing active savings account details"),
            ("Application-cum-Auto-Debit Consent Form with Nominee Details", "আবেদন ও অটো-ডেবিট সম্মতিপত্র (নমিনির বিবরণ সহ)", True, "Completed application-cum-auto-debit consent form with nominee details")
        ])

        # -------------------------------------------------------------
        # Scheme 61: Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)
        # -------------------------------------------------------------
        pm_kisan, _ = Scheme.objects.update_or_create(
            slug="pm-kisan",
            defaults={
                "department": agri,
                "category": "agriculture",
                "name_en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "name_bn": "প্রধানমন্ত্রী কিষাণ সম্মান নিধি (পিএম-কিষাণ)",
                "name_hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)",
                "tagline_en": "Central DBT income support of ₹6,000/year in 3 equal installments of ₹2,000 for landholding farmer families",
                "tagline_bn": "জমিমালিক কৃষক পরিবারের জন্য বছরে ৬,০০০ টাকা নিশ্চিত আর্থিক সহায়তা (২,০০০ টাকার ৩টি কিস্তিতে সরাসরি ডিবিটি)",
                "tagline_hi": "सभी भूमिधारक किसान परिवारों को प्रति वर्ष ₹6,000 की सुनिश्चित आय सहायता (₹2,000 की 3 समान किस्तों में)",
                "description_en": "PM-KISAN provides income support of ₹6,000 per annum to all cultivable landholding farmer families across the country, paid in three four-monthly installments of ₹2,000 directly into Aadhaar-seeded bank accounts through Direct Benefit Transfer (DBT).",
                "description_bn": "কেন্দ্রীয় সরকার দ্বারা পরিচালিত এই প্রকল্পে কৃষকদের চাষের আনুষঙ্গিক খরচ মেটাতে বছরে ৬,০০০ টাকা আর্থিক অনুদান সরাসরি ব্যাংক অ্যাকাউন্টে তিনটি সমান কিস্তিতে প্রদান করা হয়।",
                "description_hi": "कृषि आवश्यकताओं को पूरा करने हेतु किसानों को ₹6,000 प्रति वर्ष (₹2,000 की तीन किस्तों में) सीधे आधार-सीडेड बैंक खाते में।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "₹6,000 / Year Income Support directly via DBT in 3 Equal Installments of ₹2,000 every 4 months",
                "benefit_amount_text_bn": "বছরে ৬,০০০ টাকা সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি (প্রতি ৪ মাস অন্তর ২,০০০ টাকার ৩টি কিস্তিতে)",
                "application_channels": ["PM-KISAN National Portal (pmkisan.gov.in)", "Assistant Director of Agriculture (ADA) Office", "Common Service Centres (CSC)", "Bangla Sahayata Kendra (BSK)"],
                "official_portal_url": "https://pmkisan.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_kisan,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_land_record": True,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "All landholding farmer families with cultivable land parcels registered in their name in state land records. Ineligible: Institutional landholders; families where any member holds/held a constitutional post, is a serving/retired government employee (Group A, B, C), paid income tax in the last assessment year, or receives a monthly pension of ₹10,000 or more; professionals (doctors, engineers, lawyers, CAs).",
                "rules_summary_bn": "রাজ্য ভূমি রেকর্ডে নিজস্ব নামে চাষযোগ্য কৃষিজমি নথিবদ্ধ রয়েছে এমন সকল কৃষক পরিবার। অযোগ্য: প্রাতিষ্ঠানিক জমির মালিক, সাংবিধানিক পদাধিকারী, সরকারি চাকুরিজীবী/অবসরপ্রাপ্ত কর্মী, আয়কর প্রদানকারী বা ১০,০০০ টাকার বেশি পেনশনভোগী এবং পেশাদার ব্যক্তিবর্গ।"
            }
        )
        set_docs(pm_kisan, [
            ("Aadhaar Card (e-KYC Mandatory)", "আধার কার্ড (ই-কেওয়াইসি বাধ্যতামূলক)", True, "Aadhaar card (e-KYC mandatory)"),
            ("Landholding Record (RoR / Khatian / Porcha / Jamabandi)", "জমির মালিকানার রেকর্ড (পর্চা / খতিয়ান / RoR)", True, "Landholding record (RoR / Khatian / Porcha / Jamabandi / 7/12 extract) proving ownership"),
            ("Aadhaar-Seeded Bank Account Details", "আধার-সংযুক্ত ব্যাঙ্ক অ্যাকাউন্টের বিবরণ", True, "Aadhaar-seeded bank account details"),
            ("Mobile Number Linked with Aadhaar", "আধারের সাথে যুক্ত সক্রিয় মোবাইল নম্বর", True, "Mobile number linked with Aadhaar")
        ])

        # -------------------------------------------------------------
        # Scheme 62: PM-MKSSY (Matsya Kisan Samridhi Sah-Yojana)
        # -------------------------------------------------------------
        pm_mkssy, _ = Scheme.objects.update_or_create(
            slug="pm-mkssy",
            defaults={
                "department": fisheries,
                "category": "agriculture",
                "name_en": "Pradhan Mantri Matsya Kisan Samridhi Sah-Yojana (PM-MKSSY)",
                "name_bn": "প্রধানমন্ত্রী মৎস্য কিষাণ সমৃদ্ধি সহ-যোজনা (PM-MKSSY)",
                "name_hi": "प्रधानमंत्री मत्स्य किसान समृद्धि सह-योजना (PM-MKSSY)",
                "tagline_en": "Formalization, digital NFDP registration, performance grants, and aquaculture insurance incentives for fish farmers and workers",
                "tagline_bn": "মৎস্যচাষী ও মৎস্যকর্মীদের প্রাতিষ্ঠানিক আর্থিক ঋণ, এনএফডিপি ডিজিটাল রেজিস্ট্রেশন ও অ্যাকোয়াকালচার বীমা সহায়তা",
                "tagline_hi": "मत्स्य पालकों और श्रमिकों के लिए डिजिटल एनएफडीपी पंजीकरण, ऋण सुविधा और जलीय कृषि बीमा सब्सिडी",
                "description_en": "PM-MKSSY (a Central Sector sub-scheme under PMMSY) formalizes the unorganized fisheries sector through the National Fisheries Digital Platform (NFDP), facilitating institutional credit, aquaculture insurance premium subsidies, and performance grants for micro and small aquaculture enterprises.",
                "description_bn": "মৎস্যচাষি, মাছ শ্রমিক এবং ক্ষুদ্র অ্যাকোয়াকালচার উদ্যোগগুলিকে প্রাতিষ্ঠানিক ঋণের সাথে যুক্ত করা, জাতীয় মৎস্য ডিজিটাল প্ল্যাটফর্মে (NFDP) নথিভুক্তি এবং জলজ চাষের ফসল বীমায় আর্থিক ভর্তুকি প্রদান করা হয়।",
                "description_hi": "मत्स्य पालकों, मछली श्रमिकों और स्वयं सहायता समूहों को औपचारिक ऋण, नेशनल फिशरीज डिजिटल प्लेटफॉर्म पर पहचान और बीमा सब्सिडी।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Up to 40% Performance Grant / Formal Institutional Credit & Aquaculture Insurance Premium Incentive",
                "benefit_amount_text_bn": "৪০% পর্যন্ত কর্মক্ষমতা অনুদান / প্রাতিষ্ঠানিক সহজ ঋণ ও মৎস্য বীমার প্রিমিয়াম ভর্তুকি",
                "application_channels": ["National Fisheries Digital Platform (NFDP - nfdp.dof.gov.in)", "District Fisheries Officer (DFO) / BFEO", "Fisheries Cooperative Societies"],
                "official_portal_url": "https://nfdp.dof.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_mkssy,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Fishers, fish farmers, fish workers, micro and small aquaculture enterprises, SHGs, and Fisheries Cooperatives/FFPOs. Must be registered on the National Fisheries Digital Platform (NFDP). Have availed institutional credit or are applying for formal institutional finance/aquaculture insurance.",
                "rules_summary_bn": "মৎস্যচাষী, মাছ শ্রমিক, ক্ষুদ্র অ্যাকোয়াকালচার এন্টারপ্রাইজ, এসএইচজি এবং মৎস্য সমবায়/FFPO। জাতীয় মৎস্য ডিজিটাল প্ল্যাটফর্মে (NFDP) নিবন্ধিত হতে হবে এবং প্রাতিষ্ঠানিক ঋণ বা মৎস্য বীমার সুবিধা গ্রহণ করতে আগ্রহী হতে হবে।"
            }
        )
        set_docs(pm_mkssy, [
            ("NFDP Registration ID / Acknowledgement", "জাতীয় মৎস্য ডিজিটাল প্ল্যাটফর্ম (NFDP) রেজিস্ট্রেশন আইডি", True, "NFDP Registration ID / acknowledgement"),
            ("Aadhaar Card and PAN Card", "আধার কার্ড ও প্যান কার্ড", True, "Aadhaar card and PAN card"),
            ("Proof of Fish Farming Activities / Land Records / Water Body Lease", "মৎস্যচাষের প্রমাণ / জলাশয় লিজের দলিল বা খতিয়ান", True, "Proof of fish farming activities / land records / water body lease deed"),
            ("Institutional Loan Sanction Letter / Disbursement Proof or Bank Passbook", "প্রাতিষ্ঠানিক ঋণ মঞ্জুরি পত্র / ব্যাংক পাসবই", True, "Institutional loan sanction letter / disbursement proof or bank passbook"),
            ("Aquaculture Insurance Documentation", "অ্যাকোয়াকালচার মৎস্য বীমা সংক্রান্ত নথি", False, "Aquaculture insurance documentation (if seeking insurance premium incentives)")
        ])

        # -------------------------------------------------------------
        # Scheme 63: Pradhan Mantri MUDRA Yojana (PMMY)
        # -------------------------------------------------------------
        pmmy, _ = Scheme.objects.update_or_create(
            slug="pmmy",
            defaults={
                "department": dfs,
                "category": "youth",
                "name_en": "Pradhan Mantri MUDRA Yojana (PMMY)",
                "name_bn": "প্রধানমন্ত্রী মুদ্রা যোজনা (PMMY)",
                "name_hi": "प्रधानमंत्री मुद्रा योजना (PMMY)",
                "tagline_en": "Collateral-free business loans up to ₹20 Lakh in 3 tiers (Shishu, Kishore, Tarun) for non-farm micro and small enterprises",
                "tagline_bn": "জামানতমুক্ত ব্যবসায়িক ঋণ (শিশু: ৫০ হাজার, কিশোর: ৫ লাখ, তরুণ: ২০ লাখ টাকা পর্যন্ত) ক্ষুদ্র ও ছোট উদ্যোগের জন্য",
                "tagline_hi": "गैर-कृषि सूक्ष्म व छोटे उद्यमों के लिए ₹20 लाख तक का बिना गारंटी मुद्रा बैंक लोन (शिशु, किशोर, तरुण)",
                "description_en": "Pradhan Mantri MUDRA Yojana provides formal collateral-free institutional credit up to ₹20 Lakh to non-farm, non-corporate micro/small enterprises engaged in manufacturing, trading, services, and agri-allied activities across Shishu, Kishore, and Tarun loan categories.",
                "description_bn": "উৎপাদন, ব্যবসা এবং পরিষেবা খাতের নতুন বা বিদ্যমান ক্ষুদ্র ব্যবসায়ীদের জন্য জামানতবিহীন ব্যাংক ঋণ সুবিধা (শিশু: ₹৫০,০০০ পর্যন্ত, কিশোর: ₹৫০,০০০ থেকে ₹৫ লক্ষ, তরুণ: ₹৫ লক্ষ থেকে ₹২০ লক্ষ পর্যন্ত)।",
                "description_hi": "व्यापार, विनिर्माण व सेवा क्षेत्र के नए व पुराने उद्यमियों के लिए बिना गारंटी आसान बैंक ऋण।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Collateral-Free Loans: Shishu (up to ₹50,000), Kishore (up to ₹5 Lakh), Tarun (up to ₹10-₹20 Lakh)",
                "benefit_amount_text_bn": "জামানতমুক্ত ঋণ: শিশু (৫০,০০০ পর্যন্ত), কিশোর (৫ লাখ পর্যন্ত), তরুণ (১০ থেকে ২০ লাখ টাকা পর্যন্ত)",
                "application_channels": ["Udyamimitra Portal (udyamimitra.in)", "Commercial Banks, RRBs & Small Finance Banks", "NBFCs / Micro Finance Institutions (MFIs)"],
                "official_portal_url": "https://www.mudra.org.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmmy,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Any Indian citizen operating or planning a non-farm income-generating micro or small enterprise (manufacturing, trading, services, or agri-allied activities). Loan tiers: Shishu: Loans up to ₹50,000; Kishore: Loans above ₹50,000 up to ₹5,00,000; Tarun: Loans above ₹5,00,000 up to ₹10,00,000 (extended up to ₹20,00,000 under Tarun Plus for repeat borrowers who repaid past loans). Applicant must not be a defaulter to any bank or financial institution.",
                "rules_summary_bn": "অকৃষি উৎপাদনশীল ক্ষুদ্র ব্যবসা পরিচালনাকারী বা শুরু করতে ইচ্ছুক যেকোনো ভারতীয় নাগরিক। ঋণ স্তর: শিশু (৫০,০০০ পর্যন্ত), কিশোর (৫০ হাজার থেকে ৫ লক্ষ), তরুণ (৫ লক্ষ থেকে ২০ লক্ষ পর্যন্ত)। আবেদনকারী কোনো আর্থিক প্রতিষ্ঠানে ঋণখেলাপি হওয়া চলবে না।"
            }
        )
        set_docs(pmmy, [
            ("Identity Proof (Aadhaar, Voter ID, PAN Card, Driving Licence)", "পরিচয়পত্র (আধার, ভোটার কার্ড, প্যান বা ড্রাইভিং লাইসেন্স)", True, "Identity proof (Aadhaar, Voter ID, PAN card, Driving Licence)"),
            ("Residence Proof (Utility Bills, Voter ID)", "বাসস্থানের প্রমাণপত্র (বিদ্যুৎ বিল, ভোটার কার্ড)", True, "Residence proof (utility bills, Voter ID)"),
            ("Proof of Business Identity / Address (Udyam, Trade Licence, GST)", "ব্যবসায়িক পরিচয় ও ঠিকানার প্রমাণপত্র (উদ্যম, ট্রেড লাইসেন্স, জিএসটি)", True, "Proof of business identity/address (Udyam registration, trade licence, sales tax/GST returns)"),
            ("Bank Statements for the Last 6 Months", "বিগত ৬ মাসের ব্যাঙ্ক অ্যাকাউন্ট স্টেটমেন্ট", True, "Bank statements for the last 6 months"),
            ("Project Report / Quotations for Machinery, Equipment, or Inventory", "প্রকল্প রিপোর্ট বা মেশিনারি ও সামগ্রী ক্রয়ের কোটেশন", True, "Project report/quotations for machinery, equipment, or inventory purchase")
        ])

        # -------------------------------------------------------------
        # Scheme 64: Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)
        # -------------------------------------------------------------
        pm_sym, _ = Scheme.objects.update_or_create(
            slug="pm-sym",
            defaults={
                "department": labour,
                "category": "social_security",
                "name_en": "Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)",
                "name_bn": "প্রধানমন্ত্রী শ্রমযোগী মান-ধন যোজনা (PM-SYM)",
                "name_hi": "प्रधानमंत्री श्रम योगी मान-धन योजना (PM-SYM)",
                "tagline_en": "Assured monthly pension of ₹3,000 after age 60 for unorganized workers earning ₹15,000 or less",
                "tagline_bn": "৬০ বছর বয়সের পর অসংগঠিত শ্রমিকদের জন্য নিশ্চিত মাসিক ৩,০০০ টাকা বার্ধক্য পেনশন",
                "tagline_hi": "60 वर्ष की आयु के बाद असंगठित श्रमिकों के लिए ₹3,000 की सुनिश्चित मासिक पेंशन (मासिक अंशदान ₹55-₹200)",
                "description_en": "PM-SYM is a voluntary and contributory pension scheme for unorganized workers (home-based workers, street vendors, ragpickers, domestic workers, rickshaw pullers, construction workers) earning up to ₹15,000/month, providing an assured monthly pension of ₹3,000 upon reaching 60 years of age with 50% matching contribution from the Central Government.",
                "description_bn": "গৃহকর্মী, নির্মাণ শ্রমিক, পথবিক্রেতা, রিকশাচালক সহ অসংগঠিত ক্ষেত্রের শ্রমিকদের জন্য ৬০ বছর বয়সের পর মাসিক ৩,০০০ টাকা নিশ্চিত পেনশন প্রকল্প। এতে শ্রমিক ও কেন্দ্রীয় সরকার সমান হারে (৫০:৫০) মাসিক প্রিমিয়াম জমা দেয়।",
                "description_hi": "असंगठित क्षेत्र के कामगारों (घरेलू सहायिका, रेहड़ी-पटरी, रिक्शा चालक, निर्माण श्रमिक) के लिए ₹3,000 मासिक सुनिश्चित वृद्धावस्था पेंशन।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "Guaranteed Monthly Pension of ₹3,000 After Age 60 for Unorganized Workers",
                "benefit_amount_text_bn": "৬০ বছর বয়সের পর অসংগঠিত শ্রমিকদের জন্য প্রতি মাসে নিশ্চিত ৩,০০০ টাকা বার্ধক্য পেনশন",
                "application_channels": ["Common Service Centres (CSC / VLE)", "e-Shram Portal (eshram.gov.in)", "Life Insurance Corporation (LIC) Branches"],
                "official_portal_url": "https://maandhan.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_sym,
            defaults={
                "min_age": 18,
                "max_age": 40,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "max_family_income": 180000.00,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Unorganized workers (maids, street vendors, rickshaw pullers, construction workers, agricultural workers, cobblers, etc.). Entry age between 18 and 40 years. Monthly income must be ₹15,000 or less. Must not be covered under EPFO, ESIC, or NPS (government-funded) and must not be an income tax payer.",
                "rules_summary_bn": "অসংগঠিত ক্ষেত্রের শ্রমিক (গৃহসহায়ক, পথবিক্রেতা, রিকশাচালক, নির্মাণ কর্মী, দিনমজুর)। বয়স ১৮ থেকে ৪০ বছরের মধ্যে। মাসিক আয় ১৫,০০০ টাকা বা তার কম। EPFO, ESIC বা NPS আওতাভুক্ত হওয়া চলবে না এবং আয়করদাতা হওয়া যাবে না।"
            }
        )
        set_docs(pm_sym, [
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar card"),
            ("Savings Bank Account / Jan Dhan Account Passbook (with IFSC Code)", "সঞ্চয়ী ব্যাঙ্ক অ্যাকাউন্ট / জন ধন অ্যাকাউন্ট পাসবই (IFSC সহ)", True, "Savings Bank Account / Jan Dhan Account passbook (with IFSC code)"),
            ("Mobile Phone for Initial OTP Verification", "প্রাথমিক ওটিপি যাচাইয়ের জন্য সক্রিয় মোবাইল নম্বর", True, "Mobile phone for initial OTP verification")
        ])

        # -------------------------------------------------------------
        # Scheme 65: Pradhan Mantri Suraksha Bima Yojana (PMSBY)
        # -------------------------------------------------------------
        pmsby, _ = Scheme.objects.update_or_create(
            slug="pmsby",
            defaults={
                "department": dfs,
                "category": "social_security",
                "name_en": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
                "name_bn": "প্রধানমন্ত্রী সুরক্ষা বীমা যোজনা (PMSBY)",
                "name_hi": "प्रधानमंत्री सुरक्षा बीमा योजना (PMSBY)",
                "tagline_en": "Accidental death and disability insurance cover of ₹2 Lakh for an annual premium of just ₹20 (auto-debited)",
                "tagline_bn": "বছরে মাত্র ২০ টাকা প্রিমিয়ামে ২ লক্ষ টাকার দুর্ঘটনাজনিত মৃত্যু ও স্থায়ী অক্ষমতা বীমা সুরক্ষা",
                "tagline_hi": "मात्र ₹20 वार्षिक प्रीमियम पर ₹2 लाख का दुर्घटना मृत्यु एवं स्थायी दिव्यांगता बीमा कवर",
                "description_en": "PMSBY provides one-year accidental death and disability coverage of ₹2,00,000 for accidental death or total permanent disability and ₹1,00,000 for permanent partial disability, available to citizens aged 18 to 70 years holding a bank savings account with auto-debit consent.",
                "description_bn": "১৮ থেকে ৭০ বছর বয়সী যেকোনো ব্যাংক সঞ্চয়ী অ্যাকাউন্টধারীর জন্য মাত্র ২০ টাকা বার্ষিক প্রিমিয়ামে দুর্ঘটনাজনিত মৃত্যু ও স্থায়ী সম্পূর্ণ পঙ্গুত্বে ২ লক্ষ টাকা এবং আংশিক পঙ্গুত্বে ১ লক্ষ টাকার বীমা কভারেজ প্রদান করা হয়।",
                "description_hi": "18 से 70 वर्ष के बैंक खाताधारकों के लिए सालाना मात्र ₹20 में ₹2 लाख का दुर्घटना बीमा कवर।",
                "benefit_type": "insurance",
                "benefit_amount_text_en": "₹2,00,000 for Accidental Death / Permanent Total Disability; ₹1,00,000 for Partial Disability (Premium ₹20/yr)",
                "benefit_amount_text_bn": "দুর্ঘটনাজনিত মৃত্যু বা স্থায়ী পঙ্গুত্বে ২ লক্ষ টাকা; আংশিক পঙ্গুত্বে ১ লক্ষ টাকা বীমা কভার (বার্ষিক প্রিমিয়াম মাত্র ২০ টাকা)",
                "application_channels": ["Bank Branch", "Post Office Savings Bank / IPPB", "Net Banking / Mobile Banking App", "Bank Mitra / CSP"],
                "official_portal_url": "https://financialservices.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmsby,
            defaults={
                "min_age": 18,
                "max_age": 70,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian citizen aged between 18 and 70 years. Must hold an active individual or joint savings bank/post office account. Must give auto-debit authorization for the nominal annual premium (covering accidental death and permanent disability).",
                "rules_summary_bn": "১৮ থেকে ৭০ বছর বয়সী ভারতীয় নাগরিক। সক্রিয় সঞ্চয়ী ব্যাংক বা ডাকঘর অ্যাকাউন্ট থাকতে হবে এবং বার্ষিক নামমাত্র ২০ টাকা প্রিমিয়াম অটো-ডেবিটের লিখিত সম্মতি দিতে হবে।"
            }
        )
        set_docs(pmsby, [
            ("Aadhaar Card (e-KYC)", "আধার কার্ড (ই-কেওয়াইসি)", True, "Aadhaar card (e-KYC)"),
            ("Bank Passbook or Account Number with Auto-Debit Consent Form", "ব্যাঙ্ক পাসবই ও অটো-ডেবিট সম্মতিপত্র", True, "Bank passbook or account number with auto-debit consent form"),
            ("Nominee Details and Contact Number", "নমিনির বিবরণ ও যোগাযোগ নম্বর", True, "Nominee details and contact number")
        ])

        # -------------------------------------------------------------
        # Scheme 66: Pradhan Mantri Vishwakarma Yojana
        # -------------------------------------------------------------
        pm_vishwa, _ = Scheme.objects.update_or_create(
            slug="pm-vishwakarma",
            defaults={
                "department": msme,
                "category": "youth",
                "name_en": "Pradhan Mantri Vishwakarma Yojana",
                "name_bn": "প্রধানমন্ত্রী বিশ্বকর্মা যোজনা",
                "name_hi": "प्रधानमंत्री विश्वकर्मा योजना",
                "tagline_en": "Toolkit grant of ₹15,000, 5% collateral-free loans up to ₹3 Lakh, skill training, and official recognition for 18 traditional artisan trades",
                "tagline_bn": "১৮টি ঐতিহ্যবাহী হস্তশিল্প ও কারিগর পেশায় ₹১৫,০০০ টুলকিট অনুদান, ৫% সুদে ₹৩ লক্ষ পর্যন্ত জামানতবিহীন ঋণ ও প্রশিক্ষণ",
                "tagline_hi": "18 पारंपरिक शिल्पकलाओं और कारीगरों हेतु ₹15,000 टूलकिट अनुदान, 5% ब्याज पर ₹3 लाख तक बिना गारंटी लोन व स्किल ट्रेनिंग",
                "description_en": "PM Vishwakarma Yojana provides holistic end-to-end support to traditional artisans and craftspeople across 18 family-based trades (carpenters, blacksmiths, goldsmiths, potters, sculptors, cobblers, tailors, etc.), including official certificate/ID, 5–7 days basic training with ₹500/day stipend, ₹15,000 toolkit grant, and collateral-free enterprise loans up to ₹3 Lakh at a concessional interest rate of 5%.",
                "description_bn": "সূত্রধর, কামার, কুমার, ভাস্কর, চর্মকার, দর্জি সহ ১৮টি ঐতিহ্যবাহী পেশার কারিগরদের সরকারি স্বীকৃতি, প্রতিদিন ৫০০ টাকা ভাতাসহ প্রশিক্ষণ, ১৫,০০০ টাকা মূল্যের বিনামূল্যে আধুনিক টুলকিট এবং মাত্র ৫% সরল সুদে ৩ লক্ষ টাকা পর্যন্ত সহজ ঋণ প্রদান করা হয়।",
                "description_hi": "पारंपरिक बढ़ई, लोहार, कुम्हार, मूर्तिकार, मोची, दर्जी आदि 18 शिल्पकलाओं से जुड़े कारीगरों को पहचान पत्र, ₹15,000 टूलकिट वाउचर और ₹3 लाख तक रियायती लोन।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "PM Vishwakarma Certificate & ID + ₹15,000 Toolkit E-Voucher + Collateral-Free Loans up to ₹3 Lakh at 5% Interest",
                "benefit_amount_text_bn": "বিশ্বকর্মা সার্টিফিকেট ও পরিচয়পত্র + ১৫,০০০ টাকার টুলকিট ই-ভাউচার + ৫% সুদে ৩ লক্ষ টাকা পর্যন্ত জামানতমুক্ত ঋণ",
                "application_channels": ["Common Service Centre (CSC - Biometric e-KYC)", "Gram Panchayat / Municipal Ward Desk", "District Industries Centre (DIC)"],
                "official_portal_url": "https://pmvishwakarma.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_vishwa,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Traditional artisans and craftspeople working with their hands and tools in one of the 18 recognized traditional family trades (e.g., carpenter, blacksmith, potter, sculptor, cobbler, tailor, mason, barber, basket/mat maker, boat builder, etc.). Minimum age of 18 years at registration. The beneficiary should be actively engaged in the relevant trade and have not availed credit under similar government self-employment schemes (PMEGP, MUDRA, PM SVANidhi) in the past 5 years. Limited to one member per family. Regular government servants and their family members are ineligible.",
                "rules_summary_bn": "১৮টি ঐতিহ্যবাহী পেশার সাথে যুক্ত নিজস্ব হাতে ও যন্ত্রপাতিতে কর্মরত কারিগর। বয়স ন্যূনতম ১৮ বছর। পরিবারের কেবল একজন সদস্য আবেদন করতে পারবেন। বিগত ৫ বছরে PMEGP, মুদ্রা বা স্বনিধি ঋণ গ্রহণ করেননি এবং পরিবারের কেউ সরকারি চাকুরিজীবী নন।"
            }
        )
        set_docs(pm_vishwa, [
            ("Aadhaar Card (Biometric e-KYC Completed at CSC)", "আধার কার্ড (CSC সেন্টারে বায়োমেট্রিক ই-কেওয়াইসি)", True, "Aadhaar card (biometric e-KYC completed at CSC)"),
            ("Aadhaar-Linked Active Mobile Number", "আধার সংযুক্ত সক্রিয় মোবাইল নম্বর", True, "Aadhaar-linked active mobile number"),
            ("Bank Account Details (Passbook/Statement)", "ব্যাঙ্ক অ্যাকাউন্ট বিবরণ (পাসবই / স্টেটমেন্ট)", True, "Bank account details (passbook/statement)"),
            ("Skill/Trade Self-Declaration and Verification by GP / Urban Local Body", "ট্রেড স্বঘোষণাপত্র ও পঞ্চায়েত/পুরসভা অনুমোদন", True, "Skill/Trade self-declaration and verification by Gram Panchayat or Urban Local Body")
        ])

        # -------------------------------------------------------------
        # Scheme 67: Pradhan Mantri Virasat Ka Samvardhan (PM-VIKAS)
        # -------------------------------------------------------------
        pm_vikas, _ = Scheme.objects.update_or_create(
            slug="pm-vikas",
            defaults={
                "department": minority,
                "category": "tribal_caste",
                "name_en": "Pradhan Mantri Virasat Ka Samvardhan (PM-VIKAS)",
                "name_bn": "প্রধানমন্ত্রী ঐতিহ্য সংরক্ষণ ও বিকাশ যোজনা (PM-VIKAS)",
                "name_hi": "प्रधानमंत्री विरासत का संवर्धन (PM-VIKAS)",
                "tagline_en": "Integrated skilling, heritage craft revival, women entrepreneurship, and education for notified minority communities",
                "tagline_bn": "সংখ্যালঘু সম্প্রদায়ের কারিগর, নারী উদ্যোক্তা ও শিক্ষার্থীদের জন্য ঐতিহ্যবাহী দক্ষতা প্রশিক্ষণ ও কর্মসংস্থান প্রকল্প",
                "tagline_hi": "अल्पसंख्यक समुदायों के पारंपरिक कारीगरों, महिला उद्यमियों और युवाओं के लिए समग्र कौशल प्रशिक्षण व आजीविका संवर्धन योजना",
                "description_en": "PM-VIKAS converges five erstwhile schemes of the Ministry of Minority Affairs (Seekho Aur Kamao, USTTAD, Hamari Dharohar, Nai Roshni, and Nai Manzil) to provide formal education bridging, NSQF skill training, women leadership modules, and enterprise development to artisans and youth from notified minority communities.",
                "description_bn": "মুসলিম, খ্রিস্টান, শিখ, বৌদ্ধ, পার্সি ও জৈন সম্প্রদায়ের ঐতিহ্যবাহী কারিগর, স্কুলছুট শিক্ষার্থী এবং নারীদের জন্য আধুনিক কারিগরি দক্ষতা প্রশিক্ষণ, শিক্ষা সমাপ্তিকরণ এবং স্বাবলম্বী ব্যবসা গড়ে তোলার সর্বাঙ্গীন সরকারি প্রকল্প।",
                "description_hi": "छह अधिसूचित अल्पसंख्यक समुदायों के पारंपरिक कारीगरों, दस्तकारों, महिलाओं व युवाओं के सामाजिक-आर्थिक सशक्तिकरण हेतु समेकित योजना।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Free NSQF Skill Training + Monthly Stipend + Enterprise Credit & Market Linkages for Artisans",
                "benefit_amount_text_bn": "বিনামূল্যে আধুনিক কারিগরি প্রশিক্ষণ + মাসিক স্টাইপেন্ড + ব্যবসা স্থাপন ঋণ ও বাজারজাতকরণ সহায়তা",
                "application_channels": ["PM-VIKAS / Ministry of Minority Affairs Portal", "WBMDFC District Offices", "Empanelled Project Implementing Agencies (PIAs)"],
                "official_portal_url": "https://minorityaffairs.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pm_vikas,
            defaults={
                "min_age": 14,
                "max_age": 45,
                "gender_allowed": "all",
                "caste_categories": ["Minority", "EWS"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Indian nationals belonging to the six notified minority communities: Muslim, Christian, Sikh, Buddhist, Parsi, and Jain (up to 25% non-minority EWS candidates may be accommodated in traditional skilling). Age: 14 to 45 years for Skilling, Training, and Education components; 18 to 45 years for the Women Leadership & Entrepreneurship component. Target beneficiaries include traditional artisans, artisans' family members, school dropouts, and women entrepreneurs.",
                "rules_summary_bn": "ছয়টি বিজ্ঞাপিত সংখ্যালঘু সম্প্রদায়ের (মুসলিম, খ্রিস্টান, শিখ, বৌদ্ধ, পার্সি ও জৈন) ভারতীয় নাগরিক (২৫% পর্যন্ত সাধারণ EWS প্রার্থীরাও অন্তর্ভুক্ত হতে পারেন)। বয়স: দক্ষতা ও শিক্ষা উপাদানে ১৪-৪৫ বছর; মহিলা নেতৃত্ব উপাদানে ১৮-৪৫ বছর।"
            }
        )
        set_docs(pm_vikas, [
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar card"),
            ("Self-Declaration or Certificate of Minority Community Status", "সংখ্যালঘু সম্প্রদায়ের স্বঘোষণাপত্র বা শংসাপত্র", True, "Self-declaration or certificate of minority community status (or EWS certificate for non-minority participants)"),
            ("Educational Qualification Certificates / School Leaving Records", "শিক্ষাগত যোগ্যতার শংসাপত্র / স্কুল ত্যাগের প্রমাণপত্র", False, "Educational qualification certificates/school leaving records (if applying for bridging/NIOS or higher NSQF modules)"),
            ("Aadhaar-Seeded Bank Account Passbook", "আধার সংযুক্ত ব্যাঙ্ক পাসবই", True, "Aadhaar-seeded bank account passbook")
        ])

        # -------------------------------------------------------------
        # Scheme 68: Pradhan Mantri Ujjwala Yojana (PMUY)
        # -------------------------------------------------------------
        pmuy, _ = Scheme.objects.update_or_create(
            slug="pmuy",
            defaults={
                "department": mopng,
                "category": "women",
                "name_en": "Pradhan Mantri Ujjwala Yojana (PMUY)",
                "name_bn": "প্রধানমন্ত্রী উজ্জ্বলা যোজনা (PMUY)",
                "name_hi": "प्रधानमंत्री उज्ज्वला योजना (PMUY)",
                "tagline_en": "Free deposit-free domestic LPG connection + first refill & stove free for adult women in eligible poor households",
                "tagline_bn": "দারিদ্র্যসীমার নিচে থাকা পরিবারের প্রাপ্তবয়স্ক মহিলাদের জন্য সম্পূর্ণ বিনামূল্যে এলপিজি গ্যাস সিলিন্ডার সংযোগ ও রান্নার ওভেন",
                "tagline_hi": "गरीब परिवारों की वयस्क महिलाओं के लिए मुफ्त एलपीजी गैस कनेक्शन, पहला भरा सिलेंडर, चूल्हा व ₹300 सब्सिडी",
                "description_en": "PMUY provides deposit-free domestic LPG connections to adult women from poor and vulnerable households without existing gas connections, offering free connection deposit, first cylinder refill, LPG hotplate (stove), and ongoing targeted DBT subsidies of ₹300 per 14.2 kg cylinder for up to 12 refills annually.",
                "description_bn": "দরিদ্র পরিবারের প্রাপ্তবয়স্ক মহিলাদের স্বাস্থ্য সুরক্ষা এবং ধোঁয়ামুক্ত পরিবেশ নিশ্চিত করতে সম্পূর্ণ জামানতমুক্ত নতুন রান্নার গ্যাস সংযোগ, বিনামূল্যে গ্যাস ওভেন এবং ভর্তুকিযুক্ত সিলিন্ডার প্রদান করা হয়।",
                "description_hi": "महिलाओं के स्वास्थ्य की सुरक्षा हेतु बिना किसी सिक्योरिटी डिपॉजिट के नया घरेलू गैस कनेक्शन, पहला रिफिल और चूल्हा मुफ्त।",
                "benefit_type": "one_time",
                "benefit_amount_text_en": "Free Deposit-Free LPG Connection + First Refill & Stove Free + ₹300 Targeted Cylinder Subsidy",
                "benefit_amount_text_bn": "সম্পূর্ণ জামানতমুক্ত বিনামূল্যে নতুন এলপিজি সিলিন্ডার সংযোগ + প্রথম রিফিল ও ওভেন বিনামূল্যে + ₹৩০০ ভর্তুকি",
                "application_channels": ["PMUY Portal (pmuy.gov.in)", "Authorized LPG Gas Distributors (Indane / Bharatgas / HP Gas)", "Common Service Centre (CSC)"],
                "official_portal_url": "https://www.pmuy.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmuy,
            defaults={
                "min_age": 18,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Adult woman (at least 18 years old) from an eligible low-income household lacking an active LPG connection. Belongs to eligible categories: listed under SECC-2011, SC/ST households, PMAY beneficiaries, Antyodaya Anna Yojana (AAY), most backward classes, or living in tea gardens/forest areas. No existing LPG connection in any household member's name.",
                "rules_summary_bn": "১৮ বছর বা তার বেশি বয়সী নারী সদস্য যার পরিবারে কোনো সক্রিয় এলপিজি সংযোগ নেই। SECC-2011 তালিকাভুক্ত, এসসি/এসটি, অন্ত্যোদয় অন্ন যোজনা (AAY), চা বাগান বা অরণ্য এলাকার দরিদ্র পরিবার। পরিবারের কোনো সদস্যের নামে রান্নার গ্যাস থাকা চলবে না।"
            }
        )
        set_docs(pmuy, [
            ("Aadhaar Card of the Female Applicant and Adult Family Members", "মহিলা আবেদনকারী এবং পরিবারের সকল প্রাপ্তবয়স্ক সদস্যের আধার কার্ড", True, "Aadhaar card of the female applicant and adult family members"),
            ("Ration Card Confirming Family Composition", "পারিবারিক রেশন কার্ড (সদস্য তালিকার প্রমাণ)", True, "Ration Card confirming family composition (or annexure certificate from state authority)"),
            ("Proof of Address", "বাসস্থানের প্রমাণপত্র (ভোটার/আধার/বিদ্যুৎ বিল)", True, "Proof of address"),
            ("Bank Account Passbook / IFSC Details (Aadhaar-Linked)", "আধার-সংযুক্ত ব্যাঙ্ক পাসবই / IFSC বিবরণ", True, "Bank account passbook / IFSC details (Aadhaar linked for DBT subsidy)")
        ])

        # -------------------------------------------------------------
        # Scheme 69: Pre-Matric Scholarship for SC, ST & OBC Students
        # -------------------------------------------------------------
        pre_matric, _ = Scheme.objects.update_or_create(
            slug="pre-matric-scholarship-sc-st-obc",
            defaults={
                "department": school_edu,
                "category": "education",
                "name_en": "Pre-Matric Scholarship for SC, ST & OBC Students",
                "name_bn": "এসসি, এসটি ও ওবিসি শিক্ষার্থীদের জন্য প্রাক-ম্যাট্রিক স্কলারশিপ",
                "name_hi": "एससी, एसटी व ओबीसी छात्रों के लिए प्री-मैट्रिक छात्रवृत्ति",
                "tagline_en": "Centrally sponsored pre-matric scholarship for regular SC, ST, and OBC students in recognized schools",
                "tagline_bn": "সরকারি ও অনুমোদিত স্কুলে অধ্যয়নরত এসসি, এসটি ও ওবিসি ছাত্র-ছাত্রীদের প্রাক-ম্যাট্রিক সরকারি বৃত্তি",
                "tagline_hi": "सरकारी व मान्यता प्राप्त विद्यालयों में पढ़ रहे अनुसूचित जाति, जनजाति व ओबीसी छात्रों हेतु प्री-मैट्रिक छात्रवृत्ति",
                "description_en": "Centrally sponsored Pre-Matric Scholarship provides financial assistance to SC, ST, and OBC students studying in recognized government or aided schools (primarily Classes 9 and 10) to minimize dropout rates and support secondary education expenses.",
                "description_bn": "নবম ও দশম শ্রেণিতে পাঠরত অনুসূচিত জাতি (SC), অনুসূচিত উপজাতি (ST) এবং অনগ্রসর শ্রেণির (OBC) নিয়মিত ছাত্রছাত্রীদের পড়াশোনার খরচ ও বার্ষিক ভাতা প্রদানে এই কেন্দ্রীয় পৃষ্ঠপোষিত বৃত্তি প্রদান করা হয়।",
                "description_hi": "कक्षा 9वीं और 10वीं में नियमित रूप से पढ़ रहे एससी, एसटी और ओबीसी छात्र-छात्राओं को विद्यालयी शिक्षा पूरी करने हेतु आर्थिक संबल।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Annual Academic Allowance ₹3,500 to ₹7,000 / year + Ad-hoc Grant directly into student bank account",
                "benefit_amount_text_bn": "বার্ষিক ৩,৫০০ থেকে ৭,০০০ টাকা শিক্ষাবৃত্তি সরাসরি শিক্ষার্থীর ব্যাংক অ্যাকাউন্টে",
                "application_channels": ["National Scholarship Portal (NSP - scholarships.gov.in)", "State Scholarship Portal (OASIS)", "School Headmaster / HOI Desk"],
                "official_portal_url": "https://scholarships.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pre_matric,
            defaults={
                "min_age": 12,
                "max_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["SC", "ST", "OBC-A", "OBC-B"],
                "max_family_income": 250000.00,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Regular, full-time students enrolled in Class 1 to Class 10 (often restricted to Class 9 and 10 under revised central guidelines for certain categories) in a recognized government/aided school. Belongs to Scheduled Caste (SC), Scheduled Tribe (ST), or Other Backward Classes (OBC). Annual family income must not exceed ₹2,50,000. Must not hold another simultaneous government pre-matric scholarship.",
                "rules_summary_bn": "স্বীকৃত সরকারি বা সাহায্যপ্রাপ্ত বিদ্যালয়ে নবম/দশম শ্রেণিতে নিয়মিত পাঠরত এসসি, এসটি বা ওবিসি শ্রেণিভুক্ত শিক্ষার্থী। বার্ষিক পারিবারিক আয় ২.৫০ লক্ষ টাকার মধ্যে এবং অন্য কোনো সরকারি প্রাক-ম্যাট্রিক বৃত্তির সুবিধা গ্রহণকারী নন।"
            }
        )
        set_docs(pre_matric, [
            ("Student's Aadhaar Card", "শিক্ষার্থীর আধার কার্ড", True, "Student's Aadhaar card"),
            ("Valid Caste Certificate Issued by Competent Authority", "যথাযথ কর্তৃপক্ষ প্রদত্ত বৈধ জাতিগত শংসাপত্র", True, "Valid Caste Certificate issued by an authorized competent officer"),
            ("Family Income Certificate from BDO/SDO/Revenue Officer", "পারিবারিক আয়ের শংসাপত্র (BDO/SDO প্রদত্ত)", True, "Family Income Certificate from BDO/SDO/Revenue Officer"),
            ("Previous Year's Mark Sheet (Passing Report)", "পূর্ববর্তী শ্রেণির উত্তীর্ণ মার্কশিট", True, "Previous year's mark sheet (passing report)"),
            ("CBS-Enabled Bank Account Passbook in Student's Name", "শিক্ষার্থীর নামে CBS-সক্রিয় ব্যাঙ্ক পাসবই", True, "CBS-enabled bank account passbook in the student's name (with IFSC)"),
            ("School Enrollment Certificate / Bonafide Certificate", "স্কুল এনরোলমেন্ট বা বনফাইড শংসাপত্র", True, "School enrollment certificate / Bonafide certificate")
        ])

        # -------------------------------------------------------------
        # Scheme 70: Pre and Post Matric Scholarships for Minority Students
        # -------------------------------------------------------------
        min_schol, _ = Scheme.objects.update_or_create(
            slug="minority-pre-post-matric-scholarship",
            defaults={
                "department": minority,
                "category": "education",
                "name_en": "Pre and Post Matric Scholarships for Minority Students",
                "name_bn": "সংখ্যালঘু শিক্ষার্থীদের জন্য প্রাক ও উত্তর-ম্যাট্রিক স্কলারশিপ",
                "name_hi": "अल्पसंख्यक छात्रों हेतु प्री व पोस्ट मैट्रिक छात्रवृत्ति",
                "tagline_en": "Centrally sponsored pre & post-matric scholarship for meritorious minority students (min 50% marks in previous exam)",
                "tagline_bn": "সংখ্যালঘু সম্প্রদায়ের মেধাবী ছাত্রছাত্রীদের জন্য প্রাক ও উত্তর-ম্যাট্রিক কেন্দ্রীয় স্কলারশিপ (পূর্ববর্তী পরীক্ষায় ৫০% নম্বর আবশ্যক)",
                "tagline_hi": "अल्पसंख्यक वर्ग (मुस्लिम, ईसाई, सिख, बौद्ध, जैन, पारसी) के मेधावी छात्र-छात्राओं हेतु प्री व पोस्ट मैट्रिक छात्रवृत्ति",
                "description_en": "Centrally Sponsored Pre and Post Matric Scholarships for Minority Communities (Muslims, Christians, Sikhs, Buddhists, Jains, Parsis) provide tuition fee reimbursement and maintenance allowances to students with at least 50% marks in previous qualifying examinations, with 30% seats earmarked for female students.",
                "description_bn": "বিজ্ঞাপিত সংখ্যালঘু সম্প্রদায়ের ছাত্রছাত্রীদের জন্য প্রাক-ম্যাট্রিক (নবম ও দশম শ্রেণি, পারিবারিক আয় ১ লক্ষের মধ্যে) এবং উত্তর-ম্যাট্রিক (একাদশ শ্রেণি থেকে পিএইচডি, পারিবারিক আয় ২ লক্ষের মধ্যে) স্তরে পড়াশোনার সরকারি অনুদান।",
                "description_hi": "अल्पसंख्यक विद्यार्थियों की माध्यमिक व उच्च शिक्षा हेतु छात्रवृत्ति (कक्षा 9-10 हेतु आय सीमा ₹1 लाख; 11वीं से पीएचडी हेतु आय सीमा ₹2 लाख; न्यूनतम 50% अंक अनिवार्य)।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "Course Fee Reimbursement + Maintenance Allowance: Pre-Matric (up to ₹10,000/yr), Post-Matric (up to ₹20,000/yr)",
                "benefit_amount_text_bn": "কোর্স ফি ফেরত + রক্ষণাবেক্ষণ ভাতা: প্রাক-ম্যাট্রিক (১০,০০০ টাকা পর্যন্ত), উত্তর-ম্যাট্রিক (২০,০০০ টাকা পর্যন্ত/বছর)",
                "application_channels": ["National Scholarship Portal (NSP - scholarships.gov.in)", "State Minority Portal (Aikyashree/WBMDFC)", "School / College Head of Institution"],
                "official_portal_url": "https://scholarships.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=min_schol,
            defaults={
                "min_age": 13,
                "gender_allowed": "all",
                "caste_categories": ["Minority"],
                "max_family_income": 200000.00,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Students belonging to notified minority communities (Muslims, Christians, Sikhs, Buddhists, Jains, and Parsis). Pre-Matric: Enrolled in Classes 9 and 10 in recognized institutions with at least 50% marks in previous final exams; annual family income not exceeding ₹1,00,000. Post-Matric: Enrolled in Class 11, Class 12, technical/vocational, UG, PG, or Ph.D. courses with at least 50% marks in previous exams; annual family income not exceeding ₹2,00,000. At least 30% of scholarship seats are earmarked for female students.",
                "rules_summary_bn": "বিজ্ঞাপিত সংখ্যালঘু সম্প্রদায়ের (মুসলিম, খ্রিস্টান, শিখ, বৌদ্ধ, জৈন ও পার্সি) শিক্ষার্থী। প্রাক-ম্যাট্রিক: নবম ও দশম শ্রেণি, পূর্ববর্তী পরীক্ষায় ন্যূনতম ৫০% নম্বর, পারিবারিক আয় ১ লক্ষ টাকার মধ্যে। উত্তর-ম্যাট্রিক: একাদশ শ্রেণি থেকে পিএইচডি, ৫০% নম্বর, পারিবারিক আয় ২ লক্ষ টাকার মধ্যে। ৩০% আসন ছাত্রীদের জন্য সংরক্ষিত।"
            }
        )
        set_docs(min_schol, [
            ("Aadhaar Card", "আধার কার্ড", True, "Aadhaar card"),
            ("Self-Declaration of Minority Community by Student/Parent", "সংখ্যালঘু সম্প্রদায়ের স্বঘোষণাপত্র", True, "Self-declaration of minority community by student/parent"),
            ("Family Income Certificate from Competent State Revenue Authority", "পারিবারিক আয়ের শংসাপত্র (রাজস্ব কর্তৃপক্ষ কর্তৃক প্রদত্ত)", True, "Family Income Certificate from competent state revenue authority"),
            ("Mark Sheet of Previous Final Examination (50% Marks or Higher)", "পূর্ববর্তী পরীক্ষার মার্কশিট (ন্যূনতম ৫০% নম্বর)", True, "Mark sheet of the previous final qualifying examination with 50% marks or higher"),
            ("Fee Receipt and Institutional Bonafide Certificate", "কোর্সের ফি রশিদ ও প্রাতিষ্ঠানিক বনফাইড শংসাপত্র", True, "Fee receipt and Institutional Bonafide Certificate"),
            ("Active Aadhaar-Linked Savings Bank Account Passbook", "শিক্ষার্থীর সক্রিয় আধার-সংযুক্ত সেভিংস ব্যাঙ্ক পাসবই", True, "Active Aadhaar-linked savings bank account passbook")
        ])

        # -------------------------------------------------------------
        # Scheme 71: Prime Minister’s Employment Generation Programme (PMEGP)
        # -------------------------------------------------------------
        pmegp, _ = Scheme.objects.update_or_create(
            slug="pmegp",
            defaults={
                "department": msme,
                "category": "youth",
                "name_en": "Prime Minister’s Employment Generation Programme (PMEGP)",
                "name_bn": "প্রধানমন্ত্রীর কর্মসংস্থান সৃষ্টি কর্মসূচি (PMEGP)",
                "name_hi": "प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)",
                "tagline_en": "Credit-linked bank subsidy up to 35% for new micro-enterprises (up to ₹50 Lakh manufacturing, ₹20 Lakh services)",
                "tagline_bn": "নতুন ক্ষুদ্র উদ্যোগ স্থাপনে ৩৫% পর্যন্ত সরকারি মার্জিন মানি ভর্তুকি (উৎপাদনে ৫০ লাখ ও সেবায় ২০ লাখ টাকা পর্যন্ত প্রকল্প)",
                "tagline_hi": "नए सूक्ष्म उद्यमों की स्थापना हेतु 35% तक बैंक लोन सब्सिडी (विनिर्माण में ₹50 लाख, सेवा क्षेत्र में ₹20 लाख तक)",
                "description_en": "PMEGP is a major credit-linked subsidy programme aimed at generating self-employment through micro-enterprises in non-farm sectors, providing bank-financed projects up to ₹50 Lakh for manufacturing and ₹20 Lakh for services with 15%–35% margin money subsidy directly from the government.",
                "description_bn": "স্বনির্ভরতা ও কর্মসংস্থান সৃষ্টির লক্ষ্যে উৎপাদন ক্ষেত্রে ৫০ লক্ষ টাকা এবং পরিষেবা ক্ষেত্রে ২০ লক্ষ টাকা পর্যন্ত ব্যাংক ঋণের ওপর ১৫% থেকে ৩৫% সরকারি ভর্তুকি (মার্জিন মানি) প্রদান করা হয়।",
                "description_hi": "स्वरोजगार को बढ़ावा देने हेतु सूक्ष्म विनिर्माण उद्योग के लिए ₹50 लाख और सेवा उद्योग के लिए ₹20 लाख तक बैंक ऋण पर 35% तक सरकारी सब्सिडी।",
                "benefit_type": "annual_grant",
                "benefit_amount_text_en": "Margin Money Subsidy up to 35% on Bank Loans: up to ₹50 Lakh (Manufacturing) & up to ₹20 Lakh (Services)",
                "benefit_amount_text_bn": "ব্যাংক ঋণের ওপর ৩৫% পর্যন্ত সরকারি মার্জিন মানি ভর্তুকি: উৎপাদন শিল্পে ₹৫০ লক্ষ এবং পরিষেবা ক্ষেত্রে ₹২০ লক্ষ পর্যন্ত",
                "application_channels": ["KVIC PMEGP e-Portal (kviconline.gov.in)", "District Industries Centre (DIC)", "Khadi and Village Industries Board (KVIB)"],
                "official_portal_url": "https://www.kviconline.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=pmegp,
            defaults={
                "min_age": 18,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Any individual aged 18 years or above. Educational qualification: At least Class 8 pass for projects costing above ₹10 lakh in manufacturing or above ₹5 lakh in business/services. Available for new micro-enterprises (existing units or units that received subsidies under other central/state schemes are not eligible). Project limits: Up to ₹50 lakh for manufacturing and up to ₹20 lakh for service sectors.",
                "rules_summary_bn": "যেকোনো ভারতীয় নাগরিক বয়স ১৮ বছর বা তদূর্ধ্ব। শিক্ষাগত যোগ্যতা: উৎপাদন ক্ষেত্রে ১০ লক্ষ টাকার বেশি এবং পরিষেবা ক্ষেত্রে ৫ লক্ষ টাকার বেশি প্রকল্পে কমপক্ষে অষ্টম শ্রেণি উত্তীর্ণ হতে হবে। কেবল নতুন ক্ষুদ্র উদ্যোগের জন্য প্রযোজ্য।"
            }
        )
        set_docs(pmegp, [
            ("Aadhaar Card and PAN Card", "আধার কার্ড ও প্যান কার্ড", True, "Aadhaar card and PAN card"),
            ("Educational Qualification Certificates (Min Class 8 Pass Proof)", "শিক্ষাগত যোগ্যতার শংসাপত্র (ন্যূনতম অষ্টম শ্রেণি পাস)", True, "Educational qualification mark sheets / certificates (minimum 8th standard pass proof)"),
            ("Detailed Project Report (DPR) with Capital & Working Capital Breakdown", "বিশদ প্রকল্প রিপোর্ট (DPR)", True, "Detailed Project Report (DPR) including breakdown of capital expenditure and working capital"),
            ("Caste / Special Category Certificate", "জাতিগত / বিশেষ ক্যাটাগরি শংসাপত্র (উচ্চতর ভর্তুকির জন্য)", False, "Caste / Special Category Certificate (SC/ST/OBC/Women/Ex-servicemen/PH) for higher subsidy tier (up to 35%)"),
            ("EDP Training Completion Certificate", "উদ্যোক্তা উন্নয়ন প্রশিক্ষণ (EDP) শংসাপত্র", True, "EDP training completion certificate (can also be completed online post in-principle approval)")
        ])


        # -------------------------------------------------------------
        # Scheme 27: Annapurna Yojana (Women Financial Assistance 2026)
        # -------------------------------------------------------------
        annapurna_sch, _ = Scheme.objects.update_or_create(
            slug="annapurna-yojana",
            defaults={
                "department": wcd,
                "category": "women",
                "name_en": "Annapurna Yojana (Women Financial Assistance Scheme)",
                "name_bn": "অন্নপূর্ণা যোজনা (মহিলাদের মাসিক আর্থিক সহায়তা)",
                "name_hi": "अन्नपूर्णा योजना (महिलाओं के लिए मासिक वित्तीय सहायता)",
                "tagline_en": "Monthly financial assistance of ₹3,000 for eligible women residing in West Bengal (2026 Notification)",
                "tagline_bn": "পশ্চিমবঙ্গের যোগ্য মহিলাদের জন্য মাসিক ৩,০০০ টাকা সরাসরি ব্যাংক একাউন্টে আর্থিক সহায়তা (২০২৬ বিজ্ঞপ্তি)",
                "tagline_hi": "पश्चिम बंगाल की पात्र महिलाओं के लिए प्रति माह ₹3,000 सीधी बैंक वित्तीय सहायता (2026 अधिसूचना)",
                "description_en": "Annapurna Yojana provides monthly financial assistance of Rs. 3,000 directly into the Aadhaar-linked single bank account of eligible resident women aged 25-60 years through the West Bengal Social Registry portal, excluding permanent government employees, regular pension holders, and income-tax payers.",
                "description_bn": "পশ্চিমবঙ্গ সামাজিক রেজিস্ট্রি পোর্টালের মাধ্যমে ২৫-৬০ বছর বয়সী যোগ্য স্থায়ী মহিলা বাসিন্দাদের একক আধার-সংযুক্ত ব্যাংক একাউন্টে প্রতি মাসে ৩,০০০ টাকা আর্থিক সহায়তা প্রদান করা হয় (সরকারি কর্মচারী, পেনশনভোগী ও আয়করদাতাগণ ব্যতীত)।",
                "description_hi": "पश्चिम बंगाल सामाजिक रजिस्ट्री पोर्टल के माध्यम से 25-60 वर्ष की पात्र महिला निवासियों के आधार-लिंक्ड बैंक खाते में प्रति माह ₹3,000 की वित्तीय सहायता सीधे डीबीटी द्वारा प्रदान की जाती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹3,000 / month (Direct DBT to Aadhaar-Linked Bank Account)",
                "benefit_amount_text_bn": "মাসিক ৩,০০০ টাকা (আধার-সংযুক্ত ব্যাংক একাউন্টে সরাসরি DBT)",
                "application_channels": ["Social Registry Portal", "Duare Sarkar Camp", "BDO Office (Rural)", "SDO Office (Urban)"],
                "official_portal_url": "https://socialregistry.wb.gov.in/"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=annapurna_sch,
            defaults={
                "min_age": 25,
                "max_age": 60,
                "gender_allowed": "female",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Female applicant aged 25-60 years residing in West Bengal with an Aadhaar-linked bank account in her own name. Must not be a permanent government employee, regular pension/salary recipient from govt bodies, or an income-tax payer. Verification by authorised govt officials required.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্থায়ী বাসিন্দা ২৫-৬০ বছর বয়সী মহিলা আবেদনকারী, যাঁদের নিজস্ব আধার-সংযুক্ত ব্যাংক একাউন্ট রয়েছে। স্থায়ী সরকারি চাকরিজীবী, সরকারি বেতন/পেনশন প্রাপক বা আয়করদাতা হওয়া চলবে না। দায়িত্বপ্রাপ্ত সরকারি আধিকারিক দ্বারা যাচাইকরণ আবশ্যক।"
            }
        )
        set_docs(annapurna_sch, [
            ("Aadhaar Card (Aadhaar-Linked for DBT)", "আধার কার্ড (ব্যাংক DBT সংযুক্ত)", True, "Linked with bank account for Direct Benefit Transfer"),
            ("Proof of Residence in West Bengal", "পশ্চিমবঙ্গের স্থায়ী বাসিন্দার প্রমাণপত্র", True, "Voter Card / Digital Ration Card / Residential Certificate"),
            ("Bank Passbook / Cancelled Cheque", "ব্যাংক পাসবইয়ের প্রথম পাতার প্রতিলিপি", True, "Single-operated bank account in applicant's own name with IFSC"),
            ("Self-Declaration Form", "স্বঘোষণাপত্র (আয়কর ও সরকারি চাকরি না থাকার)", True, "Declaration certifying not a permanent govt employee, non-pensioner, and non-taxpayer"),
            ("Swasthya Sathi Card / Digital Ration Card", "স্বাস্থ্য সাথী কার্ড / ডিজিটাল রেশন কার্ড", True, "Family level identity verification"),
            ("Passport Size Photograph", "পাসপোর্ট মাপের রঙিন ছবি", True, "Recent photograph for verification and portal profile")
        ])

        # -------------------------------------------------------------
        # Scheme 28: Banglar Yuba Sathi / Yuvasree (Labour Dept)
        # -------------------------------------------------------------
        labour, _ = Department.objects.get_or_create(
            code="labour",
            defaults={
                "name_en": "Labour Department",
                "name_bn": "শ্রম দপ্তর",
                "name_hi": "श्रम विभाग",
                "portal_url": "https://employmentbankwb.gov.in/",
                "helpline": "033-2237-6401"
            }
        )
        yuvasree_sch, _ = Scheme.objects.update_or_create(
            slug="banglar-yuba-sathi",
            defaults={
                "department": labour,
                "category": "youth",
                "name_en": "Banglar Yuba Sathi / Yuvasree (Employment Bank Assistance)",
                "name_bn": "বাংলার যুব সাথী / যুবশ্রী (এমপ্লয়মেন্ট ব্যাংক আর্থিক সহায়তা)",
                "name_hi": "बांगलार युवा साथी / युवाश्री (रोजगार बैंक वित्तीय सहायता)",
                "tagline_en": "Monthly unemployment DBT grant of ₹1,500 for enrolled jobseekers in Employment Bank",
                "tagline_bn": "এমপ্লয়মেন্ট ব্যাংকে নথিভুক্ত কর্মপ্রার্থীদের জন্য মাসিক ১,৫০০ টাকা বেকার ভাতা অনুদান",
                "tagline_hi": "रोजगार बैंक में पंजीकृत नौकरी तलाशने वालों के लिए ₹1,500 प्रति माह बेरोजगारी डीबीटी सहायता",
                "description_en": "Banglar Yuba Sathi (Yuvasree) provides financial assistance of Rs. 1,500 per month to registered unemployed youth of West Bengal who have passed at least Class 8 and enrolled in the Employment Bank portal.",
                "description_bn": "পশ্চিমবঙ্গের বেকার যুবক-যুবতীদের চাকরির প্রস্তুতি ও দক্ষতা বৃদ্ধির জন্য প্রতি মাসে ১,৫০০ টাকা আর্থিক অনুদান সরাসরি ব্যাংক একাউন্টে দেওয়া হয় (ন্যূনতম অষ্টম শ্রেণী উত্তীর্ণ)।",
                "description_hi": "पश्चिम बंगाल के पंजीकृत बेरोजगार युवाओं को नौकरी की तैयारी और कौशल विकास के लिए प्रति माह ₹1,500 की वित्तीय सहायता सीधे बैंक खाते में दी जाती है।",
                "benefit_type": "monthly_dbt",
                "benefit_amount_text_en": "₹1,500 / month (Direct DBT to Bank Account)",
                "benefit_amount_text_bn": "মাসিক ১,৫০০ টাকা (সরাসরি ব্যাংক একাউন্টে DBT)",
                "application_channels": ["Employment Bank WB Portal", "Sub-Divisional Employment Exchange", "Duare Sarkar Camp"],
                "official_portal_url": "https://employmentbankwb.gov.in/"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=yuvasree_sch,
            defaults={
                "min_age": 18,
                "max_age": 45,
                "gender_allowed": "all",
                "caste_categories": ["General", "SC", "ST", "OBC-A", "OBC-B", "Minority"],
                "rules_summary_en": "Jobseeker enrolled in Employment Bank WB, age 18-45 years, minimum Class 8 pass, unemployed, resident of West Bengal.",
                "rules_summary_bn": "এমপ্লয়মেন্ট ব্যাংকে নথিভুক্ত, বয়স ১৮-৪৫ বছর, ন্যূনতম অষ্টম শ্রেণী পাস, বেকার এবং পশ্চিমবঙ্গের স্থায়ী বাসিন্দা।"
            }
        )
        set_docs(yuvasree_sch, [
            ("Employment Bank Registration Slip (EB-No)", "এমপ্লয়মেন্ট ব্যাংক এনরোলমেন্ট স্লিপ", True, "Enrolment copy with valid EB Registration Number"),
            ("Aadhaar Card (Linked with Bank DBT)", "আধার কার্ড (ব্যাংক DBT সংযুক্ত)", True, "Proof of Identity and DBT enablement"),
            ("Educational Qualification Certificate", "শিক্ষাগত যোগ্যতার প্রমাণপত্র", True, "Class 8 Marksheet / Madhyamik Admit Card or Certificate"),
            ("Bank Passbook / Cancelled Cheque", "ব্যাংক পাসবইয়ের প্রথম পাতার প্রতিলিপি", True, "Single account in applicant's name with IFSC code"),
            ("Proof of Residence", "পশ্চিমবঙ্গের স্থায়ী বাসিন্দার প্রমাণ", True, "Voter Card / Digital Ration Card / Residential Certificate"),
            ("Unemployment Self-Declaration (Annexure-I)", "বেকারত্বের স্বঘোষণাপত্র (অ্যানেক্সার-১)", True, "Mandatory format under Yuvasree")
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

                # -------------------------------------------------------------
        # Scheme: West Bengal Sikshashree Scheme
        # -------------------------------------------------------------
        siksha, _ = Scheme.objects.update_or_create(
            slug="sikshashree",
            defaults={
                "department": bcwd,
                "category": "education",
                "name_en": "West Bengal Sikshashree Scheme",
                "name_bn": "শিক্ষাশ্রী প্রকল্প",
                "name_hi": "पश्चिम बंगाल शिक्षाश्री योजना",
                "tagline_en": "Day-scholarship of ₹800 per annum for SC/ST students of Class 5 to 8",
                "tagline_bn": "পঞ্চম থেকে অষ্টম শ্রেণীর তপশিলি জাতি ও উপজাতি শিক্ষার্থীদের জন্য বার্ষিক ৮০০ টাকা বৃত্তি",
                "tagline_hi": "कक्षा 5 से 8 के अनुसूचित जाति व जनजाति के छात्रों हेतु ₹800 वार्षिक छात्रवृत्ति",
                "description_en": "Sikshashree is a flagship scheme providing financial assistance of Rs. 800 per annum to Scheduled Caste (SC) and Scheduled Tribe (ST) students studying in Classes V to VIII to curb school dropout rates.",
                "description_bn": "পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত তপশিলি জাতি ও উপজাতি শিক্ষার্থীদের স্কুলছুট কমাতে রাজ্য সরকারের বার্ষিক ৮০০ টাকার বিশেষ অনুদান।",
                "description_hi": "कक्षा 5 से 8 में पढ़ने वाले एससी/एसटी वर्ग के छात्रों के स्कूल छोड़ने की दर रोकने के लिए ₹800 की वार्षिक वित्तीय सहायता।",
                "benefit_type": "scholarship",
                "benefit_amount_text_en": "₹800 per annum",
                "benefit_amount_text_bn": "বার্ষিক ৮০০ টাকা",
                "application_channels": ["Through School (Banglar Shiksha Portal)", "BDO / SDO Office"],
                "official_portal_url": "https://oasis.gov.in"
            }
        )
        SchemeEligibility.objects.update_or_create(
            scheme=siksha,
            defaults={
                "min_age": 9,
                "max_age": 16,
                "gender_allowed": "all",
                "caste_categories": ["SC", "ST"],
                "max_family_income": 250000.00,
                "requires_single_bank_account": False,
                "requires_aadhaar_dbt_linking": True,
                "rules_summary_en": "Regular SC/ST student of Class 5 to 8 in recognized West Bengal schools with annual family income up to ₹2.50 lakh.",
                "rules_summary_bn": "পশ্চিমবঙ্গের স্বীকৃত বিদ্যালয়ে ৫ম থেকে ৮ম শ্রেণীতে পাঠরত SC/ST শিক্ষার্থী, পারিবারিক বার্ষিক আয় ২.৫ লক্ষ টাকার নিচে।"
            }
        )
        set_docs(siksha, [
            ("Student Aadhaar Card", "শিক্ষার্থীর আধার কার্ড", True, "Mandatory for identification"),
            ("Valid SC/ST Caste Certificate", "বৈধ তপশিলি জাতি / উপজাতি শংসাপত্র", True, "Issued by SDO / competent authority or father's certificate"),
            ("Family Income Certificate", "পারিবারিক আয়ের শংসাপত্র", True, "Issued by BDO / SDO / Gazetted Officer (annual income <= ₹2.5 Lakh)"),
            ("School Admission / Banglar Shiksha ID Proof", "বিদ্যালয়ে ভর্তির প্রমাণ / স্টুডেন্ট আইডি", True, "Banglar Shiksha student code verification"),
            ("Bank Account Passbook Copy", "ব্যাঙ্ক অ্যাকাউন্ট পাসবই", True, "Aadhaar-linked active savings account in student's name")
        ])


        self.stdout.write(self.style.SUCCESS("Successfully seeded comprehensive 2026 West Bengal schemes!"))
