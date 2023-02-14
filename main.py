import brickpi3
import math
import time

# 18cm - between wheels

BP = brickpi3.BrickPi3()

D = 6.8
C = D * math.pi


LWHEEL = BP.PORT_A
RWHEEL = BP.PORT_B
BASEROT = 216

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


try:
<<<<<<< HEAD
    rotate(-20)
    # for i in range(5):
        # rotate(-4)
    # forward(200)
    # for i in range(1):
    #     for i in range(1):
    #         print
    #         forward(200)
    #         rotate(-1)
=======
    # forward(200)
    for i in range(1):
        for i in range(1):
            print
            forward(200)
            # rotate(-1)
>>>>>>> cf9cd1f36d256ecea295bc4ee5d6d56b7c852692

except Exception as e:
    print(e)
    BP.reset_all()
