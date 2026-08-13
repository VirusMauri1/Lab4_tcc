"""Parte 1: tokenizador y shunting-yard (expresion en infix -> postfix)."""

from constantes import CONCAT

PRECEDENCIA = {"*": 3, "+": 3, "?": 3, CONCAT: 2, "|": 1}
UNARIOS = {"*", "+", "?"}


def tokenizar(expresion: str):
    tokens = []
    i = 0
    n = len(expresion)
    while i < n:
        c = expresion[i]
        if c == " ":
            i += 1
            continue
        if c == "\\" and i + 1 < n:
            tokens.append(("LITERAL", expresion[i:i + 2]))
            i += 2
        elif c == "[":
            cierre = expresion.find("]", i + 1)
            if cierre == -1:
                raise ValueError(f"Clase de caracteres sin cerrar en: {expresion}")
            tokens.append(("LITERAL", expresion[i:cierre + 1]))
            i = cierre + 1
        elif c == "(":
            tokens.append(("LPAREN", c)); i += 1
        elif c == ")":
            tokens.append(("RPAREN", c)); i += 1
        elif c == "|":
            tokens.append(("UNION", c)); i += 1
        elif c in UNARIOS:
            tokens.append(("UNARIO", c)); i += 1
        else:
            tokens.append(("LITERAL", c)); i += 1
    return tokens


def insertar_concatenacion(tokens):
    resultado = []
    for indice, token in enumerate(tokens):
        resultado.append(token)
        if indice + 1 < len(tokens):
            tipo_actual = token[0]
            tipo_siguiente = tokens[indice + 1][0]
            termina_operando = tipo_actual in ("LITERAL", "RPAREN", "UNARIO")
            inicia_operando = tipo_siguiente in ("LITERAL", "LPAREN")
            if termina_operando and inicia_operando:
                resultado.append(("CONCAT", CONCAT))
    return resultado


def shunting_yard(tokens):
    salida = []
    pila_operadores = []
    for tipo, valor in tokens:
        if tipo == "LITERAL":
            salida.append(valor)
        elif tipo == "LPAREN":
            pila_operadores.append((tipo, valor))
        elif tipo == "RPAREN":
            while pila_operadores and pila_operadores[-1][0] != "LPAREN":
                salida.append(pila_operadores.pop()[1])
            if not pila_operadores:
                raise ValueError("Parentesis desbalanceados en la expresion")
            pila_operadores.pop()
        elif tipo == "UNARIO":
            salida.append(valor)
        elif tipo in ("UNION", "CONCAT"):
            while (pila_operadores
                    and pila_operadores[-1][0] in ("UNION", "CONCAT", "UNARIO")
                    and PRECEDENCIA[pila_operadores[-1][1]] >= PRECEDENCIA[valor]):
                salida.append(pila_operadores.pop()[1])
            pila_operadores.append((tipo, valor))
    while pila_operadores:
        op = pila_operadores.pop()
        if op[0] == "LPAREN":
            raise ValueError("Parentesis desbalanceados en la expresion")
        salida.append(op[1])
    return salida


def infix_a_postfix(expresion: str):
    tokens = tokenizar(expresion)
    tokens_con_concat = insertar_concatenacion(tokens)
    return shunting_yard(tokens_con_concat)
