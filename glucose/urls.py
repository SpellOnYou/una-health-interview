from django.urls import path
from .views import GlucoseLevelListView, GlucoseLevelDetailView

# URL routing configuration for the API endpoints
urlpatterns = [
    path('levels/', GlucoseLevelListView.as_view(), name='glucose-levels'),  # List view with optional filters
    path('levels/<str:id>/', GlucoseLevelDetailView.as_view(), name='glucose-level-detail'),  # Detail view
]