"""
Template & AI Letter Generator for official West Bengal scheme grievances.
Generates respectful, factual representations in Bengali, English, and Hindi.
"""
from datetime import datetime

SCHEME_NAME_EN_MAP = {
    "প্রধানমন্ত্রী কিষাণ সম্মান নিধি (PM-KISAN)": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
    "আয়ুষ্মান ভারত (PM-JAY)": "Pradhan Mantri Ayushman Bharat Yojana (PM-JAY)",
    "প্রধানমন্ত্রী আবাস যোজনা (শহরাঞ্চল)": "Pradhan Mantri Awas Yojana (Urban)",
    "পিএম সূর্য ঘর মুফ্ত বিদ্যুৎ যোজনা": "PM Surya Ghar: Muft Bijli Yojana",
    "পিএম স্বনিধি (রাস্তার বিক্রেতা ঋণ)": "PM SVANidhi (Street Vendors AtmaNirbhar Nidhi)",
    "পশ্চিমবঙ্গ স্টুডেন্ট ক্রেডিট কার্ড": "West Bengal Student Credit Card Scheme",
    "শিক্ষাশ্রী প্রকল্প": "West Bengal Sikshashree Scheme",
    "মেধাশ্রী প্রকল্প": "West Bengal Medhashree Scheme",
    "জয় জোহার ও তপশিলী বন্ধু": "Jai Johar & Taposhili Bandhu Pension",
    "প্রধানমন্ত্রী মুদ্রা যোজনা": "Pradhan Mantri MUDRA Yojana (PMMY)",
    "প্রধানমন্ত্রী উজ্জ্বলা যোজনা": "Pradhan Mantri Ujjwala Yojana (PMUY)",
    "অটল পেনশন যোজনা": "Atal Pension Yojana (APY)",
    "বার্ধক্য বা বিধবা ভাতা (পেনশন)": "Old Age / Widow Social Pension",
}

SCHEME_NAME_HI_MAP = {
    "প্রধানমন্ত্রী কিষাণ সম্মান নিধি (PM-KISAN)": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
    "আয়ুষ্মান ভারত (PM-JAY)": "प्रधानमंत्री आयुष्मान भारत योजना (PM-JAY)",
    "প্রধানমন্ত্রী আবাস যোজনা (শহরাঞ্চল)": "प्रधानमंत्री आवास योजना (शहरी - PMAY-U)",
    "পিএম সূর্য ঘর মুফ্ত বিদ্যুৎ যোজনা": "पीएम सूर्य घर मुफ्त बिजली योजना",
    "পিএম স্বনিধি (রাস্তার বিক্রেতা ঋণ)": "पीएम स्वनिधि (स्ट्रीट वेंडर्स आत्मनिर्भर निधि)",
    "পশ্চিমবঙ্গ স্টুডেন্ট ক্রেডিট কার্ড": "पश्चिम बंगाल स्टूडेंट क्रेडिट कार्ड योजना",
    "শিক্ষাশ্রী প্রকল্প": "पश्चिम बंगाल शिक्षाश्री योजना",
    "মেধাশ্রী প্রকল্প": "पश्चिम बंगाल मेधाश्री योजना",
    "জয় জোহার ও তপশিলী বন্ধু": "जय जोहार एवं तपशिली बंधु पेंशन",
    "প্রধানমন্ত্রী মুদ্রা যোজনা": "प्रधानमंत्री मुद्रा योजना (PMMY)",
    "প্রধানমন্ত্রী উজ্জ্বলা যোজনা": "प्रधानमंत्री उज्ज्वला योजना (PMUY)",
    "অটল পেনশন যোজনা": "अटल पेंशन योजना (APY)",
    "বার্ধক্য বা বিধবা ভাতা (পেনশন)": "वृद्धावस्था / विधवा सामाजिक पेंशन",
}

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
    elif language == "hi":
        # Hindi formal administrative representation
        scheme_name_hi = SCHEME_NAME_HI_MAP.get(scheme_name, scheme_name)
        subject_map = {
            "delay": f"{scheme_name_hi} के आवेदन की स्वीकृति एवं लाभ वितरण में अत्यधिक विलंब के संबंध में आवेदन।",
            "rejection_review": f"{scheme_name_hi} के आवेदन पर पुनर्विचार एवं दस्तावेज़ पुनः सत्यापन हेतु सविनय प्रार्थना।",
            "dbt_failure": f"{scheme_name_hi} की किस्त बैंक खाते में न आने / डीबीटी (DBT/NPCI) विफलता के समाधान हेतु आवेदन।",
            "correction": f"{scheme_name_hi} के आवेदन में बैंक खाता अथवा व्यक्तिगत विवरण सुधारने हेतु आवेदन।"
        }
        subject = subject_map.get(grievance_type, f"{scheme_name_hi} संबंधित विषय में आवेदन।")

        letter = f"""दिनांक: {today_str}

सेवा में,
{addressed_to if addressed_to else 'माननीय प्रखंड विकास पदाधिकारी (BDO) महोदय / अनुमंडल पदाधिकारी (SDO) महोदय,'}

विषय: {subject}

आदरणीय महोदय / महोदया,

सविनय निवेदन है कि मैं अधोहस्ताक्षरी {applicant_name}, पिता/पति: ............................, ग्राम/वार्ड: {residence_address or '............................'} का/की स्थायी निवासी हूँ।

मैंने दिनांक {original_application_date or '................'} को {scheme_name_hi} के लाभ हेतु सभी आवश्यक एवं वैध दस्तावेज़ों के साथ आवेदन प्रस्तुत किया था। मेरे आवेदन की पावती (Acknowledgement / Ref) संख्या: {application_ref_no or '............................'} है।

मेरी वर्तमान समस्या निम्नलिखित है:
{facts_statement if facts_statement else 'आवेदन जमा किए जाने के पश्चात लंबा समय बीत जाने के बावजूद अभी तक योजना का लाभ अथवा स्पष्ट समाधान प्राप्त नहीं हुआ है।'}

मैं यह प्रमाणित करता/करती हूँ कि मैं उक्त सरकारी योजना के सभी निर्धारित पात्रता मानदंडों को पूर्ण करता/करती हूँ। इस पत्र के साथ मेरे सभी आवश्यक दस्तावेज़ (आधार कार्ड, बैंक पासबुक, मूल आवेदन पावती रसीद) संलग्न हैं।

अतः आपसे विनम्र प्रार्थना है कि कृपया मेरे आवेदन पत्र की वर्तमान स्थिति की जांच कर शीघ्र सहायता व प्रशासनिक स्वीकृति प्रदान करने की कृपा करें।

सधन्यवाद,

भवदीय / भवदीया,

हस्ताक्षर: ........................................
नाम: {applicant_name}
मोबाइल नंबर: {contact_phone}
पता: {residence_address}

संलग्नक:
१. मूल आवेदन पत्र की पावती रसीद (Acknowledgement Receipt)।
२. आधार कार्ड की स्व-सत्यापित छायाप्रति।
३. बैंक पासबुक के प्रथम पृष्ठ की स्पष्ट छायाप्रति।
"""
    else:
        # English formal representation
        scheme_name_en = SCHEME_NAME_EN_MAP.get(scheme_name, scheme_name)
        subject_map = {
            "delay": f"Representation regarding inordinate delay in processing / sanction of {scheme_name_en} application.",
            "rejection_review": f"Prayer for re-verification and reconsideration of {scheme_name_en} application.",
            "dbt_failure": f"Intimation regarding non-receipt of installment / DBT failure under {scheme_name_en}.",
            "correction": f"Prayer for correction of personal / bank account particulars under {scheme_name_en}."
        }
        subject = subject_map.get(grievance_type, f"Representation regarding application under {scheme_name_en}.")

        letter = f"""Date: {today_str}

To,
{addressed_to if addressed_to else 'The Block Development Officer (BDO) / Sub-Divisional Officer (SDO),'}

Subject: {subject}

Respected Sir/Madam,

I, the undersigned, {applicant_name}, residing at {residence_address or '[Address]'}, would like to submit the following facts for your kind consideration:

1. That I applied for the benefit under the {scheme_name_en} scheme on {original_application_date or '[Date of Application]'}, having Acknowledgement / Reference No: {application_ref_no or '[Application Reference No]'}, fulfilling all requisite eligibility norms.

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
