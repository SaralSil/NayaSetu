/**
 * NayaSetu AI - WhatsApp Dark Theme Chatbot Assistant
 * Dedicated AI assistant for West Bengal Government Schemes, Scholarships,
 * Document Checklists, Official Portal Links & Website Navigation.
 * Full multi-lingual support: English, Bengali (বাংলা), and Hindi (हिंदी).
 * Features live Gemini LLM generation, language switching, and comprehensive client intelligence.
 */
(function() {
  // Prevent multiple initializations
  if (window.NayaSetuChatbotLoaded) return;
  window.NayaSetuChatbotLoaded = true;

  // Configuration & Auto API Base Resolution
  window.API_BASE = window.API_BASE || (window.location.origin && window.location.origin.includes('8000') ? '/api' : 'http://127.0.0.1:8000/api');
  const getApiChatbotUrl = () => {
    const base = (window.API_BASE || '').replace(/\/$/, '');
    return base.endsWith('/api') ? base + '/chatbot/' : base + '/api/chatbot/';
  };

  // Active Language State (persisted in localStorage, default 'en')
  let currentLang = localStorage.getItem('nayasetu_chat_lang') || 'en';

  // System Prompt for Client-Side Gemini direct calls
  const GEMINI_SYSTEM_PROMPT = `
You are "NayaSetu AI" (नया सेतु AI / ন্যায়সেতু AI) — an intelligent, compassionate citizen rights and government welfare schemes assistant for the citizens of West Bengal.

CRITICAL IDENTITY RULES:
1. NEVER identify yourself as Google, OpenAI, ChatGPT, Claude, or Gemini. Your name is strictly "NayaSetu AI".
2. If asked who you are, state clearly that you are "NayaSetu AI", dedicated exclusively to the NayaSetu project and West Bengal welfare schemes.

STRICT DOMAIN & SCOPE GUARDRAILS:
1. You are EXCLUSIVELY dedicated to the NayaSetu project, its tools, and West Bengal Government Citizen Rights, Welfare Schemes & Scholarships.
2. YOU MUST ONLY answer queries related to:
   - The NayaSetu platform, its purpose, and navigation (Eligibility Wizard, Schemes Directory, Grievance Drafter, Notice Explainer, Helpline & Administrative Offices Directory).
   - West Bengal Government welfare schemes, scholarships, benefits, eligibility criteria, mandatory document checklists (single bank passbook, Aadhaar-NPCI DBT), official government portals, application methods, rejection remedies, and grievance petitions.
   - Greetings, identity, and language switching.
3. OUT OF SCOPE REFUSAL:
   If the user asks ANY question outside this scope (e.g. general world knowledge, international news, entertainment, cooking recipes, math/physics homework, unrelated programming code, sports trivia, personal chit-chat unrelated to NayaSetu):
   YOU MUST NOT ANSWER the unrelated topic. Politely refuse and state: "I am NayaSetu AI. I can only answer questions regarding the NayaSetu project and West Bengal Government welfare schemes."

STRICT SCHEME REDIRECTION REQUIREMENT:
Whenever you answer about any West Bengal scheme:
- Provide full scheme details: financial benefits, eligibility criteria, and mandatory documents checklist.
- ALWAYS clearly provide the Official Government Portal link and URL (e.g. [Visit Official Portal](URL)).

STRICT LANGUAGE INSTRUCTIONS:
- If user requests or writes in English ("talk in english", "speak in english", etc.), reply entirely in clear, natural English.
- If user requests or writes in Bengali ("বাংলায় বলো", "বাংলায় কথা বলো", etc.), reply entirely in natural, respectful Bengali (বাংলা).
- If user requests or writes in Hindi ("हिंदी में बोलो", "हिंदी में बात करो", etc.), reply in respectful Hindi.
- Use neat Markdown formatting with bullet points and clean emojis.
`;

  // Multilingual Knowledge Base for Client-Side Instant Replies
  const KNOWLEDGE_BASE = {
    ayushman_bharat: {
      match: ["ayushman", "pmjay", "আয়ুষ্মান", "ভারত", "आयुष्मान", "वय वंदना", "vay vandana", "70", "senior citizen health"],
      en: {
        reply: "🏥 **Ayushman Bharat (AB-PMJAY) & Vay Vandana 70+:**\n\n💰 **Coverage**: ₹5,00,000 cashless health insurance per family/year across 29,000+ empaneled hospitals across India + Universal free ₹5 Lakh health cover for ALL senior citizens aged 70+ without any income cap.\n👥 **Eligibility**: NFSA/Ration card families and all senior citizens aged 70 years and above.\n\n📑 **Required Documents:**\n• Aadhaar cards of all family members (mandatory for biometric e-KYC)\n• Digital Ration Card\n• Age proof for 70+ senior citizen (Aadhaar / Voter ID)\n• Active mobile number linked to Aadhaar\n\n🌐 **Official Portal:** [Ayushman Bharat Portal](https://beneficiary.nha.gov.in)\n📍 **How to Apply:** beneficiary.nha.gov.in, Ayushman App, or nearest Common Service Center (CSC).",
        actions: [
          { label: "🌐 PM-JAY Portal", url: "https://beneficiary.nha.gov.in", type: "link" },
          { label: "📋 Health Schemes", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🏥 **আয়ুষ্মান ভারত (AB-PMJAY) ও বয় বন্দনা ৭০+:**\n\n💰 **স্বাস্থ্য সুবিধা**: সারা ভারতের ২৯,০০০+ হাসপাতালে প্রতি পরিবার প্রতি বছর ₹৫ লাখ পর্যন্ত ক্যাশলেস চিকিৎসা + ৭০ ঊর্ধ্ব সমস্ত প্রবীণ নাগরিকদের জন্য সার্বজনীন বিনামূল্যে বিশেষ ₹৫ লাখের বয় বন্দনা স্বাস্থ্য কার্ড (কোনো আয়সীমা নেই)।\n👥 **যোগ্যতা**: ডিজিটাল রেশন কার্ডধারী পরিবার এবং ৭০ বছর বা তদূর্ধ্ব প্রবীণ নাগরিক।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পরিবারের সকলের আধার কার্ড (বায়োমেট্রিক ই-কেওয়াইসি)\n• ডিজিটাল রেশন কার্ড\n• ৭০+ প্রবীণদের বয়সের প্রমাণপত্র (আধার বা ভোটার কার্ড)\n• আধার লিঙ্ক করা মোবাইল নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [Ayushman Bharat Portal](https://beneficiary.nha.gov.in)\n📍 **আবেদন স্থল:** beneficiary.nha.gov.in, আয়ুষ্মান অ্যাপ বা নিকটবর্তী CSC কেন্দ্র।",
        actions: [
          { label: "🌐 আয়ুষ্মান পোর্টাল", url: "https://beneficiary.nha.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏥 **आयुष्मान भारत (AB-PMJAY) व वय वंदना 70+:**\n\n💰 **स्वास्थ्य लाभ**: देशभर के 29,000+ अस्पतालों में प्रति परिवार ₹5 लाख तक का कैशलेस इलाज + 70 वर्ष से अधिक के सभी बुजुर्गों हेतु निःशुल्क वय वंदना कार्ड।\n👥 **पात्रता**: राशन कार्ड धारक परिवार और 70 वर्ष से अधिक के सभी वरिष्ठ नागरिक।\n\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, डिजिटल राशन कार्ड, 70+ बुजुर्गों का आयु प्रमाण।\n\n🌐 **ऑफिशियल पोर्टल:** [Ayushman Bharat Portal](https://beneficiary.nha.gov.in)",
        actions: [
          { label: "🌐 आयुष्मान पोर्टल", url: "https://beneficiary.nha.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    wbscc: {
      match: ["student credit card", "wbscc", "क्रेडिट कार्ड", "ক্রেডিট কার্ড", "10 lakh", "loan", "এডুকেশন লোন", "education loan"],
      en: {
        reply: "💳 **West Bengal Student Credit Card (WBSCC):**\n\n💰 **Facility**: Education loan up to ₹10 Lakh at a nominal 4% simple interest for higher studies in India and abroad.\n🎯 **Eligibility**: Resident of West Bengal for at least 10 years, age up to 40 years, enrolled in Class 10/12/UG/PG/Doctoral/Competitive coaching.\n\n📑 **Documents Required:**\n• Photo and signature of student and co-borrower (guardian)\n• Student's Aadhaar card / Class 10 registration certificate\n• Co-borrower's PAN card & address proof\n• Course fee structure & admission receipt from institute\n• Bank details of student and co-borrower\n\n🌐 **Official Portal:** [WBSCC Portal (wbscc.wb.gov.in)](https://wbscc.wb.gov.in)",
        actions: [
          { label: "🌐 WBSCC Portal", url: "https://wbscc.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "💳 **পশ্চিমবঙ্গ স্টুডেন্ট ক্রেডিট কার্ড (WBSCC):**\n\n💰 **সুবিধা**: উচ্চশিক্ষার জন্য মাত্র ৪% সরল সুদে সর্বোচ্চ ১০ লক্ষ টাকা পর্যন্ত শিক্ষা ঋণ (ভারত বা বিদেশে পড়ার জন্য)।\n🎯 **যোগ্যতা**: পশ্চিমবঙ্গে ১০ বছর বসবাসকারী, সর্বোচ্চ বয়স ৪০ বছর, যেকোনো উচ্চশিক্ষা বা প্রতিযোগিতামূলক কোর্সে পাঠরত।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• শিক্ষার্থী ও অভিভাবকের ছবি ও স্বাক্ষর\n• শিক্ষার্থীর আধার কার্ড বা মাধ্যমিক রেজিস্ট্রেশন\n• অভিভাবকের প্যান কার্ড ও ঠিকানার প্রমাণ\n• শিক্ষাপ্রতিষ্ঠানের কোর্স ফি কাঠামো ও ভর্তির রশিদ\n• উভয়ের ব্যাঙ্ক অ্যাকাউন্ট নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [WBSCC Portal (wbscc.wb.gov.in)](https://wbscc.wb.gov.in)",
        actions: [
          { label: "🌐 WBSCC Portal", url: "https://wbscc.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "💳 **West Bengal Student Credit Card (WBSCC):**\n\n💰 **सुविधा**: मात्र 4% सरल ब्याज पर ₹10 लाख तक शिक्षा ऋण उच्च शिक्षा (भारत या विदेश) हेतु।\n🎯 **पात्रता**: प. बंगाल में 10 वर्ष से निवासी, अधिकतम आयु 40 वर्ष।\n\n📑 **ज़रूरी दस्तावेज़:** छात्र व अभिभावक की फोटो व हस्ताक्षर, आधार, पैन, कोर्स फीस स्ट्रक्चर व एडमिशन रसीद।\n\n🌐 **ऑफिशियल पोर्टल:** [WBSCC Portal (wbscc.wb.gov.in)](https://wbscc.wb.gov.in)",
        actions: [
          { label: "🌐 WBSCC Portal", url: "https://wbscc.wb.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    pmis: {
      match: ["pmis", "pm internship", "prime minister internship", "ইন্টার্নশিপ", "ইন্টার্ন", "ইন্টার্নশিপ প্রকল্প", "इंटर्नशिप", "प्रधानमंत्री इंटर्नशिप", "pminternship"],
      en: {
        reply: "💼 **Prime Minister Internship Scheme (PMIS):**\n\n💰 **Stipend & Grant**: ₹5,000/month stipend (₹4,500 from Central Gov + ₹500 from Company CSR) + ₹6,000 one-time incidental grant for a 12-month internship in top 500 Indian companies.\n🎯 **Eligibility**: Indian citizens aged 21 to 24 years. Passed Class 10/12, ITI, Polytechnic Diploma, or Undergraduate degrees (BA, B.Sc, B.Com, BCA, BBA, B.Pharma). Must not be in full-time employment or full-time higher education. Family annual income ≤ ₹8,00,000.\n\n📑 **Needed Documents:**\n• **Aadhaar Card** (Mandatory for e-KYC)\n• **Educational Certificates & Marksheets** (10th/12th/ITI/Diploma/Graduation)\n• **Proof of Age** (Birth Certificate / School Leaving / Admit Card)\n• **Aadhaar-Seeded Bank Account Passbook** (Aadhaar-NPCI DBT active)\n• **Recent Passport-Size Photograph**\n\n🌐 **Official Portal:** [PM Internship Portal](https://pminternship.mca.gov.in)",
        actions: [
          { label: "🌐 PMIS Official Portal", url: "https://pminternship.mca.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "💼 **প্রধানমন্ত্রী ইন্টার্নশিপ প্রকল্প (PMIS):**\n\n💰 **স্টাইপেন্ড ও অনুদান**: দেশের শীর্ষ ৫০০ সংস্থায় ১২ মাসের কাজের সুযোগ, মাসিক ₹৫,০০০ অনুদান এবং এককালীন ₹৬,০০০ টাকার আর্থিক সাহায্য।\n🎯 **যোগ্যতা**: ২১ থেকে ২৪ বছর বয়সী ভারতীয় নাগরিক। মাধ্যমিক, উচ্চমাধ্যমিক, আইটিআই, ডিপ্লোমা বা স্নাতক পাস। পারিবারিক বার্ষিক আয় ৮ লক্ষ টাকার মধ্যে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• **আধার কার্ড** (ই-কেওয়াইসি বাধ্যতামূলক)\n• **শিক্ষাগত যোগ্যতার সার্টিফিকেট ও মার্কশিট**\n• **বয়সের প্রমাণপত্র** (জন্ম সার্টিফিকেট / এডমিট কার্ড)\n• **আধার লিঙ্ক করা একক ব্যাঙ্ক পাসবই**\n• **পাসপোর্ট সাইজ রঙিন ছবি**\n\n🌐 **অফিসিয়াল পোর্টাল:** [PM Internship Portal](https://pminternship.mca.gov.in)",
        actions: [
          { label: "🌐 পিএমআইএস পোর্টাল", url: "https://pminternship.mca.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" },
          { label: "⚖️ যোগ্যতা যাচাই", action: "eligibility-wizard" }
        ]
      },
      hi: {
        reply: "💼 **प्रधानमंत्री इंटर्नशिप योजना (PMIS):**\n\n💰 **वजीफा व अनुदान**: 12 महीने की इंटर्नशिप, ₹5,00,000/माह वजीफा + ₹6,000 एकमुश्त सहायता।\n🎯 **पात्रता**: 21 से 24 वर्ष के युवा, 10वीं/12वीं/आईटीआई/डिप्लोमा/स्नातक पास, पारिवारिक आय ≤ ₹8 लाख।\n\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, शैक्षणिक अंकपत्र, आयु प्रमाण, आधार-सीडेड बैंक खाता, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [PM Internship Portal](https://pminternship.mca.gov.in)",
        actions: [
          { label: "🌐 PMIS ऑफिशियल पोर्टल", url: "https://pminternship.mca.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    rksy: {
      match: ["rksy", "rajya khadya", "খাদ্য সুরক্ষা", "খাদ্য সাথী", "rksy-1", "rksy-2", "राज्य खाद्य", "खाद्य सुरक्षा", "duare ration"],
      en: {
        reply: "🍚 **Rajya Khadya Suraksha Yojana (RKSY / Food Security Scheme):**\n\n💰 **Benefit**: Subsidized & free food grains (Rice & Wheat, 5kg/head/month) delivered through fair price shops and Duare Ration under RKSY-I and RKSY-II.\n👥 **Eligibility**: Permanent residents of West Bengal belonging to BPL, Antyodaya Anna Yojana (AAY), or Priority Household (PHH) facing economic disadvantage.\n\n📑 **Needed Documents:**\n• **Aadhaar Cards of All Family Members**\n• **Existing Ration Card / Family Card** (if updating or migrating)\n• **Proof of Residence** (Voter ID / EPIC, Electricity Bill)\n• **Income Certificate / BPL Certificate**\n• **Active Mobile Number and Passport Photo of Head of Family**\n\n🌐 **Official Portal:** [WB Food & Supplies Portal](https://food.wb.gov.in)",
        actions: [
          { label: "🌐 WB Food Portal", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🍚 **রাজ্য খাদ্য সুরক্ষা যোজনা (RKSY / খাদ্য সাথী):**\n\n💰 **সুবিধা**: RKSY-I ও RKSY-II কার্ডে পরিবারগুলিকে প্রতি মাসে বিনামূল্যে চাল ও গম এবং দুয়ারে রেশন পরিষেবা।\n👥 **যোগ্যতা**: পশ্চিমবঙ্গের স্থায়ী বাসিন্দা ও অর্থনৈতিকভাবে পিছিয়ে থাকা পরিবার।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পরিবারের সকলের আধার কার্ড\n• বর্তমান ডিজিটাল রেশন কার্ড (যদি থাকে)\n• বসবাসের প্রমাণ (ভোটার কার্ড / বিদ্যুৎ বিল)\n• আয়ের শংসাপত্র / বিপিএল সার্টিফিকেট\n• পরিবারের প্রধানের মোবাইল নম্বর ও ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [WB Food Portal](https://food.wb.gov.in)",
        actions: [
          { label: "🌐 খাদ্য দপ্তর পোর্টাল", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🍚 **राज्य खाद्य सुरक्षा योजना (RKSY / Food Security):**\n\n💰 **लाभ**: RKSY-I और RKSY-II के तहत रियायती व मुफ्त अनाज (चावल व गेहूं)।\n📑 **ज़रूरी दस्तावेज़:** सभी सदस्यों के आधार कार्ड, मौजूदा राशन कार्ड, निवास प्रमाण, आय प्रमाण पत्र, मुखिया का फोटो व मोबाइल नंबर।\n\n🌐 **ऑफिशियल पोर्टल:** [WB Food Portal](https://food.wb.gov.in)",
        actions: [
          { label: "🌐 खाद्य पोर्टल पर जाएं", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    rojgar_seva: {
      match: ["rojgar", "rojgar seva", "রোজগার সেবা", "রোজগার", "employment bank", "এমপ্লয়মেন্ট ব্যাঙ্ক", "रोजगार", "रोजगार सेवा"],
      en: {
        reply: "💼 **Rojgar Seva Portal (PBSSD / Employment Services):**\n\n💰 **Facility**: Statewide employment matching, job vacancy notifications, vocational placement, and youth skill apprenticeships.\n🎯 **Eligibility**: Resident job seekers of West Bengal aged 18 to 45 years. Educational qualifications range from Class 8th/10th pass to ITI, Diploma, and Graduation.\n\n📑 **Needed Documents:**\n• **Aadhaar Card / Voter ID (EPIC)**\n• **Academic Certificates, Diplomas, or ITI Trade Pass Certificates**\n• **Resume / Curriculum Vitae (CV)**\n• **Caste Certificate and Disability Certificate** (if applicable)\n• **Active Mobile Number and Valid Email Address**\n\n🌐 **Official Portal:** [Employment Bank WB](https://employmentbankwb.gov.in)",
        actions: [
          { label: "🌐 Employment Bank Portal", url: "https://employmentbankwb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "💼 **রোজগার সেবা পোর্টাল (PBSSD / এমপ্লয়মেন্ট ব্যাঙ্ক):**\n\n💰 **সুবিধা**: পশ্চিমবঙ্গের চাকরিপ্রার্থীদের জন্য সরকারি ও বেসরকারি চাকরি এবং শিক্ষানবিশী প্রশিক্ষণের সুযোগ।\n🎯 **যোগ্যতা**: পশ্চিমবঙ্গের স্থায়ী বাসিন্দা কর্মপ্রার্থী, বয়স ১৮ থেকে ৪৫ বছর।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড / ভোটার আইডি\n• শিক্ষাগত শংসাপত্র ও মার্কশিট\n• বায়োডাটা / জীবনবৃত্তান্ত (CV)\n• জাতিগত শংসাপত্র (প্রযোজ্য ক্ষেত্রে)\n• মোবাইল নম্বর ও ইমেল আইডি\n\n🌐 **অফিসিয়াল পোর্টাল:** [Employment Bank Portal](https://employmentbankwb.gov.in)",
        actions: [
          { label: "🌐 এমপ্লয়মেন্ট ব্যাঙ্ক পোর্টাল", url: "https://employmentbankwb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "💼 **रोजगार सेवा पोर्टल (PBSSD / Employment Services):**\n\n💰 **सुविधा**: नौकरी चाहने वालों के लिए राज्यव्यापी रोजगार पंजीकरण व शिक्षुता अवसर।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, शैक्षणिक प्रमाण पत्र, बायोडाटा (CV), जाति प्रमाण, मोबाइल व ईमेल।\n\n🌐 **ऑफिशियल पोर्टल:** [Employment Bank Portal](https://employmentbankwb.gov.in)",
        actions: [
          { label: "🌐 रोजगार पोर्टल पर जाएं", url: "https://employmentbankwb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    soil_health_card: {
      match: ["soil health", "soil health card", "মৃত্তিকা", "মৃত্তিকা স্বাস্থ্য", "মাটি পরীক্ষা", "मृदा स्वास्थ्य", "मृदा कार्ड", "soil"],
      en: {
        reply: "🌱 **Soil Health Card Scheme:**\n\n💰 **Benefit**: Free laboratory soil analysis reporting 12 parameters and scientific fertilizer advisory issued every 3 years.\n👨‍🌾 **Eligibility**: All Indian farmers cultivating or holding agricultural land in West Bengal (small, marginal, large, tenant farmers, and sharecroppers). No income ceiling.\n\n📑 **Needed Documents:**\n• **Aadhaar Card** of the farmer\n• **Land Record Documents** (RoR / Khatian / Porcha / Khasra)\n• **Tenancy or Lease Agreement** (for tenant farmers/sharecroppers)\n• **Bank Account Passbook Copy**\n• **Contact Mobile Number**\n\n🌐 **Official Portal:** [National Soil Health Portal](https://soilhealth.dac.gov.in)",
        actions: [
          { label: "🌐 Soil Health Portal", url: "https://soilhealth.dac.gov.in", type: "link" },
          { label: "📋 Agriculture Schemes", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🌱 **মৃত্তিকা স্বাস্থ্য কার্ড প্রকল্প (Soil Health Card Scheme):**\n\n💰 **সুবিধা**: বিনামূল্যে জমির মাটির গুণমান পরীক্ষা এবং ফসলভিত্তিক সুনির্দিষ্ট সারের পরিমাণ নির্ধারণ।\n👨‍🌾 **যোগ্যতা**: পশ্চিমবঙ্গের সমস্ত কৃষক, জমির মালিক ও বর্গাদার।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• কৃষকের আধার কার্ড\n• জমির পরচা বা খতিয়ান (RoR)\n• বর্গাদার বা লিজ চুক্তিপত্র (প্রযোজ্য ক্ষেত্রে)\n• ব্যাঙ্ক পাসবইয়ের জেরক্স ও মোবাইল নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [Soil Health Portal](https://soilhealth.dac.gov.in)",
        actions: [
          { label: "🌐 মৃত্তিকা স্বাস্থ্য পোর্টাল", url: "https://soilhealth.dac.gov.in", type: "link" },
          { label: "📋 কৃষি প্রকল্প তালিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🌱 **मृदा स्वास्थ्य कार्ड योजना (Soil Health Card):**\n\n💰 **लाभ**: किसानों को मिट्टी की मुफ्त वैज्ञानिक जांच व 12 पोषक तत्वों की स्थिति का कार्ड।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, जमीन का पर्चा (RoR/खतियान), बटाईदार अनुबंध (यदि लागू हो), बैंक पासबुक, मोबाइल नंबर।\n\n🌐 **ऑफिशियल पोर्टल:** [Soil Health Portal](https://soilhealth.dac.gov.in)",
        actions: [
          { label: "🌐 सॉइल हेल्थ पोर्टल", url: "https://soilhealth.dac.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    sukanya_samriddhi: {
      match: ["sukanya", "samriddhi", "ssy", "সুকন্যা", "সুকন্যা সমৃদ্ধি", "सुकन्या", "सुकन्या समृद्धि", "girl savings"],
      en: {
        reply: "👧 **Sukanya Samriddhi Yojana (SSY):**\n\n💰 **Benefit**: High sovereign interest (8.2%+ p.a.) with Triple Tax Exemption (EEE) under Section 80C for girl child higher education and marriage.\n🎯 **Eligibility**: Girl child aged under 10 years at account opening. Opened by parents/guardians. Max 2 accounts per family (triplet/twin exceptions allowed). Minimum deposit ₹250/year.\n\n📑 **Needed Documents:**\n• **Birth Certificate of the Girl Child**\n• **Identity Proof of Parent/Guardian** (Aadhaar Card, PAN Card)\n• **Address Proof of Parent/Guardian** (Voter ID, Utility Bill, Passport)\n• **Passport-Size Photographs** of child and guardian\n• **Medical Certificate** (if opening for twins/triplets on second delivery)\n\n🌐 **Official Portal:** [India Post SSY Portal](https://www.indiapost.gov.in)",
        actions: [
          { label: "🌐 India Post SSY Portal", url: "https://www.indiapost.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "👧 **সুকন্যা সমৃদ্ধি যোজনা (SSY):**\n\n💰 **সুবিধা**: কন্যা সন্তানের উচ্চশিক্ষার জন্য সর্বোচ্চ সরকারি সুদের (৮.২%+) সম্পূর্ণ করমুক্ত সঞ্চয় যোজনা।\n🎯 **যোগ্যতা**: ১০ বছর বা তার কম বয়সী কন্যা সন্তানের নামে অভিভাবক কর্তৃক খোলা যায়।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• কন্যা সন্তানের জন্ম শংসাপত্র\n• অভিভাবকের আধার কার্ড ও প্যান কার্ড\n• ঠিকানার প্রমাণপত্র (ভোটার কার্ড / বিদ্যুৎ বিল)\n• সন্তান ও অভিভাবকের পাসপোর্ট ছবি\n• যমজ সন্তানের ক্ষেত্রে মেডিকেল সার্টিফিকেট\n\n🌐 **অফিসিয়াল পোর্টাল:** [India Post Portal](https://www.indiapost.gov.in)",
        actions: [
          { label: "🌐 পোস্ট অফিস সুকন্যা পোর্টাল", url: "https://www.indiapost.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "👧 **सुकन्या समृद्धि योजना (SSY):**\n\n💰 **लाभ**: 8.2%+ ब्याज दर और धारा 80C के तहत 100% टैक्स फ्री रिटर्न।\n🎯 **पात्रता**: 10 वर्ष से कम आयु की बालिकाओं के लिए माता-पिता द्वारा खाता।\n\n📑 **ज़रूरी दस्तावेज़:** बालिका का जन्म प्रमाण पत्र, अभिभावक का आधार/पैन, निवास प्रमाण, दोनों की पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [India Post Portal](https://www.indiapost.gov.in)",
        actions: [
          { label: "🌐 सुकन्या समृद्धि पोर्टल", url: "https://www.indiapost.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    swachh_bharat: {
      match: ["swachh bharat", "swachh", "ihhl", "nirmal bangla", "নির্মল বাংলা", "শৌচাগার", "টয়লেট", "स्वच्छ भारत", "शौचालय", "12000"],
      en: {
        reply: "🚽 **Swachh Bharat Mission (Grameen IHHL & Urban Sanitation):**\n\n💰 **Financial Incentive**: ₹12,000 direct bank transfer for rural household sanitary toilet construction (IHHL) + urban community sanitation subsidies.\n👥 **Eligibility**: Households lacking access to functional sanitary toilets. Priority given to BPL and identified APL (SC/ST, small/marginal farmers, female-headed households).\n\n📑 **Needed Documents:**\n• **Aadhaar Card of Applicant** (Head of Household)\n• **Bank Passbook Details Linked with Aadhaar** (Account No. and IFSC)\n• **Ration Card / BPL Card**\n• **Active Mobile Number**\n• **Geo-Tagged Photographs of Toilet Construction Site**\n\n🌐 **Official Portal:** [Swachh Bharat Mission Portal](https://sbm.gov.in)",
        actions: [
          { label: "🌐 SBM Official Portal", url: "https://sbm.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🚽 **স্বচ্ছ ভারত মিশন / মিশন নির্মল বাংলা শৌচাগার অনুদান (IHHL):**\n\n💰 **আর্থিক অনুদান**: গ্রামীণ পরিবারে স্বাস্থ্যসম্মত পাকা শৌচাগার নির্মাণের জন্য সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ₹১২,০০০ আর্থিক সহায়তা।\n👥 **যোগ্যতা**: গ্রামীণ ও পৌর এলাকার যেসকল পরিবারের শৌচাগার নেই। বিপিএল ও অগ্রাধিকারপ্রাপ্ত পরিবার।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পরিবারের প্রধানের আধার কার্ড\n• আধার লিঙ্ক করা একক ব্যাঙ্ক পাসবই\n• ডিজিটাল রেশন কার্ড বা বিপিএল কার্ড\n• সক্রিয় মোবাইল নম্বর\n• শৌচাগার নির্মাণের জিও-ট্যাগ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [SBM Portal](https://sbm.gov.in)",
        actions: [
          { label: "🌐 নির্মল বাংলা পোর্টাল", url: "https://sbm.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🚽 **स्वच्छ भारत मिशन (शौचालय अनुदान ₹12,000):**\n\n💰 **लाभ**: ग्रामीण क्षेत्रों में व्यक्तिगत घरेलू शौचालय (IHHL) निर्माण हेतु ₹12,000 सीधे बैंक खाते में।\n📑 **ज़रूरी दस्तावेज़:** परिवार मुखिया का आधार कार्ड, बैंक पासबुक (आधार लिंक्ड), राशन कार्ड/बीपीएल कार्ड, मोबाइल नंबर, शौचालय निर्माण की जियो-टैग फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [SBM Portal](https://sbm.gov.in)",
        actions: [
          { label: "🌐 स्वच्छ भारत पोर्टल", url: "https://sbm.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    taposili_bandhu: {
      match: ["taposili", "taposhili", "taposili bandhu", "তফসিলী", "তপশিলী", "তফসিলী বন্ধু", "তপশিলী বন্ধু", "तपशिली बंधु", "sc pension", "এসসি পেনশন"],
      en: {
        reply: "👴 **Taposili Bandhu Scheme (West Bengal SC Old Age Pension):**\n\n💰 **Monthly Pension**: ₹1,000/month direct DBT pension credited to bank account for life.\n👥 **Eligibility**: Permanent residents of West Bengal belonging to Scheduled Caste (SC) category aged 60 years or above. Must not receive other government social security pensions.\n\n📑 **Needed Documents:**\n• **SC Caste Certificate** (issued by SDO/competent authority)\n• **Proof of Age** (Admit Card, Birth Certificate, or EPIC showing 60+ years)\n• **Aadhaar Card and Digital Ration Card**\n• **Voter ID Card (EPIC)**\n• **Bank Passbook Copy** (Aadhaar-linked DBT account)\n• **Passport-Sized Photographs**\n\n🌐 **Official Portal:** [Jai Bangla Portal](https://jaibangla.wb.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps or local BDO / SDO office.",
        actions: [
          { label: "🌐 Jai Bangla Portal", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "📝 Draft BDO Letter", action: "grievance-drafter" }
        ]
      },
      bn: {
        reply: "👴 **তফসিলী বন্ধু প্রকল্প (পশ্চিমবঙ্গ তফশিলী জাতি প্রবীণ পেনশন):**\n\n💰 **মাসিক পেনশন**: ৬০ বছর বা তদূর্ধ্ব এসসি (SC) প্রবীণ নাগরিকদের জন্য প্রতি মাসে ₹১,০০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি পেনশন।\n👥 **যোগ্যতা**: পশ্চিমবঙ্গের তপশিলী জাতিভুক্ত প্রবীণ নাগরিক (৬০+ বছর)। অন্য সরকারি পেনশন প্রাপকরা আওতাভুক্ত নন।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• **এসসি (SC) জাতিগত শংসাপত্র** (SDO দ্বারা প্রদত্ত)\n• **বয়সের প্রমাণপত্র** (এডমিট কার্ড, বার্থ সার্টিফিকেট বা ভোটার কার্ড)\n• **আধার কার্ড ও ডিজিটাল রেশন কার্ড**\n• **ভোটার কার্ড (EPIC)**\n• **ব্যাঙ্ক পাসবই** (আধার লিঙ্ক করা ডিবিটি অ্যাকাউন্ট)\n• **পাসপোর্ট সাইজ রঙিন ছবি**\n\n🌐 **অফিসিয়াল পোর্টাল:** [Jai Bangla Portal](https://jaibangla.wb.gov.in)",
        actions: [
          { label: "🌐 জয় বাংলা পোর্টাল", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" },
          { label: "📝 দরখাস্ত ড্রাফটার", action: "grievance-drafter" }
        ]
      },
      hi: {
        reply: "👴 **तपशिली बंधु योजना (पश्चिम बंगाल SC पेंशन):**\n\n💰 **मासिक पेंशन**: 60 वर्ष या उससे अधिक आयु के अनुसूचित जाति (SC) के नागरिकों को ₹1,000 प्रति माह सीधे बैंक खाते में।\n📑 **ज़रूरी दस्तावेज़:** SC जाति प्रमाण पत्र (SDO द्वारा जारी), आयु प्रमाण, आधार व डिजिटल राशन कार्ड, वोटर कार्ड, बैंक पासबुक, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [Jai Bangla Portal](https://jaibangla.wb.gov.in)",
        actions: [
          { label: "🌐 जय बांग्ला पोर्टल", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    udyam_msme: {
      match: ["udyam", "udyam registration", "msme registration", "উদ্যম", "উদ্যম রেজিস্ট্রেশন", "ক্ষুদ্র শিল্প", "उद्यम", "उद्यम पंजीकरण", "एमएसएमई"],
      en: {
        reply: "🏭 **Udyam Registration (MSME):**\n\n💰 **Benefits**: Official Government of India paperless MSME recognition, priority sector bank lending, collateral-free credit guarantee (CGTMSE), and subsidies on electricity & patents.\n🎯 **Eligibility**: Micro (Investment ≤ ₹1 Cr & Turnover ≤ ₹5 Cr), Small (Investment ≤ ₹10 Cr & Turnover ≤ ₹50 Cr), and Medium (Investment ≤ ₹50 Cr & Turnover ≤ ₹250 Cr) enterprises.\n\n📑 **Needed Documents:**\n• **Aadhaar Card of Proprietor/Partner/Director** (Linked with mobile for OTP)\n• **PAN Card** (Proprietor or business entity)\n• **GSTIN** (If applicable under turnover laws)\n• **Business Address Proof & Bank Details** (Account No. and IFSC)\n• **NIC Code** related to manufacturing or service activity\n\n🌐 **Official Portal:** [Udyam Registration Portal](https://udyamregistration.gov.in)",
        actions: [
          { label: "🌐 Udyam Official Portal", url: "https://udyamregistration.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🏭 **উদ্যম রেজিস্ট্রেশন (MSME):**\n\n💰 **সুবিধা**: ক্ষুদ্র ও মাঝারি শিল্পের জন্য বিনামূল্যে সরকারি স্বীকৃতিপত্র, সহজ ব্যাঙ্ক ঋণ ও সরকারি টেন্ডারে অগ্রাধিকার।\n🎯 **যোগ্যতা**: নতুন বা বিদ্যমান ক্ষুদ্র, ছোট ও মাঝারি ব্যবসায়ী।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• ব্যবসার মালিকের আধার কার্ড (মোবাইল লিঙ্ক)\n• প্যান কার্ড (ব্যক্তিগত বা বাণিজ্যিক)\n• জিএসটি নম্বর (প্রযোজ্য ক্ষেত্রে)\n• ব্যবসার ঠিকানা ও ব্যাঙ্ক অ্যাকাউন্টের বিবরণ\n• এনআইসি (NIC) কোড\n\n🌐 **অফিসিয়াল পোর্টাল:** [Udyam Registration Portal](https://udyamregistration.gov.in)",
        actions: [
          { label: "🌐 উদ্যম সরকারি পোর্টাল", url: "https://udyamregistration.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏭 **उद्यम पंजीकरण (MSME Registration):**\n\n💰 **लाभ**: आधिकारिक सरकारी एमएसएमई प्रमाण पत्र, सस्ता बैंक लोन व सरकारी सब्सिडी।\n📑 **ज़रूरी दस्तावेज़:** मालिक का आधार कार्ड (ओटीपी हेतु मोबाइल लिंक्ड), पैन कार्ड, जीएसटी नंबर (यदि लागू हो), बैंक खाता विवरण, व्यवसाय स्थल का प्रमाण।\n\n🌐 **ऑफिशियल पोर्टल:** [Udyam Portal](https://udyamregistration.gov.in)",
        actions: [
          { label: "🌐 उद्यम पोर्टल पर जाएं", url: "https://udyamregistration.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    utkarsh_bangla: {
      match: ["utkarsh", "utkarsh bangla", "উৎকর্ষ", "উৎকর্ষ বাংলা", "vocational training", "কারিগরি প্রশিক্ষণ", "বৃত্তিমূলক", "उत्कर्ष बांग्ला"],
      en: {
        reply: "⚙️ **Utkarsh Bangla (PBSSD Vocational Skill Training):**\n\n💰 **Benefit**: 100% free industry-aligned vocational skills training in certified trades (Healthcare, IT, Automotive, Electronics) with assured placement assistance.\n🎯 **Eligibility**: Permanent residents of West Bengal aged 18 to 40 years. School dropouts, Class 8th/10th pass, or higher depending on the course trade.\n\n📑 **Needed Documents:**\n• **Aadhaar Card and Voter ID (EPIC)**\n• **Academic Marksheets of Highest Qualification** (8th/10th/12th)\n• **Domicile Certificate / Address Proof**\n• **Bank Passbook Copy**\n• **Passport-Size Photographs**\n• **Caste Certificate** (if seeking reserved seat benefits)\n\n🌐 **Official Portal:** [Utkarsh Bangla Portal](https://pbssd.gov.in)",
        actions: [
          { label: "🌐 Utkarsh Bangla Portal", url: "https://pbssd.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "⚙️ **উৎকর্ষ বাংলা প্রকল্প (PBSSD কারিগরি ও বৃত্তিমূলক প্রশিক্ষণ):**\n\n💰 **সুবিধা**: সম্পূর্ণ বিনামূল্যে আধুনিক শিল্পের উপযোগী কারিগরি প্রশিক্ষণ এবং সফল উত্তীর্ণদের চাকরির সুযোগ।\n🎯 **যোগ্যতা**: ১৮ থেকে ৪০ বছর বয়সী পশ্চিমবঙ্গের স্থায়ী বাসিন্দা। অষ্টম/দশম শ্রেণী পাস বা স্কুলছুট।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড ও ভোটার কার্ড\n• শিক্ষাগত যোগ্যতার মার্কশিট\n• বসবাসের প্রমাণপত্র\n• ব্যাঙ্ক পাসবইয়ের কপি\n• পাসপোর্ট সাইজ ছবি\n• জাতিগত শংসাপত্র (প্রযোজ্য ক্ষেত্রে)\n\n🌐 **অফিসিয়াল পোর্টাল:** [PBSSD Portal](https://pbssd.gov.in)",
        actions: [
          { label: "🌐 উৎকর্ষ বাংলা পোর্টাল", url: "https://pbssd.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "⚙️ **उत्कर्ष बांग्ला (PBSSD वोकेशनल ट्रेनिंग):**\n\n💰 **लाभ**: 100% मुफ्त व्यावसायिक कौशल प्रशिक्षण व रोजगार सहायता।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, वोटर आईडी, शैक्षणिक अंकपत्र, निवास प्रमाण, बैंक पासबुक, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [PBSSD Portal](https://pbssd.gov.in)",
        actions: [
          { label: "🌐 उत्कर्ष बांग्ला पोर्टल", url: "https://pbssd.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    medhashree: {
      match: ["medhashree", "মেধাশ্রী", "মেধাশ্রী প্রকল্প", "মেধাশ্রী স্কলারশিপ", "মেধাশ্রী বৃত্তি", "मेधाश्री", "obc scholarship", "ওবিসি স্কলারশিপ"],
      en: {
        reply: "🎓 **West Bengal Medhashree Scheme (OBC Pre-Matric Scholarship):**\n\n💰 **Scholarship Amount**: ₹800/year direct bank transfer for OBC day scholars studying in Classes V to VIII.\n📚 **Eligibility**: Permanent resident of West Bengal. Must belong to Other Backward Classes (OBC) category. Studying in Class V to VIII in a Government / Govt-aided / sponsored school. Must be a day scholar (hostellers not eligible). Family annual income ≤ ₹2,50,000.\n\n📑 **Needed Documents:**\n• **Student’s Aadhaar Card**\n• **Valid OBC Caste Certificate**\n• **Previous Year’s Mark Sheet** (confirming promotion)\n• **CBS-Enabled Bank Account Passbook in Student's Name** (with IFSC)\n• **School Enrollment / Bonafide Certificate** (from Headmaster)\n• **Passport-Size Photograph**\n\n🌐 **Official Portal:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 OASIS Official Portal", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🎓 **পশ্চিমবঙ্গ মেধাশ্রী প্রকল্প (OBC প্রাক-মাধ্যমিক স্কলারশিপ):**\n\n💰 **বৃত্তি রাশি**: পঞ্চম থেকে অষ্টম শ্রেণীতে পাঠরত ওবিসি (OBC) পড়ুয়াদের জন্য বার্ষিক ₹৮০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে।\n📚 **যোগ্যতা**: পশ্চিমবঙ্গের স্থায়ী বাসিন্দা ওবিসি শিক্ষার্থী। সরকারি বা অনুমোদিত বিদ্যালয়ের ডে-স্কলার শিক্ষার্থী। পারিবারিক বার্ষিক আয় ২.৫ লক্ষ টাকার মধ্যে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• শিক্ষার্থীর আধার কার্ড\n• বৈধ ওবিসি (OBC) জাতিগত শংসাপত্র\n• পূর্ববর্তী শ্রেণীর উত্তীর্ণ মার্কশিট\n• ছাত্র/ছাত্রীর নিজস্ব ব্যাঙ্ক পাসবই (CBS ও IFSC সহ)\n• বিদ্যালয়ের বোনাফাইড শংসাপত্র\n• পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 ওএসিস পোর্টাল", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🎓 **पश्चिम बंगाल मेधाश्री योजना (OBC छात्रवृत्ति):**\n\n💰 **राशि**: कक्षा 5 से 8वीं तक के ओबीसी (OBC) छात्रों हेतु ₹800 प्रति वर्ष सीधे बैंक खाते में।\n📑 **ज़रूरी दस्तावेज़:** छात्र का आधार कार्ड, वैध OBC प्रमाण पत्र, पिछली कक्षा की अंकतालिका, सीबीएस बैंक पासबुक, स्कूल बोनाफाइड, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 मेधाश्री पोर्टल", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    wb_migrant_worker: {
      match: ["migrant", "migrant worker", "shramashree", "karmasathi", "পরিযায়ী", "পরিযায়ী শ্রমিক", "শ্রমশ্রী", "কর্মসাথী পরিযায়ী", "প্রবাসী श्रमिक", "श्रमश्री", "कर्मसाथी"],
      en: {
        reply: "🧳 **West Bengal Migrant Worker Welfare Scheme (Shramashree / Karmasathi):**\n\n💰 **Benefits**: ₹2 Lakh Accidental Death Benefit, ₹50,000 permanent disability coverage, ₹30,000 repatriation assistance, and emergency relief distress aid.\n👥 **Eligibility**: Permanent resident of West Bengal who has migrated or intends to migrate to other states or abroad for work, registered on Karmasathi / Shramashree portal.\n\n📑 **Needed Documents:**\n• **Aadhaar Card and Voter ID (EPIC)**\n• **Household Ration Card**\n• **Migrant Worker Identification Number (MWIN/MWINP Receipt)**\n• **Bank Passbook Copy**\n• **Passport and Valid Work Visa** (if working abroad)\n• **Details & Mobile Number of Employer / Contractor**\n\n🌐 **Official Portal:** [Karmasathi Parijayee Shramik Portal](https://karmasathi.wb.gov.in)",
        actions: [
          { label: "🌐 Karmasathi Portal", url: "https://karmasathi.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🧳 **পশ্চিমবঙ্গ পরিযায়ী শ্রমিক কল্যাণ প্রকল্প (শ্রমশ্রী / কর্মসাথী পরিযায়ী):**\n\n💰 **সুবিধা**: ভিনরাজ্যে কর্মরত পরিযায়ী শ্রমিকদের জন্য ২ লক্ষ টাকা দুর্ঘটনা বীমা, ৫০,০০০ টাকা অঙ্গহানি ক্ষতিপূরণ ও জরুরি আর্থিক সহায়তা।\n👥 **যোগ্যতা**: ভিনরাজ্যে বা বিদেশে কর্মরত পশ্চিমবঙ্গের স্থায়ী বাসিন্দা এবং কর্মসাথী পোর্টালে নথিভুক্ত পরিযায়ী শ্রমিক।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড ও ভোটার কার্ড\n• পারিবারিক ডিজিটাল রেশন কার্ড\n• পরিযায়ী শ্রমিক রেজিস্ট্রেশন নম্বর (MWIN)\n• ব্যাঙ্ক পাসবইয়ের জেরক্স\n• পাসপোর্ট ও ওয়ার্ক ভিসা (বিদেশে কর্মরতদের)\n• নিয়োগকর্তা বা ঠিকাদারের মোবাইল নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [Karmasathi Portal](https://karmasathi.wb.gov.in)",
        actions: [
          { label: "🌐 কর্মসাথী পোর্টাল", url: "https://karmasathi.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🧳 **पश्चिम बंगाल प्रवासी श्रमिक कल्याण योजना (श्रमश्री / कर्मसाथी):**\n\n💰 **लाभ**: ₹2 लाख दुर्घटना बीमा, ₹50,000 दिव्यांगता सहायता और आपातकालीन राहत।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, वोटर आईडी, राशन कार्ड, MWIN पंजीकरण पर्ची, बैंक पासबुक, नियोक्ता/ठेकेदार का फोन नंबर।\n\n🌐 **ऑफिशियल पोर्टल:** [Karmasathi Portal](https://karmasathi.wb.gov.in)",
        actions: [
          { label: "🌐 कर्मसाथी पोर्टल", url: "https://karmasathi.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    sikshashree: {
      match: ["sikshashree", "শিক্ষাশ্রী", "শিক্ষাশ্রী স্কলারশিপ", "শিক্ষাশ্রী প্রকল্প", "শিক্ষাশ্রী", "sc st scholarship", "এসসি এসটি স্কলারশিপ"],
      en: {
        reply: "🎓 **West Bengal Sikshashree Scheme (SC/ST Pre-Matric Scholarship):**\n\n💰 **Scholarship Amount**: ₹800/year direct DBT grant for Scheduled Caste (SC) and Scheduled Tribe (ST) students in Classes V to VIII.\n📚 **Eligibility**: Domicile of West Bengal. Must belong to Scheduled Caste (SC) or Scheduled Tribe (ST). Day scholar studying in Class V to VIII in a recognized government/aided school. Family annual income ≤ ₹2,50,000.\n\n📑 **Needed Documents:**\n• **SC or ST Caste Certificate** (issued by competent authority)\n• **Student’s Aadhaar Card**\n• **Family Income Certificate** (issued by BDO/SDO/Executive Officer)\n• **School Bonafide / Enrollment Certificate** (confirming day scholar status)\n• **CBS Bank Passbook in Student’s Name**\n• **Passport-Size Photographs**\n\n🌐 **Official Portal:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 OASIS Official Portal", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🎓 **পশ্চিমবঙ্গ শিক্ষাশ্রী প্রকল্প (SC/ST প্রাক-মাধ্যমিক স্কলারশিপ):**\n\n💰 **বৃত্তি রাশি**: পঞ্চম থেকে অষ্টম শ্রেণীর তপশিলী জাতি (SC) ও উপজাতি (ST) পড়ুয়াদের জন্য বার্ষিক ₹৮০০ সরকারি অনুদান।\n📚 **যোগ্যতা**: পশ্চিমবঙ্গের স্থায়ী বাসিন্দা এসসি/এসটি শিক্ষার্থী। ডে-স্কলার হিসেবে অনুমোদিত স্কুলে পাঠরত। পারিবারিক বার্ষিক আয় ২.৫ লক্ষ টাকার মধ্যে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• এসসি বা এসটি জাতিগত শংসাপত্র\n• শিক্ষার্থীর আধার কার্ড\n• পারিবারিক বার্ষিক আয়ের সার্টিফিকেট\n• বিদ্যালয়ের বোনাফাইড শংসাপত্র\n• শিক্ষার্থীর নিজস্ব একক ব্যাঙ্ক পাসবই (CBS)\n• পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 ওএসিস পোর্টাল", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🎓 **पश्चिम बंगाल शिक्षाश्री योजना (SC/ST छात्रवृत्ति):**\n\n💰 **राशि**: कक्षा 5 से 8वीं तक के एससी/एसटी छात्रों हेतु ₹800 प्रति वर्ष सीधे बैंक खाते में।\n📑 **ज़रूरी दस्तावेज़:** SC/ST जाति प्रमाण पत्र, छात्र का आधार कार्ड, आय प्रमाण पत्र, स्कूल बोनाफाइड, बैंक पासबुक, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [OASIS Portal](https://oasis.gov.in)",
        actions: [
          { label: "🌐 शिक्षाश्री पोर्टल", url: "https://oasis.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

aadhaar_enrolment_seeding: {
      match: ["aadhaar", "adhar", "আধার", "आधार", "enrolment", "seeding", "npci mandate", "baal aadhaar"],
      en: {
        reply: "🆔 **Aadhaar Enrolment & Bank Seeding:**\n\n📋 **Eligibility:**\n• **Enrolment:** Any individual resident of India (residing in India for 182 days or more in the preceding 12 months), regardless of age or gender.\n• **Seeding:** Any citizen holding an active bank account, ration card, LPG connection, or voter identity card seeking DBT/government benefit delivery.\n\n📑 **Needed Documents:**\n• **Proof of Identity (PoI):** Passport, PAN Card, Voter ID, Driving Licence, or Government photo ID.\n• **Proof of Address (PoA):** Electricity/water/gas bill (last 3 months), bank/post office passbook, or registered rent agreement.\n• **Proof of Date of Birth (DoB):** Birth certificate, SSLC/10th admit card, or marksheet.\n• **For Minors (Baal Aadhaar):** Birth certificate of the child and Aadhaar card of either parent (with biometric consent).\n• **For Bank Seeding:** Completed Aadhaar Seeding / NPCI Mapping consent mandate form along with bank passbook copy.\n\n🌐 **Official Portal:** [UIDAI Official Portal](https://uidai.gov.in)\n📍 **Where to Apply:** Aadhaar Enrolment Centres, Post Offices, Bank Branches, or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 UIDAI Portal", url: "https://uidai.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🆔 **আধার নথিভুক্তি ও ব্যাঙ্ক সিডিং (Aadhaar Enrolment & Seeding):**\n\n📋 **যোগ্যতা (Eligibility):**\n• **নথিভুক্তি:** বিগত ১২ মাসে ভারতে ১৮২ দিন বা তার বেশি বসবাসকারী যে কোনো ভারতীয় বাসিন্দা (বয়স বা লিঙ্গ নির্বিশেষে)।\n• **ব্যাঙ্ক সিডিং:** যে কোনো নাগরিক যাঁর সক্রিয় ব্যাঙ্ক অ্যাকাউন্ট, রেশন কার্ড, এলপিজি সংযোগ বা ভোটার কার্ড রয়েছে এবং ডিবিটি বা সরকারি সুবিধা পেতে চান।\n\n📑 **প্রয়োজনীয় নথিপত্র (Needed Documents):**\n• **পরিচয়ের প্রমাণ (PoI):** পাসপোর্ট, প্যান কার্ড, ভোটার কার্ড, ড্রাইভিং লাইসেন্স বা সরকারি ফটো আইডি।\n• **ঠিকানার প্রমাণ (PoA):** সাম্প্রতিক ৩ মাসের বিদ্যুৎ/জল/গ্যাস বিল, ব্যাঙ্ক/পোস্ট অফিস পাসবুক বা রেজিস্টার্ড বাড়িভাড়া চুক্তি।\n• **জন্ম তারিখের প্রমাণ (DoB):** জন্ম শংসাপত্র, মাধ্যমিক অ্যাডমিট কার্ড বা মার্কশিট।\n• **নাবালকদের ক্ষেত্রে (বাল আধার):** শিশুর জন্ম শংসাপত্র এবং পিতা বা মাতার আধার কার্ড (বায়োমেট্রিক সম্মতিসহ)।\n• **ব্যাঙ্ক সিডিংয়ের জন্য:** পূরণকৃত আধার সিডিং / NPCI ম্যাপিং কনসেন্ট ফর্ম এবং ব্যাঙ্ক পাসবইয়ের কপি।\n\n🌐 **অফিসিয়াল পোর্টাল:** [UIDAI Portal](https://uidai.gov.in)\n📍 **আবেদন স্থল:** আধার সেবা কেন্দ্র, পোস্ট অফিস, ব্যাঙ্ক শাখা বা দুয়ারে সরকার ক্যাম্প।",
        actions: [
          { label: "🌐 আধার পোর্টাল", url: "https://uidai.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🆔 **आधार नामांकन एवं बैंक सीडिंग (Aadhaar Enrolment & Seeding):**\n\n📋 **पात्रता (Eligibility):**\n• **नामांकन:** भारत का कोई भी निवासी जो पिछले 12 महीनों में 182 दिन या उससे अधिक भारत में रहा हो (उम्र या लिंग का कोई बंधन नहीं)।\n• **सीडिंग:** सक्रिय बैंक खाता, राशन कार्ड, एलपीजी कनेक्शन या वोटर कार्ड धारक जो डीबीटी (DBT) लाभ पाना चाहते हैं।\n\n📑 **ज़रूरी दस्तावेज़ (Needed Documents):**\n• **पहचान प्रमाण (PoI):** पासपोर्ट, पैन कार्ड, वोटर आईडी, ड्राइविंग लाइसेंस या सरकारी फोटो पहचान पत्र।\n• **निवास प्रमाण (PoA):** बिजली/पानी/गैस बिल (पिछले 3 माह), बैंक/डाकघर पासबुक या रेंट एग्रीमेंट।\n• **जन्मतिथि प्रमाण (DoB):** जन्म प्रमाण पत्र, 10वीं का एडमिट कार्ड या अंकपत्र।\n• **नाबालिगों हेतु (बाल आधार):** बच्चे का जन्म प्रमाण पत्र एवं माता/पिता का आधार कार्ड।\n• **बैंक सीडिंग हेतु:** आधार सीडिंग/NPCI मैपिंग सहमति फॉर्म एवं बैंक पासबुक कॉपी।\n\n🌐 **ऑफिशियल पोर्टल:** [UIDAI Portal](https://uidai.gov.in)",
        actions: [
          { label: "🌐 UIDAI पोर्टल", url: "https://uidai.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    aif_agriculture: {
      match: ["aif", "agriculture infrastructure", "কৃষি পরিকাঠামো", "कृषि अवसंरचना", "cold storage loan", "post harvest"],
      en: {
        reply: "🌾 **Agriculture Infrastructure Fund (AIF):**\n\n💰 **Benefit:** Up to ₹2 Crore debt financing with 3% per annum interest subvention (up to 7 years) + CGTMSE credit guarantee.\n📋 **Eligibility:**\n• Primary Agricultural Credit Societies (PACS), Marketing Cooperative Societies, FPOs, SHGs, JLGs, Multipurpose Cooperative Societies, Agri-entrepreneurs, and startups.\n• Investment must be directed toward post-harvest management infrastructure (warehouses, cold storages, assaying units, pack-houses, silos) or community farming assets (smart agri-tech, farm automation, nurseries).\n\n📑 **Needed Documents:**\n• KYC documents of promoter/partners/directors (Aadhaar, PAN card).\n• Business registration/incorporation certificate, partnership deed, or society bylaws.\n• Detailed Project Report (DPR) detailing project costs, financial viability, and capacity.\n• Land ownership documents (RoR/Khatian) or registered long-term lease agreement.\n• Bank statements (last 1 year) and audited financials / ITR (last 3 years, if applicable).\n• Local municipal/Panchayat sanctions and statutory clearance approvals.\n\n🌐 **Official Portal:** [agriinfra.dac.gov.in](https://agriinfra.dac.gov.in)",
        actions: [
          { label: "🌐 AIF Portal", url: "https://agriinfra.dac.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🌾 **কৃষি পরিকাঠামো তহবিল (Agriculture Infrastructure Fund - AIF):**\n\n💰 **সুবিধা:** ২ কোটি টাকা পর্যন্ত ঋণে বার্ষিক ৩% সুদের ছাড় (৭ বছর পর্যন্ত) ও সিজিটিএমএসই ক্রেডিট গ্যারান্টি।\n📋 **যোগ্যতা:**\n• প্রাথমিক কৃষি ঋণ সমিতি (PACS), সমবায় সমিতি, FPO, স্বনির্ভর দল (SHG), যৌথ দায়বদ্ধতা দল (JLG), কৃষি-উদ্যোক্তা এবং স্টার্টআপ।\n• বিনিয়োগ অবশ্যই ফসলোত্তর পরিকাঠামো (গুদাম, কোল্ড স্টোরেজ, সাইলো, প্যাক-হাউস) বা আধুনিক খামার সম্পদের জন্য হতে হবে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• প্রবর্তক/অংশীদারদের কেওয়াইসি (আধার ও প্যান কার্ড)।\n• ব্যবসায়িক রেজিস্ট্রেশন সার্টিফিকেট, পার্টনারশিপ দলিল বা সমবায় উপ-আইন।\n• বিস্তারিত প্রকল্প রিপোর্ট (DPR)।\n• জমির মালিকানা স্বত্ব (RoR/খতিয়ান) বা দীর্ঘমেয়াদী লিজ চুক্তিপত্র।\n• ব্যাঙ্ক স্টেটমেন্ট (বিগত ১ বছর) এবং অডিট রিপোর্ট/আইটিআর (বিগত ৩ বছর)।\n• স্থানীয় পঞ্চায়েত/পৌরসভার অনুমোদন ও সংবিধিবদ্ধ ক্লিয়ারেন্স।\n\n🌐 **অফিসিয়াল পোর্টাল:** [agriinfra.dac.gov.in](https://agriinfra.dac.gov.in)",
        actions: [
          { label: "🌐 AIF পোর্টাল", url: "https://agriinfra.dac.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🌾 **कृषि अवसंरचना कोष (AIF):**\n\n💰 **ऋण लाभ:** ₹2 करोड़ तक के ऋण पर 7 वर्षों हेतु 3% ब्याज छूट + क्रेडिट गारंटी।\n📋 **पात्रता:** PACS, FPO, SHG, JLG, सहकारी समितियां, कृषि-उद्यमी व स्टार्टअप। फसल कटाई बाद प्रबंधन अवसंरचना (कोल्ड स्टोरेज, गोदाम, साइलो) अथवा आधुनिक कृषि परिसंपत्तियों हेतु।\n📑 **ज़रूरी दस्तावेज़:** प्रमोटर KYC (आधार, पैन), व्यवसाय पंजीकरण प्रमाण, DPR (विस्तृत परियोजना रिपोर्ट), भूमि रिकॉर्ड/पट्टा, 1 वर्ष का बैंक स्टेटमेंट, स्थानीय अनापत्ति प्रमाण पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [agriinfra.dac.gov.in](https://agriinfra.dac.gov.in)",
        actions: [
          { label: "🌐 AIF पोर्टल", url: "https://agriinfra.dac.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    annapurna_yojana: {
      match: ["annapurna yojana", "অন্নপূর্ণা যোজনা", "अन्नपूर्णा योजना", "senior foodgrain", "10 kg rice", "noaps"],
      en: {
        reply: "🍚 **Annapurna Yojana (National Social Assistance & WB Food Security):**\n\n💰 **Benefit:** 10 kg free foodgrains (rice/wheat) per month via PDS + State social welfare coverage.\n📋 **Eligibility Criteria:**\n• **National / PDS Framework:** Indigent senior citizens aged 65 years or above who are eligible for NOAPS but not receiving any regular pension or government financial assistance.\n• **State Special Framework (West Bengal Annapurna):** Female residents from economically vulnerable households with personal monthly income under ₹10,000 and total family annual income within prescribed limits (under ₹12 lakh), not employed in regular government service.\n\n📑 **Needed Documents:**\n• Aadhaar card of the applicant.\n• Digital Ration Card / Food Security card.\n• Voter ID card (EPIC) and residential proof.\n• Age proof (admit card, school leaving certificate, or birth record).\n• Bank account passbook copy (Aadhaar-seeded for DBT).\n• Non-receipt of pension declaration / Income certificate issued by BDO/SDO.\n\n🌐 **Official Portal:** [WB Food & Supplies](https://food.wb.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps, BDO / SDO Office, or local Food Inspector counter.",
        actions: [
          { label: "🌐 Food Portal", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🍚 **অন্নপূর্ণা যোজনা (Annapurna Yojana):**\n\n💰 **সুবিধা:** প্রতি মাসে ১০ কেজি বিনামূল্যে খাদ্যশস্য (চাল/গম) ও সামাজিক সুরক্ষা সহায়তা।\n📋 **যোগ্যতা:**\n• **জাতীয়/পিডিএস কাঠামো:** ৬৫ বছর বা তার বেশি বয়সী অসহায় প্রবীণ নাগরিক যাঁরা NOAPS পাওয়ার যোগ্য কিন্তু কোনো নিয়মিত পেনশন বা সরকারি সাহায্য পাচ্ছেন না।\n• **রাজ্য বিশেষ কাঠামো:** মাসিক ₹১০,০০০-এর কম ব্যক্তিগত আয় এবং বাৎসরিক ₹১২ লাখের কম পারিবারিক আয়ের মহিলারা, যাঁরা সরকারি চাকরিজীবী নন।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আবেদনকারীর আধার কার্ড\n• ডিজিটাল রেশন কার্ড / খাদ্য সুরক্ষা কার্ড\n• ভোটার আইডি কার্ড (EPIC) ও বসবাসের প্রমাণ\n• বয়সের প্রমাণপত্র (অ্যাডমিট কার্ড, স্কুল সার্টিফিকেট বা জন্ম শংসাপত্র)\n• আধার সংযুক্ত ব্যাঙ্ক পাসবুকের কপি\n• পেনশন না-পাওয়ার ঘোষণাপত্র বা BDO/SDO প্রদত্ত আয়ের শংসাপত্র\n\n🌐 **অফিসিয়াল পোর্টাল:** [WB Food Portal](https://food.wb.gov.in)",
        actions: [
          { label: "🌐 খাদ্য দপ্তর", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🍚 **अन्नपूर्णा योजना (Annapurna Yojana):**\n\n💰 **लाभ:** प्रतिमाह 10 किग्रा निःशुल्क खाद्यान्न (चावल/गेहूं) एवं सामाजिक सुरक्षा।\n📋 **पात्रता:** 65 वर्ष या अधिक के निराश्रित वरिष्ठ नागरिक जो कोई पेंशन नहीं पा रहे हैं, एवं आर्थिक रूप से कमजोर परिवारों की महिलाएं (मासिक आय ₹10,000 से कम)।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, डिजिटल राशन कार्ड, वोटर आईडी, आयु प्रमाण पत्र, आधार-सीडेड बैंक पासबुक, पेंशन न मिलने का स्व-घोषणा पत्र / आय प्रमाण पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [food.wb.gov.in](https://food.wb.gov.in)",
        actions: [
          { label: "🌐 खाद्य विभाग", url: "https://food.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    atal_pension_yojana: {
      match: ["atal", "apy", "অটল", "अटल पेंशन", "pension 60", "pfrda", "auto debit"],
      en: {
        reply: "🛡️ **Atal Pension Yojana (APY):**\n\n💰 **Benefit:** Guaranteed monthly pension of ₹1,000 to ₹5,000 after age 60 + lifelong spouse pension and full corpus refund to nominee.\n📋 **Eligibility Criteria:**\n• Any Indian citizen aged between 18 and 40 years.\n• Must hold an active individual savings bank account or post office savings account.\n• Must not be an income tax payer (individuals who have been income tax assessees are ineligible for fresh enrolment).\n• Must give auto-debit consent for periodic contributions up to age 60.\n\n📑 **Needed Documents:**\n• Aadhaar card.\n• Savings bank account number and IFSC code (passbook copy/cheque).\n• Completed APY application-cum-auto-debit mandate form.\n• Nominee and spouse details.\n• Active mobile number.\n\n🌐 **Official Portal:** [PFRDA APY Portal](https://npai.pfrda.org.in)\n📍 **Where to Apply:** Nearest Bank Branch, Post Office, or through your Mobile Banking App.",
        actions: [
          { label: "🌐 PFRDA Portal", url: "https://npai.pfrda.org.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🛡️ **অটল পেনশন যোজনা (Atal Pension Yojana - APY):**\n\n💰 **পেনশন সুবিধা:** ৬০ বছর বয়সের পর থেকে আজীবন মাসিক ₹১,০০০ থেকে ₹৫,০০০ নিশ্চিত পেনশন + পত্নী পেনশন ও নমিনিকে এককালীন তহবিল ফেরত।\n📋 **যোগ্যতা:**\n• ১৮ থেকে ৪০ বছর বয়সী যে কোনো ভারতীয় নাগরিক।\n• নিজস্ব সক্রিয় সেভিংস ব্যাঙ্ক বা পোস্ট অফিস অ্যাকাউন্ট থাকতে হবে।\n• আয়করদাতা হওয়া চলবে না।\n• ৬০ বছর বয়স পর্যন্ত নিয়মিত অবদানের অটো-ডেবিট সম্মতি দিতে হবে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড\n• সেভিংস ব্যাঙ্ক অ্যাকাউন্ট নম্বর ও আইএফএসসি কোড (পাসবইয়ের কপি/চেক)\n• পূরণকৃত APY আবেদন ও অটো-ডেবিট ম্যান্ডেট ফর্ম\n• নমিনি ও জীবনসঙ্গীর বিবরণ\n• সক্রিয় মোবাইল নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [PFRDA APY Portal](https://npai.pfrda.org.in)",
        actions: [
          { label: "🌐 PFRDA পোর্টাল", url: "https://npai.pfrda.org.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🛡️ **अटल पेंशन योजना (APY):**\n\n💰 **पेंशन लाभ:** 60 वर्ष की आयु के बाद ₹1,000 से ₹5,000 की आजीवन मासिक पेंशन + जीवनसाथी को पेंशन व नॉमिनी को कॉर्पस।\n📋 **पात्रता:** 18 से 40 वर्ष के भारतीय नागरिक जिनके पास बचत बैंक या डाकघर खाता हो। आयकर दाता न हों। 60 वर्ष की उम्र तक ऑटो-डेबिट योगदान की सहमति।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, बचत बैंक पासबुक/चेक, APY आवेदन व ऑटो-डेबिट मैन्डेट फॉर्म, नॉमिनी व जीवनसाथी का विवरण, सक्रिय मोबाइल नंबर।\n\n🌐 **ऑफिशियल पोर्टल:** [npai.pfrda.org.in](https://npai.pfrda.org.in)",
        actions: [
          { label: "🌐 PFRDA पोर्टल", url: "https://npai.pfrda.org.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    beti_bachao_beti_padhao: {
      match: ["beti bachao", "bbbp", "বেটি বাঁচাও", "बेटी बचाओ", "mcp card", "girl child protection"],
      en: {
        reply: "👧 **Beti Bachao Beti Padhao (BBBP) Yojana:**\n\n🎯 **Objective:** National campaign to prevent gender-biased sex selection, protect survival, and ensure education of girl children, linking with Sukanya Samriddhi Yojana (SSY) and Kanyashree.\n📋 **Eligibility Criteria:**\n• Targets every Indian family with a girl child.\n• Eligibility focuses on institutional access: pregnant and lactating mothers registering their pregnancy (MCP card) and newborn girl children accessing institutional healthcare and education.\n• Direct linkage with financial tools like Sukanya Samriddhi Yojana (SSY).\n\n📑 **Needed Documents (for linked entitlements):**\n• Mother and Child Protection (MCP) card.\n• Birth Certificate of the girl child.\n• Aadhaar cards of the parents/guardians.\n• School enrollment/bonafide certificate for secondary educational tracking.\n\n🌐 **Official Portal:** [MoWCD BBBP Portal](https://wcd.nic.in/bbbp-schemes)\n📍 **Where to Access:** Anganwadi Centres (ICDS), Primary Health Centres, and local schools.",
        actions: [
          { label: "🌐 MoWCD Portal", url: "https://wcd.nic.in/bbbp-schemes", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "👧 **বেটি বাঁচাও বেটি পড়াও যোজনা (BBBP):**\n\n🎯 **উদ্দেশ্য:** কন্যা সন্তানের জন্ম হার বৃদ্ধি, সুরক্ষা ও মাধ্যমিক শিক্ষা নিশ্চিতকরণ এবং সুকন্যা সমৃদ্ধি ও কন্যাশ্রী প্রকল্পের সংযোগ সাধন।\n📋 **যোগ্যতা:** কন্যা সন্তান রয়েছে এমন প্রতিটি পরিবার। প্রাতিষ্ঠানিক সুবিধা পেতে গর্ভবতী মায়েদের রেজিস্ট্রেশন (MCP কার্ড) ও কন্যা সন্তানের প্রাতিষ্ঠানিক স্বাস্থ্যসেবা নিশ্চিতকরণ।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• মা ও শিশু সুরক্ষা (MCP) কার্ড\n• কন্যা সন্তানের জন্ম শংসাপত্র\n• পিতা-মাতা/অভিভাবকের আধার কার্ড\n• বিদ্যালয়ে ভর্তির প্রশংসাপত্র (School Bonafide Certificate)\n\n🌐 **অফিসিয়াল পোর্টাল:** [wcd.nic.in](https://wcd.nic.in/bbbp-schemes)",
        actions: [
          { label: "🌐 কেন্দ্রীয় পোর্টাল", url: "https://wcd.nic.in/bbbp-schemes", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "👧 **बेटी बचाओ बेटी पढ़ाओ (BBBP) योजना:**\n\n🎯 **उद्देश्य:** बालिकाओं का संरक्षण, संस्थागत स्वास्थ्य ट्रैकिंग व गुणवत्तापूर्ण शिक्षा सुनिश्चित करना, साथ ही सुकन्या समृद्धि योजना (SSY) से जोड़ना।\n📋 **पात्रता:** बालिका युक्त परिवार, संस्थागत MCP कार्ड पंजीकरण एवं विद्यालयी शिक्षा।\n📑 **ज़रूरी दस्तावेज़:** मातृ एवं शिशु सुरक्षा (MCP) कार्ड, बालिका का जन्म प्रमाण पत्र, माता-पिता का आधार कार्ड, स्कूल बोनाफाइड/नामांकन प्रमाण पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [wcd.nic.in](https://wcd.nic.in/bbbp-schemes)",
        actions: [
          { label: "🌐 आधिकारिक पोर्टल", url: "https://wcd.nic.in/bbbp-schemes", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    bmssy: {
      match: ["bmssy", "bina mulya", "বিনা মূল্যে সামাজিক সুরক্ষা", "बिना मूल्य", "unorganized workers", "6500 income"],
      en: {
        reply: "👷 **Bina Mulya Samajik Suraksha Yojana (BMSSY - West Bengal):**\n\n💰 **Benefit:** 100% state-funded Provident Fund contribution + ₹2,00,000 accidental death cover + ₹50,000 disability cover + children education grants.\n📋 **Eligibility Criteria:**\n• Permanent resident of West Bengal aged between 18 and 60 years.\n• Engaged in notified unorganized industries (46 sectors) or self-employed categories (15 occupations, such as carpenters, barbers, street hawkers, rickshaw pullers).\n• Monthly family income must not exceed ₹6,500 (no income cap applies to building/construction and transport workers).\n\n📑 **Needed Documents:**\n• Aadhaar card and Voter ID (EPIC).\n• Digital Ration Card.\n• Bank passbook copy (showing IFSC and Aadhaar seeding).\n• Passport-size photographs and specimen signature.\n• Self-declaration / Trade or unorganized profession proof certified by local councillor or Panchayat representative.\n\n🌐 **Official Portal:** [bmssy.wblabour.gov.in](https://bmssy.wblabour.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps or Regional Labour Welfare Facilitation Centres (LWFC).",
        actions: [
          { label: "🌐 BMSSY Portal", url: "https://bmssy.wblabour.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "👷 **বিনা মূল্যে সামাজিক সুরক্ষা যোজনা (BMSSY - পশ্চিমবঙ্গ):**\n\n💰 **সুবিধা:** সম্পূর্ণ সরকারি খরচে প্রভিডেন্ট ফান্ড অনুদান + ₹২ লক্ষ দুর্ঘটনা মৃত্যু বীমা + ₹৫০ হাজার অঙ্গহানি ক্ষতিপূরণ + সন্তানদের শিক্ষাবৃত্তি।\n📋 **যোগ্যতা:**\n• পশ্চিমবঙ্গের স্থায়ী বাসিন্দা, বয়স ১৮ থেকে ৬০ বছর।\n• ৪৬টি বিজ্ঞাপিত অসংগঠিত শিল্প বা ১৫টি পেশার (ছুতোর, নাপিত, হকার, রিকশাচালক ইত্যাদি) স্বনিযুক্ত শ্রমিক।\n• মাসিক পারিবারিক আয় অনূর্ধ্ব ₹৬,৫০০ (নির্মাণ ও পরিবহন শ্রমিকদের আয়ের কোনো ঊর্ধ্বসীমা নেই)।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড ও ভোটার কার্ড (EPIC)\n• ডিজিটাল রেশন কার্ড\n• ব্যাঙ্ক পাসবুকের কপি (IFSC ও আধার সিডিংযুক্ত)\n• পাসপোর্ট সাইজ ছবি ও স্বাক্ষর\n• স্থানীয় কাউন্সিলার বা পঞ্চায়েত প্রতিনিধি দ্বারা প্রত্যয়িত পেশার স্ব-ঘোষণাপত্র\n\n🌐 **অফিসিয়াল পোর্টাল:** [bmssy.wblabour.gov.in](https://bmssy.wblabour.gov.in)",
        actions: [
          { label: "🌐 শ্রম দপ্তর পোর্টাল", url: "https://bmssy.wblabour.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "👷 **बिना मूल्य सामाजिक सुरक्षा योजना (BMSSY - पश्चिम बंगाल):**\n\n💰 **लाभ:** पूर्णतः मुफ्त राज्य पीएफ अंशदान + ₹2,00,000 दुर्घटना मृत्यु मुआवजा + बच्चों की शिक्षा सहायता।\n📋 **पात्रता:** प. बंगाल के 18-60 वर्ष के असंगठित कामगार (46 उद्योग, 15 स्वरोजगार)। मासिक पारिवारिक आय ₹6,500 से कम (निर्माण व परिवहन श्रमिकों हेतु कोई आय सीमा नहीं)।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, वोटर आईडी, डिजिटल राशन कार्ड, आधार-सीडेड बैंक पासबुक, पासपोर्ट फोटो, स्थानीय प्रतिनिधि द्वारा प्रमाणित स्व-घोषणा पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [bmssy.wblabour.gov.in](https://bmssy.wblabour.gov.in)",
        actions: [
          { label: "🌐 BMSSY पोर्टल", url: "https://bmssy.wblabour.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    caa: {
      match: ["caa", "citizenship", "নাগরিকত্ব", "নাগরিকত্ব সংশোধনী", "नागरिकता", "2014", "refugee citizenship"],
      en: {
        reply: "📜 **Citizenship Amendment Act (CAA - 2019):**\n\n📜 **Benefit:** Grant of Certificate of Naturalization / Registration establishing Indian Citizenship under Section 6B.\n📋 **Eligibility Criteria:**\n• Migrants belonging to six minority religious communities: Hindus, Sikhs, Buddhists, Jains, Parsis, or Christians.\n• Originating from Pakistan, Bangladesh, or Afghanistan.\n• Entered India on or before December 31, 2014.\n• Not residing in Sixth Schedule tribal areas (Assam, Meghalaya, Mizoram, Tripura) or states covered by the Inner Line Permit (ILP).\n\n📑 **Needed Documents:**\n• **Proof of nationality of origin:** Passport, birth certificate, school/college certificate, tenancy records, or national ID issued by authorities in Pakistan/Bangladesh/Afghanistan.\n• **Proof of entry into India on or before 31.12.2014:** Visa stamp, FRRO permit, Indian census slip, driving licence, school certificate, or land tenancy deed in India.\n• **Affidavit & Certificate:** Affidavit verifying eligibility under CAA rules and an eligibility certificate from a locally recognized community institution.\n\n🌐 **Official Portal:** [indiancitizenshiponline.nic.in](https://indiancitizenshiponline.nic.in)",
        actions: [
          { label: "🌐 CAA Portal", url: "https://indiancitizenshiponline.nic.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "📜 **নাগরিকত্ব সংশোধনী আইন (CAA - ২০১৯):**\n\n📜 **সুবিধা:** ধারা ৬বি অনুযায়ী বৈধ ভারতীয় নাগরিকত্ব শংসাপত্র ও আইনি অধিকার প্রদান।\n📋 **যোগ্যতা:**\n• পাকিস্তান, বাংলাদেশ বা আফগানিস্তান থেকে ধর্মীয় নিপীড়নের কারণে আগত ৬টি সংখ্যালঘু সম্প্রদায়: হিন্দু, শিখ, বৌদ্ধ, জৈন, পার্সি বা খ্রিস্টান।\n• ৩১ ডিসেম্বর ২০১৪-এর পূর্বে বা ওই দিনে ভারতে প্রবেশ করেছেন।\n• ষষ্ঠ তফসিল ও আইএলপি (ILP) বহির্ভূত এলাকায় অবস্থানকারী।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• **উৎপত্তিস্থল দেশের প্রমাণ:** পাসপোর্ট, জন্ম শংসাপত্র, স্কুল সার্টিফিকেট বা পাকিস্তান/বাংলাদেশ/আফগানিস্তান কর্তৃক প্রদত্ত জাতীয় পরিচয়পত্র।\n• **৩১.১২.২০১৪-এর পূর্বে ভারতে প্রবেশের প্রমাণ:** ভিসা স্ট্যাম্প, FRRO পারমিট, আদমশুমারির স্লিপ, ভারতীয় ড্রাইভিং লাইসেন্স, স্কুলের প্রশংসাপত্র বা ভাড়ার দলিল।\n• **হলফনামা ও প্রত্যয়ন:** CAA বিধিমালার অধীনে যোগ্যতার হলফনামা এবং স্থানীয় সমাজিক প্রতিষ্ঠান প্রদত্ত যোগ্যতার শংসাপত্র।\n\n🌐 **অফিসিয়াল পোর্টাল:** [indiancitizenshiponline.nic.in](https://indiancitizenshiponline.nic.in)",
        actions: [
          { label: "🌐 নাগরিকত্ব পোর্টাল", url: "https://indiancitizenshiponline.nic.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "📜 **नागरिकता संशोधन अधिनियम (CAA - 2019):**\n\n📜 **लाभ:** धारा 6B के तहत भारतीय नागरिकता प्रमाणपत्र व विधिक अधिकार।\n📋 **पात्रता:** पाकिस्तान, बांग्लादेश या अफगानिस्तान से 31 दिसंबर 2014 को या उससे पहले भारत आए 6 अल्पसंख्यक समुदाय (हिंदू, सिख, बौद्ध, जैन, पारसी, ईसाई)। छठी अनुसूची व इनर लाइन परमिट (ILP) क्षेत्रों से बाहर।\n📑 **ज़रूरी दस्तावेज़:** मूल देश की नागरिकता का प्रमाण (पासपोर्ट/जन्म प्रमाण/आईडी), 31.12.2014 से पूर्व भारत आगमन का प्रमाण (वीजा/FRRO/लाइसेंस/किरायानामा), CAA शपथ पत्र व समुदाय संस्थान प्रमाण पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [indiancitizenshiponline.nic.in](https://indiancitizenshiponline.nic.in)",
        actions: [
          { label: "🌐 CAA पोर्टल", url: "https://indiancitizenshiponline.nic.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    shg_credit_linkage: {
      match: ["shg credit", "credit linkage", "স্বনির্ভর দল ঋণ", "ক্রেডিট লিঙ্কেজ", "panchasutra", "mcp loan"],
      en: {
        reply: "🤝 **Credit Linkage to Self-Help Groups (SHGs):**\n\n💰 **Benefit:** Collateral-free institutional bank loans from ₹1.5 Lakh up to ₹20 Lakh with interest subvention (effective 4% on prompt repayment).\n📋 **Eligibility Criteria:**\n• The SHG must be in active existence for at least 6 months with updated books of account.\n• Adherence to 'Panchasutra' principles: Regular meetings, regular savings, regular internal lending, timely recovery, and proper maintenance of books.\n• Qualified under grading norms prescribed by NABARD / State Rural Livelihood Mission.\n• Minimum 70% of members must be from poor households (for DAY-NRLM groups).\n\n📑 **Needed Documents:**\n• Loan application form along with the group's approved Micro-Credit Plan (MCP).\n• Resolution of the SHG to apply for a bank loan, signed by all group members.\n• KYC documents (Aadhaar, PAN/Form 60, photos) of authorized office bearers (President, Secretary, Cashier) and all members.\n• SHG grading sheet / appraisal score from NRLM/Sponsoring agency.\n• Existing savings bank passbook and account audit/statement.\n\n🌐 **Official Portal:** [DAY-NRLM Portal](https://nrlm.gov.in)\n📍 **Where to Apply:** Local Bank Branch, Sangha Co-operative, or BDO Office (Anandadhara Cell).",
        actions: [
          { label: "🌐 NRLM Portal", url: "https://nrlm.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🤝 **স্বনির্ভর দলের (SHG) ব্যাঙ্ক ক্রেডিট লিঙ্কেজ:**\n\n💰 **ঋণ সুবিধা:** জামানতবিহীন ১.৫ লক্ষ থেকে ২০ লক্ষ টাকা পর্যন্ত সহজ ব্যাঙ্ক ঋণ এবং ৪% পর্যন্ত সুদের ছাড়।\n📋 **যোগ্যতা:**\n• স্বনির্ভর দলটির বয়স ন্যূনতম ৬ মাস ও হিসাবের খাতা নিয়মিত হতে হবে।\n• 'পঞ্চসূত্র' নীতি পালন: নিয়মিত মিটিং, নিয়মিত সঞ্চয়, অভ্যন্তরীণ ঋণদান, সময়মতো ঋণ আদায় এবং খাতা রক্ষণাবেক্ষণ।\n• নাবার্ড বা রাজ্য গ্রামীণ জীবিকা মিশনের গ্রেডিংয়ে উত্তীর্ণ।\n• দলের অন্তত ৭০% সদস্য দরিদ্র পরিবারের হতে হবে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• অনুমোদিত মাইক্রো-ক্রেডিট প্ল্যান (MCP) সহ ব্যাঙ্ক ঋণ আবেদন ফর্ম।\n• ব্যাঙ্ক ঋণের জন্য সকল সদস্যের স্বাক্ষরিত রেজোলিউশন।\n• কর্মকর্তা (সভানেত্রী, সম্পাদিকা, কোষাধ্যক্ষা) ও সকল সদস্যের কেওয়াইসি (আধার ও ছবি)।\n• স্বনির্ভর দলের গ্রেডিং মূল্যায়ন স্কোর কার্ড।\n• ব্যাঙ্কের সেভিংস পাসবই ও অডিট স্টেটমেন্ট।\n\n🌐 **অফিসিয়াল পোর্টাল:** [nrlm.gov.in](https://nrlm.gov.in)",
        actions: [
          { label: "🌐 আনন্দধারা", url: "https://nrlm.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🤝 **स्वयं सहायता समूह (SHG) बैंक क्रेडिट लिंकेज:**\n\n💰 **ऋण लाभ:** ₹1.5 लाख से ₹20 लाख तक का बिना गारंटी का बैंक लोन, समय पर भुगतान करने पर मात्र 4% प्रभावी ब्याज।\n📋 **पात्रता:** कम से कम 6 माह पुराना सक्रिय समूह। 'पंचसूत्र' का अनुपालन (नियमित बैठक, बचत, आंतरिक ऋण, वसूली, बही-खाता)। NABARD/NRLM ग्रेडिंग में उत्तीर्ण।\n📑 **ज़रूरी दस्तावेज़:** ऋण आवेदन पत्र व स्वीकृत माइक्रो-क्रेडिट प्लान (MCP), सभी सदस्यों द्वारा हस्ताक्षरित समूह प्रस्ताव, पदाधिकारियों व सदस्यों के KYC दस्तावेज़, ग्रेडिंग शीट, बैंक पासबुक व ऑडिट रिपोर्ट।\n\n🌐 **ऑफिशियल पोर्टल:** [nrlm.gov.in](https://nrlm.gov.in)",
        actions: [
          { label: "🌐 NRLM पोर्टल", url: "https://nrlm.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    ddu_gky: {
      match: ["ddu-gky", "ddugky", "গ্রামীণ কৌশল্য", "दीन दयाल उपाध्याय कौशल्य", "residential skill", "placement"],
      en: {
        reply: "🎓 **Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY):**\n\n💰 **Benefit:** 100% free residential market-driven vocational training + guaranteed job placement (min 70%) + post-placement stipend.\n📋 **Eligibility Criteria:**\n• Rural youth aged between 15 and 35 years (upper age relaxed up to 45 years for women, PwDs, and Special Groups like PVTGs).\n• Household must belong to economically poor backgrounds verified through: BPL card, AAY card, active MGNREGA household (with at least 15 days of work in previous FY), or members of NRLM SHGs.\n\n📑 **Needed Documents:**\n• Aadhaar card or Voter ID (proof of identity and age).\n• Proof of rural residence (Panchayat domicile certificate / Ration Card).\n• Proof of poverty entitlement: BPL card, Antyodaya Anna Yojana (AAY) card, or MGNREGA Job Card.\n• Educational certificates and mark sheets (Class 8, 10, or 12).\n• Caste certificate / PwD certificate (if applicable).\n• Aadhaar-linked bank passbook.\n\n🌐 **Official Portal:** [ddugky.gov.in](https://ddugky.gov.in)\n📍 **Where to Apply:** District PBSSD Centers, Gram Panchayat Office, or Kaushal Panjee Portal.",
        actions: [
          { label: "🌐 DDU-GKY Portal", url: "https://ddugky.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🎓 **দীন দয়াল উপাধ্যায় গ্রামীণ কৌশল্য যোজনা (DDU-GKY):**\n\n💰 **সুবিধা:** বিনামূল্যে থাকা-খাওয়াসহ আধুনিক বৃত্তিমূলক প্রশিক্ষণ + নিশ্চিত চাকরির সুযোগ (কমপক্ষে ৭০%) + চাকরির পরবর্তী স্টাইপেন্ড।\n📋 **যোগ্যতা:**\n• ১৫ থেকে ৩৫ বছর বয়সী গ্রামীণ যুবক-যুবতী (মহিলা ও বিশেষ ক্ষেত্রে ৪৫ বছর পর্যন্ত)।\n• দরিদ্র পরিবার: বিপিএল কার্ড, এএওয়াই কার্ড, জব কার্ডে ১৫ দিনের কাজ বা স্বনির্ভর দলের পরিবারভুক্ত।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড বা ভোটার আইডি\n• গ্রামীণ আবাসিক শংসাপত্র (পঞ্চায়েত সার্টিফিকেট/রেশন কার্ড)\n• দারিদ্র্যসীমার প্রমাণ (BPL/AAY/জব কার্ড)\n• শিক্ষাগত যোগ্যতার মার্কশিট (অষ্টম, দশম বা দ্বাদশ শ্রেণি)\n• জাতিগত/প্রতিবন্ধী শংসাপত্র (প্রযোজ্য ক্ষেত্রে)\n• আধার লিঙ্ক করা ব্যাঙ্ক পাসবই\n\n🌐 **অফিসিয়াল পোর্টাল:** [ddugky.gov.in](https://ddugky.gov.in)",
        actions: [
          { label: "🌐 DDU-GKY পোর্টাল", url: "https://ddugky.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🎓 **दीन दयाल उपाध्याय ग्रामीण कौशल्य योजना (DDU-GKY):**\n\n💰 **लाभ:** पूर्णतः मुफ्त आवासीय कौशल प्रशिक्षण + कम से कम 70% गारंटीशुदा नौकरी + पोस्ट-प्लेसमेंट वजीफा।\n📋 **पात्रता:** 15 से 35 वर्ष के ग्रामीण निर्धन युवा (महिलाओं व दिव्यांगों हेतु 45 वर्ष तक)। BPL, AAY कार्ड धारक, मनरेगा (15 दिन काम) या SHG सदस्य परिवार।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, ग्रामीण निवास प्रमाण, निर्धनता पात्रता प्रमाण (BPL/AAY/जॉब कार्ड), शैक्षणिक अंकपत्र (8वीं/10वीं/12वीं), जाति प्रमाण पत्र (यदि लागू हो), आधार-लिंक्ड बैंक पासबुक।\n\n🌐 **ऑफिशियल पोर्टल:** [ddugky.gov.in](https://ddugky.gov.in)",
        actions: [
          { label: "🌐 कौशल्य पोर्टल", url: "https://ddugky.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    day_nrlm_anandadhara: {
      match: ["anandadhara", "আনন্দধারা", "day-nrlm", "nrlm", "आनंदधारा", "pip survey", "revolving fund"],
      en: {
        reply: "🌸 **DAY-NRLM / Anandadhara (State Rural Livelihoods Mission):**\n\n💰 **Benefit:** ₹15,000 Revolving Fund (RF) + ₹1.5 Lakh Community Investment Fund (CIF) per SHG + micro-enterprise incubation.\n📋 **Eligibility Criteria:**\n• Rural women belonging to poor and vulnerable households identified via the Participatory Identification of the Poor (PIP) process.\n• One female member per identified household is brought into an affinity-based Self-Help Group (10–20 women).\n• Special priority given to manual scavengers, bonded labourers, PVTGs, and single-women households.\n\n📑 **Needed Documents:**\n• Aadhaar card and Voter ID of the applicant.\n• Proof of residence in the Gram Panchayat.\n• BPL Ration Card / PIP survey confirmation.\n• Bank savings account passbook.\n• Passport-size photograph.\n\n🌐 **Official Portal:** [wbprd.gov.in](https://wbprd.gov.in)\n📍 **Where to Apply:** Gram Panchayat Office, BDO Office (Anandadhara Cell), or local Duare Sarkar Camp.",
        actions: [
          { label: "🌐 Anandadhara Portal", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🌸 **আনন্দধারা / ডে-এনআরএলএম (Anandadhara - WBSRLM):**\n\n💰 **সুবিধা:** প্রতি স্বনির্ভর দলে ₹১৫,০০০ রিভলভিং ফান্ড + ₹১.৫ লক্ষ সিআইএফ অনুদান ও আধুনিক জীবিকা সহায়তা।\n📋 **যোগ্যতা:** অংশগ্রহণমূলক দারিদ্র্য চিহ্নিতকরণ (PIP) প্রক্রিয়ার মাধ্যমে নির্বাচিত গ্রামীণ দরিদ্র পরিবারের মহিলারা। প্রতি পরিবার থেকে ১ জন মহিলা সদস্য ১০-২০ জনের দলে যুক্ত হবেন।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আবেদনকারীর আধার কার্ড ও ভোটার কার্ড\n• গ্রাম পঞ্চায়েতে বসবাসের প্রমাণপত্র\n• বিপিএল রেশন কার্ড বা পিআইপি তালিকাভুক্তির স্লিপ\n• সেভিংস ব্যাঙ্ক অ্যাকাউন্টের পাসবই\n• পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [wbprd.gov.in](https://wbprd.gov.in)",
        actions: [
          { label: "🌐 আনন্দধারা পোর্টাল", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🌸 **डे-एनआरएलएम / आनंदधारा (DAY-NRLM / Anandadhara):**\n\n💰 **लाभ:** प्रति SHG समूह ₹15,000 रिवॉल्विंग फंड + ₹1.5 लाख तक सामुदायिक निवेश फंड (CIF) एवं आजीविका प्रशिक्षण।\n📋 **पात्रता:** PIP प्रक्रिया द्वारा चिन्हित ग्रामीण निर्धन परिवारों की महिलाएं। प्रति परिवार 1 महिला सदस्य स्वयं सहायता समूह में शामिल होंगी।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, वोटर आईडी, ग्राम पंचायत निवास प्रमाण, BPL राशन कार्ड / PIP सर्वेक्षण रसीद, बैंक पासबुक, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [wbprd.gov.in](https://wbprd.gov.in)",
        actions: [
          { label: "🌐 आनंदधारा पोर्टल", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    e_shram: {
      match: ["e-shram", "eshram", "ই-শ্রম", "ई-श्रम", "uan", "unorganized card", "pmsby 2 lakh"],
      en: {
        reply: "🛠️ **E-Shram Card (NDUW):**\n\n💰 **Benefit:** Universal 12-digit UAN Card + ₹2,00,000 accidental death/permanent disability insurance under PMSBY + seamless access to social security benefits across India.\n📋 **Eligibility Criteria:**\n• Unorganized worker (agricultural labourer, gig worker, construction worker, domestic help, rickshaw driver, etc.).\n• Age: Between 16 and 59 years.\n• Must not be an active member of EPFO, ESIC, or NPS (government-sponsored).\n• Must not be an income tax assessee.\n\n📑 **Needed Documents:**\n• Aadhaar card (mandatory with mobile number linked for OTP/e-KYC).\n• Active Aadhaar-seeded bank account number with IFSC code.\n• Occupational/trade details.\n• Nominee details.\n\n🌐 **Official Portal:** [eshram.gov.in](https://eshram.gov.in)\n📍 **Where to Register:** Self-registration at eshram.gov.in or nearest Common Service Centre (CSC).",
        actions: [
          { label: "🌐 e-Shram Portal", url: "https://eshram.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🛠️ **ই-শ্রম কার্ড (e-Shram Card - NDUW):**\n\n💰 **সুবিধা:** ১২ সংখ্যার জাতীয় UAN কার্ড + ₹২,০০,০০০ দুর্ঘটনা বীমা (PMSBY) + দেশজুড়ে পরিযায়ী ও সামাজিক সুরক্ষা প্রকল্পের সুবিধা।\n📋 **যোগ্যতা:**\n• অসংগঠিত ক্ষেত্রের শ্রমিক (কৃষি শ্রমিক, নির্মাণ কর্মী, গৃহকর্মী, গিগ কর্মী ইত্যাদি)।\n• বয়স: ১৬ থেকে ৫৯ বছর।\n• EPFO, ESIC বা সরকারি NPS সদস্য হওয়া যাবে না।\n• আয়করদাতা হওয়া যাবে না।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• মোবাইল লিঙ্কযুক্ত আধার কার্ড (ই-কেওয়াইসির জন্য)\n• আধার সংযুক্ত সক্রিয় ব্যাঙ্ক অ্যাকাউন্ট নম্বর ও আইএফএসসি\n• পেশা ও কাজের বিবরণ\n• নমিনির পূর্ণ বিবরণ\n\n🌐 **অফিসিয়াল পোর্টাল:** [eshram.gov.in](https://eshram.gov.in)",
        actions: [
          { label: "🌐 ই-শ্রম পোর্টাল", url: "https://eshram.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🛠️ **ई-श्रम कार्ड (E-Shram Card - NDUW):**\n\n💰 **लाभ:** 12 अंकों का विशिष्ट UAN नंबर + ₹2 लाख का दुर्घटना बीमा + केंद्र व राज्य की कल्याणकारी योजनाओं से सीधा जुड़ाव।\n📋 **पात्रता:** 16 से 59 वर्ष के असंगठित कामगार (कृषि, निर्माण, घरेलू, गिग वर्कर्स आदि)। EPFO/ESIC/सरकारी NPS के सदस्य न हों और आयकर दाता न हों।\n📑 **ज़रूरी दस्तावेज़:** मोबाइल से जुड़ा आधार कार्ड (OTP हेतु), आधार-सीडेड सक्रिय बैंक खाता व IFSC कोड, व्यवसाय विवरण, नॉमिनी की जानकारी।\n\n🌐 **ऑफिशियल पोर्टल:** [eshram.gov.in](https://eshram.gov.in)",
        actions: [
          { label: "🌐 ई-श्रम पोर्टल", url: "https://eshram.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    jai_johar: {
      match: ["jai johar", "জয় জোহার", "जय जोहार", "st pension", "তফসিলি উপজাতি পেনশন"],
      en: {
        reply: "🏹 **Jai Johar (ST Old Age Pension - West Bengal):**\n\n💰 **Monthly Benefit:** ₹1,000 / month lifelong pension directly into bank account via DBT.\n📋 **Eligibility Criteria:**\n• Permanent resident of West Bengal.\n• Must belong to the Scheduled Tribe (ST) community.\n• Must have attained the age of 60 years or above.\n• Must not receive any other monthly social welfare pension or regular government salary/pension.\n\n📑 **Needed Documents:**\n• Formal ST Caste/Tribe certificate issued by a competent authority (or paternal relative certificate with undertaking).\n• Proof of age and address: Aadhaar card and Voter ID (EPIC).\n• Digital Ration Card.\n• Aadhaar-linked CBS bank passbook copy.\n• Recent passport-size photographs.\n\n🌐 **Official Portal:** [Jai Bangla Portal](https://jaibangla.wb.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps, Office of the BDO (Rural), or SDO (Urban).",
        actions: [
          { label: "🌐 Jai Bangla Portal", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🏹 **জয় জোহার (তফসিলি উপজাতি বার্ধক্য ভাতা - পশ্চিমবঙ্গ):**\n\n💰 **মাসিক ভাতা:** আজীবন প্রতি মাসে ₹১,০০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি মারফত।\n📋 **যোগ্যতা:**\n• পশ্চিমবঙ্গের স্থায়ী বাসিন্দা হতে হবে।\n• তফসিলি উপজাতি (ST) সম্প্রদায়ভুক্ত হতে হবে।\n• বয়স ৬০ বছর বা তার বেশি হতে হবে।\n• অন্য কোনো সরকারি সামাজিক পেনশন বা নিয়মিত সরকারি বেতন প্রাপক হওয়া চলবে না।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• উপযুক্ত কর্তৃপক্ষ প্রদত্ত ডিজিটাল এসটি (ST) সার্টিফিকেট\n• বয়স ও ঠিকানার প্রমাণ: আধার কার্ড ও ভোটার কার্ড (EPIC)\n• ডিজিটাল রেশন কার্ডের জেরক্স\n• আধার সংযুক্ত সিবিএস ব্যাঙ্ক পাসবইয়ের কপি\n• সাম্প্রতিক পাসপোর্ট সাইজ রঙিন ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [jaibangla.wb.gov.in](https://jaibangla.wb.gov.in)",
        actions: [
          { label: "🌐 জয় বাংলা পোর্টাল", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏹 **जय जोहार (ST वृद्धावस्था पेंशन - पश्चिम बंगाल):**\n\n💰 **मासिक सहायता:** 60 वर्ष या अधिक के अनुसूचित जनजाति (ST) वरिष्ठ नागरिकों को आजीवन ₹1,000 प्रति माह सीधे बैंक खाते में।\n📋 **पात्रता:** प. बंगाल के स्थायी निवासी, अनुसूचित जनजाति (ST) वर्ग, आयु 60 वर्ष या अधिक। कोई अन्य पेंशन या सरकारी वेतन न ले रहे हों।\n📑 **ज़रूरी दस्तावेज़:** आधिकारिक ST जाति प्रमाण पत्र, आधार कार्ड व वोटर आईडी, डिजिटल राशन कार्ड, आधार-लिंक्ड CBS बैंक पासबुक, पासपोर्ट साइज रंगीन फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [jaibangla.wb.gov.in](https://jaibangla.wb.gov.in)",
        actions: [
          { label: "🌐 जय बांग्ला पोर्टल", url: "https://jaibangla.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    mgnregs_job_card: {
      match: ["job card", "mgnrega", "mgnregs", "vb-g ram-g", "১০০ দিনের কাজ", "मनरेगा", "100 days work"],
      en: {
        reply: "⛏️ **Job Cards under VB-G RAM-G / MGNREGS:**\n\n💰 **Benefit:** Statutory legal guarantee of 100 to 125 days of unskilled manual wage employment per rural household per financial year at statutory wages disbursed directly via DBT.\n📋 **Eligibility Criteria:**\n• Adult members of rural households (aged 18 years and above) residing within the Gram Panchayat area.\n• Must be willing to perform unskilled manual labour.\n• Family must apply as a household unit to receive statutory work guarantees (100–125 days).\n\n📑 **Needed Documents:**\n• Aadhaar cards of all adult household members applying for work.\n• Proof of residence within the Gram Panchayat jurisdiction (Voter ID, Ration Card).\n• Individual/joint Aadhaar-seeded bank/post office passbook details.\n• Passport-size photos of all adult applicants.\n\n🌐 **Official Portal:** [NREGA Official Portal](https://nrega.nic.in)\n📍 **Where to Apply:** Gram Panchayat Office (Gram Rozgar Sahayak) or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 NREGA Portal", url: "https://nrega.nic.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "⛏️ **১০০ দিনের কাজের জব কার্ড (VB-G RAM-G / MGNREGS):**\n\n💰 **সুবিধা:** প্রতি গ্রামীণ পরিবারকে বছরে ১০০ থেকে ১২৫ দিনের নিশ্চিত অদক্ষ কায়িক শ্রমের অধিকার ও নির্ধারিত দৈনিক মজুরি।\n📋 **যোগ্যতা:** গ্রাম পঞ্চায়েতের বাসিন্দা ১৮ বছর বা তার বেশি বয়সী প্রাপ্তবয়স্ক গ্রামীণ নাগরিক, যাঁরা কায়িক শ্রম করতে ইচ্ছুক। পরিবার হিসেবে যৌথ আবেদন করা যায়।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আবেদনকারী পরিবারের সকল প্রাপ্তবয়স্ক সদস্যের আধার কার্ড\n• গ্রাম পঞ্চায়েত এলাকায় বসবাসের প্রমাণ (ভোটার কার্ড বা রেশন কার্ড)\n• আধার সংযুক্ত ব্যাঙ্ক বা পোস্ট অফিস পাসবইয়ের বিবরণ\n• সকল প্রাপ্তবয়স্ক আবেদনকারীর পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [nrega.nic.in](https://nrega.nic.in)",
        actions: [
          { label: "🌐 একশো দিনের কাজ", url: "https://nrega.nic.in", type: "link" },
          { label: "📋 সম্পূর্ণ বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "⛏️ **जॉब कार्ड योजना (VB-G RAM-G / MGNREGS मनरेगा):**\n\n💰 **लाभ:** प्रत्येक ग्रामीण परिवार को प्रति वित्तीय वर्ष 100 से 125 दिनों का कानूनी गारंटीशुदा अकुशल रोजगार व सीधा बैंक DBT भुगतान।\n📋 **पात्रता:** ग्राम पंचायत क्षेत्र में रहने वाले 18 वर्ष या उससे अधिक आयु के वयस्क नागरिक जो शारीरिक मजदूरी करने के इच्छुक हों।\n📑 **ज़रूरी दस्तावेज़:** परिवार के सभी वयस्क सदस्यों के आधार कार्ड, पंचायत निवास प्रमाण (वोटर आईडी/राशन कार्ड), आधार-सीडेड बैंक या डाकघर पासबुक, सभी सदस्यों की पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [nrega.nic.in](https://nrega.nic.in)",
        actions: [
          { label: "🌐 मनरेगा पोर्टल", url: "https://nrega.nic.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    kisan_credit_card: {
      match: ["kcc", "kisan credit", "কিসান ক্রেডিট", "किसान क्रेडिट", "crop loan", "4 percent interest"],
      en: {
        reply: "🌱 **Kisan Credit Card (KCC) Scheme:**\n\n💰 **Benefit:** Subsidized revolving crop and animal husbandry loan up to ₹3,00,000 at effectively 4% interest rate (7% baseline with 3% prompt repayment subvention).\n📋 **Eligibility Criteria:**\n• Individual or joint owner-cultivators owning agricultural land.\n• Tenant farmers, oral lessees, and sharecroppers cultivating leased land.\n• SHGs or Joint Liability Groups (JLGs) of farmers, including animal husbandry and fisheries practitioners.\n• Age: 18 to 75 years (borrowers over 60 require a major co-borrower/legal heir).\n\n📑 **Needed Documents:**\n• Duly filled KCC application form.\n• Identity and address proof: Aadhaar card, Voter ID, or PAN card.\n• Land title and record documents: RoR / Khatian / Porcha / 7/12 extract showing cultivable holding.\n• Crop cultivation proof / tenancy agreement (for sharecroppers/tenants).\n• Bank-approved 'No Dues' certificate / declaration of non-encumbrance from nearby credit institutions.\n\n🌐 **Official Portal:** [MoA&FW KCC Portal](https://agricoop.nic.in)\n📍 **Where to Apply:** Commercial Banks, RRBs, Cooperative Banks, or Duare Sarkar Camp.",
        actions: [
          { label: "🌐 Agriculture Portal", url: "https://agricoop.nic.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🌱 **কিসান ক্রেডিট কার্ড (Kisan Credit Card - KCC):**\n\n💰 **ঋণ সুবিধা:** মাত্র ৪% কার্যকর বার্ষিক সুদে ৩ লক্ষ টাকা পর্যন্ত সহজ ফসল ঋণ ও পশুপালন সহায়তা (৩% সময়মতো পরিশোধের ছাড় সহ)।\n📋 **যোগ্যতা:**\n• কৃষিজমির মালিক, বর্গাদার, ভাগচাষী, মৎস্যচাষী বা পশুপালক (১৮ থেকে ৭৫ বছর বয়সী)।\n• ৬০ বছরের ঊর্ধ্বে বয়স হলে প্রাপ্তবয়স্ক সহ-আবেদনকারী প্রয়োজন।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• যথাযথভাবে পূরণকৃত কেসিসি আবেদন ফর্ম\n• পরিচয় ও ঠিকানার প্রমাণ: আধার কার্ড, ভোটার কার্ড বা প্যান কার্ড\n• জমির স্বত্ব দলিল: খতিয়ান / পরচা (RoR/Porcha)\n• ফসল চাষের প্রমাণ বা ভাগচাষের চুক্তিপত্র\n• নিকটবর্তী ব্যাঙ্ক থেকে নো-ডিউস সার্টিফিকেট বা দায়হীনতার ঘোষণাপত্র\n\n🌐 **অফিসিয়াল পোর্টাল:** [agricoop.nic.in](https://agricoop.nic.in)",
        actions: [
          { label: "🌐 কৃষি মন্ত্রক", url: "https://agricoop.nic.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🌱 **किसान क्रेडिट कार्ड (KCC):**\n\n💰 **ऋण लाभ:** मात्र 4% प्रभावी रियायती ब्याज दर पर ₹3,00,000 तक का रिवाल्विंग किसान क्रेडिट कार्ड ऋण।\n📋 **पात्रता:** किसान, पट्टेदार, बटाईदार, पशुपालक व मछुआरे (आयु 18-75 वर्ष, 60+ हेतु सह-उधारकर्ता अनिवार्य)।\n📑 **ज़रूरी दस्तावेज़:** विधिवत भरा हुआ KCC आवेदन फॉर्म, पहचान व पता प्रमाण (आधार/वोटर/पैन), भू-अभिलेख पर्चा/खतियान (RoR/Porcha), बटाईदार अनुबंध, बैंक नो-ड्यूज प्रमाण पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [agricoop.nic.in](https://agricoop.nic.in)",
        actions: [
          { label: "🌐 कृषि विभाग", url: "https://agricoop.nic.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    midh_horticulture: {
      match: ["midh", "horticulture", "উদ্যানপালন", "बागवानी", "polyhouse subsidy", "cold room subsidy"],
      en: {
        reply: "🍇 **Mission for Integrated Development of Horticulture (MIDH):**\n\n💰 **Benefit:** 35% to 50% capital investment subsidy for polyhouses, shade nets, cold storage chains, tissue culture, and high-density orchards.\n📋 **Eligibility Criteria:**\n• Individual farmers, small and marginal growers, FPOs, registered cooperatives, SHGs, and agribusiness entrepreneurs.\n• Must own or hold registered long-term leasehold land suitable for horticultural crops (fruits, vegetables, spices, flowers, polyhouse cultivation, or nursery production).\n\n📑 **Needed Documents:**\n• Land record documents (RoR / Khatian / registered lease deed).\n• Aadhaar card and PAN card.\n• Detailed Project Report (DPR) / Technical blueprint (for cold rooms, polyhouses, protected shade nets).\n• Cost estimation/invoice quotations from approved empanelled vendors.\n• Bank account details and credit sanction letter (for bank-appraised credit-linked capital subsidies).\n\n🌐 **Official Portal:** [midh.gov.in](https://midh.gov.in)\n📍 **Where to Apply:** District Horticulture Officer (DHO) or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 MIDH Portal", url: "https://midh.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🍇 **সমন্বিত উদ্যানপালন বিকাশ মিশন (MIDH):**\n\n💰 **ভর্তুকি সুবিধা:** পলিহাউস, গ্রিনহাউস, কোল্ড স্টোরেজ, মাশরুম ও ফল-ফুল চাষে ৩৫% থেকে ৫০% সরকারি মূলধনী ভর্তুকি।\n📋 **যোগ্যতা:** ব্যক্তিগত কৃষক, ক্ষুদ্র ও প্রান্তিক চাষী, FPO, নিবন্ধিত সমবায় বা স্বনির্ভর দল যাঁদের নিজস্ব বা দীর্ঘমেয়াদী লিজকৃত উপযুক্ত জমি রয়েছে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• জমির খতিয়ান বা নিবন্ধিত লিজ দলিল (RoR/Khatian)\n• আধার কার্ড ও প্যান কার্ড\n• বিস্তারিত প্রকল্প রিপোর্ট (DPR) ও টেকনিক্যাল ব্লুপ্রিন্ট\n• অনুমোদিত ভেন্ডারের কাছ থেকে খরচের প্রাক্কলন কোটেশন\n• ব্যাঙ্ক বিবরণ ও ঋণ মঞ্জুরিপত্র (Credit Sanction Letter)\n\n🌐 **অফিসিয়াল পোর্টাল:** [midh.gov.in](https://midh.gov.in)",
        actions: [
          { label: "🌐 উদ্যানপালন দপ্তর", url: "https://midh.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🍇 **एकीकृत बागवानी विकास मिशन (MIDH):**\n\n💰 **सब्सिडी:** पॉलीहाउस, ग्रीनहाउस, कोल्ड स्टोरेज, फल-सब्जी बागवानी व नर्सरी हेतु 35% से 50% पूंजीगत सब्सिडी।\n📋 **पात्रता:** किसान, FPO, सहकारी समितियां, SHG उद्यमी जिनके पास उपयुक्त कृषि भूमि या पंजीकृत लीज डीड हो।\n📑 **ज़रूरी दस्तावेज़:** भूमि रिकॉर्ड (RoR/लीज डीड), आधार व पैन कार्ड, DPR (विस्तृत तकनीकी परियोजना रिपोर्ट), विक्रेता कोटेशन, बैंक ऋण स्वीकृति पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [midh.gov.in](https://midh.gov.in)",
        actions: [
          { label: "🌐 MIDH पोर्टल", url: "https://midh.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    minor_correction_land: {
      match: ["minor correction", "banglarbhumi correction", "রেকর্ড সংশোধন", "বানান ভুল", "পর্চা সংশোধন", "भू-अभिलेख सुधार", "khatian correction"],
      en: {
        reply: "📑 **Minor Correction of Land Records (West Bengal - Banglarbhumi):**\n\n⚖️ **Service:** Legal rectification of clerical, spelling, typography, or typographical area/share errors in computerized Record of Rights (CLR/Khatian/Parcha).\n📋 **Eligibility Criteria:**\n• Recorded raiyat (landholder) or their legitimate legal heirs possessing registered legal title.\n• Applies to clerical, spelling, typography, or typographical area/share errors in current computerized Record of Rights (CLR/Khatian/Parcha).\n\n📑 **Needed Documents:**\n• Certified copy of current Khatian / Record of Rights (RoR) displaying the clerical error.\n• Original and chain deeds: Registered Sale Deed, Gift Deed, or Partition Deed establishing the correct names/shares.\n• Notarized legal affidavit sworn before a Magistrate/Notary Public detailing the discrepancy.\n• Aadhaar Card / Voter ID of the recorded owner (for identity verification).\n• Up-to-date Land Revenue (Khajna) payment receipt.\n\n🌐 **Official Portal:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)\n📍 **Where to Apply:** Banglarbhumi Citizen Portal, Bangla Sahayata Kendra (BSK), or Office of the BL&LRO.",
        actions: [
          { label: "🌐 Banglarbhumi Portal", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "📑 **জমির রেকর্ডের ছোটখাটো সংশোধন (বাংলারভূমি):**\n\n⚖️ **নাগরিক পরিষেবা:** কম্পিউটারাইজড খতিয়ান বা পরচায় নাম, পিতার নাম, বানান বা অংশের করণিক ভুল দ্রুত আইনি সংশোধন।\n📋 **যোগ্যতা:** রেকর্ডভুক্ত রায়ত বা তাদের বৈধ উত্তরাধিকারী যাঁদের কাছে রেজিস্টার্ড দলিল রয়েছে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• ভুল প্রদর্শিত বর্তমান খতিয়ান / পরচার সার্টিফাইড কপি\n• মূল দলিল ও বায়া দলিল (রেজিস্টার্ড ক্রয়/দানপত্র/বণ্টননামা)\n• নোটারি পাবলিকের নিকট সম্পাদিত আইনি হলফনামা (Affidavit)\n• রেকর্ডভুক্ত মালিকের আধার কার্ড বা ভোটার আইডি\n• হালনাগাদ জমির খাজনা পরিশোধের রসিদ\n\n🌐 **অফিসিয়াল পোর্টাল:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 বাংলারভূমি পোর্টাল", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "📑 **भू-अभिलेखों का लघु संशोधन (बांगलारभूमि पश्चिम बंगाल):**\n\n⚖️ **सेवा:** कंप्यूटरीकृत खतियान/पर्चे में नाम, वर्तनी या अंश की लिपिकीय गलतियों का आधिकारिक ऑनलाइन सुधार।\n📋 **पात्रता:** पंजीकृत कानूनी हक रखने वाले दर्ज रैयत अथवा उनके वैध उत्तराधिकारी।\n📑 **ज़रूरी दस्तावेज़:** त्रुटिपूर्ण वर्तमान खतियान/पर्चे की प्रमाणित प्रति, मूल रजिस्ट्रीकृत डीड व बाया दस्तावेज, नोटरीकृत कानूनी शपथ पत्र, दर्ज मालिक का आधार/वoter कार्ड, अद्यतन भू-राजस्व (खजाना) रसीद।\n\n🌐 **ऑफिशियल पोर्टल:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 बांगलारभूमि पोर्टल", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    mutation_land: {
      match: ["mutation", "banglarbhumi mutation", "মিউটেশন", "জমির নামজারি", "नामांतरण", "section 50", "khatian"],
      en: {
        reply: "📜 **Mutation of Land Records (West Bengal - Banglarbhumi):**\n\n⚖️ **Service:** Legal transfer and recording of ownership title in computerized Record of Rights under Section 50 of WBLR Act, generating a new digital Khatian.\n📋 **Eligibility Criteria:**\n• Any person who has acquired legal ownership of land through registered purchase, gift, exchange, court decree, or ancestral inheritance (succession) under Section 50 of the West Bengal Land Reforms Act.\n• The seller/predecessor must hold a valid chain of title without unrecorded intervening encumbrances.\n\n📑 **Needed Documents:**\n• Registered deed of transfer (Sale Deed, Gift Deed, Exchange Deed).\n• For inheritance cases: Death Certificate and Legal Heir Certificate (issued by SDO/BDO/Court).\n• Previous recorded Khatian/Parcha of the transferor.\n• Up-to-date Land Tax (Khajna) / municipal property tax clearance receipt.\n• Aadhaar card and PAN card of the buyer and seller/donor.\n• Boundary sketch map and self-declaration affidavit regarding land ceilings.\n\n🌐 **Official Portal:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)\n📍 **Where to Apply:** Banglarbhumi Portal, Bangla Sahayata Kendra (BSK), or Office of the BL&LRO.",
        actions: [
          { label: "🌐 Banglarbhumi Portal", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "📜 **জমির মিউটেশন ও পৃথক খতিয়ান তৈরি (বাংলারভূমি):**\n\n⚖️ **নাগরিক পরিষেবা:** পশ্চিমবঙ্গ ভূমি সংস্কার আইনের ৫০ নম্বর ধারা অনুযায়ী ক্রয় বা উত্তরাধিকারসূত্রে প্রাপ্ত জমির আইনি নামপত্তন ও নিজস্ব খতিয়ান লাভ।\n📋 **যোগ্যতা:** যে কোনো ব্যক্তি যিনি রেজিস্টার্ড ক্রয়, হেবানামা, দানপত্র বা উত্তরাধিকারসূত্রে জমির বৈধ মালিকানা পেয়েছেন এবং বিক্রেতার স্বত্ব পরিষ্কার।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• রেজিস্টার্ড হস্তান্তর দলিল (ক্রয় দলিল, দানপত্র ইত্যাদি)\n• ওয়ারিশ সূত্রের ক্ষেত্রে: মৃত্যু শংসাপত্র ও ওয়ারিশান সার্টিফিকেট (SDO/BDO/কোর্ট)\n• বিক্রেতা বা পূর্বসূরীর পূর্ববর্তী রেকর্ডকৃত খতিয়ান/পর্চা\n• হালনাগাদ জমির খাজনা বা পুরসভার ট্যাক্স পরিশোধের রসিদ\n• ক্রেতা ও বিক্রেতার আধার কার্ড এবং প্যান কার্ড\n• সীমানা স্কেচ ম্যাপ ও ল্যান্ড সিলিং স্ব-ঘোষণাপত্র\n\n🌐 **অফিসিয়াল পোর্টাল:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 বাংলারভূমি", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "📜 **जमीन म्यूटेशन / नामांतरण (बांगलारभूमि पश्चिम बंगाल):**\n\n⚖️ **सेवा:** प. बंगाल भूमि सुधार अधिनियम की धारा 50 के अंतर्गत जमीन का आधिकारिक नामांतरण व नया डिजिटल खतियान निर्गमन।\n📋 **पात्रता:** क्रय, उपहार या पैतृक उत्तराधिकार द्वारा भूमि का स्वामित्व पाने वाले नागरिक जिनके विक्रेता का मालिकाना हक वैध हो।\n📑 **ज़रूरी दस्तावेज़:** पंजीकृत हस्तांतरण विलेख (रजिस्ट्री सेल डीड/दानपत्र), उत्तराधिकार में मृत्यु व वारिसान प्रमाणपत्र, पूर्ववर्ती खतियान/पर्चा, अद्यतन भू-राजस्व (खजाना) रसीद, क्रेता-विक्रेता का आधार व पैन कार्ड, भू-सीमा रेखाचित्र व सीलिंग शपथ पत्र।\n\n🌐 **ऑफिशियल पोर्टल:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 बांगलारभूमि पोर्टल", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    naps: {
      match: ["naps", "apprenticeship promotion", "শিক্ষানবিশি প্রচার", "शिक्षुता संवर्धन", "stipend 1500", "iti apprentice"],
      en: {
        reply: "🛠️ **National Apprenticeship Promotion Scheme (NAPS):**\n\n💰 **Benefit:** Industry practical on-job apprenticeship training + government stipend sharing (25% up to ₹1,500/month DBT) + National Apprenticeship Certificate (NAC).\n📋 **Eligibility Criteria:**\n• Trainee must have completed at least 14 years of age (18 years for designated hazardous industries).\n• Educational qualification: Class 5, 8, 10, or 12 pass, or ITI certificate holder (depending on designated or optional trade).\n• Must be registered on the Apprenticeship India Portal (apprenticeshipindia.gov.in).\n\n📑 **Needed Documents:**\n• Aadhaar card (mandatory for e-KYC).\n• Educational qualification mark sheets / ITI National Trade Certificate (NTC).\n• Aadhaar-seeded bank account passbook / cancelled cheque (for direct DBT stipend sharing).\n• Passport-size photograph.\n\n🌐 **Official Portal:** [apprenticeshipindia.gov.in](https://www.apprenticeshipindia.gov.in)\n📍 **Where to Apply:** Register online at apprenticeshipindia.gov.in or visit District Skill Development Office / ITIs.",
        actions: [
          { label: "🌐 NAPS Portal", url: "https://www.apprenticeshipindia.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🛠️ **জাতীয় শিক্ষানবিশি প্রচার যোজনা (NAPS):**\n\n💰 **সুবিধা:** শিল্প প্রতিষ্ঠানে হাতে-কলমে প্রশিক্ষণ + সরাসরি ব্যাঙ্ক অ্যাকাউন্টে সরকারি স্টাইপেন্ড (২৫% সর্বোচ্চ ₹১,৫০০/মাস) + জাতীয় শিক্ষানবিশি শংসাপত্র (NAC)।\n📋 **যোগ্যতা:**\n• বয়স ন্যূনতম ১৪ বছর (বিপজ্জনক শিল্পের জন্য ১৮ বছর)।\n• শিক্ষাগত যোগ্যতা: ৫ম, ৮ম, ১০ম, ১২শ শ্রেণি উত্তীর্ণ বা আইটিআই (ITI) পাস।\n• Apprenticeship India পোর্টালে রেজিস্ট্রেশন বাধ্যতামূলক।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• আধার কার্ড (ই-কেওয়াইসির জন্য)\n• শিক্ষাগত যোগ্যতার মার্কশিট বা ITI NTC সার্টিফিকেট\n• আধার লিঙ্কযুক্ত ব্যাঙ্ক পাসবুক বা ক্যানসেলড চেক\n• পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [apprenticeshipindia.gov.in](https://www.apprenticeshipindia.gov.in)",
        actions: [
          { label: "🌐 NAPS পোর্টাল", url: "https://www.apprenticeshipindia.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🛠️ **राष्ट्रीय शिक्षुता संवर्धन योजना (NAPS):**\n\n💰 **लाभ:** उद्योगों में हैंड्स-ऑन अप्रेंटिसशिप + सरकारी वजीफा अंशदान (25% अधिकतम ₹1,500/माह सीधे DBT) + राष्ट्रीय शिक्षुता प्रमाण पत्र।\n📋 **पात्रता:** आयु कम से कम 14 वर्ष (जोखिम उद्योगों हेतु 18 वर्ष)। 5वीं, 8वीं, 10वीं, 12वीं या ITI उत्तीर्ण। पोर्टल पर पंजीकरण अनिवार्य।\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, शैक्षणिक अंकपत्र/ITI NTC, आधार-सीडेड बैंक पासबुक/रद्द चेक, पासपोर्ट फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [apprenticeshipindia.gov.in](https://www.apprenticeshipindia.gov.in)",
        actions: [
          { label: "🌐 NAPS पोर्टल", url: "https://www.apprenticeshipindia.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    nats: {
      match: ["nats", "boat", "apprenticeship training", "শিক্ষানবিশি প্রশিক্ষণ", "शिक्षुता प्रशिक्षण", "graduate apprentice", "diploma apprentice"],
      en: {
        reply: "🎓 **National Apprenticeship Training Scheme (NATS 2.0):**\n\n💰 **Benefit:** 1-year paid practical training in leading corporate/public sector industries with monthly stipend (₹8,000 to ₹9,000+/month) + Certificate of Proficiency issued by Govt of India.\n📋 **Eligibility Criteria:**\n• Citizen of India aged 16 years or above.\n• Holds a recognized Degree or Diploma in Engineering/Technology or a general graduate degree (BA, B.Sc, B.Com, BBA, BCA, etc.) from an accredited university/board.\n• Must have graduated within the last 3 to 5 years.\n• Must not have prior formal work experience or completed apprenticeship training for 1 year or more.\n\n📑 **Needed Documents:**\n• Degree / Diploma passing certificate or consolidated final mark sheet.\n• Aadhaar card.\n• Aadhaar-linked active bank account passbook.\n• Institutional student ID / Bonafide certificate.\n• Active email address and mobile number registered on the NATS 2.0 portal.\n\n🌐 **Official Portal:** [nats.education.gov.in](https://nats.education.gov.in)\n📍 **Where to Apply:** Online enrollment at nats.education.gov.in.",
        actions: [
          { label: "🌐 NATS 2.0 Portal", url: "https://nats.education.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🎓 **জাতীয় শিক্ষানবিশি প্রশিক্ষণ যোজনা (NATS 2.0):**\n\n💰 **সুবিধা:** শীর্ষ প্রতিষ্ঠানে ১ বছরের পেইড বাস্তব প্রশিক্ষণ + প্রতি মাসে সরাসরি স্টাইপেন্ড (₹৮,০০০-₹৯,০০০+/মাস) + ভারত সরকারের দক্ষতা প্রশংসাপত্র।\n📋 **যোগ্যতা:**\n• ১৬ বছর বা তদূর্ধ্ব ভারতীয় নাগরিক।\n• ইঞ্জিনিয়ারিং/টেকনোলজিতে ডিগ্রি বা ডিপ্লোমা অথবা সাধারণ স্নাতক (BA, BSc, BCom, BCA ইত্যাদি) বিগত ৩-৫ বছরে উত্তীর্ণ।\n• পূর্বে ১ বছর বা তার বেশি চাকরির অভিজ্ঞতা বা শিক্ষানবিশি করা যাবে না।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• ডিগ্রি/ডিপ্লোমা পাসের সার্টিফিকেট বা চূড়ান্ত মার্কশিট\n• আধার কার্ড\n• আধার সংযুক্ত সক্রিয় ব্যাঙ্ক পাসবুক\n• কলেজের স্টুডেন্ট আইডি বা বোনাফাইড সার্টিফিকেট\n• পোর্টালে নিবন্ধিত সক্রিয় ইমেল ও মোবাইল নম্বর\n\n🌐 **অফিসিয়াল পোর্টাল:** [nats.education.gov.in](https://nats.education.gov.in)",
        actions: [
          { label: "🌐 NATS পোর্টাল", url: "https://nats.education.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🎓 **राष्ट्रीय शिक्षुता प्रशिक्षण योजना (NATS 2.0):**\n\n💰 **लाभ:** उद्योगों में 1 वर्ष का व्यावहारिक सवैतनिक प्रशिक्षण + ₹8,000 से ₹9,000+/माह सीधा वजीफा + भारत सरकार का प्रवीणता प्रमाण पत्र।\n📋 **पात्रता:** 16 वर्ष या अधिक आयु के भारतीय नागरिक जिन्होंने पिछले 3-5 वर्षों में इंजीनियरिंग/डिप्लोमा या सामान्य स्नातक (BA/BSc/BCom/BCA) उत्तीर्ण किया हो। पूर्व में 1 वर्ष का कार्य अनुभव न हो।\n📑 **ज़रूरी दस्तावेज़:** डिग्री/डिप्लोमा उत्तीर्ण प्रमाण पत्र या अंतिम अंकपत्र, आधार कार्ड, आधार-लिंक्ড बैंक पासबुक, कॉलेज आईडी/बोनाफाइड, वैध ईमेल व मोबाइल नंबर।\n\n🌐 **ऑफिशियल पोर्टल:** [nats.education.gov.in](https://nats.education.gov.in)",
        actions: [
          { label: "🌐 NATS पोर्टल", url: "https://nats.education.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    patta_application: {
      match: ["patta", "পাট্টা", "पट्टा", "vested land", "খাসজমি", "নিহিত জমি", "bl&lro patta", "bpl land"],
      en: {
        reply: "🏡 **Patta Application (Settlement of Vested Land - West Bengal):**\n\n📜 **Benefit:** Permanent, heritable legal settlement and Patta deed for agricultural or homestead vested government land (up to 1 acre) free of cost + land revenue exemption.\n📋 **Eligibility Criteria:**\n• Landless rural poor, agricultural labourers, marginal farmers, or village artisans permanently residing in West Bengal.\n• Priority given to Scheduled Castes (SC), Scheduled Tribes (ST), women-headed households, and families lacking any agricultural or homestead land.\n• Must be physically occupying or cultivating government-vested (khas) land.\n\n📑 **Needed Documents:**\n• Prescribed Patta application form (Form 1) submitted to the Block Land & Land Reforms Officer (BL&LRO).\n• Identity proof: Aadhaar card and Voter ID (EPIC).\n• Proof of permanent residence and local Gram Panchayat domicile.\n• Digital Ration Card / BPL certificate.\n• Family income certificate from BDO/Gram Panchayat Pradhan.\n• Possession certificate / verification report from the local Revenue Inspector proving physical possession of the vested plot.\n\n🌐 **Official Portal:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)\n📍 **Where to Apply:** Office of the BL&LRO, Gram Panchayat Office, or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 Banglarbhumi Portal", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🏡 **পাট্টা আবেদন (সরকারি খাস/ভেস্টেড খাসজমির বন্দোবস্ত - পশ্চিমবঙ্গ):**\n\n📜 **সুবিধা:** বাস্তুভিটা বা কৃষিকাজের জন্য সরকারি ভেস্টেড খাসজমির স্থায়ী উত্তরাধিকারযোগ্য পাট্টা দলিল (১ একর পর্যন্ত) সম্পূর্ণ বিনামূল্যে প্রদান ও রাজস্ব ছাড়।\n📋 **যোগ্যতা:**\n• পশ্চিমবঙ্গের স্থায়ী বাসিন্দা ভূমিহীন গ্রামীণ দরিদ্র, কৃষি শ্রমিক, প্রান্তিক চাষী বা গ্রামীণ কারিগর।\n• তফসিলি জাতি (SC), তফসিলি উপজাতি (ST), মহিলা-প্রধান পরিবার এবং ভূমিহীনরা অগ্রাধিকার পাবেন।\n• সরকারি ভেস্টেড খাসজমিতে বাস্তবিক দখল বা চাষাবাদ থাকতে হবে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• বিএলঅ্যান্ডএলআরও (BL&LRO) অফিসে জমা দেওয়ার জন্য নির্ধারিত পাট্টা আবেদন ফর্ম (ফর্ম ১)\n• পরিচয় ও ঠিকানার প্রমাণ: আধার কার্ড ও ভোটার কার্ড (EPIC)\n• স্থায়ী বাসস্থান ও স্থানীয় গ্রাম পঞ্চায়েতের ডোমিসাইল প্রমাণ\n• ডিজিটাল রেশন কার্ড / বিপিএল (BPL) শংসাপত্র\n• বিডিও বা গ্রাম পঞ্চায়েত প্রধান প্রদত্ত পারিবারিক আয়ের সার্টিফিকেট\n• স্থানীয় রেভিনিউ ইন্সপেক্টর (RI) দ্বারা প্রদত্ত জমিতে বাস্তবিক দখলের তদন্ত রিপোর্ট/প্রত্যয়ন\n\n🌐 **অফিসিয়াল পোর্টাল:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 বাংলারভূমি", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏡 **पट्टा आवेदन (सरकारी निहित/वेस्टेड भूमि बंदोबस्त - पश्चिम बंगाल):**\n\n📜 **लाभ:** कृषि अथवा आवास हेतु सरकारी निहित (खास) भूमि का स्थायी, उत्तराधिकार योग्य निःशुल्क पट्टा (1 एकड़ तक) व भू-राजस्व छूट।\n📋 **पात्रता:** प. बंगाल के भूमिहीन ग्रामीण निर्धन, खेतिहर मजदूर, सीमांत किसान या दस्तकार। SC/ST व महिला-प्रधान परिवारों को प्राथमिकता। सरकारी निहित भूमि पर वास्तविक कब्जा आवश्यक।\n📑 **ज़रूरी दस्तावेज़:** BL&LRO में प्रस्तुत निर्धारित पट्टा आवेदन फॉर्म (प्रपत्र 1), आधार कार्ड व वोटर आईडी, ग्राम पंचायत निवास प्रमाण, डिजिटल राशन कार्ड/BPL प्रमाण पत्र, BDO/प्रधान से पारिवारिक आय प्रमाण पत्र, स्थानीय राजस्व निरीक्षक (RI) द्वारा भौतिक कब्जे की सत्यापन रिपोर्ट।\n\n🌐 **ऑफिशियल पोर्टल:** [banglarbhumi.gov.in](https://banglarbhumi.gov.in)",
        actions: [
          { label: "🌐 बांगलारभूमि पोर्टल", url: "https://banglarbhumi.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    grievance: {
      match: ["complaint", "complain", "grievance", "shikayat", "অভিযোগ", "দরখাস্ত", "letter", "দরখাস্ত লেখা", "money not", "taka aseni", "taka pacchi na", "paisa nahi", "payment stuck", "dbt", "npci"],
      en: {
        reply: "📝 **How to File a Grievance or Representation Letter:**\n\n1. **NayaSetu Grievance Drafter**: Click **'Grievance Drafter' (অভিযোগ প্রস্তুতি)** in the top menu. Choose your issue (e.g. stalled application, DBT bank rejection), and the system will instantly draft an official representation letter for BDO, SDO, or Duare Sarkar counters.\n2. **Chief Minister Helpline**: Call directly at 📞 **033-2214-5555**\n3. **Bank NPCI DBT Issue**: Visit your home branch, submit the *Aadhaar NPCI DBT Seeding Mandate*, and obtain a stamped receipt.",
        actions: [
          { label: "📝 Draft Grievance Letter", action: "grievance-drafter" },
          { label: "🏢 Administrative Offices", action: "helpline-and-offices" },
          { label: "📄 Decipher Rejection SMS", action: "notice-explainer" }
        ]
      },
      bn: {
        reply: "📝 **অভিযোগ জানানো ও সরকারি দরখাস্ত লেখার নিয়ম:**\n\n1. **নয়া সেতু গ্রিভেন্স ড্রাফটার**: আমাদের **'অভিযোগ প্রস্তুতি' (Grievance Drafter)** টুলটি খুলুন। আপনার সমস্যা নির্বাচন করলেই সিস্টেম BDO বা দুয়ারে সরকার ক্যাম্পের নামাঙ্কিত প্রস্তুত আবেদনপত্র তৈরি করে দেবে।\n2. **মুখ্যমন্ত্রী হেল্পলাইন**: সরাসরি ফোন করুন 📞 **033-2214-5555** নম্বরে।\n3. **ব্যাঙ্ক NPCI DBT সমস্যা**: হোম ব্রাঞ্চে গিয়ে *Aadhaar NPCI DBT Seeding* ফর্ম জমা দিয়ে সিলমোহর করা রসিদ সংগ্রহ করুন।",
        actions: [
          { label: "📝 দরখাস্ত তৈরি করুন", action: "grievance-drafter" },
          { label: "🏢 প্রশাসনিক অফিস তালিকা", action: "helpline-and-offices" },
          { label: "📄 এসএমএস ডিক্রিপ্টার", action: "notice-explainer" }
        ]
      },
      hi: {
        reply: "📝 **शिकायत दर्ज करने व दरखास्त तैयार करने के उपाय:**\n\n1. **नया सेतु ग्रीवेंस ड्राफ्टर**: मेन्यू में **'অভিযোগ প্রস্তুতি' (Grievance Drafter)** खोलें। यहाँ से आप BDO या दुयरे सरकार के नाम आधिकारिक कानूनी आवेदन पत्र तुरंत बना सकते हैं।\n2. **मुख्यमंत्री हेल्पलाइन (CM Helpline)**: सीधे कॉल करें 📞 **033-2214-5555**\n3. **NPCI DBT समस्या**: बैंक शाखा में जाकर आधार सीडिंग मैन्डेट फॉर्म जमा करें।",
        actions: [
          { label: "📝 शिकायत पत्र बनाएं", action: "grievance-drafter" },
          { label: "🏢 प्रशासनिक कार्यालय सूची", action: "helpline-and-offices" },
          { label: "📄 रिजेक्शन SMS समझें", action: "notice-explainer" }
        ]
      }
    },

    website_guide: {
      match: ["website", "guide", "help", "kahan", "কোথায়", "কি করতে হবে", "kya karna", "kaise use", "কই", "কিসে যাব"],
      en: {
        reply: "🧭 **NayaSetu Website Navigation Guide — How to use our features:**\n\n1. 🔍 **Where to Search**: Use the prominent **'Ask NyayaSetu AI'** search bar on the homepage to find schemes in plain language.\n2. ⚖️ **Check Eligibility (Eligibility Wizard)**: Click **'যোগ্যতা যাচাই'** in the top navigation bar to discover which schemes you qualify for.\n3. 📋 **View Document Checklists (Schemes Directory)**: Click **'প্রকল্প নির্দেশিকা'** to see exhaustive document requirements, portal links, and rejection remedies.\n4. 📝 **Draft Representation Letters (Grievance Drafter)**: Click **'অভিযোগ প্রস্তুতি'** to generate formal letters for BDO, SDO, or Duare Sarkar camps.\n5. 📄 **Decipher Rejection SMS (Notice Explainer)**: Click **'নোটিশ / রসিদ বুঝুন'** to paste SMS or upload a photo of a rejection slip for a plain-language explanation.",
        actions: [
          { label: "⚖️ Eligibility Wizard", action: "eligibility-wizard" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "📝 Grievance Drafter", action: "grievance-drafter" },
          { label: "📄 Notice Explainer", action: "notice-explainer" }
        ]
      },
      bn: {
        reply: "🧭 **নয়া সেতু (NayaSetu) ওয়েবসাইটে কোথায় কি করবেন — পূর্ণ নির্দেশিকা:**\n\n1. 🔍 **সার্চ করবেন কোথায়**: হোমপেজের শীর্ষে **'Ask NyayaSetu AI'** সার্চ বক্সে সরাসরি লিখুন (যেমন: *'মেয়েদের বিয়ে'*, *'চাষীদের টাকা'*).\n2. ⚖️ **যোগ্যতা যাচাই (Eligibility Wizard)**: মেনুতে **'যোগ্যতা যাচাই'** ক্লিক করে নিজের বয়স, জাতি ও আয় নির্বাচন করুন — সিস্টেম যোগ্য প্রকল্প দেখাবে।\n3. 📋 **ডকুমেন্টস নির্দেশিকা (Schemes Directory)**: **'প্রকল্প নির্দেশিকা'** খুলে প্রতি প্রকল্পের নিয়ম ও সরকারি লিঙ্ক দেখুন।\n4. 📝 **অভিযোগ প্রস্তুতি (Grievance Drafter)**: **'অভিযোগ প্রস্তুতি'**-তে বিডিও বা দুয়ারে সরকারের নামাঙ্কিত প্রস্তুত আবেদনপত্র বানান।\n5. 📄 **এসএমএস বুঝুন (Notice Explainer)**: **'নোটিশ / রসিদ বুঝুন'**-এ সরকারি মেসেজ পেস্ট করুন, AI সহজ ভাষায় বুঝিয়ে দেবে।",
        actions: [
          { label: "⚖️ যোগ্যতা যাচাই", action: "eligibility-wizard" },
          { label: "📋 প্রকল্প তালিকা", action: "schemes-and-docs" },
          { label: "📝 অভিযোগ ড্রাফটার", action: "grievance-drafter" },
          { label: "📄 এসএমএস ডিক্রিপ্টার", action: "notice-explainer" }
        ]
      },
      hi: {
        reply: "🧭 **नया सेतु (NayaSetu) वेबसाइट पर कहाँ क्या करना है — पूरी जानकारी:**\n\n1. 🔍 **सर्च कहाँ करें**: होमपेज पर ऊपर **'Ask NyayaSetu AI'** सर्च बॉक्स में सीधे अपनी भाषा में लिखें।\n2. ⚖️ **योग्यता जाँचें (Eligibility Wizard)**: मेन्यू में **'যোগ্যতা যাচাই'** बटन दबाकर पात्रता देखें।\n3. 📋 **दस्तावेज़ सूची (Schemes Directory)**: **'প্রকল্প নির্দেশিকা'** पर क्लिक करके हर योजना की पूरी चेकलिस्ट देखें।\n4. 📝 **शिकायत ड्राफ्टर (Grievance Drafter)**: **'অভিযোগ প্রস্তুতি'** में अपनी समस्या चुनें, सिस्टम तैयार दरखास्त पत्र बना देगा।\n5. 📄 **एसएमएस समझें (Notice Explainer)**: **'নোটিশ / রসিদ বুঝুন'** में सरकारी रिजेक्शन पर्ची या एसएमएस पेस्ट करें।",
        actions: [
          { label: "⚖️ योग्यता जाँचें", action: "eligibility-wizard" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" },
          { label: "📝 शिकायत ड्राफ्टर", action: "grievance-drafter" },
          { label: "📄 एसएमएस डिक्रिप्टर", action: "notice-explainer" }
        ]
      }
    }
  };

  // Inject Styles (WhatsApp Dark Mode with Multi-Lingual Top Bar)
  const styleEl = document.createElement('style');
  styleEl.id = 'nayasetu-chatbot-whatsapp-styles';
  styleEl.textContent = `
    #nayasetu-chat-widget {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", "Noto Sans Bengali", sans-serif;
    }

    .ns-fab-btn {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: #25D366;
      color: #ffffff;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 18px rgba(37, 211, 102, 0.45), 0 2px 8px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }
    .ns-fab-btn:hover {
      transform: scale(1.08);
      background: #20BA5A;
      box-shadow: 0 6px 24px rgba(37, 211, 102, 0.6);
    }
    .ns-fab-btn:active {
      transform: scale(0.95);
    }
    .ns-fab-btn .material-symbols-outlined {
      font-size: 30px;
    }

    .ns-fab-ripple {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: #25D366;
      opacity: 0.5;
      animation: ns-pulse 2.2s infinite;
      pointer-events: none;
    }
    @keyframes ns-pulse {
      0% { transform: scale(1); opacity: 0.6; }
      70% { transform: scale(1.4); opacity: 0; }
      100% { transform: scale(1.4); opacity: 0; }
    }

    .ns-fab-tooltip {
      position: absolute;
      right: 72px;
      top: 50%;
      transform: translateY(-50%);
      background: #1f2c34;
      color: #e9edef;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 4px 14px rgba(0,0,0,0.4);
      border: 1px solid #2a3942;
      opacity: 0;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .ns-fab-btn:hover .ns-fab-tooltip {
      opacity: 1;
      transform: translateY(-50%) translateX(-4px);
    }

    .ns-chat-window {
      position: fixed;
      bottom: 96px;
      right: 24px;
      width: 410px;
      max-width: calc(100vw - 32px);
      height: 640px;
      max-height: calc(100vh - 120px);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.75), 0 0 0 1px #2a3942;
      background: #0b141a;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      transform-origin: bottom right;
      z-index: 99999;
    }
    .ns-chat-window.ns-hidden {
      opacity: 0;
      transform: scale(0.85) translateY(20px);
      pointer-events: none;
      visibility: hidden;
    }

    /* WhatsApp Header */
    .ns-chat-header {
      background: #1f2c34;
      color: #e9edef;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #2a3942;
      flex-shrink: 0;
    }
    .ns-header-profile {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .ns-header-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #005c4b;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #25D366;
      border: 2px solid #25D366;
      position: relative;
      flex-shrink: 0;
    }
    .ns-header-avatar .material-symbols-outlined {
      font-size: 22px;
    }
    .ns-online-indicator {
      position: absolute;
      bottom: -1px;
      right: -1px;
      width: 11px;
      height: 11px;
      border-radius: 50%;
      background: #25D366;
      border: 2px solid #1f2c34;
    }
    .ns-header-info h3 {
      margin: 0;
      font-size: 14.5px;
      font-weight: 700;
      color: #e9edef;
      line-height: 1.2;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .ns-ai-badge {
      font-size: 10px;
      padding: 1px 6px;
      background: #005c4b;
      color: #25D366;
      border-radius: 10px;
      border: 1px solid #25D366/40;
    }
    .ns-header-info p {
      margin: 2px 0 0;
      font-size: 11px;
      color: #8696a0;
      font-weight: 500;
      line-height: 1;
    }
    .ns-header-actions {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .ns-header-btn {
      background: transparent;
      border: none;
      color: #aebac1;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s, color 0.15s;
    }
    .ns-header-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #e9edef;
    }

    /* Sub-header Language Switcher Bar */
    .ns-lang-bar {
      background: #111b21;
      padding: 6px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #222e35;
      flex-shrink: 0;
    }
    .ns-lang-pills {
      display: flex;
      gap: 4px;
    }
    .ns-lang-pill {
      background: #202c33;
      color: #8696a0;
      border: 1px solid #2a3942;
      padding: 3px 9px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .ns-lang-pill:hover {
      color: #e9edef;
      border-color: #00a884;
    }
    .ns-lang-pill.active {
      background: #005c4b;
      color: #25D366;
      border-color: #25D366;
    }
    .ns-engine-tag {
      font-size: 10px;
      color: #8696a0;
      display: flex;
      align-items: center;
      gap: 3px;
    }

    /* API Key Drawer (collapsible) */
    .ns-api-drawer {
      background: #182229;
      padding: 10px 14px;
      border-bottom: 1px solid #2a3942;
      display: none;
      flex-direction: column;
      gap: 6px;
      font-size: 12px;
      color: #d1d7db;
    }
    .ns-api-drawer.open {
      display: flex;
    }
    .ns-api-input-row {
      display: flex;
      gap: 6px;
    }
    .ns-api-input {
      flex: 1;
      background: #2a3942;
      border: 1px solid #3b4a54;
      border-radius: 6px;
      color: #e9edef;
      padding: 6px 8px;
      font-size: 11px;
      outline: none;
    }
    .ns-api-save-btn {
      background: #00a884;
      color: #111b21;
      border: none;
      border-radius: 6px;
      padding: 6px 10px;
      font-weight: 700;
      font-size: 11px;
      cursor: pointer;
    }

    /* WhatsApp Dark Wallpaper Background */
    .ns-chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px 14px;
      background-color: #0b141a;
      background-image: 
        radial-gradient(#1f2c34 1px, transparent 1px),
        radial-gradient(#182229 1px, #0b141a 1px);
      background-size: 20px 20px;
      background-position: 0 0, 10px 10px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      scroll-behavior: smooth;
    }
    .ns-chat-messages::-webkit-scrollbar {
      width: 5px;
    }
    .ns-chat-messages::-webkit-scrollbar-thumb {
      background: #2a3942;
      border-radius: 3px;
    }

    .ns-chat-pill {
      align-self: center;
      background: #182229;
      color: #8696a0;
      font-size: 10.5px;
      padding: 5px 12px;
      border-radius: 8px;
      margin-bottom: 6px;
      text-align: center;
      border: 1px solid #222e35;
      max-width: 90%;
    }

    /* Message Bubbles */
    .ns-msg {
      max-width: 84%;
      padding: 9px 12px 7px;
      font-size: 13.5px;
      line-height: 1.45;
      word-wrap: break-word;
      position: relative;
      animation: ns-msg-in 0.2s cubic-bezier(0.2, 0.9, 0.3, 1);
    }
    @keyframes ns-msg-in {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .ns-msg-ai {
      align-self: flex-start;
      background: #005c4b;
      color: #e9edef;
      border-radius: 12px 12px 12px 2px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
    }
    .ns-msg-ai strong {
      color: #ffffff;
      font-weight: 700;
    }

    .ns-msg-user {
      align-self: flex-end;
      background: #ffffff;
      color: #111b21;
      border-radius: 12px 12px 2px 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
      font-weight: 500;
    }

    .ns-msg-meta {
      font-size: 10px;
      margin-top: 4px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 3px;
    }
    .ns-msg-ai .ns-msg-meta { color: #92b8af; }
    .ns-msg-user .ns-msg-meta { color: #667781; }
    .ns-msg-checks { color: #53bdeb; font-size: 12px; font-weight: bold; }

    .ns-msg p { margin: 0 0 6px 0; }
    .ns-msg p:last-child { margin-bottom: 0; }
    .ns-msg ul { margin: 4px 0 6px 16px; padding: 0; }
    .ns-msg li { margin-bottom: 3px; }

    .ns-portal-link {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      margin: 6px 0;
      padding: 6px 10px;
      background: #0b141a;
      border: 1px solid #25D366;
      border-radius: 8px;
      color: #25D366 !important;
      font-weight: 600;
      font-size: 12px;
      text-decoration: none;
      transition: background 0.15s, transform 0.1s;
    }
    .ns-portal-link:hover {
      background: #25D366;
      color: #111b21 !important;
    }

    /* Action Buttons in Bubbles */
    .ns-action-row {
      margin-top: 8px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .ns-chat-action-btn {
      background: #1f2c34;
      color: #e9edef;
      border: 1px solid #2a3942;
      padding: 5px 10px;
      border-radius: 14px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      text-decoration: none;
      transition: all 0.15s;
    }
    .ns-chat-action-btn:hover {
      background: #25D366;
      color: #111b21;
      border-color: #25D366;
    }
    a.ns-chat-action-btn.ns-official-redirect-btn {
      background: #25D366 !important;
      color: #111b21 !important;
      border: 1px solid #25D366 !important;
      font-weight: 700 !important;
      box-shadow: 0 2px 8px rgba(37, 211, 102, 0.35);
      text-decoration: none !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 5px !important;
    }
    a.ns-chat-action-btn.ns-official-redirect-btn:hover {
      background: #1ebc57 !important;
      color: #0b141a !important;
      border-color: #1ebc57 !important;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(37, 211, 102, 0.55);
    }

    /* Quick Suggestion Chips */
    .ns-quick-chips {
      padding: 8px 12px;
      background: #111b21;
      border-top: 1px solid #222e35;
      display: flex;
      gap: 6px;
      overflow-x: auto;
      flex-shrink: 0;
      scrollbar-width: none;
    }
    .ns-quick-chips::-webkit-scrollbar { display: none; }
    .ns-chip {
      background: #202c33;
      color: #d1d7db;
      border: 1px solid #2a3942;
      padding: 5px 10px;
      border-radius: 14px;
      font-size: 11px;
      font-weight: 500;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s;
      flex-shrink: 0;
    }
    .ns-chip:hover {
      background: #005c4b;
      color: #ffffff;
      border-color: #00a884;
    }

    /* Input Footer */
    .ns-chat-input-bar {
      background: #202c33;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-top: 1px solid #2a3942;
      flex-shrink: 0;
    }
    .ns-input-wrapper {
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
    }
    .ns-chat-input {
      width: 100%;
      background: #2a3942;
      color: #d1d7db;
      border: none;
      outline: none;
      padding: 10px 14px;
      border-radius: 20px;
      font-size: 13.5px;
      font-family: inherit;
    }
    .ns-chat-input::placeholder {
      color: #8696a0;
      font-size: 12.5px;
    }
    .ns-send-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #00a884;
      color: #111b21;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: background 0.15s, transform 0.1s;
    }
    .ns-send-btn:hover {
      background: #25D366;
      transform: scale(1.05);
    }
    .ns-send-btn:active { transform: scale(0.95); }
    .ns-send-btn .material-symbols-outlined { font-size: 20px; font-weight: bold; }

    /* Typing Dots */
    .ns-typing {
      align-self: flex-start;
      background: #005c4b;
      color: #e9edef;
      border-radius: 12px 12px 12px 2px;
      padding: 8px 14px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 4px;
    }
    .ns-dot {
      width: 6px;
      height: 6px;
      background: #25D366;
      border-radius: 50%;
      animation: ns-blink 1.2s infinite both;
    }
    .ns-dot:nth-child(2) { animation-delay: 0.2s; }
    .ns-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes ns-blink {
      0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
      40% { opacity: 1; transform: scale(1.2); }
    }

    @media (max-width: 480px) {
      .ns-chat-window {
        bottom: 0;
        right: 0;
        width: 100vw;
        height: 100vh;
        max-width: 100vw;
        max-height: 100vh;
        border-radius: 0;
      }
      #nayasetu-chat-widget {
        bottom: 16px;
        right: 16px;
      }
    }
  `;
  document.head.appendChild(styleEl);

  // Quick Chips Configuration by Language
  const CHIPS_DATA = {
    en: [
      { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
      { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
      { label: "🎓 West Bengal Student Credit Card", query: "WB Student Credit Card eligibility and documents" },
      { label: "💳 Student Credit Card", query: "West Bengal Student Credit Card loan rules" },
      { label: "📝 How to Complain", query: "How to draft a grievance letter to BDO?" },
      { label: "🧭 Website Guide", query: "How to navigate and use NayaSetu website?" }
    ],
    bn: [
      { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
      { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
      { label: "🎓 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ডের জন্য কি কি ডকুমেন্টস লাগে?" },
      { label: "💳 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ড প্রকল্পের নিয়মাবলী" },
      { label: "📝 অভিযোগ কোথায় দেব?", query: "বিডিও অফিসে কীভাবে অভিযোগ বা দরখাস্ত জমা দেব?" },
      { label: "🧭 ওয়েবসাইট নির্দেশিকা", query: "নয়া সেতু ওয়েবসাইটে কোথায় কি করতে হবে?" }
    ],
    hi: [
      { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
      { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
      { label: "🎓 स्टूडेंट क्रेडिट कार्ड", query: "Student Credit Card eligibility aur documents" },
      { label: "💳 स्टूडेंट क्रेडिट कार्ड", query: "स्टूडेंट क्रेडिट कार्ड योजना के क्या नियम हैं?" },
      { label: "📝 शिकायत पत्र तैयार करें", query: "क्वेश्चन या शिकायत कहाँ देना है?" },
      { label: "🧭 वेबसाइट गाइड", query: "वेबसाइट पे कहाँ क्या करना है?" }
    ]
  };

  const PLACEHOLDERS = {
    en: "Ask NayaSetu AI anything... (English / বাংলা / हिन्दी)",
    bn: "নয়া সেতু AI-কে যেকোনো প্রশ্ন করুন... (বাংলা / English / हिन्दी)",
    hi: "नया सेतु AI से कुछ भी पूछें... (हिन्दी / বাংলা / English)"
  };

  // Create Markup
  const container = document.createElement('div');
  container.id = 'nayasetu-chat-widget';
  container.innerHTML = `
    <!-- Floating Action Button -->
    <button class="ns-fab-btn" id="nsChatFab" title="NayaSetu AI Assistant">
      <div class="ns-fab-ripple"></div>
      <span class="material-symbols-outlined" id="nsFabIcon">smart_toy</span>
      <div class="ns-fab-tooltip">Ask NayaSetu AI</div>
    </button>

    <!-- Main WhatsApp Chat Window -->
    <div class="ns-chat-window ns-hidden" id="nsChatWindow">
      <!-- WhatsApp Dark Header -->
      <div class="ns-chat-header">
        <div class="ns-header-profile">
          <div class="ns-header-avatar">
            <span class="material-symbols-outlined">balance</span>
            <div class="ns-online-indicator"></div>
          </div>
          <div class="ns-header-info">
            <h3>NayaSetu AI <span class="ns-ai-badge" id="nsAiBadge">Active</span></h3>
            <p id="nsHeaderSub">West Bengal Citizen AI Guide</p>
          </div>
        </div>
        <div class="ns-header-actions">
          <button class="ns-header-btn" id="nsApiKeyBtn" title="Gemini AI Key Settings">
            <span class="material-symbols-outlined" style="font-size: 18px;">vpn_key</span>
          </button>
          <button class="ns-header-btn" id="nsClearBtn" title="Clear Chat History">
            <span class="material-symbols-outlined" style="font-size: 19px;">delete_sweep</span>
          </button>
          <button class="ns-header-btn" id="nsCloseBtn" title="Minimize Chat">
            <span class="material-symbols-outlined" style="font-size: 22px;">expand_more</span>
          </button>
        </div>
      </div>

      <!-- Quick Language Switcher Bar -->
      <div class="ns-lang-bar">
        <div class="ns-lang-pills">
          <button class="ns-lang-pill ${currentLang === 'en' ? 'active' : ''}" data-lang="en">English</button>
          <button class="ns-lang-pill ${currentLang === 'bn' ? 'active' : ''}" data-lang="bn">বাংলা</button>
          <button class="ns-lang-pill ${currentLang === 'hi' ? 'active' : ''}" data-lang="hi">हिंदी</button>
        </div>
        <div class="ns-engine-tag" id="nsEngineTag">
          <span class="material-symbols-outlined" style="font-size:12px; color:#25D366;">bolt</span>
          <span>AI Assistant</span>
        </div>
      </div>

      <!-- Optional API Key Drawer -->
      <div class="ns-api-drawer" id="nsApiDrawer">
        <div><strong>Google Gemini API Key</strong> (Optional for direct LLM generation):</div>
        <div class="ns-api-input-row">
          <input type="password" class="ns-api-input" id="nsApiKeyInput" placeholder="Paste AI Studio API Key..." />
          <button type="button" class="ns-api-save-btn" id="nsSaveApiKeyBtn">Save</button>
        </div>
      </div>

      <!-- Messages Stream -->
      <div class="ns-chat-messages" id="nsChatMessages">
        <div class="ns-chat-pill">🔒 West Bengal Government Schemes & Citizen Rights AI Assistant</div>
      </div>

      <!-- Quick Suggestion Chips -->
      <div class="ns-quick-chips" id="nsQuickChips"></div>

      <!-- Input Footer -->
      <form class="ns-chat-input-bar" id="nsChatForm">
        <div class="ns-input-wrapper">
          <input type="text" class="ns-chat-input" id="nsChatInput" placeholder="${PLACEHOLDERS[currentLang] || PLACEHOLDERS.en}" autocomplete="off"/>
        </div>
        <button type="submit" class="ns-send-btn" id="nsSendBtn" title="Send Message">
          <span class="material-symbols-outlined">send</span>
        </button>
      </form>
    </div>
  `;
  document.body.appendChild(container);

  // References
  const fabBtn = document.getElementById('nsChatFab');
  const chatWindow = document.getElementById('nsChatWindow');
  const closeBtn = document.getElementById('nsCloseBtn');
  const clearBtn = document.getElementById('nsClearBtn');
  const chatForm = document.getElementById('nsChatForm');
  const chatInput = document.getElementById('nsChatInput');
  const messagesBox = document.getElementById('nsChatMessages');
  const quickChips = document.getElementById('nsQuickChips');
  const fabIcon = document.getElementById('nsFabIcon');
  const apiKeyBtn = document.getElementById('nsApiKeyBtn');
  const apiDrawer = document.getElementById('nsApiDrawer');
  const apiKeyInput = document.getElementById('nsApiKeyInput');
  const saveApiKeyBtn = document.getElementById('nsSaveApiKeyBtn');
  const engineTag = document.getElementById('nsEngineTag');

  let conversationHistory = [];

  // Initialize API Key input if saved
  const savedKey = localStorage.getItem('nayasetu_gemini_api_key') || '';
  if (savedKey) {
    apiKeyInput.value = savedKey;
    engineTag.innerHTML = '<span class="material-symbols-outlined" style="font-size:12px; color:#25D366;">verified</span> <span>Gemini LLM</span>';
  }

  // Update Chips based on current language
  function renderQuickChips() {
    quickChips.innerHTML = '';
    const chips = CHIPS_DATA[currentLang] || CHIPS_DATA.en;
    chips.forEach(c => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ns-chip';
      btn.setAttribute('data-query', c.query);
      btn.textContent = c.label;
      btn.addEventListener('click', () => sendMessage(c.query));
      quickChips.appendChild(btn);
    });
  }
  renderQuickChips();

  // Helper: Time in WhatsApp format
  function getFormattedTime() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    return `${hours}:${minutes} ${ampm}`;
  }

  // Helper: Parse markdown (bold, links, lists) into safe HTML
  function renderMarkdown(text) {
    if (!text) return '';
    let html = text;
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, function(match, label, url) {
      return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="ns-portal-link"><span class="material-symbols-outlined" style="font-size:14px;">open_in_new</span> ${label}</a>`;
    });

    const lines = html.split('\n');
    let inList = false;
    let result = [];

    for (let line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('• ') || trimmed.startsWith('- ')) {
        if (!inList) {
          result.push('<ul>');
          inList = true;
        }
        result.push(`<li>${trimmed.substring(2)}</li>`);
      } else {
        if (inList) {
          result.push('</ul>');
          inList = false;
        }
        if (trimmed) {
          result.push(`<p>${line}</p>`);
        } else {
          result.push('<br/>');
        }
      }
    }
    if (inList) result.push('</ul>');
    return result.join('');
  }

  // Append Message to UI
  function appendMessage(sender, text, actions = []) {
    const isUser = sender === 'user';
    const msgEl = document.createElement('div');
    msgEl.className = `ns-msg ${isUser ? 'ns-msg-user' : 'ns-msg-ai'}`;

    const contentHtml = isUser 
      ? `<div>${text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>`
      : `<div>${renderMarkdown(text)}</div>`;

    let actionsHtml = '';
    if (actions && actions.length > 0) {
      actionsHtml = '<div class="ns-action-row">';
      actions.forEach(act => {
        if (act.type === 'link' || act.url) {
          actionsHtml += `<a href="${act.url}" target="_blank" rel="noopener noreferrer" class="ns-chat-action-btn ns-official-redirect-btn"><span class="material-symbols-outlined" style="font-size:14px; font-weight:bold;">open_in_new</span> ${act.label}</a>`;
        } else if (act.text || act.query) {
          const q = act.text || act.query;
          actionsHtml += `<button type="button" class="ns-chat-action-btn ns-query-btn" data-query="${q}"><span class="material-symbols-outlined" style="font-size:13px;">chat</span> ${act.label}</button>`;
        } else if (act.action) {
          actionsHtml += `<button type="button" class="ns-chat-action-btn ns-modal-btn" data-modal="${act.action}"><span class="material-symbols-outlined" style="font-size:13px;">touch_app</span> ${act.label}</button>`;
        }
      });
      actionsHtml += '</div>';
    }

    const timeStr = getFormattedTime();
    const checksStr = isUser ? '<span class="ns-msg-checks">✓✓</span>' : '';

    msgEl.innerHTML = `
      ${contentHtml}
      ${actionsHtml}
      <div class="ns-msg-meta">
        <span>${timeStr}</span>
        ${checksStr}
      </div>
    `;

    messagesBox.appendChild(msgEl);
    messagesBox.scrollTop = messagesBox.scrollHeight;

    // Attach click events
    msgEl.querySelectorAll('.ns-query-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        if (query) sendMessage(query);
      });
    });

    msgEl.querySelectorAll('.ns-modal-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const modalId = btn.getAttribute('data-modal');
        handleModalTrigger(modalId);
      });
    });

    conversationHistory.push({ role: sender, content: text });
    try {
      sessionStorage.setItem('nayasetu_chat_history', JSON.stringify(conversationHistory));
    } catch (e) {}
  }

  // Handle Internal NayaSetu Modal Triggers
  function handleModalTrigger(modalId) {
    if (typeof window.openModal === 'function') {
      window.openModal(modalId);
      if (modalId === 'schemes-and-docs' && typeof window.loadSchemesDirectory === 'function') {
        window.loadSchemesDirectory();
      } else if (modalId === 'helpline-and-offices' && typeof window.loadOfficesDirectory === 'function') {
        window.loadOfficesDirectory();
      }
      if (window.innerWidth < 640) toggleChat(false);
    } else {
      window.location.href = `/?open=${modalId}`;
    }
  }

  // Typing Indicator
  let typingEl = null;
  function showTypingIndicator() {
    if (typingEl) return;
    typingEl = document.createElement('div');
    typingEl.className = 'ns-typing';
    typingEl.id = 'nsTypingDots';
    const label = currentLang === 'bn' ? 'নয়া সেতু AI টাইপ করছে' : (currentLang === 'hi' ? 'नया सेतु AI लिख रहा है' : 'NayaSetu AI is thinking');
    typingEl.innerHTML = `
      <span style="font-size: 11px; margin-right: 4px; color: #aebac1;">${label}</span>
      <div class="ns-dot"></div>
      <div class="ns-dot"></div>
      <div class="ns-dot"></div>
    `;
    messagesBox.appendChild(typingEl);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  function hideTypingIndicator() {
    if (typingEl && typingEl.parentNode) {
      typingEl.parentNode.removeChild(typingEl);
      typingEl = null;
    }
  }

  // Language Switch Handler
  function setLanguage(lang, announce = true) {
    currentLang = lang;
    localStorage.setItem('nayasetu_chat_lang', lang);
    chatInput.placeholder = PLACEHOLDERS[lang] || PLACEHOLDERS.en;

    document.querySelectorAll('.ns-lang-pill').forEach(pill => {
      if (pill.getAttribute('data-lang') === lang) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });

    renderQuickChips();

    if (announce) {
      if (lang === 'en') {
        appendMessage('assistant', "👋 **Language switched to English.** How can I assist you with West Bengal schemes, scholarships, or citizen rights today?", [
          { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
          { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
          { label: "🎓 West Bengal Student Credit Card", query: "WB Student Credit Card eligibility and documents" },
          { label: "🧭 Website Guide", action: "schemes-and-docs" }
        ]);
      } else if (lang === 'bn') {
        appendMessage('assistant', "🙏 **ভাষা পরিবর্তন করা হয়েছে: বাংলা।** পশ্চিমবঙ্গ সরকারের জনকল্যাণমূলক প্রকল্প, স্কলারশিপ বা অধিকার সংক্রান্ত কী তথ্য জানতে চান?", [
          { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
          { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
          { label: "🎓 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ডের জন্য কি কি ডকুমেন্টস লাগে?" },
          { label: "⚖️ যোগ্যতা যাচাই", action: "eligibility-wizard" }
        ]);
      } else if (lang === 'hi') {
        appendMessage('assistant', "🙏 **भाषा बदल दी गई है: हिंदी।** पश्चिम बंगाल सरकार की किसी भी योजना, स्कॉलरशिप या नया सेतु वेबसाइट सहायता के लिए अपना प्रश्न पूछें।", [
          { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
          { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
          { label: "🎓 स्टूडेंट क्रेडिट कार्ड", query: "Student Credit Card eligibility aur documents" },
          { label: "🧭 वेबसाइट गाइड", action: "schemes-and-docs" }
        ]);
      }
    }
  }

  // Direct Call to Google Gemini REST API (when backend is offline or for pure client generative AI)
  async function callGeminiDirect(query) {
    const key = localStorage.getItem('nayasetu_gemini_api_key');
    if (!key) return null;

    try {
      const langPrompt = currentLang === 'en' 
        ? "Respond completely in fluent English." 
        : (currentLang === 'bn' ? "Respond completely in natural Bengali (বাংলা)." : "Respond completely in respectful Hindi.");

      const contents = [];
      conversationHistory.slice(-4).forEach(m => {
        contents.push({
          role: m.role === 'user' ? 'user' : 'model',
          parts: [{ text: m.content }]
        });
      });
      contents.push({
        role: 'user',
        parts: [{ text: `${GEMINI_SYSTEM_PROMPT}\n\nLanguage Instruction: ${langPrompt}\n\nUser Question: ${query}` }]
      });

      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: contents })
      });

      if (response.ok) {
        const data = await response.json();
        const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
        if (text) {
          return {
            reply: text,
            actions: [
              { label: "📋 Schemes Directory", action: "schemes-and-docs" },
              { label: "⚖️ Eligibility Check", action: "eligibility-wizard" }
            ]
          };
        }
      }
    } catch (e) {
      console.warn('Direct Gemini call failed:', e);
    }
    return null;
  }

  // Strict Scope Verifier for Client-Side Fallback & Offline Mode
  function isInScopeQuery(text) {
    if (!text || typeof text !== 'string') return false;
    const q = text.toLowerCase().trim();
    if (!q) return false;

    // Whole-word tokens check for short words
    const words = new Set((q.match(/\b\w+\b/g) || []).map(w => w.toLowerCase()));

    // Greetings
    const greetingWords = ["hi", "hello", "hey", "namaste", "pranam", "adaab", "salam"];
    if (greetingWords.some(w => words.has(w)) || ["নমস্কার", "হ্যালো", "नमस्ते", "प्रणाम"].some(w => q.includes(w))) {
      if (q.split(/\s+/).length <= 4) return true;
    }

    // Identity / greetings / thanks
    if (["who are you", "what is your name", "your name", "who made you", "who created you", "তোমার নাম", "আপনার নাম", "তোমার পরিচয়", "আপনার পরিচয়", "तुम्हारा नाम", "तुम कौन हो", "आप कौन हैं", "thanks", "thank you", "ধন্যবাদ", "धन्यवाद"].some(w => q.includes(w))) {
      return true;
    }

    // Language switches
    if (["talk in english", "speak in english", "বাংলায় কথা", "বাংলায় বলো", "কথা বাংলায়", "हिंदी में बात", "hindi", "english", "bangla", "bengali"].some(l => q.includes(l))) {
      return true;
    }

    // NayaSetu Platform & Tools
    const nayasetuTerms = [
      "nayasetu", "naya setu", "nyayasetu", "saral", "নয়া সেতু", "ন্যায়সেতু", "ওয়েবসাইট", "website",
      "portal", "project", "প্রকল্প", "এই সাইট", "এই ওয়েবসাইট", "এই পোর্টাল", "কি কাজ", "কি করে", "guide", "নির্দেশিকা",
      "eligibility", "wizard", "যোগ্যতা", "যোগ্যতা যাচাই", "पात्रता", "চেকার",
      "grievance", "drafter", "অভিযোগ", "দরখাস্ত", "দরখাস্ত লেখা", "আবেদনপত্র", "शिकायत", "letter", "petition",
      "notice", "explainer", "নোটিশ", "এসএমএস", "রসিদ", "মেসেজ", "decipher", "ব্যাখ্যা",
      "duare sarkar", "দুয়ারে সরকার", "ক্যাম্প", "office", "দপ্তর", "কার্যালয়", "helpline", "হেল্পলাইন", "phone", "ফোন"
    ];
    if (nayasetuTerms.some(t => q.includes(t))) return true;

    // West Bengal Schemes & Rights keywords
    const schemeTerms = [
      "lakshmi", "lakshmir", "লক্ষ্মী", "ভাণ্ডার", "লাক্ষ্মীর", "annapurna", "অন্নপূর্ণা", "लक्ष्मी", "भंडार", "भण्डार", "अन्नपूर्णा",
      "krishak", "কৃষক", "বন্ধু", "bandhu", "chashi", "চাষী", "किसान", "kisan", "porcha", "পরচা", "khatian", "খতিয়ান", "कृषक", "बंधु", "पर्चा",
      "kanya", "kanyashree", "কন্যাশ্রী", "rupashree", "রূপশ্রী", "marriage", "বিয়ে", "বিয়ের টাকা", "कन्याश्री", "रूपश्री", "शादी", "विवाह",
      "svmcm", "bikash bhavan", "বিবেকানন্দ", "বিকাশ ভবন", "scholarship", "স্কলারশিপ", "বৃত্তি", "aikyashree", "oasis", "ঐক্যশ্রী", "ওএসিস", "sikshashree", "শিক্ষাশ্রী", "medhashree", "মেধাশ্রী", "yogyasree", "যোগ্যশ্রী", "विवेकानंद", "विकास भवन", "छात्रवृत्ति", "स्कॉलरशिप",
      "swasthya", "স্বাস্থ্য", "স্বাস্থ্য সাথী", "health card", "ayushman", "আয়ুষ্মান", "বয় বন্দনা", "वय वंदना", "vay vandana", "स्वास्थ्य", "स्वास्थ्य साथी", "आयुष्मान",
      "yuva", "yuba", "যুব", "শক্তি", "युवा", "shakti", "bharosa", "ভরোসা", "unemployment", "বেকার", "युवा शक्ति",
      "karmashree", "কর্মশ্রী", "50 day", "৫০ দিন", "job card", "জব কার্ড", "100 day", "১০০ দিন", "कर्मश्री",
      "awas", "আবাস", "বাড়ি", "ঘর", "makan", "shasya", "bima", "বীমা", "বিমা", "crop insurance", "आवास", "फसल बीमा", "शस्य बीमा",
      "tarun", "swapno", "তরুণ", "স্বপ্ন", "ট্যাব", "ট্যাবলেট", "smartphone", "तरुण", "स्वप्न", "टैबलेट",
      "student credit card", "wbscc", "ক্রেডিট কার্ড", "bhabishyat", "ভবিষ্যৎ", "wbbccs", "loan", "লোন", "भविष्य", "क्रेडिट कार्ड",
      "jai bangla", "জয় বাংলা", "jai johar", "জয় জোহার", "taposili", "তফসিলী", "manabik", "মানবিক", "pension", "পেনশন", "ভাতা", "पेंशन",
      "khadya", "খাদ্য সাথী", "ration", "রেশন", "রেশন কার্ড", "chokher alo", "চোখের আলো", "sishu sathi", "শিশু সাথী", "matsyajeebi", "মৎস্যজীবী", "राशन", "राशन कार्ड",
      "ডিবিটি", "npci", "এনপিসিআই", "bank", "ব্যাঙ্ক", "passbook", "পাসবই", "aadhaar", "আধার", "account", "অ্যাকাউন্ট", "taka", "টাকা", "paisa", "paise", "rupees", "rupaye", "डीबीटी", "आधार", "बैंक",
      "single account", "joint account", "একক অ্যাকাউন্ট", "জয়েন্ট অ্যাকাউন্ট",
      "rejection", "রিজেক্ট", "বাতিল", "টাকা আসেনি", "টাকা পাইনি", "টাকা পাচ্ছি না", "টাকা কবে ঢুকবে", "stuck",
      "apply", "আবেদন", "ফর্ম", "ডকুমেন্ট", "documents", "কাগজ", "কাগজপত্র", "schema", "scheme", "schemes", "योजना", "दस्तावेज़", "दस्तावेज", "कागजात", "नियम", "पात्रता", "pmis", "internship", "ইন্টার্নশিপ", "ইন্টার্ন", "इंटर्नशिप", "rksy", "rajya khadya", "food security", "খাদ্য সুরক্ষা", "rojgar", "রোজগার", "employment bank", "এমপ্লয়মেন্ট ব্যাঙ্ক", "रोजगार", "soil health", "মৃত্তিকা", "মৃত্তিকা স্বাস্থ্য", "मृदा स्वास्थ्य", "sukanya", "samriddhi", "সুকন্যা", "সুকন্যা সমৃদ্ধি", "सुकन्या", "सुकन्या समृद्धि", "swachh bharat", "swachh", "nirmal bangla", "নির্মল বাংলা", "শৌচাগার", "স্বচ্ছ ভারত", "शौचालय", "ihhl", "udyam", "msme", "উদ্যম", "ক্ষুদ্র শিল্প", "उद्यम", "utkarsh", "উৎকর্ষ", "উৎকর্ষ বাংলা", "pbssd", "उत्कर्ष बांग्ला", "migrant", "shramashree", "karmasathi", "পরিযায়ী", "শ্রমশ্রী", "কর্মসাথী", "প্রবাসী श्रमिक", "श्रमश्री", "कर्मसाथी", "surya ghar", "সূর্য ঘর", "सूर्य घर", "svanidhi", "স্বনিধি", "स्वनिधि", "post matric", "পোস্ট ম্যাট্রিক", "पोस्ट मैट्रिक", "pmay", "awas yojana", "আবাস যোজনা", "आवास योजना", "pmfme", "pm-fme", "খাদ্য প্রক্রিয়াকরণ", "खाद्य प्रसंस्करण", "pmgkay", "গরীব কল্যাণ", "गरीब कल्याण", "jan dhan", "জন ধন", "जन धन", "pmjdy", "jeevan jyoti", "জীবন জ্যোতি", "जीवन ज्योति", "pmjjby", "pmkisan", "pm-kisan", "পিএম কিষাণ", "पीएम किसान", "mkssy", "pm-mkssy", "মৎস্য কিষাণ", "मत्स्य किसान", "mudra", "মুদ্রা", "मुद्रा", "shram yogi", "maan-dhan", "শ্রমযোগী", "मान-धन", "suraksha bima", "সুরক্ষা বীমা", "सुरक्षा बीमा", "pmsby", "vishwakarma", "বিশ্বকর্মা", "विश्वकर्मा", "vikas", "বিরাসত", "विरासत", "ujjwala", "উজ্জ্বলা", "उज्ज्वला", "lpg", "গ্যাস", "सिलेंडर", "pre matric", "প্রাক ম্যাট্রিক", "प्री मैट्रिक", "pmegp", "কর্মসংস্থান কর্মসূচি", "रोजगार सृजन"
    ];
    if (schemeTerms.some(st => q.includes(st))) return true;

    // Check against KNOWLEDGE_BASE keys & match arrays
    for (const k in KNOWLEDGE_BASE) {
      if (KNOWLEDGE_BASE[k].match && KNOWLEDGE_BASE[k].match.some(m => q.includes(m.toLowerCase()))) {
        return true;
      }
    }

    return false;
  }

  // Client-Side Conversational Intelligence Fallback
  function getClientFallbackReply(userText) {
    const q = userText.toLowerCase();

    // STRICT SCOPE CHECK: Refuse queries unrelated to NayaSetu and WB government schemes
    if (!isInScopeQuery(userText)) {
      if (currentLang === 'bn') {
        return {
          reply: "⚠️ **অনুরোধটি নয়া সেতুর পরিধির বাইরে:**\n\nআমি **নয়া সেতু AI** — আমি শুধুমাত্র **নয়া সেতু (NayaSetu) প্রকল্প** এবং **পশ্চিমবঙ্গ সরকারের বিভিন্ন জনকল্যাণমূলক প্রকল্প, স্কলারশিপ ও নাগরিক অধিকার** সম্পর্কিত প্রশ্নের উত্তর দিতে পারি।\n\n👉 অনুগ্রহ করে এই প্রকল্প (যেমন: যোগ্যতা যাচাই, অভিযোগ ড্রাফটার, নোটিশ বিশ্লেষক) অথবা পশ্চিমবঙ্গ সরকারের কোনো স্কিম (যেমন লক্ষ্মীর ভাণ্ডার, কৃষক বন্ধু, কন্যাশ্রী, স্বাস্থ্য সাথী ইত্যাদি) সম্পর্কিত প্রশ্ন করুন।",
          actions: [
            { label: "🌸 লক্ষ্মীর ভাণ্ডার প্রকল্প", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
            { label: "🌾 কৃষক বন্ধু নির্দেশিকা", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
            { label: "⚖️ যোগ্যতা যাচাই (Eligibility)", action: "eligibility-wizard" },
            { label: "🧭 নয়া সেতু ওয়েবসাইট গাইড", action: "schemes-and-docs" }
          ]
        };
      } else if (currentLang === 'hi') {
        return {
          reply: "⚠️ **यह प्रश्न नया सेतु के दायरे से बाहर है:**\n\nमैं **नया सेतु AI** हूँ — मैं केवल **नया सेतु (NayaSetu) प्रोजेक्ट** और **पश्चिम बंगाल सरकार की योजनाओं, छात्रवृत्तियों व नागरिक अधिकारों** से संबंधित प्रश्नों के उत्तर दे सकता हूँ।\n\n👉 कृपया इस प्रोजेक्ट (जैसे: पात्रता जाँच, शिकायत ड्राफ्टर, नोटिस विश्लेषक) या पश्चिम बंगाल की सरकारी योजनाओं (जैसे लक्ष्मी भंडार, कृषक बंधु, कन्याश्री, स्वास्थ्य साथी आदि) से संबंधित प्रश्न पूछें।",
          actions: [
            { label: "🌸 लक्ष्मी भंडार योजना", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
            { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
            { label: "⚖️ योग्यता जाँचें (Eligibility)", action: "eligibility-wizard" },
            { label: "🧭 नया सेतु वेबसाइट गाइड", action: "schemes-and-docs" }
          ]
        };
      } else {
        return {
          reply: "⚠️ **I can only answer questions regarding the NayaSetu project.**\n\nI am **NayaSetu AI**, the dedicated digital assistant for the **NayaSetu platform** and **West Bengal Government Welfare Schemes, Scholarships, and Citizen Rights**.\n\n👉 Please ask questions regarding this project (such as our Eligibility Wizard, Grievance Drafter, or Notice Explainer) or West Bengal government schemes (such as Lakshmir Bhandar, Krishak Bandhu, Kanyashree, SVMCM, etc.).",
          actions: [
            { label: "🌸 PM Surya Ghar Details", query: "What documents are required for PM Surya Ghar?" },
            { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
            { label: "⚖️ Eligibility Wizard", action: "eligibility-wizard" },
            { label: "🧭 NayaSetu Platform Guide", action: "schemes-and-docs" }
          ]
        };
      }
    }

    // 1. Identity & Name
    if (["who are you", "what is your name", "your name", "who made you", "who created you", "তোমার নাম", "আপনার নাম", "তোমার পরিচয়", "আপনার পরিচয়", "तुम्हारा नाम", "तुम कौन हो", "आप कौन हैं"].some(w => q.includes(w))) {
      if (currentLang === 'bn') {
        return {
          reply: "🙏 **আমার নাম 'নয়া সেতু AI' (NayaSetu AI / ন্যায়সেতু AI)।**\n\nআমি পশ্চিমবঙ্গ সরকারের জনকল্যাণমূলক প্রকল্পসমূহ, ছাত্রবৃত্তি, প্রয়োজনীয় নথিপত্র এবং নাগরিক অধিকারের সঠিক তথ্য জানাতে তৈরি একটি বিশেষ AI সহকারী। আপনি যেকোনো প্রকল্প সম্পর্কে আমাকে জিজ্ঞাসা করতে পারেন!",
          actions: [
            { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
            { label: "🧭 ওয়েবসাইট নির্দেশিকা", action: "schemes-and-docs" }
          ]
        };
      } else if (currentLang === 'hi') {
        return {
          reply: "🙏 **मेरा नाम 'नया सेतु AI' (NayaSetu AI / न्यायसेतु AI) है।**\n\nमैं पश्चिम बंगाल सरकार की सभी जन-कल्याणकारी योजनाओं, छात्रवृत्तियों और आवश्यक दस्तावेज़ों की सही जानकारी देने और इस वेबसाइट पर नागरिकों की सहायता के लिए बनाया गया AI सहायक हूँ।",
          actions: [
            { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
            { label: "🧭 वेबसाइट गाइड", action: "schemes-and-docs" }
          ]
        };
      } else {
        return {
          reply: "👋 **My name is 'NayaSetu AI' (ন্যায়সেতু AI).**\n\nI am your dedicated digital assistant for West Bengal Government Welfare Schemes (such as Lakshmir Bhandar, Krishak Bandhu, Kanyashree), Student Scholarships (SVMCM, Oasis), Mandatory Document Checklists, and Administrative Grievances.\n\nFeel free to ask me anything about any scheme or navigating this platform!",
          actions: [
            { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
            { label: "📋 Schemes Directory", action: "schemes-and-docs" },
            { label: "📝 Grievance Drafter", action: "grievance-drafter" }
          ]
        };
      }
    }

    // 2. Greetings
    const isGreeting = (["hi", "hello", "hey", "good morning", "good evening"].some(w => q === w || q.startsWith(w + " ")) || ["নমস্কার", "হ্যালো", "नमस्ते", "प्रणाम"].some(w => q.includes(w))) && q.split(" ").length <= 4;
    if (isGreeting) {
      if (currentLang === 'bn') {
        return {
          reply: "🙏 **নমস্কার! আমি নয়া সেতু AI।**\n\nপশ্চিমবঙ্গ সরকারের যেকোনো প্রকল্প, স্কলারশিপ বা অধিকার সংক্রান্ত সহায়তা পেতে আপনার প্রশ্ন লিখুন বা নিচের বিকল্প থেকে বেছে নিন।",
          actions: [
            { label: "🌸 লক্ষ্মীর ভাণ্ডার", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
            { label: "🌾 কৃষক বন্ধু", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
            { label: "🎓 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ডের জন্য কি কি ডকুমেন্টস লাগে?" }
          ]
        };
      } else if (currentLang === 'hi') {
        return {
          reply: "🙏 **नमस्ते! मैं नया सेतु AI हूँ।**\n\nपश्चिम बंगाल सरकार की योजनाओं, छात्रवृत्तियों या आवश्यक दस्तावेज़ों के बारे में आप क्या जानना चाहते हैं?",
          actions: [
            { label: "🌸 लक्ष्मी भंडार", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
            { label: "🌾 कृषक बंधु", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
            { label: "🎓 स्टूडेंट क्रेडिट कार्ड", query: "Student Credit Card eligibility aur documents" }
          ]
        };
      } else {
        return {
          reply: "👋 **Hello! I am NayaSetu AI.**\n\nHow can I help you today with West Bengal government schemes, scholarships, document checklists, or administrative grievances?",
          actions: [
            { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
            { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
            { label: "🎓 West Bengal Student Credit Card", query: "WB Student Credit Card eligibility and documents" }
          ]
        };
      }
    }

    // 3. Match against structured knowledge base (best/longest match priority)
    let bestMatchKey = null;
    let longestMatchLen = 0;
    for (let key in KNOWLEDGE_BASE) {
      const item = KNOWLEDGE_BASE[key];
      if (item.match) {
        for (const m of item.match) {
          const ml = m.toLowerCase();
          if (q.includes(ml) && ml.length > longestMatchLen) {
            longestMatchLen = ml.length;
            bestMatchKey = key;
          }
        }
      }
    }
    if (bestMatchKey) {
      const item = KNOWLEDGE_BASE[bestMatchKey];
      const localized = item[currentLang] || item.en;
      return {
        reply: localized.reply,
        actions: localized.actions || []
      };
    }

    // 4. Dynamic Context-Aware Fallback (Never static)
    if (currentLang === 'bn') {
      return {
        reply: `💡 **আপনার প্রশ্ন:** *"${userText}"*\n\nআমি **নয়া সেতু AI** হিসেবে আপনাকে পশ্চিমবঙ্গ সরকারের বিভিন্ন নাগরিক অধিকার, জনকল্যাণমূলক প্রকল্প, স্কলারশিপ ও নথিপত্রের নিয়মে সহায়তা করতে পারি।\n\n👉 অনুগ্রহ করে নিচের বিষয়গুলো থেকে বেছে নিন অথবা আপনার প্রশ্নটি আরও বিশদে লিখুন:`,
        actions: [
          { label: "🌸 লক্ষ্মীর ভাণ্ডার চেকলিস্ট", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
          { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
          { label: "⚖️ নিজের যোগ্যতা যাচাই", action: "eligibility-wizard" },
          { label: "📋 সকল প্রকল্প দেখুন", action: "schemes-and-docs" }
        ]
      };
    } else if (currentLang === 'hi') {
      return {
        reply: `💡 **आपके प्रश्न के संबंध में:** *"${userText}"*\n\nमैं **नया सेतु AI** हूँ। मैं पश्चिम बंगाल सरकार की सभी योजनाओं, छात्रवृत्तियों और आवश्यक दस्तावेज़ों की पूरी जानकारी दे सकता हूँ।\n\n👉 कृपया नीचे दिए गए विकल्पों में से चुनें या अपना प्रश्न और स्पष्ट रूप से लिखें:`,
        actions: [
          { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
          { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
          { label: "⚖️ योग्यता जाँचें", action: "eligibility-wizard" },
          { label: "📋 सभी योजनाएं देखें", action: "schemes-and-docs" }
        ]
      };
    } else {
      return {
        reply: `💡 **Regarding your query:** *"${userText}"*\n\nI am **NayaSetu AI**, your comprehensive assistant for West Bengal Government welfare schemes, scholarships, and citizen rights. I am here to assist you with document verifications, eligibility questions, and representation letters.\n\n👉 Please select an option below or specify your question with more details:`,
        actions: [
          { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
          { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
          { label: "🎓 West Bengal Student Credit Card", query: "WB Student Credit Card eligibility and documents" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      };
    }
  }

  // Send Message Logic
  async function sendMessage(text) {
    text = (text || '').trim();
    if (!text) return;

    // Detect language switch requests in text
    const lower = text.toLowerCase();
    if (lower.includes("talk in english") || lower.includes("speak in english") || lower.includes("reply in english") || lower.includes("english please") || lower === "english") {
      setLanguage('en', false);
    } else if (lower.includes("বাংলায় কথা") || lower.includes("বাংলায় বলো") || lower.includes("বাংলায় বল") || lower.includes("কথা বাংলায়") || lower === "বাংলা" || lower === "bengali" || lower === "bangla") {
      setLanguage('bn', false);
    } else if (lower.includes("हिंदी में बात") || lower.includes("हिंदी में बोलो") || lower.includes("बात हिंदी में") || lower === "हिंदी" || lower === "hindi") {
      setLanguage('hi', false);
    }

    // Append User Message to UI
    appendMessage('user', text);
    chatInput.value = '';
    showTypingIndicator();

    const storedKey = localStorage.getItem('nayasetu_gemini_api_key') || '';

    // 1. Try backend API endpoint
    try {
      const apiUrl = getApiChatbotUrl();
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 6500);

      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          message: text,
          history: conversationHistory.slice(-4),
          language: currentLang,
          api_key: storedKey
        }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (res.ok) {
        const data = await res.json();
        hideTypingIndicator();
        appendMessage('assistant', data.reply || 'Data received.', data.suggested_actions || []);
        return;
      }
    } catch (err) {
      console.warn('Backend API request skipped or unavailable:', err);
    }

    // 2. Try direct client Gemini API if user configured key
    if (storedKey) {
      const geminiDirect = await callGeminiDirect(text);
      if (geminiDirect) {
        hideTypingIndicator();
        appendMessage('assistant', geminiDirect.reply, geminiDirect.actions);
        return;
      }
    }

    // 3. Fallback to comprehensive local multi-lingual intelligence
    setTimeout(() => {
      hideTypingIndicator();
      const fallback = getClientFallbackReply(text);
      appendMessage('assistant', fallback.reply, fallback.actions);
    }, 350);
  }

  // Toggle Chat Window Open/Close
  function toggleChat(forceOpen) {
    const isHidden = chatWindow.classList.contains('ns-hidden');
    const shouldOpen = forceOpen !== undefined ? forceOpen : isHidden;

    if (shouldOpen) {
      chatWindow.classList.remove('ns-hidden');
      fabIcon.textContent = 'close';
      chatInput.focus();
      if (messagesBox.querySelectorAll('.ns-msg').length === 0) {
        showWelcomeMessage();
      }
    } else {
      chatWindow.classList.add('ns-hidden');
      fabIcon.textContent = 'smart_toy';
    }
  }

  // Welcome Message
  function showWelcomeMessage() {
    try {
      const cached = sessionStorage.getItem('nayasetu_chat_history');
      if (cached) {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) {
          conversationHistory = [];
          parsed.forEach(m => appendMessage(m.role, m.content));
          return;
        }
      }
    } catch (e) {}

    let welcomeText, actions;
    if (currentLang === 'bn') {
      welcomeText = (
        "🙏 **নমস্কার! আমি 'নয়া সেতু AI' (NayaSetu AI)।**\n\n" +
        "পশ্চিমবঙ্গ সরকারের যেকোনো জনকল্যাণমূলক প্রকল্প (যেমন লক্ষ্মীর ভাণ্ডার, কৃষক বন্ধু, কন্যাশ্রী), " +
        "ছাত্রবৃত্তি (SVMCM, Oasis), প্রয়োজনীয় ডকুমেন্টস তালিকা বা ওয়েবসাইটে যেকোনো সহায়তার জন্য আমি সর্বদা প্রস্তুত।\n\n" +
        "👉 নিচে ক্লিক করুন বা সরাসরি আপনার প্রশ্ন লিখুন:"
      );
      actions = [
        { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
        { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
        { label: "🎓 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ডের জন্য কি কি ডকুমেন্টস লাগে?" },
        { label: "🧭 ওয়েবসাইট নির্দেশিকা", action: "schemes-and-docs" }
      ];
    } else if (currentLang === 'hi') {
      welcomeText = (
        "🙏 **नमस्ते! मैं 'नया सेतु AI' (NayaSetu AI) हूँ।**\n\n" +
        "पश्चिम बंगाल सरकार की किसी भी योजना (जैसे लक्ष्मी भंडार, कृषक बंधु, कन्याश्री), छात्रवृत्ति (SVMCM, Oasis), " +
        "ज़रूरी दस्तावेज़ों या इस वेबसाइट पर नागरिक सहायता के लिए मैं तैयार हूँ।\n\n" +
        "👉 आप सीधे नीचे दिए गए बटन दबा सकते हैं या अपना सवाल लिख सकते हैं:"
      );
      actions = [
        { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
        { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
        { label: "🎓 स्टूडेंट क्रेडिट कार्ड", query: "Student Credit Card eligibility aur documents" },
        { label: "🧭 वेबसाइट गाइड", action: "schemes-and-docs" }
      ];
    } else {
      welcomeText = (
        "👋 **Hello! I am 'NayaSetu AI' (ন্যায়সেতু AI).**\n\n" +
        "I am your dedicated digital assistant for West Bengal Government Welfare Schemes, " +
        "Student Scholarships (SVMCM, Oasis, Aikyashree), Mandatory Document Checklists, and Administrative Grievances.\n\n" +
        "👉 You can type in English, Bengali, or Hindi, or choose a quick option below:"
      );
      actions = [
        { label: "🌸 PM Surya Ghar Checklist", query: "What documents are required for PM Surya Ghar?" },
        { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
        { label: "🎓 West Bengal Student Credit Card", query: "WB Student Credit Card eligibility and documents" },
        { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
      ];
    }

    appendMessage('assistant', welcomeText, actions);
  }

  // Event Listeners
  fabBtn.addEventListener('click', () => toggleChat());
  closeBtn.addEventListener('click', () => toggleChat(false));

  clearBtn.addEventListener('click', () => {
    if (confirm('Clear chat history? / চ্যাট ইতিহাস মুছে ফেলবেন?')) {
      messagesBox.innerHTML = '<div class="ns-chat-pill">🔒 West Bengal Government Schemes & Citizen Rights AI Assistant</div>';
      conversationHistory = [];
      try {
        sessionStorage.removeItem('nayasetu_chat_history');
      } catch (e) {}
      showWelcomeMessage();
    }
  });

  apiKeyBtn.addEventListener('click', () => {
    apiDrawer.classList.toggle('open');
  });

  saveApiKeyBtn.addEventListener('click', () => {
    const val = apiKeyInput.value.trim();
    if (val) {
      localStorage.setItem('nayasetu_gemini_api_key', val);
      engineTag.innerHTML = '<span class="material-symbols-outlined" style="font-size:12px; color:#25D366;">verified</span> <span>Gemini LLM</span>';
      apiDrawer.classList.remove('open');
      appendMessage('assistant', "✅ **Gemini AI API Key saved!** Live generative intelligence is now active for all your questions.");
    } else {
      localStorage.removeItem('nayasetu_gemini_api_key');
      engineTag.innerHTML = '<span class="material-symbols-outlined" style="font-size:12px; color:#25D366;">bolt</span> <span>AI Assistant</span>';
      apiDrawer.classList.remove('open');
      appendMessage('assistant', "ℹ️ Gemini API Key cleared. Using built-in NayaSetu smart conversational engine.");
    }
  });

  // Language Bar Button Clicks
  document.querySelectorAll('.ns-lang-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      const l = btn.getAttribute('data-lang');
      if (l && l !== currentLang) setLanguage(l, true);
    });
  });

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage(chatInput.value);
  });

  // Global trigger helper
  window.openNayaSetuChat = function(initialQuery) {
    toggleChat(true);
    if (initialQuery) {
      setTimeout(() => sendMessage(initialQuery), 300);
    }
  };

  console.log('NayaSetu AI WhatsApp Chatbot Widget initialized with multi-lingual support.');
})();