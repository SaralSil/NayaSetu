"""
NayaSetu AI Chatbot Assistant Service.
Dedicated AI assistant for West Bengal Government Schemes, Scholarships,
Document Checklists, Official Portals, and Website Navigation.
Full multi-lingual support: English, Bengali (বাংলা), and Hindi (हिंदी).
"""
import os
import json
import logging
import re
from django.conf import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are "NayaSetu AI" (नया सेतु AI / ন্যায়সেতু AI) — an intelligent, versatile, compassionate citizen rights and government welfare schemes assistant for the citizens of West Bengal.

CRITICAL IDENTITY RULES:
1. NEVER identify yourself as Gemini, Google, OpenAI, ChatGPT, Claude, or any third-party AI company.
2. If asked "Who are you?", "What is your name?", "তোমার নাম কি?", "तुम्हारा नाम क्या है?", or similar, ALWAYS state clearly that you are "NayaSetu AI" (नया सेतु AI / ন্যায়সেতু AI), the dedicated AI assistant for the NayaSetu platform.

STRICT LANGUAGE MATCHING RULES:
1. If the user asks in English, or requests to speak/reply in English ("talk in english", "speak in english", "english please", etc.), you MUST respond ENTIRELY in natural, fluent English.
2. If the user asks in Bengali (বাংলা), or requests Bengali ("বাংলায় কথা বলো", "বাংলায় বলো", "কথা বাংলায় বলো", etc.), you MUST respond ENTIRELY in clear, respectful Bengali (বাংলা).
3. If the user asks in Hindi, or requests Hindi ("हिंदी में बात करो", "हिंदी में बोलो", etc.), you MUST respond in respectful Hindi.
4. If the user switches language at any point, acknowledge the switch politely in the new language and proceed exclusively in that language.

COMPREHENSIVE AI CAPABILITIES (LIKE CHATGPT):
1. You can answer ANY user query: greetings, general knowledge, explanations, advice, drafting letters, calculations, and general conversations.
2. For West Bengal government schemes and scholarships, provide complete, accurate, structured information:
   - Scheme benefits and grant amounts.
   - Exact eligibility criteria (age, gender, income, caste).
   - Mandatory document checklist (highlighting single bank account vs joint account, Aadhaar-NPCI DBT linking).
   - Official West Bengal Government portal link (e.g. [Official Portal](url)).
   - Where and how to apply (Duare Sarkar camps, BDO office, SDO, ADA office, school/college).
3. For NayaSetu website guidance:
   - Where to search: Top 'Ask NyayaSetu AI' search bar or topic chips.
   - Where to check eligibility: 'যোগ্যতা যাচাই' (Eligibility Wizard).
   - Where to view schemes & documents: 'প্রকল্প নির্দেশিকা' (Schemes Directory).
   - Where to submit complaints / draft legal petitions: 'অভিযোগ প্রস্তুতি' (Grievance Drafter).
   - Where to explain SMS / rejection notices: 'নোটিশ / রসিদ বুঝুন' (Notice Explainer).
4. Formatting: Use neat Markdown with bullet points, bold headers, and clean emojis for mobile readability.
"""

# Multilingual Knowledge Base for West Bengal Government Schemes
SCHEMES_KNOWLEDGE = {
    "lakshmir_bhandar": {
        "title_en": "Annapurna Bhandar / Lakshmir Bhandar (2026 Enhanced)",
        "title_bn": "অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার (২০২৬ সংশোধিত)",
        "title_hi": "अन्नपूर्णा भंडार / लक्ष्मी भंडार योजना (2026 संशोधित)",
        "benefit_en": "₹3,000/month direct DBT bank transfer for all eligible women (₹36,000/year)",
        "benefit_bn": "সকল যোগ্য মহিলার জন্য প্রতি মাসে ₹৩,০০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি (বাৎসরিক ₹৩৬,০০০)",
        "benefit_hi": "सभी पात्र महिलाओं के लिए ₹3,000/माह सीधे बैंक खाते में DBT (वार्षिक ₹36,000)",
        "eligibility_en": "Female residents of West Bengal aged 25 to 60 years. Government employees & pension recipients are not eligible.",
        "eligibility_bn": "পশ্চিমবঙ্গের ২৫ থেকে ৬০ বছর বয়সী স্থায়ী মহিলা বাসিন্দা। সরকারি চাকুরীজীবী ও পেনশন প্রাপক ব্যতীত।",
        "eligibility_hi": "पश्चिम बंगाल की 25 से 60 वर्ष की महिला नागरिक। सरकारी कर्मचारी/पेंशनधारक अपात्र हैं।",
        "documents_en": [
            "Swasthya Sathi Card (Health Card) - Xerox copy (Female head of family)",
            "Aadhaar Card - Xerox copy of applicant woman",
            "Single Savings Bank Account Passbook (Joint accounts strictly NOT allowed)",
            "Active Aadhaar-NPCI DBT Seeding status in the bank account",
            "Recent Passport Size Color Photograph (1 copy)",
            "Mobile number linked with Aadhaar"
        ],
        "documents_bn": [
            "স্বাস্থ্য সাথী কার্ডের জেরক্স কপি (মহিলার নিজের বা পরিবারের)",
            "আবেদনকারী মহিলার আধার কার্ডের জেরক্স",
            "একক সেভিংস ব্যাঙ্ক পাসবই (জয়েন্ট অ্যাকাউন্ট সম্পূর্ণ নিষিদ্ধ)",
            "ব্যাঙ্ক অ্যাকাউন্টে আধার-NPCI DBT সক্রিয় থাকতে হবে",
            "১ কপি পাসপোর্ট সাইজ রঙিন ছবি",
            "আধারের সাথে লিঙ্ক করা মোবাইল নম্বর"
        ],
        "documents_hi": [
            "स्वास्थ्य साथी कार्ड की ज़ेरॉक्स कॉपी",
            "महिला का आधार कार्ड",
            "सिंगल बैंक बचत खाता पासबुक (जॉइंट खाता बिल्कुल मान्य नहीं है)",
            "बैंक खाते में आधार-NPCI DBT एक्टिव होना अनिवार्य",
            "1 पासपोर्ट साइज रंगीन फोटो",
            "आधार से लिंक मोबाइल नंबर"
        ],
        "portal_url": "https://socialsecurity.wb.gov.in",
        "portal_name": "WB Social Security Portal",
        "where_to_apply_en": "Duare Sarkar Camps or local BDO Office (Rural) / Municipality / SDO Office (Urban)",
        "where_to_apply_bn": "দুয়ারে সরকার ক্যাম্প অথবা স্থানীয় বিডিও (BDO) অফিস / মিউনিসিপ্যালিটি অফিস",
        "where_to_apply_hi": "दुयरे सरकार कैंप या स्थानीय BDO / नगर पालिका कार्यालय",
        "modal_target": "schemes-and-docs"
    },
    "wb_yuva_shakti": {
        "title_en": "West Bengal Yuva Shakti Yojana (Yuva Shakti Bharosa Card)",
        "title_bn": "পশ্চিমবঙ্গ যুব শক্তি যোজনা (যুব শক্তি ভরসা কার্ড)",
        "title_hi": "पश्चिम बंगाल युवा शक्ति योजना (युवा शक्ति भरोसा कार्ड)",
        "benefit_en": "₹2,000/month (10th/12th pass) or ₹3,000/month (Graduates) financial stipend + free industry skill training",
        "benefit_bn": "মাধ্যমিক/উচ্চমাধ্যমিক পাশ যুবকদের জন্য মাসিক ₹২,০০০ এবং স্নাতকদের জন্য ₹৩,০০০ আর্থিক ভাতা + বিনামূল্যে দক্ষতা প্রশিক্ষণ",
        "benefit_hi": "10वीं/12वीं पास को ₹2,000/माह व स्नातकों को ₹3,000/माह बेरोजगारी सहायता व निःशुल्क कौशल विकास प्रशिक्षण",
        "eligibility_en": "Resident youth of West Bengal aged 21 to 40 years, passed Class 10/12 or Graduation, enrolled in Employment Bank.",
        "eligibility_bn": "পশ্চিমবঙ্গের ২১ থেকে ৪০ বছর বয়সী বেকার যুবক-যুবতী, মাধ্যমিক/উচ্চমাধ্যমিক বা স্নাতক উত্তীর্ণ, এমপ্লয়মেন্ট ব্যাংকে নথিভুক্ত।",
        "eligibility_hi": "पश्चिम बंगाल के 21 से 40 वर्ष के बेरोजगार युवा, 10वीं/12वीं या स्नातक उत्तीर्ण, रोजगार बैंक में पंजीकृत।",
        "documents_en": [
            "Class 10 / 12 / Graduation Marksheets & Pass Certificates",
            "Employment Bank Registration Number / Yuvasree ID",
            "Aadhaar Card",
            "Single Savings Bank Account Passbook",
            "Active Aadhaar-NPCI DBT seeding proof",
            "Recent passport size photo"
        ],
        "documents_bn": [
            "মাধ্যমিক / উচ্চমাধ্যমিক / স্নাতক পাশের মার্কশিট ও সার্টিফিকেট",
            "এমপ্লয়মেন্ট ব্যাঙ্ক রেজিস্ট্রেশন নম্বর / যুবশ্রী আইডি",
            "আধার কার্ডের জেরক্স",
            "একক সেভিংস ব্যাঙ্ক অ্যাকাউন্টের পাসবই (IFSC স্পষ্ট)",
            "ব্যাঙ্কে আধার-NPCI DBT সক্রিয় থাকার প্রমাণ",
            "পাসপোর্ট সাইজ ছবি"
        ],
        "documents_hi": [
            "10वीं/12वीं/स्नातक अंकपत्र व प्रमाण पत्र",
            "रोजगार बैंक (Employment Bank) पंजीकरण संख्या",
            "आधार कार्ड",
            "सिंगल बैंक बचत खाता पासबुक",
            "बैंक खाते में आधार-NPCI DBT एक्टिव होना",
            "पासपोर्ट साइज फोटो"
        ],
        "portal_url": "https://yubasathi.wb.gov.in",
        "portal_name": "Yuva Shakti Official Portal",
        "where_to_apply_en": "Apply online at yubasathi.wb.gov.in or nearest District Employment Exchange",
        "where_to_apply_bn": "yubasathi.wb.gov.in পোর্টালে অথবা জেলা এমপ্লয়মেন্ট এক্সচেঞ্জে",
        "where_to_apply_hi": "yubasathi.wb.gov.in पर ऑनलाइन या जिला रोजगार कार्यालय में",
        "modal_target": "schemes-and-docs"
    },
    "ayushman_bharat": {
        "title_en": "Ayushman Bharat (AB-PMJAY) & Vay Vandana 70+",
        "title_bn": "আয়ুষ্মান ভারত (AB-PMJAY) ও বয় বন্দনা ৭০+",
        "title_hi": "आयुष्मान भारत (AB-PMJAY) व वय वंदना 70+",
        "benefit_en": "₹5 Lakh cashless hospital treatment per family/year across 29,000+ hospitals across India + Universal free ₹5 Lakh cover for all senior citizens aged 70+ regardless of income",
        "benefit_bn": "সারা ভারতের ২৯,০০০+ হাসপাতালে প্রতি পরিবার প্রতি বছর ₹৫ লাখ পর্যন্ত ক্যাশলেস চিকিৎসা + ৭০ ঊর্ধ্ব সমস্ত প্রবীণ নাগরিকদের জন্য সার্বজনীন বিনামূল্যে ₹৫ লাখের বয় বন্দনা স্বাস্থ্য কার্ড",
        "benefit_hi": "देशभर के 29,000+ अस्पतालों में प्रति परिवार ₹5 लाख तक का कैशलेस इलाज + 70 वर्ष से अधिक के सभी बुजुर्गों हेतु निःशुल्क वय वंदना कार्ड",
        "eligibility_en": "All SECC/NFSA ration card holders and all senior citizens aged 70 years and above (universal coverage without income limit).",
        "eligibility_bn": "রেশন কার্ডধারী সমস্ত পরিবার এবং ৭০ বছর বা তদূর্ধ্ব সমস্ত প্রবীণ নাগরিক (আয়সীমা নির্বিশেষে সার্বজনীন)।",
        "eligibility_hi": "राशन कार्ड धारक सभी परिवार और 70 वर्ष से अधिक के सभी वरिष्ठ नागरिक (बिना किसी आय सीमा के)।",
        "documents_en": [
            "Aadhaar Card of all family members (mandatory for biometric e-KYC)",
            "Digital Ration Card (NFSA / Khadya Sathi)",
            "Age proof for 70+ Senior Citizen (Aadhaar / Voter ID / Birth Certificate)",
            "Active mobile number linked with Aadhaar"
        ],
        "documents_bn": [
            "পরিবারের সকল সদস্যের আধার কার্ড (বায়োমেট্রিক ই-কেওয়াইসির জন্য)",
            "ডিজিটাল রেশন কার্ড",
            "৭০+ প্রবীণদের বয়সের প্রমাণপত্র (আধার বা ভোটার কার্ড)",
            "আধারের সাথে যুক্ত মোবাইল নম্বর"
        ],
        "documents_hi": [
            "परिवार के सभी सदस्यों के आधार कार्ड (ई-केवाईसी हेतु अनिवार्य)",
            "डिजिटल राशन कार्ड",
            "70+ बुजुर्गों के लिए आयु प्रमाण पत्र",
            "आधार से लिंक मोबाइल नंबर"
        ],
        "portal_url": "https://beneficiary.nha.gov.in",
        "portal_name": "Ayushman Bharat PM-JAY Portal",
        "where_to_apply_en": "Online at beneficiary.nha.gov.in, Ayushman App, or any Common Service Center (CSC)",
        "where_to_apply_bn": "beneficiary.nha.gov.in পোর্টালে, আয়ুষ্মান অ্যাপে অথবা যেকোনো CSC সেন্টারে",
        "where_to_apply_hi": "beneficiary.nha.gov.in पोर्टल, आयुष्मान ऐप या किसी भी CSC केंद्र पर",
        "modal_target": "schemes-and-docs"
    },
    "karmashree": {
        "title_en": "Karmashree (50-Day Guaranteed Wage Employment)",
        "title_bn": "কর্মশ্রী প্রকল্প (৫০ দিনের নিশ্চিত কর্মসংস্থান)",
        "title_hi": "कर्मश्री योजना (50 दिन की गारंटीड मजदूरी रोजगार)",
        "benefit_en": "50 days guaranteed wage employment per financial year for rural households at statutory daily wage (₹250+/day)",
        "benefit_bn": "গ্রামীণ পরিবারের জন্য বছরে ৫০ দিনের নিশ্চিত কাজ এবং সরাসরি ব্যাঙ্ক অ্যাকাউন্টে নির্ধারিত দৈনিক মজুরি (₹২৫০+/দিন)",
        "benefit_hi": "ग्रामीण जॉब कार्ड धारक परिवारों को प्रति वर्ष 50 दिनों का काम और सीधे खाते में दैनिक वैधानिक मजदूरी",
        "eligibility_en": "All rural households holding a valid Job Card in West Bengal willing to do unskilled manual work.",
        "eligibility_bn": "পশ্চিমবঙ্গের জব কার্ডধারী সমস্ত গ্রামীণ পরিবার যারা অদক্ষ শারীরিক কাজ করতে ইচ্ছুক।",
        "eligibility_hi": "पश्चिम बंगाल के सभी जॉब कार्ड धारक ग्रामीण परिवार जो अकुशल शारीरिक श्रम के इच्छुक हैं।",
        "documents_en": [
            "Rural Job Card (NREGA / State Job Card)",
            "Aadhaar Card",
            "Single Savings Bank Account Passbook",
            "Form 4 (Application for Work Allocation)"
        ],
        "documents_bn": [
            "গ্রামীণ জব কার্ডের জেরক্স",
            "আধার কার্ডের কপি",
            "একক সেভিংস ব্যাঙ্ক পাসবই",
            "কাজের আবেদনের ফর্ম-৪"
        ],
        "documents_hi": [
            "ग्रामीण जॉब कार्ड",
            "आधार कार्ड",
            "एकल बैंक पासबुक",
            "कार्य आवंटन आवेदन फॉर्म-4"
        ],
        "portal_url": "https://karmashree.wb.gov.in",
        "portal_name": "Karmashree Portal",
        "where_to_apply_en": "Gram Panchayat Office or Duare Sarkar Camps",
        "where_to_apply_bn": "গ্রাম পঞ্চায়েত কার্যালয় অথবা দুয়ারে সরকার ক্যাম্প",
        "where_to_apply_hi": "ग्राम पंचायत कार्यालय या दुयरे सरकार कैंप",
        "modal_target": "schemes-and-docs"
    },
    "krishak_bandhu": {
        "title_en": "Krishak Bandhu (Natun) & PM-Kisan Scheme",
        "title_bn": "কৃষক বন্ধু (নতুন) ও পিএম-কিসান প্রকল্প",
        "title_hi": "कृषक बंधु (नया) व पीएम-किसान योजना",
        "benefit_en": "Up to ₹10,000/year (₹16,000 with PM-Kisan) in Kharif & Rabi installments + ₹2,00,000 Death Benefit (age 18-60)",
        "benefit_bn": "বছরে ₹৪,০০০ থেকে ₹১০,০০০ অনুদান (পিএম-কিসানের সাথে ₹১৬,০০০) + ১৮-৬০ বছর বয়সে ₹২,০০,০০০ টাকার কৃষক মৃত্যু সহায়তা",
        "benefit_hi": "वार्षिक ₹4,000 से ₹10,000 (PM-Kisan के साथ ₹16,000) + ₹2,00,000 जीवन बीमा सहायता (18-60 वर्ष)",
        "eligibility_en": "All farmers, agricultural land owners, and recorded sharecroppers (bargadars) in West Bengal.",
        "eligibility_bn": "পশ্চিমবঙ্গের সমস্ত কৃষক, ভূমির মালিক ও নথিভুক্ত বর্গাদার।",
        "eligibility_hi": "पश्चिम बंगाल के सभी किसान, खेतिहर और दर्ज बटाईदार (recorded bargadars)।",
        "documents_en": [
            "Land Record / RoR / Porcha / Khatian in farmer's name",
            "Voter ID (EPIC) Card - Strictly mandatory for Krishak Bandhu",
            "Aadhaar Card copy",
            "Single Bank Passbook (with clear IFSC and Account number)",
            "Passport Size Photograph",
            "Bargadar registration certificate (if sharecropper)"
        ],
        "documents_bn": [
            "কৃষকের নিজের নামের জমির রেকর্ড / পরচা / খতিয়ান",
            "ভোটার আইডি (EPIC) কার্ড — কৃষক বন্ধুতে ভোটার কার্ড বাধ্যতামূলক",
            "আধার কার্ডের কপি",
            "একক ব্যাঙ্ক অ্যাকাউন্টের পাসবই (IFSC ও অ্যাকাউন্ট নম্বর স্পষ্ট)",
            "পাসপোর্ট সাইজ ছবি",
            "বর্গাদার নিবন্ধনের প্রমাণ (বর্গাদারদের ক্ষেত্রে)"
        ],
        "documents_hi": [
            "किसान के नाम का जमीन का पर्चा / खतियान (Land RoR / Porcha)",
            "वोटर कार्ड (EPIC) — कृषक बंधु में अनिवार्य है",
            "आधार कार्ड",
            "सिंगल बैंक पासबुक",
            "पासपोर्ट साइज फोटो"
        ],
        "portal_url": "https://krishakbandhu.wb.gov.in",
        "portal_name": "Krishak Bandhu Official Portal",
        "where_to_apply_en": "Block ADA (Assistant Director of Agriculture) Office, BDO Office, or Duare Sarkar Camps",
        "where_to_apply_bn": "ব্লক সহ-কৃষি অধিকর্তার (ADA) কার্যালয় অথবা দুয়ারে সরকার ক্যাম্প",
        "where_to_apply_hi": "प्रखंड कृषि कार्यालय (ADA Office) या दुयरे सरकार कैंप",
        "modal_target": "schemes-and-docs"
    },
    "bhabishyat_credit_card": {
        "title_en": "Bhabishyat Credit Card Scheme (WBBCCS)",
        "title_bn": "ভবিষ্যৎ ক্রেডিট কার্ড প্রকল্প (WBBCCS)",
        "title_hi": "भविष्य क्रेडिट कार्ड योजना (WBBCCS)",
        "benefit_en": "Collateral-free bank loan up to ₹5 Lakh for entrepreneurship with 10% state subsidy (up to ₹25,000) and 85% state credit guarantee",
        "benefit_bn": "ব্যবসা শুরুর জন্য ৫ লক্ষ টাকা পর্যন্ত ব্যাঙ্ক ঋণ, ১০% সরকারি ভরতুকি (সর্বোচ্চ ₹২৫,০০০) ও ৮৫% রাজ্য ক্রেডিট গ্যারান্টি",
        "benefit_hi": "युवाओं को नया उद्यम शुरू करने हेतु ₹5 लाख तक का बैंक लोन, 10% सरकारी सब्सिडी व राज्य गारंटी",
        "eligibility_en": "Resident youth of West Bengal aged 18 to 45 years with viable business/manufacturing/service project.",
        "eligibility_bn": "পশ্চিমবঙ্গের ১৮ থেকে ৪৫ বছর বয়সী স্থায়ী যুবক-যুবতী যাদের নতুন ব্যবসার প্রকল্প রয়েছে।",
        "eligibility_hi": "पश्चिम बंगाल के 18 से 45 वर्ष के युवा नागरिक जिनका नया व्यावसायिक प्रोजेक्ट हो।",
        "documents_en": [
            "Detailed Project Report (DPR)",
            "Aadhaar Card and PAN Card",
            "Proof of residence in West Bengal",
            "Bank statement or passbook",
            "Trade license or proposed business outline"
        ],
        "documents_bn": [
            "প্রকল্পের বিস্তারিত বিবরণ (DPR)",
            "আধার কার্ড ও প্যান কার্ড",
            "পশ্চিমবঙ্গের স্থায়ী বসবাসের প্রমাণপত্র",
            "ব্যাঙ্ক পাসবই বা স্টেটমেন্ট",
            "ট্রেড লাইসেন্স বা ব্যবসার পরিকল্পনা"
        ],
        "documents_hi": [
            "विस्तृत प्रोजेक्ट रिपोर्ट (DPR)",
            "आधार कार्ड व पैन कार्ड",
            "निवास प्रमाण पत्र",
            "बैंक पासबुक",
            "ट्रेड लाइसेंस / व्यापार योजना"
        ],
        "portal_url": "https://bccs.wb.gov.in",
        "portal_name": "Bhabishyat Credit Card Portal",
        "where_to_apply_en": "Apply online at bccs.wb.gov.in or District Industries Centre (DIC) / BDO Office",
        "where_to_apply_bn": "bccs.wb.gov.in পোর্টালে অথবা জেলা শিল্প কেন্দ্র (DIC) বা বিডিও অফিসে",
        "where_to_apply_hi": "bccs.wb.gov.in पर ऑनलाइन या जिला उद्योग केंद्र (DIC) में",
        "modal_target": "schemes-and-docs"
    },
    "banglar_awas": {
        "title_en": "Banglar Awas Yojana / Paschim Banga Awas",
        "title_bn": "বাংলার আবাস যোজনা / পশ্চিমবঙ্গ আবাস",
        "title_hi": "बांगलার आवास योजना (पक्का मकान निर्माण)",
        "benefit_en": "₹1,20,000 financial grant in 3 installments (₹60,000 + ₹50,000 + ₹10,000) directly credited to bank account for building pucca house",
        "benefit_bn": "পাকা বাড়ি তৈরির জন্য সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ₹১,২০,০০০ আর্থিক অনুদান ৩টি কিস্তিতে (৬০,০০০ + ৫০,০০০ + ১০,০০০ টাকা)",
        "benefit_hi": "पक्का मकान बनाने के लिए ₹1,20,000 की वित्तीय सहायता सीधे बैंक खाते में 3 किस्तों में",
        "eligibility_en": "Rural houseless families or those living in kutcha/dilapidated houses in West Bengal as per official survey list.",
        "eligibility_bn": "পশ্চিমবঙ্গের গ্রামীণ গৃহহীন বা কাঁচা ঘরে বসবাসকারী পরিবার যাদের নাম সমীক্ষা তালিকায় রয়েছে।",
        "eligibility_hi": "पश्चिम बंगाल के ग्रामीण बेघर या कच्चे मकानों में रहने वाले पात्र परिवार।",
        "documents_en": [
            "Aadhaar Card of all family members",
            "Ration Card",
            "Land ownership paper (RoR / Deed / Pradhan certificate)",
            "Single Bank Passbook with active DBT",
            "Geo-tagged photo of existing kutcha house"
        ],
        "documents_bn": [
            "পরিবারের সকল সদস্যের আধার কার্ড",
            "রেশন কার্ডের কপি",
            "জমির মালিকানার প্রমাণ (পরচা / দলিল / প্রধান সার্টিফিকেট)",
            "একক ব্যাঙ্ক অ্যাকাউন্টের পাসবই (ডিবিটি সক্রিয়)",
            "বর্তমান কাঁচা ঘরের ছবি"
        ],
        "documents_hi": [
            "परिवार के सभी सदस्यों के आधार कार्ड",
            "राशन कार्ड",
            "जमीन का पर्चा / दस्तावेज",
            "एकल बैंक पासबुक",
            "वर्तमान कच्चे घर का फोटो"
        ],
        "portal_url": "https://wbprd.gov.in",
        "portal_name": "P&RD Department Portal",
        "where_to_apply_en": "Gram Panchayat / BDO Office survey or Duare Sarkar Camps",
        "where_to_apply_bn": "গ্রাম পঞ্চায়েত / বিডিও অফিস অথবা দুয়ারে সরকার ক্যাম্প",
        "where_to_apply_hi": "ग्राम पंचायत / BDO कार्यालय या दुयरे सरकार कैंप",
        "modal_target": "schemes-and-docs"
    },
    "bangla_shasya_bima": {
        "title_en": "Bangla Shasya Bima (BSB Crop Insurance)",
        "title_bn": "বাংলা শস্য বীমা (BSB)",
        "title_hi": "बांग्ला शस्य बीमा (मुफ्त फसल बीमा योजना)",
        "benefit_en": "100% state government paid premium for all major crops; full compensation for flood, drought, cyclone or unseasonal rain loss",
        "benefit_bn": "সম্পূর্ণ বিনামূল্যে রাজ্য সরকার প্রদত্ত ১০০% প্রিমিয়াম; বন্যা, খরা বা শিলাবৃষ্টিতে ফসল নষ্ট হলে ব্যাঙ্ক অ্যাকাউন্টে সম্পূর্ণ ক্ষতিপূরণ",
        "benefit_hi": "किसानों के लिए 100% मुफ्त सरकारी प्रीमियम; बाढ़ या सूखे से फसल नुकसान पर पूरा मुआवजा",
        "eligibility_en": "All farmers, owner-cultivators, and tenant/bargadar farmers growing notified crops in West Bengal.",
        "eligibility_bn": "বিজ্ঞাপিত ফসল চাষকারী পশ্চিমবঙ্গের সমস্ত কৃষক, জমির মালিক ও বর্গাদার।",
        "eligibility_hi": "अधिसूचित फसल उगाने वाले पश्चिम बंगाल के सभी किसान, खेतिहर और बटाईदार।",
        "documents_en": [
            "Land RoR / Porcha / Khatian or Cultivator certificate",
            "Crop Sowing Certificate signed by Krishi Prayukti Sahayak (KPS) / Pradhan",
            "Voter ID Card",
            "Aadhaar Card",
            "Bank Passbook with clear IFSC"
        ],
        "documents_bn": [
            "জমির পরচা / খতিয়ান বা চাষের শংসাপত্র",
            "সহ-কৃষি প্রযুক্তি সহায়ক (KPS) বা প্রধানের শস্য বপন সার্টিফিকেট",
            "ভোটার আইডি কার্ড",
            "আধার কার্ড",
            "ব্যাঙ্ক পাসবই"
        ],
        "documents_hi": [
            "जमीन का पर्चा / खतियान",
            "फसल बुवाई प्रमाण पत्र (KPS या प्रधान द्वारा)",
            "वोटर कार्ड व आधार कार्ड",
            "बैंक पासबुक"
        ],
        "portal_url": "https://banglashasyabima.net",
        "portal_name": "Bangla Shasya Bima Portal",
        "where_to_apply_en": "Block ADA Office, Gram Panchayat, or banglashasyabima.net",
        "where_to_apply_bn": "ব্লক এডিএ (ADA) অফিস, গ্রাম পঞ্চায়েত বা banglashasyabima.net",
        "where_to_apply_hi": "प्रखंड कृषि कार्यालय (ADA) या banglashasyabima.net",
        "modal_target": "schemes-and-docs"
    },
    "taruner_swapno": {
        "title_en": "Taruner Swapno (Class 11 & 12 Tablet / Smartphone Scheme)",
        "title_bn": "তরুণের স্বপ্ন (ট্যাব ও স্মার্টফোন প্রকল্প)",
        "title_hi": "तरुणेर स्वप्न (टैबलेट/स्मार्टफोन अनुदान योजना)",
        "benefit_en": "One-time ₹10,000 DBT grant directly credited to student's bank account for purchasing smartphone/tablet for digital education",
        "benefit_bn": "একাদশ ও দ্বাদশ শ্রেণীর শিক্ষার্থীদের ডিজিটাল পড়াশোনার জন্য ট্যাব বা স্মার্টফোন কিনতে এককালীন ₹১০,০০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে",
        "benefit_hi": "11वीं व 12वीं के विद्यार्थियों को टैबलेट या स्मार्टफोन खरीदने हेतु ₹10,000 का एकमुश्त DBT अनुदान",
        "eligibility_en": "Regular enrolled students of Class 11 and 12 in West Bengal Government, Government-aided and Madrasah schools.",
        "eligibility_bn": "পশ্চিমবঙ্গের সরকারি, সরকার পোষিত স্কুল ও মাদ্রাসার একাদশ ও দ্বাদশ শ্রেণীতে পাঠরত নিয়মিত ছাত্র-ছাত্রী।",
        "eligibility_hi": "पश्चिम बंगाल के सरकारी व सहायता प्राप्त स्कूलों व मदरसों में 11वीं व 12वीं के नियमित छात्र।",
        "documents_en": [
            "Student Banglar Shiksha Portal Student ID",
            "Class 10 Board Marksheet and Admit Card",
            "Student's single bank passbook",
            "Aadhaar card",
            "Bonafide certificate from Head of Institution"
        ],
        "documents_bn": [
            "বাংলার শিক্ষা পোর্টালের স্টুডেন্ট আইডি (Student ID)",
            "মাধ্যমিকের মার্কশিট ও এডমিট কার্ড",
            "ছাত্র/ছাত্রীর নিজস্ব একক ব্যাঙ্ক পাসবই",
            "আধার কার্ডের কপি",
            "প্রধান শিক্ষকের বোনাফাইড শংসাপত্র"
        ],
        "documents_hi": [
            "बांग्लार शिक्षा स्टूडेंट आईडी",
            "10वीं बोर्ड मार्कशीट व एडमिट कार्ड",
            "छात्र का एकल बैंक पासबुक",
            "आधार कार्ड",
            "स्कूल संस्था प्रधान का प्रमाण पत्र"
        ],
        "portal_url": "https://school.banglarshiksha.gov.in",
        "portal_name": "Banglar Shiksha Portal",
        "where_to_apply_en": "Directly through the enrolled school/madrasah portal verification",
        "where_to_apply_bn": "ছাত্র-ছাত্রী যে স্কুলে পড়ছে সেই স্কুলের প্রধান শিক্ষকের মাধ্যমে",
        "where_to_apply_hi": "नामांकित विद्यालय के प्रधानाचार्य के माध्यम से",
        "modal_target": "schemes-and-docs"
    },
    "kanyashree": {
        "title_en": "Kanyashree Prakalpa (Girls Education & Empowerment)",
        "title_bn": "কন্যাশ্রী প্রকল্প",
        "title_hi": "कन्याश्री प्रकल्प",
        "benefit_en": "K1: ₹1,000/year annual scholarship (Class 8-12, age 13-18) | K2: ₹25,000 one-time grant at age 18 | K3: ₹2,000-₹2,500/month for PG studies",
        "benefit_bn": "K1: বার্ষিক ₹১,০০০ স্কলারশিপ (৮ম-১২শ শ্রেণী, ১৩-১৮ বছর) | K2: ১৮ বছর বয়সে এককালীন ₹২৫,০০০ অনুদান | K3: উচ্চশিক্ষা ও পিজি গবেষণায় মাসিক ₹২,০০০-₹২,৫০০",
        "benefit_hi": "K1: ₹1,000 वार्षिक (8वीं-12वीं) | K2: ₹25,000 एकमुश्त (18 वर्ष पर) | K3: ₹2,000-₹2,500/माह पीजी अध्ययन हेतु",
        "eligibility_en": "Unmarried girls studying in recognized schools/colleges in West Bengal.",
        "eligibility_bn": "পশ্চিমবঙ্গের স্বীকৃত স্কুল বা কলেজে পাঠরত অবিবাহিতা ছাত্রীরা।",
        "eligibility_hi": "प. बंगाल के मान्यता प्राप्त स्कूलों/कॉलेजों में अध्ययनरत अविवाहित छात्राएं।",
        "documents_en": [
            "Age proof: Birth Certificate or Madhyamik Admit Card",
            "Unmarried declaration signed by guardian",
            "Bonafide certificate / Institutional enrollment proof",
            "Student's personal single bank account passbook",
            "Aadhaar Card and Passport Photo"
        ],
        "documents_bn": [
            "বয়সের প্রমাণ: জন্ম শংসাপত্র বা মাধ্যমিকের এডমিট কার্ড",
            "অভিভাবক কর্তৃক স্বাক্ষরিত অবিবাহিতা ঘোষণার ফর্ম",
            "স্কুল বা কলেজের প্রাতিষ্ঠানিক বোনাফাইড শংসাপত্র",
            "ছাত্রীর নিজস্ব একক ব্যাঙ্ক পাসবই",
            "আধার কার্ড এবং পাসপোর্ট সাইজ ছবি"
        ],
        "documents_hi": [
            "जन्म प्रमाण पत्र / माध्यमिक एडमिट कार्ड",
            "अविवाहित घोषणा पत्र",
            "स्कूल/कॉलेज बोनाफाइड सर्टिफिकेट",
            "छात्रा का सिंगल बैंक खाता पासबुक",
            "आधार कार्ड व पासपोर्ट फोटो"
        ],
        "portal_url": "https://www.wbkanyashree.gov.in",
        "portal_name": "Kanyashree Official Portal",
        "where_to_apply_en": "Through the school, madrasah, or college where the student is enrolled",
        "where_to_apply_bn": "ছাত্রী যে স্কুল, মাদ্রাসা বা কলেজে পড়াশোনা করছে তার মাধ্যমে",
        "where_to_apply_hi": "छात्रा के अपने स्कूल / कॉलेज के माध्यम से",
        "modal_target": "schemes-and-docs"
    },
    "rupashree": {
        "title_en": "Rupashree Prakalpa (₹25,000 One-Time Marriage Grant)",
        "title_bn": "রূপশ্রী প্রকল্প (বিয়ের এককালীন ₹২৫,০০০ অনুদান)",
        "title_hi": "रूपश्री प्रकल्प (शादी अनुदान ₹25,000)",
        "benefit_en": "₹25,000 one-time financial grant directly transferred to bride's bank account before marriage",
        "benefit_bn": "বিয়ের আগে সরাসরি পাত্রীর নিজস্ব ব্যাঙ্ক অ্যাকাউন্টে এককালীন ₹২৫,০০০ অনুদান",
        "benefit_hi": "शादी से पहले सीधे दुल्हन के खाते में ₹25,000 की एकमुश्त वित्तीय सहायता",
        "eligibility_en": "Bride aged 18+ years, Groom aged 21+ years, family annual income ≤ ₹1.5 Lakh, resident of West Bengal.",
        "eligibility_bn": "পাত্রীর বয়স ১৮+ বছর, পাত্রের ২১+ বছর, পারিবারিক বার্ষিক আয় ১.৫ লক্ষ টাকার কম, পশ্চিমবঙ্গের বাসিন্দা।",
        "eligibility_hi": "कन्या की उम्र 18+ वर्ष, वर की उम्र 21+ वर्ष, पारिवारिक आय ≤ ₹1.5 लाख, प. बंगाल की निवासी।",
        "documents_en": [
            "Age proof of bride & groom (Aadhaar / Birth Certificate / Madhyamik Admit)",
            "Marriage proof (Wedding invitation card or legal marriage notice)",
            "Family Annual Income Certificate (issued by BDO / SDO / Councilor / Pradhan)",
            "Unmarried declaration of the bride",
            "Bride's own single savings bank account passbook",
            "Recent passport size photos of both bride and groom"
        ],
        "documents_bn": [
            "পাত্র ও পাত্রী উভয়ের বয়সের প্রমাণ (আধার / জন্ম সার্টিফিকেট / মাধ্যমিক এডমিট)",
            "বিয়ের প্রমাণ (বিয়ের নিমন্ত্রণপত্র বা ম্যারেজ রেজিস্ট্রেশনের নোটিশ)",
            "পারিবারিক বার্ষিক আয়ের সার্টিফিকেট (BDO / SDO / কাউন্সিলর / প্রধান কর্তৃক নির্গত)",
            "পাত্রীর অবিবাহিতা স্বঘোষণা পত্র",
            "পাত্রীর নিজস্ব একক ব্যাঙ্ক পাসবই",
            "উভয়ের পাসপোর্ট সাইজ রঙিন ছবি"
        ],
        "documents_hi": [
            "वर व कन्या का आयु प्रमाण पत्र (आधार / जन्म प्रमाण पत्र)",
            "शादी का प्रमाण (विवाह निमंत्रण कार्ड / मैरिज रजिस्ट्रेशन नोटिस)",
            "पारिवारिक वार्षिक आय प्रमाण पत्र (BDO / SDO द्वारा जारी)",
            "कन्या का सिंगल बैंक खाता पासबुक",
            "दोनों की पासपोर्ट साइज फोटो"
        ],
        "portal_url": "https://wbrupashree.gov.in",
        "portal_name": "Rupashree Official Portal",
        "where_to_apply_en": "Local BDO Office (Rural) or Municipality / SDO (Urban) at least 30 to 60 days before marriage",
        "where_to_apply_bn": "বিয়ের অন্তত ৩০ থেকে ৬০ দিন আগে স্থানীয় বিডিও অফিস বা পুরসভা কার্যালয়",
        "where_to_apply_hi": "शादी की तारीख से 30 से 60 दिन पूर्व BDO या नगर पालिका कार्यालय में",
        "modal_target": "schemes-and-docs"
    },
    "svmcm": {
        "title_en": "Swami Vivekananda Merit-cum-Means (SVMCM / Bikash Bhavan) Scholarship",
        "title_bn": "স্বামী বিবেকানন্দ মেরিট-কাম-মিনস স্কলারশিপ (বিকাশ ভবন)",
        "title_hi": "स्वामी विवेकानंद स्कॉलरशिप (SVMCM - विकास भवन)",
        "benefit_en": "₹1,000 to ₹5,000 per month depending on degree/course level (HS, UG, PG, Engineering, Medical)",
        "benefit_bn": "কোর্স অনুযায়ী প্রতি মাসে ₹১,০০০ থেকে ₹৫,০০০ স্কলারশিপ (উচ্চমাধ্যমিক, স্নাতক, স্নাতকোত্তর, ইঞ্জিনিয়ারিং, মেডিক্যাল)",
        "benefit_hi": "पाठ्यक्रम स्तर के अनुसार ₹1,000 से ₹5,000 प्रति माह (HS, UG, PG, इंजीनियरिंग, मेडिकल)",
        "eligibility_en": "Minimum 60% marks in previous qualifying exam, family annual income ≤ ₹2,50,000, resident of West Bengal.",
        "eligibility_bn": "পূর্ববর্তী পরীক্ষায় ন্যূনতম ৬০% নম্বর, পারিবারিক বার্ষিক আয় ₹২,৫০,০০০ টাকার মধ্যে, পশ্চিমবঙ্গের বাসিন্দা।",
        "eligibility_hi": "पिछली परीक्षा में कम से कम 60% अंक, वार्षिक पारिवारिक आय ≤ ₹2,50,000, प. बंगाल का निवासी।",
        "documents_en": [
            "Marksheet of previous qualifying exam (both sides)",
            "Current course admission receipt / fee payment slip",
            "Family Annual Income Certificate (Joint BDO / BDO / SDO / Executive Officer)",
            "Domicile proof (Aadhaar / Voter ID / Ration card)",
            "Student's personal bank passbook (single account)",
            "Passport size photo and signature"
        ],
        "documents_bn": [
            "সর্বশেষ উত্তীর্ণ পরীক্ষার উভয় দিকের মার্কশিট",
            "বর্তমান কোর্সে ভর্তির রশিদ (Admission Slip)",
            "পারিবারিক বার্ষিক আয়ের সার্টিফিকেট (BDO / SDO নির্গত)",
            "বাসস্থানের প্রমাণ (আধার / ভোটার কার্ড)",
            "ছাত্র/ছাত্রীর নিজের ব্যাঙ্ক পাসবই (IFSC স্পষ্ট)",
            "পাসপোর্ট সাইজ ছবি ও স্বাক্ষর"
        ],
        "documents_hi": [
            "पिछली परीक्षा की दोनों तरफ की मार्कशीट",
            "वर्तमान कोर्स की प्रवेश रसीद (Admission Receipt)",
            "पारिवारिक आय प्रमाण पत्र (BDO / SDO द्वारा जारी)",
            "निवास प्रमाण पत्र (आधार / वोटर कार्ड)",
            "छात्र का सिंगल बैंक पासबुक",
            "पासपोर्ट साइज फोटो व हस्ताक्षर"
        ],
        "portal_url": "https://svmcm.wbhed.gov.in",
        "portal_name": "SVMCM Bikash Bhavan Portal",
        "where_to_apply_en": "Apply online at svmcm.wbhed.gov.in",
        "where_to_apply_bn": "svmcm.wbhed.gov.in পোর্টালে গিয়ে অনলাইনে আবেদন করতে হবে",
        "where_to_apply_hi": "svmcm.wbhed.gov.in पर ऑनलाइन आवेदन करें",
        "modal_target": "schemes-and-docs"
    },
    "wbscc": {
        "title_en": "West Bengal Student Credit Card (WBSCC)",
        "title_bn": "পশ্চিমবঙ্গ স্টুডেন্ট ক্রেডিট কার্ড প্রকল্প",
        "title_hi": "स्टूडेंट क्रेडिट कार्ड योजना (WBSCC)",
        "benefit_en": "Education loan up to ₹10 Lakh at nominal 4% simple interest for higher education in India and abroad",
        "benefit_bn": "উচ্চশিক্ষার জন্য নামমাত্র ৪% সরল সুদে সর্বোচ্চ ১০ লক্ষ টাকা পর্যন্ত স্টুডেন্ট লোন (ভারতে ও বিদেশে)",
        "benefit_hi": "उच्च शिक्षा हेतु मात्र 4% सरल ब्याज पर ₹10 लाख तक शिक्षा ऋण (भारत व विदेश में)",
        "eligibility_en": "Resident of West Bengal for at least 10 years, age up to 40 years, enrolled in Class 10/12/UG/PG/Competitive Coaching.",
        "eligibility_bn": "পশ্চিমবঙ্গে অন্তত ১০ বছর বসবাসকারী, সর্বোচ্চ বয়স ৪০ বছর, যেকোনো উচ্চশিক্ষা বা প্রতিযোগিতামূলক কোর্সে পাঠরত।",
        "eligibility_hi": "प. बंगाल में 10 वर्ष से निवासी, अधिकतम आयु 40 वर्ष, उच्च शिक्षा या कोचिंग में नामांकित।",
        "documents_en": [
            "Photo & signature of student and co-borrower",
            "Student's Aadhaar card / Class 10 registration certificate",
            "Co-borrower's PAN card & address proof",
            "Course fee structure and admission receipt from institute",
            "Bank details of student and co-borrower"
        ],
        "documents_bn": [
            "শিক্ষার্থী ও সহ-ঋণগ্রহীতার ছবি ও স্বাক্ষর",
            "শিক্ষার্থীর আধার কার্ড / মাধ্যমিক রেজিস্ট্রেশন",
            "সহ-ঋণগ্রহীতার প্যান কার্ড ও ঠিকানার প্রমাণ",
            "শিক্ষাপ্রতিষ্ঠানের কোর্স ফি কাঠামো ও ভর্তির রশিদ",
            "উভয়ের ব্যাঙ্ক অ্যাকাউন্টের বিবরণ"
        ],
        "documents_hi": [
            "छात्र व अभिभावक का फोटो व हस्ताक्षर",
            "छात्र का आधार कार्ड / 10वीं का रजिस्ट्रेशन",
            "अभिभावक का पैन कार्ड व पता प्रमाण",
            "कोर्स फीस स्ट्रक्चर व एडमिशन रसीद",
            "बैंक खाता विवरण"
        ],
        "portal_url": "https://wbscc.wb.gov.in",
        "portal_name": "WBSCC Official Portal",
        "where_to_apply_en": "Apply online at wbscc.wb.gov.in",
        "where_to_apply_bn": "wbscc.wb.gov.in পোর্টালে সরাসরি অনলাইনে আবেদন",
        "where_to_apply_hi": "wbscc.wb.gov.in पर ऑनलाइन आवेदन करें",
        "modal_target": "schemes-and-docs"
    },
    "swasthya_sathi": {
        "title_en": "Swasthya Sathi (₹5 Lakh Cashless Health Cover)",
        "title_bn": "স্বাস্থ্য সাথী প্রকল্প (৫ লক্ষ টাকা ক্যাশলেস স্বাস্থ্য বীমা)",
        "title_hi": "स्वास्थ्य साथी योजना (₹5 लाख कैशलेस स्वास्थ्य बीमा)",
        "benefit_en": "Cashless health cover up to ₹5,00,000 per family per year for secondary and tertiary medical care",
        "benefit_bn": "প্রতি বছর পরিবার পিছু সর্বোচ্চ ৫,০০,০০০ (পাঁচ লক্ষ) টাকা পর্যন্ত ক্যাশলেস স্বাস্থ্য বীমা পরিষেবা",
        "benefit_hi": "प्रति परिवार प्रति वर्ष ₹5,00,000 तक कैशलेस अस्पताल इलाज सुविधा",
        "eligibility_en": "All resident families of West Bengal. Smart card is issued in the name of the eldest female member.",
        "eligibility_bn": "পশ্চিমবঙ্গের সমস্ত নাগরিক পরিবার। স্মার্ট কার্ড পরিবারের জ্যেষ্ঠ মহিলার নামে ইস্যু হয়।",
        "eligibility_hi": "पश्चिम बंगाल के सभी परिवार। स्मार्ट कार्ड परिवार की वरिष्ठ महिला के नाम जारी होता है।",
        "documents_en": [
            "Aadhaar cards of all family members",
            "Digital Ration Card / Khadya Sathi card",
            "Passport size photo of the female head of family",
            "Form B (Duare Sarkar / Municipal counter)"
        ],
        "documents_bn": [
            "পরিবারের সকল সদস্যের আধার কার্ড",
            "ডিজিটাল রেশন কার্ড / খাদ্য সাথী কার্ড",
            "পরিবারের প্রধান মহিলার ১ কপি পাসপোর্ট সাইজ ছবি",
            "ফর্ম-বি (দুয়ারে সরকার ক্যাম্প বা পঞ্চায়েত অফিস থেকে সংগৃহীত)"
        ],
        "documents_hi": [
            "परिवार के सभी सदस्यों के आधार कार्ड",
            "डिजिटल राशन कार्ड",
            "परिवार की महिला मुखिया का पासपोर्ट फोटो",
            "फॉर्म-B"
        ],
        "portal_url": "https://swasthyasathi.gov.in",
        "portal_name": "Swasthya Sathi Portal",
        "where_to_apply_en": "Duare Sarkar Camps or local BDO / Municipality office",
        "where_to_apply_bn": "দুয়ারে সরকার ক্যাম্প অথবা স্থানীয় বিডিও বা পুরসভা অফিস",
        "where_to_apply_hi": "दुयरे सरकार कैंप या स्थानीय BDO / नगर पालिका",
        "modal_target": "schemes-and-docs"
    }
}
class ChatbotAssistantService:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

    def get_reply(self, user_message: str, history: list = None, api_key_override: str = '', preferred_language: str = '') -> dict:
        """
        Process user query and return chatbot reply with action buttons and official portal links.
        Supports multi-lingual generation (English, Bengali, Hindi) via Gemini API or intelligent offline fallback.
        """
        user_message = (user_message or "").strip()
        active_api_key = api_key_override.strip() or self.api_key

        # Detect active language from message, history, or preference
        detected_lang = self._detect_language(user_message, history, preferred_language)

        if not user_message:
            return self._welcome_message(detected_lang)

        # Handle direct language switch commands
        lang_switch_reply = self._check_language_switch_command(user_message)
        if lang_switch_reply:
            return lang_switch_reply

        # If Gemini API key is available, call Gemini API
        if active_api_key:
            gemini_result = self._call_gemini_api(user_message, history, active_api_key, detected_lang)
            if gemini_result:
                return gemini_result

        # Fallback to rich multi-lingual intelligent conversational engine
        return self._intelligent_fallback_response(user_message, history, detected_lang)

    def _detect_language(self, query: str, history: list = None, preferred_language: str = '') -> str:
        """Detect language: 'en', 'bn', or 'hi'"""
        if preferred_language in ['en', 'bn', 'hi']:
            return preferred_language

        q = query.lower()
        # Explicit user instructions to speak English
        if any(w in q for w in ["in english", "talk in english", "speak in english", "english please", "reply in english", "english", "ইংলিশ"]):
            return 'en'
        # Explicit user instructions to speak Bengali
        if any(w in q for w in ["bangla", "bengali", "বাংলা", "বাংলায়", "বাংলাতে"]):
            return 'bn'
        # Explicit user instructions to speak Hindi
        if any(w in q for w in ["hindi", "हिंदी", "हिन्दी"]):
            return 'hi'

        # Bengali Unicode block detection
        if re.search(r'[\u0980-\u09FF]', query):
            return 'bn'
        # Devanagari Unicode block detection
        if re.search(r'[\u0900-\u097F]', query):
            return 'hi'

        # Check history for last explicit language preference
        if history:
            for item in reversed(history[-4:]):
                content = item.get("content", "").lower()
                if "speak in english" in content or "talk in english" in content or "english" in content:
                    return 'en'
                if "বাংলা" in content or "bengali" in content:
                    return 'bn'
                if "हिंदी" in content or "hindi" in content:
                    return 'hi'

        # Default to English if predominantly Latin alphabet
        return 'en'

    def _check_language_switch_command(self, query: str) -> dict:
        """Check if user is requesting to change languages"""
        q = query.strip().lower()

        # Switch to English
        is_en_switch = any(p in q for p in ["talk in english", "speak in english", "reply in english", "speak english", "english please", "in english", "can you speak english"]) or q in ["english", "ইংলিশ", "इंग्लिश"]
        if is_en_switch:
            return {
                "reply": (
                    "👋 **Hello! I have switched my language to English.**\n\n"
                    "I am **NayaSetu AI**, your dedicated assistant for West Bengal Government Welfare Schemes, "
                    "Student Scholarships, Document Checklists, Official Portals, and Administrative Grievances.\n\n"
                    "How can I help you today? You can ask me anything, such as:\n"
                    "• *'What documents are needed for Lakshmir Bhandar?'*\n"
                    "• *'Krishak Bandhu eligibility and grant amount'*\n"
                    "• *'SVMCM scholarship application process'*\n"
                    "• *'Where to submit a complaint or search on this website?'*"
                ),
                "suggested_actions": [
                    {"label": "🌸 Lakshmir Bhandar Checklist", "type": "query", "text": "Lakshmir Bhandar documents required"},
                    {"label": "🌾 Krishak Bandhu Guide", "type": "query", "text": "Krishak Bandhu eligibility and benefits"},
                    {"label": "🎓 SVMCM Scholarship", "type": "query", "text": "SVMCM scholarship eligibility and documents"},
                    {"label": "🧭 Website Guide", "type": "action", "action": "schemes-and-docs"}
                ]
            }

        # Switch to Bengali
        is_bn_switch = any(p in q for p in ["বাংলায় কথা", "বাংলায় বলো", "বাংলায় বল", "কথা বাংলায়", "বাংলায় উত্তর", "talk in bengali", "speak in bengali"]) or q in ["বাংলা", "bengali", "bangla", "বাংলায়"]
        if is_bn_switch:
            return {
                "reply": (
                    "🙏 **নমস্কার! আমি এখন থেকে আপনার সাথে সম্পূর্ণ বাংলায় কথা বলব।**\n\n"
                    "আমি **নয়া সেতু AI (NayaSetu AI)** — পশ্চিমবঙ্গ সরকারের সমস্ত জনকল্যাণমূলক প্রকল্প (যেমন লক্ষ্মীর ভাণ্ডার, "
                    "কৃষক বন্ধু, কন্যাশ্রী), ছাত্রবৃত্তি (SVMCM, Oasis), প্রয়োজনীয় ডকুমেন্টস এবং সরকারি অধিকার সংক্রান্ত সহায়ক।\n\n"
                    "আজ আপনাকে কীভাবে সাহায্য করতে পারি? যেকোনো প্রশ্ন নির্দ্বিধায় জিজ্ঞাসা করুন, যেমন:\n"
                    "• *'লক্ষ্মীর ভাণ্ডার পেতে কি কি কাগজ লাগবে?'*\n"
                    "• *'কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান'*\n"
                    "• *'SVMCM বিকাশ ভবন স্কলারশিপের যোগ্যতা'*\n"
                    "• *'ওয়েবসাইটে অভিযোগ কীভাবে জমা দেব?'*"
                ),
                "suggested_actions": [
                    {"label": "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"},
                    {"label": "🌾 কৃষক বন্ধু পরচা নিয়ম", "type": "query", "text": "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান"},
                    {"label": "🎓 SVMCM স্কলারশিপ", "type": "query", "text": "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?"},
                    {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"}
                ]
            }

        # Switch to Hindi
        is_hi_switch = any(p in q for p in ["हिंदी में बात", "हिंदी में बोलो", "हिंदी में बोल", "बात हिंदी में", "हिंदी में उत्तर", "talk in hindi", "speak in hindi"]) or q in ["हिंदी", "हिन्दी", "hindi"]
        if is_hi_switch:
            return {
                "reply": (
                    "🙏 **नमस्ते! मैंने अपनी भाषा हिंदी में बदल ली है।**\n\n"
                    "मैं **नया सेतु AI (NayaSetu AI)** हूँ — पश्चिम बंगाल सरकार की सभी जन-कल्याणकारी योजनाओं, "
                    "छात्रवृत्तियों, आवश्यक दस्तावेज़ों और प्रशासनिक शिकायतों में नागरिकों की सहायता के लिए तैयार AI सहायक।\n\n"
                    "आज मैं आपकी क्या सहायता कर सकता हूँ? आप मुझसे कुछ भी पूछ सकते हैं, जैसे:\n"
                    "• *'लक्ष्मी भंडार में क्या-क्या कागज़ात लगेंगे?'*\n"
                    "• *'कृषक बंधु योजना के नियम व लाभ'*\n"
                    "• *'SVMCM स्कॉलरशिप की पात्रता'*\n"
                    "• *'वेबसाइट पे कहाँ क्या करना है?'*"
                ),
                "suggested_actions": [
                    {"label": "🌸 लक्ष्मी भंडार दस्तावेज़", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"},
                    {"label": "🌾 कृषक बंधु योजना", "type": "query", "text": "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?"},
                    {"label": "🎓 SVMCM स्कॉलरशिप", "type": "query", "text": "SVMCM scholarship eligibility aur documents"},
                    {"label": "⚖️ योग्यता जाँचें", "type": "action", "action": "eligibility-wizard"}
                ]
            }

        return None

    def _call_gemini_api(self, query: str, history: list, api_key: str, lang: str) -> dict:
        """Call Gemini API via google.genai Client with fallback models"""
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            # Build conversation history
            conversation_context = ""
            if history:
                for item in history[-6:]:
                    role = item.get("role", "user")
                    content = item.get("content", "")
                    conversation_context += f"{role.upper()}: {content}\n"

            lang_instruction = {
                'en': "RESPOND ENTIRELY IN NATURAL, CLEAR ENGLISH.",
                'bn': "RESPOND ENTIRELY IN NATURAL, RESPECTFUL BENGALI (বাংলা).",
                'hi': "RESPOND ENTIRELY IN RESPECTFUL HINDI (हिंदी)."
            }.get(lang, "RESPOND IN ENGLISH.")

            full_prompt = (
                f"Conversation History:\n{conversation_context}\n\n"
                f"CURRENT USER QUERY: {query}\n\n"
                f"LANGUAGE REQUIREMENT: {lang_instruction}\n"
                "Provide a comprehensive, empathetic, and accurately structured response as NayaSetu AI."
            )

            # Try candidate models
            candidate_models = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
            for model_name in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3,
                        )
                    )
                    if response and response.text:
                        text = response.text.strip()
                        actions = self._extract_relevant_actions(query, text, lang)
                        return {
                            "reply": text,
                            "suggested_actions": actions
                        }
                except Exception as model_err:
                    logger.info(f"Model {model_name} attempt failed: {model_err}")
                    continue

        except Exception as e:
            logger.warning(f"Gemini API chat call error: {e}")

        return None

    def _intelligent_fallback_response(self, query: str, history: list, lang: str) -> dict:
        """
        Comprehensive multi-lingual offline conversational engine.
        Delivers dynamic, context-relevant responses in English, Bengali, or Hindi.
        """
        q = query.lower()

        # 1. Greetings (Ensure whole-word matching to avoid matching 'scholarship' or 'this')
        is_greeting = False
        words = set(re.findall(r'\b\w+\b', q))
        if words.intersection({"hi", "hello", "hey", "namaste", "pranam", "adaab", "salam"}) or any(w in q for w in ["নমস্কার", "হ্যালো", "नमस्ते", "प्रणाम"]):
            if len(q.split()) <= 4:
                is_greeting = True

        if is_greeting:
            if lang == 'bn':
                return {
                    "reply": (
                        "🙏 **নমস্কার! আমি 'নয়া সেতু AI' (NayaSetu AI)।**\n\n"
                        "পশ্চিমবঙ্গ সরকারের বিভিন্ন জনকল্যাণমূলক প্রকল্প (যেমন লক্ষ্মীর ভাণ্ডার, কৃষক বন্ধু, কন্যাশ্রী), "
                        "ছাত্রবৃত্তি (SVMCM, Oasis, Aikyashree), দরকারি ডকুমেন্টস তালিকা এবং প্রশাসনিক সহায়তা প্রদানে আমি আপনাকে সাহায্য করতে পারি।\n\n"
                        "👉 আজ আপনি কী জানতে চান? নিচে ক্লিক করুন বা সরাসরি লিখুন।"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"},
                        {"label": "🌾 কৃষক বন্ধু পরচা নিয়ম", "type": "query", "text": "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান"},
                        {"label": "🎓 SVMCM স্কলারশিপ", "type": "query", "text": "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?"},
                        {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"}
                    ]
                }
            elif lang == 'hi':
                return {
                    "reply": (
                        "🙏 **नमस्ते! मैं 'नया सेतु AI' (NayaSetu AI) हूँ।**\n\n"
                        "पश्चिम बंगाल सरकार की सभी जन-कल्याणकारी योजनाओं (जैसे लक्ष्मी भंडार, कृषक बंधु, कन्याश्री), "
                        "स्कॉलरशिप्स (SVMCM, Oasis), ज़रूरी दस्तावेज़ों और नया सेतु वेबसाइट पर नागरिक सहायता के लिए मैं तैयार हूँ।\n\n"
                        "👉 आप क्या जानना चाहते हैं? सीधे लिखें या नीचे दिए गए विकल्पों में से चुनें:"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 लक्ष्मी भंडार दस्तावेज़", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"},
                        {"label": "🌾 कृषक बंधु योजना", "type": "query", "text": "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?"},
                        {"label": "🎓 SVMCM स्कॉलरशिप", "type": "query", "text": "SVMCM scholarship eligibility aur documents"},
                        {"label": "🧭 वेबसाइट गाइड", "type": "action", "action": "schemes-and-docs"}
                    ]
                }
            else:
                return {
                    "reply": (
                        "👋 **Hello! I am 'NayaSetu AI' (ন্যায়সেতু AI).**\n\n"
                        "I am your dedicated digital assistant for West Bengal Government Welfare Schemes, "
                        "Student Scholarships (SVMCM, Oasis, Aikyashree), Mandatory Document Checklists, and Administrative Grievances.\n\n"
                        "👉 How can I assist you today? Feel free to ask any question or choose from the options below:"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 Lakshmir Bhandar Checklist", "type": "query", "text": "Lakshmir Bhandar documents required"},
                        {"label": "🌾 Krishak Bandhu Guide", "type": "query", "text": "Krishak Bandhu eligibility and benefits"},
                        {"label": "🎓 SVMCM Scholarship", "type": "query", "text": "SVMCM scholarship eligibility and documents"},
                        {"label": "⚖️ Check Eligibility", "type": "action", "action": "eligibility-wizard"}
                    ]
                }

        # 2. Identity / Name query
        if any(w in q for w in ["who are you", "what is your name", "your name", "naam", "kon ho", "tum kaun", "পরিচয়", "তোমার নাম", "নাম কি", "तुम्हारा नाम", "कौन हो"]):
            if lang == 'bn':
                return {
                    "reply": (
                        "🙏 **আমার নাম 'নয়া সেতু AI' (NayaSetu AI / ন্যায়সেতু AI)।**\n\n"
                        "আমি পশ্চিমবঙ্গ সরকারের জনকল্যাণমূলক প্রকল্পসমূহ, নাগরিক অধিকার, ছাত্রবৃত্তি ও নথিপত্রের সঠিক তথ্য প্রদানের "
                        "জন্য তৈরি একটি বিশেষ AI সহকারী।\n\n"
                        "💡 **আমি কীভাবে আপনাকে সাহায্য করতে পারি:**\n"
                        "• যেকোনো সরকারি প্রকল্পের প্রয়োজনীয় নথিপত্রের সঠিক তালিকা প্রদান\n"
                        "• সরকারি প্রত্যাখ্যান বা এসএমএস-এর সহজ সরল ব্যাখ্যা\n"
                        "• বিডিও বা দুয়ারে সরকারের জন্য আনুষ্ঠানিক অভিযোগ পত্র (দরখাস্ত) প্রস্তুত করা\n"
                        "• যোগ্যতার ভিত্তিতে আপনার জন্য উপযুক্ত স্কিম নির্বাচন"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"},
                        {"label": "🧭 ওয়েবসাইট নির্দেশিকা", "type": "action", "action": "schemes-and-docs"},
                        {"label": "📝 অভিযোগ প্রস্তুতি", "type": "action", "action": "grievance-drafter"}
                    ]
                }
            elif lang == 'hi':
                return {
                    "reply": (
                        "🙏 **मेरा नाम 'नया सेतु AI' (NayaSetu AI / न्यायसेतु AI) है।**\n\n"
                        "मैं पश्चिम बंगाल सरकार की सभी जन-कल्याणकारी योजनाओं, छात्रवृत्तियों, आवश्यक दस्तावेज़ों और प्रशासनिक "
                        "सहायता के लिए बनाया गया एक समर्पित AI सहायक हूँ।\n\n"
                        "💡 **मेरी मुख्य सेवाएँ:**\n"
                        "• योजनाओं के आवश्यक दस्तावेज़ों की सही सूची देना\n"
                        "• रिजेक्शन एसएमएस और नोटिस का सरल भाषा में विश्लेषण\n"
                        "• BDO / SDO के नाम तैयार दरखास्त पत्र तैयार करना\n"
                        "• वेबसाइट नेविगेशन और योग्यता जाँच"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 लक्ष्मी भंडार दस्तावेज़", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"},
                        {"label": "🧭 वेबसाइट गाइड", "type": "action", "action": "schemes-and-docs"},
                        {"label": "📝 शिकायत ड्राफ्टर", "type": "action", "action": "grievance-drafter"}
                    ]
                }
            else:
                return {
                    "reply": (
                        "🙏 **My name is 'NayaSetu AI' (ন্যায়সেতু AI).**\n\n"
                        "I am an intelligent citizen assistant designed specifically for the West Bengal Government Welfare Ecosystem. "
                        "I help citizens understand scheme benefits, mandatory document requirements, avoid common rejection traps, "
                        "and draft formal representation letters for BDO and Duare Sarkar offices.\n\n"
                        "💡 **What I can do for you:**\n"
                        "• Detailed document checklists for all WB schemes (Lakshmir Bhandar, Krishak Bandhu, SVMCM, etc.)\n"
                        "• Explain government rejection notices and SMS in plain language\n"
                        "• Guide you to official government portals and offices\n"
                        "• Assist you in drafting formal grievance letters"
                    ),
                    "suggested_actions": [
                        {"label": "🌸 Lakshmir Bhandar Checklist", "type": "query", "text": "Lakshmir Bhandar documents required"},
                        {"label": "📋 Schemes Directory", "type": "action", "action": "schemes-and-docs"},
                        {"label": "📝 Grievance Drafter", "type": "action", "action": "grievance-drafter"}
                    ]
                }

        # 3. Lakshmir Bhandar / Annapurna Bhandar
        if any(w in q for w in ["लक्ष्मी", "lakshmi", "lakshmir", "লক্ষ্মী", "ভাণ্ডার", "লাক্ষ্মীর", "মহিলাদের", "annapurna", "অন্নপূর্ণা", "अन्नपूर्णा", "3000"]):
            return self._format_scheme_response("lakshmir_bhandar", lang)

        # 3.1. West Bengal Yuva Shakti Yojana
        if any(w in q for w in ["yuva", "yuba", "যুব", "শক্তি", "युवा", "shakti", "bharosa", "ভরোসা", "unemployment", "বেকার", "2000"]):
            return self._format_scheme_response("wb_yuva_shakti", lang)

        # 3.2. Ayushman Bharat PM-JAY & Vay Vandana 70+
        if any(w in q for w in ["ayushman", "pmjay", "আয়ুষ্মান", "ভারত", "आयुष्मान", "वय वंदना", "vay vandana", "70", "senior citizen"]):
            return self._format_scheme_response("ayushman_bharat", lang)

        # 3.3. Karmashree 50 Days Work
        if any(w in q for w in ["karmashree", "কর্মশ্রী", "कर्मश्री", "50 day", "৫০ দিন", "50 din", "job card"]):
            return self._format_scheme_response("karmashree", lang)

        # 3.4. Bhabishyat Credit Card (WBBCCS)
        if any(w in q for w in ["bhabishyat", "bccs", "ভবিষ্যৎ", "भविष्य"]):
            return self._format_scheme_response("bhabishyat_credit_card", lang)

        # 3.5. Banglar Awas Yojana
        if any(w in q for w in ["awas", "আবাস", "বাড়ি", "आवास", "makan", "ঘর", "120000"]):
            return self._format_scheme_response("banglar_awas", lang)

        # 3.6. Bangla Shasya Bima (BSB)
        if any(w in q for w in ["shasya", "bima", "বীমা", "বিমা", "বীমা", "crop insurance", "फसल बीमा"]):
            return self._format_scheme_response("bangla_shasya_bima", lang)

        # 3.7. Taruner Swapno
        if any(w in q for w in ["tarun", "swapno", "তরুণের", "স্বপ্ন", "তরুণ", "taruner", "tab", "ট্যাব", "ট্যাবলেট", "smartphone"]):
            return self._format_scheme_response("taruner_swapno", lang)

        # 4. Krishak Bandhu
        if any(w in q for w in ["कृषक", "krishak", "কৃষক", "bandhu", "বন্ধু", "chashi", "চাষী", "किसान", "kisan", "পরচা", "porcha"]):
            return self._format_scheme_response("krishak_bandhu", lang)

        # 5. Kanyashree
        if any(w in q for w in ["कन्याश्री", "kanya", "kanyashree", "কন্যাশ্রী", "k1", "k2", "k3"]):
            return self._format_scheme_response("kanyashree", lang)

        # 6. Rupashree
        if any(w in q for w in ["रूपश्री", "rupashree", "রূপশ্রী", "शादी", "विवाह", "biye", "marriage", "বিয়ে"]):
            return self._format_scheme_response("rupashree", lang)

        # 7. SVMCM Scholarship & Higher Education Scholarships
        if any(w in q for w in ["svmcm", "swami vivekananda", "bikash bhavan", "বিবেকানন্দ", "বিকাশ ভবন", "स्वामी विवेकानंद", "विकास भवन", "scholarship", "scholarships", "স্কলারশিপ", "स्कॉलरशिप", "বৃত্তি", "aikyashree", "oasis", "ঐক্যশ্রী", "ওএসিস"]):
            return self._format_scheme_response("svmcm", lang)

        # 8. Student Credit Card (WBSCC)
        if any(w in q for w in ["student credit card", "wbscc", "क्रेडिट कार्ड", "ক্রেডিট কার্ড", "10 lakh", "loan", "এডুকেশন লোন"]):
            return self._format_scheme_response("wbscc", lang)

        # 9. Swasthya Sathi
        if any(w in q for w in ["swasthya sathi", "স্বাস্থ্য সাথী", "स्वास्थ्य साथी", "health card", "5 lakh", "chikitsa", "ilaj"]):
            return self._format_scheme_response("swasthya_sathi", lang)

        # 10. Website Navigation / "Where to do what"
        if any(w in q for w in ["website", "guide", "help", "kahan", "কোথায়", "কি করতে হবে", "kya karna", "kaise use", "কই", "কিসে যাব"]):
            return self._format_website_guide(lang)

        # 11. Complaints / Grievances / Letter Drafting / Money not credited
        if any(w in q for w in ["complaint", "complain", "grievance", "shikayat", "অভিযোগ", "দরখাস্ত", "letter", "দরখাস্ত লেখা", "money not", "taka aseni", "taka pacchi na", "paisa nahi", "payment stuck", "dbt reject", "npci"]):
            return self._format_grievance_guide(lang)

        # 12. Documents Where / Checklist
        if any(w in q for w in ["document", "documents", "ডকুমেন্ট", "নথি", "কাগজ", "कागजात", "कागज़ात", "checklist"]):
            return self._format_documents_guide(lang)

        # 13. General / Open-ended query handling (Never output static repeated text)
        return self._format_dynamic_fallback(query, lang)

    def _format_scheme_response(self, scheme_key: str, lang: str) -> dict:
        s = SCHEMES_KNOWLEDGE.get(scheme_key)
        if not s:
            return self._format_dynamic_fallback(scheme_key, lang)

        if lang == 'bn':
            docs = "\n".join([f"  • **{d}**" for d in s["documents_bn"]])
            reply = (
                f"🌸 **{s['title_bn']} — বিস্তারিত নির্দেশিকা ও নথিপত্র:**\n\n"
                f"💰 **সুবিধা ও অনুদান**: {s['benefit_bn']}\n"
                f"👩‍💼 **যোগ্যতা**: {s['eligibility_bn']}\n\n"
                f"📑 **প্রয়োজনীয় নথিপত্রের তালিকা (Mandatory Documents):**\n"
                f"{docs}\n\n"
                f"⚠️ **গুরুত্বপূর্ণ নিয়ম:**\n"
                f"• ব্যাঙ্ক অ্যাকাউন্ট অবশ্যই **একক (Single)** হতে হবে এবং **Aadhaar-NPCI DBT** সক্রিয় থাকা বাধ্যতামূলক।\n\n"
                f"🌐 **অফিসিয়াল সরকারি পোর্টাল:**\n"
                f"👉 [{s['portal_name']}]({s['portal_url']})\n\n"
                f"📍 **আবেদন কোথায় করবেন:** {s['where_to_apply_bn']}"
            )
            actions = [
                {"label": f"🌐 {s['portal_name']}", "type": "link", "url": s["portal_url"]},
                {"label": "📋 প্রকল্প নির্দেশিকা", "type": "action", "action": s["modal_target"]},
                {"label": "📝 বিডিও অভিযোগ ড্রাফট", "type": "action", "action": "grievance-drafter"}
            ]
        elif lang == 'hi':
            docs = "\n".join([f"  • **{d}**" for d in s["documents_hi"]])
            reply = (
                f"🌸 **{s['title_hi']} — आवश्यक दस्तावेज़ व नियम:**\n\n"
                f"💰 **लाभ**: {s['benefit_hi']}\n"
                f"👩 **पात्रता**: {s['eligibility_hi']}\n\n"
                f"📑 **ज़रूरी दस्तावेज़ों की चेकलिस्ट:**\n"
                f"{docs}\n\n"
                f"⚠️ **महत्वपूर्ण चेतावनी:**\n"
                f"• बैंक खाता **सिंगल (Single Account)** होना चाहिए, और **Aadhaar-NPCI DBT Seeding** अनिवार्य है।\n\n"
                f"🌐 **ऑफिशियल सरकारी वेबसाइट:**\n"
                f"👉 [{s['portal_name']}]({s['portal_url']})\n\n"
                f"📍 **आवेदन कहाँ करें:** {s['where_to_apply_hi']}"
            )
            actions = [
                {"label": f"🌐 {s['portal_name']}", "type": "link", "url": s["portal_url"]},
                {"label": "📋 दस्तावेज़ चेकलिस्ट", "type": "action", "action": s["modal_target"]},
                {"label": "📝 BDO शिकायत पत्र बनाएं", "type": "action", "action": "grievance-drafter"}
            ]
        else:
            docs = "\n".join([f"  • **{d}**" for d in s["documents_en"]])
            reply = (
                f"🌸 **{s['title_en']} — Complete Guide & Documents:**\n\n"
                f"💰 **Financial Benefit**: {s['benefit_en']}\n"
                f"👩‍💼 **Eligibility**: {s['eligibility_en']}\n\n"
                f"📑 **Mandatory Document Checklist:**\n"
                f"{docs}\n\n"
                f"⚠️ **Critical Guidelines:**\n"
                f"• Bank account must be a **Single Savings Account** (joint accounts are rejected).\n"
                f"• The account must have **Active Aadhaar-NPCI DBT Seeding** to receive payments.\n\n"
                f"🌐 **Official West Bengal Portal:**\n"
                f"👉 [{s['portal_name']}]({s['portal_url']})\n\n"
                f"📍 **Where to Apply:** {s['where_to_apply_en']}"
            )
            actions = [
                {"label": f"🌐 {s['portal_name']}", "type": "link", "url": s["portal_url"]},
                {"label": "📋 View Scheme Details", "type": "action", "action": s["modal_target"]},
                {"label": "📝 Draft Grievance Letter", "type": "action", "action": "grievance-drafter"}
            ]

        return {"reply": reply, "suggested_actions": actions}

    def _format_website_guide(self, lang: str) -> dict:
        if lang == 'bn':
            return {
                "reply": (
                    "🧭 **নয়া সেতু (NayaSetu) ওয়েবসাইটে কোথায় কি করবেন — পূর্ণ নির্দেশিকা:**\n\n"
                    "1. 🔍 **সার্চ করবেন কোথায়**: হোমপেজের শীর্ষে **'Ask NyayaSetu AI'** সার্চ বক্সে সরাসরি লিখুন (যেমন: *'মেয়েদের বিয়ে'*, *'চাষীদের টাকা'*).\n"
                    "2. ⚖️ **যোগ্যতা যাচাই (Eligibility Wizard)**: মেনুতে **'যোগ্যতা যাচাই'** ক্লিক করে নিজের বয়স, জাতি ও আয় নির্বাচন করুন — সিস্টেম যোগ্য প্রকল্প দেখাবে।\n"
                    "3. 📋 **ডকুমেন্টস নির্দেশিকা (Schemes Directory)**: **'প্রকল্প নির্দেশিকা'** খুলে প্রতি প্রকল্পের নিয়ম ও সরকারি লিঙ্ক দেখুন।\n"
                    "4. 📝 **অভিযোগ / দরখাস্ত প্রস্তুতি (Grievance Drafter)**: **'অভিযোগ প্রস্তুতি'**-তে বিডিও বা দুয়ারে সরকারের নামাঙ্কিত প্রস্তুত আবেদনপত্র বানান।\n"
                    "5. 📄 **এসএমএস বা রিজেকশন বুঝুন (Notice Explainer)**: **'নোটিশ / রসিদ বুঝুন'**-এ সরকারি মেসেজ পেস্ট করুন, AI সহজ ভাষায় বুঝিয়ে দেবে।"
                ),
                "suggested_actions": [
                    {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"},
                    {"label": "📋 প্রকল্প তালিকা", "type": "action", "action": "schemes-and-docs"},
                    {"label": "📝 অভিযোগ ড্রাফটার", "type": "action", "action": "grievance-drafter"},
                    {"label": "📄 এসএমএস ডিক্রিপ্টার", "type": "action", "action": "notice-explainer"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": (
                    "🧭 **नया सेतु (NayaSetu) वेबसाइट पर कहाँ क्या करना है — पूरी जानकारी:**\n\n"
                    "1. 🔍 **सर्च कहाँ करें**: होमपेज के ऊपर **'Ask NyayaSetu AI'** सर्च बॉक्स में सीधे अपनी भाषा में लिखें।\n"
                    "2. ⚖️ **योग्यता जाँचें (Eligibility Wizard)**: मेन्यू में **'योग्यत যাচাই'** पर क्लिक करके अपनी पात्रता देखें।\n"
                    "3. 📋 **दस्तावेज़ सूची (Schemes Directory)**: **'প্রকল্প নির্দেশিকা'** पर क्लिक करके हर योजना के पूरे नियम देखें।\n"
                    "4. 📝 **शिकायत पत्र बनाएं (Grievance Drafter)**: **'অভিযোগ প্রস্তুতি'** से BDO/SDO के लिए तैयार दरखास्त पत्र प्राप्त करें।\n"
                    "5. 📄 **रिजेक्शन एसएमएस समझें (Notice Explainer)**: **'নোটিশ / রসিদ বুঝুন'** में सरकारी रिजेक्शन पर्ची या एसएमएस पेस्ट करें।"
                ),
                "suggested_actions": [
                    {"label": "⚖️ योग्यता जाँचें", "type": "action", "action": "eligibility-wizard"},
                    {"label": "📋 योजना सूची", "type": "action", "action": "schemes-and-docs"},
                    {"label": "📝 शिकायत ड्राफ्टर", "type": "action", "action": "grievance-drafter"},
                    {"label": "📄 एसएमएस डिक्रिप्टर", "type": "action", "action": "notice-explainer"}
                ]
            }
        else:
            return {
                "reply": (
                    "🧭 **NayaSetu Website Navigation Guide — How to use our tools:**\n\n"
                    "1. 🔍 **Where to Search**: Use the prominent **'Ask NyayaSetu AI'** search bar at the top of the homepage to search in everyday English, Bengali, or Hindi.\n"
                    "2. ⚖️ **Check Eligibility (Eligibility Wizard)**: Click **'যোগ্যতা যাচাই'** in the top navigation bar, enter basic details (age, income, caste), and discover all schemes you qualify for.\n"
                    "3. 📋 **View Document Checklists (Schemes Directory)**: Click **'প্রকল্প নির্দেশিকা'** to view exhaustive checklists, official portal links, and rejection remedies.\n"
                    "4. 📝 **Draft Grievance Letters (Grievance Drafter)**: Click **'অভিযোগ প্রস্তুতি'** to automatically generate a formal legal representation letter for BDO, SDO, or Duare Sarkar camps.\n"
                    "5. 📄 **Decipher Rejection SMS (Notice Explainer)**: Click **'নোটিশ / রসিদ বুঝুন'** to paste SMS or upload a photo of a rejection slip for a plain-language explanation."
                ),
                "suggested_actions": [
                    {"label": "⚖️ Eligibility Wizard", "type": "action", "action": "eligibility-wizard"},
                    {"label": "📋 Schemes Directory", "type": "action", "action": "schemes-and-docs"},
                    {"label": "📝 Grievance Drafter", "type": "action", "action": "grievance-drafter"},
                    {"label": "📄 Notice Explainer", "type": "action", "action": "notice-explainer"}
                ]
            }

    def _format_grievance_guide(self, lang: str) -> dict:
        if lang == 'bn':
            return {
                "reply": (
                    "📝 **সরকারি অভিযোগ বা দরখাস্ত লেখার উপায়:**\n\n"
                    "1. **নয়া সেতু গ্রিভেন্স ড্রাফটার**: আমাদের **'অভিযোগ প্রস্তুতি' (Grievance Drafter)** টুলটি খুলুন। আপনার সমস্যা (যেমন টাকা না আসা, আবেদন আটকে থাকা) নির্বাচন করলেই সিস্টেম BDO বা দুয়ারে সরকার ক্যাম্পের নামাঙ্কিত প্রস্তুত দরখাস্ত তৈরি করে দেবে।\n"
                    "2. **মুখ্যমন্ত্রী হেল্পলাইন**: সরাসরি ফোন করুন 📞 **033-2214-5555** নম্বরে।\n"
                    "3. **দুয়ারে সরকার ডেস্ক**: ক্যাম্প চলাকালীন সরাসরি হেল্পডেস্কে লিখিত আবেদন জমা দিতে পারেন।"
                ),
                "suggested_actions": [
                    {"label": "📝 দরখাস্ত তৈরি করুন", "type": "action", "action": "grievance-drafter"},
                    {"label": "🏢 প্রশাসনিক কার্যালয় তালিকা", "type": "action", "action": "helpline-and-offices"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": (
                    "📝 **शिकायत दर्ज करने व दरखास्त तैयार करने के उपाय:**\n\n"
                    "1. **नया सेतु ग्रीवेंस ड्राफ्टर**: मेन्यू में **'অভিযোগ প্রস্তুতি' (Grievance Drafter)** खोलें। यहाँ से आप BDO या दुयरे सरकार के नाम आधिकारिक कानूनी आवेदन पत्र तुरंत बना सकते हैं।\n"
                    "2. **मुख्यमंत्री हेल्पलाइन (CM Helpline)**: 📞 **033-2214-5555** पर कॉल करें।\n"
                    "3. **BDO ऑफिस**: अपने स्थानीय प्रखंड कार्यालय में लिखित दरखास्त जमा करें।"
                ),
                "suggested_actions": [
                    {"label": "📝 शिकायत पत्र बनाएं", "type": "action", "action": "grievance-drafter"},
                    {"label": "🏢 प्रशासनिक कार्यालय सूची", "type": "action", "action": "helpline-and-offices"}
                ]
            }
        else:
            return {
                "reply": (
                    "📝 **How to Submit a Complaint or Representation Letter:**\n\n"
                    "1. **NayaSetu Grievance Drafter**: Use our dedicated **'Grievance Drafter' (অভিযোগ প্রস্তুতি)** tool. Select your issue (e.g. stalled application, DBT bank rejection), and the tool will instantly draft a customized, formal Bengali/English representation letter addressed to your BDO or SDO.\n"
                    "2. **Chief Minister's Helpline**: Directly dial 📞 **033-2214-5555** for statewide grievance escalation.\n"
                    "3. **Duare Sarkar Counters**: Submit your drafted representation at the official assistance counter during camp dates."
                ),
                "suggested_actions": [
                    {"label": "📝 Open Grievance Drafter", "type": "action", "action": "grievance-drafter"},
                    {"label": "🏢 Administrative Offices", "type": "action", "action": "helpline-and-offices"}
                ]
            }

    def _format_documents_guide(self, lang: str) -> dict:
        if lang == 'bn':
            return {
                "reply": (
                    "📂 **প্রয়োজনীয় ডকুমেন্টস দেখার নিয়ম:**\n\n"
                    "1. উপরে মেনু থেকে **'প্রকল্প নির্দেশিকা' (Schemes Directory)** খুলুন।\n"
                    "2. সেখানে প্রতিটি স্কিমের বিস্তারিত কার্ডে সম্পূর্ণ চেকলিস্ট, জিরক্স নাকি অরিজিনাল লাগবে এবং নিয়মাবলী স্পষ্টভাবে দেওয়া আছে।\n"
                    "3. অথবা আপনি আমাকে সরাসরি যেকোনো স্কিমের নাম লিখতে পারেন, যেমন: *'লক্ষ্মীর ভাণ্ডারে কি কি কাগজ লাগবে?'*।"
                ),
                "suggested_actions": [
                    {"label": "📋 প্রকল্প নির্দেশিকা", "type": "action", "action": "schemes-and-docs"},
                    {"label": "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": (
                    "📂 **डॉक्यूमेंट्स चेकलिस्ट देखने का तरीका:**\n\n"
                    "1. ऊपर नेविगेशन मेन्यू में **'প্রকল্প নির্দেশিকা' (Schemes Directory)** खोलें।\n"
                    "2. हर योजना कार्ड में पूरी दस्तावेज़ सूची और आवश्यक शर्तें दी गई हैं।\n"
                    "3. आप मुझसे भी सीधे पूछ सकते हैं, जैसे: *'लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?'*।"
                ),
                "suggested_actions": [
                    {"label": "📋 योजना सूची खोलें", "type": "action", "action": "schemes-and-docs"},
                    {"label": "🌸 लक्ष्मी भंडार दस्तावेज़", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"}
                ]
            }
        else:
            return {
                "reply": (
                    "📂 **How to Access Document Checklists:**\n\n"
                    "1. Click **'Schemes Directory' (প্রকল্প নির্দেশিকা)** from the top navigation bar.\n"
                    "2. Every scheme card includes an exhaustive checklist of required documents, indicating whether original or xerox is needed, and specific caveats (e.g., single bank passbook).\n"
                    "3. You can also ask me directly right here in the chat, for example: *'What documents are needed for Lakshmir Bhandar?'*."
                ),
                "suggested_actions": [
                    {"label": "📋 Open Schemes Directory", "type": "action", "action": "schemes-and-docs"},
                    {"label": "🌸 Lakshmir Bhandar Checklist", "type": "query", "text": "Lakshmir Bhandar documents required"}
                ]
            }

    def _format_dynamic_fallback(self, query: str, lang: str) -> dict:
        """Dynamic, conversational fallback that addresses the query intelligently in user's language"""
        clean_q = query.strip()

        if lang == 'bn':
            return {
                "reply": (
                    f"🙏 **আমি আপনার প্রশ্নটি বুঝতে পেরেছি:** *\"{clean_q}\"*\n\n"
                    "**নয়া সেতু AI** হিসেবে আমি পশ্চিমবঙ্গ সরকারের যাবতীয় নাগরিক অধিকার, জনকল্যাণমূলক প্রকল্প, "
                    "ছাত্রবৃত্তি এবং আবেদন প্রক্রিয়ায় আপনাকে সাহায্য করতে পারি।\n\n"
                    "💡 **আপনার প্রয়োজনীয় বিষয়টি বেছে নিন বা আরও নির্দিষ্টভাবে লিখুন:**\n"
                    "• **লক্ষ্মীর ভাণ্ডার ও মহিলা সহায়তা**: প্রতি মাসে ₹১০০০/₹১২০০ পাওয়ার নিয়ম ও নথিপত্র\n"
                    "• **কৃষক বন্ধু ও কৃষি সহায়তা**: বার্ষিক ₹১০,০০০ অনুদান ও পরচা যাচাই\n"
                    "• **স্কলারশিপ (SVMCM / Oasis / Aikyashree)**: স্কুল ও কলেজের অনুদান\n"
                    "• **অভিযোগ ও দরখাস্ত প্রস্তুতি**: BDO অফিসের জন্য দরখাস্ত ড্রাফটিং\n\n"
                    "👉 আপনি ইংরেজিতে কথা বলতে চাইলে লিখুন: *'talk in english'* বা সরাসরি আপনার প্রশ্নটি লিখুন।"
                ),
                "suggested_actions": [
                    {"label": "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"},
                    {"label": "🌾 কৃষক বন্ধু পরচা নিয়ম", "type": "query", "text": "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান"},
                    {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"},
                    {"label": "📋 প্রকল্প নির্দেশিকা", "type": "action", "action": "schemes-and-docs"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": (
                    f"🙏 **मैंने आपका प्रश्न देखा:** *\"{clean_q}\"*\n\n"
                    "**नया सेतु AI** के रूप में मैं पश्चिम बंगाल सरकार की सभी योजनाओं, छात्रवृत्तियों, सरकारी "
                    "दस्तावेज़ों और प्रशासनिक प्रक्रियाओं में नागरिकों की सहायता करता हूँ।\n\n"
                    "💡 **आप नीचे दिए गए विकल्पों में से चुन सकते हैं या अपना प्रश्न विस्तार से लिख सकते हैं:**\n"
                    "• **लक्ष्मी भंडार**: ₹1000/₹1200 मासिक अनुदान व ज़रूरी कागज़ात\n"
                    "• **कृषक बंधु**: वार्षिक ₹10,000 सहायता व परचा नियम\n"
                    "• **SVMCM स्कॉलरशिप**: कॉलेज व उच्च शिक्षा छात्रवृत्ति\n"
                    "• **शिकायत पत्र**: BDO/SDO के लिए तैयार दरखास्त पत्र\n\n"
                    "👉 अगर आप इंग्लिश या बंगाली में बात करना चाहें, तो बस लिखें: *'talk in english'* या *'বাংলায় কথা বলো'*।"
                ),
                "suggested_actions": [
                    {"label": "🌸 लक्ष्मी भंडार दस्तावेज़", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"},
                    {"label": "🌾 कृषक बंधु योजना", "type": "query", "text": "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?"},
                    {"label": "⚖️ योग्यता जाँचें", "type": "action", "action": "eligibility-wizard"},
                    {"label": "📋 योजना सूची", "type": "action", "action": "schemes-and-docs"}
                ]
            }
        else:
            return {
                "reply": (
                    f"💡 **Regarding your query:** *\"{clean_q}\"*\n\n"
                    "I am **NayaSetu AI**, your comprehensive assistant for West Bengal Government welfare schemes, "
                    "student scholarships, and citizen rights. I am here to help answer questions, verify document requirements, "
                    "and assist you with administrative procedures.\n\n"
                    "Here are key areas I can assist you with right now:\n"
                    "• **Women's Welfare (Lakshmir Bhandar, Rupashree)**: Documents, ₹1,000-₹1,200/month criteria, single bank passbook.\n"
                    "• **Farmer Assistance (Krishak Bandhu)**: Up to ₹10,000/year assistance, land record (Porcha) rules.\n"
                    "• **Student Scholarships (SVMCM, Oasis, Aikyashree)**: 60% eligibility, income certificates, portal links.\n"
                    "• **Administrative Support**: Formal grievance drafting for BDO/SDO offices & Duare Sarkar camps.\n\n"
                    "👉 You can switch languages anytime by saying: *'বাংলায় কথা বলো'* or *'हिंदी में बोलो'*."
                ),
                "suggested_actions": [
                    {"label": "🌸 Lakshmir Bhandar Checklist", "type": "query", "text": "Lakshmir Bhandar documents required"},
                    {"label": "🌾 Krishak Bandhu Guide", "type": "query", "text": "Krishak Bandhu eligibility and benefits"},
                    {"label": "🎓 SVMCM Scholarship", "type": "query", "text": "SVMCM scholarship eligibility and documents"},
                    {"label": "⚖️ Check Eligibility", "type": "action", "action": "eligibility-wizard"}
                ]
            }

    def _welcome_message(self, lang: str) -> dict:
        if lang == 'bn':
            return {
                "reply": "নমস্কার! আমি **নয়া সেতু AI**। পশ্চিমবঙ্গ সরকারের যেকোনো প্রকল্প, স্কলারশিপ বা অধিকার সংক্রান্ত সহায়তা পেতে আপনার প্রশ্ন লিখুন।",
                "suggested_actions": [
                    {"label": "🌸 লক্ষ্মীর ভাণ্ডার", "type": "query", "text": "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?"},
                    {"label": "🌾 কৃষক বন্ধু", "type": "query", "text": "কৃষক বন্ধু প্রকল্পের নিয়ম"},
                    {"label": "🎓 SVMCM স্কলারশিপ", "type": "query", "text": "SVMCM স্কলারশিপ"},
                    {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": "नमस्ते! मैं **नया सेतु AI** हूँ। पश्चिम बंगाल सरकार की किसी भी योजना, स्कॉलरशिप या वेबसाइट सहायता के लिए अपना प्रश्न पूछें।",
                "suggested_actions": [
                    {"label": "🌸 लक्ष्मी भंडार", "type": "query", "text": "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?"},
                    {"label": "🌾 कृषक बंधु", "type": "query", "text": "कृषक बंधु योजना"},
                    {"label": "🎓 SVMCM स्कॉलरशिप", "type": "query", "text": "SVMCM scholarship"},
                    {"label": "⚖️ योग्यता जाँचें", "type": "action", "action": "eligibility-wizard"}
                ]
            }
        else:
            return {
                "reply": "Hello! I am **NayaSetu AI**. How can I help you today with West Bengal government schemes, scholarships, document checklists, or administrative grievances?",
                "suggested_actions": [
                    {"label": "🌸 Lakshmir Bhandar", "type": "query", "text": "Lakshmir Bhandar documents required"},
                    {"label": "🌾 Krishak Bandhu", "type": "query", "text": "Krishak Bandhu eligibility"},
                    {"label": "🎓 SVMCM Scholarship", "type": "query", "text": "SVMCM scholarship"},
                    {"label": "⚖️ Check Eligibility", "type": "action", "action": "eligibility-wizard"}
                ]
            }

    def _extract_relevant_actions(self, query: str, text: str, lang: str = 'en') -> list:
        """Helper to attach quick modal action buttons based on AI response context"""
        actions = []
        q = (query + " " + text).lower()

        if "lakshmir" in q or "লক্ষ্মীর" in q or "लक्ष्मी" in q:
            actions.append({"label": "🌐 Official WB Portal", "type": "link", "url": "https://wb.gov.in"})
            actions.append({"label": "📋 NayaSetu Checklist", "type": "action", "action": "schemes-and-docs"})
        elif "krishak" in q or "কৃষক" in q or "कृषक" in q:
            actions.append({"label": "🌐 Krishak Bandhu Portal", "type": "link", "url": "https://krishakbandhu.wb.gov.in"})
            actions.append({"label": "📋 NayaSetu Checklist", "type": "action", "action": "schemes-and-docs"})
        elif "svmcm" in q or "বিবেকানন্দ" in q or "विवेकानंद" in q:
            actions.append({"label": "🌐 SVMCM Official Portal", "type": "link", "url": "https://svmcm.wbhed.gov.in"})
        elif "kanyashree" in q or "কন্যাশ্রী" in q or "कन्याश्री" in q:
            actions.append({"label": "🌐 Kanyashree Portal", "type": "link", "url": "https://www.wbkanyashree.gov.in"})
        elif "rupashree" in q or "রূপশ্রী" in q or "रूपश्री" in q:
            actions.append({"label": "🌐 Rupashree Portal", "type": "link", "url": "https://wbrupashree.gov.in"})

        if any(w in q for w in ["grievance", "shikayat", "darji", "letter", "অভিযোগ", "দরখাস্ত"]):
            actions.append({"label": "📝 Grievance Drafter", "type": "action", "action": "grievance-drafter"})
        if any(w in q for w in ["eligibility", "patrata", "jogota", "যোগ্যতা", "पात्रता"]):
            actions.append({"label": "⚖️ Eligibility Wizard", "type": "action", "action": "eligibility-wizard"})

        # Always ensure at least 2 actions
        if not actions:
            actions = [
                {"label": "📋 Schemes Directory", "type": "action", "action": "schemes-and-docs"},
                {"label": "⚖️ Eligibility Wizard", "type": "action", "action": "eligibility-wizard"}
            ]
        return actions[:3]
