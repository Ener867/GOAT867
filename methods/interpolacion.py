def interpolacion_lineal(puntos, x_eval):
    if len(puntos) < 2:
        raise ValueError("Se requieren al menos dos puntos para interpolación lineal.")
    
    # Ordenar puntos por x para evitar confusiones
    puntos = sorted(puntos, key=lambda p: p[0])
    
    (x0, y0), (x1, y1) = puntos[:2]
    
    if x1 == x0:
        raise ValueError("Los valores de x de los dos puntos no pueden ser iguales.")
    
    def f(x):
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    
    return f(x_eval)


def interpolacion_cuadratica(puntos, x_eval):
    if len(puntos) < 3:
        raise ValueError("Se requieren al menos tres puntos para interpolación cuadrática.")
    
    # Ordenar puntos por x
    puntos = sorted(puntos, key=lambda p: p[0])
    
    (x0, y0), (x1, y1), (x2, y2) = puntos[:3]
    
    # Validar que no haya x repetidos
    if x0 == x1 or x0 == x2 or x1 == x2:
        raise ValueError("Los valores de x deben ser distintos entre los puntos.")
    
    def f(x):
        term0 = y0 * (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2))
        term1 = y1 * (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2))
        term2 = y2 * (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))
        return term0 + term1 + term2
    
    return f(x_eval)