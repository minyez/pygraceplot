#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demonstration of xy plot"""
import numpy as np
from pygraceplot import Plot

p, ax = Plot.subplots(1, 1, description="Bar plot drawn by pygraceplot")
x = [1, 2, 3]
y = [3, 4, 5]
labels = ["bin1", "bin2", "bin3"]
ax.plot(x, y, datatype="bar", ls="none", ssize=5.0, symbol="none", color="blue")
ax.set_xlim(xmin=0, xmax=4)
ax.set_ylim(ymin=2, ymax=6)
ax.x.set_spec(x, labels=labels)
ax.set_legend(loc="upper left", charsize=2.0)
p.write("bar.agr")

