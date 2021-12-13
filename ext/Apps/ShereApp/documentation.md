# Sphere App : PLANET VIEWER
**`planet_viewer`** est une application (très performante) qui permet de voir la progression du robot sur la planète. Un `circle` bleu indique le point de départ du robot, des `circle` verts indiquent les `flags` que le robot a déposés, sur lesquels on peut cliquer pour que le robot retourne à cet endroit (Attention, le robot a un nombre limité de `flags` qu'il peut placer) et un `circle` rouge indique la position actuelle du robot. Enfin, une courbe orange représente les endroits où le robot a déjà exploré.

________________________

**_r_**: float = 100;
  rayon de la planète

**_perspective_index_**: float = 150;
  indice permettant de calculer la position des `Point` sur l'écran avec une perspective

**_applyScreen_**: function(`p`:tuple(float,2))=>tuple(float,2);
  Cette fonction renvoie la position du point `p` entré en argument, relatif au milieu de l'écran (`mid_screen`)

**_sumTuple_** function(`t`:tuple)->float|int|str;
  fonction qui renvoie l'addition/concaténation des valeurs comprises dans le tuple `t` 

**_multiply_3Dmatrices_** function(m1:tuple(tuple(float,3),3),m2:tuple(tuple(float,3),3))->tuple(tuple(float,3),3);
  fonction qui renvoie la multiplication de 2 matrices entrées en argument: `m1` et `m2`

**_sign_**: function(`n`:float)-> 1|-1|0;
  fonction qui prend un nombre `n` en argment et renvoie le signe de ce nombre (1 s'il est positif, -1 s'il est négatif et 0 s'il est nul)

**_a_**: function(`x`:float, `y`:float);
  fonction qui prend une abscisse `x` et en ordonnée `y` en argument et retourne l'angle grâce à la fonction trigo `atan`, sans erreur de division par zero (juste une prévention)

________________________

## class Point:

  **_constructor_**: function(`x`:float, `y`:float, `z`:float)=>Point;
    Cette classe crée un point dans l'espace grâce à son abscisse `x`, son ordonnée `y` et sa profondeur `z`
    
  **_pos_**: tuple(float, 3);
    paramètre dans lequel on stocke le point

  **_persp_coef_**: int;
    coéfficient qui dépend de la profondeur `z` du point par lequel il faut multiplier l'abscisse `x` et l'ordonnée `y` de ce point pour avoir sa position sur un plan à partir de l'indice de perspective `perspective_index`
  
  **_draw_position_**:
    position du point sur le plan après toutes les modifications éffectuées: bouger en fonction de la perspective et déplacer le point jusqu'au milieu grâce à la fonction `applyScreen` qui utiliser la variable `mid_screen`

  **_rotate_**: function(`R`: tuple(tuple(float,2),3))=>None;
    L'argument `R` et un tuple contenant 3 tuples pour les rotation sur l'axe X, Y et Z respectivement qui contiennent les valeurs des cosinus et sinus respectivement des angles de ces rotations. Avec ces valeurs, on peut effectuer les modifications nécessaires grâce aux matrices de rotation pour changer la position du point en respectant la rotation demandée. Puis on redéfinit la le paramètre `draw_position` grâce à la position donnée.

  **_applyMatrixRotation_**: function(matrix: tuple(tuple(float,3),3))->None;
    méthode qui applique à la position du point les modifications nécessaires dues à l'ensemble des rotations de la planète traduites par la matrice `matrix`
  
  **_applyPerspective_**: function()=>tuple(float, 2);
    cette méthode change d'abord le coéfficient `persp_coef` pour enfin retourner la position du point dans un plan en appliquant une perspective de `perspective_index` (note: on utilise du logarithme pour cela)

  **_updateDrawPosition_**: function()->None;
    méthode qui permet de rafraichir le position du point sur l'écran `draw_position` (sans l'afficher)

________________________

## class Trait:

  **_Trait.dimension_**: float = 2*r;
    valeur permettant de calculer la couleur et la taille du trait en fonction de son `z_index`

  **_constructor_**: function(`point1`:Point, `point2`:Point)=>Trait;
    cette classe crée un trait entre 2 points: `point1` et `point2`

  **_z_index_**: float;
    moyenne des profondeurs `z` des points qui forment ce trait

  **_color_**: tuple(float,3);
    paramètre qui stocke la couleur du trait sous forme RGB (un trait proche sera plus foncé qu'un trait loin [très proche, très loin 😅])

  **_marker_width_**: float;
    taille du markeur pour dessinner le trait (un trait proche sera plus gros qu'un trait loin 😅)

  **_update_**: function()=>None;
    méthode qui change le `z_index` du trait et permet de calculer la couleur `color` de ce trait et la taille du markeur `marker_width` en fonction de ce `z_index` 
  
  **_display_**: function()=>None;
    méthode qui permet d'afficher le trait sur l'écran `screen`

________________________

## class Flag:

  **_Flag.color_**: tuple(float,3) = (0,255,0);
    stocke la couleur de objets de type `Flag` sur l'écran `screen`
  
  **_constructor_**: function(`scrolling_platformer`: float, `planet_view`: Point)=>Flag;
    classe qui crée un `Flag` (point de repère) au cas où l'on voudrait revenir à l'endoit définit pas `scrolling_platformer` ou `planet_view` (sachant que connaissant l'un on peut retrouver l'autre)

  **_point_**: Point;
    position du flag sur la `Planet`

  **_display_**: function()=>None;
    permet d'afficher le `Flag` sur l'écran `screen`

________________________

## class Planet:
  **_constructor_**: function(`lon`:int=20, `lat`:int=10, `r`:float=100, `type`:tuple(bool,4)=(1,1,0,0))=>Planet;
    on crée une planète grâce à une matrice de taille `lon+1`&times;`lat+1` ce qui permet de définir des traits afin de former la planète de rayon `r` sur l'écran en fonction du `type` (il y a en tout 15 types de planètes)

  **_r_**: float;
    rayon de la planète
  
  **_d_**: tuple(int,2) = (lon+1, lat+1);
    dimensions de la planète
  
  **_mat_** = tuple(tuple(Point, lat+1), lon+1);
    matrice dans laquelle se trouve les points qui forment la surface de la planète
  
  **_traits_**: list;
    paramètre dans lequel on stocke tous les traits

  **_flags_**: list;
    paramètre dans lequel on stocke les flags sur la map

  **_orientation_matrices_**: tuple(tuple(float,3),3);
    matrices qui varie à chaque rotation par laquelle il faut multiplier un `Point` pour avoir la position réelle de ce point sur la planète (c'est une matrice qui permet de stocker l'entièreté des rotations effectuées par la planète)

  **_request_display_**: bool;
    paramètre qui permet de savoir s'il y a eu une modification afin dans la rotation de la planète afin que l'on ne calcule pas trop de choses pour rien

  **_addFlag_**: function(`flag`: Flag)=>None;
    méthode qui permet d'ajouter le `flag` sur la planète et d'effectuer les rotations sur le `flag` relatives à l'ensemble de rotations de la planète que l'on trouve grâce à `_orientation_matrices_`
    
  **_rotate_**: function(`rotX`:float, `rotY`:float, `rotZ`:float)=>None;
    méthode qui permet d'effectuer les modifications nécessaires aux points dans la map uniquement s'il y a réellement une rotation à effectuer (afin de ne pas faire trop de calculs pour rien)

  **_display_**: function()=>None;
    méthode qui permet d'afficher les traits qui constituent la sphère et les flags de la map