from pybricks.hubs import InventorHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Port
from pybricks.pupdevices import Motor
from pybricks.tools import run_task

hub = InventorHub()
# hub.display.text("Hello, World")


tilt_motor = Motor(Port.F)
pan_motor = Motor(Port.B)
drive_motor = Motor(Port.D)

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
        _, drive = controller.joystick_right()
        # left = clamp(y + x, -100, 100)
        # right = clamp(y - x, -100, 100)
        # print(x, y, left, right, tx, ty)
        pan_motor.dc(-x)
        tilt_motor.dc(y)
        drive_motor.dc(drive)


run_task(main())
