import threading
import time
import firebase_admin
from firebase_admin import credentials, db
from AQ.models import SensorReading  # your model
from django.utils.timezone import make_aware
from datetime import datetime
import pytz
import os

running = True  # Global flag to control thread

# Initialize Firebase App
if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'secret_firebase.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://airsense-1a319-default-rtdb.firebaseio.com/'   # your database URL
    })

def fetch_and_save_firebase_data():
    while running:
        try:
            ref = db.reference('/AQMonitor/logs')  # logs path where your ESP32 stores data
            data = ref.get()

            if data:
                for timestamp, entry in data.items():
                    # Check if this entry already exists
                    if not SensorReading.objects.filter(timestamp=entry['timestamp']).exists():
                        SensorReading.objects.create(
                            temperature=entry['temperature'],
                            humidity=entry['humidity'],
                            ppm=entry['ppm'],
                            timestamp=make_aware(datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"))
                        )
                        print(f"Synced entry: {entry['timestamp']}")
            else:
                print("No data found in Firebase.")
        
        except Exception as e:
            print(f"Error syncing data: {e}")

        time.sleep(5)  # Wait 5 seconds before next check

def start_sync_thread():
    thread = threading.Thread(target=fetch_and_save_firebase_data)
    thread.daemon = True
    thread.start()
