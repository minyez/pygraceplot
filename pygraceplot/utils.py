# -*- coding: utf-8 -*-
"""supporting uitlities for grace plotting"""
from __future__ import print_function
import os
from io import StringIO
from re import sub, findall
from numpy import loadtxt

lower_greeks = ["alpha", "beta", "gamma", "theta", "omega"]
upper_greeks = list(x.capitalize() for x in lower_greeks)
greeks = lower_greeks + upper_greeks

GREEK_PATTERN = dict((r"\\{}".format(_g), r"\\x%s\\f{}" % _g[0]) for _g in greeks)
SPECIAL_CHAR_PATTERN = {
    r"\\AA": r"\\cE\\C",
    }


# pylint: disable=bad-whitespace
def encode_string(string):
    r"""encode a string to grace format.

    Args:
        string (str): the string to encode. Supported markup:
            Greek letters: \alpha, \Beta, \gamma
            special characters: Angstrom \AA
            italic: / ... /.
    """
    if string is None:
        return None
    # greek letter
    for pat, agrstr in GREEK_PATTERN.items():
        string = sub(pat, agrstr, string)
    for pat, agrstr in SPECIAL_CHAR_PATTERN.items():
        string = sub(pat, agrstr, string)
    # italic
    has_italic = len(findall(r"/", string))
    if has_italic > 1:
        if has_italic % 2 == 0:
            for _ in range(has_italic // 2):
                string = sub(r"/", r"\\f{Times-Italic}", string, count=1)
                string = sub(r"/", r"\\f{}", string, count=1)
        else:
            raise ValueError("italic markers are not paired")
    return string


def get_int_const(name, pair, marker):
    """get the integer constant in the pair for an integer constant mapping `name`

    Args:
        name (str) : name for the integer constant mapping
        pair (dict)
        marker (str or int): the marker of the constant.
            If str, it should be registered in pair.
            If int, it will be directly returned
    Raises:
        TypeError for other type
        ValueError for unknown constant

    Returns:
        int
    """
    if marker is None:
        return None
    if isinstance(marker, str):
        try:
            return pair.get(marker.lower())
        except KeyError:
            return ValueError("unknown marker \"{:s}\" for {:s}".format(marker.lower(), name))
    if isinstance(marker, int):
        return marker
    raise TypeError("should be str or int")


def get_file_ext(path):
    """Return the extension name of file at path

    Args:
        path (str): the path of the file

    Returns:
        str, if extension of the file is found
        If file ``path`` is an existing directory, None will be returned
        If the path have no characters after "." or have no ".", 
        an empty string will be returned.
    """
    if os.path.isdir(path):
        return None
    base = os.path.basename(os.path.abspath(path))
    return os.path.splitext(base)[1][1:]


def get_filename_wo_ext(path):
    """Get the filename without extension

    Args:
        path (str): the path of file
    """
    fn = os.path.basename(os.path.abspath(path))
    return os.path.splitext(fn)[0]


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
            datastring = "".join(lines[start:end])
            try:
                s = StringIO(datastring)
            except TypeError:
                s = StringIO(unicode(datastring))
            data.append(loadtxt(s, unpack=True))
    return types, data

