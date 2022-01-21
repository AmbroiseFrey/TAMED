import pygame, time
from math import ceil, sin, pi, floor
from random import randint
###################################
####voir documentation.md!!!!!!####
###################################


resolution = (600,600)
screen = pygame.display.set_mode(resolution, pygame.DOUBLEBUF, 32)
mid_screen = tuple(i/2 for i in resolution)
clock = pygame.time.Clock()

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

class Map:
  def __init__(self, w, h):
    self.dimensions = (w, h)
    self.matrix = tuple(tuple((150, 150, 150) if (i+j)%2 else (50,50,50) for i in range(w)) for j in range(h))
    self.middle = (ceil(w/2-.5), ceil(h/2-.5))
    self.case_taille = minInt(resolution[0]/w, resolution[1]/h)
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

def drawAlphaRect(pos, size, color):
  s = pygame.Surface(size, pygame.SRCALPHA)
  s.fill(color)
  screen.blit(s, pos)
def drawAlphaImage(pos,size,href, alpha, center=False):
  loaded_img= pygame.image.load(href).convert()
  loaded_img = pygame.transform.scale(loaded_img, size)
  loaded_img.set_alpha(alpha)
  if center:
    pos = tuple(
      pos[i]-size[i]/2 +mid_screen[i]
      for i in (0,1)
    )
  screen.blit(loaded_img, pos)
  return (
    (149/240*size[1]+pos[1],.85*size[1]+pos[1]),
    (.125*size[0]+pos[0],35/96*size[0]+pos[0]),
    (61/96*size[0]+pos[0],.875*size[0]+pos[0])
  )

def requireStop():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      return True
  return False

def loop():
  carte = Map(11,11)
  carte.ajouter_Serpent()
  carte.nouveau_Fruit()
  while True:
    if carte.update():
      break
    screen.fill((0,0,0))
    if carte.display():
      break
    if requireStop(): return
    pygame.display.flip()
    clock.tick(60)
  gameover()

mn = min(*resolution)
def gameover():
  arr = pygame.surfarray.array2d(screen)
  for i in range(0,255,2):
    pygame.surfarray.blit_array(screen, arr)
    drawAlphaImage((0,0),(mn/2,mn/4),'Assets/snake/snake_game_goScreen.png', min(int(i),255), True)
    if requireStop(): return
    pygame.display.flip()
    clock.tick(60)
  data = drawAlphaImage((0,0),(mn/2,mn/4),'Assets/snake/snake_game_goScreen.png', 255, True)
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)
          if data[0][0]<=event.pos[1]<=data[0][1]:
            if data[1][0]<=event.pos[0]<=data[1][1]:
              loop()
              return
            elif data[2][0]<=event.pos[0]<=data[2][1]:
              return