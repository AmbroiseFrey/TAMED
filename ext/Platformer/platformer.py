import pygame, time
from ext.Core import operations as Opr
from ext.Platformer.plat_variables import screen, clock, mi, mid_screen
import ext.Platformer.map_utils as mp
from ext.Platformer.math_utils import Vector


# matrix = (0,0,0,0,0,0,0,0,0,0),(1,0,0,0,0,0,0,0,0,0),(1,2,0,0,0,0,1,2,2,2),(1,1,0,1,1,1,1,2,2,2),(1,1,1,1,1,1,1,1,1,2)
images = {}
images[0] = []
with open('ext/Platformer/images.txt') as f:
    for i in f.readlines()[0].split(' '):
        s = i.split(',')
        images[0].append(float(s[1]))
        loaded_img= pygame.image.load("ext/Platformer/"+s[0])
        x = int(s[2]) if s[2].isdecimal() else 0
        y = int(s[3]) if s[3].isdecimal() else 0
        w = int(s[4]) if s[4].isdecimal() else loaded_img.get_width()
        h = int(w/loaded_img.get_width()*loaded_img.get_height())
        loaded_img = pygame.transform.scale(loaded_img, (w,h))
        images[float(s[1])]=loaded_img,(x,y),(w,h)
images[0].sort()
images[0].reverse()
print(images)
with open('ext/Platformer/data.txt') as f:
    carte = mp.Carte(
        tuple(
            map(
                lambda x : tuple(map(lambda i: int(i), x.split(','))),
                f.readlines()[0].split(' ')
            )
        ),
        (5,10),
        mi/50,
        images
    )
print(carte.points)
print(carte.blocks, "blocks")
block = mp.Block(((0,0),(1,-1),(0,-2),(-2,-1),(-1,2),(1,3)))
# print(block.vectors, block.v_ns, block.offset_vectors, sep='\n')

# wheel = mp.Wheel((0,-10),1)
# carte.insert_wheel(wheel)
chassis = mp.Chassis(
    carte,
    (0,-100),
    ((-20,0),(0,-10),(20,0)),
    20,
    ((-5,5),(5,5),(-15,5),(15,5))
)

# chassis = mp.Chassis((0,-10),((-3,0),(3,0),(0,-2)), ((-3,1),(0,1),(3,1)),1) # position, path, wheels_pos, wheels_rad, spring_elas=.5
# carte.insert_chassis(chassis)
def play_game(level = (700,800)):
  pygame.mixer.init()
  pygame.mixer.music.load('Assets/theme.wav')
  pygame.mixer.music.play()
  print('should play music')
  RUN = True

  while RUN:
      # screen.fill(0xffffff)
      # for w in block.elab_walls(1).walls:
      #     w.draw(mid_screen, 50)
      # block.draw(mid_screen, 50)
      # for b in carte.radBlocks[chassis.w_r]:
      #     for w in b.walls:
      #         w.draw(Vector.subtract(carte.center,carte.relative), 1)
      # Vector.draw((100,100),(198.29424612264538, 218.90053972500195),3, 0x00ff00)
      #On display l'icon pour revenir a l'ordi

      
      carte.update()
      # chassis.update()
      carte.relative = chassis.p
      # chassis.draw()
      carte.draw()

      Opr.render_image('Assets/Icons/App Icons/Normal_Home.png',(0,0),(50,50))
      # for v in mp.vectors:
      #     Vector.draw(v[0], Vector.add(Vector.subtract(carte.center, carte.relative),Vector.multiply(v[1],carte.l)),1, 0xaaaaaa)
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
                return 'home'
      pygame.display.flip()
      # time.sleep(.1)
      clock.tick(60)
  pygame.quit()