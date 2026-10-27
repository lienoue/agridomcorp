from django_cron import CronJobBase, Schedule
from django.core.management import call_command

class VerifierAlertesTraitementsCron(CronJobBase):
    RUN_EVERY_MINS = 60 * 6 # Toutes les 6 heures

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'vegetables_fruits.verifier_alertes_traitements_cron'

    def do(self):
        call_command('verifier_alertes_traitements')

class SnapshotValeurJardinCron(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 30 # ~1 fois par mois
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'vegetables_fruits.snapshot_valeur_jardin_cron'

    def do(self):
        call_command('snapshot_valeur_jardin')


class UpdateTauxChangeCron(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 30 # ~1 fois par mois
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'vegetables_fruits.update_taux_change_cron'

    def do(self):
        call_command('update_taux_change')