"""Parte 2: postfix -> arbol sintactico."""

import copy

from constantes import CONCAT, EPSILON


class Nodo:
    def __init__(self, valor, tipo, izquierdo=None, derecho=None):
        self.valor = valor
        self.tipo = tipo
        self.izquierdo = izquierdo
        self.derecho = derecho


def construir_arbol(postfix_tokens):
    pila = []
    for token in postfix_tokens:
        if token == "*":
            operando = pila.pop()
            pila.append(Nodo("*", "estrella", izquierdo=operando))
        elif token == "+":
            operando = pila.pop()
            estrella = Nodo("*", "estrella", izquierdo=copy.deepcopy(operando))
            pila.append(Nodo(CONCAT, "concat", izquierdo=operando, derecho=estrella))
        elif token == "?":
            operando = pila.pop()
            epsilon = Nodo(EPSILON, "operando")
            pila.append(Nodo("|", "union", izquierdo=operando, derecho=epsilon))
        elif token == CONCAT:
            derecho = pila.pop(); izquierdo = pila.pop()
            pila.append(Nodo(CONCAT, "concat", izquierdo=izquierdo, derecho=derecho))
        elif token == "|":
            derecho = pila.pop(); izquierdo = pila.pop()
            pila.append(Nodo("|", "union", izquierdo=izquierdo, derecho=derecho))
        else:
            pila.append(Nodo(token, "operando"))

    if len(pila) != 1:
        raise ValueError(f"El postfix no genero un arbol valido (quedaron {len(pila)} subarboles sueltos)")
    return pila[0]
