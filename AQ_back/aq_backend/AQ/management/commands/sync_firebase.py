from django.core.management.base import BaseCommand
from AQ.models import SensorReading
from AQ.firebase_config import db
from datetime import datetime

class Command(BaseCommand):
    help = 'Sync Firebase data to PostgreSQL database'

    def handle(self, *args, **options):
        ref = db.reference('/AQMonitor/logs') 

        def parse_and_save(data):
            for key, value in data.items():
                try:
                    timestamp_str = value.get('timestamp')
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                    SensorReading.objects.update_or_create(
                        timestamp=timestamp,
                        defaults={
                            'temperature': value.get('temperature'),
                            'humidity': value.get('humidity'),
                            'ppm': value.get('ppm'),  # assuming 'ppm' maps to air_quality
                        }
                    )
                except Exception as e:
                    print(f"Error saving reading {key}: {e}")

        # Initial full sync
        data = ref.get()
        if data:
            parse_and_save(data)

        self.stdout.write(self.style.SUCCESS('Initial Firebase data synced.'))

        # 🔁 Real-time listener
        def listener(event):
            print(f"Realtime update: {event.event_type}")
            if event.data and isinstance(event.data, dict):
                parse_and_save({event.path.strip('/'): event.data})

        ref.listen(listener)
