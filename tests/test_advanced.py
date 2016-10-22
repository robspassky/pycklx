# -*- coding: utf-8 -*-

from .context import pycklx

import unittest


def done():
    print("All Done")


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        pycklx.topickle("tests/simple.xml", done)


if __name__ == '__main__':
    unittest.main()
