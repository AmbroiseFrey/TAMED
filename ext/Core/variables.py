import pygame
from screeninfo import get_monitors

#Couleurs
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
TRANSPARENT = pygame.Color(0,0,0,0) # si jamais

#resolution (probablement la variable la plus importante du projet)
for monitor in get_monitors():
  resolution = monitor.width, monitor.height
mid_screen = tuple(i/2 for i in resolution)
Login_Background = 'Assets/Backgrounds/Login_Background_(Test).png'
RUN_plat = True
unlocked = [] #Variable type 'achievements' qui permet d'acceder à de nouveaux fichiers/messages

popup = 0

flags = [(0,0,0)]# Coordinates
n_flags = 0

page = 'home'
sub_page ='' #Sous page (utile pour le web)
file_dir_path = '' #Les fichiers

recovered_drive = { #Le drive trouvé par le robot
'D:':{
  'Project:Zeus' : {
    'Programmes' : {
      'gyro_system.exe' : 'FILE NOT FOUND',
      'destroy.exe' : 'destroy.exe',
    },
    'Station Logs' : {
      'Zeus - Log 1.odt' :[
        'Jour 1',
        'Colonel Thompson',
        "Je suis bien arrivé sur le site d'orbite de la station.",
        "Déployement du bras robotique: 83/100",
        "Arrimage des modules lab et main: 96/100"
      ],
      '???.odt' : 'Hardware damaged',
      'Zeus - Log 52.odt' :[
        'Jour 52',
        'Colonel Thompson',
        "Je capte des signals inconnus"
      ]
    }
  },
},
}

messages = { # les messages recus de base
    1000:{
    "[URGENT] TAMED Mission - 1":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour,",
      "Nous sommes enfin prêts pour lancer la première mission du projet T.A.M.E.D.",
      "Nous devons déjà retrouver la boîte noire de la station Zeus.",
      "Comme vous le savez tous, l'incident qui a malheuresement fait un mort doit être élucidé.",
      "Je compte donc sur vous pour pouvoir trouver les informations nécessaires à l'enquête.",
      "Nous nous lancerons dans le but pincipal de cette mission après avoir trouvé le disque dur.",
      "Veuillez:", 
      " - Envoyer un mail intitulé Réussite de la Mission 1 une fois que vous avez récupéré le disque dur.",
      " - Evaluer le niveau de fichiers endommagés une fois le disque dur transféré sur votre ordinateur",
      "Merci,",
      "Général Michael Fredlyn",
      "P.S.",
      "Merci de faire toute communication a propos du projet TAMED à l'adresse Group:Tamed"]
  },
  0.1:{
    "Bug Majeur de la Messagerie":[
      "from: Services Techniques",
      "to: Group:KryptCorp-Europe",
      "Bonjour a tous,",
      "Malheuresement, un bug ne permet plus d'utiliser de caractère accentués dans la messagerie.",
      "Nous sommes désolé pour ce gêne et nous tentons de le réparer au plus vite",
      "Cordialement,",
      "Services Techniques Internes de Krypt Corp Europe"],
  },
  0:{
    "J.M.T.D. Europe Meeting":[
      "from: Dir. Slane",
      "to: Group:JMTD-Europe",
      "Bonjour a tous,",
      "La reunion du departement J.M.T.D. aura lieu demain a 20:00 GMT+1.",
      "Cordialement,",
      "Director Slane,",
      "J.M.T.D. Europe Director"],
  },
}


notes = [0,['']] # [n de ligne, [texte dans chaque ligne]]

sound = 'Assets/Computer-Start.wav'