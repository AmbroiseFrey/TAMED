# Cahier des Charges

## Caracteristiques
- 1 joueur
- Jeu 2D avec quelques petits elements 3D
- Jeu en temps réél (boucle while)

- Platformer:
  - Une map avec plusieurs points de 'spawn', niveau de difficulté qui augmente au fur et a mesure que l'on avance
  - Contrôler un robot sur une map
  - Possibilité de PNJ
- Système d'exploitation:
  - Gestionnaire de fichier:
    - Paroucir des dossiers
    - Lire des fichiers
    - Ecrire des fichiers simples
  - Messagerie:
    - Lire des messages
    - 'Envoyer' des messages et analyser son contenu
  - Web explorer:
    - Afficher quelques pages web de base
- Musique en fond et possibilité de lire des fichiers de musique

## Informations techniques:
~`2000` lignes de code réparties en plusieurs fichiers
- **main.py** Un fichier pour construire la serie d'evenements et d'actions pour le  bon deroulement du jeu.
- **ext** : Toutes les extensions
  - **Core**:
    - **variables.py**: Variables importantes utilisées dans la plupart des programmes
    - **operations.py**: Fonctions qui permettent de faciliter certaines actions de base
    - **scan_unlocks.py**: Tout le systeme d'unlocks qui permet de lier messagerie, platformer et fichiers
    - **sphere.py**: Permet le render de la sphere au login
  - **Apps**:
    - **file_explorer.py**: Continent le stockage de type json dans un dictionnaire qui correspond au files dans l'ordinateur, plus une fonction pour parcourir les dossiers
    - **snake.py**: Un petit jeu snake auquel on peut jouer via l'ordinateur
    - **web_search.py**: 
  - **Platformer**:
    - **components.py**: On y definit les differents sprites du platformer (Player, Floor etc.)
    - **game_utils.py**: Partie technique du platformer avec les classes et sous classes des sprites
    - **platformer.py**: Boucle infinie du platformer dans un fonction qui permet de faire le lien Ordinateur - Platformer
- **Assets** : Contient tous les fichiers necessaires au jeu

---
>Vous pouvez aussi trouver des programmes qui ont été dévellopés mais abandonés au profit d'un autre script dans le dossier `Project Notes/Archive`

## But du jeu
On est un technicien qui travaille pour une compagnie de haute technologie qui travaille sur un projet pour la France. Ce projet consiste à savoir si la planète Kepler-272-alpha est habitable pour une mission militaire. Pour réaliser la mission on a accès à un ordinateur qui permet de contrôler un robot déjà présent sur cette planète. On peut contrôler ce robot par un platformer, et on a accès aux fichiers présents sur l'ordinateur, à un navigateur internet. Pour réaliser à bien la mission on doit réaliser plusieurs petites missions qui nous seront données par mail, et on devra envoyer des rapports, on sera donc en communication avec une collegue. Le fait de réaliser ces missions permet d'avancer avec le robot dans le platformer, et pour réaliser ces missions on devra trouver des indices dans les fichiers, dans le navigateur...

## Histoire
* **John Doe** travaille dans une entreprise de haute technologie en relation avec l'état et l'armée/services secrets. Il est de double nationalité anglaise et francaise
  * Il travaille sur un projet hautement sensible pour l'armée francaise
    * Un robot d'exploration militaire (T.A.M.E.D.)

* **Charlotte Coulson** travaille aussi pour Krypt Korp
  * Amie de l'agent mort dans le crash de la station, elle envoi des emails au joueur par rapport à son sceptisme quand au raison du crash
  * Elle travaillait sur le Project:Zeus

* **Project:Zeus**:
  * Un projet de station destiné a acceuilir des militaires dans l'espace profond
  * Un certain *Colonel Thompson* avait pour mission de consituer les modules de base de la station mais un incident mysterieux c'est passé

* **Project:TAMED**:
  * Technologically Advanced Military Exploration Device
    * Le robot en lui meme a d'abord été concu pour l'exploration militaire de zones tres dangereuses
  * Partenariat avec l'armée francaise pour but de trouver une planete habitable
    * Mené par le *General Michael Fredlyn*, chef du Commandement de l’Espace

## Besoins
### Ordinateur
- File directory:
  - [X] Paroucir des dossiers
  - [X] Lire des fichiers
  - [X] Ecrire des fichiers simples
- Messagerie:
  - [X] Lire des messages
  - [X] 'Envoyer' des messages
- Web explorer:
  - [ ] Lire quelques pages de base

### Jeu type platformer:
- Platformer de type 'scrolling':
  - [X] Gravité et physiques de sol
  - [X] Mouvement latéral
  - [X] Sauts
  - [X] Physique de murs
  - [ ] Render la map
  - [ ] Elements avec lequels l'on peut interagir
  - [ ] Carte avec checkpoints
