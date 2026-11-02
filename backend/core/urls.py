"""
Core URL Configuration for NyayaSetu AI
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
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

urlpatterns = [
    # Direct Asset & Favicon routes
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend' / 'assets'}),
    re_path(r'^(?:[^/]+/)*wb_emblem\.webp$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'wb_emblem.webp'}),
    re_path(r'^favicon\.ico$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'wb_emblem.webp'}),
    re_path(r'^sw\.js$', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'sw.js'}),

    # Frontend Pages (Support both clean URLs and .html filenames for complete compatibility)
    path('', TemplateView.as_view(template_name='Landing.html'), name='landing'),
    re_path(r'^(?:Landing\.html)?$', TemplateView.as_view(template_name='Landing.html')),
    
    re_path(r'^home/?$', TemplateView.as_view(template_name='Home.html'), name='home'),
    re_path(r'^Home\.html$', TemplateView.as_view(template_name='Home.html')),

    re_path(r'^login/?$', TemplateView.as_view(template_name='Login.html'), name='login'),
    re_path(r'^Login\.html$', TemplateView.as_view(template_name='Login.html')),

    re_path(r'^register/?$', TemplateView.as_view(template_name='Register.html'), name='register'),
    re_path(r'^Register\.html$', TemplateView.as_view(template_name='Register.html')),

    re_path(r'^notice-explainer/?$', TemplateView.as_view(template_name='notice_explainer.html'), name='notice_explainer'),
    re_path(r'^notice_explainer\.html$', TemplateView.as_view(template_name='notice_explainer.html')),

    re_path(r'^eligibility-wizard/?$', TemplateView.as_view(template_name='EligibilityWizard.html'), name='eligibility_wizard'),
    re_path(r'^EligibilityWizard\.html$', TemplateView.as_view(template_name='EligibilityWizard.html')),

    re_path(r'^grievance-drafter/?$', TemplateView.as_view(template_name='GrievanceDrafter.html'), name='grievance_drafter'),
    re_path(r'^GrievanceDrafter\.html$', TemplateView.as_view(template_name='GrievanceDrafter.html')),

    path('admin/', admin.site.urls),
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
