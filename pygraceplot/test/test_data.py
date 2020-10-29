#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest as ut
import numpy as np
from pygraceplot.data import Data

class test_xy_data(ut.TestCase):
    """xy data object"""
    def test_raise(self):
        x = [1, 2]
        y = [3, 4]
        e = [0.1, 0.2, 0.3]
        self.assertRaises(ValueError, Data, x, y + [5,])
        self.assertRaises(ValueError, Data, x, y, dx=e)

    def test_get(self):
        """test data extraction"""
        x = [1, 2]
        y = [3, 4]
        xy = np.array([x, y])
        data = Data(x, y)
        self.assertTrue(np.all(xy == data.get()))
        self.assertTrue(np.all(np.transpose(xy) == np.array(data.get(True))))

    def test_export(self):
        """test data export"""
        x = (1.0, 2.0, 3.0)
        y = (3.0, 4.0, 5.0)
        data = Data(x, y)
        s_transp = ["1.0 3.0",
                    "2.0 4.0",
                    "3.0 5.0"]
        s_normal = ["1.0 2.0 3.0",
                    "3.0 4.0 5.0"]
        s_transp_51f = ["  1.0   3.0",
                        "  2.0   4.0",
                        "  3.0   5.0"]
        s_normal_51f = ["  1.0   2.0   3.0",
                        "  3.0   4.0   5.0"]
        s_transp_51f_42f = ["  1.0 3.00",
                            "  2.0 4.00",
                            "  3.0 5.00"]
        s_normal_51f_42f = ["  1.0   2.0   3.0",
                            "3.00 4.00 5.00"]
        self.assertListEqual(s_normal, data.export(form="{:3.1f}"))
        self.assertListEqual(s_transp, data.export(form="{:3.1f}", transpose=True))
        self.assertListEqual(s_normal_51f, data.export(form="{:5.1f}"))
        self.assertListEqual(s_transp_51f, data.export(form="{:5.1f}", transpose=True))
        self.assertListEqual(s_normal_51f_42f, data.export(form=["{:5.1f}", "{:4.2f}"]))
        self.assertListEqual(s_transp_51f_42f,
                             data.export(form=["{:5.1f}", "{:4.2f}"], transpose=True))
        
if __name__ == "__main__":
    ut.main()
