"""
Core URL Configuration for NyayaSetu AI
"""
import os
from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse, HttpResponse
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.analyzer.views import ChatbotAssistantView

def api_health_check(request):
    return JsonResponse({
        "status": "active",
        "service": "NyayaSetu AI Backend",
        "version": "1.0.0",
        "description": "West Bengal Government Scheme & Citizen Rights Assistant API"
    })

def api_root(request):
    return JsonResponse({
        "status": "active",
        "service": "NyayaSetu AI API",
        "version": "1.0.0",
        "description": "West Bengal Government Scheme & Citizen Rights Assistant API",
        "endpoints": {
            "health": "/api/health/",
            "schemes": "/api/schemes/",
            "departments": "/api/schemes/departments/",
            "check_eligibility": "/api/schemes/check-eligibility/",
            "analyzer": "/api/analyzer/explain/",
            "grievances": "/api/grievances/generate/",
            "chatbot": "/api/chatbot/",
            "accounts": "/api/accounts/"
        }
    })

_PAGE_CACHE = {}

def fast_page_view(filename):
    file_path = settings.BASE_DIR.parent / 'frontend' / filename
    def view(request):
        mtime = None
        if settings.DEBUG:
            try:
                mtime = os.path.getmtime(file_path)
            except OSError:
                mtime = 0
            cached = _PAGE_CACHE.get(filename)
            if cached and cached[0] == mtime:
                return HttpResponse(cached[1], content_type='text/html; charset=utf-8')
        elif filename in _PAGE_CACHE:
            return HttpResponse(_PAGE_CACHE[filename][1], content_type='text/html; charset=utf-8')

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

        if settings.DEBUG and mtime is not None:
            _PAGE_CACHE[filename] = (mtime, content)
        elif not settings.DEBUG:
            _PAGE_CACHE[filename] = (0, content)

        return HttpResponse(content, content_type='text/html; charset=utf-8')
    return view

landing_view = fast_page_view('Landing.html')
home_view = fast_page_view('Home.html')
login_view = fast_page_view('Login.html')
register_view = fast_page_view('Register.html')
notice_view = fast_page_view('notice_explainer.html')
wizard_view = fast_page_view('EligibilityWizard.html')
grievance_view = fast_page_view('GrievanceDrafter.html')

urlpatterns = [
    # Direct Asset & Favicon routes
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend' / 'assets'}),
    re_path(r'^(?:[^/]+/)*wb_emblem\.webp$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'wb_emblem.webp'}),
    re_path(r'^favicon\.ico$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'wb_emblem.webp'}),
    re_path(r'^sw\.js$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'sw.js'}),

    # Frontend Pages (Optimized direct high-speed delivery)
    path('', landing_view, name='landing'),
    re_path(r'^(?:Landing\.html)?$', landing_view),
    
    re_path(r'^home/?$', home_view, name='home'),
    re_path(r'^Home\.html$', home_view),

    re_path(r'^login/?$', login_view, name='login'),
    re_path(r'^Login\.html$', login_view),

    re_path(r'^register/?$', register_view, name='register'),
    re_path(r'^Register\.html$', register_view),

    re_path(r'^notice-explainer/?$', notice_view, name='notice_explainer'),
    re_path(r'^notice_explainer\.html$', notice_view),

    re_path(r'^eligibility-wizard/?$', wizard_view, name='eligibility_wizard'),
    re_path(r'^EligibilityWizard\.html$', wizard_view),

    re_path(r'^grievance-drafter/?$', grievance_view, name='grievance_drafter'),
    re_path(r'^GrievanceDrafter\.html$', grievance_view),

    path('admin/', admin.site.urls),
    re_path(r'^api/?$', api_root, name='api_root'),
    path('api/health/', api_health_check, name='api_health_check'),
    
    # Core API Endpoints
    path('api/chatbot/', ChatbotAssistantView.as_view(), name='api-chatbot'),
    path('api/schemes/', include('apps.schemes.urls')),
    path('api/analyzer/', include('apps.analyzer.urls')),
    path('api/grievances/', include('apps.grievances.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
]

# Static files delivery in development
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
