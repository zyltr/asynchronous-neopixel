from asyncio import sleep

from neopixel import NeoPixel

"""
This file uses modified functions found in the reference below (specifically, 'rainbow_cycle' and 'wheel')
https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython#full-example-code-3005651
"""


async def cycle(brightness: float, delay: float, pixels: NeoPixel):
    """
    Transitions through a series of colors linearly.
    :param brightness: controls the brightness of the NeoPixels
    :param delay: time in seconds between each color transition
    :param pixels: NeoPixel object
    """

    await __validate(brightness, delay)

    rgb = getattr(pixels, "bpp") == 3

    for j in range(255):
        color = await __wheel(j & 255, rgb)
        color = tuple(map(lambda value: int(value * brightness), color))
        pixels.fill(color)
        pixels.write()
        await sleep(delay)


async def off(brightness: float, delay: float, pixels: NeoPixel):
    """
    Removes all color from the NeoPixels.
    :param brightness: controls the brightness of the NeoPixels
    :param delay: time in seconds between each color transition
    :param pixels: NeoPixel object
    """

    darkness = (0, 0, 0) if getattr(pixels, "bpp") == 3 else (0, 0, 0, 0)
    pixels.fill(darkness)
    pixels.write()
    await sleep(delay)


async def rainbow(brightness: float, delay: float, pixels: NeoPixel):
    """
    Illuminates individuals pixels in a series of colors.
    :param brightness: controls the brightness of the NeoPixels
    :param delay: time in seconds between each color transition
    :param pixels: NeoPixel object
    """

    await __validate(brightness, delay)

    total = len(pixels)
    rgb = getattr(pixels, "bpp") == 3

    for j in range(255):
        for i in range(total):
            index = (i * 256 // total) + j
            color = await __wheel(index & 255, rgb)
            color = tuple(map(lambda value: int(value * brightness), color))
            pixels[i] = color

        pixels.write()
        await sleep(delay)


async def __validate(brightness: float, delay: float):
    """
    Validates the parameters against negativeness and extreme limits.
    :param brightness: controls the brightness of the NeoPixels
    :param delay: time in seconds between each color transition
    """

    if brightness < 0.0 or brightness > 1.0:
        raise ValueError(f"Brightness is outside the range of [0.0, 1.0]")

    if delay < 0.0:
        raise ValueError(f"Delay must be non-negative")


async def __wheel(position: int, rgb: bool = True):
    """
    Returns an appropriately sized tuple representing a color
    :param position: an integer between 0 and 255
    :param rgb: whether, or not, to return an RGB tuple
    """

    if position < 0 or position > 255:
        r = g = b = 0
    elif position < 85:
        r = int(position * 3)
        g = int(255 - position * 3)
        b = 0
    elif position < 170:
        position -= 85
        r = int(255 - position * 3)
        g = 0
        b = int(position * 3)
    else:
        position -= 170
        r = 0
        g = int(position * 3)
        b = int(255 - position * 3)

    return (r, g, b) if rgb else (r, g, b, 0)
