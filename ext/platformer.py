import pygame, time
import ext.operations as Opr

resolution = (600,400)
niveau = 0

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction fini on revient à la fenetre de main de la ou la fonction est appelée

WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode([600, 400])

def test():
  screen.fill((0,0,0))
  return 'Platformer connected'
    
def play_game():
  RUN = True
  while RUN:
    screen.fill((0,0,0))
    Opr.render_text('Works',(100,100))
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))

    pygame.display.flip()


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        RUN = False

      #Si la souris est pressée
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)

          #On check si l'utilisateur veut quitter le jeu
          if Opr.check_interaction(event.pos, (0,50,360,400),['plat'], 'plat') == True:
            RUN = False
            return 'home'