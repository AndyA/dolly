from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, run_task, multitask
from pybricks.iodevices import XboxController

hub = InventorHub()
# hub.display.text("Hello, World")

print("Hello, World")

h_motor = Motor(Port.A)
s_motor = Motor(Port.C)
v_motor = Motor(Port.E)

c_sense = ColorSensor(Port.F)

d_sense = UltrasonicSensor(Port.B)
d_motor = Motor(Port.D)
controller = XboxController()


async def track_distance():
    dist = await d_sense.distance()
    # print(dist)
    # await wait(500)
    d_motor.track_target(dist * 359 / 2000)


async def track_colour():
    col = await c_sense.hsv()
    hub.light.on(col)
    print(col)
    # await wait(500)
    h_motor.track_target(col.h)
    s_motor.track_target(col.s)
    v_motor.track_target(col.v)


# SPEED = 500
async def main():
    while True:
        await multitask(
            track_colour(),
            track_distance(),
        )
        horizontal, vertical = controller.joystick_left()
        print(horizontal, vertical)


run_task(main())
