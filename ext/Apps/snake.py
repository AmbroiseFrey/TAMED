import pygame, time, random
from math import ceil, sin, pi
from ext.Core import variables as varia
from ext.Core import operations as Opr
pygame.init()

def test():
  return 'Successfully built snake game'

resolution = varia.resolution
screen = pygame.display.set_mode(resolution)
mid_screen = tuple(i/2 for i in resolution)
clock = pygame.time.Clock()

def minInt(a,b): return a if a<b else b

class Serpent:
  tilePerCase = 10
  def __init__(self, p, caseT: float, v = (1,0), taille = 15, d = ((255,255,0),(255,167,0))):
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
    c = self.caseT/7*(.5+.5*coef)
    return (
      p[0]-sin(p[1]*self.off)*c,
      p[1]+sin(p[0]*self.off)*c
      )
  def change_destination(self):
    if self.vecteur == self.current_v:
      return
    if self.current_v[0]:
      e=(self.p[0]+self.caseT*.5)%self.caseT
      if self.current_v[0] == 1: e = self.caseT-e
    else:
      e =(self.p[1]+self.caseT*.5)%self.caseT
      if self.current_v[1] == 1: e = self.caseT-e
    if (e<self.caseT/Serpent.tilePerCase):
      self.p = (
        int(2*(self.p[0]+e*self.current_v[0]))/2,
        int(2*(self.p[1]+e*self.current_v[1]))/2
      )
      self.current_v = self.vecteur
  def update(self):
    self.change_destination()
    self.p= tuple(self.p[i]+self.current_v[i]*self.caseT/Serpent.tilePerCase for i in range(2))
    self.tiles = (self.p,)+self.tiles[:self.taille-1]
  def display(self):
    for i in range(len(self.tiles)-1,-1,-1):
      tile = self.tiles[i]
      coef1 = i/self.taille
      coef2=(1-coef1)
      coef = .5+.5*coef2
      c = self.coefColor(coef1)#(0,255,0) if i%2 else (255,255,0)
      r = (.3 if i else .35)*self.caseT*coef
      pygame.draw.circle(screen, c, self.slither(tile, 2**(-i/100)), r)

class Food:
  def __init_(self, x, y):
    self.pos = [x,y]
    pass
  def spawn_food(self):
    pass
    


class Map:
  def __init__(self, w, h):
    self.dimensions = (w, h)
    self.matrix = tuple(tuple((150, 150, 150) if (i+j)%2 else (50,50,50) for i in range(w)) for j in range(h))
    self.middle = (ceil(w/2-.5), ceil(h/2-.5))
    self.case_taille = minInt(resolution[0]/w, resolution[1]/h)
  # def matrix_addSerpent(self):
  #   for case in self.serpent.cases:
  #     #print(' ',case)
  #     self.matrix[case[1]][case[0]] = 1
  def ajouter_Serpent(self):
    self.serpent = Serpent(self.middle, self.case_taille)
    # self.matrix_addSerpent()
  def draw_rectangle(self, x,y):
    pygame.draw.rect(screen, self.matrix[y][x], pygame.Rect((x*self.case_taille,y*self.case_taille) + (self.case_taille,)*2))
  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and self.serpent.current_v[1]!=+1: self.serpent.vecteur = (0,-1)
    elif keys[pygame.K_DOWN] and self.serpent.current_v[1]!=-1: self.serpent.vecteur = (0,+1)
    elif keys[pygame.K_LEFT] and self.serpent.current_v[0]!=+1: self.serpent.vecteur = (-1,0)
    elif keys[pygame.K_RIGHT] and self.serpent.current_v[0]!=-1: self.serpent.vecteur = (+1,0)
    # reset_case = self.serpent.update()
    # #print(reset_case)
    # self.matrix[reset_case[1]][reset_case[0]] = 0
    # self.matrix_addSerpent()
    self.serpent.update()
  def display(self):
    for i in range(self.dimensions[0]):
      for j in range(self.dimensions[1]):
        self.draw_rectangle(i,j)
    self.serpent.display()


def game():
    carte = Map(11,11)
    carte.ajouter_Serpent()
    x=0
    RUN = True
    x,y = varia.mid_screen
    while RUN:
      x+=1
      if x%10==0:
        carte.serpent.taille+=1
        screen.fill((0,0,0))
        carte.update()
        carte.display()
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            RUN = False
      clock.tick(60)
      Opr.render_image('Assets/Icons/cross.png',(0,0),(50,50))
      #Ici on check les events autre que les touches fleches
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          RUN = False

        #Si la souris est pressée
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse_presses = pygame.mouse.get_pressed()
          if mouse_presses[0]:

            #On check si l'utilisateur veut quitter le jeu
            if Opr.check_interaction(event.pos, (0,50,0,50),['plat'], 'plat') == True:
              RUN = False
              return 'fd0'
        pygame.display.flip()
    return 'fd0'