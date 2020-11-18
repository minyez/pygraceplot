#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest as ut
import os

from pygraceplot.utils import encode_string, get_file_ext, get_filename_wo_ext, extract_data_from_agr

class test_string_encoder(ut.TestCase):
    """test encoder to get grace-favored text string"""
    def test_greek(self):
        """encoding greek"""
        self.assertEqual(encode_string(r"\Gamma \beta"), r"\xG\f{} \xb\f{}")

    def test_special(self):
        """encoding special characters"""
        self.assertEqual(encode_string(r"\AA \BB"), r"\cE\C \BB")

    def test_italic(self):
        """encoding special characters"""
        self.assertEqual(encode_string(r"/this is italic/, this not"),
                         r"\f{Times-Italic}this is italic\f{}, this not")
        self.assertEqual(encode_string(r"/italic here/, /also here/"),
                         r"\f{Times-Italic}italic here\f{}, \f{Times-Italic}also here\f{}")

    def test_super_or_subscript(self):
        """encoding either super or subscript """
        subs = [
            ("A_{b}", "A\\sb\\N"),
            ("A_{b}C_{d}", "A\\sb\\NC\\sd\\N"),
            ("C^{d}", "C\\Sd\\N"),
            ("A^{b}C_{d}", "A\\Sb\\NC\\sd\\N"),
            ]
        for latex, encoded in subs:
            self.assertEqual(encode_string(latex), encoded)

class test_file_ext(ut.TestCase):
    """test extension extract"""
    def test_ext(self):
        """get extension name"""
        self.assertEqual(get_file_ext(__file__), "py")
        self.assertEqual(get_file_ext("test.dat"), "dat")
        self.assertEqual(get_file_ext("somedir/test.dat"), "dat")

    def test_filename_wo_ext(self):
        """get file name without extension"""
        self.assertEqual(get_filename_wo_ext(__file__), "test_utils")
        self.assertEqual(get_filename_wo_ext("test.dat"), "test")
        self.assertEqual(get_filename_wo_ext("somedir/test.dat"), "test")

class test_extract_data(ut.TestCase):
    def test_4g_1111(self):
        """extract data from four graph with 1 dataset each"""
        pagr = os.path.join(os.path.dirname(__file__), "fake_4g_1111.agr")
        legends, types, data = extract_data_from_agr(pagr)
        self.assertEqual(len(legends), 4)
        self.assertEqual(len(types), 4)
        self.assertEqual(len(data), 4)



if __name__ == "__main__":
    ut.main()

