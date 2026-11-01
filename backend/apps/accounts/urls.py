from django.urls import path
from .views import UserProfileView, SavedSchemeListCreateView, SavedSchemeDetailView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('saved-schemes/', SavedSchemeListCreateView.as_view(), name='saved-schemes-list'),
    path('saved-schemes/<int:pk>/', SavedSchemeDetailView.as_view(), name='saved-scheme-detail'),
]
