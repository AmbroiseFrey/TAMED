import web_search
import pygame
import time

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
output = ''
page = 'home'


##--------------------------------------------------------------------------##
##--Calculs et fonctionnement de notre ordinateur (si on garde cette idée)--##
##----------------Sinon, toujours utile d'avoir une classe------------------##
##Qui comprend toutes les fonctions qui facilitent l'interaction avec pygame##
##--------------------------------------------------------------------------##

class OperatingSystem:


  def log_in():
    '''Fonction qui demande un username et un passcode. Les seuls valides pour l'instant son User: User1 et Password: 0000 '''
    return True
    #user = input('User: ')
    #password = input('Password: ')
    #if password == '0000' and user == 'User1':
      #print('Welcome back ' + user + '!')
      #return user
    #else:
      #print('Wrong !')
      #return False


  def render_text(text,pos):
    '''
    Fonction qui permet d\'afficher du texte.
    Prend en argument le texte (str) et sa position (tuple)
    '''
    assert type(text) == str, 'Le texte doit etre un string !'
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(text, False, (255, 255, 255))
    screen.blit(text,pos)

  def render_typing_text(pos):
    '''
    Fonction qui permet d\'afficher du texte qui est tapé et qui interagit avec le programme sans utiliser input().
    Prend en argument le texte (str) et sa position (tuple)
    '''
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(output, False, (255, 255, 255))
    screen.blit(text,pos)


  def render_image(image_name,pos,size):
    '''
    Fonction qui permet d\'afficher une image.
    Prend en argument le nom de l'image (str), sa position (tuple), et sa taille (tuple)'''
    assert type(image_name) == str, 'Le nom de l\'image doit etre un string !'
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    assert type(size) == tuple, 'La taille doit etre un tuple !'
    loaded_img= pygame.image.load(image_name)
    loaded_img = pygame.transform.scale(loaded_img, size)
    screen.blit(loaded_img, pos + size)


  def render_rectangle(color,size,pos):
    '''
    Fonction qui permet d\'afficher un rectangle.
    Prend en argument la couleur (un tuple), sa taille (tuple), et sa position (tuple)'''
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    assert type(size) == tuple, 'La taille doit etre un tuple !'
    pygame.draw.rect(screen, color, pygame.Rect(pos + size))


  def render_circle(color,radius,pos):
    assert type(pos) == tuple, 'La position doit etre un tuple !'
    assert type(radius) == int, 'Le rayon doit etre un chiffre !'
    '''
    Fonction qui permet d\'afficher un cercle.
    Prend en argument la couleur (un tuple), son rayon (int), et sa position (tuple)
    '''
    pygame.draw.circle(screen, color, pos, radius)


  def check_interaction(clickpos, wanted_area, wanted_pages):
    '''
    Fonction qui prend en parametre la position de la souris au moment du click que l'on check et qui la compare avec la zone que l'on veut sous forme de tuple - (x1, x2,y1,y2)
    Compare aussi la page du jeu et la page dans lesquelles le bouton marche. 
    La fonction renvoi True ou False selon si la souris est bien a l'endroit voulu
    '''
    assert type(wanted_pages) == list, 'Les pages marchant doivent etre une liste !'
    if page in wanted_pages:
      if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
        return True
      else:
        return False
    else:
      return False

    




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
    Os.render_circle(BLACK,20,(100,100))
    Os.render_typing_text((100,100))


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)
        if Os.check_interaction(event.pos, (100,200,100,200)) == True:
          print('Clicked area')
    

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_KP_ENTER:
        open = True
        output = ''
      
      if event.type == pygame.KEYDOWN and open:
        if event.key == pygame.K_RETURN:
          open = False
        elif event.key == pygame.K_BACKSPACE:
          output =  output[:-1]
        else:
          output += event.unicode


  pygame.display.flip()

pygame.quit()
