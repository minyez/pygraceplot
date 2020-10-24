#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demonstration of xy plot"""
import numpy as np
from pygraceplot import Plot

p, ax = Plot.subplots(1, 1, description="sin(x) drawn by pygraceplot")
x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)
ax.plot(x, y, symbol="none", color="blue", label="sin(x)")
p.tight_graph()
ax.set_legend(loc="upper left", charsize=2.0)
p.write("sin.agr")

