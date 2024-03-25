"""
Some functions of turtle graphics.
"""
import turtle
from typing import Tuple, Optional, Union
turtle = turtle.Turtle()
turtle.speed(0)
RGBInt = Union[list[int, int, int], Tuple[int, int, int]]
RGBIntList = Union[list[RGBInt], Tuple[RGBInt]]
ColorInt = Union[RGBIntList, RGBInt]
RGBFloat = Union[list[float, float, float], Tuple[float, float, float]]
RGBFloatList = Union[list[RGBFloat], Tuple[RGBFloat]]
ColorFloat = Union[RGBFloatList, RGBFloat]
Color = Union[RGBInt, RGBFloat]
ColorList = Union[list[Color], Tuple[Color], Color]
OptionalColor = Optional[ColorList]
def get_color_type(colors: Union[ColorInt, ColorFloat]) -> str:
    """
    Identifies the type of color data provided

    Args:
        colors (Union[ColorInt, ColorFloat]): A tuple or list 
            representing color values.

    Raises:
        TypeError: Raised if the color type is invalid.

    Returns:
        str: A string indicating the type of color data ("int", "float", 
            "int list", "float list")
    """
    if isinstance(colors[0], (list, tuple)):
        for color in colors:
            if all(isinstance(color_value, int) for color_value in color):
                result = "int list"
            elif all(isinstance(color_value, float) for color_value in color):
                result = "float list"
            else:
                raise TypeError("Invalid color type.")
    else:
        if all(isinstance(color_value, int) for color_value in colors):
            result = "int"
        elif all(isinstance(color_value, float) for color_value in colors):
            result = "float"
        else:
            raise TypeError("Invalid color type.")
    return result


def is_valid_rgb(colors: Union[ColorInt, ColorFloat]) -> bool:
    """
    Checks if the RGB color values are valid.

    Args:
        colors (Union[ColorInt, ColorFloat]): A tuple or list representing
            color values.

    Returns:
        bool: True if all the RGB values are valid, False otherwise.
    """
    color_type = get_color_type(colors)
    if color_type == "int" and len(colors) == 3:
        return all(0 <= color_value <= 255 for color_value in colors)
    if color_type == "float" and len(colors) == 3:
        return all(0.0 <= color_value <= 1.0 for color_value in colors)
    if color_type == "int float":
        for color in colors:
            if len(color) != 3:
                return False
            if not all(color_value < 0 <= 255 for color_value in colors):
                return False
    return True


def int_color(float_colors: ColorFloat) -> ColorInt:
    """
    Converts a floating point RGB color to an integer RGB color.

    Args:
        float_colors (ColorFloat): A tuple or list representing the RGB color 
            in floating point format.

    Raises:
        ValueError: Raised if the input does not represent a valid RGB color.

    Returns:
        ColorInt: A tuple or list representing the RGB color in integer format.
    """
    int_colors = []
    color_type = get_color_type(float_colors)
    if color_type == "float list":
        for rgb_color in float_colors:
            color = []
            for i in rgb_color:
                if 0 <= i <= 1:
                    color.append(int(i * 255))
                else:
                    raise ValueError("Invalid RGB color.")
            int_colors.append(color)
    elif color_type == "float":
        color = []
        for i in float_colors:
            if 0 <= i <= 1:
                color.append(int(i * 255))
            else:
                raise ValueError("Invalid RGB color.")
        int_colors = color[:]
    else:
        raise ValueError("Invalid RGB color.")
    return int_colors


def float_color(int_colors: ColorInt) -> ColorFloat:
    """
    Converts an integer RGB color to a floating point RGB color.

    Args:
        int_colors (ColorInt): A tuple or list representing the RGB color 
            in integer format.

    Raises:
        ValueError: If the input does not represent a valid RGB color.

    Returns:
        ColorInt: A tuple or list representing the RGB color in floating 
            point format.
    """
    float_colors = []
    color_type = get_color_type(int_colors)
    if color_type == "int list":
        for rgb_color in int_colors:
            color = []
            for i in rgb_color:
                if 0 <= i <= 255:
                    color.append(i / 255.0)
                else:
                    raise ValueError("Invalid RGB color.")
            float_colors.append(color)
    elif color_type == "int":
        color = []
        for i in int_colors:
            if 0 <= i <= 255:
                color.append(int(i / 255.0))
            else:
                raise ValueError("Invalid RGB color.")
        float_colors = color[:]
    else:
        raise ValueError("Invalid RGB color.")
    return float_colors


def set_color(colors: ColorList) -> bool:
    """
    Set the color for the turtle graphics.
    Default to black.

    Args:
        colors (ColorList): A tuple or list representing color values.

    Raises:
        ValueError: Raised if the input is not a valid RGB color list or RGB
            color tuple.

    Returns:
        bool: Returns True if the color is successfully set with a fill color, 
            False if no fill color is set.
    """
    if not colors:
        turtle.color([0, 0, 0])
        return False
    color_type = get_color_type(colors)
    if "int" in color_type:
        colors = float_color(colors)
    if "list" in color_type and len(colors) == 2:
        if len(colors) != 2:
            raise ValueError("Invalid RGB color list or RGB color tuple.")
        turtle.color(colors[0], colors[1])
        return True
    if "list" not in color_type:
        turtle.color(colors)
        return False
    return False


def polygon(side: int, side_length: int, color: OptionalColor = None) -> None:
    """
    This function draws a polygon with the specified number of sides, 
    side length, border color and fill color.
    If side is 0, it will draw a circle instead.
    Set whether to fill based on the provision of fill_color.
    If fill_color is provided, then fill.

    Args:
        side (int): The number of sides of the polygon. 
            If side is 0, a circle will be drawn.
        side_length (int): The length of each side of the polygon.
        color (Optional[RGB]): The border color of the polygon in RGB format. 
            Default to black.
    
    Raises:
        TypeError:
            Raised if side number is not an integer.
        ValueError:
            Raised if side number is not greater than 3 and is not 0.
            Side length is not greater than 0.
    """
    if not color:
        color = []
    if not isinstance(side, int):
        raise TypeError("Number of sides must be an integer.")
    if side < 3 and side != 0:
        raise ValueError("Number of sides must be greater than 3, or 0.")
    if side_length <= 0:
        raise ValueError("Side length must be greater than 0.")
    fill_color = set_color(color)
    if side == 0:
        if fill_color:
            turtle.begin_fill()
            turtle.circle(side_length)
            turtle.end_fill()
        else:
            turtle.circle(side_length / 2)
    if side >= 3:
        angle = 180 - (side - 2) * 180 / side
        if fill_color:
            turtle.begin_fill()
            for _ in range(side):
                turtle.forward(side_length)
                turtle.left(angle)
            turtle.end_fill()
        else:
            for _ in range(side):
                turtle.forward(side_length)
                turtle.left(angle)


def generate_color_gradient(step: int, colors: ColorList) -> ColorList:
    """
    Function to generate a color gradient.

    Args:
        step (int): The number of steps of gradient, controlling the
            level of detail in the gradient effect.
        colors (ColorList): List containing all colors to participate 
            in the gradient.

    Returns:
        ColorList: A list containing RGB color values, representing the 
            sequence of gradient colors from the start color to the 
            end color.
    """
    gradient_colors = []
    colors_number = len(colors)
    step = step // (colors_number - 1) + 1 if colors_number > 1 else step + 1
    for i in range(colors_number - 1):
        start_color = colors[i]
        end_color = colors[i + 1]
        for j in range(step):
            ratio = j / (step - 1) if colors_number > 1 else step
            r = (start_color[0] + (end_color[0] \
                                   - start_color[0]) * ratio) / 255.0
            g = (start_color[1] + (end_color[1] \
                                   - start_color[1]) * ratio) / 255.0
            b = (start_color[2] + (end_color[2] \
                                   - start_color[2]) * ratio) / 255.0
            gradient_colors.append([r, g, b])
        del gradient_colors[-1]
    if get_color_type(colors[-1]) == "float":
        gradient_colors.append(colors[-1])
    elif get_color_type(colors[-1]) == "int":
        gradient_colors.append(float_color(colors[-1]))
    return gradient_colors
