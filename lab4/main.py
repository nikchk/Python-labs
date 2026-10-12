import numpy as np
import sympy as sp
import matplotlib.pyplot as plot
import random


def monte_carlo_area(func_f, func_g, a, b, num_points, plot_result=True):
    x = sp.Symbol('x')
    f = sp.lambdify(x, func_f, "numpy")
    g = sp.lambdify(x, func_g, "numpy")

    x_values = np.linspace(a, b, 1000)
    f_values = np.array(f(x_values), dtype=float).flatten()
    g_values = np.array(g(x_values), dtype=float).flatten()

    y_min = min(np.min(f_values), np.min(g_values))
    y_max = max(np.max(f_values), np.max(g_values))

    count_inside = 0
    x_random = []
    y_random = []
    inside_x = []
    inside_y = []
    outside_x = []
    outside_y = []
    for _ in range(num_points):
        x_rand = random.uniform(a, b)
        y_rand = random.uniform(y_min, y_max)
        x_random.append(x_rand)
        y_random.append(y_rand)

        if (y_rand <= f(x_rand) and y_rand >= g(x_rand)) or (y_rand >= f(x_rand) and y_rand <= g(x_rand)):
            count_inside += 1
            inside_x.append(x_rand)
            inside_y.append(y_rand)
        else:
            outside_x.append(x_rand)
            outside_y.append(y_rand)

    area_rectangle = (b - a) * (y_max - y_min)
    area_figure = (count_inside / num_points) * area_rectangle

    print(f'Estimated area between f(x) and g(x) from {a} to {b}: {area_figure}')

    if plot_result:
        plot.figure(figsize=(10, 6))
        plot.plot(x_values, f_values, label='f(x)', color='blue')
        plot.plot(x_values, g_values, label='g(x)', color='orange')
        plot.axvline(x=a, color='red', linestyle='--', label='x=a')
        plot.axvline(x=b, color='green', linestyle='--', label='x=b')
        plot.axhline(y=y_min, color='grey', linestyle='--')
        plot.axhline(y=y_max, color='grey', linestyle='--')
        plot.scatter(inside_x, inside_y, color='green', s=1, label='Inside')
        plot.scatter(outside_x, outside_y, color='gray', s=1, label='Outside')
        plot.fill_betweenx([y_min, y_max], a, b, color='lightgrey', alpha=0.5)
        plot.title('Monte Carlo Area Estimation')
        plot.xlabel('x')
        plot.ylabel('y')
        plot.legend()
        plot.grid()
        plot.show()
    return area_figure


def __main__():
    print('Input functions f(x) and g(x):')
    func_f = sp.sympify(input('f(x) = '))
    func_g = sp.sympify(input('g(x) = '))

    a, b = map(float, input('Input [a, b]: ').split())
    num_points = int(input('Input number of random points: '))

    monte_carlo_area(func_f, func_g, a, b, num_points)

if __name__ == '__main__':
    __main__()

   
