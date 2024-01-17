from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST


# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = UtilisateurCreationForm(request.POST)
        etudiant_form = EtudiantCreationForm(request.POST)
        enseignant_form = EnseignantCreationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            if etudiant_form.is_valid():
                etudiant = etudiant_form.save(commit=False)
                etudiant.utilisateur = user
                etudiant.save()
                login(request, user)
                return redirect('#')  
            elif enseignant_form.is_valid():
                enseignant = enseignant_form.save(commit=False)
                enseignant.utilisateur = user
                enseignant.save()
                login(request, user)
                return redirect('#') 

    else:
        user_form = UtilisateurCreationForm()
        etudiant_form = EtudiantCreationForm()
        enseignant_form = EnseignantCreationForm()

    return render(request, 'auth/register.html', {'user_form': user_form, 'etudiant_form': etudiant_form, 'enseignant_form': enseignant_form})




def login(request):
    if request.method == 'POST':
        form = ConnexionForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigez l'utilisateur après la connexion
                return redirect('#')  # Remplacez '#' par l'URL souhaitée
    else:
        form = ConnexionForm()

    return render(request, 'auth/login.html', {'form': form})
   


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def dashboard(request):
    return render(request, 'dashboard.html')


# USER
# @login_required(login_url="/login/")
def users(request):
    elt = Utilisateur.objects.all()

    return render(request, 'user/liste.html', {'utilisateurs': elt})


def etudiants(request):
    elt = Etudiant.objects.all()

    context = {
        'utilisateurs': elt,
    }

    return render(request, 'user/liste_etudiant.html', context)


def enseignants(request):
    elt = Enseignant.objects.all()

    context = {
        'utilisateurs': elt,
    }

    return render(request, 'user/enseignant.html', context)


def user_detail(request, id: int):
    try:
        elt = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        raise ('Introuvable')

    return render(request, 'user/detail.html', {'utilisateurs': elt})


# Niveau
def niveaux(request):
    elt = {}
    # elt = Niveau.objects.all()

    return render(request, 'niveau/liste.html', {'niveaux': elt})


"""
 Niveau
"""


class NiveauViews:
    @staticmethod
    def ajouter_niveau(request):
        if request.method == 'POST':
            form = NiveauForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Niveau ajouté avec succès.')
                return redirect('niveau_list')  # Redirige vers une autre vue après l'ajout
        else:
            form = NiveauForm()

        return render(request, 'ajouter_niveau.html', {'form': form})

    @staticmethod
    def modifier_niveau(request, niveau_id):
        niveau = get_object_or_404(Niveau, pk=niveau_id)

        if request.method == 'POST':
            form = NiveauForm(request.POST, instance=niveau)
            if form.is_valid():
                form.save()
                messages.success(request, 'Niveau modifié avec succès.')
                return redirect('niveau_list')  # Redirige vers une autre vue après la modification
        else:
            form = NiveauForm(instance=niveau)

        return render(request, 'modifier_niveau.html', {'form': form, 'niveau': niveau})

    @staticmethod
    def recherche_niveau(request):
        query = request.GET.get('q', '')
        niveaux = Niveau.objects.filter(libelle__icontains=query)
        return render(request, 'recherche_niveau.html', {'niveaux': niveaux})

    @staticmethod
    def supprimer_niveau(request, niveau_id):
        niveau = get_object_or_404(Niveau, pk=niveau_id)
        niveau.delete()
        messages.success(request, 'Niveau supprimé avec succès.')
        return redirect('niveau_list')

    def affiche_niveau(request):
        niveaux = Niveau.objects.all()
        return render(request, 'niveau_list.html', {'niveaux': niveaux})


# Spécialité
def specialites(request):
    elt = {}
    # elt = Specialite.objects.all()

    return render(request, 'specialite/liste.html', {'specialites': elt})


# Mémoire
MSG = {
    "rejet": "Impossible de modifier un mémoire rejeté",
    "auth": "Vous n'êtes pas authorisé à effectuer cette action",
    "erreur": "Une erreur est survenue",
    "success": "Action effectuée avec success"
}

def check_auth(request, id:int, auth=[]):
    if request.user not in auth or (auth == [] and not request.user.is_staff):
        messages.error(request, MSG['auth'])
        return redirect(reverse('memoires.detail', args=[id]))
    return None
    
def memoires(request):
    elt = Memoire.objects.all()

    return render(request, 'memoire/liste.html', {'memoires': elt})


def memoires_add(request):
    if request.method == 'POST':
        form = MemoireForm(request.POST)
        if form.is_valid():
            # Créer une instance du modèle
            user = request.user

            try:
                memoire = form.save(commit=False)

                # Associer l'utilisateur connecté au champ etudiant
                # memoire.etudiant = user.etudiant

                memoire.etudiant = Etudiant.objects.get(id=2)
                memoire.save()  # Enregistrer les données du form pour créer une instance de Memoire

                # Enregistrer l'action dans l'historique
                MemoireHistory.objects.create(memoire=memoire, action='ajouter', utilisateur=memoire.etudiant.utilisateur)

                # Redirection vers la liste des memoires
                return redirect(reverse('memoires.liste'))
            except Exception as e:
                print(f"Une erreur s'est produite : {str(e)}")
                return render(request, 'memoire/ajouter.html', {'error': 'Seul un étudiant peut créer son mémoire.'})

    else:
        form = MemoireForm()
    return render(request, 'memoire/ajouter.html', {'form': form})


def memoires_detail(request, id: int):
    try:
        elt = Memoire.objects.get(id=id)
        form = MemoireForm(instance=elt)
    except Memoire.DoesNotExist:
        raise ('Introuvable')

    return render(request, 'memoire/detail.html', {'memo': elt, 'form': form})


def memoires_update(request, id: int):
    memoire = get_object_or_404(Memoire, id=id)

    if request.method == 'POST':
        # Remplir le formulaire avec les données de l'instance
        form = MemoireForm(request.POST, request.FILES, instance=memoire, fields=request.POST.keys())
                  
        if memoire.statut != 1 and (form.is_valid() or form.has_changed()):
            form.save()
            messages.success(request, 'Memoire reformulé avec succès!')
            MemoireHistory.objects.create(memoire=memoire, action='reformuler', utilisateur=request.user)
            return redirect(reverse('memoires.detail', args=[id]))
        else:
            # Add an error message
            messages.error(request, MSG['erreur'])
    else:
        form = MemoireForm(instance=memoire)

    return render(request, 'memoire/modifier.html', {'form': form})

@require_POST
def memoires_statut(request, id:int):
    memoire = get_object_or_404(Memoire, id=id)

    authorized_user = [memoire.directeur.utilisateur]
    error = check_auth(request, id, authorized_user)
    if error:
        return error

    if memoire.statut == 0:
        # Si rejeté, ne permettre aucune autre action
        messages.error(request, MSG['rejet'])
    
    statut_value = int(request.POST.get('valider', -1))  # si "Valider" a été soumis, -1 sinon
    
    if(statut_value != -1):
        if statut_value == 1:
            # Enregistrement de l'action dans l'historique
            MemoireHistory.objects.create(memoire=memoire, action='valider', utilisateur=request.user)

        elif statut_value == 0:
            # Enregistrement de l'action dans l'historique
            MemoireHistory.objects.create(memoire=memoire, action='rejeter', utilisateur=request.user)

        memoire.statut = statut_value
        memoire.save()

    return redirect(reverse('memoires.detail', args=[id]))

@require_POST
def memoires_assigner_directeur(request, id):
    memoire = get_object_or_404(Memoire, id=id)
    
    error = check_auth(request,id, [])
    """ if error:
        return error """
    
    form = MemoireForm(request.POST, instance=memoire, fields=["directeur"])
    if form.is_valid():
        form.save()
        MemoireHistory.objects.create(memoire=memoire, action='assigner_directeur', utilisateur=request.user)
    else:
        messages.error(request, MSG['erreur'])
        
    return redirect('memoires.detail', id=id)

@require_POST
def memoires_soumettre(request, id):
    memoire = get_object_or_404(Memoire, pk=id)
    # Vérifier si le mémoire a été rejeté
    if memoire.statut == 0:
        # Si rejeté, ne permettre aucune autre action
        messages.error(request, MSG['rejet'])

    if 'fichier' in request.FILES:
        form = MemoireForm(request.FILES, instance=memoire, fields=['fichier'])
        #memoire.fichier = request.FILES['fichier']
        form.save()

        messages.success(request, MSG['success'])
        MemoireHistory.objects.create(memoire=memoire, action='depot_definitif', utilisateur=memoire.etudiant.utilisateur)

    return redirect('memoires.detail', id=id)

@require_POST
def memoires_publier(request, id):
    memoire = get_object_or_404(Memoire, pk=id)

    authorized_user = [memoire.etudiant.utilisateur]
    error = check_auth(request, id, authorized_user)
    """ if error:
        return error """

    if memoire.statut == 0:
        # Si rejeté, ne permettre aucune autre action
        messages.error(request, MSG['rejet'])
    
    est_public = int(request.POST.get('est_public', -1))
    
    if(est_public != -1):
        if est_public == 1:
            # Enregistrement de l'action dans l'historique
            MemoireHistory.objects.create(memoire=memoire, action='publier', utilisateur=request.user)

        elif est_public == 0:
            # Enregistrement de l'action dans l'historique
            MemoireHistory.objects.create(memoire=memoire, action='depublier', utilisateur=request.user)

        memoire.est_public = est_public
        memoire.save()

    return redirect('memoires.detail', id=id)
