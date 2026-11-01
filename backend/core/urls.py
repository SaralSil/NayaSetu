"""
Core URL Configuration for NyayaSetu AI
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_health_check(request):
    return JsonResponse({
        "status": "active",
        "service": "NyayaSetu AI Backend",
        "version": "1.0.0",
        "description": "West Bengal Government Scheme & Citizen Rights Assistant API"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', api_health_check, name='api_health_check'),
    
    # Core API Endpoints
    path('api/schemes/', include('apps.schemes.urls')),
    path('api/analyzer/', include('apps.analyzer.urls')),
    path('api/grievances/', include('apps.grievances.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
]
