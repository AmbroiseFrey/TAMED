import pygame
from ext.Core import variables

screen = pygame.display.set_mode(variables.resolution)
clock = pygame.time.Clock()

matrix = (
 (0,0,0,0,0,0,0,0,0,0,0),
 (0,1,0,0,0,0,0,0,0,0,0),
 (1,1,0,0,0,0,0,0,0,0,0),
 (1,1,1,0,0,0,0,0,0,0,0),
 (1,1,1,0,0,1,1,1,0,0,0),
 (1,1,1,1,1,1,1,1,1,0,1),
)
d=(len(matrix), len(matrix[0]))

color = (0,0,0)
r=((0,.5),(0,0),(.5,0)),((.5,0),(1,0),(1,.5)),((1,.5),(1,1),(.5,1)),((.5,1),(0,1),(0,.5))

def remove_doublons(t):
    return tuple(t[i] for i in range(len(t)) if t[i]!=t[i-1] and t[i]!=t[(i+1)%len(t)])

#----------------------#
#----- init tiles -----#
#----------------------#
tiles = [0]*16
for i in (0,1):
    for j in (0,1):
        for k in (0,1):
            for l in (0,1):
                tiles[i*8+j*4+k*2+l] = remove_doublons(
                      (r[0] if i else ())
                    + (r[1] if j else ())
                    + (r[2] if k else ())
                    + (r[3] if l else ())
                    )
print(tiles)
                

def draw_pol(d,l, p):
  if d[0] or d[1] or d[2] or d[3]:
    points = tuple(tuple((p[0]+t[0])*l for i in (0,1)) for t in tiles[d[0]*8+d[1]*4+d[2]*2+d[3]])
    pygame.draw.polygon(screen, color, points)

l= min(400/(d[0]-1), 400/(d[1]-1))

def draw_map():
  screen.fill((255,0,0))
  for i in range(d[0]-1):
    for j in range(d[1]-1):
      draw_pol((matrix[i][j],matrix[i][j+1],matrix[i+1][j+1],matrix[i+1][j]),l,(j,i))