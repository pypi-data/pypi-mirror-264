from typing import Optional
from .Terminal import color

def color_input(text: str = "", beforeColor: Optional[color.foreground] = color.RESET):
    r"""Gets an input

    executes the input() function in cyan and changes the color back to beforeColor if given

    Parameters
    ----------
    text: Optional[str]
        The text that is printed before getting the input
        DEFAULT: ""
    beforeColor: Optional[Terminal.color.foreground]
        The color that was used before (if u want it to change back)
        DEFAULT: Terminal.color.RESET
    """
    if text:
        res = input(text + color.foreground.FCYAN)
    else:
        res = input(color.foreground.FCYAN)
    if beforeColor is not None:
        print(beforeColor, end="")
    return res