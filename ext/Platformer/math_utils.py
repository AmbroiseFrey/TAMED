import pygame
from ext.Platformer.plat_variables import screen, resolution

def sumTuple(t, callback = lambda x : x):
    S = 0
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
    def isOpposite(cl,v, u, m = -.01): 
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
    def draw(cl,v,p,w=.5,c=0x000000):
        # pygame.draw.line(screen, c, p, Vector.add(p,v), w)
        pass


class Point(Vector):
    @classmethod
    def distance(cl, p, q):
        return hypot(p[0] - q[0], p[1] - q[1]) 
    @classmethod
    def translate(cl, p, v):
        return Vector.add(p, v)


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