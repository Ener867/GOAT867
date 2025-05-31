import numpy as np

def ajuste_curvas(puntos, grado=2):
    x_vals = np.array([p[0] for p in puntos])
    y_vals = np.array([p[1] for p in puntos])
    A = np.vstack([x_vals**i for i in range(grado + 1)]).T
    coeficientes = np.linalg.lstsq(A, y_vals, rcond=None)[0]
    return coeficientes.tolist()