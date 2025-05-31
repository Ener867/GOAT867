import os
from flask import Flask, render_template, request, jsonify
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

frontend = Flask(__name__,
                 template_folder=os.path.join(BASE_DIR, "templates"),
                 static_folder=os.path.join(BASE_DIR, "static"))

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/resolver', methods=['POST'])
def resolver():
    datos = request.get_json()

    # Limpiar exponentes problemáticos antes de enviar al backend
    if "funcion" in datos and isinstance(datos["funcion"], str):
        datos["funcion"] = datos["funcion"].replace('²', '**2').replace('³', '**3').replace('^', '**')

    try:
        respuesta = requests.post("http://127.0.0.1:5000/resolver", json=datos)
        return jsonify(respuesta.json())
    except Exception as e:
        return jsonify({"error": f"Error al conectar con el backend: {e}"}), 500

if __name__ == '__main__':
    frontend.run(port=5001, debug=True)