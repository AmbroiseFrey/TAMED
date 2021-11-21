import web_search
import pygame

s = web_search

# Couleurs de base - un tuple (R,V,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Setup de la fenetre pygame
pygame.init()
screen = pygame.display.set_mode([700, 500])
pygame.display.set_caption("Projet")
screen.fill(RED)
RUN = True
user_logged = False




##----------------------------------------------------------------------##
##Calculs et fonctionnement de notre ordinateur (si on garde cette idée)##
##----------------------------------------------------------------------##

class OperatingSystem:


  def log_in():
    '''Fonction qui demande un username et un passcode. Les seuls valides pour l'instant son User: User1 et Password: 0000 '''
    user = input('User: ')
    password = input('Password: ')
    if password == '0000' and user == 'User1':
      print('Welcome back ' + user + '!')
      return user
    else:
      print('Wrong !')
      return False


  def render_text(text,pos):
    assert type(text) == str, 'Le text doit etre un string !'
    assert type(pos) == tuple, 'La pos doit etre un tuple !'
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(text, False, (255, 255, 255))
    screen.blit(text,pos)


  def render_image(image_name,pos,size):
    '''Fonction qui permet d\'afficher une image. Prend en argument le nom de l'image (str), sa position (tuple), et sa taille (tuple)'''
    assert type(image_name) == str, 'Le nom de l\'image doit etre un string !'
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    assert type(pos) == tuple, 'La taille doit etre un tuple !'
    loaded_img= pygame.image.load(image_name)
    loaded_img = pygame.transform.scale(loaded_img, size)
    screen.blit(loaded_img, pos + size)


  def render_rectangle(color,size,pos):
    '''Fonction qui permet d\'afficher un rectangle. Prend en argument la couleur (un tuple), sa taille (tuple), et sa position (tuple)'''
    pygame.draw.rect(screen, color, pygame.Rect(pos + size))

Os = OperatingSystem

##------------------------------##
##---Boucle Principale du Jeu---##
##------------------------------##

while RUN:

  #Parametres de notre souris
  click = pygame.mouse.get_pressed()[0]
  pos = pygame.mouse.get_pos()
  x = pos[0]
  y = pos[1]

  if not(user_logged):
    user_logged = Os.log_in()
      
  else:
    screen.fill(RED)
    Os.render_rectangle(WHITE, (20,30), (0,300))
    Os.render_text('Loading...',(0,0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN= False
    
    if click:
      print('Click')

  pygame.display.flip()

pygame.quit()
