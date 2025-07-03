from django.db import models

class SensorReading(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ppm = models.FloatField()  # Air Quality Index (e.g., ppm or similar)
    
    def __str__(self):
        return f"{self.timestamp} - {self.temperature}°C, {self.humidity}%, {self.ppm}ppm"
