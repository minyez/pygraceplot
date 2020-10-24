# -*- coding: utf-8 -*-
# pylint: disable=C0326,R0903,C0116
r"""A high-level Python interface to the Grace plotting package

The main purpose of this implementation is to write grace plot file
with similar methods to matplotlib, and without any concern about
whether xmgrace is installed or not.
Therefore, platform-related functions are generally discarded. (minyez)
"""
import sys
from io import TextIOWrapper, StringIO
from collections.abc import Iterable

from numpy import shape, absolute, loadtxt

from pygraceplot.map import FontMap
from pygraceplot.base import (plot_colormap, set_loclike_attr,
                              Color, Switch, LineStyle, Pattern, Justf, Arrow, Position,
                              _Region, _Graph, _WorldLike,
                              _BaseLine, _DropLine, _Annotation, _Symbol,
                              _Line, _Box, _Legend, _Frame, _Axis, _Axes,
                              _Fill, _Default, _Dataset, _TimesStamp, _Page,
                              _Bar, _Errorbar,
                              _Title, _SubTitle, _Label, _Tick, _TickLabel,
                              _DrawString, _DrawLine, _DrawEllipse)
from pygraceplot.data import Data
from pygraceplot.utils import encode_string
from pygraceplot.logger import create_logger

_logger = create_logger("Plot")
del create_logger

class Region(_Region):
    """user interface of region"""
    def __init__(self, index, switch=None, ls=None, lw=None, rt=None,
                 color=None, line=None, **kwargs):
        _Region.__init__(self, index, r_switch=Switch.get(switch), linestyle=LineStyle.get(ls),
                         linewidth=lw, type=rt, color=Color.get(color), line=line)
        _raise_unknown_attr(self, *kwargs)

    def set(self, switch=None, ls=None, lw=None, rt=None,
            color=None, line=None, **kwargs):
        self._set(r_switch=Switch.get(switch), linestyle=LineStyle.get(ls), linewidth=lw,
                  type=rt, color=Color.get(color), line=line)
        _raise_unknown_attr(self, *kwargs)


class Title(_Title):
    """user interface of title"""
    def __init__(self, title=None, font=None, fontsize=None, color=None, **kwargs):
        _Title.__init__(self, title_comment=encode_string(title), size=fontsize,
                        color=Color.get(color), font=font)
        _raise_unknown_attr(self, *kwargs)
    
    def set(self, title=None, font=None, fontsize=None, color=None, **kwargs):
        self._set(title_comment=encode_string(title),
                  size=fontsize, color=Color.get(color), font=font)
        _raise_unknown_attr(self, *kwargs)

    @property
    def title(self):
        return self.title_comment

class SubTitle(_SubTitle):
    """user interface of title"""
    def __init__(self, subtitle=None, font=None, fontsize=None, color=None, **kwargs):
        _SubTitle.__init__(self, subtitle_comment=encode_string(subtitle), size=fontsize,
                           color=Color.get(color), font=font)
        _raise_unknown_attr(self, *kwargs)

    def set(self, subtitle=None, font=None, fontsize=None, color=None, **kwargs):
        self._set(subtitle_comment=encode_string(subtitle),
                  size=fontsize, color=Color.get(color), font=font)
        _raise_unknown_attr(self, *kwargs)

    @property
    def subtitle(self):
        return self.subtitle_comment


class World(_WorldLike):
    """world of graph"""
    _marker = 'world'
    _attrs = set_loclike_attr(_marker, '{:8f}', 0., 0., 1., 1.)

    def __init__(self, **kwargs):
        _WorldLike.__init__(self, **kwargs)
        self.set_world = self.set
        self.get_world = self.get

class StackWorld(_WorldLike):
    """stack world of graph"""
    _marker = 'stack_world'
    _attrs = set_loclike_attr(_marker, '{:8f}', 0., 1., 0., 1.)

class View(_WorldLike):
    """View of graph on the image canvas """
    _marker = 'view'
    _attrs = set_loclike_attr(_marker, '{:8f}', 0.15, 0.10, 1.20, 0.85)

    def __init__(self, **kwargs):
        _WorldLike.__init__(self, **kwargs)
        self.set_view = self.set
        self.get_view = self.get

class Znorm(_WorldLike):
    """stack world of graph"""
    _marker = 'znorm'
    _attrs = set_loclike_attr('znorm', '{:d}', 1)

def _raise_unknown_attr(obj, *attrs):
    if attrs:
        raise ValueError("unsupported attributes for {:s}:".format(type(obj).__name__),
                         *attrs)

class Line(_Line):
    """User interface of line object"""
    def __init__(self, lt=None, color=None, pattern=None, width=None, style=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Line.__init__(self, type=lt, color=Color.get(color), pattern=Pattern.get(pattern),
                       linewidth=width, linestyle=LineStyle.get(style))

    def set(self, lt=None, color=None, pattern=None, width=None, style=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(type=lt, color=Color.get(color), pattern=Pattern.get(pattern),
                  linewidth=width, linestyle=LineStyle.get(style))


class Box(_Box):
    """User interface of box of legend"""
    def __init__(self, color=None, pattern=None, lw=None, ls=None,
                 fc=None, fp=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Box.__init__(self, color=Color.get(color), pattern=Pattern.get(pattern), linewidth=lw,
                      linestyle=LineStyle.get(ls), fill_color=Color.get(fc),
                      fill_pattern=Pattern.get(fp))

    def set(self, color=None, pattern=None, lw=None, ls=None,
            fc=None, fp=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(color=Color.get(color), pattern=Pattern.get(pattern), linewidth=lw,
                  linestyle=LineStyle.get(ls), fill_color=Color.get(fc),
                  fill_pattern=Pattern.get(fp))


# pylint: disable=too-many-locals
class Legend(_Legend):
    """User interface of legend object"""
    def __init__(self, switch=None, loc=None, loctype=None, font=None,
                 color=None, length=None, vgap=None, hgap=None, invert=None,
                 charsize=None,
                 bc=None, bp=None, blw=None, bls=None, bfc=None, bfp=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Legend.__init__(self, legend_switch=Switch.get(switch), legend_location=loc,
                         loctype=loctype, font=font, color=Color.get(color),
                         length=length, vgap=vgap, hgap=hgap, invert=invert, char_size=charsize)
        self.box = Box(color=bc, pattern=bp, lw=blw, ls=bls, fc=bfc, fp=bfp)

    def export(self):
        return _Legend.export(self) + [self._marker + " " + i for i in self.box.export()]

    def set(self, switch=None, loc=None, loctype=None, font=None,
            color=None, length=None, vgap=None, hgap=None, invert=None,
            charsize=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(legend_switch=Switch.get(switch), legend_location=loc, loctype=loctype,
                  font=font, color=Color.get(color), length=length, vgap=vgap, hgap=hgap,
                  invert=invert, char_size=charsize)

    def set_box(self, **kwargs):
        """set the attribute of legend box"""
        self.box.set(**kwargs)


class Frame(_Frame):
    """User interface of frame"""
    def __init__(self, ft=None, ls=None, lw=None, color=None, pattern=None,
                 bgc=None, bgp=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Frame.__init__(self, type=_Frame.get(ft), linestyle=LineStyle.get(ls), linewidth=lw,
                        color=Color.get(color), pattern=Pattern.get(pattern), 
                        background_pattern=Pattern.get(bgp),
                        background_color=Color.get(bgc))

    def set(self, ft=None, ls=None, lw=None, color=None, pattern=None,
            bgc=None, bgp=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(type=_Frame.get(ft), linestyle=LineStyle.get(ls), linewidth=lw,
                  color=Color.get(color), pattern=Pattern.get(pattern), 
                  background_pattern=Pattern.get(bgp),
                  background_color=Color.get(bgc))


class BaseLine(_BaseLine):
    """User interface of baseline"""
    def __init__(self, lt=None, switch=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _BaseLine.__init__(self, type=lt, baseline_switch=Switch.get(switch))
    
    def set(self, lt=None, switch=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(type=lt, baseline_switch=Switch.get(switch))


class DropLine(_DropLine):
    """user interface of dataset baseline"""
    def __init__(self, switch=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _DropLine.__init__(self, dropline_switch=Switch.get(switch))

    def set(self, switch=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(dropline_switch=Switch.get(switch))


class Fill(_Fill):
    """User interface of fill"""
    def __init__(self, ft=None, rule=None, color=None, pattern=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Fill.__init__(self, type=_Fill.get(ft), rule=rule, color=Color.get(color),
                       pattern=Pattern.get(pattern))
    
    def set(self, ft=None, rule=None, color=None, pattern=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(type=_Fill.get(ft), rule=rule, color=Color.get(color),
                  pattern=Pattern.get(pattern))


class Default(_Default):
    """User interface of default setup"""
    def __init__(self, lw=None, ls=None, color=None, pattern=None, font=None,
                 charsize=None, symbolsize=None, sformat=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Default.__init__(self, linewidth=lw, linestyle=LineStyle.get(ls),
                          pattern=Pattern.get(pattern), color=Color.get(color),
                          font=font, char_size=charsize, symbol_size=symbolsize,
                          sformat=sformat)

    def set(self, lw=None, ls=None, color=None, pattern=None, font=None,
            charsize=None, symbolsize=None, sformat=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(linewidth=lw, linestyle=LineStyle.get(ls),
                  pattern=Pattern.get(pattern), color=Color.get(color),
                  font=font, char_size=charsize, symbol_size=symbolsize,
                  sformat=sformat)


class Annotation(_Annotation):
    """user interface of data annotation"""
    def __init__(self, switch=None, at=None, rot=None, color=None, prec=None, font=None,
                 charsize=None, offset=None, append=None, prepend=None, af=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Annotation.__init__(self, avalue_switch=Switch.get(switch), type=at, char_size=charsize,
                             font=font, color=Color.get(color), rot=rot, format=af, prec=prec,
                             append=append, prepend=prepend, offset=offset)

    def set(self, switch=None, at=None, rot=None, color=None, prec=None, font=None,
            charsize=None, offset=None, append=None, prepend=None, af=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(avalue_switch=Switch.get(switch), type=at, char_size=charsize,
                  font=font, color=Color.get(color), rot=rot, format=af, prec=prec,
                  append=append, prepend=prepend, offset=offset)

class Symbol(_Symbol):
    """user interface of symbol"""
    def __init__(self, st=None, size=None, color=None, pattern=None,
                 fc=None, fp=None, lw=None, ls=None, char=None, charfont=None, skip=None,
                 **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Symbol.__init__(self, type=_Symbol.get(st), size=size, color=Color.get(color),
                         pattern=Pattern.get(pattern), fill_color=Color.get(fc),
                         fill_pattern=Pattern.get(fp), linewidth=lw, linestyle=LineStyle.get(ls),
                         char=char, char_font=charfont, skip=skip)

    def set(self, st=None, size=None, color=None, pattern=None,
            fc=None, fp=None, lw=None, ls=None, char=None, charfont=None, skip=None,
            **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(type=st, size=size, color=Color.get(color),
                  pattern=Pattern.get(pattern), fill_color=Color.get(fc),
                  fill_pattern=Pattern.get(fp), linewidth=lw, linestyle=LineStyle.get(ls),
                  char=char, char_font=charfont, skip=skip)

class Page(_Page):
    """user interface of page"""
    def __init__(self, size=None, scroll=None, inout=None, bgfill=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Page.__init__(self, size=size, scroll=scroll, inout=inout,
                       background_fill_switch=Switch.get(bgfill))

    def set(self, size=None, scroll=None, inout=None, bgfill=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(size=size, scroll=scroll, inout=inout,
                  background_fill_switch=Switch.get(bgfill))

class TimesStamp(_TimesStamp):
    """User interface of timestamp"""
    def __init__(self, switch=None, color=None, rot=None, font=None, charsize=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _TimesStamp.__init__(self, timestamp_switch=Switch.get(switch), color=Color.get(color),
                             rot=rot, font=font, char_size=charsize)

    def set(self, switch=None, color=None, rot=None, font=None, charsize=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(timestamp_switch=Switch.get(switch), color=Color.get(color),
                  rot=rot, font=font, char_size=charsize)

class Tick(_Tick):
    """User interface of axis tick"""
    def __init__(self, major=None, mjc=None, mjs=None, mjlw=None, mjls=None, mjg=None,
                 mic=None, mis=None, mit=None,
                 milw=None, mils=None, mig=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Tick.__init__(self, major=major, major_color=Color.get(mjc), major_size=mjs,
                       major_grid_switch=Switch.get(mjg), major_linewidth=mjlw,
                       major_linestyle=LineStyle.get(mjls),
                       minor_color=Color.get(mic), minor_size=mis, minor_ticks=mit,
                       minor_grid_switch=Switch.get(mig), minor_linewidth=milw,
                       minor_linestyle=LineStyle.get(mils))

    def set(self, major=None, mjc=None, mjs=None, mjlw=None, mjls=None, mjg=None,
            mic=None, mis=None, mit=None, milw=None, mils=None,
            mig=None, **kwargs):
        """setup axis ticks
        Args:
            major (float) : distance between major ticks
            mjc, mic (str or int) : color of major and minor ticks
            mjs, mis (str or int) : tick style of major and minor ticks
        """
        _raise_unknown_attr(self, *kwargs)
        self._set(major=major, major_color=Color.get(mjc), major_size=mjs,
                  major_grid_switch=Switch.get(mjg), major_linewidth=mjlw,
                  major_linestyle=LineStyle.get(mjls),
                  minor_color=Color.get(mic), minor_size=mis, minor_ticks=mit,
                  minor_grid_switch=Switch.get(mig), minor_linewidth=milw,
                  minor_linestyle=LineStyle.get(mils))

    def set_major(self, major=None, color=None, size=None,
                  lw=None, ls=None, grid=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(major=major, major_color=Color.get(color), major_size=size,
                  major_grid_switch=Switch.get(grid),
                  major_linewidth=lw, major_linestyle=LineStyle.get(ls))

    def set_minor(self, color=None,
                  size=None, ticks=None, grid=None,
                  lw=None, ls=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(minor_color=Color.get(color), minor_size=size,
                  minor_ticks=ticks, minor_grid_switch=Switch.get(grid),
                  minor_linewidth=lw, minor_linestyle=LineStyle.get(ls))

    def set_place(self, rounded=None, place=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(place_rounded=rounded, place_position=Position.get(place))

    def set_spec(self, locs, labels=None, use_minor=None):
        """set custom specific ticks on axis.

        Note that locs should have same length as labels

        Args:
            locs (Iterable) : locations of custom ticks on the axis
            labels (Iterable) : labels of custom ticks
            use_minor (Iterable) : index of labels to use minor tick
        """
        if not isinstance(locs, Iterable):
            raise TypeError("locs should be Iterable, but got ", type(locs))
        self.__setattr__("spec_type", "ticks")
        spec_ticks = locs
        if labels is not None:
            if len(labels) != len(locs):
                raise ValueError("labels should have the same length as locs")
            self.spec_labels.extend(encode_string(str(l)) for l in labels)
            self.__setattr__("spec_type", "both")
        spec_major = ["major" for _ in locs]
        if use_minor:
            for i in use_minor:
                spec_major[i] = "minor"
        self.spec_ticks.extend(spec_ticks)
        self.spec_majors.extend(spec_major)

class Bar(_Bar):
    """User interface of axis bar"""
    def __init__(self, switch=None, color=None, ls=None, lw=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Bar.__init__(self, bar_switch=switch, color=color, linestyle=ls, linewidth=lw)

    def set(self, switch=None, color=None, ls=None, lw=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(bar_switch=Switch.get(switch),
                  color=Color.get(color), linestyle=LineStyle.get(ls), linewidth=lw)

class Label(_Label):
    """user interface of axis label"""
    def __init__(self, label=None, layout=None, position=None, charsize=None,
                 font=None, color=None, place=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self.label = label
        if label is None:
            self.label = ""
        self.label = self.label
        _Label.__init__(self, layout=layout, place_position=Position.get(position),
                        char_size=charsize, font=font, color=Color.get(color), place=place)

    def set(self, s=None, layout=None, position=None, charsize=None, font=None,
            color=None, place=None, **kwargs):
        """set the label to s

        Args:
            s (str or string-convertable) : the label of the axis
        """
        _raise_unknown_attr(self, *kwargs)
        if s:
            self.label = encode_string(str(s))
        self._set(layout=layout, color=Color.get(color),
                  place_position=Position.get(position), char_size=charsize,
                  font=font, place=place)

    def export(self):
        _logger.debug("exporting label: %s", self.label)
        slist = [self._marker + " \"{:s}\"".format(encode_string(self.label)),]
        slist += _Label.export(self)
        return slist

# pylint: disable=too-many-locals
class TickLabel(_TickLabel):
    """user interface of label of axis tick

    Args:
        switch (bool) : switch of tick label
        tlf (str) : ticklabel format
        formular (str)
    """
    def __init__(self, switch=None, tlf=None, formula=None, append=None, prepend=None, prec=None,
                 angle=None, font=None, color=None, skip=None, stagger=None,
                 place=None, offset=None, offset_switch=None, charsize=None,
                 start=None, stop=None, start_switch=None, stop_switch=None,
                 **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _TickLabel.__init__(self, ticklabel_switch=Switch.get(switch),
                            format=tlf, formula=formula,
                            append=append, prepend=prepend, prec=prec, angle=angle, font=font,
                            color=Color.get(color), skip=skip, stagger=stagger, place=place,
                            offset_switch=Switch.get(offset_switch), offset=offset,
                            char_size=charsize, start=start,
                            start_type_switch=Switch.get(start_switch),
                            stop=stop, stop_type_switch=Switch.get(stop_switch))

    def set(self, switch=None, tlf=None, formula=None, append=None, prepend=None, prec=None,
            angle=None, font=None, color=None, skip=None, stagger=None,
            place=None, offset=None, offset_switch=None, charsize=None,
            start=None, stop=None, start_switch=None, stop_switch=None,
            **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(ticklabel_switch=Switch.get(switch), format=tlf, formula=formula, append=append,
                  prepend=prepend, prec=prec, angle=angle, font=font, color=Color.get(color),
                  skip=skip, stagger=stagger, place=place, offset_switch=Switch.get(offset_switch),
                  offset=offset, start=start, start_type_switch=Switch.get(start_switch),
                  stop=stop, stop_type_switch=Switch.get(stop_switch), char_size=charsize)

class Errorbar(_Errorbar):
    """User interface of dataset errorbar appearance"""
    def __init__(self, switch=None, position=None, color=None, pattern=None, size=None,
                 lw=None, ls=None, rlw=None, rls=None, rc=None, rcl=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Errorbar.__init__(self, errorbar_switch=Switch.get(switch),
                           place_position=Position.get(position), color=Color.get(color),
                           pattern=Pattern.get(pattern), size=size, linewidth=lw,
                           linestyle=LineStyle.get(ls), riser_linewidth=rlw,
                           riser_linestyle=LineStyle.get(rls), riser_clip_switch=Switch.get(rc),
                           riser_clip_length=rcl)

    def set(self, switch=None, position=None, color=None, pattern=None, size=None,
            lw=None, ls=None, rlw=None, rls=None, rc=None, rcl=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(errorbar_switch=Switch.get(switch),
                  place_position=Position.get(position), color=Color.get(color),
                  pattern=Pattern.get(pattern), size=size, linewidth=lw,
                  linestyle=LineStyle.get(ls), riser_linewidth=rlw,
                  riser_linestyle=LineStyle.get(rls), riser_clip_switch=Switch.get(rc),
                  riser_clip_length=rcl)

class Axis(_Axis):
    """user interface of graph axis apperance

    Args:
        axis (str) : in ['x', 'y', 'altx', 'alty']
        switch (bool): 
        at (str) : axis type
        offset (2-member list):
        bar (bool)
        bc (str/int) : bar color
        bls (str/int) : bar line style
        blw (number)
        mjls (str/int) : major tick line style
    """

    def __init__(self, axis, switch=None, at=None, offset=None,
                 bar=None, bc=None, bls=None, blw=None,
                 major=None, mjc=None, mjs=None, mjlw=None, mjls=None, mjg=None,
                 mic=None, mis=None, mit=None,
                 milw=None, mils=None, mig=None,
                 label=None, layout=None, position=None, lsize=None,
                 lfont=None, lc=None, lplace=None,
                 ticklabel=None, tlf=None, formula=None, append=None, prepend=None,
                 angle=None, tlfont=None, tlc=None, skip=None, stagger=None,
                 tlplace=None, tloffset=None, tlo_switch=None, tlsize=None,
                 start=None, stop=None, start_switch=None, stop_switch=None,
                 **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Axis.__init__(self, axis, axis_switch=Switch.get(switch), type=at, offset=offset)
        self._bar = Bar(switch=bar, color=bc, ls=bls, lw=blw)
        self._tick = Tick(major=major, mjc=mjc, mjs=mjs, mjlw=mjlw, mjls=mjls, mjg=mjg,
                          mic=mic, mis=mis, mit=mit, milw=milw, mils=mils, mig=mig)
        self._label = Label(label=label, layout=layout, position=position, charsize=lsize,
                            font=lfont, color=lc, place=lplace)
        self._ticklabel = TickLabel(switch=ticklabel, tlf=tlf, formula=formula, append=append,
                                    prepend=prepend, angle=angle, font=tlfont, color=tlc,
                                    skip=skip, stagger=stagger, offset=tloffset, charsize=tlsize,
                                    offset_switch=tlo_switch, start=start, stop=stop, place=tlplace,
                                    start_switch=start_switch, stop_switch=stop_switch)

    def set(self, switch=None, at=None, offset=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(axis_switch=Switch.get(switch), type=at, offset=offset)

    def export(self):
        if self.axis_switch is Switch.OFF:
            return [self._affix + self._marker + "  " + Switch.get_str(Switch.OFF),]
        slist = _Axis.export(self) 
        header = [self._bar, self._label, self._tick, self._ticklabel]
        for x in header:
            slist += [self._affix + self._marker + " " + i for i in x.export()]
        return slist

    def bind(self, *axis):
        """Bind Axis objects

        Args:
            axis (Axis) : 
        """

    def set_major(self, **kwargs):
        """set major ticks"""
        self._tick.set_major(**kwargs)

    def set_minor(self, **kwargs):
        """set minor ticks"""
        self._tick.set_minor(**kwargs)

    def set_bar(self, **kwargs):
        self._bar.set(**kwargs)

    def set_tick(self, **kwargs):
        self._tick.set(**kwargs)

    def set_ticklabel(self, **kwargs):
        self._ticklabel.set(**kwargs)

    def set_label(self, s=None, **kwargs):
        """set the label of axis"""
        self._label.set(s, **kwargs)

    def set_spec(self, locs, labels=None, use_minor=False):
        """set specific tick marks and labels

        Args:
            locs (Iterable)
            labels (Iterable)
        """
        self._tick.set_spec(locs, labels=labels, use_minor=use_minor)

class Axes(_Axes):
    """User interface of axes"""
    def __init__(self, axes, scale=None, invert=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Axes.__init__(self, axes, scale=scale, invert_switch=Switch.get(invert))

    def set(self, scale=None, invert=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(scale=scale, invert_switch=Switch.get(invert))

class Dataset(_Dataset):
    """User interface of dataset object
    
    Args:
        index
        xy (arraylike)
        label (str)
        datatype (str)
        color (str) : global color control
        comment (str)
        symbol (str) : symbol type
        ssize (number) : symbol size
        sc (str) : symbol color
        sp (str) : symbol pattern
        line (str) : line type
        lw (number) : linewidth
        ls (str/int) : line style
        lp (str/int) : line pattern
        lc (str/int) : line color
        keyword arguments (arraylike): error data
    """
    def __init__(self, index, *xy, label=None, color=None, datatype=None, comment=None,
                 symbol=None, ssize=None, sc=None, sp=None, sfc=None, sfp=None,
                 slw=None, sls=None, char=None, charfont=None, skip=None,
                 line=None, lw=None, lc=None, ls=None, lp=None,
                 baseline=None, blt=None, dropline=None, ft=None, rule=None, fc=None, fp=None,
                 anno=None, at=None, asize=None, ac=None, rot=None, font=None, af=None, prec=None,
                 prepend=None, append=None, offset=None,
                 errorbar=None, ebpos=None, ebc=None, ebp=None, ebsize=None, eblw=None,
                 ebls=None, ebrlw=None, ebrls=None, ebrc=None, ebrcl=None,
                 **extras):
        # pop comment and legend out to avoid duplicate arguments
        if label is None:
            label = ""
        if comment is None:
            comment = ""
        label=encode_string(label)
        comment=encode_string(comment)
        self.data = Data(*xy, datatype=datatype, label=label, comment=comment, **extras)

        _Dataset.__init__(self, index, type=self.data.datatype, comment=comment, legend=label)
        if sc is None:
            sc = color
        if sfc is None:
            sfc = color
        self._symbol = Symbol(st=symbol, color=sc, size=ssize, pattern=sp, fc=sfc, fp=sfp, lw=slw,
                              ls=sls, char=char, charfont=charfont, skip=skip)
        if lc is None:
            lc = color
        self._line = Line(lt=line, color=lc, width=lw, style=ls, pattern=lp)
        self._baseline = BaseLine(lt=blt, switch=baseline)
        self._dropline = DropLine(switch=dropline)
        if fc is None:
            fc = color
        self._fill = Fill(ft=ft, rule=rule, color=fc, pattern=fp)
        if ac is None:
            ac = color
        self._avalue = Annotation(switch=anno, at=at, rot=rot, charsize=asize, color=ac, font=font,
                                  af=af, append=append, prepend=prepend, prec=prec, offset=offset)
        if ebc is None:
            ebc = color
        self._errorbar = Errorbar(switch=errorbar, position=ebpos, color=ebc, pattern=ebp,
                                  size=ebsize, lw=eblw, ls=ebls, rlw=ebrlw, rls=ebrls, rc=ebrc,
                                  rcl=ebrcl)
    
    def xmin(self):
        """get the minimal value of abscissa"""
        return self.data.xmin()

    def xmax(self):
        """get the maximal value of abscissa"""
        return self.data.xmax()

    def min(self):
        """get the minimal value of data"""
        return self.data.min()

    def max(self):
        """get the maximal value of data"""
        return self.data.max()

    def set_symbol(self, **kwargs):
        self._symbol.set(**kwargs)

    def set_line(self, **kwargs):
        """set attributes of data line"""
        self._line.set(**kwargs)

    def set_baseline(self, **kwargs):
        """set attributes of baseline"""
        self._baseline.set(**kwargs)

    def set_dropline(self, **kwargs):
        """set attributes of dropline"""
        self._dropline.set(**kwargs)

    def set_fill(self, **kwargs):
        """set attributes of marker fill"""
        self._fill.set(**kwargs)

    def set_annotation(self, **kwargs):
        """set attributes of data annotation"""
        self._avalue.set(**kwargs)

    def set_errorbar(self, **kwargs):
        """set attributes of error bar"""
        self._errorbar.set(**kwargs)

    @property
    def label(self):
        """string. label mark of the dataset"""
        return self.legend

    def export(self):
        """Export the header part of dataset"""
        slists = _Dataset.export(self)
        to_exports = [self._symbol,
                      self._line,
                      self._baseline,
                      self._dropline,
                      self._fill,
                      self._avalue,
                      self._errorbar,]
        for ex in to_exports:
            _logger.debug(type(ex).__name__)
            slists += [self._marker + self._affix + " " + i for i in ex.export()]
        return slists

    def export_data(self, igraph):
        """Export the data part"""
        slist = ['@target G' + str(igraph) + '.' + self._marker.upper() + self._affix,
                 '@type ' + self.type,]
        slist.extend(self.data.export())
        slist.append('&')
        return slist

class DrawString(_DrawString):
    """user interface of string drawing

    Args:
        s (str) : content of string
        xy (2-member list) : location of string
    """
    def __init__(self, s: str, xy, ig=None, color=None, just=None, charsize=None,
                 rot=None, font=None, loctype=None, **kwargs):
        if ig is not None:
            ig = "g" + str(ig)
        _DrawString.__init__(self, loctype=loctype, color=Color.get(color), string_comment=ig,
                             just=Justf.get(just), rot=rot, char_size=charsize, font=font,
                             string_location=xy)
        self.__setattr__("def", encode_string(s))
        _raise_unknown_attr(self, *kwargs)

    def export(self):
        return ["with " + self._marker,] + \
               ["    {:s}".format(s) for s in _DrawString.export(self)]

class DrawLine(_DrawLine):
    """user interface of drawing line object

    Args:
        start, end (2-member Iterable)
    """
    def __init__(self, start, end, ig=None, color=None, lw=None, ls=None,
                 arrow=None, at=None, length=None, layout=None, loctype=None, **kwargs):
        if ig is not None:
            ig = "g" + str(ig)
        if len(start) != 2 or len(end) != 2:
            raise TypeError("Endpoint of line should have both x and y")
        _DrawLine.__init__(self, loctype=loctype, color=Color.get(color), line_comment=ig,
                           linestyle=LineStyle.get(ls), linewidth=lw,
                           arrow=Arrow.get(arrow), arrow_type=Arrow.get(at),
                           arrow_length=length, arrow_layout=layout, line_location=(*start, *end))
        _raise_unknown_attr(self, *kwargs)

    def export(self):
        return ["with " + self._marker,] + ["    {:s}".format(s) for s in _DrawLine.export(self)] \
               + [self._marker + " def"]

class DrawEllipse(_DrawEllipse):
    """user interface of drawing line object
    
    Args:
        xy (2-member Iterable) : location of center
        width (float) : width of ellipse
        heigh (float) : height of ellipse. Use width if not set
    """
    def __init__(self, xy, width, heigh=None, ig=None, color=None, lw=None, ls=None,
                 fc=None, fp=None, loctype="world", **kwargs):
        if ig is not None:
            ig = "g" + str(ig)
        if heigh is None:
            heigh = width
        x, y = xy
        if color is not None and fc is None:
            fc = color
        _DrawEllipse.__init__(self, loctype=loctype, color=Color.get(color), ellipse_comment=ig,
                              linestyle=LineStyle.get(ls), linewidth=lw,
                              ellipse_location=(x-width/2, y+heigh/2, x+width/2, y-heigh/2),
                              fill_color=Color.get(fc),
                              fill_pattern=Pattern.get(fp))
        _raise_unknown_attr(self, *kwargs)

    def export(self):
        return ["with " + self._marker,] \
               + ["    {:s}".format(s) for s in _DrawEllipse.export(self)] \
               + [self._marker + " def"]

# pylint: disable=too-many-locals
class Graph(_Graph):
    """user interface of grace graph

    Args:
        index (int)
        xmin, ymin, xmax, ymax
        gt : graph type
        title : title string
        subtitle : subtitle string
        tc : title color
        stc : subtitle color
    """
    def __init__(self, index, xmin=None, ymin=None, xmax=None, ymax=None,
                 hidden=None, gt=None, stacked=None, barhgap=None,
                 fp=None, fpt=None, fpxy=None, fpform=None, fpprec=None,
                 title=None, subtitle=None, tsize=None, stsize=None,
                 tc=None, stc=None,
                 **kwargs):
        _raise_unknown_attr(self, *kwargs)
        _Graph.__init__(self, index, hidden=hidden, type=gt, stacked=stacked, bar_hgap=barhgap,
                        fixedpoint_switch=Switch.get(fp), fixedpoint_type=fpt, fixedpoint_xy=fpxy,
                        fixedpoint_format=fpform, fixedpoint_prec=fpprec)
        self._world = World()
        self._if_xlim_set = any([xmin, xmax])
        self._if_ylim_set = any([ymin, ymax])
        self.set_lim(xmin, ymin, xmax, ymax)
        self._stackworld = StackWorld()
        self._view = View()
        self._znorm = Znorm()
        self._title = Title(title=title, fontsize=tsize, color=tc)
        self._subtitle = SubTitle(subtitle=subtitle, fontsize=stsize, color=stc)
        self._if_xtick_set = False
        self._if_ytick_set = False
        self._xaxes = _Axes('x')
        self._yaxes = _Axes('y')
        #self._altxaxes = _Axes('altx', switch=Switch.OFF)
        #self._altyaxes = _Axes('alty', switch=Switch.OFF)
        self._xaxis = Axis('x')
        self._yaxis = Axis('y')
        self._altxaxis = Axis('altx', switch=Switch.OFF)
        self._altyaxis = Axis('alty', switch=Switch.OFF)
        self._legend = Legend()
        self._frame = Frame()
        self._datasets = []
        self._objects = []

    def __len__(self):
        return len(self._datasets)

    def get_objects(self):
        """get the drawing objects of graph"""
        return self._objects

    def set(self, hidden=None, gt=None, stacked=None, barhgap=None,
            fp=None, fpt=None, fpxy=None, fpform=None, fpprec=None, **kwargs):
        _raise_unknown_attr(self, *kwargs)
        self._set(hidden=hidden, type=gt, stacked=stacked, bar_hgap=barhgap,
                  fixedpoint_switch=Switch.get(fp), fixedpoint_type=fpt, fixedpoint_xy=fpxy,
                  fixedpoint_format=fpform, fixedpoint_prec=fpprec)

    def __getitem__(self, i):
        return self._datasets[i]

    def xmin(self):
        """get the minimal value of x-data"""
        v = 0
        if self._datasets:
            v = min(ds.xmin() for ds in self._datasets)
        return v

    def xmax(self):
        """get the maximal value of x-data"""
        v = 1
        if self._datasets:
            v = max(ds.xmax() for ds in self._datasets)
        return v

    def min(self):
        """get the minimal value of y/z-data"""
        v = 0
        if self._datasets:
            v = min(ds.min() for ds in self._datasets)
        return v

    def max(self):
        """get the maximal value of y/z-data"""
        v = 1
        if self._datasets:
            v = max(ds.max() for ds in self._datasets)
        return v

    def tight_graph(self, nxticks=5, nyticks=5, xscale=1.1, yscale=1.1):
        """make the graph looks tight by adopting x/y min/max as axis extremes"""
        self.set_lim(xmin=self.xmin()-absolute(self.xmin())*(xscale-1.0),
                     xmax=self.xmax()+absolute(self.xmax())*(xscale-1.0),
                     ymin=self.min()-absolute(self.min())*(yscale-1.0),
                     ymax=self.max()+absolute(self.max())*(yscale-1.0))
        xmin, ymin, xmax, ymax = self.get_limit()
        if not self._if_xtick_set:
            self._xaxis.set_major(major=(xmax-xmin)/nxticks)
        if not self._if_ytick_set:
            self._yaxis.set_major(major=(ymax-ymin)/nyticks)
        
    def export(self):
        """export the header of graph, including `with g` part and data header"""
        slist = []
        slist += _Graph.export(self)
        slist.append("with g" + self._affix)
        header = [self._world, self._stackworld,
                  self._znorm, self._view, self._title, self._subtitle,
                  self._xaxes, self._yaxes,
                  #self._altxaxes, self._altyaxes,
                  self._xaxis, self._yaxis,
                  self._altxaxis, self._altyaxis,
                  self._legend, self._frame, *self._datasets]
        for x in header:
            _logger.debug("marker: %s", x._marker)
            slist += ["    " + s for s in x.export()]
        return slist

    def export_data(self):
        """export the dataset part"""
        slist = []
        for ds in self._datasets:
            slist += ds.export_data(igraph=self._index)
        return slist

    @property
    def ndata(self):
        """Number of datasets in current graph"""
        return len(self._datasets)

    def set_axis(self, axis, **kwargs):
        """set axis"""
        d = {'x': self._xaxis, 'y': self._yaxis, 'altx': self._altxaxis, 'alty': self._altyaxis}
        try:
            ax = d.get(axis)
        except KeyError:
            raise ValueError("axis name %s is not supported. %s" % (axis, d.keys()))
        ax.set(**kwargs)

    def get_axis(self, axis):
        """set axis
        
        Args:
            axis (str) : x, y, altx, alty
        """
        d = {'x': self._xaxis, 'y': self._yaxis, 'altx': self._altxaxis, 'alty': self._altyaxis}
        try:
            ax = d.get(axis)
        except KeyError:
            raise ValueError("axis name %s is not supported. %s" % (axis, d.keys()))
        return ax

    def set_xlim(self, xmin=None, xmax=None):
        """set limits of x axis"""
        self.set_lim(xmin=xmin, xmax=xmax)

    def set_ylim(self, ymin=None, ymax=None):
        """set limits of y axis"""
        self.set_lim(ymin=ymin, ymax=ymax)

    def set_lim(self, xmin=None, ymin=None, xmax=None, ymax=None):
        """set the limits (world) of graph"""
        pre = self._world.get_world()
        for i, v in enumerate([xmin, ymin, xmax, ymax]):
            if v is not None:
                pre[i] = v
        self._world.set_world(pre)

    def get_limit(self):
        """get the limits (world) of graph

        Returns
            tuple. xmin, ymin, xmax, ymax
        """
        return self._world.get_world()

    def get_view(self):
        return self._view.get_view()

    def set_view(self, xmin=None, ymin=None, xmax=None, ymax=None):
        """set the view (apperance in the plot) of graph on the plot"""
        pre = self._view.get_view()
        _logger.debug("view before %8f %8f %8f %8f", *pre)
        for i, v in enumerate([xmin, ymin, xmax, ymax]):
            if v is not None:
                pre[i] = v
        self._view.set_view(pre)
        _logger.debug("view after %8f %8f %8f %8f", *self._view.get_view())

    @property
    def x(self):
        """x axis"""
        return self._xaxis

    @property
    def y(self):
        """y axis"""
        return self._yaxis

    def set_xaxis(self, **kwargs):
        """set x axis"""
        self.set_axis(axis='x', **kwargs)

    def set_yaxis(self, **kwargs):
        """set x axis"""
        self.set_axis(axis='y', **kwargs)

    def set_altxaxis(self, **kwargs):
        """set x axis"""
        self.set_axis(axis='altx', **kwargs)

    def set_altyaxis(self, **kwargs):
        """set x axis"""
        self.set_axis(axis='alty', **kwargs)

    def plot(self, *xy, **kwargs):
        """plot a dataset
        
        multiple y can be parsed along with one x.
        In this case, the keyword arguments except `label`
        will be parsed for each y. `label` will be parsed
        only for the first set
        """
        # check if a band structure like `y` data is parsed
        if len(xy) == 2 and len(shape(xy[1])) == 2:
            x, ys = xy
            n = self.ndata
            # check error in keyword arguments as well
            extras = {}
            for t in Data.extra_data:
                if t in kwargs:
                    extras[t] = kwargs.pop(t)
            extras_first = {k: v[0] for k, v in extras.items()}
            ds = [Dataset(n, x, ys[0], **extras_first, **kwargs),]
            kwargs.pop("label", None)
            for i, y in enumerate(ys[1:]):
                extra = {k: v[i+1] for k, v in extras.items()}
                ds.append(Dataset(n+i+1, x, y, **kwargs, **extra))
            self._datasets.extend(ds)
        else: 
            ds = Dataset(self.ndata, *xy, **kwargs)
            self._datasets.append(ds)

    def set_legend(self, **kwargs):
        """set up the legend. For arguments, see Legend

        Particularly, a string can be parsed to ``loc``, e.g. 'upper left',
        'lower right'. Available token:
            lower/bottom, middle, upper/top;
            left, center, right;
        """
        x = None
        y = None
        try:
            loc_token = kwargs["loc"]
            int(loc_token)
        except ValueError:
            try:
                loctype = kwargs.get("loctype")
                assert loctype == "world"
                xmin, ymin, xmax, ymax = self._world.get_world()
            except (KeyError, AssertionError):
                xmin, ymin, xmax, ymax = self._view.get_view()

            if loc_token.endswith("left"):
                x = 0.8 * xmin + 0.2 * xmax
            elif loc_token.endswith("right"):
                x = 0.3 * xmin + 0.7 * xmax
            elif loc_token.endswith("center"):
                x = 0.6 * xmin + 0.4 * xmax

            if loc_token.startswith("lower") or loc_token.startswith("bottom"):
                y = 0.9 * ymin + 0.1 * ymax
            elif loc_token.startswith("upper") or loc_token.startswith("top"):
                y = 0.1 * ymin + 0.9 * ymax
            elif loc_token.startswith("middle"):
                y = 0.5 * ymin + 0.5 * ymax

            loc = (x, y)
            if x is None or y is None:
                raise ValueError("invalid location token for legend: {}".format(kwargs["loc"]))
            kwargs["loc"] = loc
        except KeyError:
            # location of legend is specified
            pass

        self._legend.set(**kwargs)

    def set_legend_box(self, **kwargs):
        """set up the legend box"""
        self._legend.set_box(**kwargs)

    def set_xlabel(self, s, **kwargs):
        """set x label of graph to s"""
        self._xaxis.set_label(s, **kwargs)

    def set_ylabel(self, s, **kwargs):
        """set y label of graph to s"""
        self._yaxis.set_label(s, **kwargs)

    def set_xticklabel(self, **kwargs):
        """set x label of graph"""
        self._xaxis.set_ticklabel(**kwargs)

    def set_yticklabel(self, **kwargs):
        """set y label of graph"""
        self._yaxis.set_ticklabel(**kwargs)

    def set_title(self, title=None, **kwargs):
        """set the title string or its attributes"""
        if title:
            self._title.__setattr__('title_comment', title)
        self._title._set(**kwargs)

    @property
    def title(self):
        return self._title.title
    @title.setter
    def title(self, new: str):
        self.set_title(title=new)

    def set_subtitle(self, subtitle=None, **kwargs):
        """set the subtitle string or its attributes"""
        if subtitle:
            self._subtitle.__setattr__('subtitle_comment', subtitle)
        self._subtitle._set(**kwargs)

    @property
    def subtitle(self):
        return self._subtitle.subtitle
    @subtitle.setter
    def subtitle(self, new: str):
        self.set_subtitle(subtitle=new)

    def text(self, s, xy, loctype=None, color=None,
             just=None, charsize=None,rot=None, font=None, **kwargs):
        """add string text to the plot
        Args:
            s (str)
            xy (2-member list) : the location of text string
        """
        o = DrawString(s, xy, ig=self._index, loctype=loctype, color=color, just=just,
                       charsize=charsize, rot=rot, font=font, **kwargs)
        self._objects.append(o)

    def circle(self, xy, width, heigh=None, color=None, loctype="world",
               lw=None, ls=None, fc=None, fp=None, **kwargs):
        """draw a circle on the plot

        Args:
            xy (2-member list)
            width (float)
            heigh (float): if left as None, it will try to draw a round circle
            color (str/int)
            lw (float) : line width
            ls (str/int) : line style
            fc (str/int) : fill color
            fp (str/int) : fill pattern
        """
        if heigh is None:
            xmin, ymin, xmax, ymax = {"world": self.get_limit, "view": self.get_view}.get(loctype)()
            heigh = width / (xmax-xmin) * (ymax-ymin)
        o = DrawEllipse(xy, width, heigh=heigh, ig=self._index, color=color, lw=lw,
                        ls=ls, fc=fc, fp=fp, loctype=loctype, **kwargs)
        self._objects.append(o)

    def axhline(self, y, xmin=None, xmax=None, loctype=None, **kwargs):
        """add a horizontal line

        Args:
            y (float) :
            xmin, xmax (float, str): endpoints of horizontal line.
                If str is parsed, it will be recognized as a percentage of the axis
        """
        if loctype is None:
            loctype = "world"
        try:
            ends = {"view": self.get_view, "world": self.get_limit}
            left, _, right, _ = ends[loctype]()
        except KeyError:
            raise KeyError("unknown location type {}".format(loctype))
        if xmin is None:
            xmin = left
        elif isinstance(xmin, str):
            xmin = left + float(xmin) / 100 * (right-left)
        if xmax is None:
            xmax = right
        elif isinstance(xmax, str):
            xmax = left + float(xmax) / 100 * (right-left)
        start = (xmin, y)
        end = (xmax, y)
        self.axline(start, end, loctype=loctype, **kwargs)

    def axvline(self, x, ymin=None, ymax=None, loctype=None, **kwargs):
        """add a vertical line

        Args:
            x (float) :
            ymin, ymax (float, str): endpoints of vertical line.
                If str is parsed, it will be recognized as a percentage of the axis
        """
        if loctype is None:
            loctype = "world"
        try:
            ends = {"view": self.get_view, "world": self.get_limit}
            _, bottom, _, top = ends[loctype]()
        except KeyError:
            raise KeyError("unknown location type {}".format(loctype))
        if ymin is None:
            ymin = bottom
        elif isinstance(ymin, str):
            ymin = bottom + float(ymin) / 100 * (top-bottom)
        if ymax is None:
            ymax = top
        elif isinstance(ymax, str):
            ymax = bottom + float(ymax) / 100 * (top-bottom)
        start = (x, ymin)
        end = (x, ymax)
        self.axline(start, end, loctype=loctype, **kwargs)

    def axline(self, start, end, loctype=None, **kwargs):
        """add a custom line"""
        o = DrawLine(start, end, ig=self._index, loctype=loctype, **kwargs)
        self._objects.append(o)

    def arrow(self, start, end, color=None, lw=None, ls=None, arrow=Arrow.END,
              at=None, length=None, layout=None, loctype=None, **kwargs):
        o = DrawLine(start, end, ig=self._index, color=color, lw=lw, ls=ls,
                     arrow=arrow, at=at, length=length, layout=layout, loctype=loctype,
                     **kwargs)
        self._objects.append(o)

# ===== functions related to graph alignment =====
def __ga_regular(rows, cols, hgap, vgap, width_ratios=None, heigh_ratios=None):
    """regular graph alignment.

    By regular means graphs in the same column have the same width,
    and those in the same row have the same height.

    Args:
        rows, cols (int)
        hgap, vgap (float or Iterable)
        width_ratios, heigh_ratios (string): ratios of width/height, separated by colon.

    Returns:
        3 list, each has rows*cols members
    """
    if not isinstance(hgap, Iterable):
        hgap = [hgap,] * (cols-1)
    if not isinstance(vgap, Iterable):
        vgap = [vgap,] * (rows-1)
    if len(hgap) != cols-1 or len(vgap) != rows-1:
        raise ValueError("inconsistent number of rows/cols with vgap/hgap")

    # default global min and max
    gxmin, gymin, gxmax, gymax = View._attrs['view_location'][1]
    widths_all = gxmax - gxmin - sum(hgap)
    heighs_all = gymax - gymin - sum(vgap)
    if width_ratios:
        ws_cols = list(map(float, width_ratios.split(":")))
        ws_cols = [w * widths_all / sum(ws_cols) for w in ws_cols]
    else:
        ws_cols = [widths_all / cols,] * cols
    if heigh_ratios:
        hs_rows = list(map(float, heigh_ratios.split(":")))
        hs_rows = [h * heighs_all / sum(hs_rows) for h in hs_rows]
    else:
        hs_rows = [heighs_all / rows,] * rows
    if len(hs_rows) != rows or len(ws_cols) != cols:
        raise ValueError("inconsistent number of rows/cols with heighs/width_ratios")
    left_tops = []
    ws = []
    hs = []
    for row in range(rows):
        for col in range(cols):
            left = gxmin + sum(hgap[:col]) + sum(ws_cols[:col])
            top = gymax - sum(vgap[:row]) - sum(hs_rows[:row])
            left_tops.append((left, top))
            ws.append(ws_cols[col])
            hs.append(hs_rows[row])
    return left_tops, ws, hs

# pylint: disable=too-many-locals
def _set_graph_alignment(rows, cols, hgap=0.02, vgap=0.02, width_ratios=None, heigh_ratios=None,
                         **kwargs):
    """Set the graph alignment

    Args:
        rows, cols (int)
        hgap, vgap (float or Iterable)

    TODO:
        intricate handling of graph view with kwargs
    """
    # graphs from left to right, upper to lower
    if rows * cols == 0:
        raise ValueError("no graph is set!")

    graphs = []
    if not kwargs:
        left_up_corners, widths, heighs = __ga_regular(rows, cols, hgap, vgap,
                                                       width_ratios=width_ratios,
                                                       heigh_ratios=heigh_ratios)
    else:
        raise NotImplementedError("Unknown keywords for graph alignment:", *kwargs)

    for i, ((left, top), w, h) in enumerate(zip(left_up_corners, widths, heighs)):
        g = Graph(index=i)
        g.set_view(xmin=left, xmax=left+w, ymin=top-h, ymax=top)
        graphs.append(g)
    for i, g in enumerate(graphs):
        _logger.debug("initializting graphs %d done, view %8f %8f %8f %8f",
                      i, *g._view.view_location)
    return graphs

# ===== main object =====
class Plot:
    """the general control object for the grace plot

    Args:
        rows, cols (int) : graph alignment
        hgap, vgap (float or Iterable) : horizontal and vertical gap between graphs
        lw (number) : default linewidth
        ls (str/int) : default line style
        color (str/int) : default color
        bc (str/int) : background color
        background (str/int) : switch of background fill
        qtgrace (bool) : if true, QtGrace comments will be added 
    """
    def __init__(self, rows=1, cols=1, hgap=0.02, vgap=0.02, bc=0, background=None,
                 lw=None, ls=None, color=None, pattern=None, font=None,
                 charsize=None, symbolsize=None, sformat=None,
                 width_ratios=None, heigh_ratios=None,
                 qtgrace=False, description=None, **kwargs):
        self._comment_head = ["# Grace project file", "#"]
        # header that seldom needs to change
        self._head = ["version 50122",
                      "link page off",
                      "reference date 0",
                      "date wrap off",
                      "date wrap year 1950",
                      ]
        self.description = description
        self._background_color = Color.get(bc)
        self._page = Page(bgfill=Switch.get(background))
        self._regions = [_Region(i) for i in range(5)]
        self._fontmap = FontMap()
        self._colormap = plot_colormap
        self._timestamp = TimesStamp()
        self._default = Default(lw=lw, ls=ls, color=color, pattern=pattern,
                                font=font, charsize=charsize, symbolsize=symbolsize,
                                sformat=sformat)
        # drawing objects
        # set the graphs by alignment
        self._graphs = _set_graph_alignment(rows=rows, cols=cols, hgap=hgap, vgap=vgap,
                                            width_ratios=width_ratios, heigh_ratios=heigh_ratios,
                                            **kwargs)
        self._use_qtgrace = qtgrace

    def __len__(self):
        return len(self._graphs)

    def __str__(self):
        """print the whole agr file"""
        slist = self._head + ["background color {:d}".format(self._background_color),]
        if self.description is not None:
            slist.append("description \"{}\"".format(self.description))
        headers = [self._page, self._fontmap, self._colormap,
                   self._default, self._timestamp, *self._regions]
        for h in headers:
            slist += h.export()
        for g in self._graphs:
            slist += g.export()
        for g in self._graphs:
            for o in g.get_objects():
                slist += o.export()
        # add @ to each header line
        slist = self._comment_head + ["@" + v for v in slist]
        # export all data
        for g in self._graphs:
            slist += g.export_data()
        return "\n".join(slist)

    def set_default(self, **kwargs):
        """set default format"""
        self._default.set(**kwargs)

    def __getitem__(self, i):
        return self._get_graph(i)

    def get(self, i: int = None):
        """Get the Graph object of index i
        
        Args:
            i (int) : index of graph.
                If not specified, all graphs are returned in a list
        """
        if i:
            return self._get_graph(i)
        return self._graphs

    def _get_graph(self, i: int) -> Graph:
        """Get the Graph object of index i"""
        try:
            return self._graphs[i]
        except IndexError:
            raise IndexError(f"G.{i} does not exist")

    def add_graph(self, xmin=None, xmax=None, ymin=None, ymax=None):
        """add a new graph

        the location and size of graph is determined by x/ymin/max.
        
        Args:
            view (4-member iterable)

        Returns:
            list of graphs after addition of new graph
        """
        g = Graph(index=len(self))
        self._graphs.append(g)
        g.set_view(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        return self._graphs

    def plot(self, *xy, **kwargs):
        """plot a data set to the first graph

        Args:
            positional *xy (arraylike): x, y data. Error should be parsed to keyword arguments
            igraph (int) : index of graph to plot
            keyword arguments will parsed to Graph object
        """
        self._graphs[0].plot(*xy, **kwargs)

    def title(self, title=None, ig=0, **kwargs):
        """set the title of graph `igraph`"""
        self._graphs[ig].set_title(title=title, **kwargs)

    def subtitle(self, subtitle=None, ig=0, **kwargs):
        """set the subtitle of graph `igraph`"""
        self._graphs[ig].set_subtitle(subtitle=subtitle, **kwargs)

    def xticks(self, **kwargs):
        """setup ticks of x axis of all graphs"""
        for g in self._graphs:
            g.xticks(**kwargs)

    def yticks(self, **kwargs):
        """setup ticks of y axis of all graphs"""
        for g in self._graphs:
            g.yticks(**kwargs)

    def xlabel(self, s, **kwargs):
        """set xlabel of all graphs. emulate pylab.xlabel"""
        for g in self._graphs:
            g.set_xlabel(s, **kwargs)

    def ylabel(self, s, **kwargs):
        """set ylabel of all graphs. emulate pylab.ylabel"""
        for g in self._graphs:
            g.set_ylabel(s, **kwargs)

    def set_xaxis(self, **kwargs):
        """set up x-axis of all graph"""
        for g in self._graphs:
            g.set_xaxis(**kwargs)

    def set_yaxis(self, **kwargs):
        """set up y-axis of all graphs"""
        for g in self._graphs:
            g.set_yaxis(**kwargs)

    def set_xlim(self, xmin=None, xmax=None):
        """set xlimit of all graphs

        Args:
            graph (int)
            xmin (float)
            xmax (float)
        """
        for g in self._graphs:
            g.set_xlim(xmin=xmin, xmax=xmax)

    def set_ylim(self, ymin=None, ymax=None):
        """set ylimit of all graphs

        Args:
            graph (int)
            ymin (float)
            ymax (float)
        """
        for g in self._graphs:
            g.set_ylim(ymin=ymin, ymax=ymax)

    def write(self, file=sys.stdout, mode='w'):
        """write grace plot file to `fn`

        Args:
            file (str or file handle)
            mode (str) : used only when `file` is set to a filename
        """
        if isinstance(file, str):
            fp = open(file, mode)
            print(self.__str__(), file=fp)
            fp.close()
            return
        if isinstance(file, TextIOWrapper):
            print(self.__str__(), file=file)
            return
        raise TypeError("should be str or TextIOWrapper type")

    def tight_graph(self, nxticks=5, nyticks=5, xscale=1.1, yscale=1.1):
        """make graph axis tight"""
        for g in self._graphs:
            g.tight_graph(nxticks=nxticks, nyticks=nyticks,
                          xscale=xscale, yscale=yscale)


    @classmethod
    def subplots(cls, *args, **kwargs):
        """emulate matplotlib.pyplot.subplots

        ArgsL
            args: can be one string/int, or two int
            keyword arguments: see Plot class
        """
        if not args:
            rows = 1
            cols = 1
        elif len(args) == 1:
            s = int(args[0])
            if 10 < s < 100:
                cols = s % 10
                rows = s // 10
            elif 0 < s < 10:
                rows = s
                cols = 1
            else:
                raise ValueError("identifier is not supported: {}".format(s))
        elif len(args) == 2:
            rows, cols = args
        else:
            raise ValueError("identifier is not supported: {}".format(args))
        p = cls(rows=rows, cols=cols, **kwargs)
        if len(p) == 1:
            g = p[0]
        else:
            g = p._graphs
        return p, g


def extract_data_from_agr(pagr):
    """extract all data from agr file

    Args:
        pagr (str) : path to the agr file

    Returns:
        list, type of each dataset; list, each member is a dataset as a 2d-array
    """
    starts = []
    ends = []
    types = []
    with open(pagr, 'r') as h:
        for i, l in enumerate(h.readlines()):
            if l.startswith("@type"):
                # exclude @type line
                starts.append(i+1)
                types.append(l.split()[-1].lower())
            if l == "&\n":
                ends.append(i)
    data = []
    
    with open(pagr, 'r') as h:
        lines = h.readlines()
        for i, (start, end) in enumerate(zip(starts, ends)):
            s = StringIO("".join(lines[start:end]))
            data.append(loadtxt(s, unpack=True))
    return types, data

