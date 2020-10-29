#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test commands"""
import unittest as ut
import os
from pygraceplot.commands import run_gracebat

try:
    from shutil import which
    has_gracebat = which("gracebat")
    del which
except ImportError:
    path = os.popen("which gracebat").read()
    if path:
        has_gracebat = path.strip()
    else:
        has_gracebat = None
    del os, path

class test_commands(ut.TestCase):
    """test commands such as gracebat """

    def test_raise_missing_gracebat(self):
        """gracebat is usually not installed by default on OS"""
        try:
            raise FileNotFoundError
        except NameError:
            pass
        except FileNotFoundError:
            if has_gracebat is None:
                self.assertRaises(FileNotFoundError, run_gracebat,
                                  "test agr stinrg", "test.eps", "EPS")


if __name__ == "__main__":
    ut.main()
