import pygame
from ext.Core import operations as Opr
from ext.Core import variables as varia
from ext.Platformer.math_utils import hypot, mp, sumTuple, Vector, Point, Droite, Circle
from math import floor, pi
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
        pygame.draw.circle(screen, c, Vector.add(Vector.subtract(p1,self.relative),self.center), Vector.add(Vector.subtract(p2,self.relative),self.center), r)
    def drawLineLine(self, l):
        drt = Droite(l[0],l[1],l[2] * self.l)
        drt.translate((-50, -50))
        drt.draw(self.view)
    def drawVector(self, vector, point, w=.5, c=0x000000):
        Vector.draw(vector, Vector.add(Vector.subtract(point,self.relative),self.center),w,c)

class Chassis:
    def __init__(self, pos, size: tuple):
        self.pos = pos
        self.size = size # (largeur [x], hauteur [y])
        self.vector = [0, 0]
        self.weight = [0, .1]
        self.forces = [self.weight]

    def update(self):
        pass
    def addForce(self, force):
        self.forces.append(force)
    def display(self):
        pass

class Propeller:
    def __init__(self, chassis, pos, el):
        self.power = 0
        self.chassis = chassis
        self.force = [0, 0]
        self.pos = pos
        self.el = el

class Wheel:
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r
        self.vector = [0, 0]
        self.weight = [0, .1]
        self.rotate = 0
        self.powerIndex = .97
        self.decuplation = 9
        self.map = None
        self.element = None
        self.bounce = .9
        self.forces = [self.weight]
    def update(self):
        for f in self.forces:
            self.vector = Vector.add(self.vector, f)
        point = self.pos
        vector = self.vector
        self.drawVec()
        size = Vector.getNorm(self.vector)
        Size = size
        mp = self.map
        index = 0
        while (True and index < 3):
            # on récupère les cases sur lesquelles se trouve la roue
            cases = tuple(c for c in mp.vectorCases(point, vector) if self.map.withinMap(c))
            droite = Droite.Point_Vector(Vector.multiply(point, 1 / self.map.l), vector)# on définit l'objet droite qui permettra de trouver les intersections avec les droites des murs
            murs = () # variable ou l'on stocke tous les murs
            for c in cases: # on ajoute les murs sur lesquelles il y a une intersection
                a = tuple(
                    (mur, droite.intersection(mur.line)) 
                    for mur in self.map.readMatrixCase(c, self.r) if Vector.isOpposite(vector, mur.vector)
                )
                a = tuple(
                    (mur[0],mur[1],Point.distance(Vector.multiply(point, 1 / self.map.l), mur[1]))
                    for mur in a if mur[1]
                )
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

            keys = pygame.key.get_pressed()
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
    def display(self):
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
        