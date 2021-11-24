import ext.web_search as s
import pygame ,time
import ext.platformer as plat

#plat.test()
#s.load_page('www.test.com')


# Couleurs de base - un tuple (R,V,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Setup de la fenetre pygame
pygame.init()

#Taille
screen = pygame.display.set_mode([700, 500])

#Nom et icon de notre fenetre
pygame.display.set_caption("Projet")
logo = pygame.image.load('Assets/Logos/Icon_(Test).png')
pygame.display.set_icon(logo)

#Variables pour faire marcher la base de notre programme
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
    '''
    Fonction qui demande un username et un passcode.
    Les seuls valides pour l'instant son User: User1 et Password: 0000
    '''

    #On demande le user
    open = True
    output = ''
    while open:
      screen.fill(RED)
      Os.render_text('User: '+output, (100,100))
      Os.render_text('Password: ', (100,120))
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            user = output
            open = False
          elif event.key == pygame.K_BACKSPACE:
            output =  output[:-1]
          else:
            output += event.unicode

    #On demande le password
    open = True
    output = ''
    while open:
      screen.fill(RED)
      Os.render_text('User: '+user, (100,100))
      Os.render_text('Password: '+output, (100,120))
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            password = output
            open = False
          elif event.key == pygame.K_BACKSPACE:
            output =  output[:-1]
          else:
            output += event.unicode

    #On check le password et le user
    if password == '0000' and user == 'User1':
      Os.loading('bar', 3)
      print('Welcome back ' + user + '!')
      return user
    else:
      print('Wrong !')
      return False



  def render_text(text: str,pos: tuple,color: tuple = WHITE,size: int = 30):
    '''
    Fonction qui permet d\'afficher du texte.
    Prend en argument le texte (str) et sa position (tuple)
    '''
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(text, True, color)
    screen.blit(text,pos)


  def render_typing_text(pos:tuple):
    '''
    Fonction qui permet d\'afficher du texte qui est tapé et qui interagit avec le programme sans utiliser input().
    Prend en argument le texte (str) et sa position (tuple)
    '''
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(output, False, (255, 255, 255))
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


  def check_interaction(clickpos: tuple, wanted_area: tuple, wanted_pages: list):
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

  def loading(animation_type: str,time_run: int):
    if animation_type == 'text':
      for i in range(100):
        Os.render_text('Loading '+str(i)+'% ...',(0,0))
        pygame.display.flip()
        time.sleep(float(time_run/100))
        screen.fill(RED)
    elif animation_type == 'bar':
      for i in range(100):
        Os.render_rectangle(BLACK, (5*i,50), (100,200))
        pygame.display.flip()
        time.sleep(float(time_run/100))
        screen.fill(RED)
      for i in range(5):
        Os.render_rectangle(BLACK, (500,50), (100,200))
        pygame.display.flip()
        time.sleep(0.2)
        screen.fill(RED)
        pygame.display.flip()
        time.sleep(0.2)
  
  def time():
    Os.render_text(time.strftime("%Y-%m-%d", time.gmtime()),(620,385),BLACK,20)
    Os.render_text(time.strftime("%H:%M", time.gmtime()),(620,355),BLACK,40)
    




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
    Os.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),(700,500))
    Os.render_rectangle(WHITE, (700,70), (0,350))
    Os.render_text('Welcome back!',(0,0))
    Os.time()
    Os.render_circle(BLACK,20,(100,100))
    Os.render_typing_text((100,100))
    Os.render_image('Assets/Logos/Home_Button_(Test).png',(x,y),(50,50))


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)
        if Os.check_interaction(event.pos, (100,200,100,200),['home']) == True:
          print('Clicked area')
    
    #Si le clavier est utilisé
    if event.type == pygame.KEYDOWN:

      #Lien entre le clavier et le script sans utiliser input
      if open:
        if event.key == pygame.K_RETURN:
          open = False
        elif event.key == pygame.K_BACKSPACE:
          output =  output[:-1]
        else:
          output += event.unicode

      if event.key == pygame.K_KP_ENTER:
        #Si le enter du key pad (les chiffres) est utilisé, lancer le lien entre clavier et notre programme sans passer par input
        open = True
        output = ''
      
      if event.key == pygame.K_LCTRL:
        Os.render_text('Hacking...',(200,200))

  pygame.display.flip()

pygame.quit()
