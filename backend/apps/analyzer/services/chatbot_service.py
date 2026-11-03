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
                    {"label": "🌾 PM-KISAN Guide", "type": "query", "text": "PM-KISAN eligibility and benefits"},
                    {"label": "🎓 Student Credit Card", "type": "query", "text": "Student Credit Card eligibility and documents"},
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
                        {"label": "🌾 PM-KISAN Guide", "type": "query", "text": "PM-KISAN eligibility and benefits"},
                        {"label": "🎓 Student Credit Card", "type": "query", "text": "Student Credit Card eligibility and documents"},
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

        # 3.2. Ayushman Bharat PM-JAY & Vay Vandana 70+
        if any(w in q for w in ["ayushman", "pmjay", "আয়ুষ্মান", "ভারত", "आयुष्मान", "वय वंदना", "vay vandana", "70", "senior citizen"]):
            return self._format_scheme_response("ayushman_bharat", lang)

        # 8. Student Credit Card (WBSCC)
        if any(w in q for w in ["student credit card", "wbscc", "क्रेडिट कार्ड", "ক্রেডিট কার্ড", "10 lakh", "loan", "এডুকেশন লোন"]):
            return self._format_scheme_response("wbscc", lang)

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
                    {"label": "🌾 PM-KISAN Guide", "type": "query", "text": "PM-KISAN eligibility and benefits"},
                    {"label": "🎓 Student Credit Card", "type": "query", "text": "Student Credit Card eligibility and documents"},
                    {"label": "⚖️ Check Eligibility", "type": "action", "action": "eligibility-wizard"}
                ]
            }

    def _welcome_message(self, lang: str) -> dict:
        if lang == 'bn':
            return {
                "reply": "নমস্কার! আমি **নয়া সেতু AI**। পশ্চিমবঙ্গ সরকারের যেকোনো প্রকল্প, স্কলারশিপ বা অধিকার সংক্রান্ত সহায়তা পেতে আপনার প্রশ্ন লিখুন।",
                "suggested_actions": [
                    {"label": "☀️ পিএম সূর্য ঘর", "type": "query", "text": "পিএম সূর্য ঘর প্রকল্পে কি কি কাগজ লাগে?"},
                    {"label": "🌾 পিএম কিষাণ", "type": "query", "text": "পিএম কিষাণ সম্মান নিধি প্রকল্পের নিয়ম"},
                    {"label": "🎓 স্টুডেন্ট ক্রেডিট কার্ড", "type": "query", "text": "স্টুডেন্ট ক্রেডিট কার্ড"},
                    {"label": "⚖️ যোগ্যতা যাচাই", "type": "action", "action": "eligibility-wizard"}
                ]
            }
        elif lang == 'hi':
            return {
                "reply": "नमस्ते! मैं **नया सेतु AI** हूँ। पश्चिम बंगाल सरकार की किसी भी योजना, स्कॉलरशिप या वेबसाइट सहायता के लिए अपना प्रश्न पूछें।",
                "suggested_actions": [
                    {"label": "☀️ पीएम सूर्य घर", "type": "query", "text": "पीएम सूर्य घर योजना में क्या-क्या देना पड़ेगा?"},
                    {"label": "🌾 पीएम किसान", "type": "query", "text": "पीएम किसान सम्मान निधि योजना"},
                    {"label": "🎓 स्टूडेंट क्रेडिट कार्ड", "type": "query", "text": "स्टूडेंट क्रेडिट कार्ड योजना"},
                    {"label": "⚖️ योग्यता जाँचें", "type": "action", "action": "eligibility-wizard"}
                ]
            }
        else:
            return {
                "reply": "Hello! I am **NayaSetu AI**. How can I help you today with West Bengal government schemes, scholarships, document checklists, or administrative grievances?",
                "suggested_actions": [
                    {"label": "☀️ PM Surya Ghar", "type": "query", "text": "PM Surya Ghar documents required"},
                    {"label": "🌾 PM-KISAN", "type": "query", "text": "PM-KISAN eligibility"},
                    {"label": "🎓 Student Credit Card", "type": "query", "text": "Student Credit Card"},
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
