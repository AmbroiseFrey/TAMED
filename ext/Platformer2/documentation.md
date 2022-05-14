
# math_utils.py:

**_hypot_**: function(*v)->float; function qui permet de trouver l'hypothénus en en fonction des coordonnées d'un point 

**_sort_**: function(*a)->tuple; function presque équivalente à sorted mais qui simlifie les fonctions à venir  

  **_binomialcoefs_**: function(n)-> fonction qui permet de trouver les coefficients binomiaux i de 
 degrés `n` tels que (a+b)<sup>n</sup> = i<sub>0</sub>·a<sup>n</sup> + i<sub>1</sub>·a<sup>n 1</sup>b + ... + i<sub>n-1</sub>·ab<sup>n-1</sup> + i<sub>n</sub>·b<sup>n</sup> 
 
    par exemple
      >>> binomialcoefs(2) 
      >>> (1,2,1) 
        car (a+b)² = 1·a² + 2·ab + 1·b² 
      
**_BezierCurve_**: function(*pts)->function; crée la fonction d'une BezierCurve de dimension `len(pts)` _(if you don't know what a bezier curve is, go check it out, it's really cool)_

________________________

## class Vector(Sequence):

  **_constructor_**: function(A,B)->Vector; retourne un Objet vecteur (séquençable) représentant le vecteur de A à B si B est définit, le vecteur A si A est séquençable ou le vecteur nul de dimension A si a est un nombre

  **_add_**: function(*v)->Vector; ajoute les vecteurs `v` à l'objet Vector

  **_substract_**: function(*v)->Vector; soustrait les vecteurs `v` à l'objet Vector

  **_multiply_**: function(n)->Vector; multiplie l'objet Vector par `n`

  **_map_**: function(callback:function)->Vector; change toutes les valeurs `e` de l'objet Vector par `callback(e,i)` en fonction de leur indice `i`

  **_setValue_**: function(Sequence)->Vector; permet de changer les coordonnées du vecteur sans changer l'objet en lui-même

  **_rotate_**: function(a, origin:Sequence)->Vector; fait une rotation du vecteur 2D
  
  **_norm_**: <getter|setter>; renvoie ou impose (en conservation sa direction et son sens) la norme de l'objet object 

  **_opposite2D_**: &lt;getter>; renvoie un vecteur orthogonal à l'objet Vector


________________________


## class MemoryVector(Vector):

  **_constructor_**: function(*a); class qui extend la class Vector mais qui se rapelle de sa position initiale


________________________


## class Circle:
  
  **_constructor_**: function(r, c); crée un Objet cercle qui contient le rayon et le centre du cercle
  
  **_intersect_**: function(circle); fonction qui renvoie le.s point.s d'intersection avec un autre Objet cercle s'il.s existe.nt


________________________


## class Segment:

  **_constructor_**: function(p:Sequence,q:Sequence);  crée un Object segment (qui fonctionne comme un segment)

  **_separate_**: function(l); division du segment dans plusieurs cases de taille `l`


________________________


## class Cartesienne:

  **_constructor_**: function(a,b,c); fonction cartésienne de la forme ax + by + c = 0
  
  **_intersect_**: function(l); point d'intersection (s'il existe) entre les deux droites 

  **_distance_**: function(point:Sequence); renvoie la distance minimale du point à la droite

  **_closest_**: function(point:Sequence); renvoie le point appartenant à l'équation cartésienne le plus proche du `point` 


________________________

# map_utils.py

________________________

## class Wall(Segment):

  **_constructor_**: function(p,q); classe du même type que Segment mais avec de vecteurs qui permettent de bloquer

  **_collides_**: function(segment:Segment); renvoie l'intersection avec un segment s'elle existe

  **_draw_**: function(t:tuple,k:float); dessine le mur sur l'écran

  **_closeToInterval_**: function(point, err); renvoie si un point est proche de l'intervalle du mur


________________________


## class CaseMatrix:
    def __init__(self, x,y,l):
        self.rect = x,y,x+l,y+l
        self.contains = []
    def add(self, wall:Wall):
        self.contains.append(wall)


________________________


## class FloorMatrix:
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


________________________

# robot_utils.py

**_gravity_**: Vector; gravité

________________________


## class Spring:
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


________________________


## class Leg:

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


________________________


## class Robot:

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
