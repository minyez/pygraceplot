# -*- coding: utf-8 -*-
# pylint: disable=C0326,R0903,C0116,R0205
"""base classes for objects in grace plot"""
import time
from copy import deepcopy
from pygraceplot.map import ColorMap
from pygraceplot.utils import get_int_const, encode_string

plot_colormap = ColorMap()

class _IntMap:
    pair = {None: None}

    @classmethod
    def get(cls, marker):
        return get_int_const(cls.__name__, cls.pair, marker)


class Color(_IntMap):
    """Predefined color constant"""
    WHITE = 0
    BLACK = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5
    BROWN = 6
    GREY = 7
    VIOLET = 8
    CYAN = 9
    MAGENTA = 10
    ORANGE = 11
    INDIGO = 12
    MAROON = 13
    TURQUOISE = 14
    GREEN4 = 15
    pair = {
        "white": WHITE, "w": WHITE,
        "black": BLACK, "k": BLACK,
        "red": RED, "r": RED,
        "green": GREEN, "g": GREEN,
        "blue": BLUE, "b": BLUE,
        "yellow": YELLOW, "y": YELLOW,
        "brown": BROWN,
        "grey": GREY, "gray": GREY, "e": GREY,
        "violet": VIOLET,
        "cyan": CYAN,
        "magenta": MAGENTA,
        "orange": ORANGE,
        "indigo": INDIGO,
        "maroon": MAROON,
        "turquoise": TURQUOISE,
        "green4": GREEN4,
        }
    @classmethod
    def get(cls, marker):
        if marker is None:
            return None
        try:
            return get_int_const(cls.__name__, cls.pair, marker)
        except ValueError:
            return plot_colormap.get(marker)
        raise ValueError


class Pattern(_IntMap):
    """Pattern"""
    NONE = 0
    SOLID = 1
    pair = {
        "none" : NONE,
        "solid": SOLID,
        }


class LineStyle(_IntMap):
    """line style
    """
    NONE = 0
    SOLID = 1
    DOTTED = 2
    DASHED = 3
    LONGDASHED = 4
    DOTDASHED = 5

    pair = {
        "none" : NONE,
        "solid": SOLID, "-": SOLID,
        "dotted": DOTTED, "..": DOTTED,
        "dashed": DASHED, "--": DASHED,
        "longdashed": LONGDASHED, "---": LONGDASHED,
        "dotdashed": DOTDASHED, ".-": DOTDASHED,
        }


class LineType(_IntMap):
    """type of data line
    """
    NONE = 0
    STRAIGHT = 1
    LEFT_STAIRS = 2
    RIGHT_STAIRS = 3
    SEGMENTS = 4
    THREE_SEGMENTS = 5
    INCREASE_X_ONLY = 6
    DECREASE_X_ONLY = 7
    pair = {
        "none": NONE,
        "straight": STRAIGHT,
        "left stairs": LEFT_STAIRS, "stair": LEFT_STAIRS,
        "right stairs": RIGHT_STAIRS, "rstair": RIGHT_STAIRS,
        "segments": SEGMENTS, "seg": SEGMENTS,
        "three segments": THREE_SEGMENTS, "3-seg": THREE_SEGMENTS,
        "increase x only": INCREASE_X_ONLY, "inx": INCREASE_X_ONLY,
        "decrease x only": DECREASE_X_ONLY, "dex": DECREASE_X_ONLY,
        }


class BaseLineType(_IntMap):
    """type of data baseline"""
    ZERO = 0
    SET_MIN = 1
    SET_MAX = 2
    GRAPH_MIN = 3
    GRAPH_MAX = 4
    SET_AVERAGE = 5
    pair = {
        "none": ZERO, "zero": ZERO,
        "setmin": SET_MIN, "smin": SET_MIN,
        "setmax": SET_MAX, "smax": SET_MAX,
        "graphmin": GRAPH_MIN, "gmin": GRAPH_MIN,
        "graphmax": GRAPH_MAX, "gmax": GRAPH_MAX,
        "setaverage": SET_AVERAGE, "average": SET_AVERAGE,
        }


class Just(_IntMap):
    """Justification of text"""
    LEFT = 0
    CENTER = 2
    RIGHT = 1
    LEFT_BOTTOM = 4
    LEFT_MIDDLE = 12
    LEFT_TOP = 8
    CENTER_BOTTOM = 6
    CENTER_MIDDLE = 14
    CENTER_TOP = 10
    RIGHT_BOTTOM = 5
    RIGHT_MIDDLE = 13
    RIGHT_TOP = 9

    pair = {
        "left": LEFT,
        "center": CENTER,
        "right": RIGHT,
        "lb": LEFT_BOTTOM,
        "lm": LEFT_MIDDLE,
        "lt": LEFT_TOP,
        "cb": CENTER_BOTTOM,
        "cm": CENTER_MIDDLE,
        "ct": CENTER_TOP,
        "rb": RIGHT_BOTTOM,
        "rm": RIGHT_MIDDLE,
        "rt": RIGHT_TOP,
        }


class Switch:
    """Class for switch control"""
    ON = 1
    AUTO = -1
    OFF = 0
    pair = {"on": ON, "auto": AUTO, "off": OFF}

    @classmethod
    def get(cls, marker):
        if isinstance(marker, bool):
            return {True: cls.ON, False: cls.OFF}[marker]
        return get_int_const(cls.__name__, cls.pair, marker)
    @classmethod
    def get_str(cls, i):
        """get the corresponding attribute string"""
        d = {cls.ON: "on", cls.AUTO: "auto", cls.OFF: "off",
             True: "on", False: "off", None: "off"}
        return d.get(i)

class Placement(_IntMap):
    """Class for place contorl"""
    BOTH = 0
    NORMAL = 1
    OPPO = 2
    pair = {
        "both": BOTH,
        "normal": NORMAL,
        "n": NORMAL,
        "opposite": OPPO,
        "oppo": OPPO,
        }

    @classmethod
    def get_str(cls, i):
        """get the correspond attribute string"""
        d = {cls.NORMAL: "normal", cls.BOTH: "both", cls.OPPO: "opposite"}
        return d.get(i)

class Pointing(_IntMap):
    """Class for contorl of label pointing"""
    IN = -1
    BOTH = 0
    OUT = 1
    AUTO = 2
    pair = {
        "in": IN,
        "both": BOTH,
        "out": OUT,
        "auto": AUTO,
        }
    @classmethod
    def get_str(cls, i):
        """get the correspond attribute string"""
        d = {cls.IN: "in", cls.BOTH: "both", cls.OUT: "out", cls.AUTO: "auto"}
        return d.get(i)


class _Affix:
    """object to dataset (s0,s1...), graph (g0,g1...), axis (x,y,altx,alty), etc.

    Args:
        affix (str) : the content to add as the affix, 0,1,2 or x,y,altx,alty
        is_prefix (bool) : if True, the content will be added as prefix to object marker
            Otherwise as suffix
    """
    _marker = ""

    def __init__(self, affix, is_prefix=False):
        self._affix = str(affix)
        self._is_prefix = is_prefix
    

class _BaseOutput(object):
    """abstract class for initializing and printing element object

    _attrs and _marker must be redefined,
    with _attrs as a dict, each key is the name for the attribute
    and each value is a 3-member tuple, type, default value and print format
    for the attribute.

    When type is bool, it will be treated invidually as a special
    attribute.
    """
    _attrs = {None: [None, None, None]}
    _marker = ''

    def __init__(self, **kwargs):
        assert isinstance(self._attrs, dict)
        for x in self._attrs.values():
            assert len(x) == 3
        assert isinstance(self._marker, str)
        for attr, (typ, default, _) in self._attrs.items():
            v = kwargs.get(attr, None)
            if v is None:
                v = default
            try:
                self.__getattribute__(attr)
            except AttributeError:
                if typ is not bool:
                    v = typ(v)
                elif attr.endswith('_location'):
                    v = list(v)
                self.__setattr__(attr, v)

    def _set(self, **kwargs):
        """backend method to set attributes"""
        if kwargs:
            if len(kwargs) < len(self._attrs):
                for k, v in kwargs.items():
                    if k in self._attrs and v is not None:
                        self.__setattr__(k, v)
            else:
                for k in self._attrs:
                    v = kwargs.get(k, None)
                    if v is not None:
                        self.__setattr__(k, v)

    # pylint: disable=R0912
    def export(self):
        """export all object attributes as a list of string

        Each member is a line in agr file"""
        slist = []
        prefix = deepcopy(self._marker).replace("_", " ")
        try:
            affix = self.__getattribute__('_affix')
            is_p = self.__getattribute__('_is_prefix')
            if is_p:
                prefix = str(affix) + prefix
            else:
                prefix += str(affix)
        except (TypeError, AttributeError):
            pass

        for attr, (typ, _, f) in self._attrs.items():
            attrv = self.__getattribute__(attr)
            if typ in [list, tuple, set]:
                temps = attr.replace("_", " ") + " " + f.format(*attrv)
            # special property marked by the type as bool
            elif typ is bool:
                # for Symbol
                if attr == "type":
                    temps = f.format(attrv)
                # for on off attribute 
                if attr.endswith("_switch"):
                    temps = attr.replace("_switch", "") + " " + Switch.get_str(attrv)
                # for inout attribute 
                elif attr.endswith("_pointing"):
                    temps = attr.replace("_pointing", "") + " " + Pointing.get_str(attrv)
                elif attr.endswith("_placement"):
                    temps = attr.replace("_placement", "") + " " + Placement.get_str(attrv)
                # for location-like attribute
                elif attr.endswith("_location"):
                    temps = attr.replace("_location", "") + " " + f.format(*attrv)
                # for arbitray string attribute
                elif attr.endswith("_comment"):
                    temps = attr.replace("_comment", "") + " " + encode_string(f.format(attrv))
                # remove the marker name in the attribute to avoid duplicate
                temps = temps.replace(self._marker, "").replace("_", " ")
            else:
                temps = attr.replace("_", " ") + " " + f.format(attrv)
            s = prefix + " " + temps
            slist.append(s)

        # cover extra lines with an _extra_export attribute
        try:
            slist += self.__getattribute__('_extra_export')
        except (TypeError, AttributeError):
            pass

        return slist

    def __str__(self):
        return "\n".join(self.export())

    def __repr__(self):
        return str(self)


class _Region(_BaseOutput, _Affix):
    """Region of plot, i.e. the `r` part"""
    _marker = 'r'
    _attrs = {
        'r_switch': (bool, Switch.OFF, '{:s}'),
        'linestyle': (int, LineStyle.SOLID, '{:d}'),
        'linewidth': (float, 1.0, '{:3.1f}'),
        'type': (str, "above", '{:s}'),
        'color': (int, Color.BLACK, '{:d}'),
        'line': (list, [0., 0., 0., 0.], '{:f}, {:f}, {:f}, {:f}'),
        }

    def __init__(self, index, **kwargs):
        _BaseOutput.__init__(self, **kwargs)
        _Affix.__init__(self, index, is_prefix=False)
        self._link_ig = "0"

    def set_link(self, ig):
        """set the graph to which the region is linked to"""
        self._link_ig = str(ig)

    def export(self):
        """export as a list of string"""
        slist = ["link " + self._marker + self._affix + " to g" + self._link_ig]
        slist += _BaseOutput.export(self)
        return slist

class _TitleLike(_BaseOutput):
    """title and subtitle of graph"""
    _attrs = {
        'font': (int, 0, "{:d}"),
        'size': (float, 1.5, "{:8f}"),
        'color': (int, Color.BLACK, "{:d}"),
        }

class _Title(_TitleLike):
    """title of graph"""
    _marker = 'title'
    _attrs = dict(**_TitleLike._attrs)
    _attrs[_marker+'_comment'] = (bool, "", "\"{:s}\"")

class _SubTitle(_TitleLike):
    """title of graph"""
    _marker = 'subtitle'
    _attrs = dict(**_TitleLike._attrs)
    _attrs[_marker+'_comment'] = (bool, "", "\"{:s}\"")

class _WorldLike(_BaseOutput):
    """super class for object with only one attribute whose
    value is floats separated by comma

    """
    _marker = ''

    def get(self):
        return self.__getattribute__(self._marker + '_location')

    def set(self, loc):
        self.__setattr__(self._marker + '_location', loc)

class _Line(_BaseOutput):
    """Line object of dataset"""
    _marker = 'line'
    _attrs = {
        'type': (int, LineType.STRAIGHT, "{:d}"),
        'linestyle': (int, LineStyle.SOLID, "{:d}"),
        'linewidth': (float, 1.5, "{:3.1f}"),
        'color': (int, Color.BLACK, "{:d}"),
        'pattern': (int, 1, "{:d}"),
        }
    
class _Box(_BaseOutput):
    """Box of legend for internal use"""
    _marker = 'box'
    _attrs = {
        'color': (int, Color.BLACK, '{:d}'),
        'pattern': (int, Pattern.NONE, '{:d}'),
        'linewidth': (float, 1.0, '{:3.1f}'),
        'linestyle': (int, LineStyle.SOLID, '{:d}'),
        'fill_color': (int, Color.BLACK, '{:d}'),
        'fill_pattern': (int, Pattern.NONE, '{:d}'),
        }


class _Legend(_BaseOutput):
    """object to control the appearance of graph legend"""
    _marker = 'legend'
    _attrs = {
        'legend_switch': (bool, Switch.ON, '{:d}'),
        'legend_location': (bool, [0.75, 0.50], '{:6f} , {:6f}'),
        'loctype': (str, 'view', '{:s}'),
        'font': (int, 0, '{:d}'),
        'color': (int, Color.BLACK, '{:d}'),
        'length': (int, 4, '{:d}'),
        'vgap': (int, 1, '{:d}'),
        'hgap': (int, 1, '{:d}'),
        'invert': (str, False, '{:s}'),
        'char_size': (float, 1.2, '{:8f}'),
        }

class _Frame(_BaseOutput, _IntMap):
    """frame"""
    CLOSED = 0
    HALFOPEN = 1
    BREAKTOP = 2
    BREAKBOT = 3
    BREAKLEFT = 4
    BREAKRIGHT = 5
    pair = {
        "closed": CLOSED,
        "halfopen": HALFOPEN,
        "breaktop": BREAKTOP,
        "breakbot": BREAKBOT,
        "breakleft": BREAKLEFT,
        "breakright": BREAKRIGHT,
        }
    _marker = "frame"
    _attrs = {
        'type': (int, 0, "{:d}"),
        'linestyle': (int, LineStyle.SOLID, "{:d}"),
        'linewidth': (float, 1.0, "{:3.1f}"),
        'color': (int, Color.BLACK, "{:d}"),
        'pattern': (int, 1, "{:d}"),
        'background_color': (int, Color.WHITE, "{:d}"),
        'background_pattern': (int, 0, "{:d}"),
        }

class _BaseLine(_BaseOutput):
    """baseline of dataset"""
    _marker = 'baseline'
    _attrs = {
        'type': (int, BaseLineType.ZERO, '{:d}'),
        'baseline_switch': (bool, Switch.OFF, '{:s}'),
        }

class _DropLine(_BaseOutput):
    """baseline of dataset"""
    _marker = 'dropline'
    _attrs = {
        'dropline_switch': (bool, Switch.OFF, '{:s}'),
        }


class _Fill(_BaseOutput, _IntMap):
    """Fill of dataset dropline"""
    NONE = 0
    POLYGON = 1
    BASELINE = 2
    pair = {
        "none": NONE,
        "polygon": POLYGON, "poly": POLYGON, "p": POLYGON,
        "baseline": BASELINE, "b": BASELINE,
        }
    _marker = 'fill'
    _attrs = {
        'type': (int, NONE, '{:d}'),
        'rule': (int, 0, '{:d}'),
        'color': (int, Color.BLACK, '{:d}'),
        'pattern': (int, Pattern.SOLID, '{:d}'),
        }

class _Default(_BaseOutput):
    """_Default options at head"""
    _marker = "default"
    _attrs = {
        "linewidth": (float, 1.5, "{:3.1f}"),
        "linestyle": (int, LineStyle.SOLID, "{:d}"),
        "color": (int, Color.BLACK, "{:d}"),
        "pattern": (int, Pattern.SOLID, "{:d}"),
        "font": (int, 0, "{:d}"),
        "char_size": (float, 1.5, "{:8f}"),
        "symbol_size": (float, 1., "{:8f}"),
        "sformat": (str, "%.8g", "\"{:s}\""),
        }

class AnnotationType(_IntMap):
    """type of annotation value"""
    NONE = 0
    X = 1
    Y = 2
    XY = 3
    STRING = 4
    Z = 5
    pair = {
        "none": NONE,
        "x": X,
        "y": Y,
        "xy": XY,
        "string": STRING, "s": STRING,
        "z": Z,
        }

class _Annotation(_BaseOutput):
    """dataset annotation"""
    _marker = "avalue"
    _attrs = {
        "avalue_switch": (bool, Switch.OFF, "{:s}"),
        "type": (int, AnnotationType.Y, "{:d}"),
        "char_size": (float, 1., "{:8f}"),
        "font": (int, 0, "{:d}"),
        "color": (int, Color.BLACK, "{:d}"),
        "rot": (int, 0, "{:d}"),
        "format": (str, "general", "{:s}"),
        "prec": (int, 3, "{:d}"),
        "append": (str, "\"\"", "{:s}"),
        "prepend": (str, "\"\"", "{:s}"),
        "offset": (list, [0.0, 0.0], "{:8f} , {:8f}"),
        }

class _Symbol(_BaseOutput, _IntMap):
    """Symbols of marker"""
    NONE = 0
    CIRCLE = 1
    SQUARE = 2
    DIAMOND = 3
    TUP = 4
    TLEFT = 5
    TDOWN = 6
    TRIGHT = 7
    PLUS = 8
    CROSS = 9
    STAR  = 10
    CHARACTER = 11

    pair = {
        "none": NONE,
        "circle": CIRCLE, "o": CIRCLE,
        "square": SQUARE,
        "diamond": DIAMOND,
        "tup": TUP, "^": TUP,
        "tleft": TLEFT, "<": TLEFT,
        "tdown": TDOWN, "v": TDOWN,
        "tright": TRIGHT, ">": TRIGHT,
        "plus": PLUS, "+": PLUS,
        "cross": CROSS, "x": CROSS,
        "star": STAR,
        "character": CHARACTER,
    }
    _marker = "symbol"
    _attrs = {
        "type": (bool, CIRCLE, "{:d}"),
        "size": (float, 1., "{:8f}"),
        "color": (int, Color.BLACK, "{:d}"),
        "pattern": (int, Pattern.SOLID, "{:d}"),
        "fill_color": (int, Color.BLACK, "{:d}"),
        "fill_pattern": (int, Pattern.SOLID, "{:d}"),
        "linewidth": (float, 1, "{:3.1f}"),
        "linestyle": (int, LineStyle.SOLID, "{:d}"),
        "char": (int, 1, "{:d}"),
        "char_font": (int, 0, "{:d}"),
        "skip": (int, 0, "{:d}"),
        }


class _Page(_BaseOutput):
    """Page"""
    _marker = "page"
    _attrs = {
        "size": (list, [792, 612], "{:d}, {:d}"),
        "scroll": (float, 0.05, "{:.0%}"),
        "inout": (float, 0.05, "{:.0%}"),
        "background_fill_switch": (bool, Switch.ON, "{:s}"),
        }

class _TimesStamp(_BaseOutput):
    """Timestamp"""
    _marker = "timestamp"
    _attrs = {
        'timestamp_switch': (bool, Switch.OFF, "{:s}"),
        'color': (int, 1, "{:d}"),
        'rot': (int, 0, "{:d}"),
        'font': (int, 0, "{:d}"),
        'char_size': (float, 1.0, "{:8f}"),
        'def': (str, time.strftime("%a %b %d %H:%M:%S %Y"), "\"{:s}\""),
        }

class _Tick(_BaseOutput):
    """Tick of axis
    """
    _marker = 'tick'
    _attrs = {
        'tick_switch': (bool, Switch.ON, "{:s}"),
        'tick_pointing': (bool, Pointing.IN, "{:s}"),
        'default': (int, 6, "{:d}"),
        'major': (float, 1., "{:3.1f}"),
        'major_size': (float, 1.0, "{:8f}"),
        'major_color': (float, 1., "{:3.1f}"),
        'major_linewidth': (float, 1.5, "{:3.1f}"),
        'major_linestyle': (int, LineStyle.SOLID, "{:d}"),
        'major_grid_switch': (bool, Switch.OFF, "{:s}"),
        'minor_color': (float, 1., "{:3.1f}"),
        'minor_size': (float, 0.5, "{:8f}"),
        'minor_ticks': (int, 1, "{:d}"),
        'minor_grid_switch': (bool, Switch.OFF, "{:s}"),
        'minor_linewidth': (float, 1.5, "{:3.1f}"),
        'minor_linestyle': (int, LineStyle.SOLID, "{:d}"),
        'place_rounded': (str, True, "{:s}"),
        'place_placement': (bool, Placement.BOTH, "{:s}"),
        'spec_type': (str, None, "{:s}"),
        }

    def __init__(self, **kwargs):
        _BaseOutput.__init__(self, **kwargs)
        self.spec_ticks = []
        self.spec_labels = []
        self.spec_majors = []

    def export(self):
        slist = _BaseOutput.export(self)
        if self.__getattribute__("spec_type") in ["ticks", "both"]:
            slist.append("{:s} spec {:d}".format(self._marker, len(self.spec_ticks)))
            for i, (loc, m) in enumerate(zip(self.spec_ticks, self.spec_majors)):
                slist.append("{:s} {:s} {:d}, {:.3f}".format(self._marker, m, i, loc))
        if self.__getattribute__("spec_type") == "both":
            for i, (label, m) in enumerate(zip(self.spec_labels, self.spec_majors)):
                if m == "major":
                    slist.append("ticklabel {:d}, \"{:s}\"".format(i, encode_string(label)))
        return slist


class _Bar(_BaseOutput):
    """_Axis bar"""
    _marker = 'bar'
    _attrs = {
        'bar_switch': (bool, Switch.ON, '{:s}'),
        'color': (int, Color.BLACK, '{:d}'),
        'linestyle': (int, LineStyle.SOLID, '{:d}'),
        'linewidth': (float, 1.5, '{:3.1f}'),
        }

class _Label(_BaseOutput):
    """Axis label"""
    _marker = 'label'
    _attrs = {
        'layout': (str, 'para', '{:s}'),
        'place': (str, "auto", '{:s}'),
        'place_location': (bool, [0., 0.], '{:8f}, {:8f}'),
        'char_size': (float, 1.5, "{:8f}"),
        'font': (int, 0, "{:d}"),
        'color': (int, Color.BLACK, "{:d}"),
        'place_placement': (bool, Placement.NORMAL, "{:s}"),
        }

class _TickLabel(_BaseOutput):
    """Label of axis tick"""
    _marker = 'ticklabel'
    _attrs = {
        'ticklabel_switch': (bool, Switch.ON, "{:s}"),
        'format': (str, "general", "{:s}"),
        'formula': (str, "", "\"{:s}\""),
        'append': (str, "", "\"{:s}\""),
        'prepend': (str, "", "\"{:s}\""),
        "prec": (int, 5, "{:d}"),
        'angle': (int, 0, "{:d}"),
        'font': (int, 0, "{:d}"),
        'color': (int, Color.BLACK, "{:d}"),
        'skip': (int, 0, "{:d}"),
        'stagger': (int, 0, "{:d}"),
        'place_placement': (bool, Placement.NORMAL, "{:s}"),
        'offset_switch': (bool, Switch.AUTO, "{:s}"),
        'offset': (list, [0.00, 0.01], "{:8f} , {:8f}"),
        'start_type_switch': (bool, Switch.AUTO, "{:s}"),
        'start': (float, 0.0, "{:8f}"),
        'stop_type_switch': (bool, Switch.AUTO, "{:s}"),
        'stop': (float, 0.0, "{:8f}"),
        'char_size': (float, 1.5, "{:8f}"),
        }

class _Errorbar(_BaseOutput):
    """Errorbar of dataset"""
    _marker = 'errorbar'
    _attrs = {
        'errorbar_switch': (bool, Switch.ON, '{:s}'),
        'place_placement': (bool, Placement.BOTH, '{:s}'),
        'color': (int, Color.BLACK, '{:d}'),
        'pattern': (int, Pattern.SOLID, '{:d}'),
        'size': (float, 1.0, '{:8f}'),
        'linewidth': (float, 1.5, '{:3.1f}'),
        'linestyle': (int, LineStyle.SOLID, '{:d}'),
        'riser_linewidth': (float, 1.5, '{:3.1f}'),
        'riser_linestyle': (int, LineStyle.SOLID, '{:d}'),
        'riser_clip_switch': (bool, Switch.OFF, '{:s}'),
        'riser_clip_length': (float, 0.1, '{:8f}'),
        }

class _Axis(_BaseOutput, _Affix):
    """Axis of graph
    """
    _marker = 'axis'
    _attrs = {
        'axis_switch': (bool, Switch.ON, '{:s}'),
        'type': (list, ["zero", "false"], '{:s} {:s}'),
        'offset': (list, [0.0, 0.0], '{:8f} , {:8f}'),
        }
    def __init__(self, axis, **kwargs):
        assert axis in ['x', 'y', 'altx', 'alty']
        _BaseOutput.__init__(self, **kwargs)
        _Affix.__init__(self, axis, is_prefix=True)

class _Axes(_BaseOutput, _Affix):
    """_Axes object for graph

    Args:
        axes ('x' or 'y')
    """
    _marker = 'axes'
    _attrs = {
        'scale': (str, 'Normal', "{:s}"),
        'invert_switch': (bool, Switch.OFF, "{:s}")
        }
    def __init__(self, axes, **kwargs):
        assert axes in ['x', 'y']
        _BaseOutput.__init__(self, **kwargs)
        _Affix.__init__(self, axes, is_prefix=True)

class _Dataset(_BaseOutput, _Affix):
    """Object of grace dataset"""
    _marker = 's'
    _attrs = {
        'hidden': (str, False, '{:s}'),
        'type': (str, 'xy', '{:s}'),
        'legend': (str, "", "\"{:s}\""),
        'comment': (str, "", "\"{:s}\""),
        }
    def __init__(self, index, **kwargs):
        _BaseOutput.__init__(self, **kwargs)
        _Affix.__init__(self, index, is_prefix=False)

class Arrow(_IntMap):
    """type of line arrow"""
    NONE = 0
    START = 1
    END = 2
    LINE = 0
    FILLED = 1
    OPAQUE = 2
    pair = {
        "none": NONE,
        "start": START,
        "end": END,
        "line": LINE,
        "filled": FILLED,
        "opaque": OPAQUE,
        }


def set_loclike_attr(marker, form, sep, *args):
    f = [form,] * len(args)
    return {marker + '_location': (bool, list(args), sep.join(f))}


class _DrawString(_BaseOutput):
    """class for string drawing"""
    _marker = 'string'
    _attrs = {
        "string_switch": (bool, Switch.ON, '{:s}'),
        # graph number when using for world coordinate
        "string_comment": (bool, "g0", '{:s}'),
        "loctype": (str, "view", '{:s}'),
        "color": (int, Color.BLACK, '{:d}'),
        "rot": (int, 0, '{:d}'),
        "font": (int, 0, '{:d}'),
        "just": (int, Just.LEFT, '{:d}'),
        "char_size": (float, 1.0, '{:.8f}'),
        "def": (str, "", '\"{:s}\"'),
        }
    # add string_location
    _attrs.update(set_loclike_attr(_marker, '{:10f}', ', ', 0.0, 0.0))

class _DrawLine(_BaseOutput):
    """class for line drawing"""
    _marker = 'line'
    _attrs = {
        "line_switch": (bool, Switch.ON, '{:s}'),
        # graph number when using for world coordinate
        "line_comment": (bool, "g0", '{:s}'),
        "loctype": (str, "view", '{:s}'),
        "color": (int, Color.BLACK, '{:d}'),
        "linestyle": (int, LineStyle.SOLID, '{:d}'),
        "linewidth": (float, 1.5, '{:8f}'),
        "arrow": (int, Arrow.NONE, '{:d}'),
        "arrow_type": (int, Arrow.LINE, '{:d}'),
        "arrow_length": (float, 1.0, '{:8f}'),
        "arrow_layout": (list, [1.0, 1.0], '{:8f}, {:8f}'),
        }
    # add string_location
    _attrs.update(set_loclike_attr(_marker, '{:10f}', ', ', 0.0, 0.0, 0.0, 0.0))

class _DrawEllipse(_BaseOutput):
    """class for line drawing"""
    _marker = 'ellipse'
    _attrs = {
        _marker + "_switch": (bool, Switch.ON, '{:s}'),
        # graph number `gn` when using world coordinate
        _marker + "_comment": (bool, "g0", '{:s}'),
        "loctype": (str, "view", '{:s}'),
        "color": (int, Color.BLACK, '{:d}'),
        "linestyle": (int, LineStyle.SOLID, '{:d}'),
        "linewidth": (float, 1.5, '{:8f}'),
        "fill_color": (int, Color.BLACK, '{:d}'),
        "fill_pattern": (int, Pattern.SOLID, '{:d}'),
        }
    # add string_location
    _attrs.update(set_loclike_attr(_marker, '{:10f}', ', ', 0.0, 0.0, 0.0, 0.0))

class _Graph(_BaseOutput, _Affix):
    """Graph object, similar to Axes in matplotlib
    """
    _marker = 'g'
    _attrs = {
        'hidden': (str, False, '{:s}'),
        'type': (str, 'XY', '{:s}'),
        'stacked': (str, False, '{:s}'),
        'bar_hgap': (float, 0.0, '{:8f}'),
        'fixedpoint_switch': (bool, Switch.OFF, '{:s}'),
        'fixedpoint_type': (int, 0, '{:d}'),
        'fixedpoint_xy': (list, [0.0, 0.0], '{:8f}, {:8f}'),
        'fixedpoint_format': (list, ['general', 'general'], '{:s} {:s}'),
        'fixedpoint_prec': (list, [6, 6], '{:d}, {:d}'),
        }
    def __init__(self, index, **kwargs):
        self._index = index
        _BaseOutput.__init__(self, **kwargs)
        _Affix.__init__(self, index, is_prefix=False)

