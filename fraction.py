import numpy
import polynom


def form_result(denom, result, specs_one, specs_two):
    final = []
    result = result.tolist()
    for i in range(len(result)):
        res = result[i]
        if res != 0:
            if i in specs_two:
                n = {1: res}
            else:
                n = {0: res}
            final.append((n, denom[specs_one[i]]))
    return final


def decompose_to_simplest(nom, denom):
    variable = []
    specs_one = []
    specs_two = []
    max = 0
    flag = False
    for i in range(len(denom)):
        if list(denom[i].keys())[0] == 2 and len(denom[i]) != 1:
            specs_two.append(len(specs_one))
            specs_one.append(i)
            variable.append({1: 1})
            flag = True
        variable.append({0: 1})
        specs_one.append(i)
        j = 0
        index = len(variable)
        for poly in denom:
            if j != i:
                if flag:
                    variable[index - 2] = polynom.polynom_mult(variable[index - 2], poly)
                variable[index - 1] = polynom.polynom_mult(variable[index - 1], poly)
            j += 1
        flag = False
    for poly in variable:
        degree = list(poly.keys())[0]
        if degree > max:
            max = degree
    matrix = []
    means = []
    j = 0
    for degree in range(max + 1):
        if degree in nom:
            means.append(nom[degree])
        else:
            means.append(0)
        matrix.append([])
        sum = 0
        for poly in variable:
            if degree in poly:
                matrix[j].append(poly[degree])
                sum += abs(poly[degree])
                continue
            matrix[j].append(0)
        if sum == 0:
            matrix.pop(j)
            means.pop(j)
            continue
        j += 1
    M1 = numpy.array(matrix)  # Матрица (левая часть системы)
    v1 = numpy.array(means)  # Вектор (правая часть системы)
    try:
        result = numpy.linalg.solve(M1, v1)
        return form_result(denom, result, specs_one, specs_two)
    except:
        return False

