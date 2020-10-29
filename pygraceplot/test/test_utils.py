#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest as ut

from pygraceplot.utils import encode_string

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


if __name__ == "__main__":
    ut.main()

