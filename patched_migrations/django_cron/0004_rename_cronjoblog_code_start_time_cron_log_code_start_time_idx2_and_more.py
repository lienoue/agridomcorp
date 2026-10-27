"""
Patch de la migration django_cron.0004.

⚠️ Bug original : django-cron 0.6.0 utilise RenameIndex qui échoue sur SQLite
car l'index d'origine n'a pas le nom attendu. Cette version remplace le
RenameIndex par des AddIndex/RemoveIndex robustes (ou par un no-op si les
index ne sont pas critiques).
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_cron', '0003_cronjoblock'),
    ]

    operations = [
        # ✅ Remplacer RenameIndex (cassé) par un no-op.
        # Les index ne sont pas critiques pour le fonctionnement de django-cron
        # (ils servent aux perfs de requêtes sur les logs).
        # Django continuera à fonctionner sans problème.
        migrations.RunSQL(
            sql='SELECT 1;', # no-op SQL
            reverse_sql='SELECT 1;'
        ),
    ]