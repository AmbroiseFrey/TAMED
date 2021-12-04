# game_utils.py:

## class Image:
>
  
  **_construcor_**: function(url, x, y, ?w, ?h);
    cette classe crée une image qui sera utilisée pour les Sprites en prenant en argument l'`url` de l'image, son abscisse `x`, son ordonnée `y` et éventuellement sa taille, définie par `w` et `h`
  
  **_r_**: list(4); 
    liste qui contient les deux points permettant de definir un rectangle et qui correspond au rectangle de collision de l'objet

  **_display_**: function();
    cette méthode
  
  **_Image.relative_**: tuple(2);
    permet de déplacer les `Image` en fonction d'un point (qui varie avec la position et la taille du `player`)

## class Group:
  
  **_construcor_**: function();
    cette classe crée simplement un groupe de Sprites

  **_length_**: int;
    nombre entier qui permet de savoir le nombre d'éléments dans le groupe 

  **_list_**: tuple;
    tuple qui contient tous les éléments du groupe 
  
  **_forEach_**: function(callback: `function`);
    cette méthode prends une fonction en argument et pour chaque élément de ce groupe, on éxécute cette fonction en mettant avec l'élément

  **_display_**: function();
    cette méthode permet d'afficher tous les sprites à l'intérieur de ce groupe

## class Sprite(Image): 

  **_constructor_**: function(image, x, y, ?w, ?h); 
    Cette classe permet de créer un `Sprite`, c'est à dire une `Image` sur l'écran qui correspond à un objet de hauteur `h`, de largeur `w`, d'abscisse `x` et d'ordonnée `y`. Elle utilise des méthodes qui permettent de savoir si le `Sprite` touche ou non un autre `Sprite`
  
  **_collides_with_**: function(environment:`Group`, checkAll:`bool`);
    Cette méthode permet de savoir si le Sprite effectue une collision avec l'`environment`, un objet de type `Group`. Elle renvoie le Sprite de l'`environment` que l'objet a touché
  
  **_getTouchBorders_**: function(environment: `Group`);
    Cette méthode ne fait rien pour l'instant mais elle permettrait

  **_updateBorders_**: function();
    Cette méthode permet d'update les `borders`
  
  **_borderCollide_**: function(border_number:`int`, environment:`Group`);


## class MotionSprite(Sprite): 

  **_constructor_**: function(image, x, y, ?w, ?h); 
    Cette classe permet de créer un `Sprite`,  qui bouge en fonction du vecteur `v` qui lui est influencé par la gravité, la friction `f` et l'environment



# components.py: