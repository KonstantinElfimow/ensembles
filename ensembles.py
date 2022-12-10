from functools import reduce
import numpy as np


accurateness: int = 6  # Округдение до знака


def test_valid(input_ensemble: dict) -> bool:
    # Сумма вероятностей ансамбля должна быть равна 1.0
    summary: float = reduce(lambda x, y: round(x + y, accurateness), input_ensemble.values())
    return abs(1.0 - summary) < 1e-10


def conditional_entropy(p: list, conditional_p: list) -> float:
    """ Условная энтропия """
    H: float = 0
    s1: str = ''

    start: int = 0
    end: int = len(conditional_p) // len(p)
    for p1 in p:
        H_i: float = 0
        for p2 in conditional_p[start: end]:
            H_i = round(H_i + (-p2 * np.log2(p2)), accurateness)
        start, end = end, (end + (len(conditional_p) // len(p)))

        print('H_i = {}'.format(round(H_i, 2)))
        H = round(H + p1 * H_i, accurateness)
        s1 += '{} * {} + '.format(p1, H_i)

    print('H = {} = {} (бит)'.format(s1, H))
    print()

    return H


def entropy(p: list) -> float:
    """ Энтропия """
    H: float = round(sum([round(-x * np.log2(x), accurateness) for x in p]), accurateness)
    s1: str = '- (' + ' + '.join([f'{x} * log2({x})' for x in p]) + ')'
    s2: str = ' + '.join([f'{round(-x * np.log2(x), accurateness)}' for x in p])

    print('H = {} = {} = {} (бит)'.format(s1, s2, H))
    print()

    return H


def calculate_conditional_p_x_p_y(X: dict, Y: dict, XY: dict) -> dict:
    conditional_X_Y: dict = dict()

    for y, y_value in Y.items():
        for x, x_value in X.items():
            conditional_X_Y['{}|{}'.format(x, y)] = round(XY.get('{} {}'.format(x, y)) / y_value, accurateness)

    for x, x_value in X.items():
        for y, y_value in Y.items():
            conditional_X_Y['{}|{}'.format(y, x)] = round(XY.get('{} {}'.format(x, y)) / x_value, accurateness)
    return conditional_X_Y


def calculate_p_x_p_y(X: dict, Y: dict) -> dict:
    X_and_Y: dict = dict()

    for y, y_value in Y.items():
        for x, x_value in X.items():
            X_and_Y['{} {}'.format(x, y)] = round(x_value * y_value, accurateness)
    return X_and_Y


def make_X_and_Y(XY: dict) -> (dict, dict):
    X: dict = dict()
    Y: dict = dict()

    for key, value in XY.items():
        x_y = key.split()
        X[x_y[0]] = round(X.get(x_y[0], 0) + value, accurateness)
        Y[x_y[1]] = round(Y.get(x_y[1], 0) + value, accurateness)
    return X, Y


def is_dependent(XY: dict, X_and_Y: dict) -> bool:
    for key in XY.keys():
        if XY[key] != X_and_Y[key]:
            return True
    return False


def task(XY: dict):
    X, Y = make_X_and_Y(XY)
    print('X = ', X)
    print()
    print('Y = ', Y)
    print()
    if not test_valid(X) or not test_valid(Y):
        raise ValueError('Сумма вероятностей компонентов X или Y не равна 1.0')
    X_and_Y = calculate_p_x_p_y(X, Y)
    print('Для определения независимости:', X_and_Y)
    print()
    conditional_X_Y = calculate_conditional_p_x_p_y(X, Y, XY)
    print('Условные вероятности: ', conditional_X_Y)
    print()

    print('H(X):')
    H_x = entropy(list(X.values()))
    print('H(Y):')
    H_y = entropy(list(Y.values()))
    print('H(XY):')
    H_x_y = entropy(list(XY.values()))
    print('Hy(X):')
    Hy_x = conditional_entropy(list(Y.values()), list(conditional_X_Y.values())[:len(conditional_X_Y) // 2])
    print('Hx(Y):')
    Hx_y = conditional_entropy(list(X.values()), list(conditional_X_Y.values())[len(conditional_X_Y) // 2:])
    dependence: int = int(is_dependent(XY, X_and_Y))
    return dependence, X, Y, X_and_Y, conditional_X_Y, H_x, H_y, H_x_y, Hx_y, Hy_x
