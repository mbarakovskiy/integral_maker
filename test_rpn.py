#!/usr/bin/env python3

import unittest
import rpn


class TestRPN(unittest.TestCase):
    def test_simple_rpn(self):
        expression = 'x+1'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', '1', '+'])
        self.assertEqual(rpn.translate_to_polynom(notation), {1: 1, 0: 1})

        expression = 'x-1'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', '1', '-'])
        self.assertEqual(rpn.translate_to_polynom(notation), {1: 1, 0: -1})

        expression = 'x*1'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', '1', '*'])
        self.assertEqual(rpn.translate_to_polynom(notation), {1: 1})

        expression = 'x^2'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', '2', '^'])
        self.assertEqual(rpn.translate_to_polynom(notation), {2: 1})

        expression = 'x^x'  #Incorrect degree
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', 'x', '^'])
        self.assertFalse(rpn.translate_to_polynom(notation))

        expression = '2^2'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['2', '2', '^'])
        self.assertEqual(rpn.translate_to_polynom(notation), {0: 4})

    def test_translation_to_rpn(self):
        expression = '(1-2)*(3+4)'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['1', '2', '-', '3', '4', '+', '*'])
        self.assertEqual(rpn.translate_to_polynom(notation), {0: -7})

        expression = '(1+(-2))*(3+4)'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['1', '-2', '+', '3', '4', '+', '*'])
        self.assertEqual(rpn.translate_to_polynom(notation), {0: -7})

        expression = '(x^2+1)*(x^2-x+1)'
        notation = rpn.make_notation(expression)
        self.assertEqual(notation, ['x', '2', '^', '1', '+', 'x', '2', '^', 'x', '-', '1', '+', '*'])
        self.assertEqual(rpn.translate_to_polynom(notation), {4: 1, 3: -1, 2: 2, 1: -1, 0: 1})


if __name__ == '__main__':
    unittest.main()
