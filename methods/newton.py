from sympy import symbols, diff, lambdify, sympify
from utils.preprocesador import limpiar_expresion

def newton_raphson(expr_str, x0, tol=1e-5, max_iter=100):
    x = symbols('x')
    expr = sympify(limpiar_expresion(expr_str))
    f = lambdify(x, expr, 'numpy')
    df = lambdify(x, diff(expr, x), 'numpy')

    pasos = []
    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)
        if dfx == 0:
            break
        x1 = x0 - fx / dfx
        pasos.append({
            "iteración": i + 1,
            "x0": round(float(x0), 6),
            "f(x)": round(float(fx), 6),
            "f'(x)": round(float(dfx), 6),
            "x1": round(float(x1), 6)
        })
        if abs(x1 - x0) < tol:
            break
        x0 = x1
    return round(float(x1), 6), pasos