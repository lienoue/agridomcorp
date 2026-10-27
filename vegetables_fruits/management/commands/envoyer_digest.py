# vegetables_fruits/management/commands/envoyer_digests.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import date, timedelta

from vegetables_fruits.models import DigestMeteo


class Command(BaseCommand):
    help = "Envoie les digests météo quotidiens (1 email par utilisateur)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help="Date des digests à envoyer (format YYYY-MM-DD). Par défaut : hier.",
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Simule l'envoi sans envoyer d'email.",
        )

    def handle(self, *args, **options):
        # Date des digests à traiter
        if options['date']:
            try:
                cible = date.fromisoformat(options['date'])
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    f"❌ Format de date invalide : {options['date']} (attendu YYYY-MM-DD)"
                ))
                return
        else:
            cible = date.today() - timedelta(days=1)

        dry_run = options['dry_run']

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n📧 Envoi des digests météo du {cible.strftime('%d/%m/%Y')}"
        ))
        self.stdout.write("=" * 60)

        if dry_run:
            self.stdout.write(self.style.WARNING("🧪 Mode DRY-RUN activé (aucun email envoyé)\n"))

        # Récupérer les digests non envoyés de la date cible
        digests = DigestMeteo.objects.filter(
            date=cible,
            envoye=False,
        ).select_related('utilisateur')

        self.stdout.write(f"📋 {digests.count()} digest(s) à traiter\n")

        envoyes = 0
        vides = 0
        erreurs = 0

        for digest in digests:
            user = digest.utilisateur

            # Skip si vide
            if digest.est_vide:
                vides += 1
                self.stdout.write(f" ⏭️ {user.username} : digest vide → ignoré")
                digest.envoye = True # Marquer comme traité
                if not dry_run:
                    digest.save()
                continue

            # Skip si pas d'email
            if not user.email:
                erreurs += 1
                self.stdout.write(self.style.WARNING(
                    f" ⚠️ {user.username} : pas d'email → ignoré"
                ))
                continue

            # Construire l'email
            try:
                html_content = render_to_string(
                    'emails/digest_meteo.html',
                    {
                        'user': user,
                        'digest': digest,
                        'alertes': digest.alertes,
                        'nb_alertes': digest.total_alertes,
                    }
                )

                # Sujet
                total = digest.total_alertes
                critiques = sum(1 for a in digest.alertes if a.get('est_critique'))
                if critiques > 0:
                    sujet = f"🌦️ {total} alerte(s) météo — dont {critiques} critique(s)"
                else:
                    sujet = f"🌦️ {total} alerte(s) météo dans votre jardin"

                # Message texte (fallback)
                texte = f"Bonjour {user.username},\n\n"
                texte += f"Vous avez {total} alerte(s) météo dans votre jardin :\n\n"
                for a in digest.alertes:
                    prefix = "🚨 CRITIQUE" if a.get('est_critique') else "🌦️"
                    texte += f"{prefix} {a['message']}\n"
                texte += "\nConsultez l'application pour plus de détails.\n\n"
                texte += "L'équipe Agriculture 2.0"

                if dry_run:
                    self.stdout.write(f" 🧪 {user.username} : {total} alerte(s) → simulé")
                else:
                    send_mail(
                        subject=sujet,
                        message=texte,
                        html_message=html_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    digest.envoye = True
                    digest.date_envoi = timezone.now()
                    digest.save()
                    self.stdout.write(self.style.SUCCESS(
                        f" ✅ {user.username} : {total} alerte(s) envoyée(s)"
                    ))

                envoyes += 1

            except Exception as e:
                erreurs += 1
                self.stdout.write(self.style.ERROR(
                    f" ❌ {user.username} : erreur → {e}"
                ))

        # ============================================================
        # RAPPORT
        # ============================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("📊 RAPPORT"))
        self.stdout.write("=" * 60)
        self.stdout.write(f" ✅ Envoyés : {envoyes}")
        self.stdout.write(f" ⏭️ Vides : {vides}")
        self.stdout.write(f" ❌ Erreurs : {erreurs}")
        self.stdout.write(f" 📊 Total : {digests.count()}")
        self.stdout.write("")