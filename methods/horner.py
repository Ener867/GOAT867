import re
from sympy import Symbol, sympify, Poly

def parse_polynomial(expr_str):
    """
    Convierte una cadena como '2x² + x³ - 4x + 5' en coeficientes numéricos.
    """
    x = Symbol('x')
    try:
        expr_str = expr_str.replace('^', '**').replace('²', '**2').replace('³', '**3')

        # Insertar '*' entre número y variable si falta (ej: 2x → 2*x)
        expr_str = re.sub(r'(\d)(x)', r'\1*\2', expr_str)
        expr_str = re.sub(r'(x)(\d)', r'\1**\2', expr_str)  # por si acaso hay x2 en lugar de x^2

        expr = sympify(expr_str)
        if not expr.has(x):
            raise ValueError("La expresión no contiene la variable 'x', no es un polinomio válido.")
        poly = Poly(expr, x)
        coeffs = poly.all_coeffs()
        return [float(c.evalf()) for c in coeffs]
    except Exception as e:
        raise ValueError(f"No se pudo interpretar el polinomio: {e}")

def horner(expr_str, x_val):
    try:
        coeffs = parse_polynomial(expr_str)
    except ValueError as e:
        return None, [str(e)]

    pasos = []
    result = coeffs[0]
    pasos.append(f"Iniciamos con el coeficiente principal: {result}")

    for i, coef in enumerate(coeffs[1:], start=1):
        paso = result * x_val + coef
        pasos.append(f"Paso {i}: ({result} * {x_val}) + {coef} = {paso}")
        result = paso

    pasos.append(f"\nResultado final: P({x_val}) = {result}")
    return round(result, 6), pasos