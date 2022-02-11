import pygame
from math import cos, sin, pi
from ext.Core import variables as variables
from ext.Core import operations as Opr

# on créer les paramètres de la sphère
lon = 20
lat = 10
r = 110

mat_d = (lon, lat+1) # dimension de la matrice `mat`
mat = tuple(tuple((cos(i/lon*2*pi)*cos((j/lat-.5)*pi)*r, sin(i/lon*2*pi)*r, cos(i/lon*2*pi)*sin((j/lat-.5)*pi)*r) for j in range(mat_d[1])) for i in range(mat_d[0])) # création de la matrice en fonction des paramètres

screen = pygame.display.set_mode(variables.resolution) #initiation de l'écran
mid_screen = variables.mid_screen+(r*2,) # coordonnées du milieu de l'écran
clock = pygame.time.Clock() 
perspective_index = 1.5*r # indice de perspective pour la sphère

a = (cos,sin) # variable pour simplifier les commandes
def applyRotation(p, R:tuple): # 
  """prend un point et une Rotation et renvoie le point auquel on a appliqué les rotations définies par `R`"""
  (cx,sx), (cy,sy), (cz,sz)=R
  k = (
    p[0],
    p[1]*cx - p[2]*sx,
    p[2]*cx + p[1]*sx
  )
  l = (
    k[0]*cy + k[2]*sy,
    k[1],
    k[2]*cy - k[0] *sy
  )
  return (
    l[0]*cz - l[1]*sz,
    l[1]*cz + l[0]*sz,
    l[2]
  )
def moy(A,B):
  """prend 2 points en argument et renvoie la moyenne des positions z de ces points"""
  return (A[2]+B[2])/2
def width(A,B):
  """prend 2 points en argument et renvoie la taille d'un trait entre ces points en fonction de leur profondeur"""
  return int((A[2]+B[2])/1.25*2)
def applyScreen(p):
  """prend un point en argument et renvoie la position de ce point en fonction du milieu de l'écran pour centrer la sphère"""
  return tuple(p[i]+mid_screen[i] for i in range(2))+(p[2],)
def applyPerspective(p):
  """prend un point et renvoie la coordonnée de ce point en 2 dimensions après application de la perspective et le coefficient qui a permis d'ateindre ce""" 
  coef = 2**(p[2]/perspective_index)
  return tuple(p[i]*coef for i in range(2))+(coef,)

def update_matrix(matrix, rX, rY,rZ):
  """on prend la matrice en argument et les rotations x,y et z et on renvoie la matrice issue de la matrice mais à laquelle on a changé tous les points pour avoir leurs positions en fonction de ces rotations""" 
  rot = tuple(tuple(a[i](j) for i in range(2)) for j in (rX,rY,rZ)) 
  return tuple(tuple(applyScreen(applyPerspective(applyRotation(j, rot))) for j in i) for i in matrix)

def display_matrix(matrix,d, rotX, rotY, rotZ):
  """affiche la matrice directement sans se soucier de la prodfondeur moyenne des traits""" 
  updated_matrix = update_matrix(matrix, rotX, rotY, rotZ)
  for i in range(d[0]):
    for j in range(d[1]-1):
      point = updated_matrix[i][j]
      p_right = updated_matrix[(i+1)%d[0]][j]
      p_down = updated_matrix[i][j+1]
      pygame.draw.line(screen, (255,255,255), point[:2], p_right[:2], width=width(point, p_right))
      pygame.draw.line(screen, (255,255,255), point[:2], p_down[:2], width=width(point, p_down))

def display_matrix_image(matrix,d, rotX, rotY, rotZ, image):
  """affiche la matrice avec une image à l'intérieur""" 
  updated_matrix = update_matrix(matrix, rotX, rotY, rotZ)
  traits = ()
  for i in range(d[0]):
    for j in range(d[1]-1):
      p = updated_matrix[i][j]
      q = updated_matrix[(i+1)%d[0]][j]
      m = updated_matrix[i][j+1]
      traits= traits+((p[:2],q[:2],moy(p,q),width(p,q)),(p[:2],m[:2],moy(p,m),width(p,m)))
  traits = sorted(traits, key = lambda t: t[2])
  x=0
  while traits[x][2]<1:
    trait = traits[x]
    pygame.draw.line(screen, (255*(trait[2]-.25),)*3, trait[0], trait[1], width=trait[3])
    x+=1
  Opr.render_image(image, (0,0), (int(r*1.5),)*2, True)
  for i in range(x, len(traits)):
    trait = traits[i]
    pygame.draw.line(screen, (255*min(trait[2]-.25,1),)*3, trait[0], trait[1], width=trait[3])