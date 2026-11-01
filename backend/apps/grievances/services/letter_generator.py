"""
Template & AI Letter Generator for official West Bengal scheme grievances.
Generates respectful, factual representations in Bengali or English.
"""
from datetime import datetime

def generate_representation_letter(
    applicant_name: str,
    contact_phone: str,
    residence_address: str,
    scheme_name: str,
    application_ref_no: str,
    original_application_date: str,
    grievance_type: str,
    addressed_to: str,
    facts_statement: str,
    language: str = "bn"
) -> str:
    today_str = datetime.now().strftime("%d/%m/%Y")
    
    if language == "bn":
        # Bengali formal administrative representation
        subject_map = {
            "delay": f"{scheme_name} প্রকল্পের আবেদন মঞ্জুর ও সহায়তা প্রদানের বিলম্ব প্রসঙ্গে আবেদন।",
            "rejection_review": f"{scheme_name} প্রকল্পের আবেদন পুনর্বিবেচনা ও তথ্য যাচাইকরণের বিনীত প্রার্থনা।",
            "dbt_failure": f"{scheme_name} প্রকল্পের ব্যাংক অ্যাকাউন্টে কিস্তির টাকা না আসা / ডিবিটি সমস্যা সমাধানের আবেদন।",
            "correction": f"{scheme_name} প্রকল্পের আবেদনে ব্যাংক/ব্যক্তিগত তথ্য সংশোধনের আবেদন।"
        }
        subject = subject_map.get(grievance_type, f"{scheme_name} প্রকল্প সম্পর্কিত বিষয়ে আবেদন।")

        letter = f"""তারিখ: {today_str}

প্রতি,
{addressed_to if addressed_to else 'মাননীয় সমষ্টি উন্নয়ন আধিকারিক (BDO) মহাশয় সমীপেষু,'}

বিষয়: {subject}

মহাশয়,
বিনীত নিবেদন এই যে, আমি নিম্নস্বাক্ষরকারী {applicant_name}, পিতা/স্বামী: ............................, গ্রাম/ওয়ার্ড: {residence_address or '............................'} এর স্থায়ী বাসিন্দা।

আমি বিগত {original_application_date or '................'} তারিখে {scheme_name} প্রকল্পের সুবিধার জন্য যথাযথ নথিপত্র সহ আবেদন জমা দিয়েছিলাম। আমার আবেদন পত্রের প্রাপ্তিস্বীকার (Acknowledgement / Ref) নম্বর হলো: {application_ref_no or '............................'}।

আমার বর্তমান সমস্যাটি নিম্নরূপ:
{facts_statement if facts_statement else 'আবেদন জমা দেওয়ার দীর্ঘদিন অতিবাহিত হওয়া সত্ত্বেও অদ্যাবধি কোনো সন্তোষজনক অগ্রগতি বা সহায়তা প্রাপ্তি ঘটেনি।'}

আমি নিশ্চিত করছি যে, আমি উক্ত প্রকল্পের নির্দেশিকা অনুযায়ী সমস্ত প্রয়োজনীয় যোগ্যতা পূরণ করি এবং এই পত্রের সাথে আমার প্রয়োজনীয় সমস্ত নথিপত্র (আধার কার্ড, ব্যাংক পাসবুক, আবেদন রশিদ) সংযুক্ত করলাম।

অতএব, মহাশয়ের নিকট আমার সনির্বন্ধ প্রার্থনা, দয়া করে আমার আবেদনপত্রটির বর্তমান অবস্থা খতিয়ে দেখে দ্রুত প্রয়োজনীয় পদক্ষেপ গ্রহণ করতে আজ্ঞা হয়।

ধন্যবাদান্তে,

বিনীত,
স্বাক্ষর: ........................................
নাম: {applicant_name}
মোবাইল নম্বর: {contact_phone}
ঠিকানা: {residence_address}

সংযুক্তি:
১. মূল আবেদন পত্রের প্রাপ্তিস্বীকার রশিদের প্রতিলিপি।
২. আধার কার্ডের প্রতিলিপি।
৩. ব্যাংক পাসবুকের প্রথম পাতার প্রতিলিপি।
"""
    else:
        # English formal representation
        subject_map = {
            "delay": f"Representation regarding inordinate delay in processing / sanction of {scheme_name} application.",
            "rejection_review": f"Prayer for re-verification and reconsideration of {scheme_name} application.",
            "dbt_failure": f"Intimation regarding non-receipt of installment / DBT failure under {scheme_name}.",
            "correction": f"Prayer for correction of personal / bank account particulars under {scheme_name}."
        }
        subject = subject_map.get(grievance_type, f"Representation regarding application under {scheme_name}.")

        letter = f"""Date: {today_str}

To,
{addressed_to if addressed_to else 'The Block Development Officer (BDO),'}

Subject: {subject}

Respected Sir/Madam,

I, the undersigned, {applicant_name}, residing at {residence_address or '[Address]'}, would like to submit the following facts for your kind consideration:

1. That I applied for the benefit under the {scheme_name} scheme on {original_application_date or '[Date of Application]'}, having Acknowledgement / Reference No: {application_ref_no or '[Application Reference No]'}, fulfilling all requisite eligibility norms.

2. Brief statement of facts/issue:
{facts_statement if facts_statement else 'Despite the lapse of considerable time, the benefit/status has not been updated or resolved.'}

3. I have enclosed photocopies of all requisite documents, including my Aadhaar card, bank passbook, and the original acknowledgement slip for your immediate perusal.

In view of the above circumstances, I earnestly request your good office to kindly look into the matter and initiate necessary administrative steps to expedite my application.

Thanking you.

Yours faithfully,

Signature: __________________________
Name: {applicant_name}
Mobile No: {contact_phone}
Address: {residence_address}

Enclosures:
1. Copy of Application Acknowledgement Slip.
2. Self-attested copy of Aadhaar Card.
3. Copy of Bank Passbook front page.
"""

    return letter
