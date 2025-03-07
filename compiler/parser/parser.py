class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0  # Índice para recorrer la lista de tokens
        self.error = 0

    def analizar(self):
        try:
            # Comienza analizando la estructura de 'package main'
            self.analizar_paquete()

            # Analiza las importaciones (si existen)
            if self.idx < len(self.tokens) and self.tokens[self.idx].valor == 'import':
                self.analizar_import()

            # Analiza las funciones (al menos debe haber una función main)
            self.analizar_funciones()

            # Si todo es correcto, imprimimos que el análisis sintáctico es exitoso
            print("\nAnálisis sintáctico completado con éxito.")
        
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            self.error += 1

    def analizar_paquete(self):
        # Verificar la palabra clave 'package'
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'package':
            raise SyntaxError(f"Se esperaba 'package', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el nombre del paquete (main en este caso)
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'main':
            raise SyntaxError(f"Se esperaba 'main', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

    def analizar_import(self):
        # Verificar la palabra clave 'import'
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'import':
            raise SyntaxError(f"Se esperaba 'import', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el siguiente token sea un string con el nombre del paquete importado
        if self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError(f"Se esperaba un string con el nombre del paquete, pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

    def analizar_funciones(self):
        # Analiza todas las funciones en el código
        while self.idx < len(self.tokens):
            if self.tokens[self.idx].tipo == '[KEYWORD]' and self.tokens[self.idx].valor == 'func':
                self.analizar_funcion()
            else:
                raise SyntaxError(f"Se esperaba 'func', pero se encontró: {self.tokens[self.idx]}")

    def analizar_funcion(self):
        # Verificar la palabra clave 'func'
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'func':
            raise SyntaxError(f"Se esperaba 'func', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el nombre de la función
        if self.tokens[self.idx].tipo != '[IDENTIFIER]':
            raise SyntaxError(f"Se esperaba un identificador de función, pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar los paréntesis de la función
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '(':
            raise SyntaxError(f"Se esperaba '(', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar los parámetros de la función (si los hay)
        while self.tokens[self.idx].valor != ')':
            if self.tokens[self.idx].tipo != '[IDENTIFIER]':
                raise SyntaxError(f"Se esperaba un identificador de parámetro, pero se encontró: {self.tokens[self.idx]}")
            self.idx += 1  # Avanzamos al siguiente token

            if self.tokens[self.idx].tipo != '[KEYWORD]':
                raise SyntaxError(f"Se esperaba un tipo de dato, pero se encontró: {self.tokens[self.idx]}")
            self.idx += 1  # Avanzamos al siguiente token

            if self.tokens[self.idx].valor == ',':
                self.idx += 1  # Avanzamos al siguiente parámetro

        # Verificar el cierre de paréntesis
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != ')':
            raise SyntaxError(f"Se esperaba ')', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el inicio del bloque de código '{'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '{':
            raise SyntaxError(f"Se esperaba '{{', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Analizar el cuerpo de la función
        self.analizar_cuerpo_funcion()

        # Verificar el cierre del bloque de código '}'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '}':
            raise SyntaxError(f"Se esperaba '}}', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

    def analizar_cuerpo_funcion(self):
        while self.idx < len(self.tokens):
            # Buscar que la función termine correctamente
            if self.tokens[self.idx].tipo == '[DELIMITER]' and self.tokens[self.idx].valor == '}':
                break  # Fin de la función

            # Analizar declaraciones de variables
            elif self.tokens[self.idx].tipo == '[KEYWORD]' and self.tokens[self.idx].valor == 'var':
                self.analizar_declaracion_variable()

            # Analizar llamadas a funciones como 'Printf'
            elif self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.tokens[self.idx].valor == 'fmt':
                self.analizar_llamada_printf()

            # Analizar otras estructuras (bucles, condicionales, etc.)
            else:
                raise SyntaxError(f"Error sintáctico inesperado: {self.tokens[self.idx]}")

    def analizar_declaracion_variable(self):
        self.idx += 1  # Avanza al identificador de la variable (ej. 'num1')
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]':
            raise SyntaxError("Se esperaba un identificador de variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[KEYWORD]' or (self.tokens[self.idx].valor != 'int' and  self.tokens[self.idx].valor != 'string'):
            raise SyntaxError("Se esperaba tipo 'int' o 'string' para la variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor != '=':
            raise SyntaxError("Se esperaba '=' en la declaración de la variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[INTEGER]' and self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError("Se esperaba un valor entero o cadena para la variable")
        self.idx += 1

    def analizar_llamada_printf(self):
        # Verificar que el token actual sea 'fmt'
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'fmt':
            raise SyntaxError(f"Se esperaba 'fmt', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el siguiente token sea '.'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '.':
            raise SyntaxError(f"Se esperaba '.', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el siguiente token sea 'Printf'
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'Printf':
            raise SyntaxError(f"Se esperaba 'Printf', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Ahora, se espera un '(' después de 'Printf'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '(':
            raise SyntaxError(f"Se esperaba '(', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar los parámetros dentro del 'Printf'
        if self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError(f"Se esperaba una cadena de texto, pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Si hay más parámetros, procesarlos
        while self.tokens[self.idx].valor == ',':
            self.idx += 1  # Avanzamos al siguiente token
            if self.tokens[self.idx].tipo != '[IDENTIFIER]' and self.tokens[self.idx].tipo != '[INTEGER]':
                raise SyntaxError(f"Se esperaba un identificador o número, pero se encontró: {self.tokens[self.idx]}")
            self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el token final sea ')'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != ')':
            raise SyntaxError(f"Se esperaba ')', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token