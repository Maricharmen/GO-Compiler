from lexer import Lexer

""" Lee el contenido de un archivo y lo retorna como un string """ 
def leerArchivo(archivo):
    with open(archivo, 'r') as f:
        return f.read()

""" Imprime la lista de tokens generados por el analizador léxico """
def imprimirTokens(tokens):
    for token in tokens:
        print(repr(token))
        
""" Guarda la lista de tokens en un archivo de texto """
def generarArchivo(tokens, archivo):
    with open(archivo, 'w') as f:
        for token in tokens:
            f.write(repr(token))
    print("Generacion de archivo exitosa")

""" Muestra el estado de la compilación según la cantidad de errores léxicos """
def estadoCompilacion(errores, tokens):
    if errores >= 1:
        print(f"Errores encontrados {errores}")
    else:
        print("Compilacion exitosa")
        generarArchivo(tokens, "tokens.txt")

""" Función de prueba para el analizador léxico """      
def testLexer(archivo):
    codigo = leerArchivo(archivo)
    lexer = Lexer(codigo)
    lexer.analizar()
    imprimirTokens(lexer.tokens)
    estadoCompilacion(lexer.error, lexer.tokens)
    
if __name__ == "__main__":
    testLexer('programa_1.go')
    
    
    
    
    