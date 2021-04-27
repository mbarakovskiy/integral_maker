import polynom

Notation = []


def get_number(i, data):
    num = ''
    while i < len(data) and (data[i].isdigit() or data[i] == '.'):
        num += data[i]
        i += 1
    return num


def try_negative(i, data):
    num = ''
    if i > 0 and data[i - 1] == '(' or i == 0:
        num = get_number(i + 1, data)
    if len(num) > 0:
        if float(num) % 1 == 0:
            return (-1) * int(num)
        return (-1) * float(num)
    return '-'


def make_adding(operators):
    i = len(operators) - 1
    while i >= 0:
        if operators[i] == '(':
            operators.pop()
            break
        Notation.append(operators.pop())
        i -= 1


def get_priority(operator):
    if operator == '+' or operator == '-':
        return 0
    if operator == '*' or operator == '/':
        return 1
    if operator == '^':
        return 2


def add_operators(operators, elem):
    if elem == ')':
        make_adding(operators)
        return
    if elem == '(' or len(operators) == 0 or len(operators) > 0 and operators[len(operators) - 1] == '(' or \
            get_priority(elem) > get_priority(
            operators[len(operators) - 1]):
        operators.append(elem)
        return
    if len(operators) > 0 and operators[len(operators) - 1] != '(' and \
            int(get_priority(elem)) < int(get_priority(operators[len(operators) - 1])):
        make_adding(operators)
        operators.append(elem)
        return
    if len(operators) > 0 and get_priority(elem) == get_priority(operators[len(operators) - 1]):
        Notation.append(operators[len(operators) - 1])
        operators.pop()
        operators.append(elem)


def make_notation(data):
    Notation.clear()
    ops = '+-*/^()'
    opers = []
    variable = ''
    i = 0
    brackets_count = 0
    while i < len(data):
        symb = data[i]
        if symb == '-':
            symb = str(try_negative(i, data))
            if symb == '-':
                add_operators(opers, symb)
            else:
                Notation.append(symb)
            i += len(symb)
            continue
        if symb.isdigit():
            symb = get_number(i, data)
            Notation.append(symb)
            i += len(symb)
            continue
        if symb in ops:
            if symb == '(':
                brackets_count += 1
            if symb == ')':
                brackets_count -= 1
            add_operators(opers, symb)
        else:
            if variable == '':
                variable = symb
            else:
                if variable != symb:
                    print('Unknown symbol - ', symb)
                    return
            Notation.append(symb)
        if brackets_count < 0:
            print('error')
            return
        i += len(symb)
    make_adding(opers)
    if len(opers) > 0 or brackets_count != 0:
        print('error')
        return
    return Notation


def translate_to_polynom(notation):
    opers = '*/+-^'
    expression = []
    for e in notation:
        if e not in opers:
            if 'x' not in str(e):
                expression.append({0: eval(e)})
                continue
            expression.append({1: 1})
        second = expression.pop()
        first = expression.pop()
        if e == '*':
            result = polynom.polynom_mult(first, second)
        if e == '+':
            result = polynom.polynom_sum(first, second)
        if e == '-':
            result = polynom.polynom_sub(first, second)
        if e == '^':
            result = polynom.polynom_pow(first, second)
            if not result:
                return False
        if e == '/':
            result, rem = polynom.polynom_div(first, second)
        expression.append(result)
    return expression[0]
