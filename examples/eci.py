#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bar plot for effective cluster interaction"""
import numpy as np
from pygraceplot.graceplot import Plot

# data generation
x_two_body = np.arange(1, 24, 1)
x_three_body = np.arange(24, 34, 1)
y_two_body = np.random.randint(-2, 4, size=len(x_two_body))
y_three_body = np.random.randint(-2, 4, size=len(x_three_body))

# plot
p, ax = Plot.subplots(1, 1, description="ECI drawn by pygraceplot", background=False)
ax.set_view(xmin=0.3235, xmax=1.1, ymin=0.25, ymax=0.85)
ax.plot(x_two_body, y_two_body,
        ls="none", label="two-body", color="red", datatype="bar")
ax.plot(x_three_body, y_three_body,
        ls="none", label="three-body", color="green", datatype="bar")
ax.axhline(0.0)

ax.set_title("XxXx", charsize=2)
ax.set_xlim(xmin=0, xmax=35)
ax.set_ylim(ymin=-3, ymax=5)
ax.x.set_major(major=10)
ax.y.set_major(major=1)
ax.set_ylabel("ECI / meV", charsize=2)
ax.set_xlabel("Index of cluster", charsize=2)
ax.set_legend(loc="upper right", charsize=1.65)

p.write("eci.agr")
p.savefig("eci.eps")
