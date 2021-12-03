import pygame, time
import ext.Core.variables as varia

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(varia.resolution)

def render_text(text: str,pos: tuple,color: tuple = varia.WHITE,size: int = 30):
  '''
  Fonction qui permet d'afficher du texte.
  Prend en argument le texte (str) et sa position (tuple)
  '''
  pygame.font.init()
  font = pygame.font.SysFont('Comic Sans MS', size)
  text = font.render(text, True, color)
  screen.blit(text,pos)


def render_image(image_name: str,pos: tuple,size: tuple):
  '''
  Fonction qui permet d'afficher une image.
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
  Fonction qui permet d'afficher un cercle.
  Prend en argument la couleur (un tuple), son rayon (int), et sa position (tuple)
  '''
  pygame.draw.circle(screen, color, pos, radius)

def check_interaction(clickpos: tuple, wanted_area: tuple, wanted_pages: list, page: str):
  '''
  Fonction qui prend en parametre la position de la souris au moment du click que l'on check et qui la compare avec la zone que l'on veut sous forme de tuple - (x1, x2,y1,y2)
  Compare aussi la page du jeu et la page dans lesquelles le bouton marche. 
  La fonction renvoi True ou False selon si la souris est bien a l'endroit voulu
  '''
  if page in wanted_pages:
    if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
      return True
    else:
      return False
  else:
    return False

def render_time():
  '''
  Affiche l'heure
  '''
  hour = time.strftime("%H")
  hour = int(hour) +1
  render_text(time.strftime("%Y-%m-%d"),(522,385),varia.BLACK,20)
  render_text(str(hour) +':' + time.strftime("%M"),(520,355),varia.BLACK,40)

def render_file(file_contents: list, file_name: str = 'File', x: int = 20, y: int =50, espacement_ligne : int = 20):
  '''
  Render le content d'un fichier
  '''
  if type(file_contents) == list:
    for el in file_contents:
      render_text(el, (x,y), varia.WHITE,20)
      y += espacement_ligne
  elif type(file_contents) == str:
    if file_contents[len(file_contents)-3:len(file_contents)] == 'mp3':
      pygame.mixer.music.load('Assets/Directory Files/'+file_contents)
      pygame.mixer.music.play()
    elif file_contents[len(file_contents)-3:len(file_contents)] in ['png','jpg']:
      render_image('Assets/Directory Files/'+file_contents, (x,y), (480,280))
    else:
      render_text(file_contents, (x,y))
  else:
    pass