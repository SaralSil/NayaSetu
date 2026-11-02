# -*- coding: utf-8 -*-
"""
Script to apply comprehensive trilingual localization to frontend/Home.html:
1. Adds data-i18n to all remaining Bengali elements.
2. Updates I18N dictionary for bn, en, and hi.
3. Implements trilingual generateOfflineLetter(data) supporting bn, en, and hi.
4. Adds Hindi option to grvLang select.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/Home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Helper replacement function that handles line ending differences
def safe_replace(text, old, new):
    if old in text:
        return text.replace(old, new)
    old_lf = old.replace('\r\n', '\n')
    new_lf = new.replace('\r\n', '\n')
    if old_lf in text:
        return text.replace(old_lf, new_lf)
    old_crlf = old.replace('\n', '\r\n')
    new_crlf = new.replace('\n', '\r\n')
    if old_crlf in text:
        return text.replace(old_crlf, new_crlf)
    print(f"WARNING: Replacement not found:\n{old[:60]}...")
    return text

# 1. Quick search chips
content = safe_replace(content,
    '<div class="text-[11px] font-label font-bold uppercase text-[#A39788] mb-2">দ্রুত প্রাসঙ্গিক ফলাফল (Quick Results):</div>',
    '<div class="text-[11px] font-label font-bold uppercase text-[#A39788] mb-2" data-i18n="quick_results_title">দ্রুত প্রাসঙ্গিক ফলাফল (Quick Results):</div>'
)
content = safe_replace(content,
    '<span>অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>',
    '<span data-i18n="chip_lb">অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#F2CBA5]">₹৩০০০/মাস</span>',
    '<span class="text-[10px] text-[#F2CBA5]" data-i18n="chip_lb_amt">₹৩০০০/মাস</span>'
)
content = safe_replace(content,
    '<span>যুব শক্তি যোজনা</span>',
    '<span data-i18n="chip_ys">যুব শক্তি যোজনা</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#F2CBA5]">₹২০০০-₹৩০০০</span>',
    '<span class="text-[10px] text-[#F2CBA5]" data-i18n="chip_ys_amt">₹২০০০-₹৩০০০</span>'
)
content = safe_replace(content,
    '<span>আয়ুষ্মান ভারত</span>',
    '<span data-i18n="chip_ab">আয়ুষ্মান ভারত</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#F2CBA5]">₹৫L + ৭০+ ফ্রি</span>',
    '<span class="text-[10px] text-[#F2CBA5]" data-i18n="chip_ab_amt">₹৫L + ৭০+ ফ্রি</span>'
)
content = safe_replace(content,
    '<span>কৃষক বন্ধু</span>',
    '<span data-i18n="chip_kb">কৃষক বন্ধু</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#F2CBA5]">শস্য বীমা</span>',
    '<span class="text-[10px] text-[#F2CBA5]" data-i18n="chip_kb_amt">শস্য বীমা</span>'
)
content = safe_replace(content,
    '>কর্মশ্রী ৫০ দিন<',
    ' data-i18n="chip_km">কর্মশ্রী ৫০ দিন<'
)
content = safe_replace(content,
    '>স্বাস্থ্য সাথী কার্ড<',
    ' data-i18n="chip_ss">স্বাস্থ্য সাথী কার্ড<'
)
content = safe_replace(content,
    '<span>আধার লিঙ্ক (NPCI/DBT)</span>',
    '<span data-i18n="chip_dbt">আধার লিঙ্ক (NPCI/DBT)</span>'
)

# 2. Stepper & Cards
content = safe_replace(content,
    '<span>প্রস্তাবিত ধাপ ১</span>',
    '<span data-i18n="step_1_pill">প্রস্তাবিত ধাপ ১</span>'
)
content = safe_replace(content,
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>',
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="card_chip_lb">অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>'
)
content = safe_replace(content,
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">যুব শক্তি যোজনা</span>',
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="card_chip_ys">যুব শক্তি যোজনা</span>'
)
content = safe_replace(content,
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী</span>',
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="card_chip_ab">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী</span>'
)
content = safe_replace(content,
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">কৃষক বন্ধু ও শস্য বীমা</span>',
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="card_chip_kb">কৃষক বন্ধু ও শস্য বীমা</span>'
)
content = safe_replace(content,
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">কর্মশ্রী ও আবাস যোজনা</span>',
    '<span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="card_chip_km">কর্মশ্রী ও আবাস যোজনা</span>'
)

content = safe_replace(content,
    '<span>\'DBT Failed / Inactive Aadhaar\' সংক্রান্ত সমস্যা সমাধান</span>',
    '<span data-i18n="card_notice_b1">\'DBT Failed / Inactive Aadhaar\' সংক্রান্ত সমস্যা সমাধান</span>'
)
content = safe_replace(content,
    '<span>ব্যাঙ্ক অ্যাকাউন্ট মিসম্যাচ সংশোধন নির্দেশ</span>',
    '<span data-i18n="card_notice_b2">ব্যাঙ্ক অ্যাকাউন্ট মিসম্যাচ সংশোধন নির্দেশ</span>'
)
content = safe_replace(content,
    '<span>স্বাক্ষরের নির্দিষ্ট স্থান ও সংযুক্তি (Enclosures) তালিকা স্বয়ংক্রিয়ভাবে তৈরি</span>',
    '<span data-i18n="card_grv_b1">স্বাক্ষরের নির্দিষ্ট স্থান ও সংযুক্তি (Enclosures) তালিকা স্বয়ংক্রিয়ভাবে তৈরি</span>'
)
content = safe_replace(content,
    '<span>সরাসরি বাংলায় PDF বা এক ক্লিকে প্রিন্ট করার সুবিধা</span>',
    '<span data-i18n="card_grv_b2">সরাসরি বাংলায় PDF বা এক ক্লিকে প্রিন্ট করার সুবিধা</span>'
)
content = safe_replace(content,
    '<span>স্বাস্থ্যসাথী কার্ড, আধার, ও একক ব্যাংক অ্যাকাউন্টের নির্দেশিকা</span>',
    '<span data-i18n="card_schemes_b1">স্বাস্থ্যসাথী কার্ড, আধার, ও একক ব্যাংক অ্যাকাউন্টের নির্দেশিকা</span>'
)
content = safe_replace(content,
    '<span>দুয়ারে সরকার ক্যাম্পে জমা দেওয়ার আগে সেলফ-অ্যাটেস্টেড নিয়ম</span>',
    '<span data-i18n="card_schemes_b2">দুয়ারে সরকার ক্যাম্পে জমা দেওয়ার আগে সেলফ-অ্যাটেস্টেড নিয়ম</span>'
)

# 3. Camp banner
content = safe_replace(content,
    '<div class="text-xs sm:text-sm font-headline font-bold text-[#F7F4EE]">সুশাসন সেবা শিবির সময়সূচি ও BDO/SDO আবেদন জমাদানের সময়সীমা</div>',
    '<div class="text-xs sm:text-sm font-headline font-bold text-[#F7F4EE]" data-i18n="camp_banner_title">সুশাসন সেবা শিবির সময়সূচি ও BDO/SDO আবেদন জমাদানের সময়সীমা</div>'
)
content = safe_replace(content,
    'অন্নপূর্ণা ভাণ্ডার, আয়ুষ্মান ভারত (PM-JAY), পিএম কিষাণ ও আবাস যোজনা সহ সরকারি প্রকল্পের সরাসরি ফর্ম জমা ও স্পট ভেরিফিকেশন চলছে। আপনার অঞ্চলে ক্যাম্প না থাকলেও যেকোনো কাজের দিনে নিকটস্থ BDO (গ্রামীণ পঞ্চায়েত) বা SDO (পৌরসভা/শহর) অফিসে আবেদন জমা দিন ও প্রাপ্তি রসিদ সংগ্রহ করুন।',
    '<span data-i18n="camp_banner_desc">অন্নপূর্ণা ভাণ্ডার, আয়ুষ্মান ভারত (PM-JAY), পিএম কিষাণ ও আবাস যোজনা সহ সরকারি প্রকল্পের সরাসরি ফর্ম জমা ও স্পট ভেরিফিকেশন চলছে। আপনার অঞ্চলে ক্যাম্প না থাকলেও যেকোনো কাজের দিনে নিকটস্থ BDO (গ্রামীণ পঞ্চায়েত) বা SDO (পৌরসভা/শহর) অফিসে আবেদন জমা দিন ও প্রাপ্তি রসিদ সংগ্রহ করুন।</span>'
)
content = safe_replace(content,
    '<span>নিকটস্থ BDO / SDO অফিস খুঁজুন</span>',
    '<span data-i18n="camp_btn_find">নিকটস্থ BDO / SDO অফিস খুঁজুন</span>'
)

# 4. Stories
content = safe_replace(content,
    '<span class="font-label font-bold text-[#E2A97B]">মুর্শিদাবাদ • লালবাগ ব্লক</span>',
    '<span class="font-label font-bold text-[#E2A97B]" data-i18n="story1_loc">মুর্শিদাবাদ • লালবাগ ব্লক</span>'
)
content = safe_replace(content,
    '<span class="text-[11px] text-[#A39788] font-label">২ দিন আগে</span>',
    '<span class="text-[11px] text-[#A39788] font-label" data-i18n="story1_time">২ দিন আগে</span>'
)
content = safe_replace(content,
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold">আধার DBT সক্রিয়করণে সফল সমাধান</p>',
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold" data-i18n="story1_title">আধার DBT সক্রিয়করণে সফল সমাধান</p>'
)
content = safe_replace(content,
    '"লক্ষ্মীর ভাণ্ডারের এসএমএস রিজেকশন স্ক্যান করে ব্যাঙ্কে জমা দেওয়ার সঠিক চিঠি তৈরি করে ৩ মাসের বকেয়া টাকা অ্যাকাউন্টে জমা হয়েছে।"',
    '<span data-i18n="story1_quote">"লক্ষ্মীর ভাণ্ডারের এসএমএস রিজেকশন স্ক্যান করে ব্যাঙ্কে জমা দেওয়ার সঠিক চিঠি তৈরি করে ৩ মাসের বকেয়া টাকা অ্যাকাউন্টে জমা হয়েছে।"</span>'
)
content = safe_replace(content,
    '<span>BDO অফিসে সফল নিষ্পত্তিকরণ</span>',
    '<span data-i18n="story1_tag">BDO অফিসে সফল নিষ্পত্তিকরণ</span>'
)

content = safe_replace(content,
    '<span class="font-label font-bold text-[#E2A97B]">পূর্ব বর্ধমান • কালনা</span>',
    '<span class="font-label font-bold text-[#E2A97B]" data-i18n="story2_loc">পূর্ব বর্ধমান • কালনা</span>'
)
content = safe_replace(content,
    '<span class="text-[11px] text-[#A39788] font-label">৩ দিন আগে</span>',
    '<span class="text-[11px] text-[#A39788] font-label" data-i18n="story2_time">৩ দিন আগে</span>'
)
content = safe_replace(content,
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold">কৃষক বন্ধু খতিয়ান মিউটেশন প্রতিকার</p>',
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold" data-i18n="story2_title">কৃষক বন্ধু খতিয়ান মিউটেশন প্রতিকার</p>'
)
content = safe_replace(content,
    '"ওয়ারিশান সূত্রে রেকর্ড হওয়া জমির খতিয়ান আপডেট না থাকায় টাকা আটকে ছিল। সঠিক দরখাস্তের বয়ান নিয়ে সহকারী কৃষি অধিকর্তা (ADA) দফতরে জমা দেওয়া হয়।"',
    '<span data-i18n="story2_quote">"ওয়ারিশান সূত্রে রেকর্ড হওয়া জমির খতিয়ান আপডেট না থাকায় টাকা আটকে ছিল। সঠিক দরখাস্তের বয়ান নিয়ে সহকারী কৃষি অধিকর্তা (ADA) দফতরে জমা দেওয়া হয়।"</span>'
)
content = safe_replace(content,
    '<span>মিউটেশন অনুমোদন ও পোর্টাল আপডেট</span>',
    '<span data-i18n="story2_tag">মিউটেশন অনুমোদন ও পোর্টাল আপডেট</span>'
)

content = safe_replace(content,
    '<span class="font-label font-bold text-[#E2A97B]">দক্ষিণ ২৪ পরগনা • ক্যানিং</span>',
    '<span class="font-label font-bold text-[#E2A97B]" data-i18n="story3_loc">দক্ষিণ ২৪ পরগনা • ক্যানিং</span>'
)
content = safe_replace(content,
    '<span class="text-[11px] text-[#A39788] font-label">আজ</span>',
    '<span class="text-[11px] text-[#A39788] font-label" data-i18n="story3_time">আজ</span>'
)
content = safe_replace(content,
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold">রূপশ্রী প্রকল্পের এককালীন অনুদান যাচাই</p>',
    '<p class="text-xs font-body text-[#F7F4EE] font-semibold" data-i18n="story3_title">রূপশ্রী প্রকল্পের এককালীন অনুদান যাচাই</p>'
)
content = safe_replace(content,
    '"বিয়ের তারিখের ১৫ দিন আগে ফর্ম জমা দিতে ভুল নথিপত্র বাদ দেওয়ার জন্য চেকলিস্ট ব্যবহার করে প্রথম দফায় ফর্ম গৃহীত হয়েছে।"',
    '<span data-i18n="story3_quote">"বিয়ের তারিখের ১৫ দিন আগে ফর্ম জমা দিতে ভুল নথিপত্র বাদ দেওয়ার জন্য চেকলিস্ট ব্যবহার করে প্রথম দফায় ফর্ম গৃহীত হয়েছে।"</span>'
)
content = safe_replace(content,
    '<span>দুয়ারে সরকার সেন্টারে ফর্ম জমা সম্পন্ন</span>',
    '<span data-i18n="story3_tag">দুয়ারে সরকার সেন্টারে ফর্ম জমা সম্পন্ন</span>'
)

# 5. Notice samples & dropzone
content = safe_replace(content,
    '<span>অন্নপূর্ণা ভাণ্ডার নমুনা</span>',
    '<span data-i18n="notice_sample_lb">অন্নপূর্ণা ভাণ্ডার নমুনা</span>'
)
content = safe_replace(content,
    '>কৃষক বন্ধু নমুনা<',
    ' data-i18n="notice_sample_kb">কৃষক বন্ধু নমুনা<'
)
content = safe_replace(content,
    '<p class="text-xs font-label font-bold text-[#F7F4EE]" id="noticeDropzoneTitle">আবেদনপত্র, নোটিশ স্লিপ বা স্ক্রিনশটের ছবি নির্বাচন করুন</p>',
    '<p class="text-xs font-label font-bold text-[#F7F4EE]" id="noticeDropzoneTitle" data-i18n="notice_dropzone_title">আবেদনপত্র, নোটিশ স্লিপ বা স্ক্রিনশটের ছবি নির্বাচন করুন</p>'
)
content = safe_replace(content,
    '<p class="text-[11px] text-[#A39788] mt-0.5 font-body">ছবি টেনে আনুন অথবা এখানে ক্লিক করে ছবি আপলোড করুন (JPG, PNG, WebP • সর্বোচ্চ ১০ এমবি)</p>',
    '<p class="text-[11px] text-[#A39788] mt-0.5 font-body" data-i18n="notice_dropzone_sub">ছবি টেনে আনুন অথবা এখানে ক্লিক করে ছবি আপলোড করুন (JPG, PNG, WebP • সর্বোচ্চ ১০ এমবি)</p>'
)
content = safe_replace(content,
    '<span class="inline-block mt-0.5 px-1.5 py-0.2 rounded bg-[#201C18] text-[10px] text-[#78FBB6] font-bold">✓ ছবি যুক্ত করা হয়েছে</span>',
    '<span class="inline-block mt-0.5 px-1.5 py-0.2 rounded bg-[#201C18] text-[10px] text-[#78FBB6] font-bold" data-i18n="notice_img_attached">✓ ছবি যুক্ত করা হয়েছে</span>'
)
content = safe_replace(content,
    '<span>মুছুন</span>',
    '<span data-i18n="notice_btn_remove">মুছুন</span>'
)

# 6. Grievance Modal
content = safe_replace(content,
    '<span class="text-[#F2CBA5]">আপনার একটি পূর্ববর্তী প্রস্তুতকৃত চিঠি সংরক্ষিত রয়েছে।</span>',
    '<span class="text-[#F2CBA5]" data-i18n="grv_resume_text">আপনার একটি পূর্ববর্তী প্রস্তুতকৃত চিঠি সংরক্ষিত রয়েছে।</span>'
)
content = safe_replace(content,
    '<span>চিঠি দেখুন (View Letter)</span>',
    '<span data-i18n="grv_resume_btn">চিঠি দেখুন (View Letter)</span>'
)

# Add Hindi to grvLang
old_grv_lang = """                <select id="grvLang" class="w-full bg-[#141210] border border-[#453C33] rounded-lg p-2.5 text-[#F7F4EE] focus:border-[#C98A5B] outline-none">

                  <option value="bn">বাংলা (Bengali Official Draft)</option>

                  <option value="en">English (Official English Draft)</option>

                </select>"""

new_grv_lang = """                <select id="grvLang" class="w-full bg-[#141210] border border-[#453C33] rounded-lg p-2.5 text-[#F7F4EE] focus:border-[#C98A5B] outline-none">

                  <option value="bn" data-i18n="grv_opt_lang_bn">বাংলা (Bengali Official Draft)</option>

                  <option value="en" data-i18n="grv_opt_lang_en">English (Official English Draft)</option>

                  <option value="hi" data-i18n="grv_opt_lang_hi">हिन्दी (Hindi Official Draft)</option>

                </select>"""

content = safe_replace(content, old_grv_lang, new_grv_lang)

content = safe_replace(content,
    '<span>তথ্য সংশোধন (Edit Details)</span>',
    '<span data-i18n="grv_btn_edit">তথ্য সংশোধন (Edit Details)</span>'
)
content = safe_replace(content,
    '<span class="font-semibold">পশ্চিমবঙ্গ প্রশাসনিক নাগরিক সহায়তা উদ্যোগ (Citizen Representation Format)</span>',
    '<span class="font-semibold" data-i18n="grv_doc_header">পশ্চিমবঙ্গ প্রশাসনিক নাগরিক সহায়তা উদ্যোগ (Citizen Representation Format)</span>'
)
content = safe_replace(content,
    '<span>নতুন দরখাস্ত তৈরি করুন (New Draft)</span>',
    '<span data-i18n="grv_btn_new_draft">নতুন দরখাস্ত তৈরি করুন (New Draft)</span>'
)
content = safe_replace(content,
    '<span>উইন্ডো বন্ধ করুন (Close)</span>',
    '<span data-i18n="grv_btn_close_window">উইন্ডো বন্ধ করুন (Close)</span>'
)

# 7. BDO / SDO Directory Modal
content = safe_replace(content,
    '<span>স্বয়ংক্রিয় GPS লোকেশন সনাক্তকরণ (Live GPS Detection)</span>',
    '<span data-i18n="off_gps_title">স্বয়ংক্রিয় GPS লোকেশন সনাক্তকরণ (Live GPS Detection)</span>'
)
content = safe_replace(content,
    '<p id="geoStatusMsg" class="text-[11px] text-[#A39788] mt-0.5">ডিভাইসের লোকেশন অন করে আপনার নিকটবর্তী BDO (গ্রাম) ও SDO (পৌরসভা/শহর) অফিস এক ক্লিকে চিহ্নিত করুন।</p>',
    '<p id="geoStatusMsg" class="text-[11px] text-[#A39788] mt-0.5" data-i18n="off_gps_sub">ডিভাইসের লোকেশন অন করে আপনার নিকটবর্তী BDO (গ্রাম) ও SDO (পৌরসভা/শহর) অফিস এক ক্লিকে চিহ্নিত করুন।</p>'
)
content = safe_replace(content,
    '<span id="btnDetectLocationText">লাইভ লোকেশন সক্ষম করুন (Find Nearest BDO / SDO)</span>',
    '<span id="btnDetectLocationText" data-i18n="off_btn_detect_text">লাইভ লোকেশন সক্ষম করুন (Find Nearest BDO / SDO)</span>'
)
content = safe_replace(content,
    '<span class="text-[11px] text-[#DDD5C7] font-semibold">দপ্তরের ধরন (Filter):</span>',
    '<span class="text-[11px] text-[#DDD5C7] font-semibold" data-i18n="off_filter_lbl">দপ্তরের ধরন (Filter):</span>'
)
content = safe_replace(content,
    '<button id="filterAllOffices" type="button" class="px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#C98A5B] text-[#141210] transition-colors cursor-pointer">সকল দপ্তর (All)</button>',
    '<button id="filterAllOffices" type="button" class="px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#C98A5B] text-[#141210] transition-colors cursor-pointer" data-i18n="off_filter_all">সকল দপ্তর (All)</button>'
)
content = safe_replace(content,
    '<span>🏢 মহকুমা শাসক (SDO) — পৌরসভা/শহর</span>',
    '<span data-i18n="off_filter_sdo">🏢 মহকুমা শাসক (SDO) — পৌরসভা/শহর</span>'
)
content = safe_replace(content,
    '<span>🏛️ ব্লক উন্নয়ন (BDO) — গ্রাম পঞ্চায়েত</span>',
    '<span data-i18n="off_filter_bdo">🏛️ ব্লক উন্নয়ন (BDO) — গ্রাম পঞ্চায়েত</span>'
)
content = safe_replace(content,
    '<label class="block text-[11px] font-semibold text-[#DDD5C7] mb-1">পশ্চিমবঙ্গের জেলা নির্বাচন করুন (District):</label>',
    '<label class="block text-[11px] font-semibold text-[#DDD5C7] mb-1" data-i18n="off_dist_lbl">পশ্চিমবঙ্গের জেলা নির্বাচন করুন (District):</label>'
)
content = safe_replace(content,
    '<option value="">পশ্চিমবঙ্গের সব জেলা (All 23 Districts)</option>',
    '<option value="" data-i18n="off_dist_all">পশ্চিমবঙ্গের সব জেলা (All 23 Districts)</option>'
)
content = safe_replace(content,
    '<label class="block text-[11px] font-semibold text-[#DDD5C7] mb-1">ব্লক, শহর বা এলাকার নাম দিয়ে খুঁজুন (Search by Area):</label>',
    '<label class="block text-[11px] font-semibold text-[#DDD5C7] mb-1" data-i18n="off_search_area_lbl">ব্লক, শহর বা এলাকার নাম দিয়ে খুঁজুন (Search by Area):</label>'
)
content = safe_replace(content,
    '<span>আপনার অবস্থানের ভিত্তিতে প্রস্তাবিত দপ্তরসমূহ (Recommended for You):</span>',
    '<span data-i18n="off_rec_title">আপনার অবস্থানের ভিত্তিতে প্রস্তাবিত দপ্তরসমূহ (Recommended for You):</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#A39788]">পৌরসভা অথবা পঞ্চায়েত এলাকা অনুযায়ী বেছে নিন</span>',
    '<span class="text-[10px] text-[#A39788]" data-i18n="off_rec_sub">পৌরসভা অথবা পঞ্চায়েত এলাকা অনুযায়ী বেছে নিন</span>'
)
content = safe_replace(content,
    '<span id="heroJurisdictionTag">চিহ্নিত দায়িত্বপ্রাপ্ত প্রশাসনিক দপ্তর</span>',
    '<span id="heroJurisdictionTag" data-i18n="off_jurisdiction_tag">চিহ্নিত দায়িত্বপ্রাপ্ত প্রশাসনিক দপ্তর</span>'
)
content = safe_replace(content,
    '<span>দূরত্ব গণনা করুন</span>',
    '<span data-i18n="off_calc_dist">দূরত্ব গণনা করুন</span>'
)
content = safe_replace(content,
    '<span>কাজের সময়: সোম-শুক্র (১০:০০ AM - ৫:০০ PM)</span>',
    '<span data-i18n="off_work_hours">কাজের সময়: সোম-শুক্র (১০:০০ AM - ৫:০০ PM)</span>'
)
content = safe_replace(content,
    '<span>গুগল ম্যাপে পথ ও দূরত্ব দেখুন (Google Maps)</span>',
    '<span data-i18n="off_btn_maps">গুগল ম্যাপে পথ ও দূরত্ব দেখুন (Google Maps)</span>'
)
content = safe_replace(content,
    '<span>এই অফিসে দরখাস্ত লিখুন (Draft Grievance)</span>',
    '<span data-i18n="off_btn_draft">এই অফিসে দরখাস্ত লিখুন (Draft Grievance)</span>'
)
content = safe_replace(content,
    '<span>ভৌগোলিক মানচিত্র ও নেভিগেশন (Interactive Map)</span>',
    '<span data-i18n="off_map_title">ভৌগোলিক মানচিত্র ও নেভিগেশন (Interactive Map)</span>'
)
content = safe_replace(content,
    '<span class="text-[10px] text-[#A39788]">🔵 আপনার স্থান | 🏢 SDO দপ্তর | 🏛️ BDO দপ্তর</span>',
    '<span class="text-[10px] text-[#A39788]" data-i18n="off_map_legend">🔵 আপনার স্থান | 🏢 SDO দপ্তর | 🏛️ BDO দপ্তর</span>'
)
content = safe_replace(content,
    '<span>পশ্চিমবঙ্গের BDO ও SDO অফিসের সম্পূর্ণ তালিকা:</span>',
    '<span data-i18n="off_list_title">পশ্চিমবঙ্গের BDO ও SDO অফিসের সম্পূর্ণ তালিকা:</span>'
)

# 8. Auth Modal
content = safe_replace(content,
    '<h3 class="font-headline font-bold text-lg text-[#F7F4EE]">নাগরিক পোর্টাল (Citizen Portal)</h3>',
    '<h3 class="font-headline font-bold text-lg text-[#F7F4EE]" data-i18n="auth_modal_title">নাগরিক পোর্টাল (Citizen Portal)</h3>'
)
content = safe_replace(content,
    '<p class="text-[11px] text-[#A39788]">Supabase সিকিওর লগইন ও ড্রাফট সংরক্ষণ</p>',
    '<p class="text-[11px] text-[#A39788]" data-i18n="auth_modal_sub">Supabase সিকিওর লগইন ও ড্রাফট সংরক্ষণ</p>'
)
content = safe_replace(content,
    '<span class="font-bold text-[#F2CBA5]">গেস্ট মোড সক্রিয়:</span>',
    '<span class="font-bold text-[#F2CBA5]" data-i18n="auth_guest_title">গেস্ট মোড সক্রিয়:</span>'
)
content = safe_replace(content,
    '<span>প্রকল্প খোঁজা, যোগ্যতা যাচাই ও নোটিশ বিশ্লেষণ সম্পূর্ণ বিনামূল্যে বিনা লগইনেই করা সম্ভব।</span>',
    '<span data-i18n="auth_guest_desc">প্রকল্প খোঁজা, যোগ্যতা যাচাই ও নোটিশ বিশ্লেষণ সম্পূর্ণ বিনামূল্যে বিনা লগইনেই করা সম্ভব।</span>'
)
content = safe_replace(content,
    '<label class="block text-xs font-label text-[#DDD5C7] mb-1 font-semibold">মোবাইল নম্বর (Mobile OTP Login):</label>',
    '<label class="block text-xs font-label text-[#DDD5C7] mb-1 font-semibold" data-i18n="auth_mobile_lbl">মোবাইল নম্বর (Mobile OTP Login):</label>'
)
content = safe_replace(content,
    '<div class="text-center text-[11px] text-[#A39788]">— অথবা সরাসরি গুগল দিয়ে —</div>',
    '<div class="text-center text-[11px] text-[#A39788]" data-i18n="auth_or_google">— অথবা সরাসরি গুগল দিয়ে —</div>'
)
content = safe_replace(content,
    '<span>Google একাউন্ট দিয়ে লগইন করুন</span>',
    '<span data-i18n="auth_btn_google">Google একাউন্ট দিয়ে লগইন করুন</span>'
)
content = safe_replace(content,
    '<span>হোয়াইট ও গোল্ডেন লগইন পেইজে যান (Login Page)</span>',
    '<span data-i18n="auth_link_login">হোয়াইট ও গোল্ডেন লগইন পেইজে যান (Login Page)</span>'
)
content = safe_replace(content,
    '<span>নতুন নাগরিক নিবন্ধন (Register Page)</span>',
    '<span data-i18n="auth_link_register">নতুন নাগরিক নিবন্ধন (Register Page)</span>'
)

# 9. Helplines & Footer
content = safe_replace(content,
    '<li><span class="font-semibold text-[#E2A97B] block">মুখ্যমন্ত্রী গ্রিভেন্স সেল (Didi ke Bolo):</span> 9137091370 / ১৮০০-৩৪৫-৫৫৮৮</li>',
    '<li><span class="font-semibold text-[#E2A97B] block" data-i18n="hl_cm_label">মুখ্যমন্ত্রী গ্রিভেন্স সেল (Didi ke Bolo):</span> 9137091370 / ১৮০০-৩৪৫-৫৫৮৮</li>'
)
content = safe_replace(content,
    '<li><span class="font-semibold text-[#E2A97B] block">দুয়ারে সরকার কন্ট্রোল রুম:</span> ১৮০০-৩৪৫-০১১১</li>',
    '<li><span class="font-semibold text-[#E2A97B] block" data-i18n="hl_ds_label">দুয়ারে সরকার কন্ট্রোল রুম:</span> ১৮০০-৩৪৫-০১১১</li>'
)
content = safe_replace(content,
    '<li><span class="font-semibold text-[#E2A97B] block">জাতীয় আইনি সেবা (NALSA Toll-Free):</span> ১৫১০০ (24x7 বিনামূল্যে আইনি সহায়তা)</li>',
    '<li><span class="font-semibold text-[#E2A97B] block" data-i18n="hl_nalsa_label">জাতীয় আইনি সেবা (NALSA Toll-Free):</span> ১৫১০০ (24x7 বিনামূল্যে আইনি সহায়তা)</li>'
)
content = safe_replace(content,
    '<li><span class="font-semibold text-[#E2A97B] block">মহিলা সহায়তা হেল্পলাইন:</span> ১৮১ / ১০৯১</li>',
    '<li><span class="font-semibold text-[#E2A97B] block" data-i18n="hl_women_label">মহিলা সহায়তা হেল্পলাইন:</span> ১৮১ / ১০৯১</li>'
)
content = safe_replace(content,
    '<p class="text-xs leading-relaxed text-[#A39788] font-body">কোনো আবেদনের চূড়ান্ত প্রক্রিয়াকরণের জন্য সর্বদা নিকটস্থ স্থানীয় কর্তৃপক্ষের সাথে যোগাযোগ করুন:</p>',
    '<p class="text-xs leading-relaxed text-[#A39788] font-body" data-i18n="hl_local_head">কোনো আবেদনের চূড়ান্ত প্রক্রিয়াকরণের জন্য সর্বদা নিকটস্থ স্থানীয় কর্তৃপক্ষের সাথে যোগাযোগ করুন:</p>'
)
content = safe_replace(content,
    '<li>• ব্লক উন্নয়ন আধিকারিক (BDO Office)</li>',
    '<li data-i18n="hl_bdo_line">• ব্লক উন্নয়ন আধিকারিক (BDO Office)</li>'
)
content = safe_replace(content,
    '<li>• মহকুমা শাসক কার্যালয় (SDO Office)</li>',
    '<li data-i18n="hl_sdo_line">• মহকুমা শাসক কার্যালয় (SDO Office)</li>'
)
content = safe_replace(content,
    '<li>• গ্রাম পঞ্চায়েত তথ্যমিত্র কেন্দ্র (CSC)</li>',
    '<li data-i18n="hl_csc_line">• গ্রাম পঞ্চায়েত তথ্যমিত্র কেন্দ্র (CSC)</li>'
)
content = safe_replace(content,
    '<li>• বাংলা সহায়তা কেন্দ্র (BSK)</li>',
    '<li data-i18n="hl_bsk_line">• বাংলা সহায়তা কেন্দ্র (BSK)</li>'
)
content = safe_replace(content,
    '<span>ফন্ট সাইজ:',
    '<span data-i18n="footer_font_size">ফন্ট সাইজ:'
)

# 10. Update generateOfflineLetter in Home.html to support bn, en, and hi
old_offline_fn_start = "    function generateOfflineLetter(data) {"
old_offline_fn_end = "    // View Switching Functions"

idx_off_start = content.find(old_offline_fn_start)
idx_off_end = content.find(old_offline_fn_end, idx_off_start)

if idx_off_start != -1 and idx_off_end != -1:
    new_offline_letter = """    function generateOfflineLetter(data) {

      const today = new Date();
      const day = String(today.getDate()).padStart(2, '0');
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const year = today.getFullYear();
      const todayStr = `${day}/${month}/${year}`;

      const scheme = data.scheme_name || 'লক্ষ্মীর ভাণ্ডার';
      const name = data.applicant_name || 'আবেদনকারী';
      const phone = data.contact_phone || 'N/A';
      const address = data.residence_address || 'পশ্চিমবঙ্গ';
      const refNo = data.application_ref_no || 'N/A';
      const facts = data.facts_statement || '';
      const gType = data.grievance_type || 'delay';
      const lang = data.language || localStorage.getItem('nyayasetu_lang') || 'bn';

      if (lang === 'hi') {
        const subjectMap = {
          'delay': `${scheme} के आवेदन की स्वीकृति एवं सहायता राशि में अत्यधिक विलंब के संबंध में आवेदन।`,
          'rejection_review': `${scheme} के आवेदन पर पुनर्विचार एवं दस्तावेज़ पुनः सत्यापन हेतु सविनय प्रार्थना।`,
          'dbt_failure': `${scheme} की किस्त बैंक खाते में न आने / डीबीटी (DBT/NPCI) विफलता के समाधान हेतु आवेदन।`,
          'correction': `${scheme} के आवेदन में बैंक खाता अथवा व्यक्तिगत विवरण सुधारने हेतु आवेदन।`
        };
        const subject = subjectMap[gType] || `${scheme} संबंधित विषय में आवेदन।`;
        const defaultFacts = 'आवेदन जमा किए जाने के पश्चात लंबा समय बीत जाने के बावजूद अभी तक योजना का लाभ अथवा स्पष्ट समाधान प्राप्त नहीं हुआ है।';

        return `दिनांक: ${todayStr}

सेवा में,
माननीय प्रखंड विकास पदाधिकारी (BDO) महोदय / अनुमंडल पदाधिकारी (SDO) महोदय,

विषय: ${subject}

आदरणीय महोदय / महोदया,

सविनय निवेदन है कि मैं अधोहस्ताक्षरी ${name}, पिता/पति: ............................, ग्राम/वार्ड: ${address || '............................'} का/की स्थायी निवासी हूँ।

मैंने ${scheme} के लाभ हेतु सभी आवश्यक एवं वैध दस्तावेज़ों के साथ आवेदन प्रस्तुत किया था। मेरे आवेदन की पावती (Acknowledgement / Ref) संख्या: ${refNo || '............................'} है।

मेरी वर्तमान समस्या निम्नलिखित है:
${facts || defaultFacts}

मैं यह प्रमाणित करता/करती हूँ कि मैं उक्त सरकारी योजना के सभी निर्धारित पात्रता मानदंडों को पूर्ण करता/करती हूँ। इस पत्र के साथ मेरे सभी आवश्यक दस्तावेज़ (आधार कार्ड, बैंक पासबुक, मूल आवेदन पावती रसीद) संलग्न हैं।

अतः आपसे विनम्र प्रार्थना है कि कृपया मेरे आवेदन पत्र की वर्तमान स्थिति की जांच कर शीघ्र सहायता व प्रशासनिक स्वीकृति प्रदान करने की कृपा करें।

सधन्यवाद,

भवदीय / भवदीया,

हस्ताक्षर: ........................................
नाम: ${name}
मोबाइल नंबर: ${phone}
पता: ${address}

संलग्नक:
१. मूल आवेदन पत्र की पावती रसीद (Acknowledgement Receipt)।
२. आधार कार्ड की स्व-सत्यापित छायाप्रति।
৩. बैंक पासबुक के प्रथम पृष्ठ की स्पष्ट छायाप्रति।`;

      } else if (lang === 'bn') {
        const subjectMap = {
          'delay': `${scheme} প্রকল্পের আবেদন মঞ্জুর ও সহায়তা প্রদানের বিলম্ব প্রসঙ্গে আবেদন।`,
          'rejection_review': `${scheme} প্রকল্পের আবেদন পুনর্বিবেচনা ও তথ্য যাচাইকরণের বিনীত প্রার্থনা।`,
          'dbt_failure': `${scheme} প্রকল্পের ব্যাংক অ্যাকাউন্টে কিস্তির টাকা না আসা / ডিবিটি সমস্যা সমাধানের আবেদন।`,
          'correction': `${scheme} প্রকল্পের আবেদনে ব্যাংক/ব্যক্তিগত তথ্য সংশোধনের আবেদন।`
        };
        const subject = subjectMap[gType] || `${scheme} প্রকল্প সম্পর্কিত বিষয়ে আবেদন।`;
        const defaultFacts = 'আবেদন জমা দেওয়ার দীর্ঘদিন অতিবাহিত হওয়া সত্ত্বেও অদ্যাবধি কোনো সন্তোষজনক অগ্রগতি বা সহায়তা প্রাপ্তি ঘটেনি।';

        return `তারিখ: ${todayStr}

প্রতি,
মাননীয় সমষ্টি উন্নয়ন আধিকারিক (BDO) মহাশয় সমীপেষু,

বিষয়: ${subject}

মহাশয়,
বিনীত নিবেদন এই যে, আমি নিম্নস্বাক্ষরকারী ${name}, পিতা/স্বামী: ............................, গ্রাম/ওয়ার্ড: ${address || '............................'} এর স্থায়ী বাসিন্দা।

আমি ${scheme} প্রকল্পের সুবিধার জন্য যথাযথ নথিপত্র সহ আবেদন জমা দিয়েছিলাম। আমার আবেদন পত্রের প্রাপ্তিস্বীকার (Acknowledgement / Ref) নম্বর হলো: ${refNo || '............................'}।

আমার বর্তমান সমস্যাটি নিম্নরূপ:
${facts || defaultFacts}

আমি নিশ্চিত করছি যে, আমি উক্ত প্রকল্পের নির্দেশিকা অনুযায়ী সমস্ত প্রয়োজনীয় যোগ্যতা পূরণ করি এবং এই পত্রের সাথে আমার প্রয়োজনীয় সমস্ত নথিপত্র (আধার কার্ড, ব্যাংক পাসবুক, আবেদন রশিদ) সংযুক্ত করলাম।

অতএব, মহাশয়ের নিকট আমার সনির্বন্ধ প্রার্থনা, দয়া করে আমার আবেদনপত্রটির বর্তমান অবস্থা খতিয়ে দেখে দ্রুত প্রয়োজনীয় পদক্ষেপ গ্রহণ করতে আজ্ঞা হয়।

ধন্যবাদান্তে,

বিনীত,
স্বাক্ষর: ........................................
নাম: ${name}
মোবাইল নম্বর: ${phone}
ঠিকানা: ${address}

সংযুক্তি:
১. মূল আবেদন পত্রের প্রাপ্তিস্বীকার রশিদের প্রতিলিপি।
২. আধার কার্ডের প্রতিলিপি।
৩. ব্যাংক পাসবুকের প্রথম পাতার প্রতিলিপি।`;

      } else {
        // English
        const subjectMap = {
          'delay': `Representation regarding inordinate delay in processing / sanction of ${scheme} application.`,
          'rejection_review': `Prayer for re-verification and reconsideration of ${scheme} application.`,
          'dbt_failure': `Intimation regarding non-receipt of installment / DBT failure under ${scheme}.`,
          'correction': `Prayer for correction of personal / bank account particulars under ${scheme}.`
        };
        const subject = subjectMap[gType] || `Representation regarding application under ${scheme}.`;
        const defaultFacts = 'Despite the lapse of considerable time, the benefit/status has not been updated or resolved.';

        return `Date: ${todayStr}

To,
The Block Development Officer (BDO) / Sub-Divisional Officer (SDO),

Subject: ${subject}

Respected Sir/Madam,

I, the undersigned, ${name}, residing at ${address || '[Address]'}, would like to submit the following facts for your kind consideration:

1. That I applied for the benefit under the ${scheme} scheme having Acknowledgement / Reference No: ${refNo || '[Application Reference No]'}, fulfilling all requisite eligibility norms.

2. Brief statement of facts/issue:
${facts || defaultFacts}

3. I have enclosed photocopies of all requisite documents, including my Aadhaar card, bank passbook, and the original acknowledgement slip for your immediate perusal.

In view of the above circumstances, I earnestly request your good office to kindly look into the matter and initiate necessary administrative steps to expedite my application.

Thanking you.

Yours faithfully,

Signature: __________________________
Name: ${name}
Mobile No: ${phone}
Address: ${address}

Enclosures:
1. Copy of Application Acknowledgement Slip.
2. Self-attested copy of Aadhaar Card.
3. Copy of Bank Passbook front page.`;
      }
    }
"""
    content = content[:idx_off_start] + new_offline_letter + "\n\n" + content[idx_off_end:]

with open('frontend/Home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Home.html tags and letter generator updated successfully!")
