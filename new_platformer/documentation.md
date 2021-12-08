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

## class Sprite(Image):

# components.py:

## class Player(MotionSprite):