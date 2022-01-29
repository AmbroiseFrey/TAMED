$ = (s, p = document) => p.querySelector(s);
svg = $('svg');
orient = $('#orientation')
p2 = Math.PI / 2
keys = {};
onkeydown = ({ key }) => keys[key] = true;
onkeyup = ({ key }) => keys[key] = false;
mouseposition = { x: innerWidth / 2, y: innerHeight / 2 }
onmousemove = ({ x, y }) => { mouseposition.x = x; mouseposition.y = y };

class Map:
    def __init__(self, height = 250, width = 250):
        self.height = height
        self.width = width
        svg.setAttribute('viewBox', `${-width / 2} ${-height / 2} ${width} ${height}`)

class Propeller:
    def __init__(self, chassis, pos, el):
        self.power = 0
        self.chassis = chassis
        self.force = [0, 0]
        self.pos = pos
        self.el = el

    def update(self):
        self.force = [
            Math.cos(self.chassis.orientation) * self.power,
            -Math.sin(self.chassis.orientation) * self.power
        ]
        self.nextpos = self.pos.map((e, i) => e + self.force[i])

    def display(self):
        [self.el.x1.baseVal.value,
        self.el.y1.baseVal.value] = self.pos
        [self.el.x2.baseVal.value,
        self.el.y2.baseVal.value] = self.pos.map((e, i) => e - self.force[i] * 5)

class Weight:
    def __init__(self,pos):
        self.force = [0, 1]
        self.pos = pos
    def update():
      self.nextpos = self.pos.map((e, i) => e + self.force[i])

class Chassis:
    def __init__(self, map, r = 10):
        self.line = $('line', svg)
        self.line.x1.baseVal.value = -r
        self.line.x2.baseVal.value = r
        self.r = r
        self.p = [0, 0]
        self.orientation = p2
        self.vector = [0, 0]
        self.map = map
        self.propellers = [
            Propeller(self, [-r, 0], $('#prop1', svg)),
            Propeller(self, [r, 0], $('#prop2', svg))
        ]
        self.weight = Weight([0, 0])
        self.rotateIndex = 0

    def update(self):
        // const coef1 = 2 - mouseposition.y / innerHeight * 2
        // const coef2 = mouseposition.x / innerWidth
        // self.propellers[0].power = coef1 * coef2
        // self.propellers[1].power = coef1 * (1 - coef2)
        // console.log(keys.ArrowUp && (keys.ArrowRight || .5))
        self.propellers[0].power = keys.ArrowUp && (keys.ArrowRight || .75) || 0;
        self.propellers[1].power = keys.ArrowUp && (keys.ArrowLeft || .75) || 0;
        self.propellers.forEach(p => p.update())
        self.weight.update()
        self.vector = self.vector.map((v, i) => v + self.propellers[0].force[i] + self.propellers[1].force[i] + self.weight.force[i])
        self.p = [
            self.vector[0] * .1 + (self.propellers[0].nextpos[0] + self.propellers[1].nextpos[0] + self.weight.nextpos[0]) / 3,
            self.vector[1] * .1 + (self.propellers[0].nextpos[1] + self.propellers[1].nextpos[1] + self.weight.nextpos[1]) / 3
        ]
        // const arr = [self.p, self.weight.pos, self.weight.nextpos];
        // const [a, c, b] = arr.map((e, i) => Math.hypot(e[0] - arr[(i + 1) % 3][0], e[1] - arr[(i + 1) % 3][1]));
        self.rotateIndex += Math.asin(self.propellers[0].power / -self.r) + Math.asin(self.propellers[1].power / self.r);
        self.orientation += self.rotateIndex * .1 + Math.asin(self.propellers[0].power / -self.r) + Math.asin(self.propellers[1].power / self.r);
        self.line.x1.baseVal.value = self.propellers[0].pos[0] = self.p[0] - Math.sin(self.orientation) * self.r
        self.line.y1.baseVal.value = self.propellers[0].pos[1] = self.p[1] - Math.cos(self.orientation) * self.r
        self.line.x2.baseVal.value = self.propellers[1].pos[0] = self.p[0] + Math.sin(self.orientation) * self.r
        self.line.y2.baseVal.value = self.propellers[1].pos[1] = self.p[1] + Math.cos(self.orientation) * self.r
        self.weight.pos = self.p
        self.propellers.forEach(p => p.display())
        self.vector = self.vector.map(e => e * .99)
        self.rotateIndex *= .95


map = Map()
chassis = Chassis(map)

while True:
    chassis.update()