from vegetables_fruits.models import ChronologieCulture, Fruit, Vegetable, Culture
from datetime import timedelta

for chrono in ChronologieCulture.objects.all():
    nom = chrono.culture_nom
    jours = None
    emoji = None

    f = Fruit.objects.filter(nom__iexact=nom).first()
    if f and f.jours_recolte:
        jours = f.jours_recolte
        emoji = f.get_emoji()
    else:
        v = Vegetable.objects.filter(nom__iexact=nom).first()
        if v and v.jours_recolte:
            jours = v.jours_recolte
            emoji = v.get_emoji()
        else:
            c = Culture.objects.filter(nom__iexact=nom).first()
            if c and c.duree_culture_max_jours:
                jours = c.duree_culture_max_jours

    if jours and chrono.date_semis:
        chrono.date_recolte_prevue = chrono.date_semis + timedelta(days=jours)
        if emoji:
            chrono.culture_emoji = emoji
        chrono.calculer_progression()
        print(f"✅ {nom} → {jours}j → récolte {chrono.date_recolte_prevue}")
    else:
        print(f"⚠️ {nom} → durée introuvable, conservée")