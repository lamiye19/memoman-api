from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(Enseignant)
admin.site.register(Memoire)