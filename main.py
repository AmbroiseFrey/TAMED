#https://www.pygame.org/docs/
import pygame, time
from ext.Apps import web_search as s
from ext.Apps import file_explorer as files
from ext.Platformer import platformer as plat
from ext.Apps import snake as snk
from ext.Core import variables as varia
from ext.Core import operations as Opr
from ext.Core import sphere as sphere
from ext.Core import scan_unlocks as scan
from ext.Core.variables import file_dir_path
#Setup de la fenetre pygame
pygame.init()
pygame.mixer.init() # setup de l'extension de fichiers audio


#Variables pour faire marcher la base de notre programme
RUN = True #est-ce que la boucle while tourne
user_logged = False #est-ce que le joueur est dans l'ordi
output = '' #Le texte type input directement via le clavier
clickable_icons = {}
plat_check = 0 #variable qui permet de faire le lien platformer - ordinateur
level = 0 # ⚠️ variable possiblement obsolete
message = varia.messages
#variables spécifiques a des sous stages quand il faut écrire
email_data = []
web_data = []
varia.unlocked = [0, 0.1, 1000]
clavier_open = False

#-----------test area--------
def dev_use():
  '''
  Bypass du login
  '''
  varia.unlocked.append(1010) #bypass steps
  # varia.resolution = (600,400) # resolution de devellopement
  return True

user_logged = dev_use() #bypass login

#-------end test area---------


#Taille
screen = pygame.display.set_mode(varia.resolution) #pygame.NOFRAME - sans bordure

#Nom et icon de notre fenetre
pygame.display.set_caption("Krypt Corp")
logo = pygame.image.load('Assets/Icons/logo.png')
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

res0,res1 = tuple(i/100 for i in varia.resolution)#variables qui seront utilisées pour positionner et dimensionner les rectangles/images/etc. en fonction de la taille de l'écran

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
    clavier_open = True
    output = ''
    rY = 0
    while clavier_open:
      rY+=.002
      screen.fill((83,130,168))
      sphere.display_matrix_image(sphere.mat, sphere.mat_d, 0, rY, 0, 'Assets/Icons/Logo_Sphere.png')
      Opr.render_image('Assets/Icons/secureAccess.png',(0,130), (varia.resolution[0]/2,8.75*res1), True )
      Opr.render_text('User: '+output, (8.33*res0,12.5*res1))
      Opr.render_text('Password: ', (8.33*res0,17.5*res1))
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #si on presse une touche
          if event.key == pygame.K_RETURN: # on revient à la ligne
            user = output
            clavier_open = False
          elif event.key == pygame.K_BACKSPACE: #on delete
            output =  output[:-1]
          else:
            output += event.unicode # on ajoute le character

    #On demande le 'Password'
    clavier_open = True
    output = ''
    while clavier_open:
      rY +=.002
      screen.fill((83,130,168))
      sphere.display_matrix_image(sphere.mat, sphere.mat_d, 0, rY, 0, 'Assets/Icons/Logo_Sphere.png')
      Opr.render_image('Assets/Icons/secureAccess.png',(0,130), (varia.resolution[0]/2,8.75*res1), True )
      Opr.render_text('User: '+user, (8.33*res0,12.5*res1))
      Opr.render_text('Password: '+len(output)*'*', (8.33*res0,17.5*res1))
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #si on presse une touche
          if event.key == pygame.K_RETURN:# on revient à la ligne
            password = output
            clavier_open = False
          elif event.key == pygame.K_BACKSPACE: #on delete
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
        Opr.render_rectangle(varia.WHITE, (0.66*res0*i,12.5*res1), (16.66*res0,82.5*res1))
        pygame.display.flip()
        time.sleep(float(time_run/100))
      for i in range(5):
        Opr.render_rectangle(varia.WHITE, (66.66*res0,12.5*res1), (16.66*res0,82.5*res1))
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
    i = int(11.25*res1)
    files_loaded = files.explore_file(file_path)
    if type(files_loaded) == dict:
      for el in files_loaded:
        if el[-4:-3] == '.': #on render le icon d'un fichier
          Opr.render_image(f'Assets/Icons/File Icons/{el[len(el)-3:len(el)].upper()}.png',(0.33*res0,i-1.25*res1),(5.5*res1,5.5*res1))
        else: # on render le icon d'un folder
          Opr.render_image('Assets/Icons/App Icons/Folder.png',(0.33*res0,i),(5.5*res1, 5.5*res1))
        #On render le text
        Opr.render_text(el,(4.167*res0,i-0.6*res1),varia.WHITE,5*res1)
        clickable_icons[(0.33*res0,3.66*res0,i,i+5.5*res1)] = el +'/' # On rajoute l'elemnt pour qu'il soit clickable
        i+=int(7.5*res1)
    else:
      clickable_icons = {}
      varia.page = Opr.render_file(files_loaded)


  def render_messagerie(messages: dict):
    '''
    Render les dossiers dans un file path
    '''
    global clickable_icons
    i = 12.5*res1
    for lock in messages:
      for el in messages[lock]:
        #On render le text
        Opr.render_rectangle(varia.GREY, (1.83*res0*len(el),6*res1), (6*res0, i-(0.5*res1))) #rectangle derriere le titre
        Opr.render_image('Assets/Icons/App Icons/Messages.png',(0,i-(2*res1)),(8.75*res1,8.75*res1))
        Opr.render_text(el,(6*res0,i-(0.5*res1)),varia.WHITE,int(5*res1))
        # clickable_icons[(2,12*len(el),i-3,i-3+22)] = (lock,el) # On rajoute l'element
        clickable_icons[(0.33*res0,2*res0*len(el), i, i+4.5*res1)] = (lock,el) # On rajoute l'element
        i+=7.5*res1 # On itere
      


  def render_barre_taches(pos:tuple, app : bool = True):
    '''
    Render la barre des taches par rapport a la la fenetre ouverte
    '''
    if app:
      screen.fill(varia.BLUE_GREY) #Background
      #Bar haut de Fenetre
      Opr.render_rectangle(varia.GREY, (varia.resolution[0],7.5*res1), (0,0))
      Opr.render_image('Assets/Icons/cross.png',(0.16*res0,(7.5*res1-6.75*res1)/2),(6.75*res1,6.75*res1))
      #Carré bleu appli en cours
      Opr.render_rectangle(varia.LIGHT_BLUE, (55,55),pos)
    Opr.render_rectangle(varia.WHITE, (varia.resolution[0],12.5*res1), (0,87.5*res1)) #Rectangle de la barre des taches
    Opr.render_time()
    #Applications
    Opr.render_image('Assets/Icons/App Icons/Home_Button.png',(0,88*res1),(11.25*res1,11.25*res1))
    Opr.render_image('Assets/Icons/App Icons/Folder.png',(10*res0,87.5*res1),(12.5*res1,12.5*res1))
    Opr.render_image('Assets/Icons/App Icons/Platformer_Button.png',(20*res0,87.5*res1),(12.5*res1,12.5*res1))
    Opr.render_image('Assets/Icons/App Icons/Internet.png',(30*res0,87.5*res1),(12.5*res1,12.5*res1))
    Opr.render_image('Assets/Icons/App Icons/Messages.png',(39*res0,87.5*res1),(12.5*res1,12.5*res1))
    Opr.render_image('Assets/Icons/App Icons/Notes.png',(49*res0,87.5*res1),(12.5*res1,12.5*res1))
    if varia.popup != 0:
      Opr.render_circle(varia.RED, 1.75*res1, (46.5*res0,90.5*res1))
      Opr.render_text(str(varia.popup),(46.1*res0,89*res1),varia.WHITE,int(2.5*res1))


  def check_icons(clickpos: tuple):
    '''
    On check par rapport a la position de la souris quand on click (clickpos), si cette position correspond à une zone avec la quelle l'utilisateur peut intéragir
    '''
    for wanted_area in clickable_icons.keys():
      if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
        return clickable_icons[wanted_area] # On renvoit le content correspondant à la zone

Compu = Computer

ctrlKeyPressed = False


##------------------------------##
##---Boucle Principale du Jeu---##
##------------------------------##

while RUN:
  #Parametres keys
  keys = pygame.key.get_pressed()
  #Parametres de notre souris
  click = pygame.mouse.get_pressed()[0]
  pos = pygame.mouse.get_pos()
  x = pos[0]
  y = pos[1]

  if not(user_logged):
    user_logged = Compu.log_in()
      
  else:
    scan.update_messagerie() #on update par rapport aux unlocks
    if not 'D:' in files.Files.keys() and 1010 in varia.unlocked:
      files.Files = dict(files.Files,**varia.recovered_drive)
      print(files.Files)
    #HOME
    elif varia.page == 'home':
      #Opr.render_image('Assets/Backgrounds/Background_(Test).jpg',(0,0),varia.resolution) # On render le background
      Opr.render_image("Assets/Backgrounds/Mars-Wallapaper.jpg",(0,0),varia.resolution)
      Compu.render_barre_taches((55,350), False) #On render la barre des taches
      pygame.display.flip() #on display

    #FILE Directory
    elif varia.page == 'fd0':
      Compu.render_barre_taches((10*res0,87.5*res1)) #On render la barre des taches
      Compu.render_file_tree(file_dir_path) #on render les files/dossiers par rapport au chemin
      file_dir_path = output # on synchronise le texte tapé avec le chemin
      Opr.render_text(output, (11.66*res0,res1),varia.WHITE, 4*res1) # on render le texte qui est tapé
      Opr.render_image('Assets/Icons/arrow_ul.png', (5*res0,(7.5*res1-6.75*res1)/2), (6.75*res1,6.75*res1)) # on render le bouton back
      clavier_open = True # on permet de taper au clavier
      pygame.display.flip() #on display
    
    #Navigateur Internet
    elif varia.page == 'web': #on regarde si on est dans l'application web(le navigateur)
      Compu.render_barre_taches((30*res0,87.5*res1))#on affiche la bare des taches
      Opr.div(top=1.25*res1,height=5*res1,left="10vw",width="80vw", padding=5, border=(0,0,0)) #on affiche le rectangle pour saisir l'url, avec un rectangle en coordonné relative
      Opr.render_text(varia.sub_page, (11.66*res0,res1),varia.WHITE, round(4.25*res1))#permet d'afficher l'url tapé par l'utilisateur dans le rectangle du dessus
      if clavier_open == False and output != '' and varia.sub_page.startswith('www'): #Si l'utilisateur ne tape plus
        s.load_page(output) # on load la page
        output = ''
        web_data = ['','']
      elif clavier_open == True:
        varia.sub_page = output


      if varia.sub_page == 'binaire.it':#c'est ce qu'on affiche quand on va sur le site www.binaire.it. Site web non terminé
        Opr.div(top='40vh',height=15,left='7vw',width="35vw", padding=2, border=(0,0,0)) #on affiche un rectangle
        Opr.div(top='40vh',height=15,left="58vw",width="35vw", padding=2, border=(0,0,0)) #on affiche un rectangle
        Opr.render_text(output,(8*res0,43*res1),varia.WHITE,round(2*res1))
        if len(output)%8 == 0 and output != '': # si il y a un ou plusieurs octets
          web_data[0] = Opr.ConvertDecimaltoText(output)
          web_data[1] = Opr.ConvertBinarytoDecimal(int(output))
        Opr.render_text(web_data[0],(8*res0,52*res1),varia.WHITE,round(2*res1))
        Opr.render_text(str(web_data[1]),(8*res0,62*res1),varia.WHITE,round(2*res1))
      pygame.display.flip() #on display
        
    #Si le fichier snake.py est ouvert (snake.py etant dans le jeu et se trouvant dans le file directory: C:Program Files)
    elif varia.page == 'snake': 
      snk.loop() #lance le snake game
      varia.page = 'fd0' #quand le snake game est terminé on revient dans le file directory
      file_dir_path = 'C:/Program Files/' #on revient ici
      output = 'C:/Program Files/' #on affiche en haut là où on est dans les fichiers
    
    #Platformer
    elif varia.page == 'plat': # si la page est celle du platformer
      if type(plat_check) == str: #si le platformer renvoit le fait que il revient a un varia.page de l'ordi
        varia.page = plat_check # on va a cette page
        file_dir_path = 'C:/' #on reset le file dir au cas ou c'est un acces par le fichier exe
        plat_check = 0
      else:
        plat_check = plat.play_game(plat_check) # on check par rapport à ce que la fonction retourne
        if type(plat_check) == int: # si la fonction retourne un chiffre
          level = plat_check #on synchronise avec le level

    #Messagerie
    elif varia.page == 'messages':
      if 0 in varia.unlocked: # si on a unlock la boite mail
        Compu.render_barre_taches((39*res0,87.5*res1)) #on affiche la bare des taches
        if type(message) == dict: #si on est dans la boite de reception
          message = varia.messages #on initialise les messages d'après les messages que l'on a unlock
          Compu.render_messagerie(message)
        elif message == 'New message': #quand on est dans la page pour ecrire un mail
          clickable_icons = {} #on clear les clickables icons 
          #rectangle destinataire
          Opr.div(varia.GREY, height='5.25vh', left='11.66vw', width="76.68vw", top=13.5*res1, border=(0,0,0), padding=4) #on render le padding qui constitue l'espace du texte
          Opr.render_text("Destinataire: "+email_data[1],(12*res0,13*res1),varia.BLACK,int(4.5*res1)) # texte destinataire ecrit par l'utilisateur

          #rectangle object du mail
          Opr.div(varia.GREY, height=5*res1, left=11.66*res0, width="76.68vw", top=23*res1, border=(0,0,0), padding=4)
          Opr.render_text("Objet: "+email_data[2],(12*res0,22.5*res1),varia.BLACK,int(4.5*res1)) #texte de l'objet du mail ecrit par l'utilisateur

          #rectangle du contenu du mail
          Opr.div(varia.GREY, height=46*res1, left=11.66*res0, width="76.68vw", top=33.5*res1, border=(0,0,0), padding=4)
          # Opr.render_text("Mail:"+email_data[3],(76,132),varia.BLACK,18)
          Opr.render_text("Mail: ",(12.66*res0,33*res1),varia.BLACK,4.5*res1) #on affiche ce que l'utilisateur ecrit dans le contenu du mail
          t=Opr.textarea(email_data[3], ("76vw",40*res1), (12.33*res0,39.5*res1), varia.GREY, font_size=int(3.75*res1))
          #bouton send mail
          Opr.render_image('Assets/Icons/send-mail-replit.jpg', (15*res0,(7.5*res1-6.75*res1)/2), (6.75*res1,6.75*res1))
          #lien entre input et les differentes parties du mail.
          if email_data[0] == 'dest':
            email_data[1] = output #on fait le lien entre le destinataire sauvegardé et ce qu'on ecrit
          elif email_data[0] == 'topic':
            email_data[2] = output #on fait le lien entre le sujet sauvegardé et ce qu'on ecrit
          elif email_data[0] == 'content':
            if len(output)<len(t):
              #soit on a enlevé du texte ou on a fait un saut a la ligne
              if len(Opr.textData_str(output,' '))<len(Opr.textData_str(t,' ')):
                email_data[3] = output #on initialise le crops du texte au texte tappé
              else:
                email_data[3]=t # ou alors on prend le corps du texte formaté en plusieurs lignes
                output=t # on initialise le texte tapé au corps de texte
            else:  
              email_data[3] = output
            #on fait le lien entre le texte sauvegardé et ce qu'on ecrit

          #Si on a essayé d'envoyer un mail mais il ya des parties vides
          elif email_data[4] == 'vide':
            Opr.render_text("Vous devez remplir le destinataire, l'objet et le contenu du mail", (21.66*res0,0.5*res1), varia.WHITE, int(3.75*res1)) #si le mail est complétement vide lors de l'envoi du mail
          elif email_data[4] == 'casedestinatairevide':
            Opr.render_text('Vous devez préciser un destinataire pour envoyer ce mail', (21.66*res0,0.5*res1), varia.WHITE, int(3.75*res1)) #si pas de destinataire
          elif email_data[4] == 'caseobjetvide':
            Opr.render_text('Vous devez préciser un objet pour envoyer ce mail', (21.66*res0,0.5*res1), varia.WHITE, int(3.75*res1)) #objet
          elif email_data[4] == 'casemailvide':
            Opr.render_text('Vous devez écrire du contenu dans le mail pour envoyer ce mail', (21.66*res0,0.5*res1), varia.WHITE, int(3.75*res1))#contenu du mail
          
        else:
          Opr.render_file(message) #sinon on affiche l'email
        Opr.render_image('Assets/Icons/arrow_ul.png', (5*res0,(7.5*res1-6.75*res1)/2), (6.75*res1,6.75*res1)) #on affiche le bouton back
        Opr.render_image('Assets/Icons/pensil-replit.jpg', (10*res0,(7.5*res1-6.75*res1)/2), (6.75*res1,6.75*res1)) #on affiche le bouton pour ecrire un mail
        pygame.display.flip() #on display
      else:
        Compu.render_barre_taches((232,350)) #affiche bare tache
        Opr.render_text('Acces Sécurisé !', (varia.resolution[0]/2, varia.resolution[1]/2)) #si on a pas encore debloqué les mail on affiche que c'est un accès securisé
    
    #Notes
    elif varia.page == 'notes':
      Compu.render_barre_taches((49*res0,87.5*res1)) # affiche barre taches
      Opr.div(top=12.5*res1,height="70vh",left=20,width="100vw-40", padding=5, border=(0,0,0)) #zone de saisie
      for i in range(len(varia.notes[1])): # pour chaque element dans les notes
        varia.notes[1][varia.notes[0]] = varia.notes[1][varia.notes[0]] #on coordonnes les variables pour eviter les bugs
        Opr.render_text(varia.notes[1][i], (6.66*res0, 12.5*res1+i*4*res1), varia.WHITE, 4*res1) #on affiche chaque note
        clickable_icons[(6.66*res0, 600 ,12.5*res1+i*4*res1, 12.5*res1+i*4*res1 + 22)] = i # on rajoute chaque ligne pour qu'on puisse clicquer sur la ligne pour la modifer

      varia.notes[1][varia.notes[0]] += output #On ajoute le texte tapé au texte des notes
      output = ''

    

  ###----------------------------------------------------------###
  ###------Ici on check toutes les interactions possibles-------###
  ###----------------------------------------------------------###
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Si la souris est pressée
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        print(event.pos)

        if Opr.check_interaction(event.pos, (9.15*res0,18.35*res0,90*res1,varia.resolution[1]), ['home','web','messages','notes'], varia.page) == True: #si l'on click sur la zone de l'app des files
          clickable_icons = {} #on reset les clickable icons 
          varia.page = 'fd0' # on change la 'page'
          output = ''

        #Appli home
        elif Opr.check_interaction(event.pos, (0,8.35*res0,90*res1,varia.resolution[1]), ['home', 'fd0','web','messages','notes'], varia.page) == True: #si on click sur la zone home(en bas à gauche)
          varia.page = 'home' #on change la variable page pour afficher le bureau
          clickable_icons = {} #on reset les clickable icons 
        
        #Bouton close
        elif Opr.check_interaction(event.pos, (0,7.5*res1,0,7.5*res1), ['fd0','web','messages','notes'], varia.page) == True: #si on appuie sur la croix
          varia.page = 'home' #on change la variable page pour afficher le bureau
          clickable_icons = {} #on reset les clickable icons         
        
        #Accès au robot
        elif Opr.check_interaction(event.pos, (20.66*res0,27.16*res0,88.75*res1,varia.resolution[1]), ['home','fd0','web','messages','notes'], varia.page) == True: #si on click sur la zone pour acceder au robot
          plat_check = level 
          varia.page = 'plat'
        
        #Internet explorer
        elif Opr.check_interaction(event.pos, (30.66*res0,38.33*res0,90*res1,varia.resolution[1]), ['home','fd0','messages','notes'], varia.page) == True:
          clickable_icons = {} #on reset les clickable icons 
          varia.page = 'web' #comme avant
          varia.sub_page = ''
          output=''
          clavier_open=False #le clavier est desactivé, l'utilisateur ne peux plus taper du texte

        #Messagerie
        elif Opr.check_interaction(event.pos, (38.33*res0,48.33*res0,90*res1,varia.resolution[1]), ['home','fd0','web','notes'], varia.page) == True: #si on click dans la zone de l'appli mail
          clickable_icons = {} #on reset les clickable icons 
          varia.page = 'messages'
          output = ''
          varia.popup = 0 #vu qu'on click sur l'appli message, on enleve les notifications
        
        #Notes
        elif Opr.check_interaction(event.pos, (50.16*res0,55.66*res0,88.75*res1,varia.resolution[1]), ['home','fd0','web', 'messages'], varia.page) == True: #si on click dans la zone de l'appli notes
          clickable_icons = {} #reset les clickables icons
          varia.page = 'notes'
          output = ''
          clavier_open=True #le clavier est activé, l'utilisateur peut taper du code
        
        #Si on click sur la barre de recherches dans l'internet explorer
        elif Opr.check_interaction(event.pos, (7.2*res0,varia.resolution[0],0.25*res1,7*res1), ['web'], varia.page) == True:
          clavier_open=True #on active le clavier
  
        #Test si click sur une ligne des notes
        elif varia.page == 'notes': # si on est bien sur la page notes
          check = Compu.check_icons(event.pos) # on check si on a cliqué sur une zone avec laquelle on peut intéragir
          if type(check) == int: #si check est un nombre
            varia.notes[0] = check
            output = '' # on reset le texte tapé
            print(varia.notes[0])

        
        # Ouvrir des messages via la messagerie
        elif varia.page == 'messages':
          
          check = Compu.check_icons(event.pos)
          if type(check) == tuple:
            message = varia.messages[check[0]][check[1]] #Si on click un mail on l'ouvre
          if Opr.check_interaction(event.pos, (5*res0,10*res0,0,7.5*res1), ['messages'], varia.page) == True:
            message = varia.messages
            varia.popup = 0 #Si bouton back on revient a la boite mail

          #bouton écrire un mail  
          elif Opr.check_interaction(event.pos, (10*res0,14.5*res0,0,6.75*res1), ['messages'], varia.page) == True: #si on click sur la zone pour écrire un mail
            message = 'New message' 
            output = '' #reset output
            email_data = ['dest', '','',('',),''] #on réinitialise la liste email_data essentiel pour écrire l'objet, le destinataire, et le contenue du mail
            clickable_icons = {} 
            clavier_open=True

          #bouton pour envoyer un mail
          elif Opr.check_interaction(event.pos, (15*res0,19.5*res0,0,6.75*res1), ['messages'], varia.page) == True and message == 'New message':
            
            #check si les contenus du mail ne sont pas vide
            if email_data[1] and email_data[2] and email_data[3]:
              email_data[4] = '!vide'
              varia.unlocked.append(scan.check_message(email_data))
              print(email_data)
            elif email_data[1]=='' and email_data[2]=='' and email_data[3]==('',): # si tous les elements de texte sont vides
              email_data[4] = 'vide' # alors on renvoit que vide
            elif email_data[1]=='' : # si la case destinataire est vide
              email_data[4] = 'casedestinatairevide' # alors on renvoit que vide
            elif email_data[2]=='': # si l'objet est vide
              email_data[4] = 'caseobjetvide' # alors on renvoit que vide
            elif email_data[3]==('',): # si le corps de texte est vide
              email_data[4] = 'casemailvide' # alors on renvoit que vide
              
          #Si click la boîte destinataire
          elif Opr.check_interaction(event.pos, (11*res0,99.66*res0,12.75*res1,19.25*res1), ['messages'], varia.page) == True and message == 'New message':
            email_data[0] = 'dest' # la writing stage est celle du destinataire
            output = email_data[1]
            clavier_open = True # on autorise a faire le lien clavier - pygame
          
          #Si click la boite sujet
          elif Opr.check_interaction(event.pos, (11*res0,99.66*res0,22.25*res1,28.75*res1), ['messages'], varia.page) == True and message == 'New message':
            email_data[0] = 'topic'
            output = email_data[2]
            clavier_open = True # on autorise a faire le lien clavier - pygame
          
          #Si click la boite corps du mail
          elif Opr.check_interaction(event.pos, (12.33*res1,99.66*res0,33.5*res1,81.5*res1), ['messages'], varia.page) == True and message == 'New message':
            email_data[0] = 'content'
            output = email_data[3]
            clavier_open = True # on autorise a faire le lien clavier - pygame

        elif varia.page == 'fd0':
          if Opr.check_interaction(event.pos, (5*res0,10*res0,0,7.5*res1), ['fd0'], varia.page) == True: #Si on click sur le boutton 'arrière'
            clickable_icons = {} #reset les zones clickables
            file_dir_path = file_dir_path[:-1] # on enlève le '/' qui permettait d'entrer dans le fichier
            for c in reversed(file_dir_path): # pour chaque caracter dans le file path
              if c == '/': # jusqu'a que le character ne soit pas un '/'
                output = file_dir_path # on fait le lien avec le texte tapé
                break
              else:
                file_dir_path = file_dir_path[:-1]  #on revient en arrière dans les fichiers

        
          check = Compu.check_icons(event.pos) # Icons
          if type(check) == str:
            clickable_icons = {} #reset les icons clickables
            file_dir_path += check # ajoute le fichier cliqué
            output = file_dir_path # fait le lien avec le clavier
        
        #Regarde si on clique sur la notification d'un mail s'il y en a une
        elif varia.popup != 0:
          if Opr.check_interaction(event.pos,(81.66*res0,varia.resolution[0],80*res1,87.5*res1), ['home','fd0','web','plat','notes'],varia.page) == True:
            varia.popup=0 #vu qu'on click sur la notifiaction, il n'y a plus de notifications
            varia.page = 'messages' 
    
    #Si le clavier est utilisé
    if event.type == pygame.KEYDOWN:
      #Lien entre le clavier et le script sans utiliser input
      if varia.page == 'web' and varia.sub_page == 'binaire.it':
        print('bintetext')
        if event.key == pygame.K_BACKSPACE:
          output = output[:-1]
        else:#si le texte tapé est du simple texte
          print('ajout de charactère')
          output += event.unicode # on ajoute le character au output
      elif clavier_open:
        if event.key == pygame.K_RETURN: # si on utilise la touche entrée
          if varia.page == 'notes': #si on est dans les notes
            varia.notes[1].append('') # on ajoute une ligne
            varia.notes[0] += 1 # on ajoute au nombre de lignes
            output = '' # on rénitialise le output
          elif varia.page == 'messages': # si on est dans la messagerie
            output += ('',) # on rajoute une ligne vide
          else:
            clavier_open = False
        elif event.key == pygame.K_BACKSPACE:
          if varia.page == 'notes':
            varia.notes[1][varia.notes[0]] = varia.notes[1][varia.notes[0]][:-1]
            output = ''
          else:
            if type(output) is str:
              output = output[:-1] # on ajoute le character au output
            else:
              keysDown = pygame.key.get_pressed() 
              if keysDown[pygame.K_LCTRL] or keysDown[pygame.K_RCTRL]: # si on presse sur ctrl
                l = output[-1].rfind(' ')
                if l == -1:
                  if len(output) == 1:
                    output = ('',) # on réinitialise la ligne
                  else:
                    output = output[:-1]
                else:
                  output = output[:-1]+(output[-1][:l],)
              else:
                if len(output[-1]) == 0:
                  if len(output) > 1:
                    output = output[:-2]+(output[-2][:-1],)
                else: 
                  output = output[:-1]+(output[-1][:-1],) #on enleve le dernier character 
        else:
          if type(output) is str: # si le texte tapé est du simple texte
            output += event.unicode # on ajoute le character au output
          else:  # si le texte tapé contient plusieurs ligens
            output = output[:-1]+(output[-1]+event.unicode,) # on ajoute le texte à la ligne
  pygame.display.flip()
  clock.tick(60) # on limite les fps

pygame.quit() # si la boucle s'arrète, on quite
#à l'apolinairehereuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu