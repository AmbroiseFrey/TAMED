import pygame, time
from ext.Platformer.plat_variables import screen, clock, mi
import ext.Platformer.map_utils as mp
from ext.Platformer.map_matrix import map_matrix as matrix

# matrix = (0,0,0,0,0,0,0,0,0,0),(1,0,0,0,0,0,0,0,0,0),(1,2,0,0,0,0,1,2,2,2),(1,1,0,1,1,1,1,2,2,2),(1,1,1,1,1,1,1,1,1,2)
def play_game(level = 0):
  map = mp.MAP(matrix, mi/10)

  r=mi/32

  wheel = mp.Wheel((700,10),r)
  map.addWheel(wheel)

  wheel2 = mp.Wheel((700+mi/8*0.7,0),r)
  map.addWheel(wheel2)

  wheel3 = mp.Wheel((700+mi/4*0.7,0),r)
  map.addWheel(wheel3)

  e = .92 # l'elasticité des ressorts
  ressort1 = mp.Ressort(wheel, wheel2, e,mi/8*0.7)
  ressort2 = mp.Ressort(wheel, wheel3, e,mi/8*0.7)
  #ressort3 = mp.Ressort(wheel2,wheel3, e,mi/8*0.6)
  RUN = True
  while RUN:
    screen.fill(0xffffff)
    map.draw()
    ressort1.update()
    ressort2.update()
    #ressort3.update()
    wheel.update()
    wheel2.update()
    wheel3.update()
    map.relative = wheel.pos
    wheel.display()
    wheel2.display()
    wheel3.display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    pygame.display.flip()
    # time.sleep(1)
    clock.tick(60)
  pygame.quit()