import datetime
from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur(AbstractUser):
	date_naiss = models.DateField(null=True)
	telephone = models.CharField(max_length=20, null=True, blank=True)
	adresse = models.CharField(max_length=15, null=True, blank=True)

	def __str__(self) -> str:
		return super().__str__()
		


class Enseignant(models.Model):
	utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
	code_enseignant = models.CharField(max_length=15)
	matiere = models.CharField(max_length=15)

	def __str__(self):
		return f"Enseignant {self.utilisateur.username}"

	

class Niveau(models.Model):
	libelle = models.CharField(max_length=255)
	code = models.CharField(max_length=2)


class Specialite(models.Model):
	code = models.CharField(max_length=10)
	libelle = models.CharField(max_length=200)
	Niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='niveau_specialite')



class Etudiant(models.Model):
	utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
	specialite = models.OneToOneField(Specialite, on_delete=models.CASCADE)
	num_etudiant = models.CharField(max_length=15)


	def __str__(self):
		return f"Étudiant {self.utilisateur.username}"
	



class Memoire(models.Model):
	theme = models.CharField(max_length=250)
	contexte = models.TextField()
	problematique = models.TextField()
	objectifs = models.TextField()
	existant = models.TextField(null=True)
	resultats = models.TextField()
	planing = models.TextField(null=True, blank=True)
	nom_entreprise = models.CharField(max_length=250, null=True, blank=True)
	statut = models.BooleanField(null=True, blank=True)
	cote = models.CharField(max_length=250, null=True, blank=True)
	tags = models.CharField(max_length=250, null=True, blank=True)
	fichier = models.FileField(upload_to='memoires/', null=True, blank=True)
	etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='auteur', blank=True)
	directeur = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='directeur', null=True, blank=True)
	annee = models.IntegerField(default=datetime.datetime.now().year, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	est_public = models.BooleanField(default=1)

	def __str__(self):
		return f"Memoire - {self.annee} - {self.etudiant}"

class MemoireHistory(models.Model):
    memoire = models.ForeignKey('Memoire', on_delete=models.CASCADE)
    ACTION_CHOICES = (
        ('ajouter', 'Mémoire ajouté'),
        ('assigner_directeur', 'Un Directeur a été assigné'),
        ('reformuler', 'Mémoire reformulation'),
        ('valider', 'Mémoire validé'),
        ('rejeter', 'Mémoire rejeté'),
        ('depot_definitif', 'Dépot définitif effectué'),
        ('publier', 'Mémoire visible au public ou dépublication effectuée'),
        ('depublier', 'Mémoire dépublié'),
    )
    action = models.CharField(max_length=25, choices=ACTION_CHOICES)
    date_action = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.memoire} - {self.action}"