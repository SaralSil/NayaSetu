with open('frontend/GrievanceDrafter.html', encoding='utf-8') as f:
    html = f.read()

ids = ['previewName', 'previewSigName', 'previewGuardian', 'previewAddress', 'previewPhone', 'previewAck', 'previewRecipient', 'previewOfficeAddress', 'previewDistrictLine', 'previewScheme', 'previewBodyDynamic', 'previewSubject', 'printContainer', 'generateBtn', 'generateBtnText', 'generateSpinner']
for i in ids:
    print(f"{i}: {'id=\"' + i + '\"' in html}")
