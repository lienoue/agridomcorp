# vegetables_fruits/tasks.py
from background_task import background
from django.utils import timezone
from .models import GeometricFigure, AlerteMeteo
from django.conf import settings
import requests


@background(schedule=3600)  # toutes les heures
def verifier_alertes_meteo_background():
    SEUILS = {
        'gel': 0,
        'canicule': 35,
    }

    figures = GeometricFigure.objects.filter(adresse_lat__isnull=False, adresse_lng__isnull=False)

    for figure in figures:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={figure.adresse_lat}&lon={figure.adresse_lng}&units=metric&lang=fr&appid={settings.OPENWEATHER_API_KEY}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']

                if temp <= SEUILS['gel']:
                    AlerteMeteo.objects.create(
                        utilisateur=figure.user,
                        figure=figure,
                        type_alerte='gel',
                        message=f"❄️ Alerte gel ! Température : {temp}°C.",
                        temperature=temp,
                        date_declenchement=timezone.now()
                    )

                if temp >= SEUILS['canicule']:
                    AlerteMeteo.objects.create(
                        utilisateur=figure.user,
                        figure=figure,
                        type_alerte='canicule',
                        message=f"🌡️ Alerte canicule ! Température : {temp}°C.",
                        temperature=temp,
                        date_declenchement=timezone.now()
                    )
        except Exception as e:
            print(f"Erreur: {e}")