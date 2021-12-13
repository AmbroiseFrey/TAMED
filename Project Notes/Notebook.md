# Notebook

## Planning
J = Joachim
A = Ambroise
M = Mathis
-Semaine 1 (du 13/12/2021):
  - Terminer le systeme de unlocks et l'application messagerie - A
  - Continuer les sprites du joueur - J
  - Animation nouveau mail recu - M
-Semaine 2:
  - Coordonnées relatives - M
  - Essayer de terminer les physiques joueur et les lier à la map - J
  - Travailler sur les 'sites web' -> mettre du contenu dedans et creer plus d'interactions - A
- Semaine 3:
  - Ecrire l'histoire  et la map dans les détails sur papier- A + M
  - Commencer le render de la map (front-end, realisme) -J
- Semaine 4:
  - Ajout d'objet d'environment dans le platformer (tremplins, platformes qui bougent, lave) - J
  - Ajout de l'histoire en terme de code dans l'ordinateur (messages/mail, files, documents) - A + M
- Semaine 5:
  - Terminer le snake game - J 
  - Possibilité d'écrire des fichiers textes pour le joueur - A + M
- Semaine 6:
  - Ajout d'objets a interagir pour l'histoire dans le platformer (murs a detruires, objets a recuperer) - J
  - Terminer la possiblité d'écrire des notes - A + M
- Semaine 7:
  - Ajout de la musique (plus compliqué que ce qu'on pourrait penser) - A
  - Parametres permettant de changer le fond d'ecran ect. - M
  - Debut de la construction de la map (en terme de chose a faire dans le platformer par le joueur) - J
- Semaine 8:
  - Terminer la map + ajout de flag et de sauvegarde - J + M + A
- Semaine 9:
  - Grande seance de test du jeu, repoter les bugs, suggestions ect.
- Semaine 10:
  - Travail sur tout les bugs/ suggestions + encore des tests
- Semaine 11:
  - Travail sur tout les bugs/ suggestions part 2
 - Semaine 12:
  - Ajout de fichiers 'rigolos' et inutiles qui caractérisent 'John Doe'





## Taches generales:
Note:<br/>
Tout le monde a travaillé sur d'autre parties, c'est un plan approximatif<br/>
Pour valoriser les efforts de chacuns, la categorie `Archive` a été créé. Elle renferme des scripts qui, même s'ils on été totalement remaniés ou remplacés par d'autres methodes, ont été créés pendant plusieurs jours par certains membres du groupe.


- **Ambroise**:
  - Algorithmes permettant de detecter des clicks/inputs, parcourir des dictionnaires ou afficher des textes présents dans un dictionnaire
  - *Contributions majeures*:
    - Fonctions de base de l'ordinateur et de pygame
    - File directory
    - Messagerie:
      - Display de messages recus
      - Check de messages envoyés
    - Concretisation de l'histoire dans le jeu (Designs Canva d'images relatant la vie du personnage)


- **Joachim**:
  - Algorithmes types 3d et display de graphiques complexes
  - *Contributions majeures*:
    - Platformer
    - Sphere
    - Concretisation de l'histoire dans le jeu (Design SVG du robot)


- **Mathis**:
  - Interaction graphique en general
  - *Contributions majeures*:
    - Internet Explorer
    - Messagerie
      - Design graphique et lien entre application de messagerie et le main.py
      - Graphiques de la page d'envoi de mail et interactions/extraction de données rentrées par l'utilisateur 
    - Pauffinement de l'histoire et buts du jeu
## Logs

#### 17/11/2021:
- _Ambroise_ : Creation du repository et du repl.it

#### Du 17/11 au 01/12/2021:
- _Ambroise_ :
  - Creation de l'interface pygame
  - Ajout de fonctions 'de base' pour faciliter l'ecriture de texte, les images ect.
  - Debut de la creation de l'interface de base de l'ordinateur
  - Creation de la base du file directory

#### 01/12/2021:
- _Joachim_: création du Notebook, il servira à faire part aux autres d'éventuels changements.
- _Ambroise_: Travail sur la sauvegarde de niveau de platformer et correction de bug par rapport au lien Platformer - Ordinateur
- _Joachim et Ambroise_: Travail sur les differents graphiques dans le platformer et la simulation de l'Ordinateur
- _Joachim_: Travail sur l'amelioration du platformer en un type scrolling.

#### 03/12/2021:
- _Ambroise + Joachim + Mathis_ : Pauffinement de l'histoire et organisation du cahier des charges
- _Mathis_ : 
  - Ecriture de l'histoire dans le cahier des charges  
  - Création de la barre de recherche dans le navigateur
- _Ambroise_ :
  - Ajouts et correction de bugs dans l'Ordinateur
  - Travail sur la messagerie
- _Joachim_ : Remaniement du platformer

#### 04/12/2021:
- _Ambroise + Mathis_ : Ajout du fait qu'il faut clicker sur la barre de recherche pour pouvoir taper l'url
- _Joachim_ : Travail sur la platformer. Correction de bugs.

#### 05/12/2021:
- _Ambroise_ : Petit travail sur la messagerie
- _Joachim_ : Documentation du platformer

#### 06/12/2021:
- _Mathis_ : Travail sur l'interface pour ecrire un nouveau mail

#### 07/12/2021:
- _Ambroise_: Correction de bugs de font
- _Joachim_: Ajout d'une sphere au load. Création d'un `snake_game` sur `https://replit.com/@JoachimLaplanch/snakegame` uniquement avec des cases de couleurs
- _Mathis_: Travail sur le `snake_game`

#### 08/12/2021:
- _Joachim_: 
  - Travail sur le display au load
  - Travail sur le `snake_game` dans le display: serpent formé de cercle plutôt que de cases, déplacement du serpent avec des courbes sinusoïdales, couleurs dégradées du serpent; et déplacement vertical et horizontal en fonction du vecteur
  - Début de l'application `planet_viewer` et de sa documentation
- _Ambroise_: Travail sur la messagerie et le file directory

#### 09/12/2021:
- _Joachim_: 
  - Ajout des calculs dans le dossier _Archive_ pour pouvoir expliquer comment marche la classe `Planet`
  - Travail sur les `Flag` pour qu'ils puissent apparaître à leur endroit réel sur la planète dans `planet_viewer` en créant des méthodes pour appliquer la matrice relative à l'orientation générale de la planète 
  - Travail sur une _smooth map_ pour le platformer grâce au concept des _marching squares_
- _Ambroise_: Creation de la fonction pour check le content d'un email envoyé
- _Mathis_: Travail sur l'envoi d'un mail, avec création du bouton send mail, commencement pour regarder si le destinataire, l'objet et le mail est correcte pour valider la tache/ le niveau à l'aide de la fonction check message

#### 10/12/2021:
- *Ambroise + Mathis*: Travail sur la messagerie
- *Joachim*: Travail sur la sphere et la map du platformer
- *Ambroise*: Correction de tout les bugs liés à Pyzo

#### 11/12/2021:
- *Ambroise*:
  - Travail sur la messagerie et l'ajout de nouveaux messages
  - Travail sur le systeme des unlocks et ajout de fonctions pour le décoder
  - Travail sur le file explorer et reformattage du source code pour les files
- *Joachim*:
  - Création d'une fonction div (comme le &#60;div> en html) et d'une function understandValue pour dessiner des rectangles avec des positions et des tailles relatives à la résolution de l'écran et avec des bords