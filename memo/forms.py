from django import forms
import datetime
from .models import Memoire, Niveau, Utilisateur, Etudiant, Enseignant, Specialite
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm



class NiveauForm:
    class Meta:
        model = Niveau
        fields = ['libelle', 'specialite']

class MemoireForm(forms.ModelForm):
    class Meta:
        model = Memoire
        fields = '__all__'

    def __init__(self, *args, fields=None, **kwargs):
        super(MemoireForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput) or isinstance(field.widget, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-select file'
                field.widget.attrs['data-browse-on-zone-click'] = 'true'
            else:
                field.widget.attrs['class'] = 'form-control'

        def has_changed(self):
            # Override has_changed to consider only fields that have been changed
            return any(field in self.changed_data for field in self.fields.keys())

        if fields:
            # Si des champs sont spécifiés, utilisez-les
            allowed_fields = set(fields)
            existing_fields = set(self.fields.keys())
            for field_name in existing_fields - allowed_fields:
                del self.fields[field_name]


## creation des formulaires de creation de compte etudiant et enseignant 
        
class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'password1', 'password2', 'date_naiss', 'telephone', 'adresse')

class EtudiantCreationForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ('specialite', 'num_etudiant')

class EnseignantCreationForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ('code_enseignant', 'matiere')

class ConnexionForm(AuthenticationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'password']