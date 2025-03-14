import re

''' Definir la clase Token que representa un token léxico '''
class Token:
    """ 
        Constructor de un Token.

        Args:
            tipo (str): Tipo de token (ej. palabra clave, identificador, número).
            valor (str): Valor del token extraído del código fuente.
    """
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        """ 
        Representación en string del token.

        Retorna:
            str: Representación en formato 'Token(TIPO: VALOR)'.
        """
        return f"Token({self.tipo}: {self.valor}) \n"

''' Definir expresiones regulares para los tokens reconocidos '''
TOKENS = [
    ("[FLOAT]", r"\d+\.\d+"),  # Números flotantes (ej. 3.14)
    ("[INTEGER]", r"\d+"),  # Números enteros (ej. 42)
    ("[COMMENT]", r"//[^\n]*"),  # Comentarios (ej. // esto es un comentario)
    ("[KEYWORD]", r"(package|import|func|var|return|int|string|for|if|else)"),  # Palabras clave
    ("[IDENTIFIER]", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Identificadores (ej. i, j, main)
    ("[STRING]", r"\"([^\"]|\\\")*\""),  # Cadenas de texto (ej. "Hola, mundo")
    ("[DELIMITER]", r"(\(|\)|{|}|[\[\]\,;.])"),  # Delimitadores (ej. (, ), {, }, [, ], ,, ;, .)
    ("[OPERATOR]", r"\+\+|--|:=|=|<=|>=|==|!=|[+\-*/%]|&&|\|\|"),  # Operadores (ej. :=, =, +, -, *, /)
    ("[WHITESPACE]", r"\s+"),  # Espacios en blanco (ignorados)
]



