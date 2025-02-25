import os

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser

def leerArchivo(archivo):
    with open(archivo, 'r') as f:
        return f.read()

def imprimirTokens(tokens):
    for token in tokens:
        print(repr(token))
        
def generarArchivo(tokens, archivo):
    with open(archivo, 'w') as f:
        for token in tokens:
            f.write(repr(token))
    print("Generacion de archivo exitosa")

def estadoLexico(errores, tokens):
    if errores >= 1:
        print(f"Errores encontrados {errores}")
    else:
        print("Compilacion exitosa")
        generarArchivo(tokens, "compiler/test/tokens.txt")
    
def test(archivo):
    codigo = leerArchivo(archivo)
    lexer = Lexer(codigo)
    lexer.analizar()
    #imprimirTokens(lexer.tokens)
    estadoLexico(lexer.error, lexer.tokens)
    parser= Parser(lexer.tokens)
    parser.analizar()

ruta_archivo = os.path.join(os.path.dirname(__file__), 'p1.go')
test(ruta_archivo)