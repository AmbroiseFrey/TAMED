import pygame ,time
import ext.web_search as s
import ext.platformer as plat
import ext.file_explorer as files




# Couleurs de base - un tuple (R,V,B)
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

#Setup de la fenetre pygame
pygame.init()

#Taille
resolution = (600,400)
screen = pygame.display.set_mode([600,400])

#Nom et icon de notre fenetre
pygame.display.set_caption("Krypt Corp")
logo = pygame.image.load('Assets/Logos/Icon_(Test).png')
pygame.display.set_icon(logo)

#Variables pour faire marcher la base de notre programme
RUN = True
user_logged = False
output = ''
page = 'home'
fd_dict = 'C:/'


##--------------------------------------------------------------------------##
##--------------Calculs et fonctionnement de notre ordinateur---------------##
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
      screen.fill(BASE_COLOR)
      Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
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
      screen.fill(BASE_COLOR)
      Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
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
      Os.loading('bar', 2)
      return user
    else:
      Os.render_text('Acces Denied!', (100,150), RED)
      pygame.display.flip()
      time.sleep(3)
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
    '''
    Fonction qui fait une animation de load. Type d'animation et temps de l'animation a spécifier
    '''
    if animation_type == 'text':
      Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      for i in range(100):
        Os.render_text('Loading '+str(i)+'% ...',(0,0))
        pygame.display.flip()
        time.sleep(float(time_run/100))
        Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
    elif animation_type == 'bar':
      Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      for i in range(100):
        Os.render_rectangle(WHITE, (4*i,50), (100,330))
        pygame.display.flip()
        time.sleep(float(time_run/100))
      for i in range(5):
        Os.render_rectangle(WHITE, (400,50), (100,330))
        pygame.display.flip()
        time.sleep(0.2)
        Os.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
        pygame.display.flip()
        time.sleep(0.2)
  
  def time():
    '''
    Affiche l\'heure
    '''
    Os.render_text(time.strftime("%Y-%m-%d"),(522,385),BLACK,20)
    Os.render_text(time.strftime("%H:%M"),(520,355),BLACK,40)
  

  def render_file(file_contents: list, file_name: str = 'File', x: int = 20, y: int =100, espacement_ligne : int = 20):
    '''
    Render le content d'un file
    '''
    if type(file_contents) == list:
      for el in file_contents:
        Os.render_text(el, (x,y))
        y += espacement_ligne
    else:
      Os.render_text(file_contents, (x,y))

  def render_file_tree(file_path: str):
    '''
    Render les dossiers dans un file path
    '''
    i = 50
    files_loaded = files.explore_file(file_path)
    print(type(files_loaded), end = "\r")
    if type(files_loaded) == dict:
      for el in files_loaded:
        Os.render_text(el,(20,i),WHITE,30)
        i+=20
    else:
      Os.render_file(files_loaded)
    
      
  def render_fd_base():
    '''
    Render la base du file directory
    '''
    #Background
    screen.fill(BLUE_GREY)

    #Bar haut de Fenetre
    Os.render_rectangle(GREY, (600,30), (0,0))
    Os.render_image('Assets/Icons/Close_(Test).png',(0,0),(30,30))

    #Barre des taches
    Os.render_rectangle(WHITE, (600,70), (0,350))
    Os.time()

    #Applications
    Os.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))
    Os.render_rectangle(LIGHT_BLUE, (55,55),(55, 350))
    Os.render_image('Assets/Icons/Folder_(Test).png',(60,350),(50,50))

    



Os = OperatingSystem

#tests des extensions
#peut etre utilisé pour le load
def test_ext(time_sleep:int = 0.5):
  print(plat.test())
  screen.fill(BASE_COLOR)
  Os.render_text('Tests: This is a Beta Version',(0,0))
  pygame.display.flip()
  time.sleep(0.4)
  Os.render_text('Built Robot Core',(0,20))
  pygame.display.flip()
  time.sleep(0.4)
  files.explore_file()
  print(files.Files)
  print('File Directory Connected')
  Os.render_text('Built File Directory',(0,40))
  pygame.display.flip()
  time.sleep(0.4)
  s.load_page('www.test.com')
  Os.render_text('Connected to Web',(0,60))
  pygame.display.flip()
  time.sleep(time_sleep)

test_ext()
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

    #Pour la page HOME
    if page == 'home':

      #Background
      screen.fill(BASE_COLOR)
      Os.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),resolution)

      #Barre des taches
      Os.render_rectangle(WHITE, (600,70), (0,350))
      Os.time()

      #Applications
      Os.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))
      Os.render_image('Assets/Icons/Folder_(Test).png',(60,350),(50,50))

    #Pour le FILE Directory
    if page == 'fd0':
      Os.render_fd_base()
      Os.render_file_tree(fd_dict)
      fd_dict = output
      Os.render_typing_text((40,7))
      open = True
      


      



  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)

        #Appli file directory
        if Os.check_interaction(event.pos, (55,110,260,400),['home']) == True:
          page = 'fd0'
          output = 'C:/'
        
        #Appli home (comme le bouton windows ?)
        elif Os.check_interaction(event.pos, (0,50,360,400),['home', 'fd0']) == True:
          page = 'home'
        #Close button
        elif Os.check_interaction(event.pos, (0,30,0,30),['fd0']) == True:
          page = 'home'
    
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
