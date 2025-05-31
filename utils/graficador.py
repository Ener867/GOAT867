import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sympify
from utils.preprocesador import limpiar_expresion

def graficar_funcion(expr_str, xmin=-10, xmax=10, puntos=None, nombre_archivo='grafico.png'):
    x = symbols('x')
    expr = sympify(limpiar_expresion(expr_str))
    f = lambdify(x, expr, 'numpy')

    x_vals = np.linspace(xmin, xmax, 400)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label='f(x)', color='blue')

    if puntos:
        px = [p[0] for p in puntos]
        py = [p[1] for p in puntos]
        plt.scatter(px, py, color='red', label='Puntos dados')

    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.legend()
    plt.grid(True)
    plt.title('Gráfico de f(x)')
    plt.savefig(f'static/{nombre_archivo}')
    plt.close()
    return f'static/{nombre_archivo}'