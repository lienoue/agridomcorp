"""
Middleware pour logger les connexions et détecter les abus
"""

from django.utils import timezone
from datetime import timedelta
from .models import ConnexionLog
import logging

logger = logging.getLogger(__name__)


class ConnexionLogMiddleware:
    """
    Middleware qui enregistre chaque connexion d'un utilisateur authentifié
    et détecte les comportements suspects.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Logger SEULEMENT si l'utilisateur est authentifié
        if request.user.is_authenticated:
            self.log_connexion(request)

        response = self.get_response(request)
        return response

    def log_connexion(self, request):
        """Enregistre la connexion et détecte les abus"""

        try:
            # ✅ Récupérer l'IP
            ip = self.get_client_ip(request)

            # ✅ Récupérer le User Agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

            # ✅ Récupérer le device_id (cookie)
            device_id = request.COOKIES.get('device_id', None)

            # ✅ Vérifier si c'est une nouvelle connexion (pas de log dans les 5 dernières minutes)
            derniere_connexion = ConnexionLog.objects.filter(
                utilisateur=request.user
            ).order_by('-date_connexion').first()

            if derniere_connexion:
                temps_ecoule = timezone.now() - derniere_connexion.date_connexion
                if temps_ecoule < timedelta(minutes=5):
                    # Ne pas logger si c'est la même session
                    if derniere_connexion.ip == ip:
                        return

            # ✅ Détecter les comportements suspects
            est_suspect = False
            raison = ""

            # Règle 1 : Plus de 3 IP différentes en 24h
            il_y_a_24h = timezone.now() - timedelta(hours=24)
            ips_recentes = ConnexionLog.objects.filter(
                utilisateur=request.user,
                date_connexion__gte=il_y_a_24h
            ).values_list('ip', flat=True).distinct()

            if len(set(list(ips_recentes) + [ip])) > 3:
                est_suspect = True
                raison = f"Plus de 3 IP différentes en 24h : {len(set(list(ips_recentes) + [ip]))}"

            # Règle 2 : Plus de 5 appareils différents en 7 jours
            il_y_a_7j = timezone.now() - timedelta(days=7)
            appareils_recents = ConnexionLog.objects.filter(
                utilisateur=request.user,
                date_connexion__gte=il_y_a_7j
            ).exclude(device_id__isnull=True).values_list('device_id', flat=True).distinct()

            if device_id and len(set(list(appareils_recents) + [device_id])) > 5:
                est_suspect = True
                raison = f"Plus de 5 appareils différents en 7 jours"

            # ✅ Créer le log
            ConnexionLog.objects.create(
                utilisateur=request.user,
                ip=ip,
                user_agent=user_agent,
                device_id=device_id,
                est_suspect=est_suspect,
                raison_suspicion=raison
            )

            if est_suspect:
                logger.warning(
                    f"⚠️ Connexion suspecte : {request.user.username} "
                    f"(IP: {ip}, Raison: {raison})"
                )

        except Exception as e:
            logger.error(f"❌ Erreur log connexion : {e}")

    def get_client_ip(self, request):
        """Récupère l'IP du client (gère les proxys)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip