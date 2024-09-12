from asyncio import CancelledError, create_task, gather, run, Task
from collections import deque
from time import gmtime

from hardware import Output, Input

from lighting import cycle, off, rainbow

"""
Global Constant and Variables
"""

_brightnesses: deque = deque((0.10, 0.25, 0.50, 0.75, 1.00), 5)
_brightness: float = _brightnesses.popleft()

_delays: deque = deque((0.1, 0.01, 0.001, 0.0001, 0.00001), 5)
_delay: float = _delays.popleft()

_effects: deque = deque((rainbow, cycle, off), 3)
_effect = _effects.popleft()

"""
Global Tasks
"""

_lighting: Task = None

"""
Event Handlers
"""


async def alight():
    """
    Causes the NeoPixel object to illuminate using the desired effect.
    """

    global _effect

    try:
        _, _, _, hour, minute, second, _, _ = gmtime()
        print(f"Pixels are now alight < {hour}:{minute}:{second} >")
        while True:
            await _effect(_brightness, _delay, Output.pixels)
    except CancelledError:
        print("Pixels are now dark")
    finally:
        print("Lighting task terminated", "", sep="\n")


async def brightness():
    """
    Adjusts the NeoPixel's brightness when the input device is depressed.
    """

    global _brightness, _brightnesses

    while True:
        await Input.brightness.press.wait()
        Input.brightness.press.clear()
        _brightnesses.append(_brightness)
        _brightness = _brightnesses.popleft()
        print(f"Brightness : {_brightness * 100:.0f}%")
        await relight()


async def delay():
    """
    Adjusts the NeoPixel's transitional delay when the input device is depressed.
    """

    global _delay, _delays

    while True:
        await Input.delay.press.wait()
        Input.delay.press.clear()
        _delays.append(_delay)
        _delay = _delays.popleft()
        print(f"Delay : {_delay:.5f}s")
        await relight()


async def change():
    """
    Changes the lighting effect used on the NeoPixel when the input device is depressed.
    """

    global _effect, _effects

    while True:
        await Input.change.press.wait()
        Input.change.press.clear()
        _effects.append(_effect)
        _effect = _effects.popleft()
        print("Effect Changed")
        await relight()


"""
"""


async def relight():
    """
    Restarts the lighting task.
    """

    global _lighting

    _lighting.cancel()
    _lighting = create_task(alight())


async def start():
    """
    Start of the program.
    """

    global _lighting

    await gather(_lighting := create_task(alight()), brightness(), change(), delay())


"""
"""

run(start())
