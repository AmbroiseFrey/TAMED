import pygame, time
from ext.Core import operations as Opr
from ext.Core import variables as varia
from ext.Platformer.components import Floor, Player, Level_Flag, Lava
from ext.Platformer.game_utils import Group

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

#Boucle du jeu platformer
def play_game(level = 0):
  varia.RUN_plat == True
  clock = pygame.time.Clock()
  player = Player(100, 200)
  print(player.r)
  print(player.size)
  floor = Group()
  for tile in range(0,10000,50): 
    floor.add(Floor(tile,380+tile/12))
  for tile in range(330,0,-50): 
    floor.add(Floor(0,tile))
  #Boucle de jeu
  while varia.RUN_plat:
    Opr.render_image('Assets/Platformer/Background.jpg', (0,0), (600,400)) #on display le Background

    #On display et update les sprites ici
    player.update(floor)
    floor.display()

    #On display l'icon pour revenir a l'ordi
    Opr.render_image('Assets/Icons/home.png',(0,0),(50,50))
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

    clock.tick(60) #permet de s'adapter à nos boucles, les animations et même les mouvements sont beacoup plus 'smooth'

    pygame.display.flip()