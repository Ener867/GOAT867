def lagrange(x_vals, y_vals, x_eval):
    if len(x_vals) != len(y_vals):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")
    if len(x_vals) < 2:
        raise ValueError("Se requieren al menos dos puntos para interpolar.")

    n = len(x_vals)
    resultado = 0.0
    pasos = []
    pasos.append("Interpolación de Lagrange\n")
    
    # Construcción simbólica del polinomio
    polinomio_partes = []

    for i in range(n):
        li_valor = 1.0
        li_simb = []
        pasos.append(f"--- Término L_{i}(x) ---")

        for j in range(n):
            if i != j:
                num = f"(x - {x_vals[j]})"
                den = f"({x_vals[i]} - {x_vals[j]})"
                li_simb.append(f"{num}/{den}")
                li_valor *= (x_eval - x_vals[j]) / (x_vals[i] - x_vals[j])

        simbolico = " * ".join(li_simb)
        termino_str = f"{y_vals[i]} * ({simbolico})"
        polinomio_partes.append(termino_str)

        pasos.append(f"L_{i}(x) = {simbolico}")
        pasos.append(f"L_{i}({x_eval}) = {li_valor:.6f}")
        pasos.append(f"{y_vals[i]} * {li_valor:.6f} = {y_vals[i] * li_valor:.6f}\n")

        resultado += y_vals[i] * li_valor

    polinomio = "P(x) = " + " + ".join(polinomio_partes)
    pasos.insert(1, polinomio + "\n")
    pasos.append(f"Resultado final: P({x_eval}) = {resultado:.6f}")

    return round(resultado, 6), pasos