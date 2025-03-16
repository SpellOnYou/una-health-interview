# Create your models here.
from django.db import models

# Model to store glucose level readings for users
class GlucoseLevel(models.Model):
    user_id = models.CharField(max_length=255)  # Stores the unique identifier for a user
    timestamp = models.DateTimeField()  # Stores the time when the glucose reading was taken
    value = models.FloatField()  # Stores the glucose level value as a floating point number

    class Meta:
        ordering = ['timestamp']  # Default ordering by timestamp (oldest first)

    def __str__(self):
        return f"User: {self.user_id} - Glucose: {self.value} at {self.timestamp}"
