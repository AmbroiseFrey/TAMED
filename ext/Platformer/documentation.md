# game_utils.py:

## class Image:
  
  **_construcor_**: function(url, x, y, ?w, ?h)=>Image;
    cette classe crée une image qui sera utilisée pour les Sprites en prenant en argument l'`url` de l'image, son abscisse `x`, son ordonnée `y` et éventuellement sa taille, définie par `w` et `h`

  **_img_**: Surface();
    paramètre qui permet de stocker l'image afin qu'on n'est pas besoin de la convertir à chaque tour de boucle
  
  **_size_**: tuple(2);
    tuple dans lequel on stocke la taille de l'image

  **_pos_**: tuple(2);
    tuple dans lequel on stocke la position de l'image
  
  **_r_**: list(4); 
    liste qui contient les 2 points permettant de definir un rectangle et qui correspond au rectangle de collision de l'objet

  **_display_**: function()=>None;
    cette méthode permet d'afficher l'image en fonction de sa position
  
  **_Image.relative_**: tuple(2);
    permet de déplacer les `Image` en fonction d'un point (qui varie avec la position et la taille du `player`)

## class Group:
  
  **_construcor_**: function()=>Group;
    cette classe crée simplement un groupe de Sprites (ou MotionSprites) il permet de créer des environnements utilisés pour savoir si le joueur touche ou non un Sprite appartenant à ce groupe

  **_length_**: int;
    nombre entier qui permet de savoir le nombre d'éléments dans le groupe 

  **_list_**: tuple;
    tuple qui contient tous les éléments du groupe 

  **_add_**: function(obj: Sprite|MotionSprite)=>None;
    cette méthode permet d'ajouter un objet de type Sprite ou  MotionSprite dans la liste des éléments que cet objet contient
  
  **_forEach_**: function(callback: `function`)=>None;
    cette méthode prends une fonction en argument et pour chaque élément de ce groupe, on éxécute cette fonction en mettant avec l'élément

  **_display_**: function()=>None;
    cette méthode permet d'afficher tous les sprites à l'intérieur de ce groupe

## class Sprite(Image): 

  **_constructor_**: function(image, x, y, ?w, ?h)=>Sprite; 
    Cette classe permet de créer un `Sprite`, c'est à dire une `Image` sur l'écran qui correspond à un objet de hauteur `h`, de largeur `w`, d'abscisse `x` et d'ordonnée `y`. Elle utilise des méthodes qui permettent de savoir si le `Sprite` touche ou non un autre `Sprite`
  
  **_borders_**: tuple(4);
    tuple qui permet de stocker les bords du Sprite afin que l'on puisse savoir si le Sprite touche un environnement de type `Group` par le haut, la droite, le bas et la gauche (respectivement)
  
  **_collides_with_**: function(environment:`Group`, checkAll:`bool`)=>Sprite|MotionSprite|list;
    Cette méthode permet de savoir si le Sprite effectue une collision avec l'`environment`, un objet de type `Group`. Elle renvoie le Sprite de l'`environment` que l'objet a touché
  
  **_getTouchBorders_**: function(environment: `Group`)=>tuple(4);
    Cette méthode ne fait rien pour l'instant mais elle permettrait de renvoyer un tuple contenant des booléens qui indiqueraient si le Sprite touche un Sprite de l'environment par le haut, la droite, le bas, ou la gauche (respectivement)

  **_updateBorders_**: function()=>None;
    Cette méthode permet d'update les `borders` (et oui, j'étais très inspiré pour écrire cette spécification)
  
  **_borderCollide_**: function(border_number:`int`, environment:`Group`)=>Sprite|MotionSprite;
    Cette méthode prends 2 arguments: le premier sert à savoir quel border on veut checker pour voir s'il collide avec un Sprite dans l'environment et le deuxième permet de définir l'environment

## class MotionSprite(Sprite): 

  **_constructor_**: function(image, x, y, ?w, ?h)=>MotionSprite; 
    Cette classe permet de créer un `Sprite`,  qui bouge en fonction du vecteur `v` qui lui est influencé par la gravité, la friction `f` et l'environment dans lequel il se trouve
  
  **_vector_**: list(2);
    Liste dans laquelle on stocke le vecteur relatif à la force qui s'applique sur le player à chaque tour de boucle afin que les physiques sur la planète soient à peu près cohérentes
  
  **_f_**: tuple(2);
    Tuple dans lequel on stocke la friction qui s'applique sur le player à chaque tour de boucle
  
  **_newRect_**: function()=>list(4);
    Méthode qui renvoie le rectangle de collision de l'objet après une translation du vecteur _vector_

  **_updateVector_**: function()=>None;
    Méthode qui permet de changer le vecteur en fonction de la friction du robot


# components.py:

## class Player(MotionSprite):
  
  **_construcor_**: function(x: int, y: int, ?w, ?h)=>Player;
    Classe qui crée un objet mobile (qui peut se déplacer dans la map)

  **_move_**: function()=>None;
    Cette Méthode permet de bouger l'objet player en fonction du vecteur _v_ définit dans la classe `MotionSprite` qui dépend de l'environment

  **_update_**: function(floor:Group)=>None;
    Méthode qui permet de changer la position du player en fonction des touches appuyées et de l'environment (entré dans les arguments) et change le point relatif aux images afin que la map se déplace en suivant le player (c'est le but d'un scrolling_platformer)

## class Floor(Sprite):
  **_construcor_**: function(x:int,y:int)=>Floor;
    Cette classe crée un Sprite qui sera ensuite utilisé pour pour savoir si le player touche cet le sol ou non, et doit donc être empêché d'avancer (malgré les quelques compliquations que ça apporte) 