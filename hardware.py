from machine import Pin
from neopixel import NeoPixel

from primitives.pushbutton import Pushbutton

"""
Asyncio Reference
https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#01-installing-asyncio-primitives

Pushbutton Event Reference
https://github.com/peterhinch/micropython-async/blob/master/v3/docs/DRIVERS.md#event-interface-1
"""


class Input:
    """
    Simple class to manage the various connected input devices.
    """

    __BRIGHTNESS_PIN = 2
    __CHANGE_PIN = 3
    __DELAY_PIN = 1

    brightness = Pushbutton(Pin(__BRIGHTNESS_PIN, Pin.OUT, Pin.PULL_DOWN))
    change = Pushbutton(Pin(__CHANGE_PIN, Pin.OUT, Pin.PULL_DOWN))
    delay = Pushbutton(Pin(__DELAY_PIN, Pin.OUT, Pin.PULL_DOWN))

    brightness.press_func(None)
    change.press_func(None)
    delay.press_func(None)


class Output:
    """
    Simple class to manage the various output connected devices.
    """

    __PIXELS_COUNT = 8
    __PIXELS_PIN = 0
    ___RGB = True

    pixels = NeoPixel(Pin(__PIXELS_PIN), __PIXELS_COUNT, bpp=3 if ___RGB else 4)
