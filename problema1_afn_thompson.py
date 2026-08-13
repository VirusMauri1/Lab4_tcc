"""Punto de entrada: regex -> postfix -> arbol -> AFN de Thompson -> dibujo -> simulacion."""

import os
import sys

from shunting_yard import infix_a_postfix
from arbol_sintactico import construir_arbol
from automata_thompson import Estado, arbol_a_afn, estados_alcanzables
from simulacion import simular_afn
from dibujo import dibujar_afn


def procesar_linea(expresion: str, cadenas: list, indice: int, carpeta_salida: str):
    print("=" * 70)
    print(f"Expresion {indice} (infix): {expresion}")
    print("-" * 70)

    postfix = infix_a_postfix(expresion)
    print(f"Postfix: {''.join(postfix)}")

    raiz = construir_arbol(postfix)

    Estado._contador = 0  # reiniciar numeracion de estados por expresion
    fragmento = arbol_a_afn(raiz)
    orden, _ = estados_alcanzables(fragmento.inicio)
    print(f"AFN generado: {len(orden)} estados | inicial: {fragmento.inicio.id} | aceptacion: {fragmento.fin.id}")

    nombre_archivo = f"{carpeta_salida}/afn_{indice}"
    ruta = dibujar_afn(fragmento, nombre_archivo)
    print(f"Imagen del AFN guardada en: {ruta}")

    if not cadenas:
        print("(no se especificaron cadenas de prueba para esta expresion)\n")
        return

    for cadena in cadenas:
        etiqueta_cadena = cadena if cadena != "" else "ε (cadena vacia)"
        print(f"\nSimulando w = {etiqueta_cadena}")
        acepta, pasos = simular_afn(fragmento, cadena)
        for paso in pasos:
            print(paso)
        print(f"  => w {'SI' if acepta else 'NO'} pertenece a L(r)  ({'si' if acepta else 'no'})")
    print()


def procesar_archivo(ruta_archivo: str, carpeta_salida: str = "."):
    os.makedirs(carpeta_salida, exist_ok=True)

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = [linea.rstrip("\n") for linea in archivo if linea.strip() != ""]

    for indice, linea in enumerate(lineas, start=1):
        try:
            if ";" in linea:
                expresion, resto = linea.split(";", 1)
                cadenas = resto.split(",") if resto != "" else []
            else:
                expresion, cadenas = linea, []
            procesar_linea(expresion.strip(), cadenas, indice, carpeta_salida)
        except ValueError as error:
            print(f"  ERROR procesando linea {indice} ('{linea}'): {error}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 problema1_afn_thompson.py <archivo_entrada.txt> [carpeta_salida]")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    carpeta = sys.argv[2] if len(sys.argv) > 2 else "."
    procesar_archivo(archivo_entrada, carpeta)
