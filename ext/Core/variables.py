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
resolution = (600,400)
mid_screen = tuple(i/2 for i in resolution)
Login_Background = 'Assets/Backgrounds/Login_Background_(Test).png'
RUN_plat = True
unlocked = [] #Variable type 'achievements' qui permet d'acceder à de nouveaux fichiers/messages

flags = [(0,0,0)]# Coordinates
n_flags = 0

page = 'home'
file_dir_path = '' #Les fichiers

recovered_drive = {'D:':{  #Le drive trouvé par le robot
  'User:' : 'Thing',
},
}

messages = { # les messages recus de base
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
  100:{
    "TAMED Mission - 1":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED-Command",
      "Bonjour,",
      "Nous somme près pour lancer la premiere mission du projet T.A.M.E.D.",
      "Nous devons déjà retrouver la boite noire de la station ___.",
      "Comme vous le savez tous, l'incident qui a malheuresement fait un mort doit etre élucidé.",
      "Je compte donc sur vous pour pouvoir trouver les informations necessaires à l'enquete.",
      "Nous nous lancerons dans le but pincipal de cette mission apres avoir trouvé la boite noire."
    ]
  },
}

sound = 'Assets/Computer-Start.wav'