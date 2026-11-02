"""
Gemini AI Service for analyzing West Bengal Government notices, SMS, and rejection slips.
Translates bureaucratic jargon into simple Bengali, English, and Hindi with step-by-step remedies.
Now upgraded with Annapurna Bhandar (অন্নপূর্ণা ভাণ্ডার / अन्नपूर्णा भंडार), active language adaptation,
and intelligent compassionate handling for unexpected/random ('उल्टा सीधा') messages.
"""
import os
import json
import logging
from django.conf import settings
from PIL import Image
import io

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are NyayaSetu AI (नया सेतु AI / ন্যায়সেতু AI), an expert citizen rights and welfare scheme navigation assistant for the citizens of West Bengal.
Your task is to analyze West Bengal government scheme application receipts, SMS notifications, rejection slips, or citizen queries.

FOLLOW THESE STRICT GUIDELINES:

1. Identify the likely scheme:
   - Annapurna Bhandar (অন্নপূর্ণা ভাণ্ডার / अन्नपूर्णा भंडार - formerly known as Lakshmir Bhandar)
   - Krishak Bandhu (কৃষক বন্ধু)
   - Kanyashree (কন্যাশ্রী)
   - Aikyashree / Oasis / SVMCM (স্কলারশিপ)
   - Jai Johar / Taposhili Bandhu (পেনশন)
   - Swasthya Sathi (স্বাস্থ্য সাথী)
   - Khadya Sathi / Ration Card (খাদ্য সাথী)
   - Yuvasree / Yuva Shakti (যুবশ্রী)
   - Rupashree (রূপশ্রী)
   - Or "সাধারণ অনুসন্ধান / General Inquiry" if not a specific scheme.

2. Determine the status category:
   - "Action Required / On Hold" (applicant needs to fix something)
   - "Defective / Mismatch" (document/data error like name or bank mismatch)
   - "Under Process / Review" (application received and pending clerical check)
   - "Rejected" (formally rejected)
   - "Guidance / সাধারণ সহায়তা" (for general, casual, or unclassified messages)

3. LANGUAGE ADAPTATION:
   The user prompt will specify their preferred language (e.g. "Language: bn" for Bengali, "Language: hi" for Hindi, or "Language: en" for English).
   - "status_summary": Provide the primary explanation in the user's PREFERRED language in warm, simple, non-bureaucratic words.
   - Also provide "status_summary_bn" (বাংলা), "status_summary_hi" (हिंदी), and "status_summary_en" (English).
   - In "action_steps", each step's "action" must be written in the user's PREFERRED language, with "action_bn", "action_hi", "action_en" provided.

4. SPECIAL HANDLING FOR UNRELATED, CASUAL, OR GIBBERISH INPUTS ("उल्टा सीधा संदेश"):
   If the input text or image does NOT contain a recognized West Bengal Government notice, receipt, or SMS (e.g. random letters like 'asdfgh', jokes, casual chit-chat, cooking recipes, or unrelated text):
   - DO NOT throw an error or refuse to reply.
   - Set "detected_scheme": "সাধারণ অনুসন্ধান / General Inquiry" (or localized equivalent).
   - Set "status_category": "Guidance / সাধারণ সহায়তা".
   - Set "status_summary": Compassionately explain that the provided message does not match a recognized West Bengal government scheme SMS or notice (such as Annapurna Bhandar, Krishak Bandhu, Swasthya Sathi, etc.). Advise the citizen on how to verify real SMS notices or check status at the nearest BDO office or Duare Sarkar camp.
   - Set "action_steps":
     1. Check your mobile inbox for SMS from official West Bengal Government sender IDs (e.g. WBGOVT, WBLKBH, DGSGVT).
     2. Visit your local Gram Panchayat / BDO Office or Bangla Sahayata Kendra (BSK) with your application slip.
     3. You can also ask NayaSetu Sahayak AI right here on this website for scheme eligibility.
   - Set "required_documents_to_carry": ["Aadhaar Card", "Mobile Phone with Registered SIM", "Application Acknowledgment Slip"].

5. Provide concrete, actionable next steps for real notices:
   - Exact office to visit: Home bank branch, BDO office, Gram Panchayat, Duare Sarkar counter, BL&LRO office.
   - Exact document or mandate form needed: e.g. Single Bank Passbook, Aadhaar NPCI Seeding Mandate Form, Certified RoR/Porcha.

6. CRITICAL ETHICS DISCLAIMER:
   "NyayaSetu AI is an independent citizen helper and not an official government authority. It does not decide eligibility or guarantee approvals."

Output STRICTLY valid JSON matching this schema:
{
  "detected_scheme": "Annapurna Bhandar (অন্নপূর্ণা ভাণ্ডার)",
  "status_category": "Action Required / On Hold",
  "status_summary": "Explanation in user's preferred language",
  "status_summary_bn": "বাংলায় সহজ ও স্পষ্ট ব্যাখ্যা",
  "status_summary_hi": "हिंदी में सरल व स्पष्ट व्याख्या",
  "status_summary_en": "Simple explanation in English",
  "root_cause_identified": "e.g. Bank account not NPCI/Aadhaar DBT mapped",
  "action_steps": [
    {
      "step_number": 1,
      "action": "Step description in user's preferred language",
      "action_bn": "আপনার মূল ব্যাংক শাখায় যান...",
      "action_hi": "अपने मूल बैंक शाखा में जाएँ...",
      "action_en": "Visit your home bank branch...",
      "office": "Home Bank Branch / BDO Office"
    }
  ],
  "required_documents_to_carry": [
    "Aadhaar Card", "Bank Passbook"
  ],
  "disclaimer": "NyayaSetu AI is an independent citizen assistance guide and not a government authority."
}
"""


class GeminiAnalyzerService:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

    def analyze_text(self, notice_text: str, lang: str = 'bn') -> dict:
        """Analyze pasted text from SMS or status portal with language preference"""
        if lang not in ['bn', 'hi', 'en']:
            lang = 'bn'

        if not self.api_key:
            return self._mock_analysis(notice_text, lang=lang)

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            lang_instruction = {
                'bn': 'Bengali (বাংলা)',
                'hi': 'Hindi (हिंदी)',
                'en': 'English'
            }.get(lang, 'Bengali (বাংলা)')

            prompt = (
                f"Selected Citizen Language: {lang_instruction} ({lang}).\n"
                f"Analyze this West Bengal government application status or notice text:\n\n"
                f"\"\"\"\n{notice_text}\n\"\"\"\n\n"
                f"Remember: If this message is random, casual, or not a recognized scheme notice ('उल्टा सीधा संदेश'), "
                f"handle it gracefully with helpful guidance in {lang_instruction}."
            )

            # Try primary model gemini-2.5-flash, fallback to gemini-2.0-flash if needed
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
            except Exception as m_err:
                logger.warning(f"gemini-2.5-flash text failed ({m_err}), falling back to gemini-2.0-flash")
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )

            data = json.loads(response.text)
            return self._ensure_fields(data, lang)
        except Exception as e:
            logger.error(f"Gemini API text analysis error: {e}")
            return self._mock_analysis(notice_text, lang=lang, fallback_error=str(e))

    def analyze_image(self, image_file, lang: str = 'bn') -> dict:
        """Analyze an uploaded screenshot or photo of an application receipt / letter with language preference"""
        if lang not in ['bn', 'hi', 'en']:
            lang = 'bn'

        if not self.api_key:
            return self._mock_analysis("Uploaded Image Document", lang=lang)

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            pil_image = Image.open(image_file)
            
            lang_instruction = {
                'bn': 'Bengali (বাংলা)',
                'hi': 'Hindi (हिंदी)',
                'en': 'English'
            }.get(lang, 'Bengali (বাংলা)')

            prompt = (
                f"Selected Citizen Language: {lang_instruction} ({lang}).\n"
                f"Extract and analyze the text from this West Bengal scheme document, notice, application receipt, or SMS screenshot.\n"
                f"Remember: If this image is unclear, unrelated, or not an official scheme notice, "
                f"provide polite and helpful guidance in {lang_instruction} without crashing."
            )

            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[pil_image, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
            except Exception as m_err:
                logger.warning(f"gemini-2.5-flash image failed ({m_err}), falling back to gemini-2.0-flash")
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[pil_image, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )

            data = json.loads(response.text)
            return self._ensure_fields(data, lang)
        except Exception as e:
            logger.error(f"Gemini API image analysis error: {e}")
            return self._mock_analysis("Uploaded Image", lang=lang, fallback_error=str(e))

    def _ensure_fields(self, data: dict, lang: str) -> dict:
        """Ensure all required fields exist and status_summary matches user's preferred language"""
        if lang == 'en' and data.get("status_summary_en"):
            data["status_summary"] = data["status_summary_en"]
        elif lang == 'hi' and data.get("status_summary_hi"):
            data["status_summary"] = data["status_summary_hi"]
        elif lang == 'bn' and data.get("status_summary_bn"):
            data["status_summary"] = data["status_summary_bn"]
        elif not data.get("status_summary"):
            data["status_summary"] = data.get("status_summary_en") or data.get("status_summary_bn") or ""

        # Ensure action steps have localized action field
        if "action_steps" in data and isinstance(data["action_steps"], list):
            for step in data["action_steps"]:
                if lang == 'en' and step.get("action_en"):
                    step["action"] = step["action_en"]
                elif lang == 'hi' and step.get("action_hi"):
                    step["action"] = step["action_hi"]
                elif lang == 'bn' and step.get("action_bn"):
                    step["action"] = step["action_bn"]
                elif not step.get("action"):
                    step["action"] = step.get("action_en") or step.get("action_bn") or ""
        return data

    def _mock_analysis(self, raw_input: str, lang: str = 'bn', fallback_error: str = None) -> dict:
        """
        Failsafe response when API key is not configured or on network fallback.
        Includes full multilingual responses for Annapurna Bhandar, Krishak Bandhu,
        Swasthya Sathi, Scholarships, and intelligent handling of gibberish/unrelated inputs.
        """
        lower = raw_input.lower().strip()

        # 1. Annapurna Bhandar / NPCI / DBT / Bank Account error
        if any(k in lower for k in ["npci", "dbt", "annapurna", "annapurna bhandar", "lakshmi", "lakshmir", "bhandar", "lkbhd", "bank validation", "account error"]):
            if lang == 'hi':
                return {
                    "detected_scheme": "अन्नपूर्णा भंडार (Annapurna Bhandar / DBT Scheme)",
                    "status_category": "Action Required / On Hold",
                    "status_summary": "आपका आवेदन खारिज नहीं हुआ है, बल्कि रुका हुआ है। इसका मुख्य कारण आपके बैंक खाते में आधार डीबीटी (NPCI) लिंक न होना या बैंक खाते में त्रुटि होना है।",
                    "status_summary_bn": "আপনার আবেদনটি বাতিল হয়নি, সাময়িক স্থগিত আছে। কারণ আপনার ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) লিঙ্ক নেই অথবা অ্যাকাউন্টে ভুল রয়েছে।",
                    "status_summary_hi": "आपका आवेदन खारिज नहीं हुआ है, बल्कि रुका हुआ है। इसका मुख्य कारण आपके बैंक खाते में आधार डीबीटी (NPCI) लिंक न होना या बैंक खाते में त्रुटि होना है।",
                    "status_summary_en": "Your application is on hold because your bank account is not mapped for Aadhaar Direct Benefit Transfer (DBT/NPCI) or has a banking validation error.",
                    "root_cause_identified": "बैंक खाते में आधार NPCI DBT मैपिंग सक्रिय न होना (Inactive NPCI Seeding)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "अपने मूल बैंक शाखा में जाएँ जहाँ आपका सिंगल खाता है (CSP केंद्र पर न जाएँ)।",
                            "action_bn": "আপনার মূল ব্যাংক শাখায় যান যেখানে আপনার নিজস্ব একক অ্যাকাউন্ট রয়েছে।",
                            "action_hi": "अपने मूल बैंक शाखा में जाएँ जहाँ आपका सिंगल खाता है (CSP केंद्र पर न जाएँ)।",
                            "action_en": "Visit your home bank branch where your single savings account exists.",
                            "office": "Home Bank Branch"
                        },
                        {
                            "step_number": 2,
                            "action": "बैंक से 'Aadhaar NPCI DBT Seeding Mandate Form' लें, भरें और आधार की फोटोकॉपी जमा करें।",
                            "action_bn": "ব্যাংক থেকে 'আধার এনপিসিআই ডিবিটি ফরম' নিয়ে পূরণ করুন এবং আধারের জেরক্স জমা দিন।",
                            "action_hi": "बैंक से 'Aadhaar NPCI DBT Seeding Mandate Form' लें, भरें और आधार की फोटोकॉपी जमा करें।",
                            "action_en": "Submit the Aadhaar NPCI DBT Mandate form along with Aadhaar photocopy at the counter.",
                            "office": "Bank Branch Counter"
                        },
                        {
                            "step_number": 3,
                            "action": "मुहर लगी रसीद लेकर निकटतम BDO कार्यालय या दुआरे सरकार कैंप में स्थिति अपडेट करवाएँ।",
                            "action_bn": "সিলমোহরকৃত রসিদ নিয়ে বিডিও অফিস বা দুয়ারে সরকার ডেস্কে স্ট্যাটাস আপডেট করান।",
                            "action_hi": "मुहर लगी रसीद लेकर निकटतम BDO कार्यालय या दुआरे सरकार कैंप में स्थिति अपडेट करवाएँ।",
                            "action_en": "Take the stamped acknowledgment to your BDO office or Duare Sarkar helpdesk to resume processing.",
                            "office": "BDO Office / Duare Sarkar Desk"
                        }
                    ],
                    "required_documents_to_carry": [
                        "आधार कार्ड (मूल व फोटोकॉपी)",
                        "बैंक पासबुक (सिंगल अकाउंट, IFSC युक्त)",
                        "आवेदन पावती रसीद (Beneficiary ID Slip)"
                    ],
                    "disclaimer": "न्यायसेतु AI एक स्वतंत्र नागरिक सहायता गाइड है, सरकारी प्राधिकारी नहीं।"
                }
            elif lang == 'en':
                return {
                    "detected_scheme": "Annapurna Bhandar (DBT Social Welfare Scheme)",
                    "status_category": "Action Required / On Hold",
                    "status_summary": "Your application is currently paused and NOT rejected. The issue is that your bank account lacks active Aadhaar Direct Benefit Transfer (DBT/NPCI) mapping.",
                    "status_summary_bn": "আপনার আবেদনটি বাতিল হয়নি, সাময়িক স্থগিত আছে। কারণ আপনার ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) লিঙ্ক নেই অথবা অ্যাকাউন্টে ভুল রয়েছে।",
                    "status_summary_hi": "आपका आवेदन खारिज नहीं हुआ है, बल्कि रुका हुआ है। इसका मुख्य कारण बैंक खाते में आधार डीबीटी (NPCI) लिंक न होना है।",
                    "status_summary_en": "Your application is currently paused and NOT rejected. The issue is that your bank account lacks active Aadhaar Direct Benefit Transfer (DBT/NPCI) mapping.",
                    "root_cause_identified": "NPCI Aadhaar DBT Mapping Inactive / Bank Validation Failure",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "Visit your home bank branch where your single-operated savings account is located.",
                            "action_bn": "আপনার মূল ব্যাংক শাখায় যান যেখানে আপনার নিজস্ব একক অ্যাকাউন্ট রয়েছে।",
                            "action_hi": "अपने मूल बैंक शाखा में जाएँ जहाँ आपका सिंगल खाता है।",
                            "action_en": "Visit your home bank branch where your single-operated savings account is located.",
                            "office": "Home Bank Branch"
                        },
                        {
                            "step_number": 2,
                            "action": "Request the 'Aadhaar NPCI DBT Seeding Mandate Form', submit it with an Aadhaar copy, and get a stamped receipt.",
                            "action_bn": "ব্যাংক থেকে 'আধার এনপিসিআই ডিবিটি ফরম' নিয়ে পূরণ করুন এবং আধারের জেরক্স জমা দিন।",
                            "action_hi": "बैंक से 'Aadhaar NPCI DBT Seeding Mandate Form' लें और आधार कॉपी जमा करें।",
                            "action_en": "Request the 'Aadhaar NPCI DBT Seeding Mandate Form', submit it with an Aadhaar copy, and get a stamped receipt.",
                            "office": "Bank Branch Counter"
                        },
                        {
                            "step_number": 3,
                            "action": "Submit the stamped bank receipt to your BDO social welfare desk or Duare Sarkar camp.",
                            "action_bn": "সিলমোহরকৃত রসিদ নিয়ে বিডিও অফিস বা দুয়ারে সরকার ডেস্কে স্ট্যাটাস আপডেট করান।",
                            "action_hi": "मुहर लगी रसीद लेकर BDO कार्यालय या दुआरे सरकार कैंप में जमा करें।",
                            "action_en": "Submit the stamped bank receipt to your BDO social welfare desk or Duare Sarkar camp.",
                            "office": "BDO Office / Duare Sarkar Desk"
                        }
                    ],
                    "required_documents_to_carry": [
                        "Original Aadhaar Card + 2 Photocopies",
                        "Single Savings Bank Passbook (with IFSC code)",
                        "Application Acknowledgement Slip / SMS"
                    ],
                    "disclaimer": "NyayaSetu AI is an independent citizen assistance platform and not a government authority."
                }
            else:  # Default Bengali
                return {
                    "detected_scheme": "অন্নপূর্ণা ভাণ্ডার (Annapurna Bhandar / DBT Scheme)",
                    "status_category": "Action Required / On Hold",
                    "status_summary": "আপনার আবেদনটি বাতিল হয়নি, সাময়িক স্থগিত আছে। এর প্রধান কারণ আপনার ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) সক্রিয় লিঙ্ক নেই অথবা অ্যাকাউন্টে ত্রুটি রয়েছে।",
                    "status_summary_bn": "আপনার আবেদনটি বাতিল হয়নি, সাময়িক স্থগিত আছে। এর প্রধান কারণ আপনার ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) সক্রিয় লিঙ্ক নেই অথবা অ্যাকাউন্টে ত্রুটি রয়েছে।",
                    "status_summary_hi": "आपका आवेदन खारिज नहीं हुआ है, बल्कि रुका हुआ है। इसका मुख्य कारण बैंक खाते में आधार डीबीटी (NPCI) लिंक न होना है।",
                    "status_summary_en": "Your application is currently paused and NOT rejected. The issue is that your bank account lacks active Aadhaar Direct Benefit Transfer (DBT/NPCI) mapping.",
                    "root_cause_identified": "ব্যাঙ্ক অ্যাকাউন্টে আধার NPCI DBT ম্যাপিং নিষ্ক্রিয় (Inactive NPCI Seeding)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "আপনার মূল ব্যাংক শাখায় যান যেখানে আপনার নিজস্ব একক অ্যাকাউন্ট রয়েছে (কোনো উপ-গ্রাহক কেন্দ্রে না গিয়ে)।",
                            "action_bn": "আপনার মূল ব্যাংক শাখায় যান যেখানে আপনার নিজস্ব একক অ্যাকাউন্ট রয়েছে (কোনো উপ-গ্রাহক কেন্দ্রে না গিয়ে)।",
                            "action_hi": "अपने मूल बैंक शाखा में जाएँ जहाँ आपका सिंगल खाता है।",
                            "action_en": "Visit your home bank branch where your single savings account is located.",
                            "office": "মূল ব্যাঙ্ক শাখা (Home Branch)"
                        },
                        {
                            "step_number": 2,
                            "action": "ব্যাংক থেকে 'আধার এনপিসিআই ডিবিটি ম্যান্ডেট ফরম' নিয়ে পূরণ করুন এবং আধারের জেরক্স জমা দিয়ে রসিদে সিলমোহর নিন।",
                            "action_bn": "ব্যাংক থেকে 'আধার এনপিসিআই ডিবিটি ম্যান্ডেট ফরম' নিয়ে পূরণ করুন এবং আধারের জেরক্স জমা দিয়ে রসিদে সিলমোহর নিন।",
                            "action_hi": "बैंक से 'Aadhaar NPCI DBT Mandate Form' लें, भरें और मुहर लगी पावती लें।",
                            "action_en": "Fill the Aadhaar NPCI DBT Mandate Form with Aadhaar photocopy and obtain a stamped receipt.",
                            "office": "ব্যাঙ্ক শাখা কাউন্টার"
                        },
                        {
                            "step_number": 3,
                            "action": "সিলমোহরকৃত রসিদ ও আবেদন আইডি স্লিপ নিয়ে স্থানীয় বিডিও অফিস বা দুয়ারে সরকার ডেস্কে স্ট্যাটাস আপডেট করান।",
                            "action_bn": "সিলমোহরকৃত রসিদ ও আবেদন আইডি স্লিপ নিয়ে স্থানীয় বিডিও অফিস বা দুয়ারে সরকার ডেস্কে স্ট্যাটাস আপডেট করান।",
                            "action_hi": "मुहर लगी रसीद लेकर BDO कार्यालय या दुआरे सरकार कैंप में जमा करें।",
                            "action_en": "Take the stamped acknowledgment to your BDO office or Duare Sarkar helpdesk to resume processing.",
                            "office": "BDO অফিস / দুয়ারে সরকার ডেস্ক"
                        }
                    ],
                    "required_documents_to_carry": [
                        "আধার কার্ডের মূল কপি ও জেরক্স",
                        "একক সেভিংস ব্যাংক পাসবই (IFSC স্পষ্ট)",
                        "আবেদন রশিদ স্লিপ / এসএমএস (Beneficiary ID)"
                    ],
                    "disclaimer": "ন্যায়সেতু AI একটি স্বাধীন নাগরিক সহায়তা উদ্যোগ, কোনো সরকারি দফতর নয়।"
                }

        # 2. Krishak Bandhu RoR / Land Mismatch
        elif any(k in lower for k in ["krishak", "bandhu", "k-bandhu", "ror", "khaitan", "plot", "land", "porcha", "bl&lro"]):
            if lang == 'hi':
                return {
                    "detected_scheme": "कृषक बंधु (Krishak Bandhu Scheme)",
                    "status_category": "Defective / Mismatch",
                    "status_summary": "कृषक बंधु में आपके आवेदन का सत्यापन पंचायत/भूमि रिकॉर्ड के खतियान/प्लॉट एरिया से मेल न खाने के कारण रुका हुआ है।",
                    "status_summary_bn": "কৃষক বন্ধু প্রকল্পে আপনার আবেদনের তথ্য গ্রাম পঞ্চায়েত বা ভূমি রেকর্ডের খতিয়ান/দাগের তথ্যের সাথে না মেলায় যাচাইকরণ প্রক্রিয়া স্থগিত রয়েছে।",
                    "status_summary_hi": "कृषक बंधु में आपके आवेदन का सत्यापन पंचायत/भूमि रिकॉर्ड के खतियान/प्लॉट एरिया से मेल न खाने के कारण रुका हुआ है।",
                    "status_summary_en": "Verification is pending due to discrepancy between application land records and Gram Panchayat/BL&LRO RoR records.",
                    "root_cause_identified": "জমির খতিয়ান/দাগ তথ্যের অমিল (RoR Land Record Area Discrepancy)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "BL&LRO कार्यालय या बांग्लारभूमि पोर्टल से अपनी ज़मीन का नवीनतम प्रमाणित परचा (RoR) प्राप्त करें।",
                            "action_bn": "BL&LRO অফিস বা বাংলারভূমি পোর্টাল থেকে আপনার জমির সর্বশেষ সার্টিফায়েড পরচা (RoR) সংগ্রহ করুন।",
                            "action_hi": "BL&LRO कार्यालय या बांग्लारभूमि पोर्टल से अपनी ज़मीन का नवीनतम प्रमाणित परचा (RoR) प्राप्त करें।",
                            "action_en": "Collect certified copy of RoR/Porcha from BL&LRO office or Banglarbhumi portal.",
                            "office": "BL&LRO Office"
                        },
                        {
                            "step_number": 2,
                            "action": "ब्लॉक सहायक कृषि अधिकारी (ADA - Agriculture) कार्यालय में सुधार आवेदन जमा करें।",
                            "action_bn": "ব্লক সহ-কৃষি অধিকর্তা (ADA - Agriculture) কার্যালয়ে সংশোধনের আবেদন জমা দিন।",
                            "action_hi": "ब्लॉक सहायक कृषि अधिकारी (ADA - Agriculture) कार्यालय में सुधार आवेदन जमा करें।",
                            "action_en": "Submit rectification application at Block Assistant Director of Agriculture (ADA) office.",
                            "office": "ADA Agriculture Office"
                        }
                    ],
                    "required_documents_to_carry": ["नवीनतम परचा (RoR Certified)", "आधार कार्ड", "बैंक पासबुक", "कृषक बंधु पावती पर्ची"],
                    "disclaimer": "न्यायसेतु AI एक स्वतंत्र नागरिक सहायता गाइड है।"
                }
            elif lang == 'en':
                return {
                    "detected_scheme": "Krishak Bandhu (Agriculture Welfare Scheme)",
                    "status_category": "Defective / Mismatch",
                    "status_summary": "Your Krishak Bandhu verification is pending due to an area or Khaitan/Plot discrepancy between your application and land records.",
                    "status_summary_bn": "কৃষক বন্ধু প্রকল্পে আপনার আবেদনের তথ্য গ্রাম পঞ্চায়েত বা ভূমি রেকর্ডের খতিয়ান/দাগের তথ্যের সাথে না মেলায় যাচাইকরণ প্রক্রিয়া স্থগিত রয়েছে।",
                    "status_summary_hi": "कृषक बंधु में आपके आवेदन का सत्यापन भूमि रिकॉर्ड से मेल न खाने के कारण रुका हुआ है।",
                    "status_summary_en": "Your Krishak Bandhu verification is pending due to an area or Khaitan/Plot discrepancy between your application and land records.",
                    "root_cause_identified": "RoR Plot/Khaitan Land Record Discrepancy",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "Collect latest certified RoR / Porcha from the BL&LRO office or Banglarbhumi portal.",
                            "action_bn": "BL&LRO অফিস থেকে সর্বশেষ সার্টিফায়েড পরচা সংগ্রহ করুন।",
                            "action_hi": "BL&LRO कार्यालय से प्रमाणित परचा प्राप्त करें।",
                            "action_en": "Collect latest certified RoR / Porcha from the BL&LRO office or Banglarbhumi portal.",
                            "office": "BL&LRO Office"
                        },
                        {
                            "step_number": 2,
                            "action": "Visit Block ADA (Agriculture) office and submit rectification form with Porcha copy.",
                            "action_bn": "ব্লক সহ-কৃষি অধিকর্তা (ADA) কার্যালয়ে পরচার কপি জমা দিন।",
                            "action_hi": "ब्लॉक ADA (कृषि) कार्यालय में सुधार आवेदन जमा करें।",
                            "action_en": "Visit Block ADA (Agriculture) office and submit rectification form with Porcha copy.",
                            "office": "ADA Office"
                        }
                    ],
                    "required_documents_to_carry": ["Latest Certified Porcha (RoR)", "Aadhaar Card", "Bank Passbook", "Application Slip"],
                    "disclaimer": "NyayaSetu AI is an independent citizen guide."
                }
            else:
                return {
                    "detected_scheme": "কৃষক বন্ধু (Krishak Bandhu)",
                    "status_category": "Defective / Mismatch",
                    "status_summary": "কৃষক বন্ধু প্রকল্পে আপনার আবেদনের তথ্য গ্রাম পঞ্চায়েত বা ভূমি রেকর্ডের খতিয়ান/দাগের তথ্যের সাথে না মেলায় যাচাইকরণ প্রক্রিয়া স্থগিত রয়েছে।",
                    "status_summary_bn": "কৃষক বন্ধু প্রকল্পে আপনার আবেদনের তথ্য গ্রাম পঞ্চায়েত বা ভূমি রেকর্ডের খতিয়ান/দাগের তথ্যের সাথে না মেলায় যাচাইকরণ প্রক্রিয়া স্থগিত রয়েছে।",
                    "status_summary_hi": "कृषक बंधु में आपके आवेदन का सत्यापन भूमि रिकॉर्ड से मेल न खाने के कारण रुका हुआ है।",
                    "status_summary_en": "Your Krishak Bandhu verification is pending due to a discrepancy in land record (RoR/Khaitan).",
                    "root_cause_identified": "জমির খতিয়ান/দাগ তথ্যের অমিল (RoR Land Record Area Discrepancy)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "BL&LRO অফিস বা বাংলারভূমি পোর্টাল থেকে আপনার জমির সর্বশেষ সার্টিফায়েড পরচা (RoR) সংগ্রহ করুন।",
                            "action_bn": "BL&LRO অফিস বা বাংলারভূমি পোর্টাল থেকে আপনার জমির সর্বশেষ সার্টিফায়েড পরচা (RoR) সংগ্রহ করুন।",
                            "action_hi": "BL&LRO कार्यालय से प्रमाणित परचा प्राप्त करें।",
                            "action_en": "Collect certified copy of RoR/Porcha from BL&LRO office or Banglarbhumi portal.",
                            "office": "BL&LRO অফিস"
                        },
                        {
                            "step_number": 2,
                            "action": "ব্লক সহ-কৃষি অধিকর্তা (ADA - Agriculture) কার্যালয়ে সংশোধনের আবেদন জমা দিন।",
                            "action_bn": "ব্লক সহ-কৃষি অধিকর্তা (ADA - Agriculture) কার্যালয়ে সংশোধনের আবেদন জমা দিন।",
                            "action_hi": "ब्लॉक सहायक कृषि अधिकारी कार्यालय में आवेदन दें।",
                            "action_en": "Submit rectification application at Block ADA office.",
                            "office": "ব্লক কৃষি দপ্তর (ADA)"
                        }
                    ],
                    "required_documents_to_carry": ["সর্বশেষ সার্টিফায়েড পরচা (RoR)", "আধার কার্ড", "ব্যাংক পাসবই", "কৃষক বন্ধু আবেদন রশিদ"],
                    "disclaimer": "ন্যায়সেতু AI একটি স্বাধীন নাগরিক সহায়তা উদ্যোগ।"
                }

        # 3. Gibberish / Random / Unrelated ("उल्टा सीधा संदेश") or Unclassified Text
        # Check if text is gibberish, very short, random characters, or unrelated words
        is_random_or_unrelated = (
            len(lower) < 10 or
            any(k in lower for k in ["asdf", "qwer", "zxcv", "test", "hello", "hi", "kaisa hai", "kya haal", "recipe", "biryani", "weather"]) or
            not any(c.isalnum() for c in lower)
        )

        if is_random_or_unrelated:
            if lang == 'hi':
                return {
                    "detected_scheme": "सामान्य पूछताछ / अनिर्धारित संदेश (General Inquiry)",
                    "status_category": "Guidance / सामान्य सहायता",
                    "status_summary": "आपने जो संदेश या इनपुट दिया है, वह पश्चिम बंगाल सरकार के किसी आधिकारिक कल्याण नोटिस या एसएमएस (जैसे अन्नपूर्णा भंडार, कृषक बंधु, स्वास्थ्य साथी) से मेल नहीं खाता है। कृपया सरकारी मैसेज या रसीद की स्पष्ट फोटो अपलोड करें।",
                    "status_summary_bn": "আপনার দেওয়া টেক্সট বা ছবিটি পশ্চিমবঙ্গ সরকারের কোনো নির্দিষ্ট প্রকল্প নোটিশ বা সরকারি এসএমএস (যেমন অন্নপূর্ণা ভাণ্ডার, কৃষক বন্ধু ইত্যাদি)-র সাথে সরাসরি মিলছে না। অনুগ্রহ করে সঠিক সরকারি মেসেজ বা রসিদ দিন।",
                    "status_summary_hi": "आपने जो संदेश या इनपुट दिया है, वह पश्चिम बंगाल सरकार के किसी आधिकारिक कल्याण नोटिस या एसएमएस (जैसे अन्नपूर्णा भंडार, कृषक बंधु, स्वास्थ्य साथी) से मेल नहीं खाता है। कृपया सरकारी मैसेज या रसीद की स्पष्ट फोटो अपलोड करें।",
                    "status_summary_en": "The provided text or image does not appear to be an official West Bengal Government welfare notice or SMS (such as Annapurna Bhandar, Krishak Bandhu, Swasthya Sathi). Please upload a valid government SMS or slip.",
                    "root_cause_identified": "অপ্রাসঙ্গিক বা অপাঠ্য ইনপুট (Unrecognized / Non-Scheme Input)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "अपने मोबाइल इनबॉक्स में सरकारी एसएमएस खोजें (सेंडर आईडी जैसे WBGOVT, WBLKBH, DGSGVT) और उसे यहाँ पेस्ट करें।",
                            "action_bn": "আপনার মোবাইলের মেসেজ ইনবক্সে সরকারি এসএমএস (WBGOVT, WBLKBH ইত্যাদি) খুঁজে কপি করে এখানে পেস্ট করুন।",
                            "action_hi": "अपने मोबाइल इनबॉक्स में सरकारी एसएमएस खोजें (सेंडर आईडी जैसे WBGOVT, WBLKBH, DGSGVT) और उसे यहाँ पेस्ट करें।",
                            "action_en": "Check your mobile phone inbox for official SMS from WBGOVT/WBLKBH and paste the exact text.",
                            "office": "Mobile SMS Inbox"
                        },
                        {
                            "step_number": 2,
                            "action": "अपनी योजना का स्टेटस जानने के लिए निकटतम BDO कार्यालय, बांग्ला सहायता केंद्र (BSK) या दुआरे सरकार कैंप जाएँ।",
                            "action_bn": "আবেদনের স্ট্যাটাস জানতে স্থানীয় বিডিও অফিস, বাংলা সহায়তা কেন্দ্র (BSK) বা দুয়ারে সরকার ক্যাম্পে যোগাযোগ করুন।",
                            "action_hi": "अपनी योजना का स्टेटस जानने के लिए निकटतम BDO कार्यालय, बांग्ला सहायता केंद्र (BSK) या दुआरे सरकार कैंप जाएँ।",
                            "action_en": "Visit your local BDO office, Bangla Sahayata Kendra (BSK), or Duare Sarkar helpdesk with your slip.",
                            "office": "BDO Office / BSK Center"
                        },
                        {
                            "step_number": 3,
                            "action": "किसी भी योजना की पात्रता और ज़रूरी दस्तावेज़ों की जानकारी के लिए नया सेतु AI चैटबॉट से सीधे सवाल पूछें।",
                            "action_bn": "যেকোনো প্রকল্পের শর্তাবলী জানতে ওয়েবসাইটের নয়া সেতু AI চ্যাটবটকে সরাসরি প্রশ্ন করতে পারেন।",
                            "action_hi": "किसी भी योजना की पात्रता और ज़रूरी दस्तावेज़ों की जानकारी के लिए नया सेतु AI चैटबॉट से सीधे सवाल पूछें।",
                            "action_en": "You can also chat with NayaSetu Sahayak AI assistant on this website to explore scheme guidelines.",
                            "office": "NayaSetu AI Sahayak"
                        }
                    ],
                    "required_documents_to_carry": [
                        "आधार कार्ड",
                        "पंजीकृत मोबाइल नंबर वाला फोन",
                        "सरकारी आवेदन पावती रसीद (Application Slip)"
                    ],
                    "disclaimer": "न्यायसेतु AI एक स्वतंत्र नागरिक सहायता गाइड है।"
                }
            elif lang == 'en':
                return {
                    "detected_scheme": "General Citizen Inquiry (অনির্দিষ্ট অনুসন্ধান)",
                    "status_category": "Guidance / General Support",
                    "status_summary": "The input provided does not match a recognized West Bengal Government welfare scheme SMS or rejection notice (e.g. Annapurna Bhandar, Krishak Bandhu, Swasthya Sathi). Please paste the exact government SMS or upload a photo of your application slip.",
                    "status_summary_bn": "আপনার দেওয়া টেক্সট বা ছবিটি পশ্চিমবঙ্গ সরকারের কোনো নির্দিষ্ট প্রকল্প নোটিশ বা সরকারি এসএমএস-এর সাথে সরাসরি মিলছে না। অনুগ্রহ করে সঠিক সরকারি মেসেজ বা রসিদ দিন।",
                    "status_summary_hi": "आपने जो इनपुट दिया है, वह सरकारी नोटिस या एसएमएस से मेल नहीं खाता है। कृपया सही मैसेज या रसीद दें।",
                    "status_summary_en": "The input provided does not match a recognized West Bengal Government welfare scheme SMS or rejection notice (e.g. Annapurna Bhandar, Krishak Bandhu, Swasthya Sathi). Please paste the exact government SMS or upload a photo of your application slip.",
                    "root_cause_identified": "Unrecognized / Casual / Gibberish Input Format",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "Check your phone's SMS inbox for messages from sender codes like 'WBGOVT', 'WBLKBH', or 'DGSGVT' and paste that text.",
                            "action_bn": "আপনার ফোনের ইনবক্স থেকে 'WBGOVT' বা 'WBLKBH' প্রেরকের মেসেজটি কপি করে পেস্ট করুন।",
                            "action_hi": "अपने फोन इनबॉक्स से सरकारी एसएमएस कॉपी करके पेस्ट करें।",
                            "action_en": "Check your phone's SMS inbox for messages from sender codes like 'WBGOVT', 'WBLKBH', or 'DGSGVT' and paste that text.",
                            "office": "Mobile SMS Inbox"
                        },
                        {
                            "step_number": 2,
                            "action": "Visit your local BDO office or Bangla Sahayata Kendra (BSK) with your Application Acknowledgement Slip.",
                            "action_bn": "আপনার আবেদন রশিদ নিয়ে নিকটস্থ বিডিও অফিস বা বাংলা সহায়তা কেন্দ্রে (BSK) যোগাযোগ করুন।",
                            "action_hi": "अपनी आवेदन रसीद लेकर BDO कार्यालय या बांग्ला सहायता केंद्र (BSK) जाएँ।",
                            "action_en": "Visit your local BDO office or Bangla Sahayata Kendra (BSK) with your Application Acknowledgement Slip.",
                            "office": "BDO Office / BSK Center"
                        },
                        {
                            "step_number": 3,
                            "action": "You can also ask NayaSetu Sahayak AI right here on this website for any scheme guidelines or eligibility rules.",
                            "action_bn": "যেকোনো প্রকল্পের শর্তাবলী জানতে ওয়েবসাইটের নয়া সেতু AI চ্যাটবটকে সরাসরি প্রশ্ন করতে পারেন।",
                            "action_hi": "किसी भी योजना के नियम जानने के लिए नया सेतु AI चैटबॉट से सवाल पूछें।",
                            "action_en": "You can also ask NayaSetu Sahayak AI right here on this website for any scheme guidelines or eligibility rules.",
                            "office": "NayaSetu AI Sahayak"
                        }
                    ],
                    "required_documents_to_carry": [
                        "Original Aadhaar Card",
                        "Registered Mobile Phone",
                        "Application Acknowledgment Slip"
                    ],
                    "disclaimer": "NyayaSetu AI is an independent citizen assistance platform and not a government authority."
                }
            else:  # Default Bengali
                return {
                    "detected_scheme": "সাধারণ অনুসন্ধান / অনির্ধারিত বার্তা (General Inquiry)",
                    "status_category": "Guidance / সাধারণ সহায়তা",
                    "status_summary": "আপনার দেওয়া টেক্সট বা ছবিটি পশ্চিমবঙ্গ সরকারের কোনো নির্দিষ্ট প্রকল্প নোটিশ বা সরকারি এসএমএস (যেমন অন্নপূর্ণা ভাণ্ডার, কৃষক বন্ধু, স্বাস্থ্য সাথী ইত্যাদি)-র সাথে মিলছে না। অনুগ্রহ করে সঠিক সরকারি মেসেজ পেস্ট করুন অথবা রসিদের ছবি দিন।",
                    "status_summary_bn": "আপনার দেওয়া টেক্সট বা ছবিটি পশ্চিমবঙ্গ সরকারের কোনো নির্দিষ্ট প্রকল্প নোটিশ বা সরকারি এসএমএস (যেমন অন্নপূর্ণা ভাণ্ডার, কৃষক বন্ধু, স্বাস্থ্য সাথী ইত্যাদি)-র সাথে মিলছে না। অনুগ্রহ করে সঠিক সরকারি মেসেজ পেস্ট করুন অথবা রসিদের ছবি দিন।",
                    "status_summary_hi": "आपने जो संदेश दिया है, वह सरकारी नोटिस या एसएमएस से मेल नहीं खाता है। कृपया सही सरकारी मैसेज या रसीद दें।",
                    "status_summary_en": "The input provided does not match a recognized West Bengal Government welfare scheme notice or SMS. Please paste the official SMS or upload a photo of the slip.",
                    "root_cause_identified": "অপ্রাসঙ্গিক বা অপাঠ্য ইনপুট (Unrecognized / Non-Scheme Input)",
                    "action_steps": [
                        {
                            "step_number": 1,
                            "action": "আপনার মোবাইলের মেসেজ ইনবক্সে 'WBGOVT', 'WBLKBH' বা 'DGSGVT' প্রেরকের এসএমএস খুঁজে কপি করে এখানে পেস্ট করুন।",
                            "action_bn": "আপনার মোবাইলের মেসেজ ইনবক্সে 'WBGOVT', 'WBLKBH' বা 'DGSGVT' প্রেরকের এসএমএস খুঁজে কপি করে এখানে পেস্ট করুন।",
                            "action_hi": "अपने मोबाइल इनबॉक्स से सरकारी एसएमएस कॉपी करके यहाँ पेस्ट करें।",
                            "action_en": "Search your mobile inbox for SMS from 'WBGOVT' or 'WBLKBH' and paste it here.",
                            "office": "মোবাইল এসএমএস ইনবক্স"
                        },
                        {
                            "step_number": 2,
                            "action": "আবেদনের সঠিক স্ট্যাটাস জানতে আবেদন রশিদটি নিয়ে নিকটস্থ বিডিও অফিস, বাংলা সহায়তা কেন্দ্র (BSK) বা দুয়ারে সরকার ক্যাম্পে যোগাযোগ করুন।",
                            "action_bn": "আবেদনের সঠিক স্ট্যাটাস জানতে আবেদন রশিদটি নিয়ে নিকটস্থ বিডিও অফিস, বাংলা সহায়তা কেন্দ্র (BSK) বা দুয়ারে সরকার ক্যাম্পে যোগাযোগ করুন।",
                            "action_hi": "सही स्थिति जानने के लिए BDO कार्यालय या बांग्ला सहायता केंद्र (BSK) से संपर्क करें।",
                            "action_en": "Visit your local BDO office or Bangla Sahayata Kendra (BSK) to check actual application status.",
                            "office": "BDO অফিস / BSK কেন্দ্র"
                        },
                        {
                            "step_number": 3,
                            "action": "পশ্চিমবঙ্গের যেকোনো প্রকল্পের নিয়ম ও নথিপত্র জানতে ওয়েবসাইটের নিচে থাকা 'নয়া সেতু AI' সহায়কের সাথে সরাসরি চ্যাট করুন।",
                            "action_bn": "পশ্চিমবঙ্গের যেকোনো প্রকল্পের নিয়ম ও নথিপত্র জানতে ওয়েবসাইটের নিচে থাকা 'নয়া সেতু AI' সহায়কের সাথে সরাসরি চ্যাট করুন।",
                            "action_hi": "किसी भी योजना की जानकारी के लिए नया सेतु AI चैटबॉट से सवाल पूछें।",
                            "action_en": "Chat with NayaSetu Sahayak AI directly on this website for scheme eligibility and requirements.",
                            "office": "নয়া সেতু AI সহায়ক"
                        }
                    ],
                    "required_documents_to_carry": [
                        "আধার কার্ডের মূল কপি",
                        "পঞ্জিকৃত মোবাইল ফোন নম্বর",
                        "সরকারি আবেদন রশিদ স্লিপ (Acknowledgement Slip)"
                    ],
                    "disclaimer": "ন্যায়সেতু AI একটি স্বাধীন নাগরিক সহায়তা উদ্যোগ, কোনো সরকারি দফতর নয়।"
                }

        # 4. Standard Under Review response
        if lang == 'hi':
            return {
                "detected_scheme": "पश्चिम बंगाल सामाजिक सुरक्षा योजना (Welfare Scheme)",
                "status_category": "Under Review / सत्यापन जारी",
                "status_summary": "नोटिस के अनुसार आपका आवेदन प्राप्त हो चुका है और वर्तमान में विभागीय सत्यापन प्रक्रिया में है।",
                "status_summary_bn": "বিজ্ঞপ্তি অনুসারে আপনার আবেদনটি গৃহীত হয়েছে এবং তথ্য যাচাইয়ের পর্যায়ে রয়েছে।",
                "status_summary_hi": "नोटिस के अनुसार आपका आवेदन प्राप्त हो चुका है और वर्तमान में विभागीय सत्यापन प्रक्रिया में है।",
                "status_summary_en": "The notice indicates that your application has been received and is undergoing clerical verification.",
                "root_cause_identified": "नियमित दस्तावेज़ सत्यापन प्रक्रिया (Routine Verification)",
                "action_steps": [
                    {
                        "step_number": 1,
                        "action": "अपनी आवेदन पावती रसीद संख्या (Acknowledgement Slip) सुरक्षित रखें।",
                        "action_bn": "আপনার আবেদন রশিদ নম্বরটি সাবধানে রাখুন।",
                        "action_hi": "अपनी आवेदन पावती रसीद संख्या (Acknowledgement Slip) सुरक्षित रखें।",
                        "action_en": "Keep your Application Acknowledgement Slip number safe.",
                        "office": "Self"
                    },
                    {
                        "step_number": 2,
                        "action": "7 से 10 दिनों के बाद निकटतम BDO कार्यालय या दुआरे सरकार कैंप में स्थिति जाँचें।",
                        "action_bn": "৭-১০ দিন পর নিকটস্থ দুয়ারে সরকার ক্যাম্প বা বিডিও অফিসে স্ট্যাটাস চেক করুন।",
                        "action_hi": "7 से 10 दिनों के बाद निकटतम BDO कार्यालय या दुआरे सरकार कैंप में स्थिति जाँचें।",
                        "action_en": "Check status after 7-10 days at your nearest Duare Sarkar camp or BDO office.",
                        "office": "BDO Office / Duare Sarkar Desk"
                    }
                ],
                "required_documents_to_carry": ["आवेदन पावती रसीद (Acknowledgement Slip)"],
                "disclaimer": "न्यायसेतु AI एक स्वतंत्र नागरिक सहायता गाइड है।"
            }
        elif lang == 'en':
            return {
                "detected_scheme": "West Bengal Social Security Scheme",
                "status_category": "Under Review / In Progress",
                "status_summary": "The notice indicates that your application has been received and is currently undergoing official verification.",
                "status_summary_bn": "বিজ্ঞপ্তি অনুসারে আপনার আবেদনটি গৃহীত হয়েছে এবং তথ্য যাচাইয়ের পর্যায়ে রয়েছে।",
                "status_summary_hi": "नोटिस के अनुसार आपका आवेदन प्राप्त हो चुका है और वर्तमान में सत्यापन प्रक्रिया में है।",
                "status_summary_en": "The notice indicates that your application has been received and is currently undergoing official verification.",
                "root_cause_identified": "Routine Verification / Document Check",
                "action_steps": [
                    {
                        "step_number": 1,
                        "action": "Keep your Application Acknowledgement Number safe.",
                        "action_bn": "আপনার আবেদন রশিদ নম্বরটি সাবধানে রাখুন।",
                        "action_hi": "अपनी आवेदन रसीद संख्या सुरक्षित रखें।",
                        "action_en": "Keep your Application Acknowledgement Number safe.",
                        "office": "Self"
                    },
                    {
                        "step_number": 2,
                        "action": "Check status again after 7-10 days at the nearest Duare Sarkar camp or BDO office.",
                        "action_bn": "৭-১০ দিন পর নিকটস্থ দুয়ারে সরকার ক্যাম্প বা বিডিও অফিসে স্ট্যাটাস চেক করুন।",
                        "action_hi": "7-10 दिनों के बाद BDO कार्यालय में स्थिति जाँचें।",
                        "action_en": "Check status again after 7-10 days at the nearest Duare Sarkar camp or BDO office.",
                        "office": "Duare Sarkar / BDO Office"
                    }
                ],
                "required_documents_to_carry": ["Application Acknowledgement Slip"],
                "disclaimer": "NyayaSetu AI is an independent citizen assistance platform."
            }
        else:
            return {
                "detected_scheme": "পশ্চিমবঙ্গ সামাজিক সুরক্ষা প্রকল্প (Welfare Scheme)",
                "status_category": "Under Review / প্রক্রিয়াধীন",
                "status_summary": "বিজ্ঞপ্তি অনুসারে আপনার আবেদনটি গৃহীত হয়েছে এবং সংশ্লিষ্ট দফতরে তথ্য যাচাইয়ের পর্যায়ে রয়েছে।",
                "status_summary_bn": "বিজ্ঞপ্তি অনুসারে আপনার আবেদনটি গৃহীত হয়েছে এবং সংশ্লিষ্ট দফতরে তথ্য যাচাইয়ের পর্যায়ে রয়েছে।",
                "status_summary_hi": "नोटिस के अनुसार आपका आवेदन प्राप्त हो चुका है और सत्यापन प्रक्रिया में है।",
                "status_summary_en": "The notice indicates that your application has been received and is undergoing clerical verification.",
                "root_cause_identified": "নথি ও তথ্য যাচাইকরণ প্রক্রিয়া (Routine Verification)",
                "action_steps": [
                    {
                        "step_number": 1,
                        "action": "আপনার আবেদন রশিদ নম্বরটি (Application ID) সাবধানে সংরক্ষণ করুন।",
                        "action_bn": "আপনার আবেদন রশিদ নম্বরটি (Application ID) সাবধানে সংরক্ষণ করুন।",
                        "action_hi": "अपनी आवेदन रसीद संख्या सुरक्षित रखें।",
                        "action_en": "Keep your Application Acknowledgement Number safe.",
                        "office": "Self"
                    },
                    {
                        "step_number": 2,
                        "action": "৭-১০ দিন পর নিকটস্থ দুয়ারে সরকার ক্যাম্প বা বিডিও অফিসে স্ট্যাটাস চেক করুন।",
                        "action_bn": "৭-১০ দিন পর নিকটস্থ দুয়ারে সরকার ক্যাম্প বা বিডিও অফিসে স্ট্যাটাস চেক করুন।",
                        "action_hi": "7-10 दिनों के बाद BDO कार्यालय में स्थिति जाँचें।",
                        "action_en": "Check status again after 7-10 days at the nearest Duare Sarkar camp or BDO office.",
                        "office": "Duare Sarkar / BDO Office"
                    }
                ],
                "required_documents_to_carry": ["আবেদন রশিদ স্লিপ (Acknowledgement Slip)"],
                "disclaimer": "ন্যায়সেতু AI একটি স্বাধীন নাগরিক সহায়তা উদ্যোগ, কোনো সরকারি দফতর নয়।"
            }
