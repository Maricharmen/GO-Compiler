import os

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser  
#from compiler.parser.bottom_up_parser import Parser

def imprimirTokens(tokens):
    for token in tokens:
        print(repr(token))
        
def generarArchivo(tokens, archivo):
    with open(archivo, 'w') as f:
        for token in tokens:
            f.write(repr(token))
    print("Generacion de archivo de tokens completado con exito")

def estadoLexico(errores, tokens):
    if errores >= 1:
        print(f"Errores encontrados {errores}")
    else:
        print("Analisis lexico completado con exito")
        generarArchivo(tokens, "compiler/test/tokens.txt")
    
def test(codigo):
    # Analisis lexico
    lexer = Lexer(codigo)
    lexer.analizar()
    #imprimirTokens(lexer.tokens)
    estadoLexico(lexer.error, lexer.tokens)
    
    # Analisis sintactico
    parser= Parser(lexer.tokens)
    parser.analizar()

ruta_archivo = os.path.join(os.path.dirname(__file__), 'p6.go')
with open(ruta_archivo, 'r') as f:
        test(f.read())
        
        