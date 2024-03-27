from typing import Optional
from ._better_input import better_input as BetterInput
from .Terminal import color


def better_color_input(text: str = None, delay: float = .01, beforeColor: Optional[color.foreground] = color.RESET):
    r"""Gets an input

    Prints the given text letter by letter using the specified delay and gets an input() after

    Parameters
    ----------
    text: Optional[str]
        The text that is printed letter by letter
        DEFAULT: None

    delay: Optional[float]
        Changes the time between each printed letter
        DEFAULT: .01
    
    beforeColor: Optional[Terminal.color.foreground]
        The color to change back to after getting the input
        DEFAULT: Terminal.color.RESET
    """
    if text is not None:
        res = BetterInput(text, color.foreground.FCYAN, delay)
    else:
        res = BetterInput(end=color.foreground.FCYAN, delay=delay)
    if beforeColor is not None:
        print(beforeColor, end="")
    return res