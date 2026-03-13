from pybricks.hubs import InventorHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import run_task, wait

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


class OneShot:
    def __init__(self, *, trigger=10):
        self.trigger = trigger
        self.state = False

    def update(self, level):
        if level >= self.trigger:
            if not self.state:
                self.state = True
                return True
        else:
            self.state = False
        return False


class Snapper:
    def __init__(self):
        self.seq = -1

    async def snap(self):
        self.seq += 1
        await hub.ble.broadcast(self.seq)
        print("snap:", self.seq)
        # while True:
        #     ack = hub.ble.observe(101)
        #     if ack == self.seq:
        #         break
        #     wait(50)
        # print("ack")


class Engine:
    def __init__(self):
        print("Starting")
        self.left_trig = OneShot()
        self.right_trig = OneShot()
        self.snapper = Snapper()

    def poll_triggers(self) -> tuple[bool, bool]:
        left, right = controller.triggers()
        left_hit = self.left_trig.update(left)
        right_hit = self.right_trig.update(right)
        return left_hit, right_hit

    async def sequence(self):
        for frame in range(60):
            print("frame:", frame)
            left_hit, right_hit = self.poll_triggers()
            if right_hit:
                print("stopping")
                break
            await drive_motor.run_time(10, 1000, then=Stop.COAST, wait=True)
            await wait(500)
            await self.snapper.snap()
            await wait(800)

    def drive(self):
        x, y = controller.joystick_left()
        _, drive = controller.joystick_right()

        pan_motor.dc(-x)
        tilt_motor.dc(y)
        drive_motor.dc(drive)

    async def main(self):
        while True:
            # await multitask(
            #     track_colour(),
            #     track_distance(),
            # )
            self.drive()

            left_hit, right_hit = self.poll_triggers()

            if left_hit:
                await self.sequence()
            if right_hit:
                await self.snapper.snap()


engine = Engine()
run_task(engine.main())
