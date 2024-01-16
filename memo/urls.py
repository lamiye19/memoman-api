from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

# URLConf
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),

    #Utilisateurs
    path('utilisateurs', views.users, name="users.liste"),
    path('utilisateurs/etudiants', views.etudiants, name="users.etudiants"),
    path('utilisateurs/enseignants', views.enseignants, name="users.enseignants"),
    path('utilisateurs/<id>', views.user_detail, name="users.detail"),

    # Niveau
    path('niveaux', views.niveaux, name="niveaux.liste"),
    path('niveaux/<id>', views.user_detail, name="niveaux.detail"),

    # Spécialité
    path('specialites', views.specialites, name="specialites.liste"),
    path('specialites/<id>', views.user_detail, name="specialites.detail"),

    # Mémoire
    path('memoires', views.memoires, name="memoires.liste"),
    path('memoires/ajouter', views.memoires_add, name="memoires.ajouter"),
    path('memoires/modifier/<id>', views.memoires_update, name="memoires.modifier"),
    path('memoires/statut/<id>', views.memoires_statut, name="memoires.statut"),
    path('memoires/<id>', views.memoires_detail, name="memoires.detail"),


] 
# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'memo.views.custom_404'
