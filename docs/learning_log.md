# Journal d'apprentissage

## Sprint 0

### 24 septembre 2026 – Étape 0.1

- **Fait :**
  - Installation de uv, Docker Desktop et Ollama (modèle llama3.2:3b)
  - Création du dépôt GitHub et initialisation du projet Python avec uv
  - Création de la structure du projet et des fichiers de configuration
  - Premier commit et push
  - Création du tableau de backlog (6 user stories et 8 étapes du sprint 0)

- **Appris :**
  - Docker sur Windows a besoin de WSL 2 : Docker ne démarrait pas car WSL n'était pas installé
  - Le fichier `.gitignore` empêche de publier les secrets comme le fichier `.env`
  - `git check-ignore -v` permet de vérifier si un fichier est bien ignoré
  - `pyproject.toml` décrit le projet, `uv.lock` fixe les versions exactes des bibliothèques
  - Les fins de ligne diffèrent entre Windows (CRLF) et Linux (LF) : le fichier `.gitattributes` impose LF
  - Ollama utilise ma carte graphique (100 % GPU), ce qui accélère les réponses

- **Bloqué par :**
  - `uv init` lancé dans le mauvais dossier : il faut toujours vérifier avec `pwd`
  - Des fichiers vides car non enregistrés dans VS Code : j'ai activé l'enregistrement automatique
  - Erreur « Accès refusé » avec `bcdedit` : il fallait ouvrir PowerShell en administrateur

- **Prochaine étape :**
  - Étape 0.2 : comprendre le fonctionnement des LLM et écrire un premier programme avec Ollama