with open('frontend/Register.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update success-register in i18n
content = content.replace(
    '"success-register": "নাগরিক একাউন্ট সফলভাবে তৈরি হয়েছে! হোমপেজে নিয়ে যাওয়া হচ্ছে...",',
    '"success-register": "নাগরিক একাউন্ট সফলভাবে তৈরি হয়েছে! অনুগ্রহ করে লগইন করুন...",'
)
content = content.replace(
    '"success-register": "Citizen account created successfully! Redirecting...",',
    '"success-register": "Citizen account created successfully! Please login with your credentials...",'
)
content = content.replace(
    '"success-register": "नागरिक खाता सफलतापूर्वक बन गया! अग्रेषित किया जा रहा है...",',
    '"success-register": "नागरिक खाता सफलतापूर्वक बन गया! कृपया अपने विवरण से लॉगिन करें...",'
)

# 2. Update setAppLanguage to strictly update placeholders both as attribute and property
old_placeholder_logic = """      // Update all placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (i18n[lang] && i18n[lang][key]) {
          el.setAttribute('placeholder', i18n[lang][key]);
        }
      });"""

new_placeholder_logic = """      // Update all placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (i18n[lang] && i18n[lang][key]) {
          el.setAttribute('placeholder', i18n[lang][key]);
          el.placeholder = i18n[lang][key];
        }
      });

      // Explicit direct element updates for guaranteed placeholder localization
      const pMap = {
        'regFullName': 'ph-fullname',
        'regBlock': 'ph-block',
        'regPassword': 'ph-pwd',
        'regConfirmPassword': 'ph-pwd-confirm'
      };
      for (const [id, key] of Object.entries(pMap)) {
        const el = document.getElementById(id);
        if (el && i18n[lang] && i18n[lang][key]) {
          el.placeholder = i18n[lang][key];
          el.setAttribute('placeholder', i18n[lang][key]);
        }
      }"""

# Normalize line endings for replacement
content = content.replace(old_placeholder_logic.replace('\r\n', '\n'), new_placeholder_logic.replace('\r\n', '\n'))
content = content.replace(old_placeholder_logic, new_placeholder_logic)

# 3. Update post-registration redirection in handleRegisterSubmit to go to Login with ?registered=1
content = content.replace(
    "setTimeout(() => { window.location.href = (window.location.port === '8000' ? '/home/' : 'Home.html'); }, 1200);",
    "setTimeout(() => { window.location.href = (window.location.port === '8000' ? '/login/?registered=1' : 'Login.html?registered=1'); }, 1200);"
)

with open('frontend/Register.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Register.html updated successfully!")
