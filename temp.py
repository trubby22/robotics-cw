import brickpi3
import time

BP = brickpi3.BrickPi3()

LWHEEL = BP.PORT_A
RWHEEL = BP.PORT_D

BP.set_motor_position(RWHEEL, -1)

#BP.set_motor_power(BP.PORT_D, 0)