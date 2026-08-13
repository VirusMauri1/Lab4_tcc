"""Parte 4: simulacion del AFN sobre una cadena, via cerradura-epsilon."""


def cerradura_epsilon(estados):
    resultado = set(estados)
    pila = list(estados)
    while pila:
        actual = pila.pop()
        for simbolo, destino in actual.transiciones:
            if simbolo is None and destino not in resultado:
                resultado.add(destino)
                pila.append(destino)
    return resultado


def mover(estados, simbolo):
    resultado = set()
    for estado in estados:
        for s, destino in estado.transiciones:
            if s == simbolo:
                resultado.add(destino)
    return resultado


def simular_afn(fragmento, cadena: str):
    pasos = []
    actuales = cerradura_epsilon({fragmento.inicio})
    pasos.append(f"  cerradura-e del estado inicial: {{{', '.join(sorted(e.id for e in actuales))}}}")

    for caracter in cadena:
        siguientes = cerradura_epsilon(mover(actuales, caracter))
        etiqueta_conjunto = "{" + ", ".join(sorted(e.id for e in siguientes)) + "}" if siguientes else "{} (vacio)"
        pasos.append(f"  leer '{caracter}' -> {etiqueta_conjunto}")
        actuales = siguientes
        if not actuales:
            break

    acepta = fragmento.fin in actuales
    return acepta, pasos
