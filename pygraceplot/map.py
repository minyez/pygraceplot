# -*- coding: utf-8 -*-
# pylint: disable=C0326,R0903,C0116
"""class related to map, e.g. colors and fonts"""
from copy import deepcopy

class _MapOutput:
    """class for write map output, e.g. font, colormap

    the main attribute is a private dictionary, _map and an output format _format
    for the mapped values

    key : int/str/float, identifier of mapping
    value : tuple/list, value mapped

    """
    _marker = None
    _map = None
    _format = '{:s}'

    def __init__(self, marker, mapdict, form):
        self._marker = marker
        self._map = deepcopy(mapdict)
        self._format = form

    def export(self):
        """export information as a list of strings"""
        slist = []
        for k, v in self._map.items():
            s = "map {:s} {:s} to ".format(self._marker, str(k)) + self._format.format(*v)
            slist.append(s)
        return slist


def _valid_rgb(r, g, b, name):
    """Check if RGB value is valid. Give warning if it is not"""
    d = {"R": r, "G": g, "B": b}
    for k, v in d.items():
        if v not in range(256):
            _logger.warning("%s (%s value of %s) is not a valid RGB", v, k, name)

class ColorMap(_MapOutput):
    """Class to map the color
    
    Private attribute:
        _map (dict) : color map
        _cn (dict) : color names

    TODO add system configure
    """
    _format = '({:d}, {:d}, {:d}), \"{:s}\"'
    # a pre-defined color map list
    _colors = [
        (255, 255, 255, "white"),
        (  0,   0,   0, "black"),
        (255,   0,   0, "red"),
        (  0, 255,   0, "green"),
        (  0,   0, 255, "blue"),
        (255, 255,   0, "yellow"),
        (188, 143, 143, "brown"),
        (220, 220, 220, "grey"),
        (148,   0, 211, "violet"),
        (  0, 255, 255, "cyan"),
        (255,   0, 255, "magenta"),
        (255, 165,   0, "orange"),
        (114,  33, 188, "indigo"),
        (103,   7,  72, "maroon"),
        ( 64, 224, 208, "turquoise"),
        (  0, 139,   0, "green4"),
        ]

    def __init__(self, load_custom: bool = True):
        # add user defined color_map
        # user is not allowed to overwrite color
        _colors = deepcopy(ColorMap._colors)
        if load_custom:
            try:
                from pygraceplot.__config__ import color_map
                for c in color_map:
                    _valid_rgb(*c)
                    _colors.append(c)
                del color_map
            except (TypeError, ValueError):
                _logger.warning("user color_map is not loaded correctly")
            except ImportError:
                pass
        # check validity of pre-defined colormap
        # check if predefined rgb are valid, and there is no duplicate names
        _color_names = [i[3] for i in _colors]
        for color in _colors:
            _valid_rgb(*color)
        if len(_color_names) != len(set(_color_names)):
            raise ValueError('found duplicate color names:', _color_names)

        _map = {}
        for i, color in enumerate(_colors):
            _map[i] = color
        _MapOutput.__init__(self, 'color', _map, ColorMap._format)
        self._cn = _color_names

    def __getitem__(self, i):
        return self._map[i][3]

    def __str__(self):
        return '\n'.join(self.export())

    def export(self):
        """export color maps

        Returns
            list
        """
        return _MapOutput.export(self)

    @property
    def n(self):
        """Number of available colors"""
        return len(self._cn)

    def get(self, color):
        """return the color code

        Args:
            color (str, int)

        Returns:
            int
        """
        if isinstance(color, str):
            return self._get_color_code(color)
        if isinstance(color, int):
            if color in self._map:
                return color
            raise ValueError("color {:d} is not defined in the color map".format(color))
        raise TypeError("color input is not valid, use str or int", color)

    @property
    def names(self):
        """color names"""
        return self._cn

    def add(self, r, g, b, name=None):
        """Add a new color with its RGB value

        Args:
            r, g, b (int)
        """
        if name is None:
            name = 'color' + str(self.n)
        elif name in self._cn:
            msg = "color {:s} has been defined with code {:s}".format(name, self._cn.index(name))
            raise ValueError(msg)
        color = (r, g, b, name)
        _valid_rgb(*color)
        if self._colors is ColorMap._colors:
            self._colors = deepcopy(ColorMap._colors)
        self._colors.append(color)
        self._map[self.n] = color
        self._cn.append(name)

    def get_color_code(self, name):
        """get the map code of color `name`

        Args:
            name (str) : name of color, case-insensitive
        """
        try:
            return self._cn.index(name.lower())
        except ValueError:
            raise ValueError("color name {:s} is not found".format(name))

    def get_rgb(self, i):
        """get the rgb value of color with its code"""
        r, g, b, _ = self._map[i]
        return r, g, b

    def has_color(self, name):
        """Check if the color name is already defined"""
        return name in self._cn


class FontMap(_MapOutput):
    """Object to set up the font map

    For now adding fonts is not supported"""
    _fonts = [
        "Times-Roman",
        "Times-Italic",
        "Times-Bold",
        "Times-BoldItalic",
        "Helvetica",
        "Helvetica-Oblique",
        "Helvetica-Bold",
        "Helvetica-BoldOblique",
        "Courier",
        "Courier-Oblique",
        "Courier-Bold",
        "Courier-BoldOblique",
        "Symbol",
        "ZapfDingbats",
        ]
    _marker = 'font'
    _format = "\"{:s}\", \"{:s}\""
    _map = {}
    for i, f in enumerate(_fonts):
        _map[i] = (f, f)

    def __init__(self):
        _MapOutput.__init__(self, FontMap._marker, FontMap._map, FontMap._format)

    def export(self):
        """return a list of font map strings"""
        return _MapOutput.export(self)

    def __str__(self):
        return "\n".join(self.export())

