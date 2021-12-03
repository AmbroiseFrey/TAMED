from ext.Platformer_Scrolling.game_utils import Image, MotionSprite, Sprite, screen_rect
import pygame

class Player(MotionSprite):
  def __init__(self):
    super.__init__()
  def move(self, x, y):
    self.pos = (x,y)
    self.r = [self.r[i]+(x,y)[i%2] for i in range(4)]
  def update(self, floor):
    move = pygame.key.get_pressed()
    self.vector = [
      -4 if move[pygame.K_LEFT] else 4 if move[pygame.K_RIGHT] else 0,
      -4 if move[pygame.K_UP] else 0
    ]

    # on regarde si le `player` touche le sol
    touch_floor_bottom = self.collides_with(floor)
    if touch_floor_bottom:
      print("touching floor")
      self.vector[1] = 0
    else:
      self.vector[1] += .5

    # self.move() # On update la character
    # self.rect.clamp_ip(screen_rect) # Permet d'empecher le character de sortir de l'ecran
    Image.relative = self.pos
    

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