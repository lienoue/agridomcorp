from django import template
from vegetables_fruits.services_dates import est_perenne

register = template.Library()

@register.filter
def est_arbre(culture_nom):
    """
    Retourne True si la culture est pérenne (arbre, arbuste, vigne).
    Utilisable dans les templates : {% if culture|est_arbre %}
    """
    if not culture_nom:
        return False
    return est_perenne(culture_nom)