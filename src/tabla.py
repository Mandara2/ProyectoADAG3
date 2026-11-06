"""Presenta en la terminal la tabla DP y la reconstrucción de un caso resuelto."""

# Con más columnas la tabla no cabe en una terminal normal.
MAX_COLUMNAS = 31


def _celda(valor, marcada, ancho):
    texto = f"[{valor}]" if marcada else f" {valor} "
    return texto.rjust(ancho)


def formatear(etapas, resultado):
    """Devuelve las líneas de texto con la tabla DP y la reconstrucción."""
    traza = resultado["traza"]
    pasos = traza["reconstruccion"]
    presupuesto = resultado["presupuesto"]
    lineas = []

    tabla = traza.get("tabla")
    if tabla is None:
        lineas.append(f"Tabla DP: {traza['casillas_tabla']} casillas, demasiado grande para mostrarla.")
    elif presupuesto + 1 > MAX_COLUMNAS:
        lineas.append(f"Tabla DP: {presupuesto + 1} columnas, demasiado ancha para la terminal.")
    else:
        # Casillas por las que pasa la reconstrucción: (i, b) de cada paso y la fila 0 final.
        camino = {(paso["etapa"], paso["b"]) for paso in pasos}
        b_final = pasos[-1]["presupuesto_restante"] if pasos else presupuesto
        camino.add((0, b_final))

        ancho = max(len(str(max(max(fila) for fila in tabla))), len(str(presupuesto))) + 2
        etiquetas = ["0 ninguna"] + [f"{i} (c={e['c']}, d={e['d']})" for i, e in enumerate(etapas, start=1)]
        ancho_etiqueta = max(len(e) for e in etiquetas + ["Etapas \\ b"])

        lineas.append("Tabla DP: DP[i][b] = mayor reducción con las primeras i etapas y presupuesto b.")
        lineas.append("Entre [ ] van las casillas por las que pasa la reconstrucción.")
        lineas.append("")
        encabezado = "Etapas \\ b".ljust(ancho_etiqueta) + " |" + "".join(str(b).rjust(ancho - 1) + " " for b in range(presupuesto + 1))
        lineas.append(encabezado)
        lineas.append("-" * len(encabezado))
        for i, fila in enumerate(tabla):
            celdas = "".join(_celda(valor, (i, b) in camino, ancho) for b, valor in enumerate(fila))
            lineas.append(etiquetas[i].ljust(ancho_etiqueta) + " |" + celdas)

    lineas.append("")
    lineas.append("Reconstrucción (de la última etapa a la primera):")
    lineas.append(f"  {'Etapa':>5}  {'b':>5}  {'DP[i][b]':>9}  {'DP[i-1][b]':>10}  {'Decisión':<12} {'Queda':>5}")
    for paso in pasos:
        lineas.append(
            f"  {paso['etapa']:>5}  {paso['b']:>5}  {paso['DP[i][b]']:>9}  {paso['DP[i-1][b]']:>10}  "
            f"{paso['decision']:<12} {paso['presupuesto_restante']:>5}"
        )

    aceleradas = resultado["etapas_aceleradas"]
    lineas.append("")
    lineas.append(
        f"Resultado: acelerar {aceleradas if aceleradas else 'ninguna etapa'}; "
        f"costo {resultado['costo_usado']} de {presupuesto}; "
        f"duración {resultado['duracion_original']} -> {resultado['duracion_final']} "
        f"(se ahorran {resultado['reduccion']})."
    )
    return lineas
