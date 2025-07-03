from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SensorReading
from datetime import datetime
from django.db.models.functions import TruncHour
from .models import SensorReading
import os
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from firebase_admin import db

    
def get_firebase_db():
    """Helper function to get the Firebase database reference."""
    return db.reference()


@csrf_exempt
def receive_sensor_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            timestamp = data.get("timestamp")
            dt = datetime.fromisoformat(timestamp) if timestamp else datetime.now()

            SensorReading.objects.create(
                timestamp=dt,
                temperature=data.get("temperature", 0),
                humidity=data.get("humidity", 0),
                ppm=data.get("ppm", 0)
            )
            return JsonResponse({"status": "success"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def historical_data(request):
    try:
        days = int(request.GET.get('days', 7))
    except ValueError:
        days = 7

    interval = request.GET.get('interval', 'daily')
    end_datetime = timezone.now()
    start_datetime = end_datetime - timedelta(days=days)

    if interval == "hourly":
        readings = (
            SensorReading.objects
            .filter(timestamp__range=(start_datetime, end_datetime))
            .annotate(hour=TruncHour("timestamp"))
            .values("hour")
            .annotate(
                avg_temp=Avg("temperature"),
                avg_humidity=Avg("humidity"),
                avg_ppm=Avg("ppm")
            )
            .order_by("hour")
        )

        result = []
        for r in readings:
            timestamp_str = r["hour"].strftime("%Y-%m-%d %H:%M:%S")
            result.append([
                timestamp_str,
                round(r["avg_temp"], 2),
                round(r["avg_humidity"], 2),
                round(r["avg_ppm"], 2)
            ])
        return JsonResponse(result, safe=False)

    else:
        # Daily aggregation
        end_date = end_datetime.date()
        start_date = end_date - timedelta(days=days - 1)
        date_list = [start_date + timedelta(days=i) for i in range(days)]

        readings = (
            SensorReading.objects
            .filter(timestamp__date__range=(start_date, end_date))
            .values('timestamp__date')
            .annotate(
                avg_temp=Avg('temperature'),
                avg_humidity=Avg('humidity'),
                avg_ppm=Avg('ppm')
            )
        )

        reading_map = {r['timestamp__date']: r for r in readings}

        if readings:
            avg_temp = sum(r['avg_temp'] for r in readings) / len(readings)
            avg_humidity = sum(r['avg_humidity'] for r in readings) / len(readings)
            avg_ppm = sum(r['avg_ppm'] for r in readings) / len(readings)
        else:
            avg_temp = avg_humidity = avg_ppm = 0

        result = []
        for d in date_list:
            if d in reading_map:
                entry = reading_map[d]
                result.append([
                    d.strftime("%Y-%m-%d"),
                    round(entry['avg_temp'], 2),
                    round(entry['avg_humidity'], 2),
                    round(entry['avg_ppm'], 2),
                ])
            else:
                result.append([
                    d.strftime("%Y-%m-%d"),
                    round(avg_temp, 2),
                    round(avg_humidity, 2),
                    round(avg_ppm, 2),
                ])

        return JsonResponse(result, safe=False)
    
@csrf_exempt
def trigger_ota_update(request):
    if request.method == 'POST':
        delay = request.POST.get('delay')
        print(delay)
        if delay not in ['5', '10']:
            return JsonResponse({'status': 'error', 'message': 'Invalid delay selected.'})

        # Path to your firmware file
        firmware_path = rf'C:\Users\TahaK\Desktop\AQ Monitoring\AQ_back\aq_backend\firmware\MBSD_airq_{delay}s.ino.bin'
        firmware_filename = f'MBSD_airq_{delay}s.ino.bin'
        # Assuming you're serving /firmware/ through Django staticfiles or URL
        firmware_url = f"https://6fab-111-68-109-251.ngrok-free.app/firmware/{firmware_filename}"

        # Optionally check if file exists
        print(firmware_path)
        if not os.path.exists(firmware_path):
            return JsonResponse({'status': 'error', 'message': 'Firmware file not found.'})

        # Get a reference to the Firebase database
        firebase_ref = get_firebase_db()

        # Update the firmware URL in Firebase
        firebase_ref.child('AQMonitor').child('firmwareURL').set(firmware_url)

        # Return the firmware URL for ESP32
        return JsonResponse({'status': 'success', 'firmware_url': firmware_url})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
                        