import logging
import os
import pandas as pd
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from glucose.models import GlucoseLevel

# Management command to load glucose data from CSV files into the database
class Command(BaseCommand):
    help = "Load glucose levels from CSV files"  # Command description
    def add_arguments(self, parser):
        parser.add_argument('--data-path', type=str)

    def handle(self, *_, **options):
        data_path = options['data_path']  # Directory where CSV files are stored
        
        files_processed = 0

        # Loop through all CSV files in the directory
        for file in os.listdir(data_path):
            if file.endswith('.csv'):
                file_path = os.path.join(data_path, file)

                try:
                    # Skipping the first row as it seems to contain the metadata
                    df = pd.read_csv(file_path, delimiter=",", encoding="utf-8", skiprows=1)

                    # Extract relevant columns while replacing the column names
                    df = df.rename(columns={
                        "Gerätezeitstempel": "timestamp",
                        "Glukosewert-Verlauf mg/dL": "glucose_value"
                    })

                    # Convert timestamp to a standard format
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%Y %H:%M").apply(make_aware)

                    # Extract user_id from filename (assuming it's stored that way)
                    user_id = os.path.splitext(file)[0]

                    # Iterate through each row and save to the database
                    glucose_objects = []
                    for _, row in df.iterrows():
                        if not pd.isna(row['glucose_value']):  # Ensure valid glucose values
                            glucose_objects.append(
                                GlucoseLevel(
                                    user_id=user_id,
                                    timestamp=row['timestamp'],
                                    value=row['glucose_value']
                                )
                            )

                    # Bulk insert into database for efficiency
                    GlucoseLevel.objects.bulk_create(glucose_objects)
                    files_processed += 1

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing {file}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {files_processed} CSV files"))