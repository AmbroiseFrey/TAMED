import pygame, time
from math import cos, sin, pi
import ext.Core.variables as variables

lon = 30#int(input("longitude"))
lat = 15#int(input("latitude"))
r = 75

mat_d = (lon, lat+1)
mat = tuple(tuple((cos(i/lon*2*pi)*cos((j/lat-.5)*pi)*r, sin(i/lon*2*pi)*r, cos(i/lon*2*pi)*sin((j/lat-.5)*pi)*r) for j in range(mat_d[1])) for i in range(mat_d[0]))
#for i in range(lon):
#  lo = i/lon*2*pi
#  mat[i]= []
#  for j in range(lat+1):
#    la = (j/lat-.5)*pi
#    mat[i][j] = (cos(lo)*cos(la)*50, sin(lo)*50, cos(lo)*sin(la)*50)

screen = pygame.display.set_mode(variables.resolution)
mid_screen = variables.mid_screen+(r*2,)
clock = pygame.time.Clock()
perspective_index = 150

a = (cos,sin)
def applyRotation(p, R):
    ((cx,sx), (cy,sy), (cz,sz))=R
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
        l[2] + 100
    )
def moy(A,B):
    return int((A[2]+B[2])/1.5)
def applyScreen(p):
    return tuple(p[i]+mid_screen[i] for i in range(2))+(p[2],)
def applyPerspective(p):
    return tuple(p[i]*2**(p[2]/perspective_index) for i in range(2))+(2**(p[2]/(1.5*r)),)
def display_matrix(matrix,d, rotX, rotY, rotZ):
    rot = tuple(tuple(a[i](j) for i in range(2)) for j in (rotX,rotY,rotZ))
    updated_matrix = tuple(tuple(applyScreen(applyPerspective(applyRotation(j, rot))) for j in i) for i in matrix)
    for i in range(d[0]):
        for j in range(d[1]-1):
            point = updated_matrix[i][j]
            p_right = updated_matrix[(i+1)%mat_d[0]][j]
            p_down = updated_matrix[i][j+1]
            pygame.draw.line(screen, (255,255,255), point[:2], p_right[:2], width=moy(point, p_right))
            pygame.draw.line(screen, (255,255,255), point[:2], p_down[:2], width=moy(point, p_down))

# RUN = True
# rY=0
# rX=.02
# while RUN:
#     rY+=0.001
#     rX+=0.002
#     screen.fill((0,0,0))
#     display_matrix(mat,rX,rY,0)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             RUN = False

#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()