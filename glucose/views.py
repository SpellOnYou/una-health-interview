from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import GlucoseLevel
from .serializers import GlucoseLevelSerializer

# API view to retrieve a list of glucose levels with filtering, pagination, and sorting capabilities
class GlucoseLevelListView(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer  # Defines the serializer used for response formatting
    queryset = GlucoseLevel.objects.all()  # Base queryset retrieving all records
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Enables filtering and ordering
    filterset_fields = ['user_id']  # Allows filtering based on user_id
    ordering_fields = ['timestamp']  # Allows sorting by timestamp

# API view to retrieve details of a specific glucose level reading by its ID
class GlucoseLevelDetailView(generics.RetrieveAPIView):
    serializer_class = GlucoseLevelSerializer  # Uses the same serializer as the list view
    queryset = GlucoseLevel.objects.all()  # Retrieves all records to find a specific one
