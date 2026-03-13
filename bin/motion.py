from pybricks.hubs import InventorHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Port
from pybricks.pupdevices import Motor
from pybricks.tools import run_task

hub = InventorHub(
    broadcast_channel=100,
    observe_channels=[101],
)
# hub.display.text("Hello, World")


tilt_motor = Motor(Port.F, gears=[[1, 40], [8, 28]])
pan_motor = Motor(Port.B, gears=[[1, 40], [24, 24], [12, 60]])
drive_motor = Motor(Port.D, gears=[[8, 40]])

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


# def clamp(value, min_value, max_value):
#     return max(min(value, max_value), min_value)


async def main():
    print("Starting")
    sent = False
    seq = 0
    while True:
        # await multitask(
        #     track_colour(),
        #     track_distance(),
        # )
        left, right = controller.triggers()

        x, y = controller.joystick_left()
        _, drive = controller.joystick_right()
        # left = clamp(y + x, -100, 100)
        # right = clamp(y - x, -100, 100)
        # print(x, y, left, right, tx, ty)
        pan_motor.dc(-x)
        tilt_motor.dc(y)
        drive_motor.dc(drive)

        if right > 10:
            if not sent:
                await hub.ble.broadcast(seq)
                print("snap:", seq)
                seq += 1
                sent = True
        else:
            sent = False


run_task(main())
