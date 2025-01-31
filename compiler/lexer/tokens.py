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
        return f"Token({self.tipo}: {self.valor})"

''' Definir expresiones regulares para los tokens reconocidos '''
TOKENS = [
    ("[COMMENT]", r"//[^\n]*"), 
    ("[KEYWORD]", r"(package|import|func|var|return|int|string|main)"),
    ("[IDENTIFIER]", r"[a-zA-Z_][a-zA-Z0-9_]*"), 
    ("[NUMBER]", r"\d+(\.\d*)?"), 
    ("[STRING]", r"\"([^\"]|\\\")*\""),   
    ("[DELIMITER]", r"(\(|\)|{|}|[\[\]\,;.])"),
    ("[ARITHMETIC_OP]", r"[+\-*/%]"),  
    ("[ASSIGNMENT_OP]", r":=|="),
    ("[WHITESPACE]", r"\s+")
]



