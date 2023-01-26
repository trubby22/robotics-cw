import brickpi3
import time

BP = brickpi3.BrickPi3()

LWHEEL = BP.PORT_A
RWHEEL = BP.PORT_D


def stop():
    BP.reset_all()


def set_powers(lpow, rpow):
    BP.set_motor_power(LWHEEL, lpow)
    BP.set_motor_power(RWHEEL, rpow)


def set_angle(langle, rangle):
    BP.set_motor_position(LWHEEL, langle)
    BP.set_motor_position(RWHEEL, rangle)


# drives forwards then stops. time in secnods
def forward(duration):
    start = time.time()
    end = start

    set_powers(50, 50)

    while end - start < duration:
        end = time.time()

    stop()


try:
    set_angle(360, 0)
    time.sleep(1)
    set_angle(180, 0)
except Exception as e:
    # print(f"Error has occured: {e}")
    stop()

