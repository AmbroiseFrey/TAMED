import pygame, time
from ext.Platformer.plat_variables import screen, clock, mi
import ext.Platformer.map_utils as mp
from ext.Platformer.map_matrix1 import map_matrix as matrix

# matrix = (0,0,0,0,0,0,0,0,0,0),(1,0,0,0,0,0,0,0,0,0),(1,2,0,0,0,0,1,2,2,2),(1,1,0,1,1,1,1,2,2,2),(1,1,1,1,1,1,1,1,1,2)
def play_game(level = (700,800)):
  map = mp.MAP(matrix, mi/10)

  r=mi/32


  # Construction du robot
  # C H A S S I S
  # |     |     | Ressort Roue - Chassis
  # W3    W1    W2
  # |     |     |
  # |-----|     | Ressort W3 - W1
  # |     |-----| Ressort W1 - W2
  # ------------- Ressort W3 - W2

  # chassis = mp.Chassis((700,810), (50,20))

  wheel = mp.Wheel((700,810),r)
  map.addWheel(wheel)

  wheel2 = mp.Wheel((700+mi/8*0.7,800),r)
  map.addWheel(wheel2)

  wheel3 = mp.Wheel((700-mi/8*0.7,800),r)
  map.addWheel(wheel3)

  e = .92 # l'elasticité des ressorts
  ressort1 = mp.Ressort(wheel, wheel2, e,mi/8*0.7)
  ressort2 = mp.Ressort(wheel, wheel3, e,mi/8*0.7)
  ressort3 = mp.Ressort(wheel2,wheel3, e,2*mi/8*0.7)
  # ressort4 = mp.Ressort(chassis,wheel, e,mi/8*0.7)
  # ressort5 = mp.Ressort(chassis,wheel3, e,mi/8*0.7)
  # ressort6 = mp.Ressort(chassis,wheel2, e,mi/8*0.7)

  RUN = True
  while RUN:
    screen.fill(0xffffff)
    map.draw()
    ressort1.update()
    ressort2.update()
    ressort3.update()
    # ressort4.update()
    # ressort5.update()
    # ressort6.update()
    wheel.update()
    wheel2.update()
    wheel3.update()
    # chassis.update()
    map.relative = wheel.pos
    wheel.display()
    wheel2.display()
    wheel3.display()
    # chassis.display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    pygame.display.flip()
    # time.sleep(1)
    clock.tick(60)
  pygame.quit()