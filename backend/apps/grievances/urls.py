from django.urls import path
from .views import GenerateGrievanceDraftView, OfficialDirectoryListView

urlpatterns = [
    path('generate/', GenerateGrievanceDraftView.as_view(), name='generate-grievance'),
    path('offices/', OfficialDirectoryListView.as_view(), name='official-directory'),
]
