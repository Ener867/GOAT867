import re
from sympy import sympify

def limpiar_expresion(expr_str):
    """
    Convierte expresiones tipo humanas (x², √x, etc.) a formato interpretable por SymPy.
    """
    reemplazos = {
        r'(\b|\W)x²': 'x**2',
        r'(\b|\W)x³': 'x**3',
        r'√x': 'sqrt(x)',
        r'√\((.*?)\)': r'sqrt(\1)',
        r'log\((.*?)\)': r'log(\1)',
        r'sin\((.*?)\)': r'sin(\1)',
        r'cos\((.*?)\)': r'cos(\1)',
    }

    for patron, reemplazo in reemplazos.items():
        expr_str = re.sub(patron, reemplazo, expr_str)

    expr_str = expr_str.replace('^', '**')  # Permitir ^ como sinónimo de **
    return expr_str
