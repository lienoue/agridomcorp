from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, GeometricFigure, Classe
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

CustomUser = get_user_model()


# ============================================================
# FORMULAIRE DE CRÉATION DE COMPTE (général)
# ============================================================
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse mail")
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de naissance"
    )
    is_enseignant = forms.BooleanField(
        required=False,
        label="👩‍🏫 Je suis enseignant",
        help_text="Les enseignants peuvent créer des classes et suivre leurs élèves."
    )

    # ✅ NOUVEAUX CHAMPS (classe)
    est_dans_classe = forms.BooleanField(
        required=False,
        label="🎓 Je suis dans une classe",
        help_text="Coche si tu veux rejoindre une classe avec un code fourni par ton professeur."
    )
    code_classe = forms.CharField(
        required=False,
        max_length=20,
        label="Code de classe",
        help_text="Renseigne le code fourni par ton professeur.",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: A1B2C3D4',
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'location', 'birth_date', 'is_enseignant')

    # ------------------------------------------------------------
    # VALIDATIONS
    # ------------------------------------------------------------
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 5:
            raise forms.ValidationError("Le nom d'utilisateur doit contenir au moins 5 caractères.")
        if len(username) > 30:
            raise forms.ValidationError("Le nom de l'utilisateur ne doit pas dépasser 30 caractères.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("L'adresse email est obligatoire.")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Adresse email invalide.")
        if len(email) > 100:
            raise forms.ValidationError("L'adresse email ne doit pas dépasser 100 caractères.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("Le prénom est obligatoire.")
        if len(first_name) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Le nom est obligatoire.")
        if len(last_name) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        est_dans_classe = cleaned_data.get('est_dans_classe')
        code_classe = cleaned_data.get('code_classe')

        # ✅ Si l'utilisateur dit qu'il est dans une classe → code obligatoire
        if est_dans_classe and not code_classe:
            self.add_error('code_classe', "Veuillez saisir le code de votre classe.")

        # ✅ Vérifier que le code est valide
        if est_dans_classe and code_classe:
            try:
                classe = Classe.objects.get(code=code_classe.upper())
                cleaned_data['classe_obj'] = classe
            except Classe.DoesNotExist:
                self.add_error('code_classe', "❌ Code de classe invalide.")

        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ============================================================
# FORMULAIRE PARCELLE
# ============================================================
class FigureForm(forms.ModelForm):
    class Meta:
        model = GeometricFigure
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


# ============================================================
# FORMULAIRE INSCRIPTION ÉLÈVE (avec code de classe)
# ============================================================
class InscriptionEleveForm(UserCreationForm):
    """Formulaire d'inscription pour les élèves avec code de classe (obligatoire)"""

    code_classe = forms.CharField(
        max_length=20,
        label="Code de la classe",
        help_text="Entrez le code donné par votre professeur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: ABC12345'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ton@email.com'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'code_classe')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ton pseudo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})

    def clean_code_classe(self):
        """Vérifie que le code de classe existe"""
        code = self.cleaned_data.get('code_classe', '').upper()
        if not Classe.objects.filter(code=code).exists():
            raise forms.ValidationError("❌ Code de classe invalide.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.mode_junior = True
        if commit:
            user.save()
        return user