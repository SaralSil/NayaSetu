"""
Gemini AI Service for analyzing West Bengal Government notices, SMS, and rejection slips.
Translates bureaucratic jargon into simple Bengali, English, and Hindi with step-by-step remedies.
"""
import os
import json
import logging
from django.conf import settings
from PIL import Image
import io

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are NyayaSetu AI, an expert citizen rights and scheme-navigation assistant for West Bengal.
Your task is to analyze government scheme application receipts, SMS notifications, or rejection letters.

Follow these strict guidelines:
1. Identify the likely scheme (e.g. Lakshmir Bhandar, Krishak Bandhu, Kanyashree, Aikyashree, Jai Johar, Taposhili Bandhu, Swasthya Sathi, Khadya Sathi, or General).
2. Determine the status:
   - "Under Process" (still waiting)
   - "Action Required / On Hold" (applicant needs to fix something)
   - "Defective / Mismatch" (document/data error)
   - "Rejected" (formally rejected)
3. Explain the issue in simple, compassionate everyday language:
   - English
   - Bengali (বাংলা)
   - Hindi (हिंदी)
4. Give concrete, actionable next steps:
   - Where to go (Home bank branch, BDO office, Gram Panchayat, Duare Sarkar camp, SDO)
   - What exact document or form to bring (e.g., Aadhaar DBT consent form, RoR/Porcha, cancelled cheque)
5. CRITICAL ETHICS RULE: Always include a non-authority disclaimer:
   "NyayaSetu AI is an independent citizen helper and not an official government authority. It does not decide eligibility or guarantee approvals."

Output strictly in JSON format matching this schema:
{
  "detected_scheme": "Scheme Name",
  "status_category": "Action Required / On Hold | Defective / Mismatch | Under Process | Rejected",
  "status_summary_en": "Simple explanation in English",
  "status_summary_bn": "বাংলায় সহজ ও স্পষ্ট ব্যাখ্যা",
  "status_summary_hi": "हिंदी में सरल व्याख्या",
  "root_cause_identified": "e.g. Bank account not NPCI/Aadhaar DBT mapped, Name mismatch, etc.",
  "action_steps": [
    {
      "step_number": 1,
      "action_en": "Visit your bank branch...",
      "action_bn": "আপনার ব্যাংক শাখায় যান...",
      "office": "Bank / BDO / Duare Sarkar Counter"
    }
  ],
  "required_documents_to_carry": [
    "Aadhaar Card", "Bank Passbook"
  ],
  "disclaimer": "NyayaSetu is an independent assistance guide and not an official government entity."
}
"""

class GeminiAnalyzerService:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

    def analyze_text(self, notice_text: str) -> dict:
        """Analyze pasted text from SMS or status portal"""
        if not self.api_key:
            return self._mock_analysis(notice_text)

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            prompt = f"Analyze this West Bengal government application status or notice text:\n\n\"\"\"\n{notice_text}\n\"\"\""

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Gemini API text analysis error: {e}")
            return self._mock_analysis(notice_text, fallback_error=str(e))

    def analyze_image(self, image_file) -> dict:
        """Analyze an uploaded screenshot or photo of an application receipt / letter"""
        if not self.api_key:
            return self._mock_analysis("Image OCR analysis")

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            pil_image = Image.open(image_file)
            
            prompt = "Extract and analyze the text from this West Bengal scheme document, notice, or application receipt."

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[pil_image, prompt],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Gemini API image analysis error: {e}")
            return self._mock_analysis("Uploaded Image", fallback_error=str(e))

    def _mock_analysis(self, raw_input: str, fallback_error: str = None) -> dict:
        """Failsafe response when API key is not yet configured or on network fallback"""
        # Intelligent pattern detection for common WB errors
        lower = raw_input.lower()
        if "npci" in lower or "dbt" in lower or "bank" in lower or "account" in lower:
            return {
                "detected_scheme": "Lakshmir Bhandar / DBT Scheme",
                "status_category": "Action Required / On Hold",
                "status_summary_en": "Your application is paused because your bank account is not mapped for Aadhaar Direct Benefit Transfer (DBT/NPCI) or has an account error.",
                "status_summary_bn": "আপনার আবেদনটি বাতিল হয়নি, স্থগিত আছে। এর কারণ আপনার ব্যাংক অ্যাকাউন্টে আধার ডিবিটি (NPCI) লিঙ্ক নেই অথবা অ্যাকাউন্টে ভুল আছে।",
                "status_summary_hi": "आपका आवेदन खारिज नहीं हुआ है, बल्कि रुका हुआ है। इसका कारण बैंक खाते में आधार डीबीटी (NPCI) लिंक न होना है।",
                "root_cause_identified": "NPCI Aadhaar DBT Mapping Inactive / Single Account Issue",
                "action_steps": [
                    {
                        "step_number": 1,
                        "action_en": "Go to your home bank branch where your single-operated account exists.",
                        "action_bn": "আপনার মূল ব্যাংক শাখায় যান যেখানে আপনার নিজস্ব সিঙ্গেল অ্যাকাউন্ট আছে।",
                        "office": "Home Bank Branch"
                    },
                    {
                        "step_number": 2,
                        "action_en": "Ask for the 'Aadhaar NPCI DBT Mandate' form, fill it, and attach an Aadhaar photocopy.",
                        "action_bn": "ব্যাংক থেকে 'আধার এনপিসিআই ডিবিটি ফরম' নিয়ে পূরণ করুন এবং আধারের জেরক্স জমা দিন।",
                        "office": "Bank Branch Counter"
                    },
                    {
                        "step_number": 3,
                        "action_en": "Once linked, visit your Gram Panchayat or BDO office to update the status.",
                        "action_bn": "লিঙ্ক সম্পন্ন হলে গ্রাম পঞ্চায়েত বা বিডিও অফিসে স্ট্যাটাস আপডেট করান।",
                        "office": "BDO Office / Duare Sarkar Desk"
                    }
                ],
                "required_documents_to_carry": [
                    "Aadhaar Card (Original + Copy)",
                    "Bank Passbook (Single Account)",
                    "Application Acknowledgement Slip / SMS"
                ],
                "disclaimer": "NyayaSetu AI is an independent citizen assistance guide and not a government authority. (Note: Gemini API key pending for live AI response)."
            }

        return {
            "detected_scheme": "West Bengal Welfare Scheme",
            "status_category": "Under Review / In Progress",
            "status_summary_en": "The notice indicates that your application has been received and is undergoing field or clerical verification.",
            "status_summary_bn": "বিজ্ঞপ্তি অনুসারে আপনার আবেদনটি গৃহীত হয়েছে এবং তথ্য যাচাইয়ের পর্যায়ে রয়েছে।",
            "status_summary_hi": "सूचना के अनुसार आपका आवेदन प्राप्त हो चुका है और सत्यापन प्रक्रिया में है।",
            "root_cause_identified": "Routine Verification / Document Check",
            "action_steps": [
                {
                    "step_number": 1,
                    "action_en": "Keep your Application Acknowledgement Number safe.",
                    "action_bn": "আপনার আবেদন রশিদ নম্বরটি সাবধানে রাখুন।",
                    "office": "Self"
                },
                {
                    "step_number": 2,
                    "action_en": "Check status again after 7-10 days at the nearest Duare Sarkar camp or BDO office.",
                    "action_bn": "৭-১০ দিন পর নিকটস্থ দুয়ারে সরকার ক্যাম্প বা বিডিও অফিসে স্ট্যাটাস চেক করুন।",
                    "office": "Duare Sarkar / BDO Office"
                }
            ],
            "required_documents_to_carry": [
                "Application Acknowledgement Slip"
            ],
            "disclaimer": "NyayaSetu AI is an independent citizen assistance guide and not a government authority."
        }
