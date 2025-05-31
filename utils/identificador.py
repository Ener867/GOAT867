def identificar_problema(texto):
    texto = texto.lower()
    if "newton" in texto:
        return "newton"
    elif "horner" in texto:
        return "horner"
    elif "lagrange" in texto:
        return "lagrange"
    elif "cuadrática" in texto or "cuadratica" in texto:
        return "interpolacion_cuadratica"
    elif "lineal" in texto:
        return "interpolacion_lineal"
    elif "mínimos cuadrados" in texto or "minimos cuadrados" in texto:
        return "minimos_cuadrados"
    elif "menor error" in texto or "ajuste" in texto:
        return "interpolacion_menor_error"
    else:
        return "desconocido"