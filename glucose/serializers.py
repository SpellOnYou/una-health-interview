from rest_framework import serializers
from .models import GlucoseLevel

# Serializer to convert GlucoseLevel model instances to JSON format
class GlucoseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseLevel  # Specifies which model to serialize
        fields = '__all__'  # Includes all fields in the serialization output