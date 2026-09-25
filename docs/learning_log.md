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


  cat >> docs/learning_log.md << 'EOF'

### 25 septembre 2026 – Étape 0.2

- **Fait :**
  - Création d'une branche de travail `feature/premier-appel-llm`
  - Configuration du projet avec pydantic-settings (lecture du fichier `.env`)
  - Quatre exercices avec Ollama : premier appel, rôles et mémoire, température, première injection de prompt

- **Appris :**
  - Un LLM prédit le texte le plus probable token après token : il optimise la plausibilité, pas la vérité, d'où les hallucinations
  - Les tokens sont l'unité de mesure des LLM ; le français, l'arabe et la derja en consomment plus que l'anglais
  - Un LLM n'a pas de mémoire : l'application renvoie tout l'historique à chaque appel
  - Les messages ont trois rôles : system (consignes du développeur), user, assistant
  - L'injection de prompt est possible car les consignes et les messages utilisateur arrivent dans le même flux de texte
  - La température contrôle le hasard, mais même à 0 la reproductibilité n'est pas garantie

- **Résultats observés :**
  - Premier appel : 37 tokens envoyés (le chat template ajoute des balises), 88 générés, 6 s (chargement du modèle)
  - Sortie de périmètre : l'assistant refuse la recette de couscous puis donne quand même des conseils
  - Hallucination : avec l'historique, il affirme que je suis cliente de BanqueNova sans que je l'aie dit
  - Température 0 : l'essai 1 diffère des essais 2 et 3 (petites différences numériques sur GPU, cache)
  - Injection : demande directe 0/5, injection classique 0/5, jeu de rôle 1/5
  - Intervalles de confiance de Wilson à 95 % : 0/5 donne [0 % ; 43 %], 1/5 donne [4 % ; 62 %]. Avec 5 essais, impossible de conclure qu'un agent est sûr ni de comparer les attaques

- **Bloqué par :**
  - Rien de bloquant

- **Prochaine étape :**
  - Étape 0.3 : générer les fausses données bancaires avec Faker
EOF


