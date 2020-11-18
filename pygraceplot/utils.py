# -*- coding: utf-8 -*-
"""supporting uitlities for grace plotting"""
from __future__ import print_function
import os
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from io import StringIO, TextIOWrapper
from re import sub, findall, compile
try:
    from os import PathLike
except ImportError:
    PathLike = str
from numpy import loadtxt

lower_greeks = ["alpha", "beta", "gamma", "theta", "omega"]
upper_greeks = list(x.capitalize() for x in lower_greeks)
greeks = lower_greeks + upper_greeks

GREEK_PATTERN = dict((r"\\{}".format(_g), r"\\x%s\\f{}" % _g[0]) for _g in greeks)
SPECIAL_CHAR_PATTERN = {
    r"\\AA": r"\\cE\\C",
    }

def grep(pattern, filename, error_not_found=False, from_behind=False,
         return_group=False, maxcounts=None, maxdepth=None,return_linenum=False):

    """emulate command line grep with re package

    Args:
        pattern (str or re.Pattern object) : pattern to match in the line
        filename (str, file-like, Iterable of str) :
            str: filename to search
            file-like: handle of file
            Iterable: contents of a file from readlines()
        from_behind (bool): search from behind
        error_not_found (bool): raise when no match is found
        maxcounts (int) : maximal times of matching
        maxdepth (int) : end of line to search
        return_group (bool): return re.Match object
        return_linenum (bool): return both the matched lines and their indices in the contents

    Returns
        one list if return_linenum is False, re.Match object if return_group is True
            otherwise the string of the matched line
        otherwise another list of integers will be returned as well
    """
    def _ln_modifier(index, size):
        ln = index
        if from_behind:
            ln = size - 1 - index
        return ln
    if isinstance(pattern, str):
        pattern = compile(pattern)
    if isinstance(filename, (str, PathLike)):
        if not os.path.isfile(filename):
            if error_not_found:
                raise FileNotFoundError("{} is not a file".format(filename))
            return None
        with open(filename, 'r') as f:
            container = f.readlines()
    elif isinstance(filename, (TextIOWrapper, StringIO)):
        container = filename.readlines()
    elif isinstance(filename, Iterable):
        container = filename
    else:
        raise TypeError("expect str, file-like object or Iterable, got", type(filename))
    line_nums = []
    matched = []
    n = 0
    size = len(container)
    if maxcounts is None:
        maxcounts = size
    if maxdepth is None:
        maxdepth = size
    if from_behind:
        container = reversed(container)
    for i, l in enumerate(container):
        m = pattern.search(l.strip('\n'))
        if m is not None:
            line_nums.append(_ln_modifier(i, size))
            if return_group:
                if return_group is True:
                    matched.append(m)
                elif isinstance(return_group, int):
                    matched.append(m.group(return_group))
                else:
                    matched.append(tuple(map(m.group, return_group)))
            else:
                matched.append(l)
            n += 1
            if n >= maxcounts:
                break
        if i+1 >= maxdepth:
            break

    if return_linenum:
        return matched, line_nums
    return matched


# pylint: disable=bad-whitespace
def encode_string(string):
    r"""encode a string to grace format.

    Args:
        string (str): the string to encode. Supported markup:
            Greek letters: \alpha, \Beta, \gamma
            special characters: Angstrom \AA
            italic: / ... /.
            sub/superscripts: _{}, ^{}
    """
    if string is None:
        return None
    # greek letter
    for pat, agrstr in GREEK_PATTERN.items():
        string = sub(pat, agrstr, string)
    for pat, agrstr in SPECIAL_CHAR_PATTERN.items():
        string = sub(pat, agrstr, string)
    # italic
    string = sub(r"/(.+?)/", r"\\f{Times-Italic}\1\\f{}", string)
    # both super and subscript
    ## TODO better width handling of scripts
    #string = sub(r"\^{(.*?)}_{(.*?)}", r"\\S\1\\N\\s\2\\N", string)
    #string = sub(r"_{(.*?)}\^{(.*?)}", r"\\s\1\\N\\S\2\\N", string)
    # either super or subscript
    for pat, repl in [(r"\^{(.+?)}", r"\\S\1\\N"), (r"_{(.+?)}", r"\\s\1\\N")]:
        string = sub(pat, repl, string)
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
            return pair.get(marker)
        except KeyError:
            return KeyError("unknown marker \"{:s}\" for {:s}".format(marker, name))
    if isinstance(marker, int):
        return marker
    raise TypeError("expect str or int")


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
        list,list,list: label, type and data of each dataset
    """
    starts = []
    ends = []
    types = []
    with open(pagr, 'r') as h:
        lines = h.readlines()
    for i, l in enumerate(lines):
        if l.startswith("@type"):
            # exclude @type line
            starts.append(i+1)
            types.append(l.split()[-1].lower())
        if l == "&\n":
            ends.append(i)
    legends = grep(r"@\s+s(\d+)\s+legend\s+\"(.*)\"", lines, return_group=2)
    data = []

    for i, (start, end) in enumerate(zip(starts, ends)):
        datastring = "".join(lines[start:end])
        try:
            s = StringIO(datastring)
        except TypeError:
            s = StringIO(unicode(datastring))
        data.append(loadtxt(s, unpack=True))
    return legends, types, data

