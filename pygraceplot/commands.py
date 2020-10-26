# -*- coding: utf-8 -*-
"""check grace command line"""
import subprocess as sp
from shutil import which

has_gracebat = which("gracebat")
del which

ext2device = {
    "ps": "PostScript",
    "eps": "EPS",
    "png": "PNG",
    "mif": "MIF",
    "pnm": "PNM",
    "svg": "SVG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    }

def run_gracebat(agr_str, filename, device):
    """run a gracebat command for figure exporting"""
    if has_gracebat is None:
        raise FileNotFoundError("gracebat is not found in PATH")
    cmds = [has_gracebat, "-hardcopy",
            "-hdevice", device,
            "-printfile", filename,
            "-pipe"]
    p = sp.Popen(cmds, stdin=sp.PIPE)
    p.stdin.write(agr_str.encode())

