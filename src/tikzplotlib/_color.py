import matplotlib as mpl
import numpy as np
import webcolors as wc

# RGB values (as taken from xcolor.dtx):
builtin_colors = {
    "white": [1, 1, 1],
    "lightgrey": [0.75, 0.75, 0.75],
    "grey": [0.5, 0.5, 0.5],
    "darkgrey": [0.25, 0.25, 0.25],
    "black": [0, 0, 0],
    #
    "red": [1, 0, 0],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
    "brown": [0.75, 0.5, 0.25],
    "lime": [0.75, 1, 0],
    "orange": [1, 0.5, 0],
    "pink": [1, 0.75, 0.75],
    "purple": [0.75, 0, 0.25],
    "teal": [0, 0.5, 0.5],
    "violet": [0.5, 0, 0.5],
    # The colors cyan, magenta, yellow, and olive are also
    # predefined by xcolor, but their RGB approximation of the
    # native CMYK values is not very good. Don't use them here.
}

def get_closest_color_name(rgb):
    min_colors = {}
    
    for name in wc.names("css3"):
        r_c, g_c, b_c = wc.name_to_rgb(name)
        
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        
        distance = rd + gd + bd
        min_colors[distance] = name
        
    return min_colors[min(min_colors.keys())]

def get_color_name(rgb):
    try:
        return wc.rgb_to_name(rgb)
    except ValueError:
        return get_closest_color_name(rgb)


def mpl_color2xcolor(data, matplotlib_color):
    """Translates a matplotlib color specification into a proper LaTeX xcolor."""
    # Convert it to RGBA.
    my_col = np.array(mpl.colors.ColorConverter().to_rgba(matplotlib_color))

    # If the alpha channel is exactly 0, then the color is really 'none'
    # regardless of the RGB channels.
    if my_col[-1] == 0.0:
        return data, "none", my_col

    # Check if it exactly matches any of the colors already available.
    for name, rgb in builtin_colors.items():
        if all(my_col[:3] == rgb):
            return data, name, my_col

    # convert to RGB255
    rgb255 = np.array(my_col[:3] * 255, dtype=int)
    color_name = get_color_name(rgb255)
    # create a new color name
    if all(rgb255 == rgb255[0]):
        name = f"{color_name}{rgb255[0]}"
    else:
        name = f"{color_name}{rgb255[0]}{rgb255[1]}{rgb255[2]}"
    data["custom colors"][name] = ("RGB", ",".join([str(val) for val in rgb255]))
    return data, name, my_col
