from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, run_task, multitask
from pybricks.iodevices import XboxController

hub = InventorHub()
# hub.display.text("Hello, World")


left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
turret_motor = Motor(Port.C)
elevation_motor = Motor(Port.E)

print("Waiting for XBox Controller...")

controller = XboxController()

# async def track_distance():
#     dist = await d_sense.distance()
#     d_motor.track_target(dist * 359 / 2000)


# async def track_colour():
#     col = await c_sense.hsv()
#     hub.light.on(col)
#     print(col)
#     left_motor.track_target(col.h)
#     right_motor.track_target(col.s)
#     v_motor.track_target(col.v)


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


# SPEED = 500
async def main():
    while True:
        # await multitask(
        #     track_colour(),
        #     track_distance(),
        # )
        x, y = controller.joystick_left()
        tx, ty = controller.joystick_right()
        left = clamp(y + x, -100, 100)
        right = clamp(y - x, -100, 100)
        print(x, y, left, right, tx, ty)
        left_motor.dc(left)
        right_motor.dc(-right)
        turret_motor.dc(-tx)
        elevation_motor.dc(-ty)


run_task(main())
