import pygame, time
from ext.Platformer.math_utils import hypot, mp, sumTuple, Vector, Point, Droite, Circle, Segment, Force, Interval, Triangle
from math import floor, pi, asin, sin, cos, log
from ext.Platformer.plat_variables import screen, resolution, mid_screen, mi

vectors = []

def every(itera, callback=lambda x,i:True):
    for i in range(len(itera)):
        if not callback(itera[i],i):
            return False
    return True

def getOffsetVector(v,u,v_n,u_n):
    i = v[0]*u[1]-v[1]*u[0]
    return (v[0]*u_n - u[0]*v_n)/i, (v[1]*u_n - u[1]*v_n)/i

def removeDoublons(l):
    return tuple(l[i] for i in range(len(l)) if l.index(l[i]) == i)


class Block:
    class Radius:
        def __init__(self, lines, circles):
            self.lines = lines # du type Wall.Line
            self.circles = circles   # du type Wall.Circle
            self.walls= (*lines,*circles)
            self.arranged = ( # might be useful to make the getwithinWalls method faster
                sorted(self.walls, key=lambda e: e.interval[0][0]), #left
                sorted(self.walls, key=lambda e: e.interval[0][1]), #right
                sorted(self.walls, key=lambda e: e.interval[1][0]), #top
                sorted(self.walls, key=lambda e: e.interval[1][1])  #bottom
            )
            self.interval= (
                (self.arranged[0][0].interval[0][0],self.arranged[1][-1].interval[0][1]),
                (self.arranged[2][0].interval[1][0],self.arranged[3][-1].interval[1][1])
            )
        def getwithinWalls(self, segment:Segment):
            if not Interval.intersects(self.interval, segment.interval): return ()
            return tuple(w for w in self.lines if Vector.isOpposite(w.v, segment.v))+tuple(w for w in self.circles if Vector.isOpposite(Vector.subtract(segment.p,w.p),segment.v) and Interval.intersects(w.interval, segment.interval))
    def __init__(self,points):
        assert len(points)>2, "les blocks ne peuvent pas être des lines ou des points"
        self.points = points
        self.lineWalls = tuple(Wall.Line(points[i-1],points[i]) for i in range(len(points)))
        checkhole = False
        self.pointWalls = tuple(Wall.Circle(points[i],0) for i in range(len(points)) if not Vector.isOpposite(self.lineWalls[i].vp,Vector.subtract(self.lineWalls[(i+1)%len(points)].v,self.lineWalls[i].v)))
    def elab_walls(self,r:float):
        lines = mp(self.lineWalls, lambda w,j: w.radiusApplyWall(r))
        for i in range(len(self.points)):
            lines+=(Wall.Line(lines[i-1].q, lines[i].p),)
        circles = mp(self.pointWalls, lambda w,j: w.radiusApplyWall(r))
        return Block.Radius(lines,circles)
    def draw(self, t:tuple=(0,0), k:float=1):
        pygame.draw.polygon(screen, 0xaaaaaa, mp(self.points, lambda p,i: Vector.add(p,t)))

class Wall:
    class Line:
        def __init__(self, p, q):
            self.v = p[1]-q[1], q[0]-p[0]
            self.vp = Vector.subtract(q,p)
            self.line = Droite(*self.v, -(self.v[0] * p[0] + self.v[1] * p[1]))
            self.p = p
            self.q = q
            self.interval = sorted((p[0],q[0])),sorted((p[1],q[1]))
            self.u = Vector.setToNorm(self.v,1) #vecteur unitaire
            self.up = Vector.setToNorm(self.vp,1) #vecteur unitaire
        def radiusApplyWall(self, r:float):
            v = Vector.multiply(self.u,r)
            return Wall.Line(Vector.add(self.p, v), Vector.add(self.q, v))
        def collides(self, segment:Segment):
            intersect = self.line.intersection(segment.line)
            return segment.p if not intersect else intersect if Point.distance(segment.p, intersect)<=segment.getSize() else False
        def bounce(self, segment:Segment, intersect, bounciness=1):
            q = segment.getQ()
            dist = self.line.distance(q)
            # print('dist',dist)
            npos = Vector.add(q, Vector.multiply(self.u, dist*(1+bounciness)))
            k,l = Vector.multiply(((self.up[0]*segment.v[0]+self.up[1]*segment.v[1]),(self.up[1]*segment.v[0]-self.up[0]*segment.v[1])), self.up[0]**2+self.up[1]**2)
            return (
                npos,
                Vector.subtract(Vector.multiply(self.up,k*bounciness),Vector.multiply((self.up[1],-self.up[0]), l*bounciness)),
                self.up,
                self.u,
                k,l
            )
            # return (npos, Vector.setToNorm(Vector.subtract(npos,intersect), Vector.getNorm(segment.v)*bounciness), self.up, self.vp)
        def draw(self, t:tuple = (0,0), k:float = 1):
            pygame.draw.line(screen, 0, Vector.add(self.p,t), Vector.add(self.q,t), width=1)
        def closeToInterval(self,point, err=.1):
            return self.interval[0][0]-err<point[0]<self.interval[0][1]+err and self.interval[1][0]-err<point[1]<self.interval[1][1]+err
    class Circle:
        def __init__(self, p, r:float):
            self.p = p
            self.r = r
            self.circle = Circle(p,r)
            self.interval = (p[0]-r,p[0]+r),((p[1]-r,p[1]+r))
        def radiusApplyWall(self, r:float):
            return Wall.Circle(self.p, self.r+r)
        def collides(self, segment:Segment):
            intersect = mp(self.circle.intersectionLine(segment.line), lambda p,i: (p,Point.distance(p,segment.p)))
            if len(intersect) == 0: return None
            intersect = min(intersect, key= lambda x:x[1])
            return intersect[0] if intersect[1]<=segment.getSize() else False
        def bounce(self, segment:Segment, intersect, bounciness=1):
            v = Vector.multiply(Vector.subtract(intersect, self.p),1/self.r)
            u = v[1],-v[0]
            drt = Droite(*v, -v[0]*intersect[0]-v[1]*intersect[1])
            q = segment.getQ()
            print('error here?')
            dist = drt.distance(q)
            npos = Vector.add(q, Vector.multiply(v, dist*(1+bounciness)))
            k,l = Vector.multiply(((u[0]*segment.v[0]+u[1]*segment.v[1]),(u[1]*segment.v[0]-u[0]*segment.v[1])), u[0]**2+u[1]**2)
            return (
                npos,
                Vector.subtract(Vector.multiply(u,k*bounciness),Vector.multiply((u[1],-u[0]), l*bounciness)),
                u,
                v,
                k,l
            )
        def draw(self, t:tuple = (0,0), k:float = 1):
            pygame.draw.circle(screen, 0, Vector.add(self.p,t), self.r)
        def closeToInterval(self,point, err=.01):
            return self.interval[0][0]-err>point[0]>self.interval[0][1]+err and self.interval[1][0]-err>point[1]>self.interval[1][1]+err


class Wheel:
    def __init__(self, chassis, pos, r:float, bounciness:float=.1):
        self.bounciness = bounciness
        self.chassis = chassis
        self.pos = pos
        self.weight = Force(pos, (0,.01))
        self.forces = [self.weight]
        self.vector = 0,0
        self.nextPos = pos
        self.r = r
        self.bounciness = .5
    def update(self, leftArrow, rightArrow):
        seg = self.getSegment()
        self.vector = Vector.add(self.vector, *mp(self.forces, lambda f,i: f.v))
        self.pos = Vector.add(self.pos, self.vector)
        walls = self.chassis.mp.getWithinWalls(self)
        walls1 = tuple((w.collides(seg), w) for w in walls)
        walls2 = tuple(w for w in walls1 if w[0] and w[1].closeToInterval(w[0]))
        if len(walls2)>0:
            for w in sorted(walls2, key= lambda w: w[0]):
                data = w[1].bounce(seg,w[0], self.bounciness)
                if Vector.isOpposite(Vector.add(self.weight.v, data[1]), data[3]):
                    print('entered')
                    self.vector = Vector.multiply(data[2],data[4])
                    self.pos = Vector.add(Vector.subtract(w[0],Vector.multiply(data[3],-.0005)),self.vector)
                else:
                    self.pos = data[0] # ou w[0], ça rend plus joli mais ça ne marche pas (pas encore)
                    self.vector = data[1]
                self.vector = Vector.add(self.vector, Vector.multiply(data[2], (leftArrow-rightArrow)))
        self.vector = Vector.multiply(self.vector,.99)
    def addForce(self, force):
        self.forces.append(force)
    def display(self, t:tuple=(0,0), k:float=1):
        pygame.draw.circle(screen, 0, Vector.add(self.pos,t), self.r, 0xff0000)
        # Vector.draw(self.vector, mid_screen, 0, 1)
    def drawVec(self, t:tuple=(0,0), k:float=1):
        Vector.draw(Vector.multiply(self.vector,k*5), Vector.add(Vector.multiply(self.pos,k),t),.1*k,0x00ff00)
    def getSegment(self):
        return Segment(self.pos, self.vector)


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
        if h == 0: return
        s = (h-self.dist)/2 * self.elas/h
        a *= s
        b *= s
        self.v1[0] = -a
        self.v1[1] = -b
        self.v2[0] = a
        self.v2[1] = b
    def display(self, carte=None, color=0, width=1):
        if carte:
            a,b = mp((self.p.pos,self.q.pos), lambda e,i : Vector.subtract(Vector.add(Vector.multiply(e, carte.l), carte.relative), carte.center))
            pygame.draw.line(screen, color, a,b, width)
        else: pygame.draw.line(screen, color, self.p.pos, self.q.pos, width)

# class Chassis:
#     def __init__(self, position, path, wheels_pos, wheels_rad, spring_elas=.5):
#         self.pos = position
#         self.path = path
#         self.w_p = wheels_pos
#         self.w_dist = mp(wheels_pos, lambda p,i: sumTuple(p,lambda x:x*x)**.5)
#         self.wheels = mp(wheels_pos, lambda p,i: Wheel(p,wheels_rad))
#         self.springs = tuple(map(lambda p,q: Ressort(p,q,spring_elas,0)))
#         self.weight = Force((0,1),self.pos)
#         self.vector = 0,0
#         self.orientation = 0
#         self.rotationIndex = 0
#     def update(self, carte, leftArrow, rightArrow):
#         for w in self.wheels:
#             w.update()
#         w_pos = mp(self.w_p, lambda p,i: Vector.add(Point.rotate(p, self.orientation),self.pos))
#         forces = ((self.pos, self.weight),) + tuple(map(lambda s,p: (p,s.v1), self.springs, w_pos))
#         self.pos = Vector.add(
#             Vector.multiply(self.vector,.1),
#             Vector.multiply(Vector.add(self.weight.nextPos,*map(lambda w: w.nextPos, self.wheels),1/(len(self.wheels)+1)))
#         )
#         self.weight.p = self.pos
#         r_offset = mp(self.wheels, lambda w,i: Vector.getAngle(Vector.subtract(w.nextPos, self.pos)) - Vector.getAngle(Vector.subtract(w.pos, self.pos)))
#         self.rotateIndex += r_offset
#         self.orientation += self.rotateIndex * .1 + r_offset
#         self.vector = Vector.multiply(self.vector, .99)
#         self.rotationIndex *= .95
#     def display(self):
#         pts = mp(self.path, lambda p,i: Point.rotate(p,self.orientation))
#         pygame.draw.polygon(screen, 0, pts)
#         for w in self.wheels:
#             w.display()


class Carte:
    types = (
        (0, 0x888888),
        (.75, 0x00ffff)
    )
    def __init__(self, data, dimensions, tileSize, images:dict={}, centerPosition = mid_screen):
        self.matrix = tuple(tuple([] for j in range(dimensions[0]))for i in range(dimensions[1]))
        self.images = images
        self.points = ()
        self.blocks = ()
        self.wheels = ()
        self.chassis = ()
        for d in data:
            l = len(d)//2
            assert l>2, "an error overcome in the building of the map"
            nPts = tuple(
                Vector.multiply((d[i*2],d[i*2+1]),tileSize) for i in range(l)
            )
            self.points += (nPts,)
            if l>2:
                self.blocks += (Block(nPts),)
        self.radBlocks = {}
        self.l = tileSize
        self.center = centerPosition
        self.relative = 0,0
    def getWithinWalls(self, wheel:Wheel):
        seg = wheel.getSegment()
        return sumTuple(tuple(b.getwithinWalls(seg) for b in self.radBlocks[wheel.r]))
    def insert_wheel(self, wheel:Wheel):
        if wheel.r not in self.radBlocks.keys():
            self.radBlocks[wheel.r] = mp(self.blocks, lambda b,i: b.elab_walls(wheel.r))
        self.wheels += (wheel,)
    def insert_chassis(self, chassis):
        if chassis.w_r not in self.radBlocks.keys():
            self.radBlocks[chassis.w_r] = mp(self.blocks, lambda b,i: b.elab_walls(chassis.w_r))
        self.chassis += (chassis,)
    def update(self):
        keys = pygame.key.get_pressed()
        for a in self.wheels:
            a.update(self, keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
        for a in self.chassis:
            a.update(keys)
    def draw(self):
        screen.fill(0xffffff)
        self.t = Vector.subtract(self.center,self.relative)
        #for i in self.images[0]:
        #    pos = Vector.add(Vector.multiply(self.t, 1/i), self.images[i][1])
        #    screen.blit(self.images[i][0], pos + self.images[i][2])
        for b in self.blocks:
            b.draw(self.t, self.l)
        for w in self.wheels:
            w.display(self.t, self.l)
            w.drawVec(self.t, self.l)
        for c in self.chassis:
            c.draw()

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
        pygame.draw.line(screen, 0xffff, Vector.add(self.pos,self.chassis.mp.t), Vector.add(self.pos,self.chassis.mp.t, Vector.multiply(self.vector,-10*self.power**.5)), 3)

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
        self.vector = self.wheel.weight.v
        self.nextpos = self.pos
    def update(self, keys):
        self.wheel.update(keys[pygame.K_LEFT],keys[pygame.K_RIGHT])
        v = Vector.subtract(self.wheel.pos, self.pos)
        h = log(Vector.getNorm(v))
        s = log(h)*self.elas if h>1 else 0
        if s < 10:
            self.wheel.vector = Vector.add(self.wheel.vector, Vector.multiply(v, -s))
            self.vector = Vector.multiply(v, s)
        else: #pour éviter les erreurs
            pygame.quit()
            self.wheel.vector = 0,0
            self.vector = 0,0
            self.wheel.pos = self.pos
        self.nextpos = Vector.add(self.pos,self.vector)
    def draw(self):
        pass
        # pygame.draw.circle(screen, 0xffff00, Vector.add(self.pos, self.chassis.mp.t), 1)
        # pygame.draw.line(screen, 0xffaa00, Vector.add(self.pos, self.chassis.mp.t), Vector.add(self.wheel.pos, self.chassis.mp.t))

class Chassis:
    def __init__(self, mp:Carte, pos, path, r, w_pos, w_r=5):
        # assert len(propellers_positions) == 2, 'there can only be 2 propellers'
        self.p = pos
        self.path = path
        self.orientation = pi/2
        self.vector = 0,0
        self.mp = mp
        self.r = r
        self.w_r = w_r
        self.propellers = Propeller(self, Vector.add(pos, (-r,0))),Propeller(self, Vector.add(pos, (r,0)))
        self.weight = Weight(pos)
        self.rotateIndex = 0
        self.w_pos = w_pos
        self.wheels = tuple(map(lambda p:Wheel(self, Vector.add(p,self.p), w_r, 0), w_pos))
        self.aPs = tuple(map(lambda w: AttachPoint(self,w,.01),self.wheels))
        mp.insert_chassis(self)
    def update(self, keys):
        self.propellers[0].power = ((1 if keys[pygame.K_RIGHT] else .75) if keys[pygame.K_UP] else 0)*(2 if keys[pygame.K_LSHIFT] else 1)
        self.propellers[1].power = ((1 if keys[pygame.K_LEFT] else .75) if keys[pygame.K_UP] else 0)*(2 if keys[pygame.K_LSHIFT] else 1)
        for p in self.propellers:
            p.update()
        self.weight.update()
        # print(type(self.vector))
        # for i in (0,1):
        #     print(type(self.propellers[i].vector),'p', i)
        # for i in range(len(self.aPs)):
        #     print(type(self.aPs[i].vector),'a', i)
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
                ) * (-1 if Vector.isOpposite(p.vector, (a[0][1],-a[0][0])) else 1)
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
        # render_text('{},{}'.format(*map(round,self.p)))
    def draw(self):
        ro = sin(self.orientation),cos(self.orientation)
        for p in self.aPs:
            p.draw()
        for p in self.wheels:
            p.display(self.mp.t, self.mp.l)
        for p in self.propellers:
            p.draw()
        pygame.draw.polygon(screen, 0xff, tuple(map(lambda p: Vector.add(self.p,Vector.rotate(p,ro),self.mp.t),self.path)))
        Vector.draw(self.vector, Vector.add(self.p,self.mp.t), 1, 0x00ff00)


