import re
from tokens import Token, TOKENS

class Lexer:
    
    """ 
    Analizador léxico para un lenguaje similar a Go.

    Atributos:
        codigo (list): Lista de líneas del código fuente.
        linea (int): Contador de la línea actual en el código.
        posicion (int): Posición del carácter actual dentro de la línea.
        error (int): Contador de errores léxicos detectados.
        tokens (list): Lista de tokens identificados en el código.
    """
    
    def __init__(self, codigo):
        """ 
        Constructor del analizador léxico.

        Args:
            codigo (str): Código fuente en formato de string.
        """
        self.codigo = codigo.splitlines()
        self.linea = 0
        self.posicion = 0
        self.error = 0
        self.tokens = []
    
    
    def tokenizar(self):
        """ 
        Procesa la línea actual y extrae los tokens.

        Retorna:
            None si no hay más líneas por analizar.
        """
        if self.linea >= len(self.codigo):
            return None
        
        lineaActual = self.codigo[self.linea]
        self.posicion = 0
    
        while self.posicion < len(lineaActual):
            token = self.procesarToken(lineaActual)
            
            if token:
                if token.tipo not in ['[WHITESPACE]', '[COMMENT]']:
                    self.tokens.append(token)
            else: 
                raise ValueError(f"Error lexico en la linea {self.linea + 1}:{lineaActual}")
    
    def procesarToken(self, lineaActual):
        """ 
        Intenta extraer un token desde la posición actual de la línea.

        Args:
            lineaActual (str): Línea de código actual.

        Retorna:
            Token: Un objeto Token si se encuentra una coincidencia.
            None: Si no se encuentra un token válido.
        """
        for tipo, patron in TOKENS:
            regex = re.compile(patron)
            coincidencia = regex.match(lineaActual, self.posicion)

            if coincidencia:
                valor = coincidencia.group(0)
                token = Token(tipo, valor)
                self.posicion += len(valor)
                return token
    
        return None
    
    def analizar(self):
        """ 
        Recorre todas las líneas del código fuente y extrae los tokens.

        Maneja errores léxicos y cuenta el número de errores detectados.
        """
        while self.linea < len(self.codigo):
            try:
                self.tokenizar()
            except ValueError as e:
                print(e)  
                self.error += 1
            
            self.linea += 1
        
        
          