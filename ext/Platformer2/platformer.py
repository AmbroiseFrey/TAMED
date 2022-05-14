from collections.abc import Sequence
import pygame
from math import sqrt, cos, sin, floor, ceil
from copy import copy

resolution = 800,400
mid_screen = tuple(map(lambda i:i*.5, resolution))

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

#---------------- Maths ------------------------#

hypot = lambda *v: sum(map(lambda x:x**2,v))**.5 #function qui permet de trouver l'hypothénus en en fonction des coordonnées d'un point
sort = lambda *a: tuple(sorted(a)) # simlifie les fonctions à venir

def binomialcoefs(n):
    """
        permet de trouver les coéfficients i tels que (a+b)ⁿ = i₀·aⁿ + i₁·aⁿ⁻¹b + ... + iₙ₋₁·abⁿ⁻¹ + iₙ·bⁿ
        par exemple:
            >>> binomialcoefs(2)
            >>> (1,2,1)
                car (a+b)² = 1·a² + 2·ab + 1·b²
    """
    if n == 0: return (1,)
    previous = binomialcoefs(n-1)
    return (1,*map(lambda a,b:a+b, previous[:-1], previous[1:]),1)

def BezierCurve(*pts):
    """
      crée la fonction d'une BezierCurve de dimension `len(pts)`
      (if you don't know what a bezier curve is, go check it out, it's really cool)
    """
    l = len(pts)
    coefs = binomialcoefs(l-1)
    return eval(
        'lambda a:('+','.join(map(
            lambda *p: '+'.join(
                (str(c*t) if c*t!=1 else '')
                + ('' if l==k+1 else '*(1-a)' if l==k+2 else '*(1-a)**'+str(l-k-1))
                + ('' if not k else '*a' if k==1 else '*a**'+str(k))
                for c,t,k in zip(coefs,p,range(l)) if c*t!=0),
            *pts))
        +')'
    )

class Circle:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def intersect(self, circle):
        v = Vector(self.c, circle.c)
        d = v.norm
        if d == 0: return Vector(2), Vector(2)
        x = (self.r ** 2 - circle.r ** 2 + d ** 2) / 2 / d
        if self.r < x:
            print(d, self.r,x)
            return Vector(2), Vector(2)
        h = sqrt(self.r ** 2 - x ** 2)
        v1 = Vector(v).multiply(x / d)
        v2 = v.opposite2D.multiply(h / d)
        return Vector(v1).add(v2,self.c), Vector(v2,v1).add(self.c)

class Vector(Sequence):
    def __init__(self, P, Q=None):
        if Q:
            self.length = min((len(P), len(Q)))
            self.value = tuple(Q[i] - P[i] for i in range(self.length))
        else:
            if type(P) is int:
                self.length = P
                self.value = tuple(0 for i in range(P))
            else:
                self.length = len(P)
                self.value = tuple(P)
        super().__init__()
    def add(self, *v):      return self.map(lambda e,i:e+sum(map(lambda a:a[i],v))) # ajoute plusieurs vecteurs
    def subtract(self, *v): return self.map(lambda e,i:e-sum(map(lambda a:a[i],v))) # soustrait plusieurs veteurs
    def multiply(self, n):  return self.map(lambda e,i:e*n) # multiplie le vecteur 
    def map(self, callback): # comme la fonction `map()` mais pour un vecteur et avec l'index
        self.value = [callback(self[i], i) for i in range(self.length)]
        return self
    def setValue(self, a): self.value = tuple(a) # permet de changer les coordonnées du vecteur sans changer l'objet en lui-même
    def getNorm(self): return hypot(*self.value) # renvoie la norme du vecteur
    def setNorm(self, n): # change la norme du vecteur
        self.multiply(n/self.getNorm())
        return self
    def getOpposite2D(self): return Vector((-self[1], self[0])) # renvoie un vecteur orthogonal 
    def __getitem__(self, i): return self.value[i] # permet de rendre l'objet séquençable
    def __len__(self): return self.length # permet de rendre l'objet séquençable
    def rotate(self, a, origin=(0,0)): # fait une rotation du vecteur 2D
        """for 2D vectors"""
        origin = Vector(origin)
        c,s = (cos(a),sin(a)) if type(a) is float else a
        v = Vector(origin, self.value)
        self.value = origin.add((c*v[0]-s*v[1],c*v[1]+s*v[0]))
        return self
    norm = property(getNorm,setNorm)     # définit des getters et setters pour que ce soit plus simple à utiliser ensuite
    opposite2D = property(getOpposite2D) # définit des getters et setters pour que ce soit plus simple à utiliser ensuite

class MemoryVector(Vector): # vecteur qui se rapelle de sa position initiale
    def __init__(self,*a):
        super().__init__(*a)
        self.initial = copy(self.value)

class Segment:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.v = Vector(p,q)
        self.norm = self.v.norm
        self.equation = Cartesienne(q[1]-p[1], p[0]-q[0], p[0]*q[1]-q[1]*p[0])
        self.interval = tuple(map(sort,p,q))
        self.f = lambda x: self.vec[1]/self.vec[0]*(x-p[0])+p[1] if self.v[0]!=0 else None
    def separate(self, l): # division du segment dans plusieurs cases de taille `l`
        p_pos = tuple(map(lambda x:int(x//l), self.p))
        q_pos = tuple(map(lambda x:int(x//l), self.q))
        p_l,p_r= sort(p_pos,q_pos)
        inter_map = map(lambda x: (x,self.f(x*l)/l),range(p_l[0]+1,p_r[0]+1))
        pts = p_l,*inter_map,p_r
        result = []
        for i in range(1, len(pts)):
            s = sort(pts[i-1][1],pts[i][1])
            result.extend(map(lambda j:(pts[i-1][0],j), range(floor(s[0]),ceil(s[1]))))
        return result

class Cartesienne:
    def __init__(self, *a): # fonction cartésienne de la forme ax + by + c = 0
        self.a,self.b,self.c = a
        self.vecteur_unitaire = -self.b,self.a
        self.vecteur_unitaire = Vector.setToNorm(self.vecteur_unitaire,1)
    def intersect(self, l): # point d'intersection (s'il existe) entre les deux droites 
        c,d,e = l.a,l.b,l.c if type(l) is Cartesienne else l
        a, b = self.a*d,c*self.b
        if (a != b):
            return Vector.multiply((self.b*e-d*self.c, self.a*e-c*self.c), 1/(a-b))
    def distance(self, point): # renvoie la distance minimale du point à la droite
        return abs(self.a*point[0]+self.b*point[1]+self.c)/(self.a**2+self.b**2)**.5
    def closest(self, point): # renvoie le point appartenant à l'équation cartésienne le plus proche du `point` 
        a2, b2, ab = self.a ** 2, self.b ** 2, self.a * self.b
        return (
            (b2 * point[0] - ab * point[1] - self.a * self.c) / (a2 + b2),
            (a2 * point[1] - ab * point[0] - self.b * self.c) / (a2 + b2)
        )

#------------------------------- Map ---------------------------------------------#

class Wall:
    def __init__(self, p, q):
        self.vp = Vector(p,q)
        self.v = self.vP.opposite2D
        self.up = Vector.setNorm(self.vp,1) #vecteur unitaire
        self.u = Vector.setNorm(self.v,1) #vecteur unitaire
        self.equation = Cartesienne(*self.v, -(self.v[0] * p[0] + self.v[1] * p[1]))
        self.p,self.q = p,q
        self.interval = sorted((p[0],q[0])),sorted((p[1],q[1]))
    def collides(self, segment:Segment):
        intersect = self.equation.intersect(segment.equation)
        return False if not intersect or Vector(segment.p, intersect).norm<=segment.norm else intersect
    def draw(self, t:tuple = (0,0), k:float = 1):
        pygame.draw.line(screen, 0, Vector.add(self.p,t), Vector.add(self.q,t), width=1)
    def closeToInterval(self,point, err=.1):
        return self.interval[0][0]-err<point[0]<self.interval[0][1]+err and self.interval[1][0]-err<point[1]<self.interval[1][1]+err

class CaseMatrix:
    def __init__(self, x,y,l):
        self.rect = x,y,x+l,y+l
        self.contains = []
    def add(self, wall:Wall):
        self.contains.append(wall)

class FloorMatrix:
    def __init__(self, x, y, l, relative):
        self.x,self.y,self.l = x,y,l
        self.dim = x,y
        self.data = [[CaseMatrix(i,j,l) for j in range(x)] for i in range(y)]
        self.relative = relative
    def addSegment(self,wall:Wall):
        for i in wall.separate(self).l:
            self.data[i[0]][i[1]].add(wall)
    def display(self):
        pass


#--------------------------------- Robot -------------------------------------------#

gravity = Vector((0,9.81))

class Spring:
    def __init__(self,p,q,distance=None, elasticity=.5, forces=(Vector(2),Vector(2))):
        self.p = p
        self.q = q
        self.d = distance or Vector(p,q).norm
        self.e = elasticity
        self.output = (0,0)
        self.forces = forces
    def update(self):
        v = Vector(self.p,self.q)
        u = Vector(self.q,self.p)
        n = v.norm
        a = (n-self.d)/self.d*self.e
        self.output = (
            v.multiply(a).add(self.forces[1]),
            u.multiply(a).add(self.forces[0])
        )


class Leg:

    def __init__(self, attach:Vector, end:Vector, attract:Vector, femur, tibia, force_applied:Vector, body):
        self.attach = attach
        self.attract = attract
        self.end = Vector(end)
        self.femur = femur
        self.tibia = tibia
        self.maxN = self.tibia+self.femur*.9
        self.circle1 = Circle(self.femur, self.attach)
        self.circle2 = Circle(self.tibia, self.end)
        self.action = None
        self.iteration_count = 0
        self.N_iterations = 10
        self.force_applied = force_applied
        self.reaction_support = Vector(2)
        self.body = body
        self.wished = end
        self.spring = Spring(self.attach,self.end, forces=(self.force_applied, self.reaction_support))

    def update(self):
        self.spring.update()
        self.check_map_interaction
        if self.action:
            if self.iteration_count<self.N_iterations:
                self.iteration_count += 1
                self.end.setValue(self.action(self.iteration_count/self.N_iterations))
            else: self.stop()
        norm = Vector(self.attach,self.end).norm
        if norm>self.maxN or self.force_applied.norm<self.body.weight.norm*.1: self.move()

    def move(self):
        end_lPos = Vector(self.attach).add((0,self.tibia))
        print(self.attach.value, end_lPos.value)
        self.action = BezierCurve(self.end,Vector(self.attach).add(self.middle).multiply(.5), self.wished)
    def stop(self):
        self.action = None
        self.iteration_count = 0

    def display(self):
        pygame.draw.lines(screen, 0, False, tuple(map(lambda e: Vector(e).add(mid_screen),(self.attach,self.middle,self.end))))

    def get_middle(self):
        return min(self.circle1.intersect(self.circle2), key = lambda p: Vector(p,self.attract).norm)
    middle = property(get_middle)

    def get_resultante(self):
        return Vector()

    def check_map_interaction():
        pass



class Robot:

    def __init__(self, width,height, femur, tibia, mass=.01):
        self.width,self.height = width,height
        self.w2,self.h2 = width/2,height/2
        self.direction = Vector((1,0))
        self.rect = tuple(map(MemoryVector,((-self.w2,-self.h2),(self.w2,-self.h2),(self.w2,self.h2),(-self.w2,self.h2))))
        self.center = Vector(2)
        self.atL,self.atR = MemoryVector((-self.w2,0)),MemoryVector((self.w2,0))
        self.arL,self.arR = MemoryVector((-width,0)),MemoryVector((width,0))
        self.wiL,self.wiR = MemoryVector((-self.w2*1.5,tibia)),MemoryVector((self.w2*1.5,tibia))
        self.memoryVecs = self.atL,self.atR,self.arL,self.arR,self.wiL,self.wiR
        self.weight = gravity.multiply(mass)
        self.forceL,self.forceR = Vector(self.weight).multiply(.5),Vector(self.weight).multiply(.5)
        self.leg_L = Leg(self.atL,self.wiL,self.arL,50,50,self.forceL,self)
        self.leg_R = Leg(self.atR,self.wiR,self.arR,50,50,self.forceR,self)

    def update(self, keys):
        if keys[pygame.K_LEFT]:  self.center.add((-5,0))
        if keys[pygame.K_RIGHT]: self.center.add(( 5,0))
        for m in self.memoryVecs: m.setValue(Vector(m.initial).rotate(self.direction).add(self.center))
        d = self.leg_R.end[0]- self.leg_L.end[0]
        x = self.center[0] - self.leg_L.end[0]
        self.forceL.setValue(Vector(self.weight).multiply(1-x/d))
        self.forceR.setValue(Vector(self.weight).multiply(x/d))
        self.leg_L.update()
        self.leg_R.update()

    def change_movement(self):
        FL = self.leg_L.resultante
        FR = self.leg_R.resultante
        npL = Vector(self.atL).add(FL)
        npR = Vector(self.atR).add(FR)


    def display(self):
        pygame.draw.polygon(screen,0xff,tuple(map(lambda e: Vector(self.center).add(e, mid_screen).value, self.rect)))
        self.leg_L.display()
        self.leg_R.display()


def play_game(level = (700,800)):
  
  robot = Robot(50,25,50,50)
  
  RUN = True
  
  while RUN:
      screen.fill(0xffffff)
      keys = pygame.key.get_pressed()
      robot.update(keys)
      robot.display()
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              RUN = False
          
      pygame.display.flip()
      # time.sleep(.1)
      clock.tick(60)
  pygame.quit()