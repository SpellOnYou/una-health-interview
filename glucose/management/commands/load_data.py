import os
import pandas as pd
from django.core.management.base import BaseCommand
from glucose.models import GlucoseLevel

# Management command to load glucose data from CSV files into the database
class Command(BaseCommand):
    help = "Load glucose levels from CSV files"  # Command description

    def handle(self, *args, **kwargs):
        data_path = "data/"  # Directory where CSV files are stored
        
        # Iterate through all CSV files in the data directory
        for file in os.listdir(data_path):
            if file.endswith('.csv'):  # Process only CSV files
                user_id = file.replace(".csv", "")  # Extract user_id from filename
                df = pd.read_csv(os.path.join(data_path, file))  # Read CSV data into Pandas DataFrame
                
                # Loop through each row in the DataFrame and create a GlucoseLevel entry
                for _, row in df.iterrows():
                    GlucoseLevel.objects.create(
                        user_id=user_id,  # Assign extracted user_id
                        timestamp=row['timestamp'],  # Set timestamp from CSV
                        value=row['value']  # Set glucose level value from CSV
                    )
        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))  # Confirmation message
