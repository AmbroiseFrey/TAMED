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
  def getBorderPoints(self,number:int):
    """0 -> haut   1 -> droite   2 -> bas   3 -> gauche"""
    assert number < 4 and number > 0, "il n'y a que 4 côtés autour d'un sprite"
    r = self.rect
    return (
      ((r[0],r[1]),(r[2],r[1])) if number == 0 else
      ((r[2],r[1]),(r[2],r[3])) if number == 1 else
      ((r[2],r[3]),(r[0],r[3])) if number == 2 else
      ((r[0],r[3]),(r[0],r[1]))
    )
  def borderCollide(self,border_number, environment):
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
    return [self.r[i]+self.v[i%2] for i in range(4)]
  def updateVector(self):
    self.v = [self.v[i]*self.f[i] for i in range(2)]


##########  Components  ##########

class Player(MotionSprite):
  def __init__(self):
    super.__init__()
  def move(self, x, y):
    self.pos = (x,y)
    self.r = [self.r[i]+(x,y)[i%2] for i in range(4)]
  def update(self, level, floor, flag, lava):
    move = pygame.key.get_pressed()
    self.vector = [
      -4 if move[pygame.K_LEFT] else 4 if move[pygame.K_RIGHT] else 0,
      -4 if move[pygame.K_UP] else 0
    ]

    # on regarde si le `player` touche le sol
    touch_floor = self.collides_with(floor)
    if touch_floor:
      self.vector[1] = 0
    else:
      self.vector[1] += .5

    if flag:
      print("Flag")
      return 'Flag'
      

    if lava:
      print("Lava")
      return 'Lava'

    # self.move(h_move, v_move, floor) # On update la character
    self.rect.clamp_ip(screen_rect) # Permet d'empecher le character de sortir de lecran

  def check_collision(self, x, y, environment):
    self.rect.move_ip([x, y]) #On fait bouger le sprite
    collide = pygame.sprite.spritecollideany(self, environment) #On check si il touche le sol
    self.rect.move_ip([-x, -y]) #On le renvoit d'ou il vient
    return collide
    

#On definit le sol
class Floor(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Floor_(Test).png", x, y)


class Level_Flag(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Checkpoint.png", x, y)

class Lava(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Lava.png", x, y)

class Platform(Sprite): #Moving platform
  def __init__(self, x, y, speed):
    super().__init__("Assets/Platformer/Floor_(Test).png", x, y)
    self.speed = speed # Vitesse de deplacement
 
  def move(self):
    pass