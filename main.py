#https://www.pygame.org/docs/
import pygame, time
from ext.Apps import web_search as s
from ext.Apps import file_explorer as files
from ext.Platformer import platformer as plat
from ext.Apps import snake as snk
from ext.Core import operations as Opr
from ext.Core import variables as varia
from ext.Core import sphere as sphere
from ext.Core import scan_unlocks as scan
#Setup de la fenetre pygame
pygame.init()
pygame.mixer.init() # setup de l'extension de fichiers audio

#Taille
screen = pygame.display.set_mode(varia.resolution)

#Nom et icon de notre fenetre
pygame.display.set_caption("Krypt Corp")
logo = pygame.image.load('Assets/Icons/logo.svg')
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

#Variables pour faire marcher la base de notre programme
RUN = True #est ce que la boucle while tourne
user_logged = False #est ce que le joueur est dans l'ordi
output = '' #Le texte type input directement via le clavier
from ext.Core.variables import page, file_dir_path
clickable_icons = {}
plat_check = 0
level = 0
message = varia.messages
#variables specifiques a des sous stages quand il faut ecrire
writing_data = [] 
varia.unlocked = [0, 1000]

#-----------test area--------
varia.popup=2
def dev_use():
  varia.unlocked.append(1010) #bypass steps
  varia.popup +=1
  return True
print(varia.popup)
user_logged = dev_use() #bypass login

#-------end test area---------


##--------------------------------------------------------------------------##
##--------------Calculs et fonctionnement de notre ordinateur---------------##
##--------------------------------------------------------------------------##
  
class Computer:

  def log_in():
    '''
    Méthode qui demande un username et un passcode.
    Les seuls valides pour l'instant son User: User1 et Password: 0000
    '''

    #On demande le 'User'
    open = True
    output = ''
    rY = 0
    while open:
      rY+=.002
      screen.fill((83,130,168))
      sphere.display_matrix_image(sphere.mat, sphere.mat_d, 0, rY, 0, 'Assets/Icons/logo_button.png')
      Opr.render_image('Assets/Icons/secureAccess.png',(0,130), (250,35), True )
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

    #On demande le 'Password'
    open = True
    output = ''
    while open:
      rY +=.002
      screen.fill((83,130,168))
      sphere.display_matrix_image(sphere.mat, sphere.mat_d, 0, rY, 0, 'Assets/Icons/logo_button.png')
      Opr.render_image('Assets/Icons/secureAccess.png',(0,130), (250,35), True )
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
    i = 45
    files_loaded = files.explore_file(file_path)
    if type(files_loaded) == dict:
      for el in files_loaded:
        if el[-4:-3] == '.': #on render le icon d'un fichier
          Opr.render_image(f'Assets/Icons/File Icons/{el[len(el)-3:len(el)].upper()}.png',(2,i-5),(22,22))
        else: # on render le icon d'un folder
          Opr.render_image('Assets/Icons/Folder.png',(2,i),(22,22))
        #On render le text
        Opr.render_text(el,(25,i-3),varia.WHITE,20)
        clickable_icons[(2,22,i,i+22)] = el +'/' # On rajoute l'element
        i+=30 # On itere
    else:
      clickable_icons = {}
      varia.page = Opr.render_file(files_loaded)


  def render_messagerie(messages: dict):
    '''
    Render les dossiers dans un file path
    '''
    global clickable_icons
    i = 50
    for lock in messages:
      for el in messages[lock]:
        #On render le text
        Opr.render_rectangle(varia.GREY, (11*len(el),24), (32, i-2)) #rectangle derriere le titre
        Opr.render_image('Assets/Icons/Messages.png',(0,i-8),(35,35))
        Opr.render_text(el,(32,i-2),varia.WHITE,20)
        clickable_icons[(2,12*len(el),i-3,i-3+22)] = (lock,el) # On rajoute l'element
        i+=30 # On itere


  def render_barre_taches(pos:tuple, app : bool = True):
    '''
    Render la barre des taches par rapport a la la fenetre ouverte
    '''
    if app:
      screen.fill(varia.BLUE_GREY) #Background
    Opr.render_rectangle(varia.WHITE, (600,70), (0,350)) #Rectangle de la barre des taches
    Opr.render_time()
    if app:
      #Bar haut de Fenetre
      Opr.render_rectangle(varia.GREY, (600,30), (0,0))
      Opr.render_image('Assets/Icons/cross.png',(1,1),(27,27))
      #Carré bleu appli en cours
      Opr.render_rectangle(varia.LIGHT_BLUE, (55,55),pos)
    #Applications
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,352),(45,45))
    Opr.render_image('Assets/Icons/Folder.png',(60,350),(50,50))
    Opr.render_image('Assets/Icons/Platformer_Button_(Test).png',(120,350),(50,50))
    Opr.render_image('Assets/Icons/Internet_(Test).png',(180,350),(50,50))
    Opr.render_image('Assets/Icons/Messages.png',(234,350),(50,50))
    if varia.popup != 0:
      Opr.render_circle(varia.RED, 7, (279,362))
      Opr.render_text(str(varia.popup),(276,356),varia.WHITE,10)
      Opr.render_rectangle(varia.BLUE_GREY,(110,34),(491,316))
      Opr.render_text('Nouveaux mail', (495,325), varia.WHITE,15)
      Opr.render_rectangle(varia.BLACK,(350,1),(490,315))
      Opr.render_rectangle(varia.BLACK,(1,35),(490,315))
      pygame.display.flip()     



  def check_icons(clickpos: tuple):
    for wanted_area in clickable_icons.keys():
      if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
        return clickable_icons[wanted_area] # On renvoit le content correspondant à la zone

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
#test_ext()


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
    scan.update_messagerie() #on update par rapport aux unlocks
    if 110 in varia.unlocked and not 'D:' in files.Files.keys():
      files.Files = dict(files.Files,**varia.recovered_drive)
      print(files.Files)
    #HOME
    elif page == 'home':
      Opr.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),varia.resolution) # On render le background
      Compu.render_barre_taches((55,350), False) #On render la barre des taches
      pygame.display.flip() #on display le tout

    #FILE Directory
    elif page == 'fd0':
      Compu.render_barre_taches((55,350)) #On render la barre des taches
      Compu.render_file_tree(file_dir_path) #on render les files/dossiers par rapport au chemin
      file_dir_path = output # on synchronise le texte tapé avec le chemin
      Opr.render_text(output, (70,4),varia.WHITE, 17) # on render le texte qui est tapé
      Opr.render_image('Assets/Icons/arrow_ul.png', (30,0), (27,27)) # on render le bouton back
      open = True # on permet de taper au clavier
      pygame.display.flip() #on display le tout
    
    elif page == 'web':
      Compu.render_barre_taches((177,350))
      # Opr.render_rectangle_borders(varia.BLACK, (66,1), (-66,29))
      # Opr.render_rectangle_relative(varia.BLACK, (70,5), (-70, 20))
      Opr.div(top=5,height=20,left="10vw",width="80vw", padding=5, border=(0,0,0))
      Opr.render_text(output, (70,4),varia.WHITE, 17)
      if not(open): #Si l'utilisateur ne tape plus
        s.load_page(output) # on load la page
      pygame.display.flip()

    #Snake game link
    elif page == 'snake':
      page = snk.game()
    
    #Platformer
    elif page == 'plat': # si la page est celle du platformer
      if type(plat_check) == str: #si le platformer renvoit le fait que il revient a un page de l'ordi
        page = plat_check # on va a cette page
      else:
        plat_check = plat.play_game(plat_check) # on check par rapport à ce que la fonction retourne
        if type(plat_check) == int: # si la fonction retourne un chiffre
          level = plat_check #on synchronise avec le level

    elif page == 'messages':
      if 0 in varia.unlocked: # si on a unlock la boite mail
        Compu.render_barre_taches((232,350))
        if type(message) == dict: #si on est dans la boite de reception
          message = varia.messages
          Compu.render_messagerie(message)
        elif message == 'New message':
          clickable_icons = {} #on clear les clickables icons 
          #rectangle destinataire
          Opr.render_rectangle_borders(varia.BLACK, (66,50), (-66,29))
          Opr.render_rectangle_relative(varia.GREY, (70,54), (-70, 21))
          Opr.render_text("Destinataire:"+writing_data[1],(72,52),varia.BLACK,18) #texte destinataire

          #rectangle object du mail
          Opr.render_rectangle_borders(varia.BLACK, (66,88), (-66,28))
          Opr.render_rectangle_relative(varia.GREY, (70,92), (-70, 20))
          Opr.render_text("Objet:"+writing_data[2],(72,90),varia.BLACK,18)

          #rectangle du contenu du mail
          Opr.render_rectangle_borders(varia.BLACK, (66,126), (-66,200))
          Opr.render_rectangle_relative(varia.GREY, (74,134), (-74, 184))
          Opr.render_text("Mail:"+writing_data[3],(76,132),varia.BLACK,18)
          #bouton send mail
          Opr.render_image('Assets/Icons/send-mail-replit.jpg', (90,0), (27,27))
          #lien entre input et les differentes parties du mail.
          if writing_data[0] == 'dest':
            writing_data[1] = output #on fait le lien entre le destinataire sauvegardé et ce qu'on ecrit
          elif writing_data[0] == 'topic':
            writing_data[2] = output #on fait le lien entre le sujet sauvegardé et ce qu'on ecrit
          elif writing_data[0] == 'content':
            writing_data[3] = output #on fait le lien entre le texte sauvegardé et ce qu'on ecrit
          if writing_data[4] == 'vide':
            Opr.render_text("Vous devez remplir le destinataire, l'objet et le contenu du mail", (130,2), varia.WHITE, 15)
          if writing_data[4] == 'casedestinatairevide':
            Opr.render_text('Vous devez préciser un destinataire pour envoyer ce mail', (130,2))
          if writing_data[4] == 'caseobjetvide':
            Opr.render_text('Vous devez préciser un objet pour envoyer ce mail', (130,2))
          if writing_data[4] == 'casemailvide':
            Opr.render_text('Vous devez écrire du contenu dans le mail pour envoyer ce mail', (130,2))
          
        else:
          Opr.render_file(message) #sinon on render l'email
        Opr.render_image('Assets/Icons/arrow_ul.png', (30,0), (27,27))
        Opr.render_image('Assets/Icons/pensil-replit.jpg', (60,0), (27,27))
        pygame.display.flip()
      else:
        Compu.render_barre_taches((232,350))
        Opr.render_text('Acces Sécurisé !', (varia.resolution[0]/2, varia.resolution[1]/2)) 

  #On check les events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)

        if Opr.check_interaction(event.pos, (55,110,360,400), ['home','web','messages'], page) == True:
          clickable_icons = {} #on reset les clickable icons 
          page = 'fd0'
          output = ''

        #Appli home
        elif Opr.check_interaction(event.pos, (0,50,360,400), ['home', 'fd0','web','messages'], page) == True:
          page = 'home'
          clickable_icons = {} #on reset les clickable icons 
        
        #Bouton close
        elif Opr.check_interaction(event.pos, (0,30,0,30), ['fd0','web','messages'], page) == True:
          page = 'home'
          clickable_icons = {} #on reset les clickable icons         
        
        #Acces au robot
        elif Opr.check_interaction(event.pos, (124,163,355,400), ['home','fd0','web','messages'], page) == True:
          plat_check = level
          page = 'plat'
        
        #Internet explorer
        elif Opr.check_interaction(event.pos, (184,230,360,400), ['home','fd0','messages'], page) == True:
          clickable_icons = {} #on reset les clickable icons 
          page = 'web'
          output=''
          open=False

        #Messagerie
        elif Opr.check_interaction(event.pos, (230,290,360,400), ['home','fd0','web'], page) == True:
          clickable_icons = {} #on reset les clickable icons 
          page = 'messages'
          output = ''
          varia.popup = 0
          
        
        #URL
        elif Opr.check_interaction(event.pos, (66,600,1,28), ['web'], page) == True:
          open=True

        #Regarde si on clique sur la notification d'un mail
        elif Opr.check_interaction(event.pos,(490,600,320,350), ['home','fd0','web','plat',],page) == True:
          varia.popup=0
          page = 'messages'
          
        # Ouvrir des messages
        elif page == 'messages':
          check = Compu.check_icons(event.pos)
          if type(check) == tuple:
            message = varia.messages[check[0]][check[1]] #Si on click un mail on l'ouvre
          if Opr.check_interaction(event.pos, (30,60,0,30), ['messages'], page) == True:
            message = varia.messages
            varia.popup = 0 #Si bouton back on revient a la boite mail

          #bouton écrire un mail  
          elif Opr.check_interaction(event.pos, (60,87,0,27), ['messages'], page) == True:
            message = 'New message'
            output = '' #reset output
            writing_data = ['dest', '','','','']
            clickable_icons = {}
            open=True

          #bouton pour envoyer un mail
          elif Opr.check_interaction(event.pos, (90,117,0,27), ['messages'], page) == True and message == 'New message':
            
            #check si les contenus du mail ne sont pas vide
            if writing_data[1] and writing_data[2] and writing_data[3]:
              writing_data[4] = '!vide'
              print(scan.check_message(writing_data))
              varia.unlocked.append(scan.check_message(writing_data))
            elif writing_data[1]=='' and writing_data[2]=='' and writing_data[3]=='':
              writing_data[4] = 'vide'
            elif writing_data[1]=='' :
              writing_data[4] = 'casedestinatairevide'
            elif writing_data[2]=='':
              writing_data[4] = 'caseobjetvide'
            elif writing_data[3]=='':
              writing_data[4] = 'casemailvide'
              
          #Si click la boîte destinataire
          elif Opr.check_interaction(event.pos, (66,598,51,77), ['messages'], page) == True and message == 'New message':
            writing_data[0] = 'dest' # la writing stage est celle du destinataire
            output = writing_data[1]
            open = True # on autorise a faire le lien clavier - pygame
          
          #Si click la boite sujet
          elif Opr.check_interaction(event.pos, (66,598,89,115), ['messages'], page) == True and message == 'New message':
            writing_data[0] = 'topic'
            output = writing_data[2]
            open = True # on autorise a faire le lien clavier - pygame
          
          #Si click la boite corps du mail
          elif Opr.check_interaction(event.pos, (74,598,134,326), ['messages'], page) == True and message == 'New message':
            writing_data[0] = 'content'
            output = writing_data[3]
            open = True # on autorise a faire le lien clavier - pygame

        elif page == 'fd0':
          if Opr.check_interaction(event.pos, (30,60,0,30), ['fd0'], page) == True: #Back button
            clickable_icons = {} #reset les icons clickables
            file_dir_path = file_dir_path[:-1]
            for c in reversed(file_dir_path):
              if c == '/':
                output = file_dir_path
                break
              else:
                file_dir_path = file_dir_path[:-1]

          check = Compu.check_icons(event.pos) # Icons
          if type(check) == str:
            clickable_icons = {} #reset les icons clickables
            file_dir_path += check # ajoute le fichier clické
            output = file_dir_path # fait le lien avec le clavier

    #Si le clavier est utilisé
    if event.type == pygame.KEYDOWN:

      #Lien entre le clavier et le script sans utiliser input
      if open:
        if event.key == pygame.K_RETURN:
          open = False
        elif event.key == pygame.K_BACKSPACE:
          output =  output[:-1] #on enleve le dernier character
        else:
          output += event.unicode # on ajoute le character au output
      else:
        if event.key == pygame.K_RETURN: # Si on ne peux pas ecrire et la touche est enter
          open = True # on peut ecrire
  pygame.display.flip()
  clock.tick(60)

pygame.quit()