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
You are "NayaSetu AI" (नया सेतु AI / ন্যায়সেতু AI) — an intelligent, versatile, compassionate citizen rights and government welfare schemes assistant for the citizens of West Bengal.

CRITICAL IDENTITY RULES:
1. NEVER identify yourself as Google, OpenAI, ChatGPT, or Gemini. Your name is strictly "NayaSetu AI".
2. You assist citizens with West Bengal government schemes, student scholarships, document requirements, grievance letters, and platform navigation.

STRICT LANGUAGE INSTRUCTIONS:
- If user requests or writes in English ("talk in english", "speak in english", etc.), reply entirely in clear, natural English.
- If user requests or writes in Bengali ("বাংলায় বলো", "বাংলায় কথা বলো", etc.), reply entirely in natural, respectful Bengali (বাংলা).
- If user requests or writes in Hindi ("हिंदी में बोलो", "हिंदी में बात करो", etc.), reply in respectful Hindi.

COMPREHENSIVE CAPABILITIES:
- Answer ANY question asked (like ChatGPT): general knowledge, advice, letter writing, calculations, and general conversation.
- For West Bengal schemes (Lakshmir Bhandar, Krishak Bandhu, Kanyashree, Rupashree, SVMCM, Oasis, Aikyashree, Student Credit Card, Swasthya Sathi):
  * Provide exact grant amounts, eligibility rules, and full document checklists (single bank account vs joint, Aadhaar DBT).
  * Always provide the official West Bengal Government portal link (e.g. [Official Portal](url)).
  * Guide users to BDO, SDO, or Duare Sarkar camps.
- Use neat Markdown formatting with bullet points and emojis.
`;

  // Multilingual Knowledge Base for Client-Side Instant Replies
  const KNOWLEDGE_BASE = {
    lakshmir_bhandar: {
      match: ["लक्ष्मी", "lakshmi", "lakshmir", "লক্ষ্মী", "ভাণ্ডার", "লাক্ষ্মীর", "মহিলাদের", "annapurna", "অন্নপূর্ণা", "अन्नपूर्णा", "3000", "women money"],
      en: {
        reply: "🌸 **Annapurna Bhandar / Lakshmir Bhandar (2026 Enhanced):**\n\n💰 **Monthly Benefit**: ₹3,000/month direct DBT bank transfer for all eligible women (₹36,000/year).\n👩 **Eligibility**: Resident women of West Bengal aged 25 to 60 years. Government employees & pension recipients are not eligible.\n\n📑 **Mandatory Document Checklist:**\n• **Swasthya Sathi Card** — Xerox copy (Woman or family card)\n• **Aadhaar Card** — Xerox copy of applicant woman\n• **Single Bank Account Passbook** — Joint accounts are strictly rejected!\n• **Aadhaar-NPCI DBT Active Status** — Must be active in your bank branch\n• **Passport Size Color Photo** — 1 copy\n• **Mobile Number** linked to Aadhaar\n\n🌐 **Official Portal:** [WB Social Security Portal](https://socialsecurity.wb.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps or local BDO / Municipality office.",
        actions: [
          { label: "🌐 Official Portal", url: "https://socialsecurity.wb.gov.in", type: "link" },
          { label: "📋 NayaSetu Checklist", action: "schemes-and-docs" },
          { label: "📝 Draft BDO Letter", action: "grievance-drafter" }
        ]
      },
      bn: {
        reply: "🌸 **অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার — ২০২৬ সংশোধিত নিয়মাবলী:**\n\n💰 **মাসিক অনুদান**: সকল যোগ্য মহিলার জন্য মাসিক ₹৩,০০০ সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি (বাৎসরিক ₹৩৬,০০০)।\n👩 **যোগ্যতা**: পশ্চিমবঙ্গের ২৫ থেকে ৬০ বছর বয়সী স্থায়ী মহিলা বাসিন্দা। সরকারি কর্মী ও পেনশন প্রাপকরা আওতাভুক্ত নন।\n\n📑 **বাধ্যতামূলক নথিপত্রের তালিকা (Documents Checklist):**\n• **স্বাস্থ্য সাথী কার্ড** — জেরক্স কপি (মহিলার নিজের বা পরিবারের)\n• **আধার কার্ড** — আবেদনকারী মহিলার আধার জেরক্স\n• **একক সেভিংস ব্যাঙ্ক পাসবই (Single Account)** — জয়েন্ট অ্যাকাউন্ট সম্পূর্ণ বাতিল হবে\n• **আধার-NPCI DBT লিঙ্ক** — ব্যাঙ্ক অ্যাকাউন্টে ডিবিটি সক্রিয় থাকা বাধ্যতামূলক\n• **পাসপোর্ট সাইজ রঙিন ছবি** — ১ কপি\n• **আধার লিঙ্ক করা মোবাইল নম্বর**\n\n🌐 **অফিসিয়াল সরকারি পোর্টাল:** [Social Security Portal](https://socialsecurity.wb.gov.in)\n📍 **আবেদন স্থল:** দুয়ারে সরকার ক্যাম্প অথবা স্থানীয় বিডিও / পুরসভা অফিস।",
        actions: [
          { label: "🌐 সরকারি পোর্টাল", url: "https://socialsecurity.wb.gov.in", type: "link" },
          { label: "📋 সম্পূর্ণ চেকলিস্ট", action: "schemes-and-docs" },
          { label: "📝 দরখাস্ত ড্রাফটার", action: "grievance-drafter" }
        ]
      },
      hi: {
        reply: "🌸 **अन्नपूर्णा भंडार / लक्ष्मी भंडार — 2026 संशोधित नियम व लाभ:**\n\n💰 **मासिक सहायता**: सभी पात्र महिलाओं हेतु ₹3,000/माह सीधे बैंक खाते में DBT (वार्षिक ₹36,000)।\n👩 **पात्रता**: पश्चिम बंगाल की 25 से 60 वर्ष की महिला नागरिक।\n\n📑 **ज़रूरी दस्तावेज़ (Mandatory Documents):**\n• **स्वास्थ्य साथी कार्ड** — ज़ेरॉक्स कॉपी\n• **आधार कार्ड** — महिला का आधार कार्ड\n• **सिंगल बैंक अकाउंट पासबुक** — केवल महिला के नाम का खाता (जॉइंट खाता मान्य नहीं)\n• **Aadhaar-NPCI DBT Linking** — बैंक खाते में आधार डीबीटी एक्टिव होना अनिवार्य\n• **पासपोर्ट साइज फोटो** व मोबाइल नंबर\n\n🌐 **ऑफिशियल पोर्टल:** [Social Security Portal](https://socialsecurity.wb.gov.in)\n📍 **आवेदन स्थल:** दुयरे सरकार कैंप या स्थानीय BDO / नगर पालिका कार्यालय।",
        actions: [
          { label: "🌐 Official Portal", url: "https://socialsecurity.wb.gov.in", type: "link" },
          { label: "📋 चेकलिस्ट देखें", action: "schemes-and-docs" },
          { label: "📝 BDO शिकायत पत्र बनाएं", action: "grievance-drafter" }
        ]
      }
    },

    wb_yuva_shakti: {
      match: ["yuva", "yuba", "যুব", "শক্তি", "युवा", "shakti", "bharosa", "ভরোসা", "unemployment", "বেকার", "2000", "3000"],
      en: {
        reply: "⚡ **West Bengal Yuva Shakti Yojana (Yuva Shakti Bharosa Card):**\n\n💰 **Monthly Benefit**: ₹2,000/month (Class 10/12 pass) or ₹3,000/month (Graduates) monthly unemployment assistance + free industry skills training.\n🎯 **Eligibility**: Unemployed youth of West Bengal aged 21 to 40 years, passed Class 10/12 or Graduation, enrolled in Employment Bank.\n\n📑 **Required Documents:**\n• Educational qualification marksheets (10th/12th/Graduation)\n• Employment Bank Enrollment ID (Yuvasree ID)\n• Aadhaar Card copy\n• Single Savings Bank Account Passbook with IFSC\n• Active Aadhaar-NPCI DBT linking in bank account\n• Passport size photograph\n\n🌐 **Official Portal:** [Yuva Shakti Portal](https://yubasathi.wb.gov.in)\n📍 **Where to Apply:** Online at yubasathi.wb.gov.in or nearest District Employment Exchange.",
        actions: [
          { label: "🌐 Yuva Shakti Portal", url: "https://yubasathi.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "⚡ **পশ্চিমবঙ্গ যুব শক্তি যোজনা (যুব শক্তি ভরসা কার্ড):**\n\n💰 **আর্থিক ভাতা**: মাধ্যমিক/উচ্চমাধ্যমিক পাশ যুবকদের জন্য মাসিক ₹২,০০০ এবং স্নাতকদের জন্য ₹৩,০০০ বেকার ভাতা + বিনামূল্যে আধুনিক কর্মমুখী প্রশিক্ষণ।\n🎯 **যোগ্যতা**: পশ্চিমবঙ্গের ২১ থেকে ৪০ বছর বয়সী বেকার যুবক-যুবতী, এমপ্লয়মেন্ট ব্যাংকে নথিভুক্ত।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• শিক্ষাগত যোগ্যতার মার্কশিট ও সার্টিফিকেট\n• এমপ্লয়মেন্ট ব্যাঙ্ক রেজিস্ট্রেশন নম্বর\n• আধার কার্ডের জেরক্স\n• নিজস্ব একক সেভিংস ব্যাঙ্ক পাসবই\n• ব্যাঙ্কে আধার-NPCI DBT সক্রিয় থাকার প্রমাণ\n• পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [Yuva Shakti Portal](https://yubasathi.wb.gov.in)\n📍 **কোথায় আবেদন করবেন:** yubasathi.wb.gov.in পোর্টালে অথবা জেলা এমপ্লয়মেন্ট এক্সচেঞ্জে।",
        actions: [
          { label: "🌐 যুব শক্তি পোর্টাল", url: "https://yubasathi.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প নির্দেশিকা", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "⚡ **पश्चिम बंगाल युवा शक्ति योजना (युवा शक्ति भरोसा कार्ड):**\n\n💰 **मासिक सहायता**: 10वीं/12वीं पास को ₹2,000/माह और स्नातकों को ₹3,000/माह बेरोजगारी सहायता व निःशुल्क कौशल विकास।\n🎯 **पात्रता**: प. बंगाल के 21 से 40 वर्ष के बेरोजगार युवा, रोजगार बैंक में पंजीकृत।\n\n📑 **ज़रूरी दस्तावेज़:** 10वीं/12वीं/स्नातक अंकपत्र, एम्प्लॉयमेंट बैंक पंजीकरण आईडी, आधार कार्ड, सिंगल बैंक पासबुक।\n\n🌐 **ऑफिशियल पोर्टल:** [Yuva Shakti Portal](https://yubasathi.wb.gov.in)",
        actions: [
          { label: "🌐 युवा शक्ति पोर्टल", url: "https://yubasathi.wb.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

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

    karmashree: {
      match: ["karmashree", "কর্মশ্রী", "कर्मश्री", "50 day", "৫০ দিন", "50 din", "wage", "কাজ", "job card"],
      en: {
        reply: "🛠️ **Karmashree Scheme (50-Day Guaranteed Wage Employment):**\n\n💰 **Benefit**: 50 days guaranteed wage employment per financial year for rural job card holders at statutory daily wage (₹250+/day).\n👨‍🌾 **Eligibility**: All rural households holding a valid Job Card in West Bengal willing to do unskilled manual work.\n\n📑 **Required Documents:**\n• Rural Job Card (NREGA / State Job Card)\n• Aadhaar Card copy\n• Single Savings Bank Account Passbook\n• Form 4 for work demand\n\n🌐 **Official Portal:** [Karmashree Portal](https://karmashree.wb.gov.in)\n📍 **Where to Apply:** Gram Panchayat Office or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 Karmashree Portal", url: "https://karmashree.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🛠️ **কর্মশ্রী প্রকল্প (৫০ দিনের নিশ্চিত কর্মসংস্থান):**\n\n💰 **সুবিধা**: গ্রামীণ জব কার্ডধারী পরিবারের জন্য বছরে ৫০ দিনের নিশ্চিত কাজ এবং সরাসরি ব্যাঙ্ক অ্যাকাউন্টে নির্ধারিত দৈনিক মজুরি (₹২৫০+/দিন)।\n👨‍🌾 **যোগ্যতা**: জব কার্ডধারী সমস্ত গ্রামীণ পরিবার যারা অদক্ষ কাজ করতে আগ্রহী।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• গ্রামীণ জব কার্ডের জেরক্স\n• আধার কার্ডের কপি\n• একক সেভিংস ব্যাঙ্ক পাসবই\n• কাজের আবেদনের ফর্ম-৪\n\n🌐 **অফিসিয়াল পোর্টাল:** [Karmashree Portal](https://karmashree.wb.gov.in)\n📍 **কোথায় আবেদন করবেন:** গ্রাম পঞ্চায়েত কার্যালয় অথবা দুয়ারে সরকার ক্যাম্প।",
        actions: [
          { label: "🌐 কর্মশ্রী পোর্টাল", url: "https://karmashree.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🛠️ **कर्मश्री योजना (50 दिन की गारंटीड मजदूरी रोजगार):**\n\n💰 **लाभ**: ग्रामीण परिवारों को प्रति वर्ष 50 दिनों का काम और सीधे बैंक खाते में दैनिक मजदूरी।\n👨‍🌾 **पात्रता**: प. बंगाल के सभी ग्रामीण जॉब कार्ड धारक।\n\n📑 **ज़रूरी दस्तावेज़:** जॉब कार्ड, आधार कार्ड, एकल बैंक पासबुक, फॉर्म-4।\n\n🌐 **ऑफिशियल पोर्टल:** [Karmashree Portal](https://karmashree.wb.gov.in)",
        actions: [
          { label: "🌐 कर्मश्री पोर्टल", url: "https://karmashree.wb.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    bhabishyat_credit_card: {
      match: ["bhabishyat", "bccs", "ভবিষ্যৎ", "भविष्य", "business loan", "ব্যবসায় ঋণ"],
      en: {
        reply: "💼 **Bhabishyat Credit Card Scheme (WBBCCS):**\n\n💰 **Facility**: Collateral-free bank loan up to ₹5 Lakh for youth entrepreneurship with 10% government subsidy (max ₹25,000) and 85% state credit guarantee.\n🎯 **Eligibility**: Resident youth aged 18 to 45 years with a viable business or enterprise project in West Bengal.\n\n📑 **Required Documents:**\n• Detailed Project Report (DPR)\n• Aadhaar Card and PAN Card\n• Proof of residence in West Bengal\n• Single Bank Account Passbook / Statement\n• Trade license or proposed business outline\n\n🌐 **Official Portal:** [Bhabishyat Credit Card Portal](https://bccs.wb.gov.in)\n📍 **Where to Apply:** Online at bccs.wb.gov.in or District Industries Centre (DIC) / BDO Office.",
        actions: [
          { label: "🌐 WBBCCS Portal", url: "https://bccs.wb.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "💼 **ভবিষ্যৎ ক্রেডিট কার্ড প্রকল্প (WBBCCS):**\n\n💰 **সুবিধা**: নতুন ব্যবসা বা উদ্যোগের জন্য ৫ লক্ষ টাকা পর্যন্ত সহজ ব্যাঙ্ক ঋণ (১০% সরকারি ভরতুকি ও ৮৫% রাজ্য ক্রেডিট গ্যারান্টি)।\n🎯 **যোগ্যতা**: ১৮ থেকে ৪৫ বছর বয়সী স্থায়ী বাসিন্দা যাদের নতুন ব্যবসার পরিকল্পনা রয়েছে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• প্রকল্পের বিস্তারিত বিবরণ (DPR)\n• আধার কার্ড ও প্যান কার্ড\n• বসবাসের প্রমাণপত্র\n• ব্যাঙ্ক পাসবই বা স্টেটমেন্ট\n\n🌐 **অফিসিয়াল পোর্টাল:** [WBBCCS Portal](https://bccs.wb.gov.in)",
        actions: [
          { label: "🌐 WBBCCS পোর্টাল", url: "https://bccs.wb.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "💼 **भविष्य क्रेडिट कार्ड योजना (WBBCCS):**\n\n💰 **सुविधा**: स्वरोजगार हेतु ₹5 लाख तक का बैंक लोन (10% सरकारी सब्सिडी व राज्य गारंटी)।\n🎯 **पात्रता**: 18 से 45 वर्ष के युवा नागरिक।\n\n📑 **ज़रूरी दस्तावेज़:** डीपीआर (DPR), आधार, पैन, निवास प्रमाण, बैंक पासबुक।\n\n🌐 **ऑफिशियल पोर्टल:** [Bhabishyat Portal](https://bccs.wb.gov.in)",
        actions: [
          { label: "🌐 भविष्य पोर्टल", url: "https://bccs.wb.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    banglar_awas: {
      match: ["awas", "awas yojana", "আবাস", "বাড়ি", "आवास", "makan", "ঘর", "120000"],
      en: {
        reply: "🏡 **Banglar Awas Yojana / Paschim Banga Awas:**\n\n💰 **Financial Grant**: ₹1,20,000 credited directly to bank account in 3 installments (₹60,000 + ₹50,000 + ₹10,000) for pucca house construction.\n👥 **Eligibility**: Rural houseless families or those living in kutcha/dilapidated houses in West Bengal as per official survey list.\n\n📑 **Required Documents:**\n• Aadhaar cards of all family members\n• Digital Ration Card\n• Land ownership document (RoR / Deed / Pradhan certificate)\n• Single Bank Account Passbook with active DBT\n• Photo of existing kutcha house\n\n🌐 **Official Portal:** [P&RD Department Portal](https://wbprd.gov.in)\n📍 **Where to Apply:** Gram Panchayat Office survey or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 P&RD Portal", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🏡 **বাংলার আবাস যোজনা — পাকা বাড়ি তৈরির অনুদান:**\n\n💰 **অনুদান রাশি**: পাকা বাড়ি তৈরির জন্য সরাসরি ব্যাঙ্ক অ্যাকাউন্টে ₹১,২০,০০০ আর্থিক অনুদান ৩টি কিস্তিতে (৬০,০০০ + ৫০,০০০ + ১০,০০০ টাকা)।\n👥 **যোগ্যতা**: গ্রামীণ গৃহহীন ও কাঁচা বাড়িতে বসবাসকারী পরিবার যাদের নাম সমীক্ষা তালিকায় রয়েছে।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পরিবারের সকলের আধার কার্ড\n• ডিজিটাল রেশন কার্ড\n• জমির মালিকানার পরচা বা দলিল\n• একক সেভিংস ব্যাঙ্ক পাসবই\n\n🌐 **অফিসিয়াল পোর্টাল:** [P&RD Portal](https://wbprd.gov.in)",
        actions: [
          { label: "🌐 আবাস পোর্টাল", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏡 **बांगलार आवास योजना (पक्का मकान निर्माण):**\n\n💰 **सहायता**: पक्का मकान बनाने के लिए ₹1,20,000 की वित्तीय सहायता सीधे बैंक खाते में 3 किस्तों में।\n👥 **पात्रता**: ग्रामीण बेघर या कच्चे मकानों में रहने वाले पात्र परिवार।\n\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, राशन कार्ड, जमीन का पर्चा, एकल बैंक पासबुक।\n\n🌐 **ऑफिशियल पोर्टल:** [P&RD Portal](https://wbprd.gov.in)",
        actions: [
          { label: "🌐 आवास पोर्टल", url: "https://wbprd.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    krishak_bandhu: {
      match: ["कृषक", "krishak", "কৃষক", "bandhu", "বন্ধু", "chashi", "চাষী", "किसान", "kisan", "পরচা", "porcha", "farmer"],
      en: {
        reply: "🌾 **Krishak Bandhu (Natun) Scheme:**\n\n💰 **Benefits**: ₹4,000 to ₹10,000 per year (in Kharif and Rabi installments) + ₹2,00,000 Death Benefit for farmers aged 18-60 years.\n👨‍🌾 **Eligibility**: All agricultural landowners, recorded bargadars (sharecroppers), and farmers in West Bengal.\n\n📑 **Mandatory Document Checklist:**\n• **Land Record / RoR / Porcha / Khatian** in farmer's name\n• **Voter ID (EPIC) Card** — Strictly mandatory for Krishak Bandhu\n• **Aadhaar Card** copy\n• **Single Bank Account Passbook** with IFSC code\n• **Passport Size Photograph**\n• **Bargadar Certificate** (for sharecroppers)\n\n🌐 **Official Portal:** [Krishak Bandhu Portal (krishakbandhu.wb.gov.in)](https://krishakbandhu.wb.gov.in)\n📍 **Where to Apply:** Block Assistant Director of Agriculture (ADA) Office or Duare Sarkar Camps.",
        actions: [
          { label: "🌐 Krishak Bandhu Portal", url: "https://krishakbandhu.wb.gov.in", type: "link" },
          { label: "📋 Scheme Details", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🌾 **কৃষক বন্ধু (নতুন) প্রকল্প — নিয়ম ও পরচা তথ্য:**\n\n💰 **আর্থিক সুবিধা**: বছরে ₹৪,০০০ থেকে ₹১০,০০০ অনুদান (খরিফ ও রবি মরশুমে) + ১৮-৬০ বছর বয়সে স্বাভাবিক বা দুর্ঘটনাজনিত মৃত্যুতে ₹২,০০,০০০ ক্ষতিপূরণ।\n👨‍🌾 **যোগ্যতা**: পশ্চিমবঙ্গের সমস্ত কৃষক, জমির মালিক ও নথিভুক্ত বর্গাদার।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• **জমির পরচা / খতিয়ান (Land RoR / Khatian)** — কৃষকের নিজের নামের\n• **ভোটার কার্ড (Voter ID / EPIC)** — কৃষক বন্ধুতে ভোটার কার্ড আবশ্যক\n• **আধার কার্ডের কপি**\n• **একক সেভিংস ব্যাঙ্ক অ্যাকাউন্টের পাসবই**\n• **পাসপোর্ট সাইজ ছবি**\n\n🌐 **অফিসিয়াল পোর্টাল:** [Krishak Bandhu Portal (krishakbandhu.wb.gov.in)](https://krishakbandhu.wb.gov.in)\n📍 **কোথায় আবেদন করবেন:** ব্লক সহ-কৃষি অধিকর্তার (ADA) কার্যালয় অথবা দুয়ারে সরকার ক্যাম্প।",
        actions: [
          { label: "🌐 Krishak Bandhu Portal", url: "https://krishakbandhu.wb.gov.in", type: "link" },
          { label: "📋 চেকলিস্ট দেখুন", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🌾 **कृषक बंधु (नया) योजना / Krishak Bandhu:**\n\n💰 **वित्तीय सहायता**: ₹4,000 से ₹10,000 प्रति वर्ष (दो किस्तों में) + ₹2,00,000 जीवन बीमा सहायता (18-60 वर्ष)।\n👨‍🌾 **पात्रता**: पश्चिम बंगाल के सभी किसान, खेतिहर और दर्ज बटाईदार।\n\n📑 **ज़रूरी दस्तावेज़:**\n• **जमीन का पर्चा / खतियान (Land RoR / Porcha)**\n• **वोटर कार्ड (Voter ID)** — अनिवार्य है\n• **आधार कार्ड व बैंक पासबुक**\n• **पासपोर्ट साइज फोटो**\n\n🌐 **ऑफिशियल पोर्टल:** [Krishak Bandhu (krishakbandhu.wb.gov.in)](https://krishakbandhu.wb.gov.in)\n📍 **आवेदन स्थल:** प्रखंड कृषि कार्यालय (ADA Office) या दुयरे सरकार कैंप।",
        actions: [
          { label: "🌐 Krishak Bandhu Portal", url: "https://krishakbandhu.wb.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
        ]
      }
    },

    svmcm: {
      match: ["svmcm", "swami vivekananda", "bikash bhavan", "বিবেকানন্দ", "বিকাশ ভবন", "स्वामी विवेकानंद", "विकास भवन", "scholarship", "scholarships", "স্কলারশিপ", "स्कॉलरशिप", "বৃত্তি", "college student"],
      en: {
        reply: "🎓 **Swami Vivekananda Merit-cum-Means (SVMCM / Bikash Bhavan) Scholarship:**\n\n💰 **Stipend Amount**: ₹1,000 to ₹5,000 per month depending on degree level (Higher Secondary, UG, PG, Engineering, Medical).\n📚 **Eligibility**: Minimum 60% marks in previous board/university examination, family annual income ≤ ₹2,50,000, resident of West Bengal.\n\n📑 **Required Documents for Upload:**\n• Marksheet of Madhyamik / previous qualifying exam (both sides)\n• Current course Admission Receipt / Fees Slip\n• Family Annual Income Certificate (issued by Joint BDO / BDO / SDO / Executive Officer)\n• Domicile proof (Aadhaar / Voter ID / Ration Card)\n• Student's single bank account passbook (with IFSC and Account number)\n• Passport size photo and signature\n\n🌐 **Official Portal:** [SVMCM Bikash Bhavan Portal (svmcm.wbhed.gov.in)](https://svmcm.wbhed.gov.in)\n📍 **How to Apply:** Apply directly online at svmcm.wbhed.gov.in after taking admission.",
        actions: [
          { label: "🌐 SVMCM Portal", url: "https://svmcm.wbhed.gov.in", type: "link" },
          { label: "⚖️ Check Eligibility", action: "eligibility-wizard" }
        ]
      },
      bn: {
        reply: "🎓 **স্বামী বিবেকানন্দ মেরিট-কাম-মিনস স্কলারশিপ (SVMCM - বিকাশ ভবন):**\n\n💰 **বৃত্তি রাশি**: কোর্স অনুযায়ী প্রতি মাসে ₹১,০০০ থেকে ₹৫,০০০ (উচ্চমাধ্যমিক, স্নাতক, স্নাতকোত্তর, ইঞ্জিনিয়ারিং, মেডিক্যাল)।\n📚 **যোগ্যতা**: পূর্ববর্তী বোর্ড বা কলেজ পরীক্ষায় ন্যূনতম ৬০% নম্বর, পারিবারিক বার্ষিক আয় ₹২,৫০,০০০ টাকার মধ্যে, পশ্চিমবঙ্গের বাসিন্দা।\n\n📑 **আপলোডের জন্য প্রয়োজনীয় নথিপত্র:**\n• মাধ্যমিক বা সর্বশেষ উত্তীর্ণ পরীক্ষার উভয় দিকের মার্কশিট\n• বর্তমান কোর্সে ভর্তির রশিদ (Admission Slip)\n• পারিবারিক বার্ষিক আয়ের সার্টিফিকেট (BDO / SDO নির্গত)\n• বাসস্থানের প্রমাণ (আধার / ভোটার কার্ড)\n• ছাত্র/ছাত্রীর নিজের ব্যাঙ্ক পাসবই\n• পাসপোর্ট সাইজ ছবি ও স্বাক্ষর\n\n🌐 **অফিসিয়াল পোর্টাল:** [SVMCM Portal (svmcm.wbhed.gov.in)](https://svmcm.wbhed.gov.in)\n📍 **আবেদন পদ্ধতি:** কলেজে ভর্তির পর svmcm.wbhed.gov.in-এ অনলাইনে আবেদন করুন।",
        actions: [
          { label: "🌐 SVMCM Official Portal", url: "https://svmcm.wbhed.gov.in", type: "link" },
          { label: "⚖️ নিজের যোগ্যতা যাচাই", action: "eligibility-wizard" }
        ]
      },
      hi: {
        reply: "🎓 **स्वामी विवेकानंद स्कॉलरशिप (SVMCM - विकास भवन स्कॉलरशिप):**\n\n💰 **स्कॉलरशिप राशि**: ₹1,000 से ₹5,000 प्रति माह (HS, ग्रेजुएशन, पोस्ट ग्रेजुएशन, इंजीनियरिंग, मेडिकल)।\n📚 **योग्यता**: पिछली परीक्षा में न्यूनतम 60% अंक, पारिवारिक वार्षिक आय ≤ ₹2,50,000।\n\n📑 **ज़रूरी दस्तावेज़:**\n• पिछली परीक्षा की दोनों तरफ की मार्कशीट\n• वर्तमान कोर्स की प्रवेश रसीद (Admission Receipt)\n• पारिवारिक आय प्रमाण पत्र (BDO / SDO द्वारा जारी)\n• छात्र का अपना बैंक पासबुक व आधार कार्ड\n• फोटो व हस्ताक्षर\n\n🌐 **ऑफिशियल पोर्टल:** [SVMCM Portal (svmcm.wbhed.gov.in)](https://svmcm.wbhed.gov.in)",
        actions: [
          { label: "🌐 SVMCM Portal", url: "https://svmcm.wbhed.gov.in", type: "link" },
          { label: "⚖️ योग्यता चेक करें", action: "eligibility-wizard" }
        ]
      }
    },

    kanyashree: {
      match: ["कन्याश्री", "kanya", "kanyashree", "কন্যাশ্রী", "k1", "k2", "k3"],
      en: {
        reply: "👧 **Kanyashree Prakalpa (Girls Education & Welfare):**\n\n💰 **Benefits**: K1: ₹1,000 annual scholarship (Class 8-12, age 13-18) | K2: ₹25,000 one-time grant upon turning 18 | K3: ₹2,000-₹2,500/month for PG higher studies.\n🎯 **Eligibility**: Unmarried female students studying in recognized institutions in West Bengal.\n\n📑 **Mandatory Documents:**\n• Birth Certificate or Madhyamik Admit Card (Age proof)\n• Unmarried Declaration Form\n• Institutional Bonafide Certificate / School enrollment receipt\n• Student's single bank account passbook\n• Aadhaar card and passport photo\n\n🌐 **Official Portal:** [Kanyashree Portal (wbkanyashree.gov.in)](https://www.wbkanyashree.gov.in)\n📍 **Where to Apply:** Through the school, madrasah, or college where the student is studying.",
        actions: [
          { label: "🌐 Kanyashree Portal", url: "https://www.wbkanyashree.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "👧 **কন্যাশ্রী প্রকল্প — নিয়মাবলী ও সুবিধা:**\n\n💰 **অনুদান**: K1: বার্ষিক ₹১,০০০ স্কলারশিপ (৮ম-১২শ শ্রেণী, ১৩-১৮ বছর) | K2: ১৮ বছর পূর্ণ হলে এককালীন ₹২৫,০০০ অনুদান | K3: স্নাতকোত্তর ও উচ্চশিক্ষায় মাসিক ₹২,০০০-₹২,৫০০।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• জন্ম শংসাপত্র বা মাধ্যমিক এডমিট কার্ড\n• অভিভাবক কর্তৃক অবিবাহিতা ঘোষণার পত্র\n• স্কুল বা কলেজের বোনাফাইড শংসাপত্র\n• ছাত্রীর নিজস্ব একক ব্যাঙ্ক পাসবই\n• আধার কার্ড এবং পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [Kanyashree Portal (wbkanyashree.gov.in)](https://www.wbkanyashree.gov.in)\n📍 **আবেদন:** ছাত্রী যে স্কুল বা কলেজে পড়ছে তার মাধ্যমে সরাসরি আবেদন।",
        actions: [
          { label: "🌐 Kanyashree Portal", url: "https://www.wbkanyashree.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "👧 **कन्याश्री प्रकल्प (Kanyashree Prakalpa):**\n\n💰 **लाभ**: K1: ₹1,000 वार्षिक छात्रवृत्ति (13-18 वर्ष) | K2: ₹25,000 एकमुश्त (18 वर्ष पर) | K3: ₹2,000-₹2,500/माह पीजी अध्ययन।\n\n📑 **ज़रूरी दस्तावेज़:**\n• जन्म प्रमाण पत्र / एडमिट कार्ड\n• अविवाहित घोषणा पत्र\n• स्कूल/कॉलेज संस्थागत प्रमाण पत्र\n• छात्रा का एकल बैंक पासबुक व आधार कार्ड\n\n🌐 **ऑफिशियल पोर्टल:** [Kanyashree Portal (wbkanyashree.gov.in)](https://www.wbkanyashree.gov.in)",
        actions: [
          { label: "🌐 Kanyashree Portal", url: "https://www.wbkanyashree.gov.in", type: "link" },
          { label: "📋 योजना सूची", action: "schemes-and-docs" }
        ]
      }
    },

    rupashree: {
      match: ["रूपश्री", "rupashree", "রূপশ্রী", "शादी", "विवाह", "biye", "marriage", "বিয়ে", "wedding"],
      en: {
        reply: "💍 **Rupashree Prakalpa (₹25,000 One-Time Marriage Grant):**\n\n💰 **Benefit**: ₹25,000 one-time financial assistance credited directly to bride's account before marriage.\n👰 **Eligibility**: Bride aged 18+ years, groom aged 21+ years, family annual income ≤ ₹1.5 Lakh, resident of West Bengal.\n\n📑 **Required Documents:**\n• Age proof of both bride and groom (Aadhaar / Birth Certificate / Madhyamik Admit)\n• Proof of marriage (Wedding invitation card or legal notice)\n• Family Annual Income Certificate (BDO / SDO / Councilor / Pradhan)\n• Bride's single savings bank account passbook\n• Passport photos of both bride and groom\n\n🌐 **Official Portal:** [Rupashree Portal (wbrupashree.gov.in)](https://wbrupashree.gov.in)\n📍 **Where to Apply:** Local BDO or Municipality office at least 30 to 60 days before the wedding date.",
        actions: [
          { label: "🌐 Rupashree Portal", url: "https://wbrupashree.gov.in", type: "link" },
          { label: "📋 View Checklist", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "💍 **রূপশ্রী প্রকল্প (বিয়ের এককালীন ₹২৫,০০০ অনুদান):**\n\n💰 **অনুদান**: বিয়ের আগে পাত্রীর ব্যাঙ্ক অ্যাকাউন্টে সরাসরি ₹২৫,০০০ এককালীন সাহায্য।\n👰 **যোগ্যতা**: পাত্রীর বয়স ১৮+ বছর, পাত্রের ২১+ বছর, পারিবারিক বার্ষিক আয় ১.৫ লক্ষ টাকার মধ্যে, পশ্চিমবঙ্গের বাসিন্দা।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পাত্র ও পাত্রী উভয়ের বয়সের প্রমাণ (আধার / জন্ম সার্টিফিকেট)\n• বিয়ের প্রমাণ (বিয়ের নিমন্ত্রণপত্র বা নোটিশ)\n• পারিবারিক আয়ের সার্টিফিকেট (BDO / SDO নির্গত)\n• পাত্রীর নিজস্ব একক ব্যাঙ্ক পাসবই\n• উভয়ের পাসপোর্ট সাইজ ছবি\n\n🌐 **অফিসিয়াল পোর্টাল:** [Rupashree Portal (wbrupashree.gov.in)](https://wbrupashree.gov.in)\n📍 **কোথায় আবেদন করবেন:** বিয়ের অন্তত ৩০-৬০ দিন আগে স্থানীয় বিডিও অফিস বা পুরসভায়।",
        actions: [
          { label: "🌐 Rupashree Portal", url: "https://wbrupashree.gov.in", type: "link" },
          { label: "📋 চেকলিস্ট দেখুন", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "💍 **रूपश्री प्रकल्प (Rupashree Prakalpa) — ₹25,000 शादी अनुदान:**\n\n💰 **लाभ**: शादी से पहले सीधे बैंक खाते में ₹25,000 की एकमुश्त सहायता।\n👰 **पात्रता**: कन्या की आयु 18+ वर्ष, वर की आयु 21+ वर्ष, वार्षिक पारिवारिक आय ≤ ₹1.5 लाख।\n\n📑 **ज़रूरी दस्तावेज़:** दोनों का आयु प्रमाण, शादी का कार्ड/नोटिस, आय प्रमाण पत्र, कन्या का बैंक पासबुक।\n\n🌐 **ऑफिशियल पोर्टल:** [Rupashree Portal (wbrupashree.gov.in)](https://wbrupashree.gov.in)",
        actions: [
          { label: "🌐 Rupashree Portal", url: "https://wbrupashree.gov.in", type: "link" },
          { label: "📋 चेकलिस्ट देखें", action: "schemes-and-docs" }
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

    swasthya_sathi: {
      match: ["swasthya sathi", "স্বাস্থ্য সাথী", "स्वास्थ्य साथी", "health card", "5 lakh", "chikitsa", "ilaj", "hospital"],
      en: {
        reply: "🏥 **Swasthya Sathi (₹5 Lakh Cashless Health Cover):**\n\n💰 **Benefit**: Cashless treatment up to ₹5,00,000 per family per year across empaneled public & private hospitals.\n👥 **Eligibility**: All families resident in West Bengal. Smart card is issued in the name of the eldest female member of the family.\n\n📑 **Required Documents:**\n• Aadhaar cards of all family members to be enrolled\n• Digital Ration Card / Khadya Sathi card\n• Passport size photo of the female head of family\n• Form B filled and submitted at camp\n\n🌐 **Official Portal:** [Swasthya Sathi Portal (swasthyasathi.gov.in)](https://swasthyasathi.gov.in)\n📍 **Where to Apply:** Duare Sarkar Camps or local BDO / Municipality office.",
        actions: [
          { label: "🌐 Swasthya Sathi Portal", url: "https://swasthyasathi.gov.in", type: "link" },
          { label: "📋 Schemes Directory", action: "schemes-and-docs" }
        ]
      },
      bn: {
        reply: "🏥 **স্বাস্থ্য সাথী প্রকল্প (৫ লক্ষ টাকা ক্যাশলেস স্বাস্থ্য বীমা):**\n\n💰 **সুবিধা**: প্রতি পরিবার প্রতি বছর সর্বোচ্চ ₹৫,০০,০০০ (পাঁচ লক্ষ) টাকা পর্যন্ত ক্যাশলেস চিকিৎসা পরিষেবা।\n👥 **যোগ্যতা**: পশ্চিমবঙ্গের সমস্ত নাগরিক পরিবার। স্মার্ট কার্ড পরিবারের জ্যেষ্ঠ মহিলার নামে ইস্যু হয়।\n\n📑 **প্রয়োজনীয় নথিপত্র:**\n• পরিবারের সকল সদস্যের আধার কার্ড\n• ডিজিটাল রেশন কার্ড / খাদ্য সাথী কার্ড\n• পরিবারের প্রধান মহিলার পাসপোর্ট সাইজ ছবি\n• ফর্ম-বি (দুয়ারে সরকার ক্যাম্প থেকে সংগৃহীত)\n\n🌐 **অফিসিয়াল পোর্টাল:** [Swasthya Sathi Portal (swasthyasathi.gov.in)](https://swasthyasathi.gov.in)",
        actions: [
          { label: "🌐 Swasthya Sathi Portal", url: "https://swasthyasathi.gov.in", type: "link" },
          { label: "📋 প্রকল্প বিবরণ", action: "schemes-and-docs" }
        ]
      },
      hi: {
        reply: "🏥 **स्वास्थ्य साथी (Swasthya Sathi):**\n\n💰 **सुविधा**: प्रति परिवार प्रति वर्ष ₹5,00,000 तक कैशलेस अस्पताल इलाज सुविधा।\n👥 **पात्रता**: प. बंगाल के सभी परिवार। स्मार्ट कार्ड परिवार की वरिष्ठ महिला के नाम जारी होता है।\n\n📑 **ज़रूरी दस्तावेज़:** आधार कार्ड, डिजिटल राशन कार्ड, महिला मुखिया की फोटो।\n\n🌐 **ऑफिशियल पोर्टल:** [Swasthya Sathi Portal (swasthyasathi.gov.in)](https://swasthyasathi.gov.in)",
        actions: [
          { label: "🌐 Swasthya Sathi Portal", url: "https://swasthyasathi.gov.in", type: "link" },
          { label: "📋 योजना विवरण", action: "schemes-and-docs" }
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
      { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
      { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
      { label: "🎓 SVMCM Scholarship", query: "SVMCM scholarship eligibility and documents" },
      { label: "💳 Student Credit Card", query: "West Bengal Student Credit Card loan rules" },
      { label: "📝 How to Complain", query: "How to draft a grievance letter to BDO?" },
      { label: "🧭 Website Guide", query: "How to navigate and use NayaSetu website?" }
    ],
    bn: [
      { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
      { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
      { label: "🎓 SVMCM স্কলারশিপ", query: "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?" },
      { label: "💳 স্টুডেন্ট ক্রেডিট কার্ড", query: "স্টুডেন্ট ক্রেডিট কার্ড প্রকল্পের নিয়মাবলী" },
      { label: "📝 অভিযোগ কোথায় দেব?", query: "বিডিও অফিসে কীভাবে অভিযোগ বা দরখাস্ত জমা দেব?" },
      { label: "🧭 ওয়েবসাইট নির্দেশিকা", query: "নয়া সেতু ওয়েবসাইটে কোথায় কি করতে হবে?" }
    ],
    hi: [
      { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
      { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
      { label: "🎓 SVMCM स्कॉलरशिप", query: "SVMCM scholarship eligibility aur documents" },
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
          actionsHtml += `<a href="${act.url}" target="_blank" rel="noopener noreferrer" class="ns-chat-action-btn"><span class="material-symbols-outlined" style="font-size:13px;">open_in_new</span> ${act.label}</a>`;
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
          { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
          { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
          { label: "🎓 SVMCM Scholarship", query: "SVMCM scholarship eligibility and documents" },
          { label: "🧭 Website Guide", action: "schemes-and-docs" }
        ]);
      } else if (lang === 'bn') {
        appendMessage('assistant', "🙏 **ভাষা পরিবর্তন করা হয়েছে: বাংলা।** পশ্চিমবঙ্গ সরকারের জনকল্যাণমূলক প্রকল্প, স্কলারশিপ বা অধিকার সংক্রান্ত কী তথ্য জানতে চান?", [
          { label: "🌸 লক্ষ্মীর ভাণ্ডার ডকুমেন্টস", query: "লক্ষ্মীর ভাণ্ডার প্রকল্পে কি কি কাগজ লাগে?" },
          { label: "🌾 কৃষক বন্ধু পরচা নিয়ম", query: "কৃষক বন্ধু প্রকল্পের নিয়ম ও অনুদান" },
          { label: "🎓 SVMCM স্কলারশিপ", query: "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?" },
          { label: "⚖️ যোগ্যতা যাচাই", action: "eligibility-wizard" }
        ]);
      } else if (lang === 'hi') {
        appendMessage('assistant', "🙏 **भाषा बदल दी गई है: हिंदी।** पश्चिम बंगाल सरकार की किसी भी योजना, स्कॉलरशिप या नया सेतु वेबसाइट सहायता के लिए अपना प्रश्न पूछें।", [
          { label: "🌸 लक्ष्मी भंडार दस्तावेज़", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
          { label: "🌾 कृषक बंधु योजना", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
          { label: "🎓 SVMCM स्कॉलरशिप", query: "SVMCM scholarship eligibility aur documents" },
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

  // Client-Side Conversational Intelligence Fallback
  function getClientFallbackReply(userText) {
    const q = userText.toLowerCase();

    // 1. Identity & Name
    if (q.includes("who are you") || q.includes("what is your name") || q.includes("your name") || q.includes("তোমার নাম") || q.includes("তোমার পরিচয়") || q.includes("तुम्हारा नाम") || q.includes("कौन हो")) {
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
            { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
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
            { label: "🎓 SVMCM স্কলারশিপ", query: "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?" }
          ]
        };
      } else if (currentLang === 'hi') {
        return {
          reply: "🙏 **नमस्ते! मैं नया सेतु AI हूँ।**\n\nपश्चिम बंगाल सरकार की योजनाओं, छात्रवृत्तियों या आवश्यक दस्तावेज़ों के बारे में आप क्या जानना चाहते हैं?",
          actions: [
            { label: "🌸 लक्ष्मी भंडार", query: "लक्ष्मी भंडार में क्या-क्या देना पड़ेगा?" },
            { label: "🌾 कृषक बंधु", query: "कृषक बंधु योजना के लिए क्या डॉक्यूमेंट्स चाहिए?" },
            { label: "🎓 SVMCM स्कॉलरशिप", query: "SVMCM scholarship eligibility aur documents" }
          ]
        };
      } else {
        return {
          reply: "👋 **Hello! I am NayaSetu AI.**\n\nHow can I help you today with West Bengal government schemes, scholarships, document checklists, or administrative grievances?",
          actions: [
            { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
            { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
            { label: "🎓 SVMCM Scholarship", query: "SVMCM scholarship eligibility and documents" }
          ]
        };
      }
    }

    // 3. Match against structured knowledge base
    for (let key in KNOWLEDGE_BASE) {
      const item = KNOWLEDGE_BASE[key];
      if (item.match && item.match.some(m => q.includes(m.toLowerCase()))) {
        const localized = item[currentLang] || item.en;
        return {
          reply: localized.reply,
          actions: localized.actions || []
        };
      }
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
          { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
          { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
          { label: "🎓 SVMCM Scholarship", query: "SVMCM scholarship eligibility and documents" },
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
        { label: "🎓 SVMCM স্কলারশিপ", query: "SVMCM স্কলারশিপের জন্য কি কি ডকুমেন্টস লাগে?" },
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
        { label: "🎓 SVMCM स्कॉलरशिप", query: "SVMCM scholarship eligibility aur documents" },
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
        { label: "🌸 Lakshmir Bhandar Checklist", query: "What documents are required for Lakshmir Bhandar?" },
        { label: "🌾 Krishak Bandhu Guide", query: "Krishak Bandhu eligibility and benefits" },
        { label: "🎓 SVMCM Scholarship", query: "SVMCM scholarship eligibility and documents" },
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