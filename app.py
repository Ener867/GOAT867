from flask import Flask, request, jsonify
from methods.newton import newton_raphson
from methods.horner import horner
from methods.interpolacion import interpolacion_lineal, interpolacion_cuadratica
from methods.lagrange import lagrange
from methods.minimos_cuadrados import minimos_cuadrados
from methods.interpolacion_menor_error import ajuste_curvas
from utils.identificador import identificar_problema
import ast
import operator

app = Flask(__name__)

# Función para evaluar expresiones matemáticas simples con seguridad
def safe_eval_math_expr(expr):
    """
    Evalúa una expresión matemática simple de forma segura.
    Solo permite números, +, -, *, /, **, (), y espacios.
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError(f"Operador no permitido: {op_type}")
            return allowed_operators[op_type](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # - <operand> e.g., -1
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError(f"Operador unario no permitido: {op_type}")
            return allowed_operators[op_type](_eval(node.operand))
        else:
            raise ValueError(f"Expresión no válida: {expr}")

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

# --- Función auxiliar para parsear puntos ---
def parse_puntos(puntos_str):
    try:
        puntos_str = puntos_str.strip()
        if not puntos_str:
            return []
        puntos = puntos_str.split('),')
        puntos = [p.replace('(', '').replace(')', '').strip() for p in puntos]
        lista = []
        for p in puntos:
            if not p:
                continue
            coords = p.split(',')
            if len(coords) != 2:
                raise ValueError(f"Cada punto debe tener dos coordenadas: {p}")
            x = safe_eval_math_expr(coords[0].strip())
            y = safe_eval_math_expr(coords[1].strip())
            lista.append((x, y))
        return lista
    except Exception as e:
        raise ValueError(f"Error al parsear puntos: {e}")

# --- Función para parsear polinomios tipo "2x^3 + x^2 - 4x + 5" ---
def parse_polynomial(expr):
    expr = expr.replace(" ", "").replace("-", "+-")
    terms = expr.split("+")
    coeffs = {}

    for term in terms:
        if term == "":
            continue
        if 'x^' in term:
            coef, grado = term.split('x^')
            grado = int(grado)
            if coef in ["", "+"]:
                coef = 1.0
            elif coef == "-":
                coef = -1.0
            else:
                coef = safe_eval_math_expr(coef)
        elif 'x' in term:
            coef = term.replace('x', '')
            grado = 1
            if coef in ["", "+"]:
                coef = 1.0
            elif coef == "-":
                coef = -1.0
            else:
                coef = safe_eval_math_expr(coef)
        else:
            coef = safe_eval_math_expr(term)
            grado = 0
        coeffs[grado] = coeffs.get(grado, 0) + coef

    max_grado = max(coeffs.keys()) if coeffs else 0
    lista_final = [coeffs.get(i, 0.0) for i in reversed(range(max_grado + 1))]
    return lista_final

@app.route('/resolver', methods=['POST'])
def resolver():
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se recibieron datos JSON"}), 400

    problema = datos.get("metodo", "")
    metodo = identificar_problema(problema)

    funcion = datos.get("funcion", "")
    x0 = datos.get("x0", None)
    puntos_str = datos.get("puntos", "")

    try:
        if metodo == "newton":
            if x0 is None:
                return jsonify({"error": "x0 es requerido para Newton-Raphson"}), 400
            x0 = safe_eval_math_expr(str(x0))
            resultado, pasos = newton_raphson(funcion, x0)
            return jsonify({"metodo": "Newton-Raphson", "resultado": resultado, "pasos": pasos})

        elif metodo == "horner":
            if x0 is None:
                return jsonify({"error": "x0 es requerido para Horner"}), 400
            x0 = float(x0)
            try:
                resultado, pasos = horner(funcion, x0)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            return jsonify({"metodo": "Horner", "resultado": resultado, "pasos": pasos})

        elif metodo == "interpolacion_lineal":
            puntos = parse_puntos(puntos_str)

            if not funcion or funcion.strip() == "":
                return jsonify({"error": "El punto de interpolación (funcion) no puede estar vacío"}), 400
            print(f"Evaluando punto de interpolación (lineal): '{funcion}'")

            try:
                x_eval = safe_eval_math_expr(funcion)
            except Exception as e:
                return jsonify({"error": f"Error en evaluación del punto de interpolación: {str(e)}"}), 400

            resultado = interpolacion_lineal(puntos, x_eval)
            return jsonify({"metodo": "Interpolación Lineal", "resultado": resultado})

        elif metodo == "interpolacion_cuadratica":
            puntos = parse_puntos(puntos_str)

            if not funcion or funcion.strip() == "":
                return jsonify({"error": "El punto de interpolación (funcion) no puede estar vacío"}), 400
            print(f"Evaluando punto de interpolación (cuadrática): '{funcion}'")

            try:
                x_eval = safe_eval_math_expr(funcion)
            except Exception as e:
                return jsonify({"error": f"Error en evaluación del punto de interpolación: {str(e)}"}), 400

            resultado = interpolacion_cuadratica(puntos, x_eval)
            return jsonify({"metodo": "Interpolación Cuadrática", "resultado": resultado})

        elif metodo == "lagrange":
            puntos = parse_puntos(puntos_str)
            x_val = safe_eval_math_expr(funcion)
            x_vals = [p[0] for p in puntos]
            y_vals = [p[1] for p in puntos]
            resultado, pasos = lagrange(x_vals, y_vals, x_val)
            return jsonify({"metodo": "Lagrange", "resultado": resultado, "pasos": pasos})

        elif metodo == "minimos_cuadrados":
            puntos = parse_puntos(puntos_str)
            m, c = minimos_cuadrados(puntos)
            return jsonify({"metodo": "Mínimos Cuadrados", "pendiente": m, "interseccion": c})

        elif metodo == "interpolacion_menor_error":
            puntos = parse_puntos(puntos_str)
            coeficientes = ajuste_curvas(puntos)
            return jsonify({"metodo": "Ajuste por interpolación de menor error", "coeficientes": coeficientes})

        else:
            return jsonify({"error": "Método no reconocido"}), 400

    except ValueError as e:
        app.logger.error(f"VALUE ERROR: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"ERROR INTERNO: {e}")
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)