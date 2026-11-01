"""Aceleración óptima de la cadena bajo presupuesto (Algoritmo 4.2.1).

DP[i][b] = máxima reducción de tiempo usando las primeras i etapas y gastando
como máximo b.
"""

# La tabla completa solo se copia a la traza si tiene menos casillas que esto.
MAX_CASILLAS_TRAZA = 500


def llenar_tabla(etapas, presupuesto):
    """Llena la tabla DP de (n+1) x (B+1) casillas. Costo: O(n*B)."""
    n = len(etapas)
    dp = [[0] * (presupuesto + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        c = etapas[i - 1]["c"]
        d = etapas[i - 1]["d"]
        for b in range(presupuesto + 1):
            dp[i][b] = dp[i - 1][b]
            if c <= b and dp[i - 1][b - c] + d > dp[i][b]:
                dp[i][b] = dp[i - 1][b - c] + d

    return dp


def reconstruir(dp, etapas, presupuesto):
    """Recorre la tabla hacia atrás. Costo: O(n).

    Devuelve las etapas aceleradas (numeradas desde 1) y un paso de traza por
    etapa.
    """
    aceleradas = []
    pasos = []
    b = presupuesto

    for i in range(len(etapas), 0, -1):
        con_i = dp[i][b]
        sin_i = dp[i - 1][b]
        acelerar = con_i != sin_i
        paso = {
            "etapa": i,
            "b": b,
            "DP[i][b]": con_i,
            "DP[i-1][b]": sin_i,
            "decision": "acelerar" if acelerar else "no acelerar",
        }
        if acelerar:
            aceleradas.append(i)
            b -= etapas[i - 1]["c"]
        paso["presupuesto_restante"] = b
        pasos.append(paso)

    aceleradas.reverse()
    return aceleradas, pasos


def resolver(etapas, presupuesto):
    """Resuelve el caso y devuelve el resultado con su traza."""
    dp = llenar_tabla(etapas, presupuesto)
    aceleradas, pasos = reconstruir(dp, etapas, presupuesto)

    duracion_original = sum(etapa["t"] for etapa in etapas)
    reduccion = dp[len(etapas)][presupuesto]
    costo_usado = sum(etapas[i - 1]["c"] for i in aceleradas)

    casillas = (len(etapas) + 1) * (presupuesto + 1)
    traza = {"casillas_tabla": casillas, "reconstruccion": pasos}
    if casillas < MAX_CASILLAS_TRAZA:
        traza["tabla"] = dp

    return {
        "etapas_aceleradas": aceleradas,
        "costo_usado": costo_usado,
        "presupuesto": presupuesto,
        "reduccion": reduccion,
        "duracion_original": duracion_original,
        "duracion_final": duracion_original - reduccion,
        "traza": traza,
    }
