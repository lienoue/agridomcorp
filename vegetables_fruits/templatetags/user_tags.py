from django import template
from vegetables_fruits.views import est_mineur, get_user_location, get_age_majorite

register = template.Library()

@register.filter
def mineur(user):
    """Retourne True si l'utilisateur est mineur"""
    if not user or not user.is_authenticated:
        return False
    return user.mode_junior # ou un calcul basé sur birth_date

@register.filter
def location_utilisateur(user):
    return get_user_location(user)

@register.filter
def age_majorite(user):
    location = get_user_location(user)
    return get_age_majorite(location)

@register.filter
def age_utilisateur(user):
    if not user or not user.birth_date:
        return None
    from datetime import date
    today = date.today()
    age = today.year - user.birth_date.year - (
        (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
    )
    return age


@register.filter
def get_item(dictionary, key):
    """
    Récupère un élément d'un dictionnaire par sa clé
    Usage: {{ dictionnaire|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def est_eleve_en_classe(user):
    return hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None