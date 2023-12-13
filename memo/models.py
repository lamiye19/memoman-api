from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur(AbstractUser):
	date_naiss = models.DateField()
	telephone = models.CharField(max_length=20)
	adresse = models.CharField(max_length=15)

	def __str__(self) -> str:
		return super().__str__()
	

class Etudiant(models.Model):
	utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
	num_etudiant = models.CharField(max_length=15)


	def __str__(self):
		return f"Étudiant {self.utilisateur.username}"
	


class Enseignant(models.Model):
	utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
	code_enseignant = models.CharField(max_length=15)
	matiere = models.CharField(max_length=15)

	def __str__(self):
		return f"Enseignant {self.utilisateur.username}"

class Niveau(models.Model):
	libelle = models.CharField(max_length=255)
	code = models.CharField(max_length=2)



