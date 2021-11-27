import pygame, time

pygame.init()

BASE_COLOR = (32,194,14)
BLACK = (0, 0, 0)
GREY = (211,211,211)
BLUE_GREY = (102, 153, 204)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173,216,230)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


resolution = (600,400)
screen = pygame.display.set_mode([600,400])

def render_text(text: str,pos: tuple,color: tuple = WHITE,size: int = 30):
  '''
  Fonction qui permet d\'afficher du texte.
  Prend en argument le texte (str) et sa position (tuple)
  '''
  pygame.font.init()
  font = pygame.font.SysFont('Comic Sans MS', size)
  text = font.render(text, True, color)
  screen.blit(text,pos)


def render_image(image_name: str,pos: tuple,size: tuple):
  '''
  Fonction qui permet d\'afficher une image.
  Prend en argument le nom de l'image (str), sa position (tuple), et sa taille (tuple)'''
  loaded_img= pygame.image.load(image_name)
  loaded_img = pygame.transform.scale(loaded_img, size)
  screen.blit(loaded_img, pos + size)


def render_rectangle(color: tuple,size: tuple,pos: tuple):
  '''
  Fonction qui permet d\'afficher un rectangle.
  Prend en argument la couleur (un tuple), sa taille (tuple), et sa position (tuple)'''
  pygame.draw.rect(screen, color, pygame.Rect(pos + size))


def render_circle(color: tuple,radius: int,pos: tuple):
  '''
  Fonction qui permet d\'afficher un cercle.
  Prend en argument la couleur (un tuple), son rayon (int), et sa position (tuple)
  '''
  pygame.draw.circle(screen, color, pos, radius)
