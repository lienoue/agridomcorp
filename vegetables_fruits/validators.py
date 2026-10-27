from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexityValidator:
    """
    Exige au moins une majuscule, une minuscule, un chiffre et un caractère spécial.
    """
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une majuscule."),
                code='password_no_upper',
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une minuscule."),
                code='password_no_lower',
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code='password_no_digit',
            )
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(char in special_chars for char in password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*...)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins 10 caractères, "
            "dont une majuscule, une minuscule, un chiffre et un caractère spécial."
        )