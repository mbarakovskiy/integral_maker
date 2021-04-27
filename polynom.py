#!/usr/bin/env python3

import sympy


def polynom_pow(first, second):
    if 0 not in second or len(second) > 1:
        print("Incorrect degree")
        return False
    result = first.copy()
    for e in range(second[0] - 1):
        result = polynom_mult(result, first)
    return result


def polynom_sum(first, second):
    for e in second:
        val = first.get(e)
        if val is None:
            first[e] = second[e]
        else:
            first[e] += second[e]
        if first[e] == 0:
            del first[e]
    return first


def polynom_sub(first, second):
    for e in second:
        second[e] *= -1
    return polynom_sum(first, second)


def polynom_div(first, second):
    first_keys = list(first.keys())
    second_keys = list(second.keys())
    first_keys.sort(reverse=True)
    second_keys.sort(reverse=True)
    mult = {}
    rem = first.copy()
    while len(rem) > 0 and first_keys[0] >= second_keys[0]:
        key = first_keys[0] - second_keys[0]
        val = rem[first_keys[0]] / second[second_keys[0]]
        mult[key] = val
        sec = polynom_mult({key: val}, second)
        rem = polynom_sub(rem, sec)
        first_keys = list(rem.keys())
        first_keys.sort(reverse=True)
    return mult, rem


def polynom_mult(first, second):
    result = {}
    for f in first:
        for s in second:
            key = f + s
            val = result.get(key)
            if val is None:
                result[key] = second[s] * first[f]
            else:
                result[key] += second[s] * first[f]
    return result


def check_root(polynom, keys, root):
    res = 0
    for i in keys:
        res += polynom[i] * (root ** i)
    if res == 0:
        return True
    return False


def translate_to_polynoms(string):
    polyms = string.split("*(")
    result = []
    for poly in polyms:
        polynom = {}
        numbers = ["", ""]
        poly = poly.replace("(", "")
        poly = poly.replace(")", "")
        poly = poly.replace("x**", "^")
        poly = poly.replace("*", "")
        poly = poly.replace("x", "^1")
        poly = poly.replace(" ", "")
        poly += "+"
        index = 0
        for symb in poly:
            if symb in "+-":
                if index == 1:
                    index = 0
                    if numbers[0] == "-":
                        numbers[0] = "-1"
                    if numbers[0] != "":
                        polynom[int(numbers[1])] = int(numbers[0])
                    else:
                        polynom[int(numbers[1])] = 1
                    numbers = ["", ""]
                if index == 0 and numbers[0] != "":
                    polynom[0] = int(numbers[0])
            if symb in "^":
                index = 1
                continue
            numbers[index] += symb
        result.append(polynom)
    return result


def translate_to_string(polynom):
    string_poly = ""
    ads = ""
    for key in polynom.keys():
        if key == 0:
            if polynom[key] > 0:
                string_poly += ads + str(polynom[key])
                ads = "+"
                continue
            string_poly += str(polynom[key])
            ads = "+"
            continue
        if polynom[key] > 0:
            string_poly += ads + str(polynom[key]) + "*x**" + str(key)
        else:
            string_poly += str(polynom[key]) + "*x**" + str(key)
        ads = "+"
    return string_poly


def decompose_by_sympy(polynom):
    string_poly = translate_to_string(polynom)
    poly = sympy.factor(str(string_poly))
    return translate_to_polynoms(str(poly))
