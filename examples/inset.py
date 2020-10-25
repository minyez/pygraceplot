#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demonstration of xy plot"""
import numpy as np
from pygraceplot import Plot

p, ax = Plot.subplots(description="inset drawn by pygraceplot")
ax_inset = p.add_graph(xmin=0.8, xmax=1.1, ymin=0.2, ymax=0.5)
x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)
y_inset = np.cos(x)
ax.plot(x, y, symbol="none", color="blue", label="sin(x)")
ax_inset.plot(x, y_inset, symbol="none", color="blue")
p.tight_graph()

ax.set_legend(loc="upper left", charsize=2.0)
p.savefig("inset.eps")

