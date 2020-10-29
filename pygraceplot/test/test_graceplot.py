#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test graceplot"""
import unittest as ut
import tempfile

from pygraceplot.graceplot import (Color, Symbol,
                                   Graph, View, World,
                                   Plot)

class test_View(ut.TestCase):
    """test the view object"""

    def test_set_get(self):
        """test set view functionality"""
        v = View()
        new = [0.1, 0.1, 1.0, 1.0]
        v.set_view(new)
        self.assertListEqual(new, v.get_view())

        v1 = View()
        new1 = [0.2, 0.2, 2.0, 2.0]
        v1.set_view(new1)
        self.assertListEqual(new1, v1.get_view())
        self.assertListEqual(new, v.get_view())

class test_World(ut.TestCase):
    """test the world object"""

    def test_set_get(self):
        """test set view functionality"""
        w = World()
        new = [1., 2., 3.0, 4.0]
        w.set_world(new)
        self.assertListEqual(new, w.get_world())

        w1 = World()
        new1 = [2., 2., 5., 8.0]
        w1.set_world(new1)
        self.assertListEqual(new1, w1.get_world())
        self.assertListEqual(new, w.get_world())

class test_Graph(ut.TestCase):
    """test graph operations"""

    def test_graph_properties(self):
        """test graph properties"""
        g = Graph(index=0)
        g.set_title(title="Hello world!")
        self.assertEqual(g.title, "Hello world!")
        g.title = "Hello again"
        self.assertEqual(g.title, "Hello again")
        g.set_subtitle(subtitle="Hello world!")
        self.assertEqual(g.subtitle, "Hello world!")
        g.subtitle = "Hello again"
        self.assertEqual(g.subtitle, "Hello again")

    def test_change_view(self):
        """test if view changing is working"""
        g = Graph(index=1)
        g.set_view(0.0, 0.0, 1.0, 0.5)
        self.assertListEqual(g._view.view_location, [0.0, 0.0, 1.0, 0.5])

    def test_plot(self):
        """test plotting data"""
        g = Graph(index=1)
        x = [0.0, 1.0, 2.0]
        y = [1.0, 2.0, 3.0]
        g.plot(x, y, label="y=x+1", symbol="o", color="red")
        self.assertEqual(g[0]._symbol.type, Symbol.get("o"))
        # both symbol and line are colored
        self.assertEqual(g[0]._symbol.color, Color.get("red"))
        self.assertEqual(g[0]._line.color, Color.get("red"))
        

class test_Axis(ut.TestCase):
    """test Axix functionality"""


class test_Plot(ut.TestCase):
    """test Plot functionality"""

    def test_init_properties(self):
        """default properties"""
        p = Plot(1, 1, description="Hello World")
        self.assertEqual("Hello World", p.description)

    def test_set_default(self):
        """default properties"""
        p = Plot(1, 1)
        p.set_default(font=2)
        self.assertEqual(2, p._default.font)

    def test_change_limits(self):
        """test limits manipulation of all graphs"""
        p = Plot(2, 2)
        p.set_xlim(xmin=1.0, xmax=2.0)
        p.set_ylim(ymin=3.0, ymax=4.0)
        for g in p.get():
            self.assertListEqual(g._world.world_location,
                                 [1.0, 3.0, 2.0, 4.0])

    def test_add_graph(self):
        """graph addition"""
        p = Plot(2, 2)
        p.add_graph()
        self.assertEqual(len(p), 2*2+1)

    def test_regular_graphs(self):
        """generate regular graph alignment"""
        p = Plot(1, 1)
        self.assertEqual(len(p), 1*1)
        p = Plot(3, 4, hgap=[0.01, 0.0, 0.02], vgap=[0.02, 0.0],
                 width_ratios="3:2:1:4", heigh_ratios="1:3:2")
        self.assertEqual(len(p), 3*4)

    def test_subplots(self):
        """test subplots generation"""
        p, _ = Plot.subplots()
        self.assertEqual(len(p), 1)
        p, _ = Plot.subplots(3)
        self.assertEqual(len(p), 3)
        p, _ = Plot.subplots(32)
        self.assertEqual(len(p), 6)

    def test_write(self):
        """writing to agr"""
        p = Plot(1, 1)
        p.plot([0, 1, 2], [3, 2, 1])
        self.assertEqual(len(p), 1)
        tf = tempfile.NamedTemporaryFile()
        with open(tf.name, 'w') as h:
            p.write(h)
        tf.close()


if __name__ == "__main__":
    ut.main()

