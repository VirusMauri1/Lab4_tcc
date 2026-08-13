"""Parte 3: arbol sintactico -> AFN (construccion de Thompson)."""

from constantes import EPSILON


class Estado:
    _contador = 0

    def __init__(self):
        Estado._contador += 1
        self.id = f"q{Estado._contador}"
        self.transiciones = []

    def agregar_transicion(self, simbolo, destino):
        self.transiciones.append((simbolo, destino))


class Fragmento:
    def __init__(self, inicio: Estado, fin: Estado):
        self.inicio = inicio
        self.fin = fin


def _simbolo_de_literal(valor: str):
    if valor == EPSILON:
        return [None]

    if valor.startswith("\\") and len(valor) == 2:
        escapes_especiales = {"n": "\n", "t": "\t"}
        return [escapes_especiales.get(valor[1], valor[1])]

    if valor.startswith("[") and valor.endswith("]"):
        contenido = valor[1:-1]
        caracteres = []
        i = 0
        while i < len(contenido):
            # soporta rangos tipo a-z dentro de la clase
            if i + 2 < len(contenido) and contenido[i + 1] == "-":
                for codigo in range(ord(contenido[i]), ord(contenido[i + 2]) + 1):
                    caracteres.append(chr(codigo))
                i += 3
            else:
                caracteres.append(contenido[i])
                i += 1
        return caracteres

    return [valor]


def _fragmento_hoja(valor: str):
    inicio = Estado()
    fin = Estado()
    for simbolo in _simbolo_de_literal(valor):
        inicio.agregar_transicion(simbolo, fin)
    return Fragmento(inicio, fin)


def _concatenar(f1: Fragmento, f2: Fragmento):
    f1.fin.agregar_transicion(None, f2.inicio)
    return Fragmento(f1.inicio, f2.fin)


def _unir(f1: Fragmento, f2: Fragmento):
    inicio = Estado()
    fin = Estado()
    inicio.agregar_transicion(None, f1.inicio)
    inicio.agregar_transicion(None, f2.inicio)
    f1.fin.agregar_transicion(None, fin)
    f2.fin.agregar_transicion(None, fin)
    return Fragmento(inicio, fin)


def _estrella(f: Fragmento):
    inicio = Estado()
    fin = Estado()
    inicio.agregar_transicion(None, f.inicio)
    inicio.agregar_transicion(None, fin)
    f.fin.agregar_transicion(None, f.inicio)
    f.fin.agregar_transicion(None, fin)
    return Fragmento(inicio, fin)


def arbol_a_afn(nodo) -> Fragmento:
    if nodo.tipo == "operando":
        return _fragmento_hoja(nodo.valor)
    elif nodo.tipo == "estrella":
        return _estrella(arbol_a_afn(nodo.izquierdo))
    elif nodo.tipo == "concat":
        return _concatenar(arbol_a_afn(nodo.izquierdo), arbol_a_afn(nodo.derecho))
    elif nodo.tipo == "union":
        return _unir(arbol_a_afn(nodo.izquierdo), arbol_a_afn(nodo.derecho))
    else:
        raise ValueError(f"Tipo de nodo desconocido: {nodo.tipo}")


def estados_alcanzables(inicio: Estado):
    niveles = {inicio.id: 0}
    orden = [inicio]
    cola = [inicio]
    while cola:
        actual = cola.pop(0)
        for _, destino in actual.transiciones:
            if destino.id not in niveles:
                niveles[destino.id] = niveles[actual.id] + 1
                orden.append(destino)
                cola.append(destino)
    return orden, niveles
