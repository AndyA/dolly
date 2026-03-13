from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = TechnicHub()
# hub.display.text("Hello, World")

print("Hello, World")

motor = Motor(Port.A)

# SPEED = 500

while True:
    motor.track_target(0)
    wait(500)
    motor.track_target(180)
    wait(500)
