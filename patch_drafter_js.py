with open('frontend/GrievanceDrafter.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace toggleLanguage
old_toggle = """    function toggleLanguage(lang) {

      if (lang === 'en') {

        document.getElementById('previewPlace').innerText = 'Kalna, Purba Bardhaman';

        document.getElementById('previewDate').innerText = '15th March, 2025';

      } else {

        document.getElementById('previewPlace').innerText = 'কালনা, পূর্ব বর্ধমান';

        document.getElementById('previewDate').innerText = '১৫ মার্চ, ২০২৫';

      }

      updatePreview();

    }"""

new_toggle = """    function toggleLanguage(lang) {

      const today = new Date();
      const d = today.getDate();
      const m = today.getMonth() + 1;
      const y = today.getFullYear();

      if (lang === 'en') {
        const placeEl = document.getElementById('previewPlace');
        if (placeEl) placeEl.innerText = 'District Office, West Bengal';
        const dateEl = document.getElementById('previewDate');
        if (dateEl) dateEl.innerText = `${d}/${m}/${y}`;
      } else if (lang === 'hi') {
        const placeEl = document.getElementById('previewPlace');
        if (placeEl) placeEl.innerText = 'जिला कार्यालय, पश्चिम बंगाल';
        const dateEl = document.getElementById('previewDate');
        if (dateEl) dateEl.innerText = `${d}/${m}/${y}`;
      } else {
        const placeEl = document.getElementById('previewPlace');
        if (placeEl) placeEl.innerText = 'কালনা, পূর্ব বর্ধমান';
        const dateEl = document.getElementById('previewDate');
        if (dateEl) dateEl.innerText = `${d}/${m}/${y}`;
      }

      updatePreview();

    }"""

content = content.replace(old_toggle.replace('\r\n', '\n'), new_toggle.replace('\r\n', '\n'))
content = content.replace(old_toggle, new_toggle)

# Now update updatePreview()
# Find start of updatePreview() and end of updatePreview()
start_marker = "    function updatePreview() {"
end_marker = "      // Smooth visual ripple on legal preview"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_update_preview = """    function updatePreview() {

      const data = getFormData();
      const lang = data.lang || 'bn';

      // Update Applicant Name and details
      const pName = document.getElementById('previewName');
      if (pName) pName.innerText = data.applicantName;
      const pSig = document.getElementById('previewSigName');
      if (pSig) pSig.innerText = data.applicantName;
      const pGuard = document.getElementById('previewGuardian');
      if (pGuard) pGuard.innerText = data.guardianName;
      const pAddr = document.getElementById('previewAddress');
      if (pAddr) pAddr.innerText = data.address;
      const pPhone = document.getElementById('previewPhone');
      if (pPhone) pPhone.innerText = data.phone;
      const pAck = document.getElementById('previewAck');
      if (pAck) pAck.innerText = data.ack;
      const pRec = document.getElementById('previewRecipient');
      if (pRec) pRec.innerText = data.recipient;
      const pSch = document.getElementById('previewScheme');
      if (pSch) pSch.innerText = data.scheme;

      // Labels and Ribbons
      const ribbon = document.getElementById('previewHeaderRibbon');
      const dateLbl = document.getElementById('previewDateLabel');
      const placeLbl = document.getElementById('previewPlaceLabel');
      const toLbl = document.getElementById('previewToLabel');
      const subLbl = document.getElementById('previewSubjLabel');
      const salut = document.getElementById('previewSalutation');
      const offAddr = document.getElementById('previewOfficeAddress');
      const distLine = document.getElementById('previewDistrictLine');
      const body1 = document.getElementById('previewBody1');
      const dynamicBody = document.getElementById('previewBodyDynamic');
      const subjectEl = document.getElementById('previewSubject');
      const conclusion = document.getElementById('previewConclusion');
      const attachTitle = document.getElementById('previewAttachTitle');
      const attachList = document.getElementById('previewAttachList');
      const signGreeting = document.getElementById('previewSignGreeting');
      const signLabel = document.getElementById('previewSignLabel');

      if (lang === 'hi') {
        if (ribbon) ribbon.innerText = 'पश्चिम बंगाल प्रशासनिक नागरिक आवेदन • आधिकारिक प्रारूप';
        if (dateLbl) dateLbl.innerText = 'दिनांक:';
        if (placeLbl) placeLbl.innerText = 'स्थान:';
        if (toLbl) toLbl.innerText = 'सेवा में,';
        if (subLbl) subLbl.innerText = 'विषय:';
        if (salut) salut.innerText = 'आदरणीय महोदय / महोदया,';
        if (offAddr) offAddr.innerText = data.block + ' प्रखंड विकास कार्यालय,';
        if (distLine) distLine.innerText = data.district + ' जिला, पश्चिम बंगाल।';
        if (signGreeting) signGreeting.innerText = 'भवदीय / भवदीया,';
        if (signLabel) signLabel.innerText = '(आवेदक के हस्ताक्षर)';

        if (body1) {
          body1.innerHTML = `सविनय निवेदन है कि मैं <strong>${data.applicantName}</strong>, पिता/पति: <strong>${data.guardianName}</strong>, <strong>${data.address}</strong> का/की स्थायी निवासी हूँ। मैंने आपके प्रखंड के अंतर्गत दुआरे सरकार शिविर में सरकार की जनकल्याणकारी <strong>${data.scheme}</strong> योजना के तहत लाभ प्राप्ति हेतु आवश्यक दस्तावेज़ों सहित आवेदन जमा किया था (आवेदन पावती संदर्भ संख्या: <span class="font-mono font-bold bg-stone-100 border border-stone-300 px-1.5 py-0.5 rounded text-stone-900">${data.ack}</span>)।`;
        }

        if (data.issue === 'dbt_fail') {
          if (subjectEl) subjectEl.innerText = `${data.scheme} योजना (Ref: ${data.ack}) के तहत बैंक DBT/NPCI समस्या के कारण खाते में सहायता राशि न आने के संबंध में आवेदन।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              उक्त आवेदन के संदर्भ में पोर्टल पर स्वीकृति मिलने के उपरांत भी विगत कई महीनों से मेरे बैंक खाते में योजना की किस्त जमा नहीं हुई है। बैंक में संपर्क करने पर ज्ञात हुआ कि आधार डीबीटी एवं NPCI मैपिंग में तकनीकी त्रुटि के कारण सरकारी ट्रेजरी से भेजी गई राशि अस्वीकृत (Payment Failed) हो गई है।
            </p>
            <p class="leading-relaxed">
              वर्तमान में मैंने अपने एकल बैंक खाते (Single Account) में नया आधार सीडिंग एवं NPCI अधिदेश सफलतापूर्वक सक्रिय करा लिया है और बैंक प्रबंधक से सत्यापन पर्ची भी प्राप्त कर ली है।
            </p>
          `;
        } else if (data.issue === 'rejection') {
          if (subjectEl) subjectEl.innerText = `${data.scheme} योजना (Ref: ${data.ack}) के आवेदन को बिना किसी स्पष्ट कारण के निरस्त (Reject) किए जाने के विरुद्ध पुनर्विचार प्रार्थना।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              अत्यंत खेद के साथ सूचित करना पड़ रहा है कि पोर्टल पर स्टेटस जांच करने पर मेरा आवेदन पत्र बिना किसी वैध कारण के अस्वीकृत दिखाया जा रहा है। मेरे सभी आवश्यक दस्तावेज़ (आधार, वोटर, बैंक पासबुक एवं परिवार विवरण) वैध और नियमानुसार पूर्ण हैं।
            </p>
            <p class="leading-relaxed">
              सरकारी दिशानिर्देशों के अनुसार मैं इस योजना का पूर्ण रूप से पात्र नागरिक हूँ। अतः अस्वीकृति के कारणों की पुनः जांच कर पोर्टल में सुधार करने का कष्ट करें।
            </p>
          `;
        } else {
          if (subjectEl) subjectEl.innerText = `${data.scheme} योजना (Ref: ${data.ack}) के आवेदन की स्वीकृति में अत्यधिक विलंब एवं त्वरित समाधान हेतु आवेदन।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              मैंने काफी समय पूर्व (${data.appDate}) शिविर में संपूर्ण दस्तावेजों के साथ आवेदन जमा किया था। परंतु लंबा समय बीत जाने के बावजूद पोर्टल पर आवेदन अभी भी 'Pending at Block Level' दिख रहा है।
            </p>
            <p class="leading-relaxed">
              आर्थिक स्थिति को ध्यान में रखते हुए यह सरकारी सहायता मेरे परिवार के लिए अत्यंत आवश्यक है। कृपया फाइल का त्वरित भौतिक सत्यापन कर अंतिम स्वीकृति प्रदान करें।
            </p>
          `;
        }

        if (conclusion) {
          conclusion.innerText = 'अतः आपसे विनम्र प्रार्थना है कि कृपया मेरे उपर्युक्त आवेदन पत्र एवं संलग्न दस्तावेज़ों की पुनः जांच कर सरकारी पोर्टल पर सहायता राशि जारी करने का प्रशासनिक आदेश प्रदान करने की कृपा करें।';
        }

        if (attachTitle) attachTitle.innerText = 'संलग्नक (Documents Attached):';
        if (attachList) {
          attachList.innerHTML = `
            <li>आवेदक के आधार कार्ड की स्व-सत्यापित छायाप्रति (Self-attested Aadhaar Xerox)।</li>
            <li>संबंधित एकल बैंक खाते की पासबुक के प्रथम पृष्ठ की स्पष्ट छायाप्रति।</li>
            <li>बैंक शाखा द्वारा प्रदत्त सक्रिय NPCI / Aadhaar DBT लिंक स्टेटस पर्ची।</li>
            <li>दुआरे सरकार शिविर की मूल पावती रसीद की छायाप्रति (Acknowledgement Slip)।</li>
          `;
        }

      } else if (lang === 'en') {
        if (ribbon) ribbon.innerText = 'GOVERNMENT OF WEST BENGAL • OFFICIAL CITIZEN REPRESENTATION FORMAT';
        if (dateLbl) dateLbl.innerText = 'Date:';
        if (placeLbl) placeLbl.innerText = 'Place:';
        if (toLbl) toLbl.innerText = 'To,';
        if (subLbl) subLbl.innerText = 'Subject:';
        if (salut) salut.innerText = 'Respected Sir/Madam,';
        if (offAddr) offAddr.innerText = data.block + ' Block Development Office,';
        if (distLine) distLine.innerText = data.district + ' District, West Bengal.';
        if (signGreeting) signGreeting.innerText = 'Yours faithfully,';
        if (signLabel) signLabel.innerText = '(Applicant Signature)';

        if (body1) {
          body1.innerHTML = `With due respect, I, <strong>${data.applicantName}</strong>, S/o or W/o: <strong>${data.guardianName}</strong>, permanent resident of <strong>${data.address}</strong>, would like to bring to your kind notice that I duly submitted my application for the <strong>${data.scheme}</strong> welfare scheme with all required credentials at the administrative camp (Application Ref: <span class="font-mono font-bold bg-stone-100 border border-stone-300 px-1.5 py-0.5 rounded text-stone-900">${data.ack}</span>).`;
        }

        if (data.issue === 'dbt_fail') {
          if (subjectEl) subjectEl.innerText = `Representation regarding DBT Payment Failure / Non-Credit of installment under ${data.scheme} (Ref: ${data.ack}).`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              Despite successful registration and sanction on the official portal, government assistance has not been credited to my bank account for several cycles. Upon inquiry with bank officials, it was identified that technical mismatch in central NPCI mapping and Aadhaar DBT seeding caused payment rejection.
            </p>
            <p class="leading-relaxed">
              I have subsequently re-seeded my active single savings bank account with NPCI mandate and obtained verified bank validation slip.
            </p>
          `;
        } else if (data.issue === 'rejection') {
          if (subjectEl) subjectEl.innerText = `Prayer for reconsideration against arbitrary rejection of application under ${data.scheme} (Ref: ${data.ack}).`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              I regret to submit that upon verifying my status on the government portal, my valid application is displayed as rejected without assigning any specific reason. All my documents (Aadhaar, Voter ID, and Bank Passbook) are authentic and duly compliant.
            </p>
            <p class="leading-relaxed">
              I satisfy all eligibility criteria prescribed under official state government guidelines. I earnestly pray for an administrative review to rectify portal records.
            </p>
          `;
        } else {
          if (subjectEl) subjectEl.innerText = `Prayer for expeditious processing and clearance of pending application under ${data.scheme} (Ref: ${data.ack}).`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              I submitted my complete application on ${data.appDate} with all supporting records. However, despite significant lapse of time, the application continues to be marked 'Pending at Block Level'.
            </p>
            <p class="leading-relaxed">
              Given our current financial hardship, timely receipt of this government welfare benefit is critical for our livelihood.
            </p>
          `;
        }

        if (conclusion) {
          conclusion.innerText = 'Therefore, I earnestly pray that your good office kindly re-verifies my application along with attached records and issues necessary administrative sanction to release the benefit at the earliest.';
        }

        if (attachTitle) attachTitle.innerText = 'Enclosures (Documents Attached):';
        if (attachList) {
          attachList.innerHTML = `
            <li>Self-attested photocopy of Applicant's Aadhaar Card.</li>
            <li>Clear photocopy of Bank Passbook front page (showing Single A/C details).</li>
            <li>Bank-certified active NPCI / Aadhaar DBT mapping status slip.</li>
            <li>Photocopy of official Duare Sarkar Acknowledgement Slip.</li>
          `;
        }

      } else {
        // Bengali (Standard)
        if (ribbon) ribbon.innerText = 'পশ্চিমবঙ্গ প্রশাসনিক আনুষ্ঠানিক আবেদন • অফিশিয়াল ফরম্যাট';
        if (dateLbl) dateLbl.innerText = 'তারিখ:';
        if (placeLbl) placeLbl.innerText = 'স্থান:';
        if (toLbl) toLbl.innerText = 'প্রতি,';
        if (subLbl) subLbl.innerText = 'বিষয়:';
        if (salut) salut.innerText = 'মহাশয়,';
        if (offAddr) offAddr.innerText = data.block + ' সমষ্টি উন্নয়ন ব্লক কার্যালয়,';
        if (distLine) distLine.innerText = data.district + ' জেলা, পশ্চিমবঙ্গ।';
        if (signGreeting) signGreeting.innerText = 'বিনীত,';
        if (signLabel) signLabel.innerText = '(আবেদনকারীর স্বাক্ষর)';

        if (body1) {
          body1.innerHTML = `বিনীত নিবেদন এই যে, আমি <strong class="font-bold text-stone-950">${data.applicantName}</strong>, স্বামী/অভিভাবক: <strong class="font-bold text-stone-950">${data.guardianName}</strong>, <strong class="font-bold text-stone-950">${data.address}</strong>-এর স্থায়ী বাসিন্দা। আমি আপনার ব্লকের অন্তর্গত দুয়ারে সরকার শিবিরে সরকারের জনকল্যাণমূলক <strong class="font-bold text-[#B87B4C]">${data.scheme}</strong> প্রকল্পের অন্তর্ভুক্তির নিমিত্ত প্রয়োজনীয় নথিপত্রসহ আবেদনপত্র জমা দিয়েছিলাম (আবেদন স্বীকৃতি নম্বর: <span class="font-mono font-bold bg-stone-100 border border-stone-300 px-1.5 py-0.5 rounded text-stone-900">${data.ack}</span>)।`;
        }

        if (data.issue === 'dbt_fail') {
          if (subjectEl) subjectEl.innerText = `${data.scheme} প্রকল্পের আবেদন (Ref: ${data.ack}) মঞ্জুর হওয়া সত্ত্বেও ব্যাঙ্ক DBT সমস্যাজনিত কারণে অর্থ অ্যাকাউন্টে জমা না হওয়ার প্রতিকার প্রার্থনা।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              উক্ত আবেদনের প্রেক্ষিতে সরকারি তথ্যভাণ্ডারে আমার নাম নথিভুক্ত হওয়া সত্ত্বেও বিগত কয়েকমাস ধরে আমার নির্দিষ্ট ব্যাঙ্ক অ্যাকাউন্টে কোনো ভাতা জমা হচ্ছে না। ব্যাঙ্ক কর্তৃপক্ষের সাথে অনুসন্ধান করিয়া জানা যায় যে, সেন্ট্রাল NPCI ম্যাপিং ও আধার এনেবল্ড পেমেন্ট সিস্টেমে (Aadhaar DBT Link) প্রযুক্তিগত ত্রুটির কারণে সরকারি ট্রেজারি থেকে প্রেরিত কিস্তির টাকা প্রত্যাখ্যাত (Payment Failed) হইতেছে।
            </p>
            <p class="leading-relaxed">
              ইতিমধ্যে আমি আমার নিজস্ব একক ব্যাঙ্ক অ্যাকাউন্টে (Single Account) নতুন করিয়া আধার সিডিং ও NPCI ম্যান্ডেট সফলভাবে সম্পূর্ণ করিয়াছি এবং ব্যাঙ্ক ম্যানেজার কর্তৃক স্বাক্ষরিত ভ্যালিডেশন স্লিপ সংগ্রহ করিয়াছি।
            </p>
          `;
        } else if (data.issue === 'rejection') {
          if (subjectEl) subjectEl.innerText = `${data.scheme} প্রকল্পে জমা দেওয়া আবেদন (Ref: ${data.ack}) কোনো কারণ দর্শানো ব্যতীত বাতিলের (Rejection) বিরুদ্ধে পুনর্বিবেচনার আবেদন।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              অত্যন্ত পরিতাপের সাথে জানাচ্ছি যে, পোর্টালে স্ট্যাটাস যাচাইকালে দেখতে পাই আমার আবেদনপত্রটি কোনো সুস্পষ্ট কারণ ব্যতীত বাতিল হিসেবে দেখানো হচ্ছে। আমার সমস্ত কাগজপত্র (আধার, ভোটার, ব্যাঙ্ক বই ও পারিবারিক বিবরণ) নিয়মমাফিক ও বৈধ।
            </p>
            <p class="leading-relaxed">
              সরকারি গাইডলাইন অনুযায়ী আমি এই সুবিধার সম্পূর্ণ যোগ্য দাবিদার। উক্ত বাতিলের কারণ খতিয়ে দেখে পোর্টালের ভুল সংশোধনপূর্বক পুনঃবিবেচনা করার জন্য অনুরোধ জানাচ্ছি।
            </p>
          `;
        } else {
          if (subjectEl) subjectEl.innerText = `${data.scheme} প্রকল্পে দুয়ারে সরকারে জমা দেওয়া আবেদনের (Ref: ${data.ack}) দীর্ঘসূত্রিতা ও দ্রুত নিষ্পত্তির আবেদন।`;
          if (dynamicBody) dynamicBody.innerHTML = `
            <p class="leading-relaxed">
              আমি বিগত ৬ মাসের অধিক সময় পূর্বে (${data.appDate}) শিবিরে সম্পূর্ণ নথি সহ আবেদন জমা দিয়েছিলাম। কিন্তু দীর্ঘ সময় অতিবাহিত হওয়া সত্ত্বেও পোর্টালে আবেদনটি এখনও 'Pending at Block Level' হিসেবে প্রদর্শিত হচ্ছে।
            </p>
            <p class="leading-relaxed">
              আমার পরিবারের বর্তমান আর্থিক দুরবস্থার কারণে সরকারি সহায়তাটি অত্যন্ত জরুরি। অতএব ফাইলটি দ্রুত যাচাই করে চূড়ান্ত অনুমোদনের জন্য আপনার সদয় নির্দেশ প্রার্থনা করছি।
            </p>
          `;
        }

        if (conclusion) {
          conclusion.innerText = 'অতএব মহাশয়ের নিকট সনির্বন্ধ প্রার্থনা, অনুগ্রহপূর্বক আমার উপরিউক্ত আবেদনপত্র ও সংযুক্ত ব্যাঙ্ক নথিসমূহ পুনঃযাচাই করিয়া পোর্টালে ব্যাঙ্ক DBT ডেটা পুনরায় সচল (Re-trigger Disbursement) করার যথাযথ প্রশাসনিক আদেশ জারি করিতে আপনার সদয় মর্জি হয়।';
        }

        if (attachTitle) attachTitle.innerText = 'সংযোজনীসমূহ (Documents Attached):';
        if (attachList) {
          attachList.innerHTML = `
            <li>আবেদনকারীর আধার কার্ডের স্ব-প্রত্যয়িত প্রতিলিপি (Self-attested Aadhaar Xerox)।</li>
            <li>সংশ্লিষ্ট একক ব্যাঙ্ক অ্যাকাউন্টের পাসবইয়ের প্রথম পাতার স্পষ্ট প্রতিলিপি (Bank Passbook Copy)।</li>
            <li>ব্যাঙ্ক কর্তৃপক্ষ কর্তৃক প্রদত্ত সক্রিয় NPCI / Aadhaar DBT লিঙ্ক স্ট্যাটাস স্লিপ।</li>
            <li>দুয়ারে সরকার শিবিরের মূল প্রাপ্তিস্বীকার পত্রের প্রতিলিপি (Duare Sarkar Acknowledgement)।</li>
          `;
        }
      }
"""
    content = content[:idx_start] + new_update_preview + "\n\n" + content[idx_end:]

# Update handleFormSubmit to guarantee persistent visual display
old_hfs = """    async function handleFormSubmit() {

      const btn = document.getElementById('generateBtn');

      const btnText = document.getElementById('generateBtnText');

      const spinner = document.getElementById('generateSpinner');



      btn.disabled = true;

      spinner.classList.add('animate-spin');

      btnText.innerText = 'ড্রাফট প্রস্তুত করা হচ্ছে...';



      updatePreview();

      await saveDraftToBackend(false);



      const previewBox = document.getElementById('printContainer');

      if (previewBox) {

        previewBox.scrollIntoView({ behavior: 'smooth', block: 'start' });

      }



      setTimeout(() => {

        btn.disabled = false;

        spinner.classList.remove('animate-spin');

        btnText.innerText = 'দরখাস্ত আপডেট করুন (Generate/Refresh Draft)';

        showToast('দরখাস্ত সফলভাবে আপডেট ও প্রস্তুত করা হয়েছে!');

      }, 500);

    }"""

new_hfs = """    async function handleFormSubmit() {

      const btn = document.getElementById('generateBtn');

      const btnText = document.getElementById('generateBtnText');

      const spinner = document.getElementById('generateSpinner');

      const data = getFormData();
      const lang = data.lang || 'bn';

      btn.disabled = true;

      spinner.classList.add('animate-spin');

      btnText.innerText = lang === 'en' ? 'Preparing Draft Letter...' : (lang === 'hi' ? 'आवेदन तैयार किया जा रहा है...' : 'ড্রাফট প্রস্তুত করা হচ্ছে...');



      updatePreview();

      await saveDraftToBackend(false);



      const previewBox = document.getElementById('printContainer');

      if (previewBox) {

        previewBox.classList.add('ring-4', 'ring-[#C98A5B]');

        previewBox.scrollIntoView({ behavior: 'smooth', block: 'start' });

      }



      setTimeout(() => {

        btn.disabled = false;

        spinner.classList.remove('animate-spin');

        btnText.innerText = lang === 'en' ? 'Update / Regenerate Draft' : (lang === 'hi' ? 'आवेदन अपडेट करें (Regenerate)' : 'দরখাস্ত আপডেট করুন (Generate/Refresh Draft)');

        const successMsg = lang === 'en' 
          ? 'Official Letter generated and ready to print below!' 
          : (lang === 'hi' 
            ? 'आधिकारिक आवेदन तैयार हो गया है और नीचे उपलब्ध है!' 
            : 'দরখাস্ত সফলভাবে প্রস্তুত করা হয়েছে এবং নিচে স্থায়ীভাবে দৃশ্যমান!');

        showToast(successMsg, 'verified');

      }, 400);

    }"""

content = content.replace(old_hfs.replace('\r\n', '\n'), new_hfs.replace('\r\n', '\n'))
content = content.replace(old_hfs, new_hfs)

with open('frontend/GrievanceDrafter.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("GrievanceDrafter.html logic updated successfully!")
