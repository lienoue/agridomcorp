# vegetables_fruits/management/commands/envoyer_rappels.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import date
from ...models import RappelUtilisateur


class Command(BaseCommand):
    help = 'Envoie les rappels email aux utilisateurs'

    def handle(self, *args, **kwargs):
        aujourdhui = date.today()
        rappels = RappelUtilisateur.objects.filter(
            actif=True,
            date_prochain_rappel__lte=aujourdhui
        )

        envoye = 0
        for rappel in rappels:
            # Construire le message
            if rappel.type_rappel == 'semis':
                sujet = f"🌱 Rappel semis - {rappel.culture or 'Vos cultures'}"
                message = f"Bonjour,\n\nC'est le moment de semer vos {rappel.culture or 'cultures'} !\n\n"
                if rappel.message_personnalise:
                    message += f"💡 {rappel.message_personnalise}\n\n"
                message += "🌿 Connectez-vous à Agriculture 2.0 pour suivre vos plantations.\n\nL'équipe Agriculture 2.0"

            elif rappel.type_rappel == 'arrosage':
                sujet = f"💧 Rappel arrosage - {rappel.culture or 'Vos plantes'}"
                message = f"Bonjour,\n\nPensez à arroser vos {rappel.culture or 'plantes'} !\n\n"
                if rappel.message_personnalise:
                    message += f"💡 {rappel.message_personnalise}\n\n"
                message += "💧 L'équipe Agriculture 2.0"

            elif rappel.type_rappel == 'recolte':
                sujet = f"🍅 Rappel récolte - {rappel.culture or 'Vos légumes'}"
                message = f"Bonjour,\n\nVos {rappel.culture or 'légumes'} sont prêts à être récoltés !\n\n"
                if rappel.message_personnalise:
                    message += f"💡 {rappel.message_personnalise}\n\n"
                message += "🍅 L'équipe Agriculture 2.0"

            else:
                sujet = f"📋 Rappel jardinage - {rappel.get_type_rappel_display()}"
                message = f"Bonjour,\n\n{rappel.message_personnalise or 'Pensez à votre jardin !'}\n\nL'équipe Agriculture 2.0"

            # Envoyer l'email
            if rappel.utilisateur.email:
                try:
                    send_mail(
                        subject=sujet,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[rappel.utilisateur.email],
                        fail_silently=False,
                    )
                    envoye += 1
                    print(f"✅ Email envoyé à {rappel.utilisateur.email}")
                except Exception as e:
                    print(f"❌ Erreur pour {rappel.utilisateur.email}: {e}")

            # Mettre à jour la date du prochain rappel
            if rappel.frequence_jours > 0:
                from datetime import timedelta
                rappel.date_prochain_rappel = aujourdhui + timedelta(days=rappel.frequence_jours)
                rappel.dernier_envoi = timezone.now()
                rappel.save()
            else:
                rappel.actif = False
                rappel.save()

        self.stdout.write(self.style.SUCCESS(f'✅ {envoye} rappel(s) envoyé(s)'))
