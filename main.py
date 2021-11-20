from web_search import *
import pygame


# Couleurs de base
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (144,238,144)
RED = (255, 0, 0)

#Setup de la fenetre pygame
pygame.init()
screen = pygame.display.set_mode([700, 500])

user = input('User: ')
password = input('Password: ')
logged_in = False


class OperatingSystem:
  def __init__(self,user,password):
    self.password= password
    self.user = user
    if password == '0000' and user == 'User1':
      print('Welcome back ' + user + '!')
      return
    else:
      print('Wrong !')
      return
  
  def mails():
    return

while True:
  screen.fill(BLACK)
  if not (logged_in):
    os = OperatingSystem(user, password)
    logged_in = True
  action = input('Command:')
  if action == '-randompage':
    load_page(random_page())
  if action == '-search':
    page = input('Search:')
    load_page(page)
    break

pygame.quit()
