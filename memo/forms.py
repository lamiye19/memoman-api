from django import forms
import datetime
from .models import Memoire, Niveau


class NiveauForm:
    class Meta:
        model = Niveau
        fields = ['libelle', 'specialite']

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
