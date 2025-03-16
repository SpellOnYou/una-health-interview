from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from .models import GlucoseLevel
from .serializers import GlucoseLevelSerializer

# API view to retrieve a list of glucose levels with filtering, pagination, and sorting capabilities
class GlucoseLevelListView(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user_id']
    ordering_fields = ['timestamp']  # Allows sorting by timestamp

    def get_queryset(self):
        """
        Retrieve glucose levels for a given user_id, 
        with optional filtering by start/stop timestamps.
        Supports pagination, sorting, and limiting.
        """
        queryset = GlucoseLevel.objects.all()

        # Get query parameters
        user_id = self.request.query_params.get('user_id', None)
        start_time = self.request.query_params.get('start', None)
        stop_time = self.request.query_params.get('stop', None)
        limit = self.request.query_params.get('limit', None)  # Custom limit

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # Filter by timestamp range if provided
        if start_time:
            parsed_start = parse_datetime(start_time)
            if parsed_start:
                queryset = queryset.filter(timestamp__gte=parsed_start)

        if stop_time:
            parsed_stop = parse_datetime(stop_time)
            if parsed_stop:
                queryset = queryset.filter(timestamp__lte=parsed_stop)

        # Apply custom limit if provided
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]

        return queryset

# API view to retrieve details of a specific glucose level reading by its ID
class GlucoseLevelDetailView(generics.RetrieveAPIView):
    serializer_class = GlucoseLevelSerializer

    def get(self, request, id, *args, **kwargs):
        """
        Retrieve glucose levels for a given user_id.
        """
        glucose_levels = GlucoseLevel.objects.filter(id=id)

        if not glucose_levels.exists():
            return Response({"error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GlucoseLevelSerializer(glucose_levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

