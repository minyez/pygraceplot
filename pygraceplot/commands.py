# -*- coding: utf-8 -*-
"""check grace command line"""
import subprocess as sp
from shutil import which

def run_gracebat(agr_str, filename, device):
    """run a gracebat command for figure exporting"""
    exe = which("gracebat")
    if exe is None:
        raise FileNotFoundError("gracebat is not found in PATH")
    cmds = [exe, "-hardcopy",
            "-hdevice", device,
            "-printfile", filename,
            "-pipe"]
    p = sp.Popen(cmds, stdin=sp.PIPE, text=True)
    p.stdin.write(agr_str)

