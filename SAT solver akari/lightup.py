##!/usr/bin/python3

import pycosat
import itertools
import numpy as np
import math
from pysat.formula import CNF
import time
start = time.time()
n = -1
cnf = CNF()
count = -1
neighbours = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def define_var():
    global n
    global count
    var = []
    for i in range(0, n):
        for j in range(0, n):
            var.append(count)
            count = count - 1
    return var


def decide_length(input1):
    length = len(input1)
    root = math.sqrt(length)
    if int(root + 0.5) ** 2 == length:
        return int(root)
    else:
        return -1


def decipher_input(input1, light, black, zero, one, two, three, four):
    global n
    BOARD = [['0' for i in range(n)] for j in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            if input1[i * n + j] == 'W':
                light[i][j] = abs(light[i][j])
                BOARD[i][j] = 'W'
            elif input1[i * n + j] == 'B':
                black[i][j] = abs(black[i][i])
                BOARD[i][j] = 'B'
            elif input1[i * n + j] == '0':
                zero[i][j] = abs(zero[i][j])
                BOARD[i][j] = '0'
            elif input1[i * n + j] == '1':
                one[i][j] = abs(one[i][j])
                BOARD[i][j] = '1'
            elif input1[i * n + j] == '2':
                two[i][j] = abs(two[i][j])
                BOARD[i][j] = '2'
            elif input1[i * n + j] == '3':
                three[i][j] = abs(three[i][j])
                BOARD[i][j] = '3'
            elif input1[i * n + j] == '4':
                four[i][j] = abs(four[i][j])
                BOARD[i][j] = '4'
            else:
                return "0"
    return BOARD


def decipher_result(arr, BOARD):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if (i*n + j) < len(arr) and arr[i * n + j] >= 0:
                BOARD[i][j] = 'L'
    return BOARD


def is_valid(i, j):
    global n
    if 0 <= i < n and 0 <= j < n:
        return True
    else:
        return False


def find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four):
    global n
    adjacent = []
    for x, y in neighbours:
        if is_black_cell(i + x, j + y, black, zero, one, two, three, four):
            adjacent.append(bulb[i + x][j + y])
    return adjacent


def constraint_zero_cell(black, zero, one, two, three, four, bulb):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if zero[i][j] >= 0:
                adjacent = find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four)
                for x in adjacent:
                    cnf.append([x])
    return cnf


def constraint_one_cell(black, zero, one, two, three, four, bulb):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if one[i][j] >= 0:
                clause = []
                adjacent = find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four)
                if len(adjacent) == 0:
                    cnf.clauses.clear()
                    return cnf
                if len(adjacent) == 1:
                    cnf.append([-adjacent[0]])
                if len(adjacent) == 2:
                    cnf.append([adjacent[0], adjacent[1]])
                    cnf.append([-adjacent[0], -adjacent[1]])
                if len(adjacent) >= 3:
                    for x, y in itertools.combinations(adjacent, 2):
                        cnf.append([x, y])
                    if len(adjacent) == 3:
                        cnf.append([-adjacent[0], -adjacent[1], -adjacent[2]])
                    else:
                        cnf.append([-adjacent[0], -adjacent[1], -adjacent[2], -adjacent[3]])

                # for di, dj in neighbours:
                #     if is_black_cell(i + di, j + dj, black, zero, one, two, three, four):
                #         bulb_cell_1 = bulb[i + di][j + dj]
                #         clause.append(-bulb_cell_1)
                #         for ddi, ddj in neighbours:
                #             if (i + ddi, j + ddj) != (i + di, j + dj):
                #                 if is_black_cell(i + ddi, j + ddj, black, zero, one, two, three, four):
                #                     bulb_cell_2 = bulb[i + ddi][j + ddj]
                #                     cnf.append([bulb_cell_1, bulb_cell_2])
                # cnf.append(clause)
    return cnf


def constraint_two_cell(black, zero, one, two, three, four, bulb):
    # exception case     when there are only two places available
    global n
    for i in range(0, n):
        for j in range(0, n):
            if two[i][j] >= 0:
                adjacent = find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four)
                if len(adjacent) == 1:
                    cnf.clauses.clear()
                    return cnf
                if len(adjacent) == 2:
                    cnf.append([-adjacent[0]])
                    cnf.append([-adjacent[1]])
                if len(adjacent) == 3:
                    for x, y in itertools.combinations(adjacent, 2):
                        cnf.append([-x, -y])

                    cnf.append([-adjacent[0], -adjacent[1], -adjacent[2]])
                    cnf.append([adjacent[0], adjacent[1], adjacent[2]])

                if len(adjacent) == 4:
                    for x, y, z in itertools.combinations(adjacent, 3):
                        cnf.append([x, y, z])
                        cnf.append([-x, -y, -z])

    return cnf


def constraint_three_cell(black, zero, one, two, three, four, bulb):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if three[i][j] >= 0:
                adjacent = find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four)
                if len(adjacent) <= 2:
                    cnf.clauses.clear()
                    return cnf
                if len(adjacent) == 3:
                    cnf.append([-adjacent[0]])
                    cnf.append([-adjacent[1]])
                    cnf.append([-adjacent[2]])
                if len(adjacent) == 4:
                    for x, y in itertools.combinations(adjacent, 2):
                        cnf.append([-x, -y])
                    cnf.append([adjacent[0], adjacent[1], adjacent[2], adjacent[3]])
    return cnf


def constraint_four_cell(black, zero, one, two, three, four, bulb):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if four[i][j] >= 0:
                adjacent = find_adjacent_cells(i, j, bulb, black, zero, one, two, three, four)
                if len(adjacent) <= 3:
                    cnf.clauses.clear()
                    return cnf
                if len(adjacent) == 4:
                    cnf.append([-adjacent[0]])
                    cnf.append([-adjacent[1]])
                    cnf.append([-adjacent[2]])
                    cnf.append([-adjacent[3]])
    return cnf


def constraint_no_two_bulbs_shine(bulb, SR):
    for sr in SR:
        for x in sr:
            for y in sr:
                if sr.index(y) > sr.index(x) and x != y:
                    bulb_1 = bulb[x[0]][[x[1]]]
                    bulb_2 = bulb[y[0]][[y[1]]]
                    cnf.append([bulb_1[0], bulb_2[0]])
    return cnf


def is_black_cell(i, j, black, zero, one, two, three, four):
    if is_valid(i, j):
        if black[i][j] >= 0 or zero[i][j] >= 0 or one[i][j] >= 0 or two[i][j] >= 0 or 0 <= three[i][j] or four[i][
            j] >= 0:
            return False
        else:
            return True
    else:
        return False


def construct_sub_set(black, zero, one, two, three, four, row):
    global n
    SR = []
    for i in range(0, n):
        sr = []
        for j in range(0, n):
            okey = False
            if row:
                if is_black_cell(i, j, black, zero, one, two, three, four):
                    sr.append((i, j))
                else:
                    SR.append(sr)
                    sr = []
                    okey = True

            else:
                if is_black_cell(j, i, black, zero, one, two, three, four):
                    sr.append((j, i))
                else:
                    SR.append(sr)
                    okey = True
                    sr = []
        if not okey:
            SR.append(sr)
            sr = []
    return SR


def find_in_matrix(matrix, element):
    global n
    for row in matrix:
        for elem in row:
            if elem == element:
                return row
    return []


def find_index_in_matrix_for_poz(matrix):
    global n
    values = []
    for i in range(0, n):
        for j in range(0, n):
            if matrix[i][j] >= 0:
                values.append((i, j))
    return values


def constraint_each_cell_is_light_up(light, bulb, SR, SC):
    global n
    cnf2 = []
    for i in range(0, n):
        for j in range(0, n):
            if light[i][j] >= 0:
                sr = set(find_in_matrix(SR, (i, j)))
                sc = set(find_in_matrix(SC, (i, j)))
                sr = sr.union(sc)
                clause = set()
                if sr:
                    for x, y in sr:
                        clause.add(-bulb[x][y])
                append_uniq(cnf2, list(clause))
    for elem in cnf2:
        cnf.append(elem)
    return cnf


def append_uniq(x_list, elem):
    for x in x_list:
        if x == elem:
            return
    x_list.append(elem)


def some_constraints(input2):
    global n
    input3 = str(input2)
    n = decide_length(input3.lstrip())
    if n <= 0:
        return "0"
    bulb = np.array(define_var()).reshape(n, n)
    light = np.array(define_var()).reshape(n, n)
    black = np.array(define_var()).reshape(n, n)
    zero = np.array(define_var()).reshape(n, n)
    one = np.array(define_var()).reshape(n, n)
    two = np.array(define_var()).reshape(n, n)
    three = np.array(define_var()).reshape(n, n)
    four = np.array(define_var()).reshape(n, n)
    BOARD = decipher_input(input3, light, black, zero, one, two, three, four)
    if BOARD == "0":
        return BOARD
    if not constraint_zero_cell(black, zero, one, two, three, four, bulb).clauses:
        return "0"
    if not constraint_one_cell(black, zero, one, two, three, four, bulb).clauses:
        return "0"
    if not constraint_two_cell(black, zero, one, two, three, four, bulb).clauses:
        return "0"
    if not constraint_three_cell(black, zero, one, two, three, four, bulb).clauses:
        return "0"
    if not constraint_four_cell(black, zero, one, two, three, four, bulb).clauses:
        return "0"

    SR = construct_sub_set(black, zero, one, two, three, four, True)
    SR = [sr for sr in SR if sr != []]
    SC = construct_sub_set(black, zero, one, two, three, four, False)
    SC = [sc for sc in SC if sc != []]

    constraint_no_two_bulbs_shine(bulb, SC)
    constraint_no_two_bulbs_shine(bulb, SR)
    constraint_each_cell_is_light_up(light, bulb, SR, SC)
    return BOARD


def solve_light_up(input2):
    global n
    BOARD = some_constraints(input2)
    if BOARD == "0":
        return "0"

    cnf2 = []
    for x in cnf.clauses:
        clause = []
        for y in x:
            clause.append(int(y))
        cnf2.append(clause)

    array = pycosat.solve(cnf2)
    if type(array) == str or len(array) == 0:
        return "0"
    else:
        BOARD = decipher_result(array, BOARD)
        solution = []
        for row in BOARD:
            for elem in row:
                solution.append(elem)
        solution = ''.join(solution)

    return solution

# print('Insert a light-up puzzle:\n')
print(solve_light_up(input()))

print("--- %s seconds ---" % (time.time() - start))
