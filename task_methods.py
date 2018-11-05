import numpy as np
from math import e


def get_default():
    return {
        "x0": 0,
        "y0": 1,
        "x": 1,
        "grid": 20
    }


def func(x, y):
    # return x*x - 2*y
    return x*(y**1.5) + x*y


def exact_func(x, C):
    # return 0.75*e**(-2*x)+0.5*x**2-0.5*x+1/4
    return 4*e**(x*x/2)/((C + 2*e**(x*x/4))**2)


def exact(x0, y0, x, grid):
    c = (-2*e**(x0**2/4)/y0**0.5) - (2*e**(x0**2/4))
    # print("C: ", c)
    step = (x-x0)/grid
    x_range = np.array([x0+i*step for i in range(grid+1)], float)
    y_range = exact_func(x_range, c)
    not_overflow = True
    return x_range, y_range, not not_overflow


def euler(x0, y0, x, grid):
    c = (-2*e**(x0**2/4)/y0**0.5) - (2*e**(x0**2/4))
    step = (x-x0)/grid
    x_range = [x0+i*step for i in range(grid+1)]
    y_range = [y0]
    i = 1
    current_y = y0
    not_overflow = True
    while i <= grid:
        try:
            current_y = current_y + step*func(x_range[i-1], current_y)
            y_range.append(current_y)
        except OverflowError:
            not_overflow = False
            current_y = exact_func(x_range[i], c)
            y_range.append(current_y)
        i += 1
    y_array = np.array(y_range, float)
    x_array = np.array(x_range[:len(y_array)], float)
    return x_array, y_array, not not_overflow


def imp_euler(x0, y0, x, grid):
    return euler(x0, y0, x, grid)


def r_k(x0, y0, x, grid):
    return euler(x0, y0, x, grid)