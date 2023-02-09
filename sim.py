from __future__ import annotations
import math
import random
import time

import brickpi3
import math
import time

# 18cm - between wheels

BP = brickpi3.BrickPi3()

D = 6.8
C = D * math.pi


LWHEEL = BP.PORT_A
RWHEEL = BP.PORT_B
BASEROT = 207
DPS = 275


BP.set_motor_limits(LWHEEL, dps=DPS)
BP.set_motor_limits(RWHEEL, dps=DPS)


def close_enough(a, b, delta = 1):
    return abs(a - b) <= delta


def add_angle(langle, rangle):
    old_langle = BP.get_motor_encoder(LWHEEL)
    old_rangle = BP.get_motor_encoder(RWHEEL)
    target_langle = old_langle + langle
    target_rangle = old_rangle + rangle

    BP.set_motor_position_relative(LWHEEL, langle)
    BP.set_motor_position_relative(RWHEEL, rangle)

    while not close_enough(old_langle, target_langle) and not close_enough(old_rangle, target_rangle):
        old_langle = BP.get_motor_encoder(LWHEEL)
        old_rangle = BP.get_motor_encoder(RWHEEL)
        # print(old_langle, target_langle, old_rangle, target_rangle)
        time.sleep(0.01)


# drives forwards in cm
def forward(distance):
    rots = distance / C
    angle = rots * 360
    add_angle(angle, angle)


# side 1 = rotate anticlock, side -1 = rotate clock
def rotate(side):
    add_angle(BASEROT * side, BASEROT * -side)


def navto(state, waypoint):
    dx = waypoint.x - state.pos.x
    dy = waypoint.y - state.pos.y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    angle = math.degrees(math.atan2(dx, dy))
    rotate(state.a - angle / 90)
    forward(distance)


def _rng(sigma, mu=0):
        return lambda: random.normalvariate(mu=mu, sigma=sigma)


class State:
    def __init__(self, point, a) -> None:
        self.pos = point
        self.a = a


    def forward(self, d, e, f) -> None:
        self.pos.x += (d + e) *  math.cos(math.radians(self.a))
        self.pos.y += (d + e) *  math.sin(math.radians(self.a))
        self.a += f



    def rotate(self, a, g) -> State:
        self.a += a + g

    def __str__(self) -> str:
        return f"({self.pos.x}, {self.pos.y}, {self.a})"

    def __repr__(self) -> str:
        return str(self)

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, point) -> Point:
        if not isinstance(point, Point):
            raise TypeError

        return Point(self.x + point.x, self.y + point.y)



class Simulation:
    def __init__(self, e, f, g, N=100):
        self.erng = _rng(e)
        self.frng = _rng(f)
        self.grng = _rng(g)

        self.N = N
        self.states = [State(Point(0, 0), 0) for i in range(self.N)]


    def forward(self, d):
        for state in self.states:
            state.forward(d, self.erng(), self.frng())


    def rotateL(self, a):
        for state in self.states:
            state.rotate(a, self.grng())


    def drawBox(self):
        d = 400
        print(f"drawLine:(0, 0, {d}, 0)")
        print(f"drawLine:({d}, 0, {d}, {d})")
        print(f"drawLine:({d}, {d}, 0, {d})")
        print(f"drawLine:(0, {d}, 0, 0)")

    def draw(self):
        self.drawBox()
        # draw the states
        print(f"drawParticles:{str(self.states)}")


sim = Simulation(1, 1, 1, 100)

# try:
#     for _ in range(4):
#         for _ in range(4):
#             sim.forward(100)
#             sim.draw()
#             forward(10)
#         sim.rotateL(90)
#         sim.draw()
#         rotate(1)
# except Exception as e:
#     print(e)

navto(State(Point(0,0), 0), Point(10, 10))