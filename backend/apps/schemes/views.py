import time
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from .models import Scheme, Department, CommonRejectionReason
from .serializers import (
    SchemeListSerializer, SchemeDetailSerializer, 
    DepartmentSerializer, CommonRejectionReasonSerializer
)

HINDI_BENEFITS = {
    'ayushman-bharat': 'प्रति परिवार प्रति वर्ष ₹5 लाख कैशलेस स्वास्थ्य सुरक्षा + 70 वर्ष से अधिक वरिष्ठ नागरिकों को निःशुल्क वय वंदना कार्ड',
    'wb-student-credit-card': '₹10,00,000 तक उच्च शिक्षा ऋण (मात्र 4% सरल ब्याज, राज्य गारंटी)',
    'medhashree': 'कक्षा 5 से 8 के OBC छात्रों को ₹800 प्रति वर्ष छात्रवृत्ति',
    'sikshashree': 'अनुसूचित जाति/जनजाति के छात्रों को ₹800 प्रति वर्ष (कक्षा 5 से 8)',
    'taposhili-bandhu': '60 वर्ष से अधिक SC नागरिकों को मासिक ₹1,000 वृद्धावस्था पेंशन',
    'jai-johar': '60 वर्ष से अधिक ST नागरिकों को मासिक ₹1,000 वृद्धावस्था पेंशन',
    'manabik-pension': 'दिव्यांग (40%+ अक्षमता) नागरिकों को मासिक ₹1,000 मानवीय पेंशन',
    'aadhaar-enrolment-seeding': 'सार्वभौमिक 12 अंकों की विशिष्ट पहचान + डीबीटी (DBT) बैंक खाता सक्रियण',
    'agriculture-infrastructure-fund': '₹2 करोड़ तक के ऋण पर 7 वर्षों हेतु 3% ब्याज छूट + क्रेडिट गारंटी',
    'annapurna-yojana': 'प्रति माह 10 किग्रा निःशुल्क खाद्यान्न (चावल/गेहूं) + सामाजिक सुरक्षा',
    'atal-pension-yojana': '60 वर्ष के बाद ₹1,000 से ₹5,000 मासिक पेंशन + जीवनसाथी को पेंशन व नॉमिनी को कॉर्पस',
    'beti-bachao-beti-padhao': 'संस्थागत स्वास्थ्य व शिक्षा अधिकार + सुकन्या समृद्धि योजना एकीकरण',
    'bmssy-west-bengal': 'मुफ्त पीएफ अंशदान + ₹2 लाख दुर्घटना मृत्यु मुआवजा + छात्रवृत्ति',
    'citizenship-amendment-act': 'धारा 6B के तहत भारतीय नागरिकता प्रमाणपत्र व वैधानिक अधिकार',
    'credit-linkage-shg': '₹1.5 लाख से ₹20 लाख तक गारंटी-मुक्त बैंक लोन एवं ब्याज अनुदान',
    'ddu-gky': '100% मुफ्त आवासीय प्रशिक्षण + गारंटीकृत नौकरी प्लेसमेंट + पोस्ट-प्लेसमेंट सहायता',
    'day-nrlm-anandadhara': 'प्रति समूह ₹15,000 रिवाल्विंग फंड + ₹1.5 लाख तक सामुदायिक निवेश फंड (CIF)',
    'e-shram-card': '12 अंकों का UAN कार्ड + ₹2,00,000 का दुर्घटना बीमा + योजनाओं से लिंकेज',
    'job-cards-mgnregs': 'प्रति वर्ष 100-125 दिन का गारंटीशुदा रोजगार एवं सीधे बैंक खाते में दैनिक मजदूरी',
    'kisan-credit-card': '4% रियायती ब्याज दर पर ₹3,00,000 तक का रिवाल्विंग किसान क्रेडिट कार्ड ऋण',
    'midh-horticulture': 'बागवानी अवसंरचना पर 35% से 50% तक प्रत्यक्ष पूंजीगत सब्सिडी',
    'minor-correction-land-records': 'त्रुटिहीन डिजिटल खतियान / संशोधित पर्चा निर्गमन',
    'mutation-land-records': 'डिजिटल हस्ताक्षरित म्यूटेशन सर्टिफिकेट व नया स्वतंत्र खतियान',
    'national-apprenticeship-promotion-scheme': 'मासिक स्टाइपेंड में सरकारी हिस्सा (25% अधिकतम ₹1,500/माह DBT) + राष्ट्रीय प्रमाणपत्र',
    'national-apprenticeship-training-scheme': 'मासिक स्टाइपेंड (₹8,000 से ₹9,000+/माह सीधे DBT) + भारत सरकार का प्रवीणता प्रमाणपत्र',
    'patta-application-vested-land': 'स्थायी व उत्तराधिकार योग्य भूमि पट्टा विलेख (1 एकड़ तक) + भू-राजस्व छूट',
    'pm-surya-ghar': 'छत पर सोलर पैनल लगाने हेतु ₹78,000 तक की सीधी बैंक सब्सिडी + प्रति माह 300 यूनिट मुफ्त बिजली',
    'pm-svanidhi': 'स्ट्रीट वेंडर्स हेतु ₹10,00,000 तक बिना गारंटी कार्यशील ऋण + 7% ब्याज सब्सिडी',
    'post-matric-scholarship': 'कक्षा 11वीं से पीएचडी तक के एससी, एसटी, ओबीसी व ईडब्ल्यूएस छात्रों को पूर्ण शुल्क प्रतिपूर्ति व वजीफा',
    'pmay-urban': 'शहरी गरीब व बेघर परिवारों को पक्का मकान निर्माण हेतु ₹2.50 लाख तक का सरकारी अनुदान',
    'pm-fme': 'सूक्ष्म खाद्य प्रसंस्करण इकाइयों को मशीनरी व उन्नयन हेतु 35% क्रेडिट-लिंक्ड सब्सिडी (अधिकतम ₹10 लाख)',
    'pmgkay': 'अंत्योदय (AAY) परिवारों को 35 किग्रा व प्राथमिकता (PHH) कार्डधारकों को प्रति व्यक्ति 5 किग्रा 100% मुफ्त राशन',
    'pmjdy': 'जीरो बैलेंस बचत बैंक खाता + ₹2 लाख का मुफ्त रुपे दुर्घटना बीमा + ₹10,000 ओवरड्राफ्ट सुविधा',
    'pmjjby': 'मात्र ₹436 सालाना प्रीमियम पर किसी भी कारण से मृत्यु होने पर ₹2 लाख का टर्म जीवन बीमा',
    'pm-kisan': 'सभी पात्र किसान परिवारों को प्रति वर्ष ₹6,000 की सुनिश्चित आय सहायता (₹2,000 की 3 समान किस्तों में)',
    'pm-mkssy': 'मत्स्य पालकों व श्रमिकों हेतु 40% तक परफॉर्मेंस ग्रांट, संस्थागत ऋण व जलीय कृषि बीमा प्रोत्साहन',
    'pmmy': 'गैर-कृषि सूक्ष्म उद्यमों हेतु ₹20 लाख तक का बिना गारंटी मुद्रा बैंक लोन (शिशु, किशोर, तरुण)',
    'pm-sym': 'असंगठित कामगारों को 60 वर्ष की आयु के बाद ₹3,000 की मासिक सुनिश्चित वृद्धावस्था पेंशन',
    'pmsby': 'मात्र ₹20 वार्षिक प्रीमियम पर ₹2 लाख का दुर्घटना मृत्यु एवं स्थायी दिव्यांगता बीमा कवर',
    'pm-vishwakarma': '18 पारंपरिक शिल्पकलाओं के कारीगरों को ₹15,000 टूलकिट अनुदान, 5% ब्याज पर ₹3 लाख तक लोन व ट्रेनिंग',
    'pm-vikas': 'अल्पसंख्यक दस्तकारों, महिला उद्यमियों व युवाओं हेतु मुफ्त कौशल प्रशिक्षण, वजीफा व उद्यम संवर्धन',
    'pmuy': 'गरीब परिवारों की महिलाओं को मुफ्त घरेलू एलपीजी गैस कनेक्शन, पहला भरा सिलेंडर, चूल्हा व ₹300 सब्सिडी',
    'pre-matric-scholarship-sc-st-obc': 'कक्षा 9वीं-10वीं के नियमित एससी, एसटी व ओबीसी विद्यार्थियों को ₹3,500 से ₹7,000 वार्षिक छात्रवृत्ति',
    'minority-pre-post-matric-scholarship': 'अल्पसंख्यक वर्ग के मेधावी छात्र-छात्राओं हेतु प्री व पोस्ट-मैट्रिक छात्रवृत्ति व शुल्क प्रतिपूर्ति',
    'pmegp': 'नए सूक्ष्म विनिर्माण (₹50 लाख तक) व सेवा उद्यमों (₹20 लाख तक) की स्थापना हेतु 35% तक मार्जिन मनी सब्सिडी'
}

HINDI_TAGLINES = {
    'ayushman-bharat': 'देशभर के 29,000+ अस्पतालों में ₹5 लाख तक का कैशलेस इलाज व 70+ बुजुर्गों के लिए विशेष सुरक्षा।',
    'wb-student-credit-card': 'उच्च शिक्षा के लिए राज्य सरकार की गारंटी पर 4% ब्याज पर स्टूडेंट क्रेडिट कार्ड।',
    'medhashree': 'ओबीसी छात्र-छात्राओं को पढ़ाई जारी रखने के लिए प्री-मैट्रिक छात्रवृत्ति।',
    'sikshashree': 'कक्षा 5 से 8 में पढ़ने वाले अनुसूचित जाति/जनजाति के छात्रों के लिए सहायता।',
    'taposhili-bandhu': 'पश्चिम बंगाल के अनुसूचित जाति (SC) के वरिष्ठ नागरिकों के लिए मासिक वृद्धावस्था पेंशन।',
    'jai-johar': 'पश्चिम बंगाल के अनुसूचित जनजाति (ST) के वरिष्ठ नागरिकों के लिए मासिक वृद्धावस्था पेंशन।',
    'manabik-pension': 'पश्चिम बंगाल के 40% या अधिक दिव्यांगता वाले नागरिकों के लिए मासिक वित्तीय सहायता।',
    'aadhaar-enrolment-seeding': 'सार्वभौमिक डिजिटल पहचान नामांकन और डीबीटी लाभ प्राप्ति हेतु आधार-बैंक सीडिंग।',
    'agriculture-infrastructure-fund': 'फसल कटाई बाद प्रबंधन व आधुनिक कृषि संपत्तियों के निर्माण हेतु 3% ब्याज छूट पर बैंक ऋण।',
    'annapurna-yojana': '65+ निराश्रित बुजुर्गों को मासिक 10 किग्रा मुफ्त खाद्यान्न एवं पात्र महिलाओं को सामाजिक सुरक्षा।',
    'atal-pension-yojana': '60 वर्ष की आयु के बाद ₹1,000 से ₹5,000 की आजीवन मासिक पेंशन योजना।',
    'beti-bachao-beti-padhao': 'बालिकाओं के संरक्षण, स्वास्थ्य एवं गुणवत्तापूर्ण शिक्षा सुनिश्चित करने हेतु राष्ट्रीय अभियान।',
    'bmssy-west-bengal': 'पश्चिम बंगाल के असंगठित कामगारों के लिए 100% राज्य प्रायोजित सामाजिक सुरक्षा व भविष्य निधि।',
    'citizenship-amendment-act': '31 दिसंबर 2014 से पूर्व भारत आए प्रताड़ित अल्पसंख्यक प्रवासियों हेतु भारतीय नागरिकता।',
    'credit-linkage-shg': 'ग्रामीण महिला स्वयं सहायता समूहों को ₹20 लाख तक का संपार्श्विक-मुक्त रियायती बैंक ऋण।',
    'ddu-gky': '15-35 वर्ष के ग्रामीण युवाओं के लिए निःशुल्क आवासीय कौशल प्रशिक्षण व रोजगार गारंटी।',
    'day-nrlm-anandadhara': 'ग्रामीण निर्धन महिलाओं को SHG से जोड़कर रिवाल्विंग फंड व आजीविका प्रोत्साहन।',
    'e-shram-card': '12 अंकों का यूनिवर्सल अकाउंट नंबर (UAN) व ₹2 लाख का मुफ्त दुर्घटना बीमा।',
    'job-cards-mgnregs': 'प्रत्येक ग्रामीण परिवार को 100 से 125 दिनों का गारंटीकृत वैधानिक अकुशल रोजगार।',
    'kisan-credit-card': 'किसानों व बटाईदारों को 4% प्रभावी ब्याज पर ₹3 लाख तक का आसान कृषि बैंक लोन।',
    'midh-horticulture': 'पॉलीहाउस, कोल्ड स्टोरेज, फल-फूल की बागवानी व आधुनिक नर्सरी हेतु 50% तक पूंजीगत सब्सिडी।',
    'minor-correction-land-records': 'कंप्यूटरीकृत खतियान/पर्चे में नाम, वर्तनी या अंश की लिपिकीय त्रुटियों का त्वरित सुधार।',
    'mutation-land-records': 'पश्चिम बंगाल भूमि सुधार अधिनियम की धारा 50 के अंतर्गत जमीन का आधिकारिक नामांतरण।',
    'national-apprenticeship-promotion-scheme': 'उद्योगों में ऑन-द-जॉब अप्रेंटिसशिप प्रशिक्षण व ₹1,500 प्रति माह तक प्रत्यक्ष डीबीटी वजीफा।',
    'national-apprenticeship-training-scheme': 'डिप्लोमा और ग्रेजुएट युवाओं के लिए 1 वर्षीय सवैतनिक व्यावहारिक औद्योगिक प्रशिक्षण।',
    'patta-application-vested-land': 'भूमिहीन ग्रामीण निर्धन परिवारों व किसानों को सरकारी निहित भूमि का स्थायी कानूनी पट्टा।',
    'pm-surya-ghar': 'छत पर सोलर पैनल लगाकर 300 यूनिट तक मुफ्त बिजली और ₹78,000 तक की केंद्रीय वित्तीय सब्सिडी।',
    'pm-svanidhi': 'स्ट्रीट वेंडर्स और रेहड़ी-पटरी वालों के लिए ₹50,000 तक का बिना गारंटी कार्यशील पूंजी ऋण और 7% ब्याज सब्सिडी।',
    'post-matric-scholarship': '11वीं, 12वीं, आईटीआई, डिप्लोमा, यूजी, पीजी व पीएचडी के एससी, एसटी, ओबीसी और ईडब्ल्यूएस छात्रों हेतु पोस्ट-मैट्रिक छात्रवृत्ति।',
    'pmay-urban': 'शहरी क्षेत्र के आर्थिक रूप से कमजोर (EWS) और कम आय वर्ग (LIG) के परिवारों को पक्का मकान बनाने के लिए ₹2.50 लाख तक का अनुदान।',
    'pm-fme': 'सूक्ष्म खाद्य प्रसंस्करण उद्यमों को आधुनिक बनाने व नए उद्योग हेतु 35% (अधिकतम ₹10 लाख) क्रेडिट-लिंक्ड सब्सिडी।',
    'pmgkay': 'अंत्योदय (AAY) और प्राथमिकता (PHH) राशन कार्ड धारकों को प्रति माह प्रति व्यक्ति 5 किलो मुफ्त राशन वितरण।',
    'pmjdy': 'प्रत्येक परिवार को बैंकिंग प्रणाली से जोड़ने हेतु शून्य बैलेंस खाता, ₹2 लाख दुर्घटना बीमा युक्त रुपे कार्ड और ₹10,000 तक ओवरड्राफ्ट सुविधा।',
    'pmjjby': '18 से 50 वर्ष के नागरिकों के लिए मात्र ₹436 सालाना प्रीमियम में ₹2 लाख का टर्म लाइफ इंश्योरेंस।',
    'pm-kisan': 'सभी भूमिधारक किसान परिवारों को प्रति वर्ष ₹6,000 की सुनिश्चित आय सहायता (₹2,000 की 3 समान किस्तों में)।',
    'pm-mkssy': 'मत्स्य पालकों और श्रमिकों के लिए डिजिटल एनएफडीपी पंजीकरण, ऋण सुविधा और जलीय कृषि बीमा सब्सिडी।',
    'pmmy': 'गैर-कृषि सूक्ष्म व छोटे उद्यमों के लिए ₹20 लाख तक का बिना गारंटी मुद्रा बैंक लोन (शिशु, किशोर, तरुण)।',
    'pm-sym': 'असंगठित क्षेत्र के कामगारों (घरेलू सहायिका, रेहड़ी-पटरी, रिक्शा चालक, निर्माण श्रमिक) के लिए ₹3,000 मासिक सुनिश्चित वृद्धावस्था पेंशन।',
    'pmsby': '18 से 70 वर्ष के बैंक खाताधारकों के लिए सालाना मात्र ₹20 में ₹2 लाख का दुर्घटना बीमा कवर।',
    'pm-vishwakarma': '18 पारंपरिक शिल्पकलाओं और कारीगरों हेतु ₹15,000 टूलकिट अनुदान, 5% ब्याज पर ₹3 लाख तक बिना गारंटी लोन व स्किल ट्रेनिंग।',
    'pm-vikas': 'छह अधिसूचित अल्पसंख्यक समुदायों के पारंपरिक कारीगरों, महिला उद्यमियों और युवाओं के लिए समग्र कौशल प्रशिक्षण व आजीविका संवर्धन योजना।',
    'pmuy': 'महिलाओं के स्वास्थ्य की सुरक्षा हेतु बिना किसी सिक्योरिटी डिपॉजिट के नया घरेलू गैस कनेक्शन, पहला रिफिल और चूल्हा मुफ्त।',
    'pre-matric-scholarship-sc-st-obc': 'सरकारी व मान्यता प्राप्त विद्यालयों में पढ़ रहे अनुसूचित जाति, जनजाति व ओबीसी छात्रों हेतु प्री-मैट्रिक छात्रवृत्ति।',
    'minority-pre-post-matric-scholarship': 'अल्पसंख्यक विद्यार्थियों की माध्यमिक व उच्च शिक्षा हेतु छात्रवृत्ति (न्यूनतम 50% अंक अनिवार्य)।',
    'pmegp': 'नए सूक्ष्म उद्यमों की स्थापना हेतु 35% तक बैंक लोन सब्सिडी (विनिर्माण में ₹50 लाख, सेवा क्षेत्र में ₹20 लाख तक)।'
}

# High-Performance Redis / Unified Cache for Active Schemes
SCHEMES_CACHE_KEY = 'nayasetu:active_schemes_bundle:v1'
CACHE_TTL = 300  # 5 minutes

def clear_schemes_cache():
    cache.delete(SCHEMES_CACHE_KEY)
    cache.delete('nayasetu:schemes:all_active')

def get_active_schemes_bundle():
    cached = cache.get(SCHEMES_CACHE_KEY)
    if cached is not None:
        return cached

    schemes = list(
        Scheme.objects.filter(is_active=True)
        .select_related('department', 'eligibility')
        .prefetch_related('documents')
    )

    bundle = []
    for scheme in schemes:
        eligibility = getattr(scheme, 'eligibility', None)
        if not eligibility:
            continue

        sc_data = SchemeListSerializer(scheme).data
        if not sc_data.get('benefit_amount_text_hi'):
            sc_data['benefit_amount_text_hi'] = HINDI_BENEFITS.get(scheme.slug, sc_data.get('benefit_amount_text_bn', ''))
        if not sc_data.get('tagline_hi'):
            sc_data['tagline_hi'] = HINDI_TAGLINES.get(scheme.slug, sc_data.get('tagline_en', ''))

        # In-memory document count using prefetched objects - ZERO extra database queries!
        mandatory_count = sum(1 for d in scheme.documents.all() if d.is_mandatory)

        bundle.append({
            'scheme': scheme,
            'eligibility': eligibility,
            'sc_data': sc_data,
            'mandatory_count': mandatory_count,
        })

    cache.set(SCHEMES_CACHE_KEY, bundle, timeout=CACHE_TTL)
    return bundle


class SchemeListView(generics.ListAPIView):
    """
    Search and filter West Bengal schemes.
    Supports query parameters: ?search=...&category=...&department=...
    Cached via Redis for instant directory browsing.
    """
    serializer_class = SchemeListSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', '').strip()
        category = request.query_params.get('category', '').strip()
        department = request.query_params.get('department', '').strip()

        # Cache default directory query (no search or filter)
        if not search_query and not category and not department:
            cache_key = 'nayasetu:schemes:all_active'
            cached = cache.get(cache_key)
            if cached is not None:
                return Response(cached)
            resp = super().list(request, *args, **kwargs)
            cache.set(cache_key, resp.data, timeout=300)
            return resp

        return super().list(request, *args, **kwargs)

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

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        cache_key = f'nayasetu:scheme_detail:{slug}'
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)
        resp = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, resp.data, timeout=300)
        return resp


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

        bundle = get_active_schemes_bundle()
        matched_schemes = []

        for item in bundle:
            scheme = item['scheme']
            eligibility = item['eligibility']
            sc_data = item['sc_data']
            mandatory_count = item['mandatory_count']

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

            # 5. Land requirement (PM-Kisan / Agriculture)
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

            matched_schemes.append({
                "scheme": sc_data,
                "match_score": match_score,
                "notes": notes_primary,
                "notes_bn": flags_bn,
                "notes_hi": flags_hi,
                "notes_en": flags_en,
                "mandatory_documents_count": mandatory_count,
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
