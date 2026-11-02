from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Scheme, Department, CommonRejectionReason
from .serializers import (
    SchemeListSerializer, SchemeDetailSerializer, 
    DepartmentSerializer, CommonRejectionReasonSerializer
)

class SchemeListView(generics.ListAPIView):
    """
    Search and filter West Bengal schemes.
    Supports query parameters: ?search=...&category=...&department=...
    """
    serializer_class = SchemeListSerializer

    def get_queryset(self):
        queryset = Scheme.objects.filter(is_active=True).select_related('department')
        search_query = self.request.query_params.get('search', '').strip()
        category = self.request.query_params.get('category', '').strip()
        department = self.request.query_params.get('department', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_bn__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                Q(description_bn__icontains=search_query) |
                Q(tagline_en__icontains=search_query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if department:
            queryset = queryset.filter(department__code=department)

        return queryset


class SchemeDetailView(generics.RetrieveAPIView):
    """Get complete details, document checklist, and common rejection remedies for a scheme"""
    queryset = Scheme.objects.filter(is_active=True).select_related('department', 'eligibility').prefetch_related('documents', 'rejection_reasons')
    serializer_class = SchemeDetailSerializer
    lookup_field = 'slug'


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EligibilityWizardView(APIView):
    """
    Evaluates citizen profile against all WB schemes.
    Input payload:
    {
      "age": 28,
      "gender": "female",
      "caste": "SC",
      "annual_family_income": 60000,
      "has_land": false,
      "is_student": false
    }
    """
    def post(self, request):
        data = request.data
        try:
            age = int(data.get('age', 0)) if data.get('age') is not None else None
        except (ValueError, TypeError):
            age = None
            
        gender = str(data.get('gender', '')).lower()
        caste = str(data.get('caste', 'General'))
        income = float(data.get('annual_family_income', 0)) if data.get('annual_family_income') else None
        has_land = bool(data.get('has_land', False))
        is_student = bool(data.get('is_student', False))
        lang = str(data.get('lang', 'bn')).lower()
        if lang not in ['bn', 'hi', 'en']:
            lang = 'bn'

        HINDI_BENEFITS = {
            'lakshmir-bhandar': 'अन्नपूर्णा भंडार / लक्ष्मी भंडार: मासिक ₹3,000 सभी पात्र महिलाओं के लिए (2026 संशोधित)',
            'wb-yuva-shakti': 'मासिक ₹2,000 (10वीं/12वीं पास) व ₹3,000 (स्नातक) बेरोजगारी वित्तीय सहायता + युवा भरोसा कार्ड',
            'ayushman-bharat': 'प्रति परिवार प्रति वर्ष ₹5 लाख कैशलेस स्वास्थ्य सुरक्षा + 70 वर्ष से अधिक वरिष्ठ नागरिकों को निःशुल्क वय वंदना कार्ड',
            'swasthya-sathi': 'प्रति परिवार प्रति वर्ष ₹5,00,000 तक कैशलेस स्वास्थ्य सुरक्षा (स्मार्ट कार्ड)',
            'krishak-bandhu-natun': 'वार्षिक ₹4,000 से ₹10,000 कृषि सहायता (PM-Kisan के साथ ₹16,000) + ₹2 लाख मृत्यु लाभ',
            'karmashree': 'प्रति ग्रामीण परिवार 50 दिनों का पक्का काम और दैनिक वैधानिक मजदूरी (₹250+/दिन)',
            'bhabishyat-credit-card': '₹5,00,000 तक स्वरोजगार बैंक ऋण (10% राज्य सब्सिडी + बैंक गारंटी)',
            'banglar-awas-yojana': '₹1,20,000 पक्का मकान निर्माण हेतु सीधे 3 किस्तों में बैंक खाते में',
            'bangla-shasya-bima': '100% राज्य प्रायोजित फसल बीमा (बाढ़, सूखा व प्राकृतिक आपदाओं पर पूर्ण मुआवजा)',
            'taruner-swapno': 'कक्षा 11 व 12 के छात्रों को टैबलेट/स्मार्टफोन हेतु ₹10,000 एकमुश्त डीबीटी',
            'kanyashree-prakalpa': 'K1: ₹1,000 वार्षिक | K2: ₹25,000 एकमुश्त अनुदान | K3: उच्च शिक्षा पीजी स्कॉलरशिप',
            'rupashree-prakalpa': 'विवाह पूर्व ₹25,000 एकमुश्त आर्थिक अनुदान',
            'wb-student-credit-card': '₹10,00,000 तक उच्च शिक्षा ऋण (मात्र 4% सरल ब्याज, राज्य गारंटी)',
            'aikyashree': 'कक्षा के अनुसार ₹1,100 से ₹33,000 प्रति वर्ष अल्पसंख्यक छात्रवृत्ति',
            'svmcm-scholarship': 'मासिक ₹1,000 से ₹5,000 उच्च शिक्षा मेरिट छात्रवृत्ति (स्वामी विवेकानंद)',
            'oasis-scholarship': 'SC, ST व OBC छात्रों के लिए प्री-मैट्रिक और पोस्ट-मैट्रिक स्कॉलरशिप योजना',
            'medhashree': 'कक्षा 5 से 8 के OBC छात्रों को ₹800 प्रति वर्ष छात्रवृत्ति',
            'yogyasree': 'SC, ST और OBC छात्रों हेतु JEE, NEET, WBPSC, WBCS की 100% निःशुल्क कोचिंग',
            'sikshashree': 'अनुसूचित जाति/जनजाति के छात्रों को ₹800 प्रति वर्ष (कक्षा 5 से 8)',
            'taposhili-bandhu': '60 वर्ष से अधिक SC नागरिकों को मासिक ₹1,000 वृद्धावस्था पेंशन',
            'jai-johar': '60 वर्ष से अधिक ST नागरिकों को मासिक ₹1,000 वृद्धावस्था पेंशन',
            'manabik-pension': 'दिव्यांग (40%+ अक्षमता) नागरिकों को मासिक ₹1,000 मानवीय पेंशन',
            'khadya-sathi': 'मुफ्त मासिक खाद्यान्न (चावल व गेहूं) राशन कार्ड धारकों को',
            'matsyajeebi-bandhu': 'मछुआरों को ₹2 लाख आकस्मिक मृत्यु बीमा + मत्स्य उपकरण सहायता',
            'sishu-sathi': '0 से 18 वर्ष के बच्चों हेतु 100% निःशुल्क हार्ट सर्जरी व क्रिटिकल पीडियाट्रिक केयर',
            'chokher-alo': 'निःशुल्क नेत्र परीक्षण, मोतियाबिंद ऑपरेशन व मुफ्त चश्मा वितरण'
        }
        HINDI_TAGLINES = {
            'lakshmir-bhandar': 'पश्चिम बंगाल की 25-60 वर्ष की महिलाओं के लिए ₹3,000 की मासिक वित्तीय सहायता योजना।',
            'wb-yuva-shakti': 'राज्य के 21-40 वर्ष के बेरोजगार युवाओं को ₹2,000-₹3,000 मासिक सहायता व कौशल प्रशिक्षण।',
            'ayushman-bharat': 'देशभर के 29,000+ अस्पतालों में ₹5 लाख तक का कैशलेस इलाज व 70+ बुजुर्गों के लिए विशेष सुरक्षा।',
            'swasthya-sathi': 'राज्य के सभी परिवारों के लिए ₹5 लाख तक का कैशलेस स्वास्थ्य बीमा स्मार्ट कार्ड।',
            'krishak-bandhu-natun': 'राज्य के सभी पंजीकृत किसानों और बटाईदारों के लिए सुनिश्चित वित्तीय व ₹2 लाख जीवन बीमा सुरक्षा।',
            'karmashree': 'ग्रामीण श्रमिकों को 50 दिनों का गारंटीड रोजगार व समय पर बैंक खाते में मजदूरी।',
            'bhabishyat-credit-card': 'युवा उद्यमियों को नया व्यवसाय शुरू करने हेतु ₹5 लाख तक का आसान बैंक लोन।',
            'banglar-awas-yojana': 'आर्थिक रूप से कमजोर परिवारों को अपना पक्का घर बनाने के लिए वित्तीय सहायता।',
            'bangla-shasya-bima': 'किसानों के लिए बिना किसी प्रीमियम के 100% मुफ्त फसल सुरक्षा बीमा।',
            'taruner-swapno': 'डिजिटल शिक्षा को बढ़ावा देने हेतु 11वीं-12वीं के छात्रों के लिए स्मार्टफोन/टैबलेट सहायता।',
            'kanyashree-prakalpa': 'बालिकाओं की शिक्षा जारी रखने और बाल विवाह की रोकथाम हेतु वित्तीय प्रोत्साहन।',
            'rupashree-prakalpa': 'आर्थिक रूप से कमजोर परिवारों की बेटियों के विवाह हेतु एकमुश्त अनुदान।',
            'wb-student-credit-card': 'उच्च शिक्षा के लिए राज्य सरकार की गारंटी पर 4% ब्याज पर स्टूडेंट क्रेडिट कार्ड।',
            'aikyashree': 'अल्पसंख्यक वर्ग (मुस्लिम, ईसाई, सिख, बौद्ध, जैन) के मेधावी छात्रों के लिए छात्रवृत्ति।',
            'svmcm-scholarship': 'उच्च माध्यमिक व कॉलेज के मेधावी छात्र-छात्राओं हेतु उच्च मूल्य की मेरिट छात्रवृत्ति।',
            'oasis-scholarship': 'SC, ST व OBC छात्रों के लिए प्री-मैट्रिक और पोस्ट-मैट्रिक स्कॉलरशिप योजना।',
            'medhashree': 'ओबीसी छात्र-छात्राओं को पढ़ाई जारी रखने के लिए प्री-मैट्रिक छात्रवृत्ति।',
            'yogyasree': 'प्रतियोगी परीक्षाओं की तैयारी के लिए निःशुल्क सरकारी कोचिंग व्यवस्था।',
            'sikshashree': 'कक्षा 5 से 8 में पढ़ने वाले अनुसूचित जाति/जनजाति के छात्रों के लिए सहायता।',
            'taposhili-bandhu': 'पश्चिम बंगाल के अनुसूचित जाति (SC) के वरिष्ठ नागरिकों के लिए मासिक वृद्धावस्था पेंशन।',
            'jai-johar': 'पश्चिम बंगाल के अनुसूचित जनजाति (ST) के वरिष्ठ नागरिकों के लिए मासिक वृद्धावस्था पेंशन।',
            'manabik-pension': 'विशेष रूप से सक्षम नागरिकों के लिए मासिक आर्थिक सहायता।',
            'khadya-sathi': 'राज्य के सभी नागरिकों के लिए खाद्य सुरक्षा और राशन व्यवस्था।',
            'matsyajeebi-bandhu': 'मछुआरों और उनके परिवारों के कल्याण हेतु समर्पित राज्य योजना।',
            'sishu-sathi': 'बच्चों के दिल की बीमारियों के इलाज हेतु पूरी तरह मुफ्त सर्जरी की सुविधा।',
            'chokher-alo': 'नेत्र स्वास्थ्य और अंधत्व निवारण के लिए राज्यव्यापी निःशुल्क उपचार अभियान।'
        }

        schemes = Scheme.objects.filter(is_active=True).select_related('department', 'eligibility').prefetch_related('documents')
        
        matched_schemes = []

        for scheme in schemes:
            eligibility = getattr(scheme, 'eligibility', None)
            if not eligibility:
                continue

            match_score = 100
            flags_bn = []
            flags_hi = []
            flags_en = []

            # 1. Gender check
            if eligibility.gender_allowed != 'all' and eligibility.gender_allowed != gender:
                continue  # Ineligible

            # 2. Age check
            if age is not None:
                if eligibility.min_age and age < eligibility.min_age:
                    continue
                if eligibility.max_age and age > eligibility.max_age:
                    continue

            # 3. Caste check
            if eligibility.caste_categories:
                # If scheme restricts to specific categories (e.g. Jai Johar ST, Taposhili Bandhu SC)
                if caste not in eligibility.caste_categories and 'All' not in eligibility.caste_categories:
                    continue

            # 4. Income check
            if eligibility.max_family_income and income is not None:
                if income > float(eligibility.max_family_income):
                    continue

            # 5. Land requirement (Krishak Bandhu)
            if eligibility.requires_land_record and not has_land:
                match_score -= 30
                flags_bn.append("চাষযোগ্য কৃষিজমির রেকর্ডকৃত পর্চা (RoR/Porcha) আবেদনকারীর নামে থাকা আবশ্যক।")
                flags_hi.append("खेती योग्य कृषि भूमि का रिकॉर्ड/पर्चा (RoR/Porcha) आवेदक के नाम पर होना आवश्यक है।")
                flags_en.append("Requires cultivable agricultural land records (RoR/Porcha) in applicant's name.")

            # Specific rules highlights
            if eligibility.requires_single_bank_account:
                flags_bn.append("আবেদনকারীর নিজস্ব একক (Single) ব্যাঙ্ক অ্যাকাউন্ট বাধ্যতামূলক (যৌথ অ্যাকাউন্ট গ্রহণযোগ্য নয়)।")
                flags_hi.append("आवेदक के नाम पर एकल (Single) बैंक खाता अनिवार्य है (संयुक्त खाता बिल्कुल अमान्य)।")
                flags_en.append("Requires a SINGLE bank account in applicant's name (joint accounts strictly not accepted).")

            if eligibility.requires_swasthya_sathi:
                flags_bn.append("পরিবারের নিজস্ব স্বাস্থ্য সাথী কার্ড থাকা বাধ্যতামূলক।")
                flags_hi.append("परिवार का स्वास्थ्य साथी कार्ड होना अनिवार्य है।")
                flags_en.append("Family Swasthya Sathi health card is mandatory.")

            if eligibility.requires_aadhaar_dbt_linking:
                flags_bn.append("ব্যাঙ্ক অ্যাকাউন্টে আধার ও NPCI DBT সক্রিয় থাকা বাধ্যতামূলক।")
                flags_hi.append("बैंक खाते में आधार और NPCI DBT सक्रिय होना अनिवार्य है।")
                flags_en.append("Active Aadhaar-NPCI DBT linking in bank account is mandatory.")

            # Select primary notes based on requested language
            if lang == 'hi':
                notes_primary = flags_hi
            elif lang == 'en':
                notes_primary = flags_en
            else:
                notes_primary = flags_bn

            sc_data = SchemeListSerializer(scheme).data
            if not sc_data.get('benefit_amount_text_hi'):
                sc_data['benefit_amount_text_hi'] = HINDI_BENEFITS.get(scheme.slug, sc_data.get('benefit_amount_text_bn', ''))
            if not sc_data.get('tagline_hi'):
                sc_data['tagline_hi'] = HINDI_TAGLINES.get(scheme.slug, sc_data.get('tagline_en', ''))

            matched_schemes.append({
                "scheme": sc_data,
                "match_score": match_score,
                "notes": notes_primary,
                "notes_bn": flags_bn,
                "notes_hi": flags_hi,
                "notes_en": flags_en,
                "mandatory_documents_count": scheme.documents.filter(is_mandatory=True).count(),
            })

        # Sort by match score
        matched_schemes.sort(key=lambda x: x['match_score'], reverse=True)

        return Response({
            "total_matches": len(matched_schemes),
            "profile_evaluated": {
                "age": age,
                "gender": gender,
                "caste": caste,
                "income": income,
                "has_land": has_land
            },
            "results": matched_schemes
        })
