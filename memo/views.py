from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import *
from .forms import MemoireForm

# Create your views here.


def login(request):
    return render(request, 'auth/login.html')


def register(request):
    return render(request, 'auth/register.html')

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


# Spécialité
def specialites(request):
    elt = {}
    # elt = Specialite.objects.all()

    return render(request, 'specialite/liste.html', {'specialites': elt})

# Mémoire
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
                instance = form.save(commit=False)
        
                # Associer l'utilisateur connecté au champ etudiant
                # form.etudiant = user.etudiant

                instance.etudiant = Etudiant.objects.get(id=2)
                instance.save()  # Enregistrer les données su form pour créer une instance de Memoire
                
                # Redirection vers la liste des memoires
                return redirect(reverse('memoires.liste'))
            except Exception as e:
                print(f"Une erreur s'est produite : {str(e)}")
                return render(request, 'memoire/ajouter.html', {'error': 'Seul un étudiant peut créer son mémoire.'})

    else:
        form = MemoireForm()
    return render(request, 'memoire/ajouter.html', {'form': form})

def user_detail(request, id: int):
    try:
        elt = Memoire.objects.get(id=id)
    except Memoire.DoesNotExist:
        raise ('Introuvable')

    return render(request, 'memoire/detail.html', {'memo': elt})

def memoires_update(request, id: int):
    objet = get_object_or_404(Memoire, id=id)

    if request.method == 'POST':
        form = MemoireForm(request.POST, instance=objet)
        if form.is_valid():
            memoire = form.save()
            return redirect(reverse('memoires.liste'))
    else:
        form = MemoireForm(instance=objet)
    
    return render(request, 'memoire/modifier.html', {'form': form})
