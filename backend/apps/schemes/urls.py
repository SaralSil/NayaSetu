from django.urls import path
from .views import SchemeListView, SchemeDetailView, DepartmentListView, EligibilityWizardView

urlpatterns = [
    path('', SchemeListView.as_view(), name='scheme-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('check-eligibility/', EligibilityWizardView.as_view(), name='check-eligibility'),
    path('<slug:slug>/', SchemeDetailView.as_view(), name='scheme-detail'),
]
