"""
URL configuration for memoman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from memo.views import memoires_public, memoires_detail_public, file_view

urlpatterns = [
    path('', memoires_public, name="accueil"),
    path('consulter/<id>', memoires_detail_public, name="consulter"),
    path('consulter/<id>/fichier', file_view, name="consulter.fichier"),
    path('django-admin/', admin.site.urls),
    path('admin/', include('memo.urls'))
]
