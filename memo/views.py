from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from models import Niveau
# Create your views here.


"""
 Niveau
"""
class NiveauForm:
    class Meta:
        model = Niveau
        fields = '__all__'


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




