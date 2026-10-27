# Dans le shell Django
from vegetables_fruits.models import Eleve, ProgressionJunior

for eleve in Eleve.objects.all():
    progression, _ = ProgressionJunior.objects.get_or_create(user=eleve.user)
    progression.points = eleve.points
    progression.niveau = eleve.niveau
    progression.save()
    for badge in eleve.badges.all():
        progression.badges.add(badge)