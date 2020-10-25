#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from pygraceplot import Plot

p, axes = Plot.subplots(22, hgap=0.0, vgap=0.0)
x = np.linspace(-np.pi, np.pi, 40)
axes[0].plot(x, np.sin(x), symbol="none", label="sin(x)")
axes[0].x.set_ticklabel(switch="off")
axes[1].plot(x, -np.cos(x), color="red", symbol="o", ls="none", label="-cos(x)")
axes[1].x.set_ticklabel(switch="off")
axes[1].y.set_ticklabel(switch="off")
axes[2].plot(x, -np.sin(x), color="b", symbol="^", ls="none", label="-sin(x)")
axes[3].plot(x, np.cos(x), color="grey", lw=3, symbol="none", label="cos(x)")
axes[3].y.set_ticklabel(switch="off")
p.tight_graph()
axes[0].set_legend(loc="lower right")
axes[1].set_legend(loc="lower left")
axes[2].set_legend(loc="upper right")
axes[3].set_legend(loc="upper left")
p.savefig("array.eps")

