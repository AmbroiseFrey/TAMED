import pygame ,time
import ext.web_search as s
import ext.platformer as plat
import ext.file_explorer as files
import ext.operations as Opr




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
pygame.mixer.init()

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
clickable_icons = {}


##--------------------------------------------------------------------------##
##--------------Calculs et fonctionnement de notre ordinateur---------------##
##--------------------------------------------------------------------------##


  
class Computer:

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
      Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      Opr.render_text('User: '+output, (50,50))
      Opr.render_text('Password: ', (50,70))
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
      Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      Opr.render_text('User: '+user, (50,50))
      Opr.render_text('Password: '+output, (50,70))
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
      Compu.loading('bar', 2)
      return user
    else:
      Opr.render_text('Acces Denied!', (50,100), RED)
      pygame.display.flip()
      time.sleep(3)
      return False


  def render_typing_text(pos:tuple, size:int = 30):
    '''
    Fonction qui permet d\'afficher du texte qui est tapé et qui interagit avec le programme sans utiliser input().
    Prend en argument le texte (str) et sa position (tuple)
    '''
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(output, False, (255, 255, 255))
    screen.blit(text,pos)


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
      Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      for i in range(100):
        Opr.render_text('Loading '+str(i)+'% ...',(0,0))
        pygame.display.flip()
        time.sleep(float(time_run/100))
        Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
    elif animation_type == 'bar':
      Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
      for i in range(100):
        Opr.render_rectangle(WHITE, (4*i,50), (100,330))
        pygame.display.flip()
        time.sleep(float(time_run/100))
      for i in range(5):
        Opr.render_rectangle(WHITE, (400,50), (100,330))
        pygame.display.flip()
        time.sleep(0.2)
        Opr.render_image('Assets/Backgrounds/Login_Background_(Test).png',(0,0),resolution)
        pygame.display.flip()
        time.sleep(0.2)
  



  def time():
    '''
    Affiche l'heure
    '''
    Opr.render_text(time.strftime("%Y-%m-%d"),(522,385),BLACK,20)
    Opr.render_text(time.strftime("%H:%M"),(520,355),BLACK,40)
  



  def render_file(file_contents: list, file_name: str = 'File', x: int = 20, y: int =50, espacement_ligne : int = 20):
    '''
    Render le content d'un file
    '''
    if type(file_contents) == list:
      for el in file_contents:
        Opr.render_text(el, (x,y), WHITE,20)
        y += espacement_ligne
    elif type(file_contents) == str and file_contents[len(file_contents)-3:len(file_contents)] in ['pdf','odt','txt']:
      Opr.render_text(file_contents, (x,y))
    elif file_contents[len(file_contents)-3:len(file_contents)] == 'mp3':
      pygame.mixer.music.load('Assets/Directory Files/'+file_contents)
      pygame.mixer.music.play()
    elif file_contents[len(file_contents)-3:len(file_contents)] in ['png','jpg']:
      Opr.render_image(file_contents, (x,y))





  def render_file_tree(file_path: str):
    '''
    Render les dossiers dans un file path
    '''
    i = 50
    files_loaded = files.explore_file(file_path)
    if type(files_loaded) == dict:
      for el in files_loaded:

        #on render le icon
        if el[len(el)-4:len(el)] == '.mp3':
          Opr.render_image('Assets/File Icons/MP3.png',(2,i-5),(22,22))
        elif el[len(el)-4:len(el)] == '.mp4':
          Opr.render_image('Assets/File Icons/MP4.png',(2,i-5),(22,22))
        elif el[len(el)-4:len(el)] == '.exe':
          Opr.render_image('Assets/File Icons/EXE.png',(2,i-5),(22,22))
        elif el[len(el)-4:len(el)] == '.pdf':
          Opr.render_image('Assets/File Icons/PDF.png',(2,i-5),(22,22))
        else:
          Opr.render_image('Assets/Icons/Folder_(Test).png',(2,i-5),(22,22))

        #On render le text
        Opr.render_text(el,(25,i),WHITE,30)

        # On rajoute l'element
        clickable_icons[(2,22,i-5,i-5+22)] = el +'/'

        i+=30
    else:
      Compu.render_file(files_loaded)
    
      


  def render_barre_taches(pos:tuple):
    '''
    Render la bare des taches par rapport a la la fenetre ouverte
    '''
    #Background
    screen.fill(BLUE_GREY)

    #Bar haut de Fenetre
    Opr.render_rectangle(GREY, (600,30), (0,0))
    Opr.render_image('Assets/Icons/Close_(Test).png',(0,0),(30,30))

    #Barre des taches
    Opr.render_rectangle(WHITE, (600,70), (0,350))
    Compu.time()

    #Applications
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))
    Opr.render_rectangle(LIGHT_BLUE, (55,55),pos)
    Opr.render_image('Assets/Icons/Folder_(Test).png',(60,350),(50,50))
    Opr.render_image('Assets/Icons/Platformer_Button_(Test).png',(120,350),(50,50))
  



  def check_icons(clickpos: tuple):
    for wanted_area in clickable_icons.keys():
      if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
        return clickable_icons[wanted_area]


    



Compu = Computer

#tests des extensions
#peut etre utilisé pour le load
def test_ext(time_sleep:int = 1):
  print(plat.test())
  screen.fill(BASE_COLOR)
  Opr.render_text('Tests: This is a Beta Version',(0,0))
  pygame.display.flip()
  time.sleep(0.75)
  Opr.render_text('Built Robot Core',(0,20))
  pygame.display.flip()
  time.sleep(0.75)
  files.explore_file()
  print(files.Files)
  print('File Directory Connected')
  Opr.render_text('Built File Directory',(0,40))
  pygame.display.flip()
  time.sleep(0.75)
  s.load_page('www.test.com')
  Opr.render_text('Connected to Web',(0,60))
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
    user_logged = Compu.log_in()
      
  else:

    #Pour la page HOME
    if page == 'home':

      #Background
      screen.fill(BASE_COLOR)
      Opr.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),resolution)

      #Barre des taches
      Opr.render_rectangle(WHITE, (600,70), (0,350))
      Compu.time()

      #Applications
      Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))
      Opr.render_image('Assets/Icons/Folder_(Test).png',(60,350),(50,50))
      Opr.render_image('Assets/Icons/Platformer_Button_(Test).png',(120,350),(50,50))

    #Pour le FILE Directory
    if page == 'fd0':
      Compu.render_barre_taches((55,350))
      Compu.render_file_tree(fd_dict)
      fd_dict = output
      Compu.render_typing_text((40,9),25)
      open = True
    
    #Platformer
    if page == 'plat':
      plat.play_game()
      


      


  #On check les events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)


        # On render par rapport à la page
        if page == 'fd0':
          check = Compu.check_icons(event.pos)
          if type(check) == str:
            fd_dict += check
            output = fd_dict
            print(fd_dict)






        #Appli file directory
        if Compu.check_interaction(event.pos, (55,110,360,400),['home']) == True:
          page = 'fd0'
          output = 'C:/'



        #Appli home (comme le bouton windows ?)
        elif Compu.check_interaction(event.pos, (0,50,360,400),['home', 'fd0','plat']) == True:
          page = 'home'

        
        #Close button
        elif Compu.check_interaction(event.pos, (0,30,0,30),['fd0','plat']) == True:
          page = 'home'
        
        #Open platformer
        elif Compu.check_interaction(event.pos, (124,163,360,400),['home','fd0']) == True:
          page = 'plat'



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
      

  pygame.display.flip()

pygame.quit()
