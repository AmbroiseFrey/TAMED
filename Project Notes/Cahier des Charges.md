# Cahier des Charges

## Informations techniques:
`944` lignes de code réparties en plusieurs fichiers
- **main.py** Un fichier pour construire la serie d'evenements et d'actions pour le  bon deroulement du jeu.
- **ext** : Toutes les extensions
  - **Core**:
    - **variables.py**: Variables importantes utilisées dans la plupart des programmes
    - **operations.py**: Fonctions qui permettent de faciliter certaines actions de base
  - **Apps**:
    - **file_explorer.py**: Continent le stockage de type json dans un dictionnaire qui correspond au files dans l'ordinateur, plus une fonction pour parcourir les dossiers
    - **snake.py**: Un petit jeu snake auquel on peut jouer via l'ordinateur
    - **web_search.py**: 
  - **Platformer**:
    - **components.py**: On y definit les differents sprites du platformer (Player, Floor etc.)
    - **game_utils.py**: Partie technique du platformer avec les classes et sous classes des sprites
    - **platformer.py**: Boucle infinie du platformer dans un fonction qui permet de faire le lien Ordinateur - Platformer
- **Assets** : Contient tous les fichiers necessaire au jeu

>Vous pouvez aussi trouver des programmes qui ont été dévellopés mais abandonés au profit d'un autre script dans le dossier `Project Notes/Archive`

## But du jeu
On est un technicien qui travaille pour une compagnie de haute technologie qui travaille sur un projet pour la France. Ce projet consiste à savoir si la planète Kepler-272 alpha est habitable pour une mission militaire. Pour réaliser la mission on a accès à un ordinateur qui permet de contrôler un robot déjà présent sur cette planète. On peut contrôler ce robot par un platformer, et on a accès aux fichiers présents sur l'ordinateur, à un navigateur internet. Pour réaliser à bien la mission on doit réaliser plusieurs petites missions qui nous seront données par mail, et on devra envoyer des rapports, on sera donc en communication avec une collegue. Le fait de réaliser ces missions permet d'avancer avec le robot dans le platformer, et pour réaliser ces missions on devra trouver des indices dans les fichiers, dans le navigateur...

## Histoire
* John Doe travaille dans une entreprise de haute technologie en relation avec l'état et l'armée/services secrets. Il est de double nationalité anglaise et francaise
  * Il travaille sur un projet hautement sensible pour l'armée francaise
  * Il travaille sur un robot d'exploration militaire (T.A.M.E.D.)

## Besoins
### Ordinateur
- File directory:
  - [X] Paroucir des dossiers
  - [X] Lire des fichiers
  - [ ] Ecrire des fichiers simples
- Messagerie:
  - [X] Lire des messages
  - [ ] 'Envoyer' des messages
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