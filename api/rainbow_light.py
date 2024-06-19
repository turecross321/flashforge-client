import time
import math

from printer_client import FlashForgeClient

api: FlashForgeClient = FlashForgeClient("10.10.100.254", 8899)
INTERVAL = 0.05
COLOR_SAMPLE_AMOUNT = 40

def clamp(n, min, max):
    if n < min:
        return min
    if n > max:
        return max
    
    return n

def process_color(color): # clamp float between 0-255, and remove decimals
    color = math.ceil(color)
    color = clamp(color, 0, 255)
    return color
    
def rainbow():
    r, g, b = 255, 0, 0
    state = 0
    
    diff = 255 / COLOR_SAMPLE_AMOUNT
    margin_of_error = diff / 2

    while True:
        if state == 0:
            if g >= 255 - margin_of_error:
                state = 1
            else:
                g += diff
        if state == 1:
            if r <= 0 + margin_of_error:
                state = 2
            else:
                r -= diff
        if state == 2:
            if b >= 255 - margin_of_error:
                state = 3
            else:
                b += diff
        if state == 3:
            if g <= 0 + margin_of_error:
                state = 4
            else:
                g -= diff
        if state == 4:
            if r >= 255 - margin_of_error:
                state = 5
            else:
                r += diff
        if state == 5:
            if b <= 0 + margin_of_error:
                state = 0
            else:
                b -= diff

        r = process_color(r)
        g = process_color(g)
        b = process_color(b)

        api.set_light(r, g, b)
        time.sleep(INTERVAL)

rainbow()