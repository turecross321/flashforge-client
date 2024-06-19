import time

from printer_client import FlashForgeClient

api: FlashForgeClient = FlashForgeClient("10.10.100.254", 8899)

speed = 2000.0
direction = 1.0
duration = 0.2

api.set_light(255, 255, 255)

while True:
    api.start_moving(speed * direction, 4000)
    time.sleep(duration)
    api.stop_moving()
    time.sleep(duration)

    direction *= -1