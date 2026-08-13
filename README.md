# Laboratorio 4 — Problema 1 (AFN por Thompson + simulación)

## Ramas del repositorio

| Rama | Contenido |
|---|---|
| `main` | Todo el código y las 4 expresiones. |
| `expresion-1` | Solo `entrada_1.txt` → `(a*\|b*)+` |
| `expresion-2` | Solo `entrada_2.txt` → `((ε\|a)\|b*)*` |
| `expresion-3` | Solo `entrada_3.txt` → `(a\|b)*abb(a\|b)*` |
| `expresion-4` | Solo `entrada_4.txt` → `0?(1?)?0*` |

Cada rama parte de `main` y conserva únicamente el archivo de entrada de su expresión, de modo que cada una resuelve un solo problema.

## Requisitos

Solo `matplotlib` (sin binarios externos):

```bash
pip install matplotlib
```

## Cómo ejecutar

```bash
python3 problema1_afn_thompson.py entrada_problema1.txt afn
```

En las ramas por expresión, se usa el archivo de esa rama, por ejemplo:

```bash
python3 problema1_afn_thompson.py entrada_1.txt afn
```

## Resultados esperados (sí/no)

| Expresión | Cadena | ¿En L(r)? |
|---|---|---|
| `(a*\|b*)+` | `aaabbb`, `ab`, `ba`, `ε` | sí |
| `(a*\|b*)+` | `c` | no |
| `((ε\|a)\|b*)*` | `aab`, `ε` | sí |
| `((ε\|a)\|b*)*` | `c` | no |
| `(a\|b)*abb(a\|b)*` | `abb`, `aabbb`, `aabbabb` | sí |
| `(a\|b)*abb(a\|b)*` | `ba`, `aaa` | no |
| `0?(1?)?0*` | `0100`, `ε`, `0`, `1` | sí |
| `0?(1?)?0*` | `101`, `11` | no |

## Link del video

https://youtu.be/gdbFR-RpYzw 

