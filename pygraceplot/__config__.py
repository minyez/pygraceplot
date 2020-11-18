# -*- coding: utf-8 -*-
"""extract configurations from rc file at home directory"""
import os
import sys
from importlib import machinery

from pygraceplot import __NAME__
# a global configuration file
fn = "." + __NAME__ + "rc"
config_files = [
    os.path.join(os.environ["HOME"], fn),
    fn,
    ]

# pylint: disable=no-value-for-parameter,W1505
for cf in config_files:
    if os.path.isfile(cf):
        # may replace load_module later
        machinery.SourceFileLoader(__NAME__ + '.__config__', cf).load_module()

del(machinery, os, sys, config_files, fn)
