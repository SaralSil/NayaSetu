import re
import sys

with open('frontend/Landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Original HTML length:", len(html))

# =========================================================================
# 1. Update Search AI button
# =========================================================================
# Old:
# <span>AI জিজ্ঞাসা</span>
# New:
# <span data-i18n="search_ai_btn">AI জিজ্ঞাসা</span>
html = re.sub(
    r'(<span class="material-symbols-outlined text-base font-bold">smart_toy</span>\s*)<span>AI জিজ্ঞাসা</span>',
    r'\1<span data-i18n="search_ai_btn">AI জিজ্ঞাসা</span>',
    html
)

# =========================================================================
# 2. Update Popular Search Chips
# =========================================================================
# Let's replace the chips container with data-i18n attributes
old_chips_pattern = re.compile(
    r'<div class="flex items-center flex-wrap gap-2 pt-1">[\s\S]*?<button class="chip-btn[^"]*?" data-search="Lakshmir Bhandar">[\s\S]*? আধার লিঙ্ক \(NPCI/DBT\)</span>[\s\S]*?</button>\s*</div>',
    re.MULTILINE
)

new_chips_html = """<div class="flex items-center flex-wrap gap-2 pt-1">
              <span class="text-xs text-[#A39788] font-bold shrink-0 flex items-center gap-1" data-i18n="pop_search">জনপ্রিয় অনুসন্ধান:</span>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs flex items-center gap-1.5" data-search="Lakshmir Bhandar" data-i18n="chip_1">
                <span>অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>
                <span class="text-[10px] text-[#F2CBA5]">₹৩০০০/মাস</span>
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs flex items-center gap-1.5" data-search="Yuva Shakti" data-i18n="chip_2">
                <span>যুব শক্তি যোজনা</span>
                <span class="text-[10px] text-[#F2CBA5]">₹২০০০-₹৩০০০</span>
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs flex items-center gap-1.5" data-search="Ayushman Bharat" data-i18n="chip_3">
                <span>আয়ুষ্মান ভারত</span>
                <span class="text-[10px] text-[#F2CBA5]">₹৫L + ৭০+ ফ্রি</span>
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs flex items-center gap-1.5" data-search="Krishak Bandhu" data-i18n="chip_4">
                <span>কৃষক বন্ধু</span>
                <span class="text-[10px] text-[#F2CBA5]">শস্য বীমা</span>
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs" data-search="Karmashree" data-i18n="chip_5">
                কর্মশ্রী ৫০ দিন
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs" data-search="Swasthya Sathi" data-i18n="chip_6">
                স্বাস্থ্য সাথী কার্ড
              </button>
              <button class="chip-btn px-3 py-1.5 rounded-full bg-[#2F2923] hover:bg-[#C98A5B] hover:text-[#141210] border border-[#453C33] text-[#F7F4EE] font-body transition-colors text-xs flex items-center gap-1" data-search="NPCI" data-i18n="chip_7">
                <span class="material-symbols-outlined text-[14px] text-[#E57373]">warning</span>
                <span>আধার লিঙ্ক (NPCI/DBT)</span>
              </button>
            </div>"""

if old_chips_pattern.search(html):
    html = old_chips_pattern.sub(new_chips_html, html)
    print("Popular chips updated with data-i18n")
else:
    print("Warning: old_chips_pattern did not match")

# =========================================================================
# 3. Update Bento Card 1, 2, 3, 4 Inner Elements
# =========================================================================
# Card 1 pills:
c1_old = """                  <div class="text-xs text-[#1C1917] font-body flex flex-wrap gap-2">



                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>



                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">যুব শক্তি যোজনা</span>



                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী</span>



                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">কৃষক বন্ধু ও শস্য বীমা</span>



                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs">কর্মশ্রী ও আবাস যোজনা</span>



                  </div>"""

c1_new = """                  <div class="text-xs text-[#1C1917] font-body flex flex-wrap gap-2">
                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="c1_p1">অন্নপূর্ণা / লক্ষ্মীর ভাণ্ডার</span>
                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="c1_p2">যুব শক্তি যোজনা</span>
                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="c1_p3">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী</span>
                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="c1_p4">কৃষক বন্ধু ও শস্য বীমা</span>
                    <span class="bg-[#FAF7F2] border border-[#D8C7B5] px-2.5 py-1 rounded-md text-[#292524] font-medium shadow-2xs" data-i18n="c1_p5">কর্মশ্রী ও আবাস যোজনা</span>
                  </div>"""

html = html.replace(c1_old, c1_new)

# Card 2 examples:
c2_old = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">



                    <div class="flex items-center gap-2">



                      <span class="w-1.5 h-1.5 rounded-full bg-[#C98A5B] inline-block"></span>



                      <span>'DBT Failed / Inactive Aadhaar' সংক্রান্ত সমস্যা সমাধান</span>



                    </div>



                    <div class="flex items-center gap-2">



                      <span class="w-1.5 h-1.5 rounded-full bg-[#C98A5B] inline-block"></span>



                      <span>ব্যাঙ্ক অ্যাকাউন্ট মিসম্যাচ সংশোধন নির্দেশ</span>



                    </div>



                  </div>"""

c2_new = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="w-1.5 h-1.5 rounded-full bg-[#C98A5B] inline-block"></span>
                      <span data-i18n="c2_ex1">'DBT Failed / Inactive Aadhaar' সংক্রান্ত সমস্যা সমাধান</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="w-1.5 h-1.5 rounded-full bg-[#C98A5B] inline-block"></span>
                      <span data-i18n="c2_ex2">ব্যাঙ্ক অ্যাকাউন্ট মিসম্যাচ সংশোধন নির্দেশ</span>
                    </div>
                  </div>"""

html = html.replace(c2_old, c2_new)

# Card 3 features:
c3_old = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">



                    <div class="flex items-center gap-2">



                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">check_circle</span>



                      <span>স্বাক্ষরের নির্দিষ্ট স্থান ও সংযুক্তি (Enclosures) তালিকা স্বয়ংক্রিয়ভাবে তৈরি</span>



                    </div>



                    <div class="flex items-center gap-2">



                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">check_circle</span>



                      <span>সরাসরি বাংলায় PDF বা এক ক্লিকে প্রিন্ট করার সুবিধা</span>



                    </div>



                  </div>"""

c3_new = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">check_circle</span>
                      <span data-i18n="c3_f1">স্বাক্ষরের নির্দিষ্ট স্থান ও সংযুক্তি (Enclosures) তালিকা স্বয়ংক্রিয়ভাবে তৈরি</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">check_circle</span>
                      <span data-i18n="c3_f2">সরাসরি বাংলায় PDF বা এক ক্লিকে প্রিন্ট করার সুবিধা</span>
                    </div>
                  </div>"""

html = html.replace(c3_old, c3_new)

# Card 4 features:
c4_old = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">



                    <div class="flex items-center gap-2">



                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">task_alt</span>



                      <span>স্বাস্থ্যসাথী কার্ড, আধার, ও একক ব্যাংক অ্যাকাউন্টের নির্দেশিকা</span>



                    </div>



                    <div class="flex items-center gap-2">



                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">task_alt</span>



                      <span>দুয়ারে সরকার ক্যাম্পে জমা দেওয়ার আগে সেলফ-অ্যাটেস্টেড নিয়ম</span>



                    </div>



                  </div>"""

c4_new = """                  <div class="text-xs text-[#DDD5C7] font-body space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">task_alt</span>
                      <span data-i18n="c4_ch1">স্বাস্থ্যসাথী কার্ড, আধার, ও একক ব্যাংক অ্যাকাউন্টের নির্দেশিকা</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-sm text-[#C98A5B]">task_alt</span>
                      <span data-i18n="c4_ch2">দুয়ারে সরকার ক্যাম্পে জমা দেওয়ার আগে সেলফ-অ্যাটেস্টেড নিয়ম</span>
                    </div>
                  </div>"""

html = html.replace(c4_old, c4_new)

# =========================================================================
# 4. Notice / SMS Explainer Sample Buttons & Dropzone
# =========================================================================
not_sample_old = """                <button type="button" id="noticeSampleAnnapurnaBtn" class="text-[11px] text-[#E2A97B] hover:text-[#F2CBA5] font-semibold hover:underline cursor-pointer flex items-center gap-0.5">



                  <span class="material-symbols-outlined text-[12px]">autorenew</span>



                  <span>অন্নপূর্ণা ভাণ্ডার নমুনা</span>



                </button>



                <span class="text-[#453C33]">•</span>



                <button type="button" id="noticeSampleKrishakBtn" class="text-[11px] text-[#E2A97B] hover:text-[#F2CBA5] font-semibold hover:underline cursor-pointer">



                  কৃষক বন্ধু নমুনা



                </button>"""

not_sample_new = """                <button type="button" id="noticeSampleAnnapurnaBtn" class="text-[11px] text-[#E2A97B] hover:text-[#F2CBA5] font-semibold hover:underline cursor-pointer flex items-center gap-0.5">
                  <span class="material-symbols-outlined text-[12px]">autorenew</span>
                  <span data-i18n="not_sample_annapurna">অন্নপূর্ণা ভাণ্ডার নমুনা</span>
                </button>
                <span class="text-[#453C33]">•</span>
                <button type="button" id="noticeSampleKrishakBtn" class="text-[11px] text-[#E2A97B] hover:text-[#F2CBA5] font-semibold hover:underline cursor-pointer">
                  <span data-i18n="not_sample_krishak">কৃষক বন্ধু নমুনা</span>
                </button>"""

html = html.replace(not_sample_old, not_sample_new)

# Dropzone titles:
dropzone_old = """              <p class="text-xs font-label font-bold text-[#F7F4EE]" id="noticeDropzoneTitle">আবেদনপত্র, নোটিশ স্লিপ বা স্ক্রিনশটের ছবি নির্বাচন করুন</p>



              <p class="text-[11px] text-[#A39788] mt-0.5 font-body">ছবি টেনে আনুন অথবা এখানে ক্লিক করে ছবি আপলোড করুন (JPG, PNG, WebP • সর্বোচ্চ ১০ এমবি)</p>"""

dropzone_new = """              <p class="text-xs font-label font-bold text-[#F7F4EE]" id="noticeDropzoneTitle" data-i18n="not_dropzone_title">আবেদনপত্র, নোটিশ স্লিপ বা স্ক্রিনশটের ছবি নির্বাচন করুন</p>
              <p class="text-[11px] text-[#A39788] mt-0.5 font-body" id="noticeDropzoneSub" data-i18n="not_dropzone_sub">ছবি টেনে আনুন অথবা এখানে ক্লিক করে ছবি আপলোড করুন (JPG, PNG, WebP • সর্বোচ্চ ১০ এমবি)</p>"""

html = html.replace(dropzone_old, dropzone_new)

# Remove image button in preview card:
not_remove_old = """                <span class="material-symbols-outlined text-sm">delete</span>



                <span>মুছুন</span>"""

not_remove_new = """                <span class="material-symbols-outlined text-sm">delete</span>
                <span data-i18n="not_btn_remove">মুছুন</span>"""

html = html.replace(not_remove_old, not_remove_new)

# =========================================================================
# 5. Grievance Drafter Scheme Dropdown Options & Result View
# =========================================================================
grv_sch_old = """                  <option value="অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার">অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার (Annapurna / Lakshmir Bhandar - ₹3,000/মাসিক)</option>



                  <option value="পশ্চিমবঙ্গ যুব শক্তি যোজনা">পশ্চিমবঙ্গ যুব শক্তি যোজনা (WB Yuva Shakti - ₹2,000-₹3,000/মাসিক)</option>



                  <option value="আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী (Ayushman Bharat & Swasthya Sathi)</option>



                  <option value="কর্মশ্রী প্রকল্প">কর্মশ্রী প্রকল্প (Karmashree 50-Day Guaranteed Work)</option>



                  <option value="কৃষক বন্ধু ও বাংলা শস্য বীমা">কৃষক বন্ধু ও বাংলা শস্য বীমা (Krishak Bandhu & BSB)</option>



                  <option value="বাংলার আবাস যোজনা">বাংলার আবাস যোজনা (Banglar Awas Yojana)</option>



                  <option value="ভবিষ্যৎ ক্রেডিট কার্ড">ভবিষ্যৎ ক্রেডিট কার্ড (Bhabishyat Credit Card - WBBCCS)</option>



                  <option value="রূপশ্রী প্রকল্প">রূপশ্রী প্রকল্প (Rupashree Prakalpa)</option>



                  <option value="কন্যাশ্রী প্রকল্প">কন্যাশ্রী প্রকল্প (Kanyashree Prakalpa)</option>



                  <option value="তরুণের স্বপ্ন">তরুণের স্বপ্ন (Taruner Swapno Tab Scheme)</option>



                  <option value="স্বামী বিবেকানন্দ স্কলারশিপ ও স্টুডেন্ট ক্রেডিট কার্ড">স্বামী বিবেকানন্দ স্কলারশিপ ও স্টুডেন্ট ক্রেডিট কার্ড (SVMCM & WBSCC)</option>



                  <option value="জয় জোহার ও তপশিলী বন্ধু">জয় জোহার ও তপশিলী বন্ধু (Jai Johar & Taposhili Bandhu Pension)</option>



                  <option value="মানবিক প্রতিবন্ধী ভাতা">মানবিক প্রতিবন্ধী ভাতা (Manabik Pension)</option>"""

grv_sch_new = """                  <option value="অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার" data-i18n="grv_sch_annapurna">অন্নপূর্ণা ভাণ্ডার / লক্ষ্মীর ভাণ্ডার (Annapurna / Lakshmir Bhandar - ₹3,000/মাসিক)</option>
                  <option value="পশ্চিমবঙ্গ যুব শক্তি যোজনা" data-i18n="grv_sch_yuva">পশ্চিমবঙ্গ যুব শক্তি যোজনা (WB Yuva Shakti - ₹2,000-₹3,000/মাসিক)</option>
                  <option value="আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী" data-i18n="grv_sch_ayushman">আয়ুষ্মান ভারত ও স্বাস্থ্য সাথী (Ayushman Bharat & Swasthya Sathi)</option>
                  <option value="কর্মশ্রী প্রকল্প" data-i18n="grv_sch_karmashree">কর্মশ্রী প্রকল্প (Karmashree 50-Day Guaranteed Work)</option>
                  <option value="কৃষক বন্ধু ও বাংলা শস্য বীমা" data-i18n="grv_sch_krishak">কৃষক বন্ধু ও বাংলা শস্য বীমা (Krishak Bandhu & BSB)</option>
                  <option value="বাংলার আবাস যোজনা" data-i18n="grv_sch_awas">বাংলার আবাস যোজনা (Banglar Awas Yojana)</option>
                  <option value="ভবিষ্যৎ ক্রেডিট কার্ড" data-i18n="grv_sch_bhabishyat">ভবিষ্যৎ ক্রেডিট কার্ড (Bhabishyat Credit Card - WBBCCS)</option>
                  <option value="রূপশ্রী প্রকল্প" data-i18n="grv_sch_rupashree">রূপশ্রী প্রকল্প (Rupashree Prakalpa)</option>
                  <option value="কন্যাশ্রী প্রকল্প" data-i18n="grv_sch_kanyashree">কন্যাশ্রী প্রকল্প (Kanyashree Prakalpa)</option>
                  <option value="তরুণের স্বপ্ন" data-i18n="grv_sch_tarun">তরুণের স্বপ্ন (Taruner Swapno Tab Scheme)</option>
                  <option value="স্বামী বিবেকানন্দ স্কলারশিপ ও স্টুডেন্ট ক্রেডিট কার্ড" data-i18n="grv_sch_scholarship">স্বামী বিবেকানন্দ স্কলারশিপ ও স্টুডেন্ট ক্রেডিট কার্ড (SVMCM & WBSCC)</option>
                  <option value="জয় জোহার ও তপশিলী বন্ধু" data-i18n="grv_sch_pension">জয় জোহার ও তপশিলী বন্ধু (Jai Johar & Taposhili Bandhu Pension)</option>
                  <option value="মানবিক প্রতিবন্ধী ভাতা" data-i18n="grv_sch_manabik">মানবিক প্রতিবন্ধী ভাতা (Manabik Pension)</option>"""

html = html.replace(grv_sch_old, grv_sch_new)

# Grievance Result View:
grv_res_old = """              <button id="editDetailsBtn" type="button" class="px-3 py-1.5 rounded-lg bg-[#28231E] hover:bg-[#332D26] border border-[#453C33] text-xs text-[#DDD5C7] hover:text-[#F7F4EE] flex items-center gap-1.5 transition-colors">



                <span class="material-symbols-outlined text-sm">edit</span>



                <span>তথ্য সংশোধন (Edit Details)</span>



              </button>"""

grv_res_new = """              <button id="editDetailsBtn" type="button" class="px-3 py-1.5 rounded-lg bg-[#28231E] hover:bg-[#332D26] border border-[#453C33] text-xs text-[#DDD5C7] hover:text-[#F7F4EE] flex items-center gap-1.5 transition-colors">
                <span class="material-symbols-outlined text-sm">edit</span>
                <span data-i18n="grv_btn_edit">তথ্য সংশোধন</span>
              </button>"""

html = html.replace(grv_res_old, grv_res_new)

# Ribbon in letter view:
grv_ribbon_old = """<span class="font-semibold">পশ্চিমবঙ্গ প্রশাসনিক নাগরিক সহায়তা উদ্যোগ (Citizen Representation Format)</span>"""
grv_ribbon_new = """<span class="font-semibold" data-i18n="grv_header_ribbon">পশ্চিমবঙ্গ প্রশাসনিক নাগরিক সহায়তা উদ্যোগ</span>"""
html = html.replace(grv_ribbon_old, grv_ribbon_new)

# Clean up wiz_btn_submit in initial HTML
html = html.replace(
    'data-i18n="wiz_btn_submit">যোগ্য প্রকল্পগুলি দেখুন (Check Matching Schemes)</span>',
    'data-i18n="wiz_btn_submit">যোগ্য প্রকল্পগুলি দেখুন</span>'
)

with open('frontend/Landing.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Landing.html elements updated successfully!")
