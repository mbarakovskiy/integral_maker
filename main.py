#!/usr/bin/env python3
import enum
import polynom
import rpn
import fraction as fract
from sympy import *


class ExpressionState(enum.Enum):
    write_everything = 0
    operator = 1
    open_bracket = 2


def check_correctness(expression):
    correct_expression = ""
    open_brackets = []
    argument = "x"
    operators = "^*+-/"
    bracket_count = 0
    state = ExpressionState.write_everything
    for i in range(len(expression)):
        if i == 0:
            if expression[0] not in "(+-x":
                if not expression[0].isdigit():
                    raise Exception('You cannot start expression with this symbol:',
                                    expression[0])
        symbol = expression[i]
        if symbol == "(":
            if i > 0 and (expression[i - 1].isdigit() or
                          expression[i - 1] in "x)"):
                correct_expression += "*"
            bracket_count += 1
            open_brackets.append(i)
            correct_expression += symbol
            state = ExpressionState.open_bracket
            continue
        if symbol == ")":
            if state == ExpressionState.operator or \
                    state == ExpressionState.open_bracket or bracket_count == 0:
                raise Exception("Incorrect brackets, position — ", i)
            bracket_count -= 1
            open_brackets.pop()
            correct_expression += symbol
            state = ExpressionState.write_everything
            continue

        if symbol.isdigit():
            if i > 0 and (expression[i - 1] == ")" or
                          expression[i - 1] == argument):
                correct_expression += "*"
            correct_expression += symbol
            state = ExpressionState.write_everything
            continue
        if symbol in operators:
            if symbol == "+" and (i == 0 or expression[i - 1] == "("):
                state = ExpressionState.operator
                continue
            if symbol in "*/^" and state == ExpressionState.open_bracket or \
                    state == ExpressionState.operator:
                raise Exception("Incorrect operator, position — ", i)
            correct_expression += symbol
            state = ExpressionState.operator
            continue
        if symbol == argument:
            if i > 0 and (expression[i - 1].isdigit() or
                          expression[i - 1] in "x)"):
                correct_expression += "*"
            correct_expression += argument
            state = ExpressionState.write_everything
        if symbol != argument:
            raise Exception("Unknown symbol, position - ", i)
    if state == ExpressionState.operator:
        raise Exception("Incorrect: you cannot end expression with operator, position — ", correct_expression[-1])
    if bracket_count == 0:
        return correct_expression
    else:
        raise Exception("Incorrect brackets, position — ", open_brackets[0])


def split_to_summands(string):
    summands = []
    summand = ""
    brackets_count = 0
    for symb in string:
        if symb == "(":
            brackets_count += 1
            summand += symb
            continue
        if symb == ")":
            brackets_count -= 1
            summand += symb
            continue
        if brackets_count == 0 and symb in "+-":
            summands.append(summand)
            if symb == "+":
                summand = ""
            else:
                summand = "(-1)*"
            continue
        summand += symb
    summands.append(summand)
    return summands


def delete_unnecessary_brackets(expression):
    brackets = []
    to_delete = []
    for i in range(len(expression)):
        symbol = expression[i]
        if symbol == "(":
            if i == 0 or expression[i - 1] in "(+-":
                brackets.append({i: False})
                continue
            if expression[i - 1] in "*^/":
                brackets.append({i: True})
                continue
        if symbol == ")":
            bracket = brackets.pop()
            index = list(bracket.keys())[0]
            if i + 1 == len(expression) or expression[i + 1] in "+-)":
                if bracket[index]:
                    continue
                else:
                    to_delete.append(index)
                    to_delete.append(i)

    result = ""
    for i in range(len(expression)):
        if i not in to_delete:
            result += expression[i]
    return result


def split_to_num_denom(expression):
    brackets_count = 0
    fract = ["", ""]
    state = 0
    for symbol in expression:
        if symbol == "(":
            brackets_count += 1
            fract[state % 2] += symbol
            continue
        if symbol == ")":
            brackets_count -= 1
            fract[state % 2] += symbol
            continue
        if symbol == "/" and brackets_count == 0:
            fract[state % 2] += "*"
            state += 1
            continue
        fract[state % 2] += symbol
    for state in range(2):
        if len(fract[state]) > 0 and fract[state][len(fract[state]) - 1] == "*":
            fract[state] = fract[state][:-1]
    return fract


def integrate_polynom(poly):
    result = ""
    for key in poly:
        number = poly[key] / (key + 1)
        if number > 0 and result != "":
            result += " + "
        if number % 0.25 == 0:
            if number != 1:
                result += str(number) + "*"
        else:
            result += '({0}/{1})*'.format(poly[key], key + 1)
        degree = key + 1
        if degree == 1:
            result += "x"
        else:
            result += 'x^{0}'.format(degree)
    return result


def make_square_poly(poly):
    mult = poly[2]
    if abs(poly[2]) != 1:
        poly, rem = polynom.polynom_div(poly, {0: poly[2]})
    b = (abs(poly[1]) / 2)**2
    if 0 in poly:
        rem = poly[0] - b
    else:
        rem = 0 - b
    if poly[1] > 0:
        square = 'x+{0}'.format(b**(1/2))
        return mult, square, rem
    else:
        square = 'x-{0}'.format(b**(1/2))
        return mult, square, rem


def integrate_fraction_fin(numerator, denominator):
    denom_keys = list(denominator.keys())
    denom_keys.sort(reverse=True)
    if len(numerator) == 1 and 0 in numerator:
        if denom_keys[0] == 1:
            if 0 in denominator:
                if denominator[0] > 0 and denominator[1] > 0 or denominator[0] < 0 and denominator[1] < 0:
                    return '{0}*ln(x+{1})'.format(str(numerator[0] / denominator[1]), str(denominator[0] / denominator[1]))
                return '{0}*ln(x{1})'.format(str(numerator[0] / denominator[1]), str(denominator[0] / denominator[1]))
            else:
                return '{0}*ln(x)'.format(str(numerator[0] / denominator[1]))
        if len(denom_keys) == 1 and 0 not in denominator:
            degree = (denom_keys[0] - 1) * (-1)
            return '{0}*x^({1})'.format(str(numerator[0] / (denominator[denom_keys[0]] * degree)), degree)
        if 2 in denominator and 0 in denominator and len(denominator) == 2:
            if denominator[2] != 1:
                numerator, rem = polynom.polynom_div(numerator, {0:denominator[2]})
                denominator, rem = polynom.polynom_div(denominator, {0:denominator[2]})
            if denominator[0] > 0:
                return '({0})*(1/{1}^(1/2))*arctg(x/{1}^(1/2))'.format(str(numerator[0]), str(denominator[0]))
            return '({0})*(1/(2*{1}^(1/2)))*ln(x - {2}^(1/2))/(x + {2}^(1/2))'.format(
                str(numerator[0]), str(denominator[0]), str(abs(denominator[0])))
        if denom_keys[0] == 2:
            mult1, square, rem = make_square_poly(denominator)
            if rem == 0:
                return '({0})*({1})^({2})'.format(str(numerator[0] / mult1 * (-1)), square, -1)
            if rem > 0:
                return '({0})arctg({1}/{2}^(1/2))'.format(
                    str(numerator[0] / (mult1 * rem ** (1 / 2))), square, str(rem))
            else:
                return '({0})*ln({1} - {2}^(1/2))/({1}+ {2}^(1/2))'.format(
                    str(numerator[0] / (mult1 * 2 * rem ** (1 / 2))), square, abs(rem))
    if len(numerator) == 1 and 1 in numerator:
        if len(denominator) == 1 and 0 not in denominator:
            numerator, rem = polynom.polynom_div(numerator, {1: 1})
            denominator, rem = polynom.polynom_div(denominator, {1: 1})
            return integrate_fraction_fin(numerator, denominator)
        if len(denominator) == 2 and 1 not in denominator and denom_keys[0] == 2:
            a = denominator[0] / denominator[2]
            if a > 0:
                return '{0}*ln(x^2+{1})'.format(str(numerator[1] / (denominator[2] * 2)), str(a))
    numerator = "(" + polynom.translate_to_string(numerator) + ")"
    denominator = "(" + polynom.translate_to_string(denominator) + ")"
    x = Symbol('x')
    expression = '{0}/{1}'.format(numerator, denominator)
    expression = str(integrate(expression, x))
    expression = expression.replace("**", "^")
    expression = expression.replace("atan", "arctg")
    return expression


def integrate_linear(string):
    string = rpn.make_notation(string)
    string = rpn.translate_to_polynom(string)
    if string is False:
        raise Exception("Error")
    return integrate_polynom(string)


def right_fraction(numerator, denominator):
    result = []
    denominator = polynom.decompose_by_sympy(denominator)
    if len(denominator) == 1:
        result.append(integrate_fraction_fin(numerator, denominator[0]))
        return result
    expression = fract.decompose_to_simplest(numerator, denominator)
    for tuple in expression:
        result.append(integrate_fraction_fin(tuple[0], tuple[1]))
    return result


def wrong_fraction(numerator, denominator):
    result = []
    poly = polynom.polynom_div(numerator, denominator)
    result.append(integrate_polynom(poly[0]))
    if len(poly[1]) == 1 and 0 in poly[1]:
        if poly[1][0] == 0:
            return result
    result.extend(right_fraction(poly[1], denominator))
    return result


def integrate_fraction(fraction):
    result = []
    numerator = fraction[0]
    denominator = fraction[1]
    num_keys = list(numerator.keys())
    denom_keys = list(denominator.keys())
    num_keys.sort(reverse=True)
    denom_keys.sort(reverse=True)
    if num_keys[0] >= denom_keys[0]:
        result.extend(wrong_fraction(numerator, denominator))
    else:
        result.extend(right_fraction(numerator, denominator))
    return result


def print_expression(expr):
    result = ""
    for i in range(len(expr)):
        if i == 0:
            result = expr[i]
            continue
        if expr[i][0] != "-":
            result += " + " + expr[i]
            continue
        result += " - " + expr[i][1:]
    result += " + C"
    return result


def integrate(log):
    log = log.replace(" ", "")
    log = check_correctness(log)
    if log is False:
        print("Task failed")
        return
    log = delete_unnecessary_brackets(log)
    summands = split_to_summands(log)
    expression = []
    for summand in summands:
        fractions = split_to_num_denom(summand)
        if len(fractions[1]) == 0:
            expression.append(integrate_linear(fractions[0]))
            continue
        for i in range(2):
            fractions[i] = rpn.make_notation(fractions[i])
            fractions[i] = rpn.translate_to_polynom(fractions[i])
            if fractions[i] is False:
                return
        if len(fractions[1]) == 0:
            raise Exception("Unexpected division by zero")
        if len(fractions[1]) == 1 and 0 in fractions[1]:
            poly, rem = polynom.polynom_div(fractions[0], fractions[1])
            expression.append(integrate_polynom(poly))
            continue
        expression.extend(integrate_fraction(fractions))
    expression = print_expression(expression)
    return expression


def try_start(welcome_message="Enter expression"):
    print(welcome_message)
    print("Use variable - x")
    input_data = input()
    expression = integrate(input_data)
    if expression is not None:
        print(expression)
    else:
        try_start("Enter other expression")


if __name__ == '__main__':
    try_start()
