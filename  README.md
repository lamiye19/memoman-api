# MEMORY MANAGER (Memoman) API

API de l'application de gestion des memoires des étudiants d'une université.


# UTILISATION

## Créer et activer un environnement virtuel
```
python3 -m venv env
source env/bin/activate # Sous Linux
env\Scripts\activate # Sous Windows
```

## Installer les dépendances
Utilisez `pip` pour installer les dépendances spécifiées avec la commande: ```pip install -r requirements.txt```

## Configurer la base de données

Configurez les paramètres de connexion à la base de sonnées dans le fichier ```memoman/settings.py``` puis exécutez les migrations ```python manage.py migrate```

## Démarrer le serveur
Démarrez le serveur de développement Django avec la commande: ```python manage.py runserver```

