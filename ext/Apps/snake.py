import pygame, time, random
import ext.Core.variables as varia
import ext.Core.operations as Opr
pygame.init()

def test():
  return 'Successfully built snake game'
 
pygame.init()
 
resolution = varia.resolution
 
screen = pygame.display.set_mode(resolution)
 
clock = pygame.time.Clock()

snake_speed = 15
 #tu as vu le chat ?
def render_snake(snake):
  for x in snake:
    if x == 1:
      Opr.render_rectangle(varia.BLACK, (10,10), varia.mid_screen)
    elif x == 0:
      Opr.render_rectangle( varia.WHITE, (10,10), varia.mid_screen)
 
 
def game():
    RUN = True
    x,y = varia.mid_screen
 
    snake = [1,0]
    snk_length = 1
 
    while RUN:
      clock.tick(snake_speed)
      screen.fill((0,0,0))
      render_snake(snake)
      Opr.render_image('Assets/Icons/cross.png',(0,0),(50,50))
      #Ici on check les events autre que les touches fleches
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          RUN = False

        #Si la souris est pressée
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse_presses = pygame.mouse.get_pressed()
          if mouse_presses[0]:
            print(event.pos)

            #On check si l'utilisateur veut quitter le jeu
            if Opr.check_interaction(event.pos, (0,50,0,50),['plat'], 'plat') == True:
              RUN = False
        pygame.display.flip()
    pygame.quit()