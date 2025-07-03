"""
URL configuration for aq_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from AQ.views import receive_sensor_data
from django.conf.urls.static import static
from AQ.views import historical_data
from AQ.views import trigger_ota_update
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/sensor/", receive_sensor_data, name="sensor-data"),
    path("api/historical/", historical_data, name='historical-data'),
    path('ota/update/', trigger_ota_update, name='ota_update'),

]

urlpatterns += static('/firmware/', document_root='firmware')
