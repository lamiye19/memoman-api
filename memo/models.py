from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur(AbstractUser):
	date_naiss = models.DateField(null=True)
	telephone = models.CharField(max_length=20, null=True, blank=True)
	adresse = models.CharField(max_length=15, null=True, blank=True)

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
	
class Memoire(models.Model):
	theme = models.CharField(max_length=250)
	contexte = models.TextField()
	problematique = models.TextField()
	objectifs = models.TextField()
	resultats = models.TextField()
	planing = models.TextField(null=True, blank=True)
	nom_entreprise = models.CharField(max_length=250, null=True, blank=True)
	statut = models.BooleanField(default=0)
	cote = models.CharField(max_length=250, null=True, blank=True)
	tags = models.CharField(max_length=250, null=True, blank=True)
	fichier = models.FileField(upload_to='memoires/', null=True, blank=True)
	etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='auteur')
	directeur = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='directeur', null=True, blank=True)
	annee = models.IntegerField(default=2023)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return f"Memoire {self.etudiant}"