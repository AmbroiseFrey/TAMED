import pygame, time
from math import cos, sin, pi, ceil, atan
import ext.Core.variables as variables

r = 100

screen = pygame.display.set_mode(variables.resolutiuon)
mid_screen = variables.mid_screen
clock = pygame.time.Clock()
perspective_index = 150

def sumTuple(t):
    s = 0
    for i in t: s+=i
    return s
def multiply_3Dmatrices(m1:tuple,m2:tuple):
    return tuple(
        tuple(
            sumTuple(tuple(m1[i][k]*m2[k][j] for k in (0,1,2)))
            for j in (0,1,2)
        ) for i in (0,1,2)
    )
def sign(n:float): return 1 if n > 0 else -1 if n else 0 
def a(x:float,y:float):
  return atan(y/x) if x else pi/2*sign(y)

class Point:
  def __init__(self, x,y,z):
    self.pos = (x,y,z)
    self.updateDrawPosition()
  def rotate(self, R):
    (cx,sx), (cy,sy), (cz,sz) = R
    k = self.pos[2]*cx + self.pos[1]*sx
    l = self.pos[0]*cy + k*sy
    m = self.pos[1]*cx - self.pos[2]*sx
    self.pos = (
      l*cz - m*sz,
      m*cz + l*sz,
      k*cy - self.pos[0]*sy
    )
    self.updateDrawPosition()
  def applyMatrixRotation(self, matrix):
    self.pos = tuple(sumTuple(tuple(self.pos[j]* matrix[i][j])for j in (0,1,2)) for i in (0,1,2))
  def applyPerspective(self):
    self.persp_coef = 2**(self.pos[2]/perspective_index) # un petit logarithme ne fait pas de mal
    return (self.pos[0]*self.persp_coef, self.pos[1]*self.persp_coef)
  def updateDrawPosition(self):
    self.draw_position = applyScreen(self.applyPerspective())
def applyScreen(p):
  return p[0]+mid_screen[0], p[1]+mid_screen[1]

class Trait:
  dimension = 2*r
  def __init__(self, point1, point2):
    self.A = point1
    self.B = point2
    self.update()
  def update(self):
    self.z_index = (self.A.pos[2]+self.B.pos[2])/2
    coef = max(min(self.z_index/Trait.dimension+.5,1),0) # clamp()
    self.color =(255*coef,)*3
    self.marker_width = ceil(2*coef)
  def display(self):
    pygame.draw.line(screen, self.color, self.A.draw_position, self.B.draw_position, width=self.marker_width)

class Flag:
  color = (0,255,0)
  def __init__(self, scrolling_platformer, planet_view):
    self.point = planet_view # (x,y,z)
  def display(self):
    pygame.draw.circle(screen, Flag.color, self.point.drawPosition, 5)

class Planet:
  def __init__(self, lon = 20, lat = 10, r=100, type = (1,1,0,0)):
    self.r = r
    self.d = (lon+1, lat+1)
    self.mat = tuple(
      tuple(
        Point(
          cos((j/lat-.5)*pi)*cos((i/lon)*2*pi)*r,
          sin((j/lat-.5)*pi)*r,
          cos((j/lat-.5)*pi)*sin((i/lon)*2*pi)*r
        ) for j in range(self.d[1])
      ) for i in range(self.d[0])
    )
    self.traits = []
    for i in range(lon):
      for j in range(lat):
        A = self.mat[i][j]
        if type[0]:
          B = self.mat[(i+1)%self.d[0]][j]
          self.traits.append(Trait(A,B))
        if type[1]:
          C = self.mat[i][(j+1)%self.d[1]]
          self.traits.append(Trait(A,C))
        if type[2]:
          D = self.mat[i+1][j+1]
          self.traits.append(Trait(A,D))
        if type[3]:
          E = self.mat[i][j+1]
          F = self.mat[i+1][j]
          self.traits.append(Trait(E,F))
    self.flags = []
    self.orientation_vertices = Point(1,0,0), Point(0,1,0)
    self.request_display = True
  def addFlag(self, flag: Flag):
    self.flags.append(flag)
    flag.point.applyMatrixRotation(self.getOrientationMatrix())
  def getOrientationMatrix(self): # Bonne chance pour comprendre, j'ai mis 3h à faire ça
    A, B = self.orientation_vertices[0].pos, self.orientation_vertices[1].pos
    rz = a(A[0],A[1])
    cz,sz = cos(rz),sin(rz)
    ry = a(cz*A[0]+sz*A[1],A[2])
    cy,sy = cos(ry),sin(ry)
    rx = a(cz*B[1]-sz*B[0],cy*B[2]+sy*(cz*B[0]+sz*B[1]))
    cx,sx = cos(rx),sin(rx)
    z_matrix = (cz,sz,0),(-sz,cz,0),(0,0,1)
    y_matrix = (cy,0,-sy),(0,1,0),(sy,0,cy)
    x_matrix = (1,0,0),(0,cx,sx),(0,-sx,cx)
    return multiply_3Dmatrices(multiply_3Dmatrices(z_matrix,y_matrix),x_matrix)
  def rotate(self, rotX, rotY, rotZ):
    if rotX or rotY or rotZ:
      rot = tuple((cos(j),sin(j)) for j in (rotX,rotY,rotZ))
      for v in self.orientation_vertices:
        v.rotate(rot)  
      for i in self.mat:
        for j in i:
          j.rotate(rot)
      for i in (self.traits+self.flags):
          i.update()
      self.request_display = True
  def display(self):
    if self.request_display:
      screen.fill((0,0,0))
      self.request_display = False
      for i in sorted(self.traits+self.flags,key=lambda t:t.z_index):
        i.display()

planet = Planet(30,15)



##------------------------------##
##----------Utilisation---------##
##------------------------------##


# planet = Planet(20,10,r,(0,1,0,0))

# RUN = True
# while RUN:
#     keys = pygame.key.get_pressed()
#     rX = (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*.01
#     rY = (keys[pygame.K_UP]-keys[pygame.K_DOWN])*.01
#     planet.rotate(rY,rX,0)
#     planet.display()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             RUN = False
#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()