from collections.abc import Sequence
from functools import partial
import pygame, time
from math import sqrt, cos, sin, floor, ceil
from copy import copy
from random import random

resolution = 800,400
mid_screen = tuple(map(lambda i:i*.5, resolution))

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

hypot = lambda *v: sum(map(lambda x:x**2,v))**.5
sort = lambda *a: tuple(sorted(a))

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
    def add(self, *v):      return self.map(lambda e,i:e+sum(map(lambda a:a[i],v)))
    def subtract(self, *v): return self.map(lambda e,i:e-sum(map(lambda a:a[i],v)))
    def multiply(self, n):  return self.map(lambda e,i:e*n)
    def map(self, callback):
        self.value = tuple(callback(self[i], i) for i in range(self.length))
        return self
    def setValue(self, a): self.value = tuple(a)
    def getNorm(self): return hypot(*self.value)
    def setNorm(self, n):
        a = self.getNorm()
        if a!=0: self.multiply(n/a)
        return self
    def getOpposite2D(self): return Vector((self[1], -self[0]))
    def __getitem__(self, i): return self.value[i]
    def __len__(self): return self.length
    def rotate(self, a, origin=(0,0)):
        """for 2D vectors"""
        origin = Vector(origin)
        c,s = (cos(a),sin(a)) if type(a) is float else a
        v = Vector(origin, self.value)
        self.value = origin.add((c*v[0]-s*v[1],c*v[1]+s*v[0]))
        return self
    norm = property(getNorm,setNorm)
    opposite2D = property(getOpposite2D)

class MemoryVector(Vector):
    def __init__(self,*a):
        super().__init__(*a)
        self.initial = copy(self.value)

class MotionPoint(Vector):
    def __init__(self, x, y=None):
        print(x,y)
        super().__init__((x, y) if y or y == 0 else x)
        self.forces = Vector(2)
        self.inertia = Vector(2)
        self.forcesList = []
    def apply(self):
        self.inertia.multiply(.95).add(self.forces, *self.forcesList)
        self.forces.setValue((0, 0))
        self.add(self.inertia)

class Segment:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.v = Vector(p,q)
        self.norm =self.v.norm
        self.equation = Cartesienne(q[1]-p[1], p[0]-q[0], p[0]*q[1]-q[1]*p[0])
        self.interval = tuple(map(sort,p,q))
        self.f = lambda x: self.v[1]/self.v[0]*(x-p[0])+q[1] if self.v[0]!=0 else None
    def separate(self, l):
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
    def __init__(self, *a):
        self.a,self.b,self.c = a
        self.vecteur_unitaire = Vector((-self.b,self.a)).setNorm(1)
    def intersect(self, l):
        c,d,e = l.a,l.b,l.c if type(l) is Cartesienne else l
        a, b = self.a*d,c*self.b
        if (a != b):
            return Vector.multiply((self.b*e-d*self.c, self.a*e-c*self.c), 1/(a-b))
    def distance(self, point):
        return abs(self.a*point[0]+self.b*point[1]+self.c)/(self.a**2+self.b**2)**.5
    def closest(self, point):
        a2, b2, ab = self.a ** 2, self.b ** 2, self.a * self.b
        return (
            (b2 * point[0] - ab * point[1] - self.a * self.c) / (a2 + b2),
            (a2 * point[1] - ab * point[0] - self.b * self.c) / (a2 + b2)
        )

#----------------------------------------------------------------------------#

class Wall(Segment):
    def __init__(self, p, q):
        super().__init__(p,q)
        self.vp = Vector(p,q)
        self.v = self.vp.opposite2D
        self.up = Vector(self.vp).setNorm(1)
        self.u = Vector(self.v).setNorm(1)
        self.p,self.q = p,q
        self.interval = sorted((p[0],q[0])),sorted((p[1],q[1]))
    def collides(self, segment:Segment):
        intersect = self.equation.intersect(segment.equation)
        return False if not intersect or Vector(segment.p, intersect).norm<=segment.norm else intersect
    def draw(self, t:tuple = (0,0), k:float = 1):
        pygame.draw.line(screen, 0, Vector(self.p).add(t), Vector(self.q).add(t), width=1)
    def closeToInterval(self,point, err=.1):
        return self.interval[0][0]-err<point[0]<self.interval[0][1]+err and self.interval[1][0]-err<point[1]<self.interval[1][1]+err

class CaseMatrix:
    def __init__(self, x,y,l):
        self.rect = x,y,x+l,y+l
        self.contains = []
    def add(self, wall:Wall):
        self.contains.append(wall)

class FloorMatrix:
    def __init__(self, x, y, l, relative, image_url):
        self.x,self.y,self.l = x,y,l
        self.dim = x,y
        self.data = [[CaseMatrix(i,j,l) for j in range(x)] for i in range(y)]
        self.relative = relative
        self.image = pygame.transform.scale(pygame.image.load(image_url), tuple(map(lambda e:int(e*self.l), self.dim)))
    def addSegment(self,wall:Wall):
        for i in wall.separate(self.l):
            self.data[i[0]][i[1]].add(wall)
    def display(self):
        a = Vector((max(self.relative[0]-mid_screen[0],0),max(self.relative[1]-mid_screen[1],0)))
        b = Vector((min(self.relative[0]+mid_screen[0],self.x*self.l),min(self.relative[1]+mid_screen[1],self.y*self.l))).add(a)
        c = Vector(a).add(mid_screen).subtract(self.relative)
        screen.blit(self.image, c.value+Vector(c,resolution).value,(*a,*b))



#----------------------------------------------------------------------------#

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
    def __init__(self, femur, tibia, d, direction=1, relative=Vector(2)):
        self.max = (femur + tibia) * .99
        self.min = (femur + tibia) * .2
        self.changeD(d)
        self.hanche = Vector(2)
        self.pied = Vector((self.maxdeviation*.5, self.d))
        self.direction = direction
        self.genou = Vector(Circle(femur, self.hanche).intersect(Circle(tibia, self.pied))[direction])
        self.index = 0
        self.theoryPied = Vector((self.maxdeviation / 2, self.d))
        self.phase1 = 1
        self.phase2 = .5
        self.allphase = self.phase1+self.phase2
        self.femur = femur
        self.tibia = tibia
        self.relative = relative
        self.push = Vector(2)
        self.color = floor(random()*0xffffff)
    def display(self):
        pygame.draw.lines(screen, 0, False, tuple(map(lambda e: Vector(e).add(self.relative),(self.hanche, self.genou, self.pied))), 5)
    def update(self):
        while self.index < 0: self.index += self.allphase
        while self.index > self.allphase: self.index -= self.allphase
        if self.index < self.phase1:
            self.theoryPied = Vector([((1.5 if self.direction == 0 else .5) - self.index/self.phase1 * 2) * self.maxdeviation / 2, self.d])
        else:
            self.theoryPied = self.retour((self.index-self.phase1)/self.phase2)
        self.theoryGenou = Vector(Circle(self.femur, self.hanche).intersect(Circle(self.tibia, self.theoryPied))[self.direction])
        self.pied.setValue(self.theoryPied)
        self.genou.setValue(self.theoryGenou)
        self.display()
    def retour(self, a): return Vector((
        (2*a**2+2*a-1 if self.direction==0 else -2*a**2+6*a-3)/4*self.maxdeviation,
        (1+a**2-a)*self.d))
    def changeD(self, d):
        self.d = max(min(d,self.max*.95),self.min)
        self.maxdeviation =  sqrt(self.max**2 - self.d**2)


class Robot:
    def __init__(self, width,height, femur, tibia, center=Vector(2), d=None, mass=.5):
        self.d = tibia+femur/4
        self.width,self.height = width,height
        self.w2,self.h2 = width/2,height/2
        self.direction = Vector((1,0))
        self.rect = tuple(map(MemoryVector,((-self.w2,-self.h2),(self.w2,-self.h2),(self.w2,self.h2),(-self.w2,self.h2))))
        self.center = center
        self.weight = Vector(gravity).multiply(mass)
        self.A = MotionPoint(self.w2,0)
        self.B = MotionPoint(-self.w2,0)
        self.legs = (
            Leg(femur,tibia,self.d, 0, Vector(self.center).add(self.A, mid_screen)),
            Leg(femur,tibia,self.d, 0, Vector(self.center).add(self.A, mid_screen)),
            Leg(femur,tibia,self.d, 1, Vector(self.center).add(self.B, mid_screen)),
            Leg(femur,tibia,self.d, 1, Vector(self.center).add(self.B, mid_screen))
        )
        self.legs[1].index = self.legs[1].allphase/2
        self.legs[3].index = self.legs[3].allphase/2
        self.spring = Spring(self.A,self.B)
    def update(self, keys):
        if keys[pygame.K_RIGHT]:
            for leg in self.legs: leg.index+=.1
        if keys[pygame.K_LEFT]:
            for leg in self.legs: leg.index-=.1
        if keys[pygame.K_UP]:
            for leg in self.legs: leg.changeD(leg.d+1)
        if keys[pygame.K_DOWN]:
            for leg in self.legs: leg.changeD(leg.d-1)
        for leg in self.legs: leg.update()
        # self.change_movement()
    def change_movement(self):
        FL = self.leg_L.resultante
        FR = self.leg_R.resultante
        npL = Vector(self.atL).add(FL)
        npR = Vector(self.atR).add(FR)
        self.center.add(self.weight)
        # print(npL.add(npR).value)

    def display(self):
        pygame.draw.polygon(screen,0xff,tuple(map(lambda e: Vector(self.center).add(e, mid_screen).value, self.rect)))


def play_game(level = (700,800)):
  # robot = Robot(50,25,50,50)
  # floorM = FloorMatrix(40,20,20, robot.center, 'random_background.png')
  # robot.map = floorM
  # with open('data.txt') as f:
  #     values = tuple(map(lambda x : tuple(map(int, x.split(','))),f.readlines()[0].split(' ')))
  # for group in values:
  #     pts = tuple((group[i],group[i+1]) for i in range(len(group)//2))
  #     for A,B in zip(pts,pts[1:]+(pts[0],)):
  #         wall = Wall(A,B)
  #         floorM.addSegment(wall)
  # leg = Leg(40,50,60, 0, Vector(mid_screen).add((20,0)))
  # leg2 = Leg(40,50,60, 1, Vector(mid_screen).add((-20,0)))
  # leg3 = Leg(40,50,60, 0, Vector(mid_screen).add((20,0)))
  # leg4 = Leg(40,50,60, 1, Vector(mid_screen).add((-20,0)))
  # leg3.index = leg3.allphase/2
  # leg4.index = leg4.allphase/2
  robot = Robot(70,25, 40,50)
  RUN = True
  
  while RUN:
      screen.fill(0xffffff)
      keys = pygame.key.get_pressed()
      robot.update(keys)
      # floorM.display()
      robot.display()
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              RUN = False
      pygame.display.flip()
      time.sleep(.1)
      clock.tick(60)
  pygame.quit()