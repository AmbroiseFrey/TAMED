import pygame
from ext.Platformer.plat_variables import screen, resolution
from math import pi, acos, asin, cos, sin

def sumTuple(t, callback = lambda x : x):
    S = type(tuple(t)[0])()
    for i in t:
        S += callback(i)
    return S
    
def polynomial(a, b, c):
    Delta = b ** 2 - 4 * a * c
    if (Delta < 0): return ()
    if (Delta == 0): return -b / a / 2,
    Dsqrt = Delta**.5
    return -(Dsqrt + b) / a / 2, (Dsqrt - b) / a / 2,

def mp(itera, callback=lambda x,i:x):
    return tuple(callback(itera[i],i) for i in range(len(itera)))

def hypot(*v):
    return sumTuple(v, lambda x : x ** 2) ** .5

def removeDoublons(itera):
    def getBool(j,e):
        for k in range(j):
            if itera[k][0] == e[0] and itera[k][1] == e[1]:
                return False
        return True
    return tuple(itera[i] for i in range(len(itera)) if getBool(i, itera[i]))

class Vector:
    @classmethod
    def add(cl,*v):
        return tuple(map(lambda *a: sumTuple(a), *v))
    @classmethod
    def subtract(cl,v, u):
        return v[0]-u[0],v[1]-u[1] 
    @classmethod
    def multiply(cl,v, n):
        return v[0]*n,v[1]*n
    @classmethod
    def Vmul(cl,v,u):
        return v[0]*u[0],v[1]*u[1]
    @classmethod
    def isOpposite(cl,v, u, m = 0): 
        return sumTuple(Vector.add(v, u), lambda x : x ** 2) < sumTuple(v, lambda x : x ** 2) + sumTuple(u, lambda x : x ** 2) + m 
    @classmethod
    def getNorm(cl,v): 
        return hypot(v[0], v[1])
    @classmethod
    def setToNorm(cl,v, s):
        n = Vector.getNorm(v)
        s = 0 if n == 0 else s/n
        return Vector.multiply(v,s)
    @classmethod
    def getAngle(cl, v):
        return acos(v[0]/Vector.getNorm(v)) if v[1]<0 else -acos(v[0]/Vector.getNorm(v))
    @classmethod 
    def rotate(cl, v, u, trigo = True):
        if type(u) is float: u = cos(u),sin(u)
        coef = 1 if trigo else -1
        return u[0]*v[0]-u[1]*v[1]*coef, u[0]*v[1]+u[1]*v[0]*coef
    @classmethod
    def draw(cl,v,p,w=.5,c=0x000000):
        q = Vector.add(p,v)
        pygame.draw.line(screen, c, p, q, int(w))
        u = Vector.setToNorm(v, 1)
        pts = (
            Vector.add(Vector.multiply(u,w*1.5),q), 
            Vector.add(Vector.multiply((-(u[0]+u[1]),u[0]-u[1]), w*1.25),q),
            Vector.add(Vector.multiply((u[1]-u[0],-(u[0]+u[1])), w*1.25),q)
        )
        pygame.draw.polygon(screen, c, pts)


class Point(Vector):
    @classmethod
    def distance(cl, p, q):
        return hypot(p[0] - q[0], p[1] - q[1]) 
    @classmethod
    def translate(cl, p, v):
        return Vector.add(p, v)
    @classmethod
    def homothetia(cl, p, n, rel=(0,0)):
        return Vector.add(Vector.multiply(Vector.subtract(p,rel),n),rel)
    @classmethod
    def rotate(cl, p, r:float, rel=(0,0)):
        p = Vector.subtract(p,rel)
        c,s = cos(r),sin(r)
        return Vector.add((c*p[0]+s*p[1],c*p[1]-s*p[0]),rel)


class Droite:
    @classmethod
    def Point_Vector(cl, p, v):
        return Droite(v[1], -v[0], v[0] * p[1] - v[1] * p[0])
    @classmethod
    def Point_Point(cl, p, q): 
        return Droite(q[1] - p[1], p[0] - q[0], q[0] * p[1] - q[1] * p[0])
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c 
    def intersection(self, l):
        if type(l) is Droite:
            c,d,e = l.a,l.b,l.c
        else: c,d,e = l
        a, b = self.a * d, c * self.b
        if (a != b):
            x = (self.b * e - d * self.c) / (a - b)
            y = (self.a * e - c * self.c) / (b - a)
            return x, y
    def PV_intersection(self, P, v):
        b = self.a * v[0] + self.b * v[1]
        if (b):
            a = v[1] * P[0] - v[0] * P[1]
            return (
                (a * self.b - self.c * v[0]) / b, 
                (-a * self.a - self.c * v[1]) / b
            )
    def closest(self, point):
        a2, b2, ab = self.a ** 2, self.b ** 2, self.a * self.b
        return (
            (b2 * point[0] - ab * point[1] - self.a * self.c) / (a2 + b2),
            (a2 * point[1] - ab * point[0] - self.b * self.c) / (a2 + b2)
        )
    def distance(self, point):
        return abs(self.a*point[0]+self.b*point[1]+self.c)/(self.a**2+self.b**2)**.5
    def translate(self, t = (0,0)): 
        self.c -= t[0] * self.a + t[1] * self.b 
    def homothetia(self, k): 
        self.c *= k
    def draw(self, color=0,w=1):
        i = (self.intersection((0, -1, 0)),
            self.intersection((1, 0, 0)),
            self.intersection((0, -1, resolution[0])),
            self.intersection((1, 0, -resolution[1]))
            )
        i = tuple(j for j in i if j and j[0] >= 0 and j[1] >= 0 and j[0] <= resolution[0] and j[1] <= resolution[1])
        d=removeDoublons(i)
        if len(d)==2:
            pygame.draw.line(screen, color, d[0],d[1], w)

class Circle:
    def __init__(self, point, radius):
        self.a = point[0]
        self.b = point[1]
        self.c = radius
    def intersectionLine(self, line: Droite):
        return mp(polynomial(
            line.a ** 2 + line.b ** 2,
            2 * (line.b * line.c - line.a ** 2 * self.b),
            -(line.a ** 2) * (self.c ** 2 - self.b ** 2 - self.a ** 2) + 2 * line.a * self.a * (line.b + line.c) + line.c ** 2
        ), lambda y,i: Droite(0, 1, -y).intersection(line))
    def homothetia(self, k):
        self.a *= k
        self.b *= k
        self.c *= k
        
class Segment:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        q = Vector.add(self.p,self.v)
        self.line = Droite(-v[1],v[0],v[1]*p[0]-v[0]*p[1])
        self.interval = (sorted((p[0],q[0])),sorted((p[1],q[1])))
    def translate(self, t:tuple):
        self.p = Vector.add(self.p, t)
        self.line.translate(t)
        self.interval = tuple(tuple(self.interval[i][j]+t[i] for j in (0,1)) for j in (0,1))
    def getSize(self):
        return Vector.getNorm(self.v)
    def getQ(self):
        return Vector.add(self.p,self.v)

class Force:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.line = Droite(-v[1],v[0],v[1]*p[0]-v[0]*p[1])
        self.nextPos = Vector.add(p,v)
    # def translate(self, t:tuple):
    #     self.p = Vector.add(self.p, t)
    #     self.line.translate(t)
    # def getSize(self):
    #     return Vector.getNorm(self.v)
    # def update(self):
    #     self.nextPos = Vector.add(self.p,self.v)
        
class Interval:
    @classmethod
    def union(cl, i1,i2): # si i1 et i2 sont des intervalles continus
        if i2[0]<i1[0]: i1,i2 = i2,i1
        if i1[1]>i2[1]: return i1
        if i1[1]>i2[0]: return (i1[0],i2[1])
        return (i1,i2) # intervalle non continu
    @classmethod
    def intersects(cl, i1,i2):
        # print(i1,i2)
        if type(i1[0]) is int or type(i1[0]) is float:
            return i1[0]<=i2[1] and i1[1]>=i2[0]
        else:
            if Interval.intersects(i1[0],i2[0]) and Interval.intersects(i1[1],i2[1]):
                return True
            return False

class Triangle:
    @classmethod
    def angleFromSides(cl, a1,a2,o):
        return acos(min(max((a1**2+a2**2-o**2)/(2*a1*a2),-1),1))