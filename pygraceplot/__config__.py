# -*- coding: utf-8 -*-
"""extract configurations from rc file at home directory"""
import os
import sys
from importlib import machinery

__NAME__ = "pygraceplot"
# a global configuration file
config_file = os.path.join(os.environ["HOME"], "." + __NAME__ + "rc")

# pylint: disable=no-value-for-parameter,W1505
if os.path.isfile(config_file):
    # may replace load_module later
    machinery.SourceFileLoader(__NAME__ + '.__config__', config_file).load_module()

del(machinery, os, sys)
