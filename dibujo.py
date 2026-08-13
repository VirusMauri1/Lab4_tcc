"""Parte 5: dibujo del AFN con matplotlib."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

from constantes import EPSILON
from automata_thompson import estados_alcanzables


def dibujar_afn(fragmento, nombre_archivo: str):
    orden, niveles = estados_alcanzables(fragmento.inicio)
    contador_por_nivel = {}
    posiciones = {}
    for estado in orden:
        nivel = niveles[estado.id]
        y = contador_por_nivel.get(nivel, 0)
        contador_por_nivel[nivel] = y + 1
        posiciones[estado.id] = (nivel, y)

    # centrar verticalmente cada nivel
    max_altura = max(contador_por_nivel.values())
    for estado in orden:
        nivel = niveles[estado.id]
        x, y = posiciones[estado.id]
        offset = (max_altura - contador_por_nivel[nivel]) / 2
        posiciones[estado.id] = (x * 2.2, y + offset)

    fig, ax = plt.subplots(figsize=(max(6, (max(niveles.values()) + 1) * 2.0),
                                     max(4, max_altura * 1.4)))

    radio = 0.28
    combinadas = {}
    for estado in orden:
        for simbolo, destino in estado.transiciones:
            etiqueta = EPSILON if simbolo is None else simbolo
            combinadas.setdefault((estado.id, destino.id), []).append(etiqueta)

    dibujados = set()
    for (origen_id, destino_id), etiquetas in combinadas.items():
        if (origen_id, destino_id) in dibujados:
            continue
        dibujados.add((origen_id, destino_id))
        x1, y1 = posiciones[origen_id]
        x2, y2 = posiciones[destino_id]
        etiqueta_texto = ", ".join(sorted(set(etiquetas)))

        if origen_id == destino_id:
            # auto-transicion (loop): se dibuja como un lazo arriba del estado
            lazo = Circle((x1, y1 + radio + 0.28), radio * 0.6, fill=False, zorder=1)
            ax.add_patch(lazo)
            ax.text(x1, y1 + radio + 0.28 + radio * 0.9, etiqueta_texto,
                    ha="center", va="bottom", fontsize=9)
            continue

        curvatura = 0.15 if y1 <= y2 else -0.15
        flecha = FancyArrowPatch((x1, y1), (x2, y2),
                                    connectionstyle=f"arc3,rad={curvatura}",
                                    arrowstyle="-|>", mutation_scale=14,
                                    color="black", linewidth=1.0, zorder=1,
                                  shrinkA=radio * 72, shrinkB=radio * 72)
        ax.add_patch(flecha)
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2 + curvatura * 0.6
        ax.text(xm, ym, etiqueta_texto, ha="center", va="center", fontsize=9,
                    backgroundcolor="white")

    for estado in orden:
        x, y = posiciones[estado.id]
        es_aceptacion = (estado is fragmento.fin)
        es_inicial = (estado is fragmento.inicio)

        circulo = Circle((x, y), radio, fill=True, facecolor="#cfe8ff",
                            edgecolor="black", zorder=2)
        ax.add_patch(circulo)
        if es_aceptacion:
            circulo_externo = Circle((x, y), radio * 1.28, fill=False,
                                    edgecolor="black", zorder=2)
            ax.add_patch(circulo_externo)
        ax.text(x, y, estado.id, ha="center", va="center", fontsize=8, zorder=3)

        if es_inicial:
            ax.annotate("", xy=(x - radio, y), xytext=(x - radio - 0.5, y),
                        arrowprops=dict(arrowstyle="-|>", color="black"))
            ax.text(x - radio - 0.55, y, "inicio", ha="right", va="center", fontsize=9)

    todos_x = [p[0] for p in posiciones.values()]
    todos_y = [p[1] for p in posiciones.values()]
    ax.set_xlim(min(todos_x) - 1.2, max(todos_x) + 1.0)
    ax.set_ylim(min(todos_y) - 1.0, max(todos_y) + 1.0)
    ax.set_aspect("equal")
    ax.axis("off")

    ruta_salida = f"{nombre_archivo}.png"
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close(fig)
    return ruta_salida
