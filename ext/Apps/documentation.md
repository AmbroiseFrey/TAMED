# file_explorer.py:

# snake.py:
import pygame, time
from math import ceil, sin, pi, floor
from random import randint

resolution = (600,600)
screen = pygame.display.set_mode(resolution, pygame.DOUBLEBUF, 32)
mid_screen = tuple(i/2 for i in resolution)
clock = pygame.time.Clock()
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

def minInt(a,b): return a if a<b else b

class Fruit:
  def __init__(self, carte):
    self.offsetPos = tuple(map(lambda x: randint(0,x-1),carte.dimensions))
    self.pos = tuple(map(lambda x: (x+.5)*carte.case_taille,self.offsetPos))
    self.r = carte.case_taille*.4
  def display(self):
    pygame.draw.circle(screen, (255,0,0), self.pos, self.r)

class Serpent:
  tilePerCase = 20
  def __init__(self, p, caseT: float, v = (1,0), taille = 30, d = ((255,255,0),(0,255,0))):
    self.taille = taille
    self.p = tuple((i+.5)*caseT for i in p)
    print(self.p)
    self.vecteur=v
    self.current_v=v
    self.off = 2*pi/caseT
    self.caseT = caseT
    self.tiles = tuple(
      tuple(self.p[i]-j*v[i]*caseT/Serpent.tilePerCase for i in range(2)) for j in range(taille)
    )
    self.cs = tuple(
      (d[0][i], d[1][i]-d[0][i]) for i in range(3)
      )
  def coefColor(self, coef):
    return tuple(i[0]+i[1]*coef for i in self.cs)
  def slither(self, p, coef=1):
    return tuple(p[i]+sin(p[1-i]*self.off)*self.caseT/7*(.5+.5*coef) for i in range(2))
  def change_destination(self):
    if self.vecteur == self.current_v:
      return
    if self.current_v[0]:
      e=(self.p[0]+self.caseT*.5)%self.caseT
      if self.current_v[0] == 1: e = self.caseT-e
    else:
      e=(self.p[1]+self.caseT*.5)%self.caseT
      if self.current_v[1] == 1: e = self.caseT-e
    if (e<self.caseT/Serpent.tilePerCase):
      self.p = (
        int(2*(self.p[0]+e*self.current_v[0]))/2,
        int(2*(self.p[1]+e*self.current_v[1]))/2
      )
      self.current_v = self.vecteur
  def closePosition(self, p=None):
    return tuple(map(lambda x:ceil(x/self.caseT-1), p or self.p))
  def update(self, carte):
    self.change_destination()
    self.p= tuple(self.p[i]+self.current_v[i]*self.caseT/Serpent.tilePerCase for i in range(2))
    self.tiles = (self.p,)+self.tiles[:self.taille-1]
    close_p = self.closePosition()
    if (close_p[0]<0 or close_p[0]>=carte.dimensions[0] or close_p[1]<0 or close_p[1]>=carte.dimensions[1]):
      return True
    if (close_p == carte.fruit.offsetPos):
      self.taille += 25
      carte.nouveau_Fruit()
    return False
  def display(self):
    i_p = self.closePosition()
    getaway = (False,) 
    for i in range(len(self.tiles)-1,-1,-1):
      tile = self.tiles[i]
      coef1 = i/self.taille
      coef2=(1-coef1)
      coef = .5+.5*coef2
      c = self.coefColor(coef1)
      r = (.3 if i else .35)*self.caseT*coef
      p = self.slither(tile, 2**(-i/100))
      pygame.draw.circle(screen, c, p, r)
      j_p = self.closePosition(tile)
      if getaway[-1] != (j_p == i_p):
        getaway+=(j_p == i_p,)
    return len(getaway)>2


________________________

## class Map:

  **_middle_**:tuple; 
    la case la plus proche du milieu de la carte

  **_dimensions_**:tuple;
    dimension de la carte à partir des classe
  
  **_matrix_**: tuple(tuple);
    contient les cases et leur couleur
  
  **_case_taille_**: float;
    la taille des cases qui composent la carte

  **_constructor_**: function(`w`:int, `h`:int)=>Map;
    Cette classe crée une carte sur laquelle on va mettre des fruits et le serpent

  def ajouter_Serpent(self):
    self.serpent = Serpent(self.middle, self.case_taille)
  def nouveau_Fruit(self):
    self.fruit = Fruit(self)
  def draw_rectangle(self, x,y):
    pygame.draw.rect(screen, self.matrix[y][x], pygame.Rect((x*self.case_taille,y*self.case_taille) + (self.case_taille,)*2))
  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and self.serpent.current_v[1]!=+1: self.serpent.vecteur = (0,-1)
    elif keys[pygame.K_DOWN] and self.serpent.current_v[1]!=-1: self.serpent.vecteur = (0,+1)
    elif keys[pygame.K_LEFT] and self.serpent.current_v[0]!=+1: self.serpent.vecteur = (-1,0)
    elif keys[pygame.K_RIGHT] and self.serpent.current_v[0]!=-1: self.serpent.vecteur = (+1,0)
    return self.serpent.update(self)
  def display(self):
    for i in range(self.dimensions[0]):
      for j in range(self.dimensions[1]):
        self.draw_rectangle(i,j)
    self.fruit.display()
    return self.serpent.display()
  **_pos_**: tuple(float, 3);
    paramètre dans lequel on stocke le point

  **_persp_coef_**: int;
    coéfficient qui dépend de la profondeur `z` du point par lequel il faut multiplier l'abscisse `x` et l'ordonnée `y` de ce point pour avoir sa position sur un plan à partir de l'indice de perspective `perspective_index`
  
  **_draw_position_**:
    position du point sur le plan après toutes les modifications éffectuées: bouger en fonction de la perspective et déplacer le point jusqu'au milieu grâce à la fonction `applyScreen` qui utiliser la variable `mid_screen`

  **_rotate_**: function(`R`: tuple(tuple(float,2),3))=>None;
    L'argument `R` et un tuple contenant 3 tuples pour les rotation sur l'axe X, Y et Z respectivement qui contiennent les valeurs des cosinus et sinus respectivement des angles de ces rotations. Avec ces valeurs, on peut effectuer les modifications nécessaires grâce aux matrices de rotation pour changer la position du point en respectant la rotation demandée. Puis on redéfinit la le paramètre `draw_position` grâce à la position donnée.

  **_applyMatrixRotation_**: function(matrix: tuple(tuple(float,3),3))->None;
    méthode qui applique à la position du point les modifications nécessaires dues à l'ensemble des rotations de la planète traduites par la matrice `matrix` (**⚠ il faut le tester**)
  
  **_applyPerspective_**: function()=>tuple(float, 2);
    cette méthode change d'abord le coéfficient `persp_coef` pour enfin retourner la position du point dans un plan en appliquant une perspective de `perspective_index` (note: on utilise du logarithme pour cela)

  **_updateDrawPosition_**: function()->None;
    méthode qui permet de rafraichir le position du point sur l'écran `draw_position` (sans l'afficher)

________________________

**_drawAlphaRecct_**: function(pos, size, color)->bool;
  affiche un rectangle qui a une couleur qui peut-être traslucide 

**_drawAlphaImage_**: function(pos,size,href,alpha,center:bool)->bool;
  affiche une image qui peut être centrée grâce à l'argument center avec une opacité alpha et retourne la position des boutons _play_ et _exit_

**_requireStop_**: function()->bool;
  retourne True si le joueur a quitté la page pygame sinon retourne False

**_loop_**: function()->None;
  fonction principal qui sert comme une boucle _while_ qui update et display la carte et qui appelle la fonction gameover si le serpent se mord la queue ou s'il est hors de la carte 

**_mn_**:int;
  la plus petite taille de la résolution

**_gameover_**: function()->None;
  on affiche l'image de GAMEOVER qui se trouve dans les assets qui devient graduellement opaque puis on regarde si le joueur veut sortir du jeu ou bien rejouer, s'il veut rejouer on appelle la `loop` sinon, on sort le la boucle

________________________

# planet_viewer.py:
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
    méthode qui applique à la position du point les modifications nécessaires dues à l'ensemble des rotations de la planète traduites par la matrice `matrix` (**⚠ il faut le tester**)
  
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

  **_orientation_vertices_**: tuple(tuple(float,3),2);
    2 vertices qui indiquent l'orientation de la planète selon l'écran

  **_request_display_**: bool;
    paramètre qui permet de savoir s'il y a eu une modification afin dans la rotation de la planète afin que l'on ne calcule pas trop de choses pour rien

  **_addFlag_**: function(`flag`: Flag)=>None;
    méthode qui permet d'ajouter le `flag` sur la planète et d'effectuer les rotations sur le `flag` relatives à l'ensemble de rotations de la planète que l'on trouve grâce à la méthode ``

  **_getOrientationMatrix_**: function()->tuple(tuple(float, 3), 3);
    cette méthode renvoie la matrice qui traduit l'ensemble des rotations appliquées à la planète que l'on peut retrouver grâce à ses `orientation_vertices` 
    (le code est assez compliqué à comprendre, j'ai mis mes calculs dans les archives **⚠ je ne sais pas si ça marche car je ne l'ai pas encore testé**: ça semble, marcher, on a bien: ((1,0,0),(0,1,0),(0,0,1)) lorsque le script commence)
    
  **_rotate_**: function(`rotX`:float, `rotY`:float, `rotZ`:float)=>None;
    méthode qui permet d'effectuer les modifications nécessaires aux points dans la map uniquement s'il y a réellement une rotation à effectuer (afin de ne pas faire trop de calculs pour rien)

  **_display_**: function()=>None;
    méthode qui permet d'afficher les traits qui constituent la sphère et les flags de la map
