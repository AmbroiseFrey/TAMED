import pygame
from ext.Core import variables

screen = pygame.display.set_mode(variables.resolution)
screen_rect = screen.get_rect()

class Image:
  relative = (0,0)
  def __init__(self,url,x = 0,y=0, w=None, h=None):
    """
    crée une image qui sera utilisée pour les Sprites en prenant en argument l'`url` de l'image, son abscisse `x`, son ordonnée `y` et/ou sa taille définie par `w` et `h`
    """
    self.img = pygame.image.load(url) # on load l'image
    r = list(self.img.get_rect()) # on cherche les coordonnées du rectangle/hitbox
    if not (w and h):
      if w: 
        h = w/r[2]*r[3]
      elif h:
        w = h/r[3]*r[2]
      else: 
        w,h = r[2],r[3]
    self.size = r[2],r[3] = w,h
    self.r = [r[i]+(x,y)[i%2] for i in range(4)];
    self.img = pygame.transform.scale(self.img, (w,h))
    self.pos = (x,y)
  def display(self):
    screen.blit(self.img, tuple(self.pos[i]-Image.relative[i] + variables.mid_screen[i] for i in range(2))+self.size)

class Group:
  def __init__(self):
    self.length = 0
    self.list = ()
  def add(self, obj):
    self.list += (obj,)
    self.length += 1
  def forEach(self,callback):
    for i in self.list:
      callback(i)
  def display(self):
    self.forEach(lambda i: i.display())

##########  Sprites  ##########

class Sprite(Image): # Cette classe permet de créer un Sprite, c'est à dire qu'on crée un `image` sur l'écran et cette image correspond à un objet Sprite de hauteur `height`, de largeur `width`, d'abscisse `x` et d'ordonnée `y`
  def __init__(self, image, x=0, y=0, w=None, h=None): 
    super().__init__(image, x, y, w, h)
    self.borders = () # 0:top; 1:right; 2:bottom; 3:left
    self.updateBorders()
    self.display()
  
  def collides_with(self, environment, checkAll=False):
    result = [] if checkAll else None
    for i in environment.list:
      if i.r[0]<=self.r[2] and i.r[2]>=self.r[0] and i.r[1]<self.r[3] and i.r[3]>self.r[1]:
        if checkAll:
          result.append(i)
        else:
          return i
    return result
  def getTouchBorders(self,sprite):
    pass
  def updateBorders(self):
    A,B,C,D = self.r
    self.borders = (
      ((A,B),(C,B)),
      ((C,B),(C,D)),
      ((A,D),(C,D)),
      ((A,B),(A,D))
    )
  def borderCollide(self, border_number, environment:Group):
    border = self.borders[border_number]
    borderType = border[0][0] == border[1][0] # si True: border is left or right, else, border is top or down
    for i in environment.list:
      if borderType:
        if i.r[0]<border[0][0]<i.r[2] and border[0][1]+5<i.r[3] and border[1][1]-5>i.r[1]:
          return i 
      else:
        if i.r[1]<border[0][1]<i.r[3] and border[0][0]+5<=i.r[2] and border[1][0]-5>i.r[0]:
            return i
    return None

class MotionSprite(Sprite):
  def __init__(self, image: str, x: int, y: int, w: int, h: int, v = [0,0], f  = [1, 1]):
    """
    `x`: abscisse, `y`: ordonnée, `w`: largeur, `h`: hauteur,
    `v`: vecteur force, `f`: friction
    """
    super().__init__(image, x, y, w, h)
    self.vector = v
    self.f = tuple(1-i for i in f)
  def newRect(self):
    return [self.r[i] + self.v[i%2] for i in range(4)]
  def updateVector(self):
    self.v = [self.vector[i] * self.f[i] for i in range(2)]