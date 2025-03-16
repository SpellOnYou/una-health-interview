from django.urls import path
from .views import GlucoseLevelListView, GlucoseLevelDetailView, GlucoseLevelCreateView, GlucoseLevelExportView

# URL routing configuration for the API endpoints
urlpatterns = [
    path('levels/', GlucoseLevelListView.as_view(), name='glucose-levels'),  # List view with optional filters
    path('levels/<str:id>/', GlucoseLevelDetailView.as_view(), name='glucose-level-detail'),  # Detail view
    path('upload/', GlucoseLevelCreateView.as_view(), name='glucose-level-upload'),  # New Upload Endpoint
    path('export/', GlucoseLevelExportView.as_view(), name='glucose-level-export'),  # CSV Export Endpoint
]
