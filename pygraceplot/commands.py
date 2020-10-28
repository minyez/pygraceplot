# -*- coding: utf-8 -*-
"""check grace command line"""
import subprocess as sp
try:
    from shutil import which
    has_gracebat = which("gracebat")
    del which
except ImportError:
    import os
    path = os.popen("which gracebat").read()
    if path:
        has_gracebat = path.strip()
    else:
        has_gracebat = None
    del os, path

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

