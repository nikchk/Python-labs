import sympy as sp
import numpy as np
import matplotlib.pyplot as plot

def draw_parametric_curve(t_values, func_x, func_y):
    t = sp.Symbol('t')
    lambda_x = sp.lambdify(t, func_x, "numpy")
    lambda_y = sp.lambdify(t, func_y, "numpy")

    x_values = np.array([lambda_x(i) for i in t_values], dtype=float)
    y_values = np.array([lambda_y(i) for i in t_values], dtype=float)

    plot.plot(x_values, y_values, color='#3b82f6', label='Початкова крива L')
    return x_values, y_values

def deform_curve(x, y, g_expr, num_points=1000):
 
    # Нормалі
    dx = np.gradient(x)
    dy = np.gradient(y)
    lengths = np.sqrt(dx**2 + dy**2)
    nx = -dy / lengths
    ny = dx / lengths

    s = sp.Symbol('s')
    lambda_g = sp.lambdify(s, g_expr, "numpy")
    s_values = np.linspace(0, 2*np.pi, num_points)
    g_values = lambda_g(s_values)

    x_new = x + g_values * nx
    y_new = y + g_values * ny

    plot.plot(x_new, y_new, color='#ef4444', label='Деформована крива')
    plot.axis('equal')
    plot.legend()
    plot.title("Деформація кривої L за допомогою g(s)")
    plot.show()

    return x_new, y_new

if __name__ == "__main__":
    print("Введіть функції для параметричної кривої L:")
    x_expr = input("x(t) = ") 
    y_expr = input("y(t) = ") 

    print("\nВведіть періодичну функцію g(s):")
    g_expr = input("g(s) = ")
    t, s = sp.symbols('t s')

    func_x = sp.sympify(x_expr)
    func_y = sp.sympify(y_expr)
    func_g = sp.sympify(g_expr)

    t_values = np.linspace(0, 2*np.pi, 1000)
    x, y = draw_parametric_curve(t_values, func_x, func_y)

    deform_curve(x, y, func_g, num_points=len(t_values))

