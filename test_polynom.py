#!/usr/bin/env python3

import unittest
import polynom


class TestPolynom(unittest.TestCase):
    def test_polynom_sum(self):
        poly1 = {0: 1}
        poly2 = {0: 2}
        self.assertEqual(polynom.polynom_sum(poly1, poly2), {0: 3})

        poly1 = {0: 1}
        poly2 = {0: -1}
        self.assertEqual(polynom.polynom_sum(poly1, poly2), {})

        poly1 = {1: 1, 0: 1}
        poly2 = {0: -1}
        self.assertEqual(polynom.polynom_sum(poly1, poly2), {1: 1})

        poly1 = {2: 3, 1: 1, 0: 1}
        poly2 = {2: 3, 1: 2, 0: 2}
        self.assertEqual(polynom.polynom_sum(poly1, poly2), {2: 6, 1: 3, 0: 3})

    def test_polynom_subtraction(self):
        poly1 = {0: 1}
        poly2 = {0: 2}
        self.assertEqual(polynom.polynom_sub(poly1, poly2), {0: -1})

        poly1 = {0: 1}
        poly2 = {0: -1}
        self.assertEqual(polynom.polynom_sub(poly1, poly2), {0: 2})

        poly1 = {0: 1}
        poly2 = {0: 1}
        self.assertEqual(polynom.polynom_sub(poly1, poly2), {})

        poly1 = {1: 1, 0: 1}
        poly2 = {0: -1}
        self.assertEqual(polynom.polynom_sub(poly1, poly2), {1: 1, 0: 2})

        poly1 = {2: 3, 1: 1, 0: 1}
        poly2 = {2: 3, 1: 2, 0: 2}
        self.assertEqual(polynom.polynom_sub(poly1, poly2), {1: -1, 0: -1})

    def test_polynom_division(self):
        poly1 = {0: 1}
        poly2 = {0: 2}
        self.assertEqual(polynom.polynom_div(poly1, poly2), ({0: 0.5}, {}))

        poly1 = {0: 4}
        poly2 = {0: -2}
        self.assertEqual(polynom.polynom_div(poly1, poly2), ({0: -2}, {}))

        poly1 = {1: 1, 0: 1}
        poly2 = {1: 2, 0: 1}
        self.assertEqual(polynom.polynom_div(poly1, poly2), ({0: 0.5}, {0: 0.5}))

        poly1 = {2: 1, 1: 4, 0: 3}  # (x+1)*(x+3)/(x+1) = (x+3)
        poly2 = {1: 1, 0: 1}
        self.assertEqual(polynom.polynom_div(poly1, poly2), ({1: 1, 0: 3}, {}))

        poly1 = {2: 3, 1: 1, 0: 1}
        poly2 = {2: 3, 1: 1, 0: 1}
        self.assertEqual(polynom.polynom_div(poly1, poly2), ({0: 1}, {}))

    def test_polynom_multiplication(self):
        poly1 = {0: 3}
        poly2 = {0: 2}
        self.assertEqual(polynom.polynom_mult(poly1, poly2), {0: 6})

        poly1 = {0: 1}
        poly2 = {0: -1}
        self.assertEqual(polynom.polynom_mult(poly1, poly2), {0: -1})

        poly1 = {0: -2}
        poly2 = {0: -4}
        self.assertEqual(polynom.polynom_mult(poly1, poly2), {0: 8})

        poly1 = {0: 0}
        poly2 = {0: -4}
        self.assertEqual(polynom.polynom_mult(poly1, poly2), {0: 0})

        poly1 = {1: 1, 0: 1}
        poly2 = {0: -2}
        self.assertEqual(polynom.polynom_mult(poly1, poly2), {1: -2, 0: -2})

        poly1 = {2: 3, 1: 1, 0: 1}
        poly2 = {2: 3, 1: 2, 0: 2}
        self.assertEqual(len(polynom.polynom_mult(poly1, poly2)), 5)

    def test_polynom_root(self):
        poly = {2: 1, 1: 4, 0: 3}  # (x+1)*(x+3)
        self.assertFalse(polynom.check_root(poly, [2, 1, 0], 1))
        self.assertFalse(polynom.check_root(poly, [2, 1, 0], 3))
        self.assertTrue(polynom.check_root(poly, [2, 1, 0], -1))
        self.assertTrue(polynom.check_root(poly, [2, 1, 0], -3))

    def test_polynom_decompose(self):
        poly = {2: 1, 1: 4, 0: 3}
        poly = polynom.decompose_by_sympy(poly)
        self.assertEqual(len(poly), 2)
        self.assertTrue({1: 1, 0: 1} in poly)
        self.assertTrue({1: 1, 0: 3} in poly)


if __name__ == '__main__':
    unittest.main()
