from celery import shared_task


@shared_task
def verifier_alertes_meteo():
    from .views import verifier_alertes_meteo as verifier
    verifier()