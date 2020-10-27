#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from pygraceplot import Plot

p, ax = Plot.subplots(background=False, description="CV curve drawn by pygraceplot")
ax.set_view(xmin=0.323, xmax=1.1, ymin=0.25, ymax=0.85)

# main CV figure
training_size = [20, 35, 50, 65, 80]
cv = [3.8, 3.5, 3.0, 2.3, 2.1]
error = [0.7, 0.4, 0.5, 0.2, 0.2]
ax.plot(training_size, cv, dy=error, lw=3, eblw=3, ebrlw=3,
        symbol="none", color="blue", datatype="xydy")
ax.set_xlim(xmin=20, xmax=80)
ax.set_ylim(ymin=1.5, ymax=5.0)
ax.x.set_label("Training set size", charsize=2)
ax.y.set_label("Average 10-fold CV / meV", charsize=2)
ax.x.set_tick(major=15, mit=0)
ax.y.set_tick(major=0.5, mit=4)
ax.y.set_ticklabel(prec=2, tlf="decimal")

# draw inset, DFT vs CE energy
axi = p.add_graph(xmin=0.7765, xmax=1.0353,
                  ymin=0.6, ymax=0.8)
dft = np.linspace(-30, 30, 30)
ce = dft + (np.random.random(len(dft))-0.5) * 8.0
axi.plot(dft, ce, symbol="+", color="blue", ls="none", ssize=0.7, slw=2.0)
axi.x.set_label("DFT / meV", charsize=1)
axi.y.set_label("CE / meV", charsize=1)
axi.set_lim(xmin=-35, xmax=30, ymin=-35, ymax=30)
for axis in [axi.x, axi.y]:
    axis.set_tick(major=10, mit=1)
    axis.set_ticklabel(charsize=1)

p.savefig("cv.eps")
#p.write("cv.agr")

