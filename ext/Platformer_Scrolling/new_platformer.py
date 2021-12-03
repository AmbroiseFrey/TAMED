import pygame, time
import ext.Core.operations as Opr
import ext.Core.variables as varia
from ext.Platformer_Scrolling.game_utils import Floor, Player, Level_Flag, Lava

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction finit, on revient à la fenetre de main. De là où la fonction est appelée

pygame.init()
screen = pygame.display.set_mode(varia.resolution)
screen_rect = screen.get_rect()

#Test des extensions via main.py
def test():
  screen.fill((0,0,0))
  return 'Platformer connected'

def load_level(level):
  if level == 0:
    floor = pygame.sprite.Group()
    #Un groupe de sprites (des classes donc) qui peuvent etre déplacés ensemble
    for tile in range(0,650,50): #On ajoute les sprites du sol
      floor.add(Floor(tile,380))

    floor.add(Floor(300,220))
    flag = pygame.sprite.Group()
    flag.add(Level_Flag(550,340))
    lava = pygame.sprite.Group()
    lava.add(Lava(300, 340))

  elif level == 1:
    floor = pygame.sprite.Group()
    for tile in range(0,650,50): 
      floor.add(Floor(tile,380))
    floor.add(Floor(300,380))
    lava = pygame.sprite.Group()
    flag = pygame.sprite.Group()
    flag.add(Level_Flag(550,340))
  
  elif level == 2:
    floor = pygame.sprite.Group()
    for tile in range(0,650,50): 
      floor.add(Floor(tile,380))
    floor.add(Floor(300,340))
    floor.add(Floor(300,320))
    floor.add(Floor(300,300))
    for tile in range(190,0,-50):
      floor.add(Floor(300,tile))
    lava = pygame.sprite.Group()
    flag = pygame.sprite.Group()
    flag.add(Level_Flag(550,340))

  else:
    Opr.render_text('The end', (200,300))
  
  return floor, flag, lava

#Boucle du jeu platformer
def play_game(level = 0):
  varia.RUN_plat == True
  clock = pygame.time.Clock()
  player = Player(100, 200)

  floor, flag, lava = load_level(level)

  #Boucle de jeu
  while varia.RUN_plat:
    #Ici on check les events autre que les touches fleches
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        varia.RUN_plat = False

      #Si la souris est pressée
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)

          #On check si l'utilisateur veut quitter le jeu
          if Opr.check_interaction(event.pos, (0,50,0,50),['plat'], 'plat') == True:
            return 'home'

    pygame.event.pump()
    screen.fill((0,0,0))
    Opr.render_image('Assets/Platformer/Background.png', (0,0), (600,400))
    Opr.render_image('Assets/Icons/home.png',(0,0),(50,50))
    
    floor.draw(screen) #On dessine la map
    flag.draw(screen)
    lava.draw(screen)
    player.render() #On render le jouer
    action = player.update(level, floor, flag, lava) #On update par rapport au touches et interactions
    if action == 'Lava':
      action = ''
      return level
      break
    elif action == 'Flag':
      action = ''
      return level+1
      break
    clock.tick(60) #permet de s'adapter à nos boucles, les animations et même les mouvements sont beacoup plus 'smooth'

    pygame.display.flip()