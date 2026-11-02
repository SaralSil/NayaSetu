with open('frontend/Login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add placeholder property updates in Login.html's setAppLanguage
old_login_ph = """      // Update all placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (i18n[lang] && i18n[lang][key]) {
          el.setAttribute('placeholder', i18n[lang][key]);
        }
      });"""

new_login_ph = """      // Update all placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (i18n[lang] && i18n[lang][key]) {
          el.setAttribute('placeholder', i18n[lang][key]);
          el.placeholder = i18n[lang][key];
        }
      });

      const loginInput = document.getElementById('loginIdentifier');
      if (loginInput && i18n[lang] && i18n[lang]['ph-userid']) {
        loginInput.placeholder = i18n[lang]['ph-userid'];
        loginInput.setAttribute('placeholder', i18n[lang]['ph-userid']);
      }"""

content = content.replace(old_login_ph.replace('\r\n', '\n'), new_login_ph.replace('\r\n', '\n'))
content = content.replace(old_login_ph, new_login_ph)

# Add URL parameter check for registered=1 on DOMContentLoaded
old_init = """    // Initializer
    window.addEventListener('DOMContentLoaded', () => {
      const savedLang = localStorage.getItem('nayasetu_lang') || localStorage.getItem('nyayasetu_lang') || 'bn';
      setAppLanguage(savedLang);
    });"""

new_init = """    // Initializer
    window.addEventListener('DOMContentLoaded', () => {
      const savedLang = localStorage.getItem('nayasetu_lang') || localStorage.getItem('nyayasetu_lang') || 'bn';
      setAppLanguage(savedLang);

      const params = new URLSearchParams(window.location.search);
      if (params.get('registered') === '1') {
        const msg = currentLang === 'en' 
          ? "Registration successful! Please login with your registered mobile number and password." 
          : currentLang === 'hi' 
            ? "पंजीकरण सफल रहा! कृपया अपने पंजीकृत मोबाइल नंबर और पासवर्ड से लॉगिन करें।" 
            : "নাগরিক নিবন্ধন সফল হয়েছে! আপনার মোবাইল নম্বর ও পাসওয়ার্ড দিয়ে লগইন করুন।";
        showToast(msg, true);
        switchLoginTab('password');
      }
    });"""

content = content.replace(old_init.replace('\r\n', '\n'), new_init.replace('\r\n', '\n'))
content = content.replace(old_init, new_init)

with open('frontend/Login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Login.html updated successfully!")
