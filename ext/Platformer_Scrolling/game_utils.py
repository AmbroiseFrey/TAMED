import pygame
import ext.Core.variables as variables

screen = pygame.display.set_mode(variables.resolution)
screen_rect = screen.get_rect()

class Image:
  relative = (0,0) #est-ce que je peux l'avoir en faisant Image.relative ? je crois
  def __init__(self,url,x = 0,y=0, w=None, h=None):
    """crée une image qui sera utilisée pour les Sprites en prenant en argument l'`url` de l'image, son abscisse `x`, son ordonnée `y` et/ou sa taille définie par `w` et `h`"""
    self.img = pygame.image.load(url)
    r = list(self.img.get_rect())
    if not (w and h):
      if w: 
        h = w/r[2]*r[3]
      elif h:
        w = h/r[3]*r[2]
      else: 
        w,h = r[2],r[3]
    self.size = r[2],r[3] = w,h
    self.r = [r[i]+(r[i%2]if i>1 else 0) for i in range(4)];
    self.img = pygame.transform.scale(self.img, (w,h))
    self.pos = (x,y)
  def display(self):
    screen.blit(self.img, tuple(self.pos[i]-Image.relative[i] for i in range(2)))


##########  Sprites  ##########

class Sprite(Image): # Cette classe permet de créer un Sprite, c'est à dire qu'on crée un `image` sur l'écran et cette image correspond à un objet Sprite de hauteur `height`, de largeur `width`, d'abscisse `x` et d'ordonnée `y`
  def __init__(self, image, x=0, y=0, w=None, h=None): 
    super().__init__(image, x, y, w, h)
    self.borders = ()
    self.updateBorders()
  
  def collides_with(self, environment, checkAll=False):
    result = [] if checkAll else None
    for i in environment:
      if i.r[0]<=self.r[2] and i.r[2]>=self.r[0] and i.r[1]<self.r[3] and i.r[3]>self.r[1]:
        if checkAll:
          result.append(i)
        else:
          return i
    return result
  def getTouchBorders(self,sprite):
    pass
  def updateBorders(self):
    A,B,C,D = self.rect
    self.borders = (
      ((A,B),(C,B)),
      ((C,B),(C,D)),
      ((C,D),(A,D)),
      ((A,D),(A,B))
    )
  def borderCollide(self, border_number, environment):
    border = self.borders[border_number]
    borderType = border[0][0] == border[1][0] # si True: border is left or right, else, border is top or down
    for i in environment:
      if borderType:
        if border[0][1]
      else:
        pass
  
class MotionSprite(Sprite):
  def __init__(self, image: str, x: int, y: int, w: int, h: int, v: (list|tuple)[int] = [0,0], f: (list|tuple)[int] = [1, 1]):
    """
    `x`: abscisse, `y`: ordonnée, `w`: largeur, `h`: hauteur,
    `v`: vecteur force, `f`: friction
    """
    super.__init__(image, x, y, w, h)
    self.vector = v
    self.f = [1-i for i in f]
  def newRect(self):
    return [self.r[i] + self.v[i%2] for i in range(4)]
  def updateVector(self):
    self.v = [self.v[i] * self.f[i] for i in range(2)]
