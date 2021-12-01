#https://www.pygame.org/docs/
import pygame ,time
import ext.Alt.web_search as s
import ext.Core.platformer as plat
import ext.Core.file_explorer as files
import ext.Core.operations as Opr
import ext.Alt.snake as snk
import ext.Core.variables as varia
#Setup de la fenetre pygame
pygame.init()
pygame.mixer.init()

#Taille
screen = pygame.display.set_mode(varia.resolution)

#Nom et icon de notre fenetre
pygame.display.set_caption("Krypt Corp")
logo = pygame.image.load('Assets/Icons/Icon_(Test).png')
pygame.display.set_icon(logo)

#Variables pour faire marcher la base de notre programme
RUN = True
user_logged = False
output = ''
page = 'home'
pop_up = None
file_dir_path = 'C:/'
clickable_icons = {}
plat_check = 0
level = 0

##--------------------------------------------------------------------------##
##--------------Calculs et fonctionnement de notre ordinateur---------------##
##--------------------------------------------------------------------------##
  
class Computer:
  
  def render_pop_up(pop_up:str, pos:tuple):
    print(pop_up)

  def log_in():
    '''
    Fonction qui demande un username et un passcode.
    Les seuls valides pour l'instant son User: User1 et Password: 0000
    '''

    #On demande le user
    open = True
    output = ''
    while open:
      screen.fill(varia.BASE_COLOR)
      Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
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
      screen.fill(varia.BASE_COLOR)
      Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
      Opr.render_text('User: '+user, (50,50))
      Opr.render_text('Password: '+len(output)*'*', (50,70))
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
      Opr.render_text('Acces Denied!', (50,100), varia.RED)
      pygame.display.flip()
      time.sleep(3)
      return False

  def render_typing_text(pos:tuple, size:int = 30):
    '''
    Fonction qui permet d'afficher du texte qui est tapé et qui interagit avec le programme sans utiliser input().
    Prend en argument le texte (str) et sa position (tuple)
    '''
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(output, False, (255, 255, 255))
    screen.blit(text,pos)


  def loading(animation_type: str,time_run: int):
    '''
    Fonction qui fait une animation de load. Type d'animation et temps de l'animation a spécifier
    '''
    if animation_type == 'text':
      Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
      for i in range(100):
        Opr.render_text('Loading '+str(i)+'% ...',(0,0))
        pygame.display.flip()
        time.sleep(float(time_run/100))
        Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
    elif animation_type == 'bar':
      Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
      for i in range(100):
        Opr.render_rectangle(varia.WHITE, (4*i,50), (100,330))
        pygame.display.flip()
        time.sleep(float(time_run/100))
      for i in range(5):
        Opr.render_rectangle(varia.WHITE, (400,50), (100,330))
        pygame.display.flip()
        time.sleep(0.2)
        Opr.render_image(varia.Login_Background,(0,0),varia.resolution)
        pygame.display.flip()
        time.sleep(0.2)


  def render_file_tree(file_path: str):
    '''
    Render les dossiers dans un file path
    '''
    global clickable_icons
    i = 50
    files_loaded = files.explore_file(file_path)
    if type(files_loaded) == dict:
      for el in files_loaded:
        if el[-4:-3] == '.': #on render le icon d'un fichier
          Opr.render_image(f'Assets/Icons/File Icons/{el[len(el)-3:len(el)].upper()}.png',(2,i-5),(22,22))
        else: # on render le icon d'un folder
          Opr.render_image('Assets/Icons/Folder_(Test).png',(2,i-5),(22,22))
        #On render le text
        Opr.render_text(el,(25,i),varia.WHITE,30)
        # On rajoute l'element
        clickable_icons[(2,22,i-5,i-5+22)] = el +'/'
        # On itere
        i+=30
    else:
      clickable_icons = {}
      Opr.render_file(files_loaded)


  def render_barre_taches(pos:tuple, app : bool = True):
    '''
    Render la barre des taches par rapport a la la fenetre ouverte
    '''
    #Background
    if app:
      screen.fill(varia.BLUE_GREY)
    #Barre des taches
    Opr.render_rectangle(varia.WHITE, (600,70), (0,350))
    Opr.render_time()
    if app:
      #Bar haut de Fenetre
      Opr.render_rectangle(varia.GREY, (600,30), (0,0))
      Opr.render_image('Assets/Icons/Close_(Test).png',(0,0),(30,30))
      #Carré bleu appli en cours
      Opr.render_rectangle(varia.LIGHT_BLUE, (55,55),pos)
    #Applications
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,352),(45,45))
    Opr.render_image('Assets/Icons/Folder_(Test).png',(60,350),(50,50))
    Opr.render_image('Assets/Icons/Platformer_Button_(Test).png',(120,350),(50,50))
    Opr.render_image('Assets/Icons/Internet_(Test).png',(180,350),(50,50))


  def check_icons(clickpos: tuple):
    for wanted_area in clickable_icons.keys():
      if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
        return clickable_icons[wanted_area]

Compu = Computer

def test_ext(time_sleep:int = 0.5):#tests des extensions
  print(plat.test())
  screen.fill(varia.BASE_COLOR)
  Opr.render_text('Tests: This is v0.2.1',(0,0))
  pygame.display.flip()
  time.sleep(0.25)
  Opr.render_text('Built Robot Core',(0,20))
  pygame.display.flip()
  time.sleep(0.25)
  files.explore_file()
  print(files.Files)
  Opr.render_text('Built File Directory',(0,40))
  pygame.display.flip()
  time.sleep(0.25)
  s.load_page('www.test.com')
  Opr.render_text('Connected to Web',(0,60))
  pygame.display.flip()
  time.sleep(0.25)
  Opr.render_text(snk.test(), (0,80))
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
    #user_logged = Compu.log_in()
    user_logged = True
      
  else:

    #HOME
    if page == 'home':
      Opr.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),varia.resolution)
      Compu.render_barre_taches((55,350), False)
      pygame.display.flip()

    #FILE Directory
    if page == 'fd0':
      Compu.render_barre_taches((55,350))
      Compu.render_file_tree(file_dir_path)
      file_dir_path = output
      Compu.render_typing_text((70,9),25)
      Opr.render_image('Assets/Icons/Back.png', (30,0), (30,30))
      open = True
      pygame.display.flip()
    
    if page == 'web':
      Compu.render_barre_taches((177,350))
      Opr.render_text('In construction', (200,300))
      pygame.display.flip()

    #Platformer
    if page == 'plat':
      if type(plat_check) == str:
        page = plat_check
      else:
        plat_check = plat.play_game(plat_check)
        if type(plat_check) == int:
          level = plat_check

  #On check les events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)

        if Opr.check_interaction(event.pos, (55,110,360,400), ['home','web'], page) == True:
          page = 'fd0'
          output = 'C:/'

        #Appli home (comme le bouton windows ?)
        elif Opr.check_interaction(event.pos, (0,50,360,400), ['home', 'fd0','web'], page) == True:
          page = 'home'
        
        #Close button
        elif Opr.check_interaction(event.pos, (0,30,0,30), ['fd0','web'], page) == True:
          page = 'home'            
        
        #Open platformer
        elif Opr.check_interaction(event.pos, (124,163,355,400), ['home','fd0','web'], page) == True:
          plat_check = level
          page = 'plat'
        
        elif Opr.check_interaction(event.pos, (184,223,360,400), ['home','fd0'], page) == True:
          page = 'web'

        #Back button
        if page == 'fd0':
          if Opr.check_interaction(event.pos, (30,60,0,30), ['fd0'], page) == True:
            file_dir_path = file_dir_path[:-1]
            for c in reversed(file_dir_path):
              if c == '/':
                output = file_dir_path
                break
              else:
                file_dir_path = file_dir_path[:-1]

          check = Compu.check_icons(event.pos)
          if type(check) == str:
            file_dir_path += check
            output = file_dir_path

    #Si le clavier est utilisé
    if event.type == pygame.KEYDOWN:

      #Lien entre le clavier et le script sans utiliser input
      if open:
        if event.key == pygame.K_RETURN:
          open = False
        if event.key == pygame.K_BACKSPACE:
          output =  output[:-1]
        else:
          output += event.unicode

  pygame.display.flip()

pygame.quit()