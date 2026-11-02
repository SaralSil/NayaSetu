"""
Core URL Configuration for NyayaSetu AI
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
from apps.analyzer.views import ChatbotAssistantView

def api_health_check(request):
    return JsonResponse({
        "status": "active",
        "service": "NyayaSetu AI Backend",
        "version": "1.0.0",
        "description": "West Bengal Government Scheme & Citizen Rights Assistant API"
    })

urlpatterns = [
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
