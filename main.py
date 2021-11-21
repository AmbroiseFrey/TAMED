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
    
  def render_text(text):
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(text, False, (255, 255, 255))
    return text

os = OperatingSystem

##------------------------------##
##---Boucle Principale du Jeu---##
##------------------------------##

while RUN:
  screen.fill(RED)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN= False
    
    #Si clavier
    if event.type == pygame.KEYDOWN:
      if not(user_logged):
        user_logged = OperatingSystem.log_in()
      else:
        screen.fill(RED)
        action = input('Command:')
        if action == '-randompage':
          screen.blit(os.render_text(s.load_page(s.random_page())),(0,0)) 
          action = ''
        if action == '-search':
          page = input('Search:')
          screen.blit(os.render_text(s.load_page(page)),(0,0))
          action = ''


pygame.quit()
