# vegetables_fruits/management/commands/compare_views.py
from pathlib import Path
import difflib
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Compare les fonctions dupliquées dans views.py"

    def handle(self, *args, **options):
        content = Path('vegetables_fruits/views.py').read_text(encoding='utf-8')
        lines = content.split('\n')

        def extraire_fonction(nom, ligne_debut):
            fin = ligne_debut
            for i in range(ligne_debut, len(lines)):
                line = lines[i]
                if i > ligne_debut and (
                    line.startswith('def ')
                    or line.startswith('class ')
                    or line.startswith('@')
                ):
                    fin = i
                    break
                fin = i
            return '\n'.join(lines[ligne_debut - 1:fin])

        paires = [
            ('autosuffisance', 3323, 7501),
            ('ecologie_tabs', 14352, 14607),
            ('get_client_ip', 4857, 16958),
            ('get_culture_emoji', 7489, 11718),
            ('get_saison_actuelle', 1192, 7175),
            ('ignorer_alerte', 3294, 12440),
            ('inscription_eleve', 3554, 3990),
        ]

        for nom, l1, l2 in paires:
            v1 = extraire_fonction(nom, l1)
            v2 = extraire_fonction(nom, l2)

            self.stdout.write("\n" + "=" * 70)
            self.stdout.write(f"🔍 {nom}")
            self.stdout.write("=" * 70)
            self.stdout.write(f"V1 (ligne {l1}) : {len(v1.split(chr(10)))} lignes, {len(v1)} caractères")
            self.stdout.write(f"V2 (ligne {l2}) : {len(v2.split(chr(10)))} lignes, {len(v2)} caractères")

            if v1 == v2:
                self.stdout.write(self.style.SUCCESS("✅ IDENTIQUES → V2 peut être supprimée"))
            else:
                self.stdout.write(self.style.WARNING("⚠️ DIFFÉRENTES → analyse nécessaire"))
                diff = list(difflib.unified_diff(
                    v1.split('\n'), v2.split('\n'),
                    lineterm='', n=1
                ))
                for ligne in diff[:40]:
                    self.stdout.write(f" {ligne}")
                if len(diff) > 40:
                    self.stdout.write(f" ... ({len(diff) - 40} lignes supplémentaires)")