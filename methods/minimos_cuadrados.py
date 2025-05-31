import numpy as np

def minimos_cuadrados(puntos):
    x_vals = np.array([p[0] for p in puntos])
    y_vals = np.array([p[1] for p in puntos])
    A = np.vstack([x_vals, np.ones(len(x_vals))]).T
    m, c = np.linalg.lstsq(A, y_vals, rcond=None)[0]
    return m, c