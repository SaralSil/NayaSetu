with open('frontend/GrievanceDrafter.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Hindi radio button to language selection in form
old_radios = """                  <div class="flex items-center gap-4">

                    <label class="inline-flex items-center gap-2 text-xs font-body cursor-pointer">

                      <input checked class="accent-[#C98A5B]" name="letterLang" onchange="toggleLanguage('bn')" type="radio" value="bn"/>

                      <span class="font-bold text-[#F7F4EE]">বাংলা (আদর্শ প্রশাসনিক প্রথা)</span>

                    </label>

                    <label class="inline-flex items-center gap-2 text-xs font-body cursor-pointer">

                      <input class="accent-[#C98A5B]" name="letterLang" onchange="toggleLanguage('en')" type="radio" value="en"/>

                      <span class="text-[#A39788] hover:text-[#F7F4EE]">English Representation</span>

                    </label>

                  </div>"""

new_radios = """                  <div class="flex flex-wrap items-center gap-4">

                    <label class="inline-flex items-center gap-2 text-xs font-body cursor-pointer">

                      <input checked class="accent-[#C98A5B]" name="letterLang" onchange="toggleLanguage('bn')" type="radio" value="bn"/>

                      <span class="font-bold text-[#F7F4EE]">বাংলা (আদর্শ প্রশাসনিক প্রথা)</span>

                    </label>

                    <label class="inline-flex items-center gap-2 text-xs font-body cursor-pointer">

                      <input class="accent-[#C98A5B]" name="letterLang" onchange="toggleLanguage('en')" type="radio" value="en"/>

                      <span class="text-[#A39788] hover:text-[#F7F4EE]">English Representation</span>

                    </label>

                    <label class="inline-flex items-center gap-2 text-xs font-body cursor-pointer">

                      <input class="accent-[#C98A5B]" name="letterLang" onchange="toggleLanguage('hi')" type="radio" value="hi"/>

                      <span class="text-[#A39788] hover:text-[#F7F4EE]">हिन्दी आवेदन (Hindi)</span>

                    </label>

                  </div>"""

content = content.replace(old_radios.replace('\r\n', '\n'), new_radios.replace('\r\n', '\n'))
content = content.replace(old_radios, new_radios)

# 2. Add IDs to the preview template elements
content = content.replace(
    '<span class="text-[10px] uppercase font-mono tracking-widest text-[#B87B4C] font-bold">পশ্চিমবঙ্গ প্রশাসনিক আনুষ্ঠানিক আবেদন • অফিশিয়াল ফরম্যাট</span>',
    '<span id="previewHeaderRibbon" class="text-[10px] uppercase font-mono tracking-widest text-[#B87B4C] font-bold">পশ্চিমবঙ্গ প্রশাসনিক আনুষ্ঠানিক আবেদন • অফিশিয়াল ফরম্যাট</span>'
)

content = content.replace(
    'তারিখ: <span class="font-bold text-stone-900" id="previewDate">১৫ মার্চ, ২০২৫</span>',
    '<span id="previewDateLabel">তারিখ:</span> <span class="font-bold text-stone-900" id="previewDate">১৫ মার্চ, ২০২৫</span>'
)

content = content.replace(
    'স্থান: <span id="previewPlace">কালনা, পূর্ব বর্ধমান</span>',
    '<span id="previewPlaceLabel">স্থান:</span> <span id="previewPlace">কালনা, পূর্ব বর্ধমান</span>'
)

content = content.replace(
    '<p class="font-bold text-stone-800">প্রতি,</p>',
    '<p id="previewToLabel" class="font-bold text-stone-800">প্রতি,</p>'
)

content = content.replace(
    '<span class="underline decoration-[#C98A5B] font-bold text-[#B87B4C]">বিষয়:</span>',
    '<span id="previewSubjLabel" class="underline decoration-[#C98A5B] font-bold text-[#B87B4C]">বিষয়:</span>'
)

content = content.replace(
    '<p class="font-bold text-stone-900">মহাশয়,</p>',
    '<p id="previewSalutation" class="font-bold text-stone-900">মহাশয়,</p>'
)

content = content.replace(
    '<p class="leading-relaxed font-medium text-stone-900">\n\n                    অতএব মহাশয়ের নিকট সনির্বন্ধ প্রার্থনা, অনুগ্রহপূর্বক আমার উপরিউক্ত আবেদনপত্র ও সংযুক্ত ব্যাঙ্ক নথিসমূহ পুনঃযাচাই করিয়া পোর্টালে ব্যাঙ্ক DBT ডেটা পুনরায় সচল (Re-trigger Disbursement) করার যথাযথ প্রশাসনিক আদেশ জারি করিতে আপনার সদয় মর্জি হয়।\n\n                  </p>',
    '<p class="leading-relaxed font-medium text-stone-900" id="previewConclusion">\n\n                    অতএব মহাশয়ের নিকট সনির্বন্ধ প্রার্থনা, অনুগ্রহপূর্বক আমার উপরিউক্ত আবেদনপত্র ও সংযুক্ত ব্যাঙ্ক নথিসমূহ পুনঃযাচাই করিয়া পোর্টালে ব্যাঙ্ক DBT ডেটা পুনরায় সচল (Re-trigger Disbursement) করার যথাযথ প্রশাসনিক আদেশ জারি করিতে আপনার সদয় মর্জি হয়।\n\n                  </p>'
)

content = content.replace(
    'সংযোজনীসমূহ (Documents Attached):',
    '<span id="previewAttachTitle">সংযোজনীসমূহ (Documents Attached):</span>'
)

content = content.replace(
    '<ol class="list-decimal list-inside space-y-1 text-stone-700 font-body pl-1">',
    '<ol id="previewAttachList" class="list-decimal list-inside space-y-1 text-stone-700 font-body pl-1">'
)

content = content.replace(
    '<p class="text-xs font-semibold text-stone-600">বিনীত,</p>',
    '<p id="previewSignGreeting" class="text-xs font-semibold text-stone-600">বিনীত,</p>'
)

content = content.replace(
    '<p class="text-xs text-stone-500 italic">(আবেদনকারীর স্বাক্ষর)</p>',
    '<p id="previewSignLabel" class="text-xs text-stone-500 italic">(আবেদনকারীর স্বাক্ষর)</p>'
)

# 3. Replace langHeaderHi listener
old_hi_listener = """    document.getElementById('langHeaderHi').addEventListener('click', () => {

      showToast('হিন্দি ভাষা শীঘ্রই উপলব্ধ হবে (Bengali/English available)');

    });"""

new_hi_listener = """    document.getElementById('langHeaderHi').addEventListener('click', () => {

      const hiRadio = document.querySelector('input[name="letterLang"][value="hi"]');

      if (hiRadio) hiRadio.checked = true;

      toggleLanguage('hi');

      showToast('आवेदन की भाषा हिन्दी पर सेट की गई है।', 'translate');

    });"""

content = content.replace(old_hi_listener.replace('\r\n', '\n'), new_hi_listener.replace('\r\n', '\n'))
content = content.replace(old_hi_listener, new_hi_listener)

with open('frontend/GrievanceDrafter.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("GrievanceDrafter.html HTML structure patched successfully!")
