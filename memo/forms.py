from django import forms
import datetime
from .models import Memoire

class MemoireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemoireForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput) or isinstance(field.widget, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = Memoire
        fields = '__all__'

""" class Memoire(forms.Form):
    current_year = datetime.datetime.now().year
    year_choices = [(year, str(year)) for year in range(current_year, current_year - 10, -1)]
    
    theme = forms.CharField(max_length=250, required=True)
	contexte = forms.CharField(widget=forms.Textarea)
	problematique = forms.CharField(widget=forms.Textarea)
	objectifs = forms.CharField(widget=forms.Textarea)
	resultats = forms.CharField(widget=forms.Textarea)
	planing = forms.CharField(widget=forms.Textarea, null=True, blank=True)
	nom_entreprise = forms.CharField(max_length=250, null=True, blank=True)
	statut = forms.BooleanField(default=0)
	cote = forms.CharField(max_length=250, null=True, blank=True)
	tags = forms.CharField(max_length=250, null=True, blank=True)
	fichier = forms.FileField(upload_to='memoires/', null=True, blank=True)
	etudiant = forms.ForeignKey(Etudiant, on_delete=forms.CASCADE, related_name='auteur')
	directeur = forms.ForeignKey(Enseignant, on_delete=forms.CASCADE, related_name='directeur', null=True, blank=True)
	annee = forms.ChoiceField(choices=year_choices, initial=current_year)
"""


