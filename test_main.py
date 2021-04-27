import unittest
import main


class TestMain(unittest.TestCase):
    def test_Check_Correctness_mistakes_by_user(self):
        expression = '()'
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = '('
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = ')'
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = ')('
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = '(x+1))'
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = '2++2'
        # result = main.check_correctness(expression)
        # self.assertFalse(result)
        #
        # expression = '2+^2'
        # result = main.check_correctness(expression)
        # self.assertFalse(result)

    def test_Check_Correctness_no_mistakes_by_user(self):
        expression = '4(4+5)x^3/(x^2+2)/(x+1)/(x+2)'
        result = main.check_correctness(expression)
        self.assertNotEqual(result, False)

        expression = '(x^3+x^2+1)/((x^2+1)(x^2-x+1))'
        result = main.check_correctness(expression)
        self.assertNotEqual(result, False)

    def test_Split_to_summands(self):
        expression = '4*(4+5)*x^3/(x^2+2)/(x+1)/(x+2)'
        result = main.split_to_summands(expression)
        self.assertEqual(len(result), 1)

        expression = '4*(4+5)*x^3+(x^2+2)+(x+1)+(x+2)'
        result = main.split_to_summands(expression)
        self.assertEqual(len(result), 4)

    def test_delete_unnecessary_brackets(self):
        expression = '4*(4+5)*x^3/(x^2+2)/(x+1)/(x+2)'
        result = main.delete_unnecessary_brackets(expression)
        self.assertEqual(result, '4*(4+5)*x^3/(x^2+2)/(x+1)/(x+2)')

        expression = '(4*((4)+5)*x^3+((x^2+2))+(x+1)+(x+(2)))'
        result = main.delete_unnecessary_brackets(expression)
        self.assertEqual(result, '4*(4+5)*x^3+x^2+2+x+1+x+2')

        expression = '(4)*((4+5))*x^(3)/((x^2+(2)))/(x+(1))/(((x)+2))'
        result = main.delete_unnecessary_brackets(expression)
        self.assertEqual(result, '(4)*(4+5)*x^(3)/(x^2+2)/(x+1)/(x+2)')

    def test_Split_to_nom_denom(self):
        expression = '4*(4+5)*x^3/(x^2+2)/(x+1)/(x+2)'
        fraction = main.split_to_num_denom(expression)
        self.assertEqual(fraction[0], '4*(4+5)*x^3*(x+1)')
        self.assertEqual(fraction[1], '(x^2+2)*(x+2)')

        expression = '(x^3+x^2+1)/((x^2+1)*(x^2-x+1))'
        fraction = main.split_to_num_denom(expression)
        self.assertEqual(fraction[0], '(x^3+x^2+1)')
        self.assertEqual(fraction[1], '((x^2+1)*(x^2-x+1))')

        expression = '1/x'
        fraction = main.split_to_num_denom(expression)
        self.assertEqual(fraction[0], '1')
        self.assertEqual(fraction[1], 'x')

        expression = '1/(x+1)'
        fraction = main.split_to_num_denom(expression)
        self.assertEqual(fraction[0], '1')
        self.assertEqual(fraction[1], '(x+1)')

        expression = '(x+1)/x'
        fraction = main.split_to_num_denom(expression)
        self.assertEqual(fraction[0], '(x+1)')
        self.assertEqual(fraction[1], 'x')


if __name__ == '__main__':
    unittest.main()
