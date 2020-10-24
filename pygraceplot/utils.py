# -*- coding: utf-8 -*-
"""supporting uitlities for grace plotting"""
from re import sub, findall

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


