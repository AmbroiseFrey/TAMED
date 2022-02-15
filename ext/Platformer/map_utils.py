import pygame
from ext.Core import operations as Opr
from ext.Core import variables as varia
from ext.Platformer.math_utils import hypot, mp, sumTuple, Vector, Point, Droite, Circle, Triangle
from math import floor, pi, asin, cos, sin, log
from ext.Platformer.plat_variables import screen, resolution, mid_screen, mi

def every(itera, callback=lambda x,i:True):
  for i in range(len(itera)):
    if not callback(itera[i],i):
      return False
  return True


class Wall:
  def __init__(self, p, v):
    self.line = Droite(v[0], v[1], -(v[0] * p[0] + v[1] * p[1]))
    h = hypot(v[0],v[1])
    self.p = p
    self.vector = Vector.multiply(v, 1/h)
    self.v = v
  @classmethod
  def AutoConstructed(cl,wall):
    return cl(wall.p,wall.v)
  def clone(self):
    return Wall.AutoConstructed(self)

class MAP:
  marching_squares = (
    (),
    (((0, .5), (.5, 1), (0, 1)),),
    (((.5, 1), (1, .5), (1, 1)),),
    (((0, .5), (1, .5), (1, 1), (0, 1)),),
    (((1, .5), (.5, 0), (1, 0)),),
    (((1, .5), (.5, 0), (1, 0)), ((0, .5), (.5, 1), (0, 1))),
    (((.5, 0), (1, 0), (1, 1), (.5, 1)),),
    (((0, .5), (.5, 0), (1, 0), (1, 1), (0, 1)),),
    (((0, 0), (.5, 0), (0, .5)),),
    (((0, 0), (.5, 0), (.5, 1), (0, 1)),),
    (((0, 0), (.5, 0), (0, .5)), ((.5, 1), (1, .5), (1, 1))),
    (((0, 0), (.5, 0), (1, .5), (1, 1), (0, 1)),),
    (((0, 0), (1, 0), (1, .5), (0, .5)),),
    (((0, 0), (1, 0), (1, .5), (.5, 1), (0, 1)),),
    (((0, 0), (1, 0), (1, 1), (.5, 1), (0, .5)),),
    (((0, 0), (1, 0), (1, 1), (0, 1)),)
  )
  WALL = {}
  @classmethod 
  def add_WALL(cl, r):
    R = r / (2**.5)
    if r not in MAP.WALL.keys():
      MAP.WALL[r] = (
        (),
        (Wall((   R, .5-R), (1, -1)),),
        (Wall(( 1-R, .5-R), (-1, -1)),),
        (Wall((   0, .5-r), (0, -1)),),
        (Wall(( 1-R, .5+R), (-1, 1)),),
        (Wall(( 1-R, .5+R), (-1, 1)), Wall((0, .5-r), (1,-1))),
        (Wall((.5-r,    0), (-1, 0)),),
        (Wall((  -R, .5-R), (-1, -1)),),
        (Wall((   R, .5+R), (1, 1)),),
        (Wall((.5+r,    0), (1, 0)),),
        (Wall((   R, .5+R), (1, 1)), Wall((1, .5-r), (-1,-1))),
        (Wall((.5+R,   -R), (1, -1)),),
        (Wall((   0, .5+r), (0, 1)),),
        (Wall(( 1+R, .5+R), (1, 1)),),
        (Wall((  -R, .5+R), (-1, 1)),),
        ()
      )
    return MAP.WALL[r]
  types = (
    (0, 0x888888), 
    (.75, 0x00ffff)   
  )
    
  def __init__(self, matrix, l, centerPosition = mid_screen):
    self.l = l
    self.matrix = matrix
    # print(matrix)
    self.mat_d = len(self.matrix[0]), len(self.matrix)
    self.wheels = ()
    self.center = centerPosition
    self.relative = mid_screen
    self.view = Vector.multiply(centerPosition,-1),Vector.subtract(resolution,centerPosition)
  def addWheel(self, wheel):
    MAP.add_WALL(wheel.r / self.l)
    wheel.map = self
    self.wheels += (wheel,)
  def draw(self):
    self.t = Vector.subtract(self.center,self.relative)
    minX, minY = mp(self.findPointCase(Vector.add(self.relative, self.view[0])), lambda e,i : max(0, e))
    maxX, maxY = mp(self.findPointCase(Vector.add(self.relative, self.view[1])), lambda e,i : min(e + 1, self.mat_d[i] - 1))
    for y in range(minY,maxY):
      for x in range(minX,maxX):
        bl = self.matrix[y][x], self.matrix[y][x + 1], self.matrix[y + 1][x + 1], self.matrix[y + 1][x]
        for k in range(len(MAP.types), 0, -1):
          if not every(bl, lambda e,i: e!=k):
            a, b, c, d = mp(bl, lambda e,i: 1 if e and e <=k else 0)
            path = MAP.marching_squares[a * 8 + b * 4 + c * 2 + d]
            for points in path:
              points = mp(points, lambda e,j : Vector.add(Vector.subtract(Vector.multiply(Vector.add(e,(x,y)), self.l), self.relative),self.center))
              pygame.draw.polygon(screen, MAP.types[k-1][1], points)
  def findPointCase(self, p):
    return mp(p, lambda e,i : floor(e / self.l))
  def vectorCases(self, point, vector):
    p1, p2 = mp((point, Vector.add(point, vector)), lambda e,i : self.findPointCase(e))
    r = ()
    drt = Droite.Point_Vector(Vector.multiply(point, 1 / self.l), Vector.multiply(vector, 1 / self.l))
    if p1[0] == p2[0]:
      index = -1 if p1[1] > p2[1] else 1
      for i in range(p1[1], p2[1] + index, index):
        r+=((p1[0], i),)
      return r
    if p1[1] == p2[1]:
      index = -1 if p1[0] > p2[0] else 1
      for i in range(p1[0], p2[0] + index, index):
        r += ((i, p1[1]),)
      return r
    if abs(p1[0] - p2[0]) > abs(p1[1] - p2[1]):
      if vector[0] < 0: p1,p2 = p2,p1
      offsetX = p1[0]
      index = -1 if p1[1] > p2[1] else 1
      for y in range(p1[1], p2[1] + index, index):
        nX = floor(Droite(0, 1, -y -index).intersection(drt)[0])
        x = offsetX
        while x != nX + 1 and x != p2[0] + 1:
          r+=((x, y),)
          x+=1
          offsetX = nX
      return r
    else:
      if vector[1] < 0: p1,p2 = p2,p1
      offsetY = p1[1]
      index = -1 if p1[0] > p2[0] else 1
      for x in range(p1[0], p2[0]+index, index):
        nY = floor(Droite(1, 0, -x - (1 if index == 1 else 0)).intersection(drt)[1])
        y = offsetY
        while y != nY + 1 and y != p2[1] + 1:
          r+=((x, y),)
          y+=1
          offsetY = nY
      return r
  def vectorCasesWithRadius(self, point, vector, radius = 0):
    pass
  def readMatrixCase(self, point, radius):
    radius /= self.l
    j,i = point
    bl = (self.matrix[i][j], self.matrix[i][j + 1], self.matrix[i + 1][j + 1], self.matrix[i + 1][j])
    walls = ()
    for k in range(len(MAP.types), 0, -1):
      if not every(bl, lambda e,i: e!=k):
        a, b, c, d = mp(bl, lambda e,i: 1 if e and e <=k else 0)
        addwalls = MAP.WALL[radius][a * 8 + b * 4 + c * 2 + d]
        for wall in addwalls:
          wall = wall.clone()
          wall.line = Droite(wall.line.a, wall.line.b, wall.line.c)
          wall.line.translate((j, i))
          wall.type = k-1
          walls += (wall,)
    return walls 
  def withinCase(self, point, cas):
    return point[0] >= cas[0] and point[0] <= cas[0] + 1 and point[1] >= cas[1] and point[1] <= cas[1] + 1
  def withinMap(self, cas):
    return cas[0] > -1 and cas[0] < self.mat_d[0] - 1 and cas[1] > -1 and cas[1] < self.mat_d[0] - 1
  def drawCircle(self, p, r=1, c=0x000000):
    pygame.draw.circle(screen, c, Vector.add(Vector.subtract(p,self.relative),self.center), r)
  def drawLine(self, p1, p2, w, c=0x000000):
    pygame.draw.line(screen, c, Vector.add(Vector.subtract(p1,self.relative),self.center), Vector.add(Vector.subtract(p2,self.relative),self.center))
  def drawLineLine(self, l):
    drt = Droite(l[0],l[1],l[2] * self.l)
    drt.translate((-50, -50))
    drt.draw(self.view)
  def drawVector(self, vector, point, w=.5, c=0x000000):
    Vector.draw(vector, Vector.add(Vector.subtract(point,self.relative),self.center),w,c)

# class Chassis:
#   def __init__(self, points: tuple, wheels_positions, wheels_radius, propellers_positions, center: tuple = (0,0)):
#     assert len(propellers_positions) == 2, "there can  only be 2 propellers"
#     self.attachpoint = center
#     self.orientation = pi/2
#     self.rotateIndex = 0
#     self.points = points
#     self.Pts_dist = tuple(map(lambda pt: Point.distance(pt, center), points))
#     self.vector = [0, 0]
#     self.weight = [0, .1]
#     self.forces = [self.weight]
#     self.propellers = [Propeller(self, p) for p in propellers_positions]
#     self.wheels = [Wheel(p, wheels_radius) for p in wheels_positions]
#     for w in self.wheels:
      
#     self.P_dist = tuple(map(lambda pos: Point.distance(pos, center), propellers_positions))
#   def update(self):
#     keys = pygame.key.get_pressed()
#     self.propellers[0].power = keys[pygame.K_UP] and (keys[pygame.K_RIGHT] or .75) or 0
#     self.propellers[1].power = keys[pygame.K_UP] and (keys[pygame.K_LEFT] or .75) or 0
#     for prop in self.propellers:
#       prop.update()
#     self.vector = Vector.add(self.vector, self.propellers[0].force, self.propellers[1].force, self.weight)
#     self.attachpoint = (
#       self.vector[0] * .1 + (self.propellers[0].nextpos[0] + self.propellers[1].nextpos[0] + self.attachpoint[0] + self.weight[0]) / 3,
#       self.vector[1] * .1 + (self.propellers[0].nextpos[1] + self.propellers[1].nextpos[1] + self.attachpoint[1] + self.weight[1]) / 3
#     )
#     rotation =  asin(-self.propellers[0].power / self.P_dist[0]) + asin(self.propellers[1].power/self.P_dist[1])
#     self.rotateIndex += rotation
#     self.orientation += self.rotateIndex * .1 + rotation
#     self.vector = Vector.multiply(self.vector, .99)
#     self.rotateIndex *= .95
#   def addForce(self, force):
#     self.forces.append(force)
#   def display(self):
#     for prop in self.propellers:
#       prop.display()

class Wheel:
  def __init__(self, chassis, pos, r, bounciness=.5):
    self.pos = pos
    self.r = r
    self.vector = 0,0
    self.weight = 0,.1
    self.rotate = 0
    self.powerIndex = .97
    self.decuplation = 9
    self.map = chassis.mp
    self.element = None
    self.bounce = bounciness
    self.forces = [self.weight]
    self.chassis = chassis
  def update(self, keys):
    for f in self.forces:
      self.vector = Vector.add(self.vector, f)
    point = self.pos
    vector = self.vector
    self.drawVec()
    size = Vector.getNorm(self.vector)
    Size = size
    mymap = self.map
    index = 0
    while (True and index < 3):
              # on récupère les cases sur lesquelles se trouve la roue
      cases = tuple(c for c in mymap.vectorCases(point, vector) if self.map.withinMap(c))
      droite = Droite.Point_Vector(Vector.multiply(point, 1 / self.map.l), vector)# on définit l'objet droite qui permettra de trouver les intersections avec les droites des murs
      murs = () # variable ou l'on stocke tous les murs
      for c in cases: # on ajoute les murs sur lesquelles il y a une intersection
        a = tuple((mur, droite.intersection(mur.line)) for mur in self.map.readMatrixCase(c, self.r) if Vector.isOpposite(vector, mur.vector))
        a = tuple((mur[0],mur[1],Point.distance(Vector.multiply(point, 1 / self.map.l), mur[1])) for mur in a if mur[1])
        for m in a:
          murs += (m,)
      if len(murs) == 0: break # on sort de la boucle si la roue ne collide pas avec un mur
      mur = sorted(murs, key = lambda m : m[2])[0] # on prend le mur le plus proche
      R = Vector.multiply(mur[1], self.map.l) # le point d'intersection entre la roue et le mur à l'échelle réelle
      mur[0].line.homothetia(self.map.l)# on met la droite de trajectoire de la roue à l'échelle réelle
              
      # dessiner la droite du mur qui représente les vecteurs en jeu
      # drt = Droite(mur[0].line.a, mur[0].line.b, mur[0].line.c)
      # drt.translate(Vector.add(Vector.multiply(self.map.relative, -1), self.map.center))
      # drt.draw()

      Q = mur[0].line.closest(point) #le point le plus proche du point sur le mur
      PR = mur[2] * self.map.l # distance entre PR (entre le point `point` et le point R) à échelle réelle
      QR = Point.distance(R, Q) # distance QR (entre les points Q et R)
      v_QR = Vector.subtract(R, Q) # vecteur de Q à R

      Pp = mur[0].line.closest(Point.translate(point, vector)) # point P' (où se trouve la roue après la collision avec le mur) 
      PpQ = Point.distance(Pp, Q) # distance P'Q (entre les points P' et Q) 

      nV = Vector.subtract(point, R) # vecteur du point P vers R

      Size = PpQ
      if (size < PR): # si la taille du vecteur est supérieure à la distance entre P et R
        point = Vector.subtract(Pp, vector)
        break # on sort de la boucle while True
                      
      vector = Vector.subtract(Pp, R) # on change la valeur du vecteur 

      traction = []
      size = Vector.getNorm(vector) # on change la variable size par la taille du vecteur

                  
      v = (-mur[0].vector[1], mur[0].vector[0]) # le vecteur qui va vers la gauche d'un mur
      friction = 1 - MAP.types[mur[0].type][0]
      self.rotate = (vector[0] / v[0] if v[0] else vector[1] / v[1]) # la rotation effectuée par la roue 

      if (keys[pygame.K_SPACE]): # si on active le 'frein'
        power = 2 ** (-abs(self.rotate))
        wished_rotation = 0
      else:
        wished_rotation = (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * self.decuplation * self.powerIndex * pi / 2
        power = self.powerIndex / self.decuplation / 10 * mi/40
                  
              # self.rotate -= (self.rotate - wished_rotation) * power * friction # on change la rotation de la roue
      vector = Vector.add(vector, Vector.multiply(v, (self.rotate - wished_rotation) * power * friction)) # on change le vecteur on fonction de la rotation réelle de la roue
                  
      point = R
      index+=1
    self.pos = Vector.add(point, vector)
    self.vector = Vector.setToNorm(vector, Size)
    self.vector = Vector.multiply(self.vector, .995)
  def addForce(self, force):
    self.forces.append(force)
  def draw(self):
    self.map.drawCircle(self.pos, self.r, 0xff0000)
    Vector.draw(self.vector, mid_screen, 0, 1)
  def drawVec(self):
    # Vector.draw(self.vector, Vector.subtract(self.pos, self.map.relative), self.map.svg, "#0005", .3)
    pass
        
class Ressort:
  def __init__(self, p, q, elasticity=.5, distance=None):
    self.p = p
    self.q = q
    self.dist = distance if distance else Point.distance(p.pos,q.pos)
    self.v1 = [0,0]
    p.addForce(self.v1)
    self.v2 = [0,0]
    q.addForce(self.v2)
    self.elas =  1 - elasticity
  def update(self):
    a,b  = Vector.subtract(self.p.pos, self.q.pos)
    h = hypot(a,b)
    s = (h-self.dist)/2 * self.elas/h
    # print(self.dist)
    # print(a,b,h,s)
    a *= s
    b *= s
    self.v1[0] = -a
    self.v1[1] = -b
    self.v2[0] = a
    self.v2[1] = b
    # print(self.v1,self.v2)
  def display(self, Map=None, color=0, width=1):
    if Map:
      a,b = mp((self.p.pos,self.q.pos), lambda e,i : Vector.subtract(Vector.add(Vector.multiply(e, Map.l), Map.relative), Map.center))
      pygame.draw.line(screen, color, a,b, width)
    else: pygame.draw.line(screen, color, self.p.pos, self.q.pos, width)
        
class Propeller:
  def __init__(self, chassis, pos):
    self.power = 0
    self.chassis = chassis
    self.vector = 0,0
    self.pos = pos
  def update(self):
    self.vector = (
      cos(self.chassis.orientation) * self.power,
      -sin(self.chassis.orientation) * self.power
    )
    self.nextpos = Vector.add(self.pos, self.vector)
  def draw(self, vector:bool=False):
    if vector:
      Vector.draw(self.vector, Vector.add(self.pos,self.chassis.mp.t), 1)
    pygame.draw.line(screen, 0xffff, Vector.add(self.pos,self.chassis.mp.t), Vector.add(self.pos,self.chassis.mp.t,Vector.multiply(self.vector,-10*self.power**.5)), 3)

class Weight:
  def __init__(self, pos):
    self.vector = 0,1
    self.pos = pos
  def update(self):
    self.nextpos = Vector.add(self.pos, self.vector)

class AttachPoint:
  def __init__(self, chassis, wheel, elasticity):
    self.elas = 1 - elasticity
    self.chassis = chassis
    self.wheel = wheel
    self.pos = wheel.pos
    self.vector = self.wheel.weight
    self.nextpos = self.pos
  def update(self, keys):
    self.wheel.update(keys)
    v = Vector.subtract(self.wheel.pos, self.pos)
    h = log(Vector.getNorm(v))
    s = log(h)*self.elas if h>1 else 0
    if s < 10:
      self.wheel.vector = Vector.add(self.wheel.vector, Vector.multiply(v, -s))
      self.vector = Vector.multiply(v, s)
    else: #pour éviter les erreurs
      # pygame.quit()
      self.wheel.vector = 0,0
      self.vector = 0,0
      self.wheel.pos = self.pos
    self.nextpos = Vector.add(self.pos,self.vector)
  def draw(self):
    pygame.draw.circle(screen, 0xffff00, Vector.add(self.pos, self.chassis.mp.t), 1)
    pygame.draw.line(screen, 0xffaa00, Vector.add(self.pos, self.chassis.mp.t), Vector.add(self.wheel.pos, self.chassis.mp.t))

class Chassis:
  def __init__(self, m, pos, path, r, w_pos):
    # assert len(propellers_positions) == 2, 'there can only be 2 propellers'
    self.p = pos
    self.path = path
    self.orientation = pi/2
    self.vector = 0,0
    self.mp = m
    self.r = r
    self.propellers = Propeller(self, Vector.add(pos, (-r,0))),Propeller(self, Vector.add(pos, (r,0)))
    self.weight = Weight(pos)
    self.rotateIndex = 0
    self.w_pos = w_pos
    self.wheels = tuple(map(lambda p:Wheel(self, Vector.add(p,self.p), 5, 0), w_pos))
    for w in self.wheels:
      m.addWheel(w)
    self.aPs = tuple(map(lambda w: AttachPoint(self,w,.01),self.wheels))
  def update(self, keys):
    self.propellers[0].power = ((1 if keys[pygame.K_RIGHT] else .75) if keys[pygame.K_UP] else 0)*(2 if keys[pygame.K_LSHIFT] else 1)
    self.propellers[1].power = ((1 if keys[pygame.K_LEFT] else .75) if keys[pygame.K_UP] else 0)*(2 if keys[pygame.K_LSHIFT] else 1)
    for p in self.propellers:
      p.update()
    self.weight.update()
    self.vector = Vector.add(self.vector, self.propellers[0].vector, self.propellers[1].vector, self.weight.vector, *map(lambda a:a.vector, self.aPs))
    self.p = Vector.add(
      Vector.multiply(self.vector, .1),
      Vector.multiply(Vector.add(self.propellers[0].nextpos,self.propellers[1].nextpos,self.weight.nextpos), 1/3)
    )
    oA = asin(-self.propellers[0].power/self.r) + asin(self.propellers[1].power/self.r)
    out1 = tuple(map(lambda p: (Vector.subtract(p.pos, self.p),Vector.subtract(p.nextpos, self.p)), self.aPs))
    out2 = tuple(map(lambda v: (Vector.getNorm(v[0]),Vector.getNorm(v[1])), out1))
    oA += sumTuple(
      tuple(map(
        lambda p,a,b: (
          Triangle.angleFromSides(
            b[0],
            b[1],
            Vector.getNorm(p.vector),
          ) * (-1 if Vector.isOpposite(p.vector, (a[0][1],-a[0][0]))else 1)
        ) if b[0] * b[1] * Vector.getNorm(p.vector) != 0 else 0,
        self.aPs,
        out1,
        out2
      ))
    )/(len(self.w_pos))
    self.rotateIndex += oA
    self.orientation += self.rotateIndex*.1 + oA
    self.propellers[0].pos = Vector.add(self.p, Vector.multiply((sin(self.orientation),cos(self.orientation)),-self.r))
    self.propellers[1].pos = Vector.add(self.p, Vector.multiply((sin(self.orientation),cos(self.orientation)),self.r))
    self.weight.pos = self.p
    ro = sin(self.orientation),cos(self.orientation)
    for aP,p in zip(self.aPs,self.w_pos):
      aP.pos = Vector.add(self.p,Vector.rotate(p,ro))
      aP.update(keys)
    self.vector = Vector.multiply(self.vector, .99)
    self.rotateIndex *= .95
  def draw(self):
    ro = sin(self.orientation),cos(self.orientation)
    for p in self.aPs+self.wheels:
      p.draw()
    for p in self.propellers:
      p.draw()
      pygame.draw.polygon(screen, 0xff, tuple(map(lambda p: Vector.add(self.p,Vector.rotate(p,ro),self.mp.t),self.path)))
      Vector.draw(self.vector, Vector.add(self.p,self.mp.t), 1, 0x00ff00)
