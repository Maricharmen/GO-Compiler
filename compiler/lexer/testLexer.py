from lexer import Lexer

""" Lee el contenido de un archivo y lo retorna como un string """ 
def leerArchivo(archivo):
    with open(archivo, 'r') as f:
        return f.read()

""" Imprime la lista de tokens generados por el analizador léxico """
def imprimirTokens(tokens):
    for token in tokens:
        print(f"{token.tipo} : {token.valor}")

""" Guarda la lista de tokens en un archivo de texto """
def generarArchivo(tokens, archivo):
    with open(archivo, 'w') as f:
        for token in tokens:
            f.write(f"{token.tipo} : {token.valor} \n")

""" Muestra el estado de la compilación según la cantidad de errores léxicos """
def estadoCompilacion(errores):
    if errores >= 1:
        print(f"Errores encontrados {errores}")
    else:
        print("Compilacion exitosa")

""" Función de prueba para el analizador léxico """      
def testLexer(archivoGo):
    codigo = leerArchivo(archivoGo)
    lexer = Lexer(codigo)
    lexer.analizar()
    #imprimirTokens(lexer.tokens)
    generarArchivo(lexer.tokens, "tokens.txt")
    estadoCompilacion(lexer.error)
 
if __name__ == "__main__":
    testLexer("programa_1.go")
    
    
    
    
    