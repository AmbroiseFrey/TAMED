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
os = False




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
      return True
    else:
      print('Wrong !')
      return False



##------------------------------##
##---Boucle Principale du Jeu---##
##------------------------------##

while RUN:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN= False
    
    #Si clavier
    if event.type == pygame.KEYDOWN:
      if not(os):
        os = OperatingSystem.log_in()
      elif os:
        screen.fill(RED)
        action = input('Command:')
        if action == '-randompage':
          s.load_page(s.random_page())
          action = ''
        if action == '-search':
          page = input('Search:')
          s.load_page(page)
          action = ''


pygame.quit()
