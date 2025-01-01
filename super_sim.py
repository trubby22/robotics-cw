from __future__ import annotations
import math
import random

# import brickpi3
import math
import time

# 18cm - between wheels


# BP = brickpi3.BrickPi3()
# BP.reset_all()

D = 6.8
C = D * math.pi

SIGMA = 3

# SONAR = BP.PORT_1
# LWHEEL = BP.PORT_A
# RWHEEL = BP.PORT_B
BASEROT = 222
DPS = 275
DIST_RESAMPLE = 20


# BP.set_motor_limits(LWHEEL, dps=DPS)
# BP.set_motor_limits(RWHEEL, dps=DPS)
# BP.set_sensor_type(SONAR, BP.SENSOR_TYPE.NXT_ULTRASONIC)


# def close_enough(a, b, delta=1):
#     return abs(a - b) <= delta


# def add_angle(langle, rangle):
#     old_langle = BP.get_motor_encoder(LWHEEL)
#     old_rangle = BP.get_motor_encoder(RWHEEL)
#     target_langle = old_langle + langle
#     target_rangle = old_rangle + rangle

#     BP.set_motor_position_relative(LWHEEL, langle)
#     BP.set_motor_position_relative(RWHEEL, rangle)

#     while not close_enough(old_langle, target_langle) and not close_enough(old_rangle, target_rangle):
#         old_langle = BP.get_motor_encoder(LWHEEL)
#         old_rangle = BP.get_motor_encoder(RWHEEL)
#         time.sleep(0.01)


# def get_sonar_reading():
#     vals = []
#     for i in range(9):
#         vals.append(BP.get_sensor(SONAR))
#         time.sleep(0.01)
#     return sorted(vals)[5]

# # drives forwards in cm
# def forward(distance):
#     rots = distance / C
#     angle = rots * 360
#     add_angle(angle, angle)


# # side 1 = rotate anticlock, side -1 = rotate clock
# def rotate(side):
#     side = side / 90
#     add_angle(BASEROT * side, BASEROT * -side)


def navto(sim, waypoint):
    for i in range(50):
        state = sim.get_mean_state()
        dx = waypoint.x - state.pos.x
        dy = waypoint.y - state.pos.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        angle = (math.degrees(math.atan2(dy, dx)))

        angle = ((((state.a - angle)) % 360) + 360) % 360
        if angle > 180:
            angle -= 360
            
        distance = min(distance, DIST_RESAMPLE)

        # rotate(angle)
        # forward(distance)

        sim.rotate(angle)
        sim.forward(distance)
        # sim.draw()
        
        # sonar = get_sonar_reading()
        # dsts = [126, 106, 86, 66, 46, 30]
        # sonar = dsts[i+1]
        sim.resample()
        # print(f"{sonar}")
        # print(f"{waypoint}, {sim.get_mean_state()}")
        foo = sim.get_mean_state()
        print(foo)
        # a, b, c = int(a), int(b), int(c)
        # print(a, b, c)
        
        if distance < DIST_RESAMPLE:
            break


    # # turn to nearest 90 degrees
    # nearest = round(state.a / 90) * 90
    # delta = nearest - state.a
    # delta = ((((delta)) % 360) + 360) % 360
    # if delta > 180:
    #     delta -= 360
    
    # rotate(delta)
    # sim.rotate(delta)



def _rng(sigma, mu=0):
    return lambda: random.normalvariate(mu=mu, sigma=sigma)


# The one from the slides
def state_segment_distance2(state, p1, p2):
    dp2p1 = p2 - p1
    dp1s = state.pos - p1
    top = dp2p1.x * dp1s.y - dp2p1.y * dp1s.x
    bottom = dp2p1.y * math.cos(math.radians(state.a)) - dp2p1.x * math.sin(math.radians(state.a))
    if bottom == 0:
        return None
    return top / bottom


def weighted_choice(choices):
    rnum = random.random()
    for weight, state in choices:
        if rnum < weight:#
            return state.clone()
        rnum -= weight
    raise ValueError("No choice made")


class State:
    def __init__(self, point, a) -> None:
        self.pos = point
        self.a = a
        self._norma_angle()

    def _norma_angle(self):
        # mod the angles so it's between negative 180 and 180
        if -360 < self.a < 360:
            return
        self.a = abs(self.a) % 360 * (self.a / abs(self.a))
        
    def clone(self):
        return State(Point(self.pos.x, self.pos.y), self.a) 

    def forward(self, d, e, f) -> State:
        self.pos.x += (d + e) * math.cos(math.radians(self.a))
        self.pos.y += (d + e) * math.sin(math.radians(self.a))

        self.a = (self.a + f) 
        self._norma_angle()
        return self

    def rotate(self, a, g) -> State:
        self.a = (self.a - a - g)
        self._norma_angle()
        return self

    def __add__(self, state) -> State:
        return State(self.pos + state.pos, self.a + state.a)

    def __div__(self, n) -> State:
        return State(self.pos / n, self.a / n)

    def __str__(self) -> str:
        return f"({self.pos.x:.0f}, {self.pos.y:.0f}, {self.a:.0f})"

    def __repr__(self) -> str:
        return str(self)


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def mag(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, point) -> Point:
        if not isinstance(point, Point):
            raise TypeError
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point) -> Point:
        if not isinstance(point, Point):
            raise TypeError
        return Point(self.x - point.x, self.y - point.y)

    def __mul__(self, n):
        if isinstance(n, Point):
            return Point(self.x * n.x, self.y * n.y)
        elif isinstance(n, int) or isinstance(n, float):
            return Point(self.x * n, self.y * n)
        else:
            raise TypeError

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


class Simulation:
    def __init__(self, e, f, g, N=100, initial_state=State(Point(0, 0), 0)):
        self.erng = _rng(e)
        self.frng = _rng(f)
        self.grng = _rng(g)

        self.N = N
        self.states = [initial_state.clone() for i in range(self.N)]
        self.verts = [Point(0, 0),
                      Point(0, 168),
                      Point(84, 168),
                      Point(84, 126),
                      Point(84, 210),
                      Point(168, 210),
                      Point(168, 84),
                      Point(210, 84),
                      Point(210, 0)]

    def to_world_graphics(self, point):
        offset = Point(50, 300)
        dirmult = Point(1, -1)
        return point * dirmult + offset

    def drawLine(self, p1, p2):
        p1 = self.to_world_graphics(p1)
        p2 = self.to_world_graphics(p2)
        print(f"drawLine:({p1.x}, {p1.y}, {p2.x}, {p2.y})")

    def drawBox(self):
        for i in range(len(self.verts)):
            self.drawLine(self.verts[i], self.verts[(i + 1) % len(self.verts)])

    def drawStates(self):
        states = [State(self.to_world_graphics(state.pos), state.a) for state in self.states]
        # print(self.states)
        print(f"drawParticles:{str(states)}")

    def draw(self):
        self.drawBox()
        self.drawStates()

    def resample(self, measurements=None):
        ws = [(self.calc_likelihood(state, measurements), state) for state in self.states]
        # print([w for w, s in ws])
        sws = sum([w for w, s in ws])
        if sws == 0:
            print("Cannot normalize weights, all zero")
            return
        aws = [(w / sws, s) for w, s in ws]
        # print([w for w, s in aws])
        
        self.states = [weighted_choice(aws) for i in range(self.N)]

    def forward(self, d):
        for state in self.states:
            state.forward(d, self.erng(), self.frng())

    def rotate(self, a):
        for state in self.states:
            state.rotate(a, self.grng())

    def get_mean_state(self):
        x, y, a = 0, 0, 0
        n = len(self.states)
        for s in self.states:
            x += s.pos.x
            y += s.pos.y
            a += s.a
        return State(Point(x/n, y/n), a/n)

    def find_wall(self, state, measurement):
        # find the most likely wall and the expected distance to it
        # return the expected distance to the wall
        wall_distances = []
        wall_distances2 = []
        for i in range(len(self.verts)):
            wall_start = self.verts[i]
            wall_end = self.verts[(i + 1) % len(self.verts)]
            # check for line line intersection
            distance = state_segment_distance2(state, wall_start, wall_end)
            if distance is not None:
                if distance > 0:
                    wall_distances.append(distance)
                else:
                    wall_distances2.append(distance)

        if len(wall_distances) == 0:
            if len(wall_distances2) == 0:
                return None
            return -1

        return min(wall_distances)

    def calc_likelihood(self, state, measurement=None):
        expected = self.find_wall(state, measurement)
        
        
        if expected is None or expected < 0:
            # no wall is found or got out of bounds
            return 0
        
        return math.exp(-(expected - measurement) ** 2 / (2 * SIGMA ** 2))


e = 0.7071067811865475
f = 0.1426
g = 2.507533339065598

sim = Simulation(e, f, g, 100, State(Point(84, 30), 0))

time.sleep(1)

try:
#     # navto(sim, Point(84, 30))
    navto(sim, Point(180, 30))
    navto(sim, Point(180, 54))
    navto(sim, Point(138, 54))
    navto(sim, Point(138, 168))
    navto(sim, Point(114, 168))
    navto(sim, Point(114, 84))
    navto(sim, Point(84, 84))
    navto(sim, Point(84, 30))
except Exception as e:
    raise e
    # print(e)
    # BP.reset_all()
    
# BP.reset_all()


# print(state_segment_distance2(State(Point(0, 0), 0), Point(0, 1), Point(1, 0)))
# print(state_segment_distance2(State(Point(0, 0), 45), Point(0, 1), Point(1, 0)))
# print(state_segment_distance2(State(Point(0, 0), 90), Point(0, 1), Point(1, 0)))
# print(state_segment_distance2(State(Point(0, 0), 45), Point(0.7, 3.8), Point(5.9, 1.8)))
# print(state_segment_distance2(State(Point(0, 0), 45), Point(-1.6, 4.5), Point(-0.8, -3.1)))
