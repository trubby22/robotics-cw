from __future__ import annotations
import math
import random
# import time

# import brickpi3
import math
import time

# 18cm - between wheels

# BP = brickpi3.BrickPi3()

D = 6.8
C = D * math.pi

SIGMA = 3

# LWHEEL = BP.PORT_A
# RWHEEL = BP.PORT_B
# BASEROT = 207
# DPS = 275


# BP.set_motor_limits(LWHEEL, dps=DPS)
# BP.set_motor_limits(RWHEEL, dps=DPS)


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


# # drives forwards in cm
# def forward(distance):
#     rots = distance / 90 / C
#     angle = rots * 360
#     add_angle(angle, angle)


# # side 1 = rotate anticlock, side -1 = rotate clock
# def rotate(side):
#     add_angle(BASEROT * side, BASEROT * -side)


def navto(sim, waypoint):
    state = sim.get_mean_state()
    dx = waypoint.x - state.pos.x
    dy = waypoint.y - state.pos.y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    angle = (math.degrees(math.atan2(dy, dx)))

    angle = ((((state.a - angle)) % 360) + 360) % 360
    if angle > 180:
        angle -= 360

    sim.rotateL(angle)
    sim.forward(distance)
    sim.draw()

    # rotate(angle)
    # forward(distance)


def _rng(sigma, mu=0):
    return lambda: random.normalvariate(mu=mu, sigma=sigma)


# return the distance between a state and a line if it intersects, it not return None
def state_line_distance(state, p1, p2):
    # turn both into parametric form
    # segment start, segment end
    ss = p1
    se = p2

    # line in parametric form
    # line start, line delta, line end
    ls = state.pos
    ld = Point(math.cos(math.radians(state.a)), math.sin(math.radians(state.a)))
    le = ls + ld

    # find the point of intersection
    # \left(y_{1}-y_{2}\right)\left(x_{1}-x_{3}\right)+\left(x_{2}-x_{1}\right)\left(y_{1}-y_{3}\right)
    # \left(x_{4}-x_{3}\right)\left(y_{1}-y_{2}\right)-\left(x_{1}-x_{2}\right)\left(y_{4}-y_{3}\right)
    # \left(y_{3}-y_{4}\right)\left(x_{1}-x_{3}\right)+\left(x_{4}-x_{3}\right)\left(y_{1}-y_{3}\right)
    # \left(x_{4}-x_{3}\right)\left(y_{1}-y_{2}\right)-\left(x_{1}-x_{2}\right)\left(y_{4}-y_{3}\right)
    l_1 = (ss.y - se.y) * (ss.x - ls.x) + (se.x - ss.x) * (ss.y - ls.y)
    l_2 = (le.x - ls.x) * (ss.y - se.y) - (ss.x - se.x) * (le.y - ls.y)
    s_1 = (ls.y - le.y) * (ss.x - ls.x) + (le.x - ls.x) * (ss.y - ls.y)
    s_2 = (le.x - ls.x) * (ss.y - se.y) - (ss.x - se.x) * (le.y - ls.y)

    # if the lines are parallel, there is no intersection
    if s_2 == 0 or l_2 == 0:
        return None

    s = s_1 / s_2
    l = l_1 / l_2

    # if it's not between 0 and 1, it's not on the segment
    if s < 0 or s > 1:
        return None

    # find the coordinates of the intersection on the line
    inter = ls + ld * l

    print(s_1, s_2, s)
    print(l_1, l_2, l)
    print(ss, se, ls, le)
    print(ls, inter)

    # find the distance from the intersection to the segment
    distance = (inter - ls).mag()

    return distance


class State:
    def __init__(self, point, a) -> None:
        self.pos = point
        self.a = a

    def forward(self, d, e, f) -> None:
        self.pos.x += (d + e) * math.cos(math.radians(self.a))
        self.pos.y += (d + e) * math.sin(math.radians(self.a))
        self.a += f


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
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Simulation:
    def __init__(self, e, f, g, N=100):
        self.erng = _rng(e)
        self.frng = _rng(f)
        self.grng = _rng(g)

        self.N = N
        self.states = [State(Point(0, 0), 0) for i in range(self.N)]
        self.verts = [Point(0, 0),
                      Point(0, 168),
                      Point(84, 168),
                      Point(84, 126),
                      Point(84, 210),
                      Point(168, 210),
                      Point(168, 84),
                      Point(210, 84),
                      Point(210, 0)]

    def to_world_graphics(self, state):
        offset = Point(50, 300)
        dirmult = Point(1, -1)
        return state.pos * dirmult + offset

    def drawLine(self, p1, p2):
        p1 = self.to_world_graphics(p1)
        p2 = self.to_world_graphics(p2)
        print(f"drawLine:({p1.x}, {p1.y}, {p2.x}, {p2.y})")

    def drawBox(self):
        for i in range(len(self.verts)):
            self.drawLine(self.verts[i], self.verts[(i + 1) % len(self.verts)])

    def drawStates(self):
        states = [self.to_world_graphics(state) for state in self.states]
        print(f"drawStates:{str(states)}")

    def draw(self):
        self.drawBox()
        self.drawStates()

    def forward(self, d):
        for state in self.states:
            state.forward(d, self.erng(), self.frng())

    def rotateL(self, a):
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
        for i in range(len(self.verts)):
            wall_start = self.verts[i]
            wall_end = self.verts[(i + 1) % len(self.verts)]
            # check for line line intersection

        return min(wall_distances)

    def calc_likelihood(self, state, measurement):
        expected = self.find_wall(state, measurement)
        return math.exp((-(expected - measurement)) ** 2 / (2 * SIGMA ** 2))


e = 0.7071067811865475
f = 0.1426
g = 2.507533339065598

sim = Simulation(e, f, g, 100)


# try:
#     navto(sim, Point(84, 30))
#     navto(sim, Point(180, 30))
#     navto(sim, Point(180, 54))
#     navto(sim, Point(138, 54))
#     navto(sim, Point(138, 168))
#     navto(sim, Point(114, 168))
#     navto(sim, Point(114, 84))
#     navto(sim, Point(84, 84))
#     navto(sim, Point(84, 30))
# except Exception as e:
#     print(e)

# here are
print(state_line_distance(State(Point(0, 0), 0), Point(0, 1), Point(1, 0)))
print(state_line_distance(State(Point(0, 0), 45), Point(0, 1), Point(1, 0)))
print(state_line_distance(State(Point(0, 0), 90), Point(0, 1), Point(1, 0)))
print(state_line_distance(State(Point(0, 0), 45), Point(0.7, 3.8), Point(5.9, 1.8)))
print(state_line_distance(State(Point(0, 0), 45), Point(-1.6, 4.5), Point(-0.8, -3.1)))
