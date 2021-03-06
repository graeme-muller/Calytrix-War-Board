"""

Django Colors
http:///motion-m.ca/projets/django-colors/

Copyright (c) 2010 Maxime Haineault
Licensed under the MIT license.

References:

 - http://www.w3.org/TR/AERT#color-contrast
 - http://docs.python.org/library/colorsys.html
 - http://www.flett.org/2005/04/26/cool-python-tricks/
 - http://www.w3.org/TR/css3-color/#svg-color

"""

from __future__ import division
import colorsys as cs

from django import template

register = template.Library()


NAMED_COLORS = {'aliceblue': 'f0f8ff', 'antiquewhite': 'faebd7', 'aqua': '00ffff', 'aquamarine': '7fffd4', 'azure': 'f0ffff', 'beige': 'f5f5dc', 'bisque':
'ffe4c4', 'black': '000000', 'blanchedalmond': 'ffebcd', 'blue': '0000ff', 'blueviolet': '8a2be2', 'brown': 'a52a2a', 'burlywood': 'deb887', 'cadetblue':
'5f9ea0', 'chartreuse': '7fff00', 'chocolate': 'd2691e', 'coral': 'ff7f50', 'cornflowerblue': '6495ed', 'cornsilk': 'fff8dc', 'crimson': 'dc143c', 'cyan':
'00ffff', 'darkblue': '00008b', 'darkcyan': '008b8b', 'darkgoldenrod': 'b8860b', 'darkgray': 'a9a9a9', 'darkgreen': '006400', 'darkgrey': 'a9a9a9',
'darkkhaki': 'bdb76b', 'darkmagenta': '8b008b', 'darkolivegreen': '556b2f', 'darkorange': 'ff8c00', 'darkorchid': '9932cc', 'darkred': '8b0000', 'darksalmon':
'e9967a', 'darkseagreen': '8fbc8f', 'darkslateblue': '483d8b', 'darkslategray': '2f4f4f', 'darkslategrey': '2f4f4f', 'darkturquoise': '00ced1', 'darkviolet':
'9400d3', 'deeppink': 'ff1493', 'deepskyblue': '00bfff', 'dimgray': '696969', 'dimgrey': '696969', 'dodgerblue': '1e90ff', 'firebrick': 'b22222', 'floralwhite':
'fffaf0', 'forestgreen': '228b22', 'fuchsia': 'ff00ff', 'gainsboro': 'dcdcdc', 'ghostwhite': 'f8f8ff', 'gold': 'ffd700', 'goldenrod': 'daa520', 'gray': '808080',
'green': '008000', 'greenyellow': 'adff2f',  'grey': '808080', 'honeydew': 'f0fff0', 'hotpink': 'ff69b4', 'indianred': 'cd5c5c', 'indigo': '4b0082', 'ivory':
'fffff0', 'khaki': 'f0e68c','lavender': 'e6e6fa', 'lavenderblush': 'fff0f5', 'lawngreen': '7cfc00', 'lemonchiffon': 'fffacd', 'lightblue': 'add8e6',
'lightcoral': 'f08080', 'lightcyan': 'e0ffff', 'lightgoldenrodyellow': 'fafad2', 'lightgray': 'd3d3d3', 'lightgreen': '90ee90', 'lightgrey': 'd3d3d3',
'lightpink': 'ffb6c1', 'lightsalmon': 'ffa07a', 'lightseagreen': '20b2aa', 'lightskyblue': '87cefa', 'lightslategray': '778899', 'lightslategrey': '778899',
'lightsteelblue': 'b0c4de', 'lightyellow': 'ffffe0', 'lime': '00ff00', 'limegreen': '32cd32', 'linen': 'faf0e6', 'magenta': 'ff00ff', 'maroon': '800000',
'mediumaquamarine': '66cdaa', 'mediumblue': '0000cd', 'mediumorchid': 'ba55d3', 'mediumpurple': '9370db', 'mediumseagreen': '3cb371', 'mediumslateblue': '7b68ee',
'mediumspringgreen': '00fa9a', 'mediumturquoise': '48d1cc', 'mediumvioletred': 'c71585', 'midnightblue': '191970', 'mintcream': 'f5fffa', 'mistyrose': 'ffe4e1',
'moccasin': 'ffe4b5', 'navajowhite': 'ffdead', 'navy': '000080', 'oldlace': 'fdf5e6', 'olive': '808000', 'olivedrab': '6b8e23', 'orange': 'ffa500', 'orangered':
'ff4500', 'orchid': 'da70d6', 'palegoldenrod': 'eee8aa', 'palegreen': '98fb98', 'paleturquoise': 'afeeee', 'palevioletred': 'db7093', 'papayawhip': 'ffefd5',
'peachpuff': 'ffdab9', 'peru': 'cd853f', 'pink': 'ffc0cb', 'plum': 'dda0dd', 'powderblue': 'b0e0e6', 'purple': '800080', 'red': 'ff0000', 'rosybrown': 'bc8f8f',
'royalblue': '4169e1', 'saddlebrown': '8b4513', 'salmon': 'fa8072', 'sandybrown': 'f4a460', 'seagreen': '2e8b57', 'seashell': 'fff5ee', 'sienna': 'a0522d',
'silver': 'c0c0c0', 'skyblue': '87ceeb', 'slateblue': '6a5acd', 'slategray': '708090', 'slategrey': '708090', 'snow': 'fffafa', 'springgreen': '00ff7f',
'steelblue': '4682b4', 'tan': 'd2b48c', 'teal': '008080', 'thistle': 'd8bfd8', 'tomato': 'ff6347', 'turquoise': '40e0d0', 'violet': 'ee82ee', 'wheat': 'f5deb3',
'white': 'ffffff', 'whitesmoke': 'f5f5f5', 'yellow': 'ffff00', 'yellowgreen': '9acd32'}


def dec2hex(d):
    """return a two character hexadecimal string representation of integer d"""
    return "%02X" % d


# -- Filters -----------------------


def opposite(x):
    """Returns the opposite color on the HSV color space"""
    x = expand_hex(x)
    if x == '000000':
        return 'ffffff'
    elif x == 'ffffff':
        return '000000'
    else:
        h, s, v = hex_to_hsv(x, False) if len(x) == 6 else x
        if h > 180:
            h = h - 180
        else:
            h = 180 - h
        return hsv_to_hex(h, s, v)


def short_hex(x):
    """Return shorthand hexadecimal code, ex: cc3300 -> c30"""
    t = list(x)
    if t[0] == t[1] and t[2] == t[3] and t[4] == t[5]:
        return '%s%s%s' % (t[0], t[2], t[4])
    else:
        return x


def expand_hex(x):
    """Expands shorthand hexadecimal code, ex: c30 -> cc3300"""
    if len(x) == 3:
        t = list(x)
        return "".join([t[0], t[0], t[1], t[1], t[2], t[2]])
    else:
        return x


def hsv_to_hex(h, s, v):
    """Returns the hexadecimal value of a HSV color"""
    r, g, b = cs.hsv_to_rgb(h/360, s/100, v/100)
    return dec2hex(r*255) + dec2hex(g*255) + dec2hex(b*255)


def hex_to_hsv(x, format_string='%s %s %s'):
    """Returns the HSV value of a hexadecimal color"""
    x = expand_hex(x)
    h, s, v = cs.rgb_to_hsv(int(x[0:2], 16)/255.0, int(x[2:4], 16)/255.0, int(x[4:6], 16)/255.0)
    out = (int(h * 360), int(s * 100), int(v * 100))
    return format_string % out if format_string else out


def hex_to_rgb(x, format_string='%s %s %s'):
    """Returns the RGB value of a hexadecimal color"""
    x = expand_hex(x)
    out = (int(x[0:2], 16), int(x[2:4], 16), int(x[4:6], 16))
    return format_string % out if format_string else out


# -- Filters / HSV manipulations


def lightness(x, value):
    """Set lightness to x, accept hexadecimal or hsv tuple as value"""
    x = expand_hex(x)
    h, s, v = hex_to_hsv(x, False) if len(x) == 6 else x #@UnusedVariable
    return hsv_to_hex(h, s, int(value))


def saturation(x, value):
    """Set saturation to x, accept hexadecimal or hsv tuple as value"""
    x = expand_hex(x)
    h, s, v = hex_to_hsv(x, False) if len(x) == 6 else x #@UnusedVariable
    return hsv_to_hex(h, int(value), v)


def hue(x, value):
    """Set hue to x, accept hexadecimal or hsv tuple as value"""
    x = expand_hex(x)
    h, s, v = hex_to_hsv(x, False) if len(x) == 6 else x #@UnusedVariable
    return hsv_to_hex(int(value), s, v)


def color(name):
    """Returns the hexadecimal value of a named color (ex: black -> 000000)"""
    try:
        return NAMED_COLORS[name]
    except:
        return 'ffffff'

def contrast(x):
    """Returns the hexadecimal value of a color (black or white) which contrasts
       well with the given color"""
    rgb = [int(v) for v in hex_to_rgb(x).split(' ')]
    # green is twice as bright as red, which is twice as bright as blue
    # overall brightness = G*4 + R*2 + B
    # maximum brightness = (255*4 + 255*2 + 255) = 1785, minimum = 0, medium = 892.5
    val = (rgb[1] * 4) + (rgb[0] * 2) + rgb[2]
    if val < 893:
        return 'ffffff'
    return '000000'

register.filter('color',      color)
register.filter('hue',        hue)
register.filter('lightness',  lightness)
register.filter('saturation', saturation)
register.filter('opposite',   opposite)
register.filter('contrast',  contrast)
register.filter('expand_hex', expand_hex)
register.filter('short_hex',  short_hex)
register.filter('hsv_to_hex', hsv_to_hex)
register.filter('hex_to_hsv', hex_to_hsv)
register.filter('hex_to_rgb', hex_to_rgb)
