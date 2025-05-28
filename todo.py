import re
import os

# -------------------- Token y Lexer --------------------
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
        
        
          
# -------------------- Generación TAC --------------------


# -------------------- Parser --------------------

# Analiza expresiones aritmeticas e impresion de resultados
# Implementacion de expresiones aritmeticas para enteros y flotantes, y verificacion de ciclos for
# Implementacion de expresiones aritmeticas para enteros y flotantes, y verificacion de ciclos for
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0  # Índice para recorrer la lista de tokens
        self.error = 0
        self.scope_stack = [{}]  # Pila de ámbitos (scope)

    def entrar_ambito(self):
        """Crea un nuevo ámbito (scope) y lo agrega a la pila."""
        self.scope_stack.append({})

    def salir_ambito(self):
        """Elimina el ámbito actual de la pila."""
        if len(self.scope_stack) > 1:  # No eliminar el ámbito global
            self.scope_stack.pop()

    def definir_variable(self, nombre, valor):
        """Define una variable en el ámbito actual."""
        self.scope_stack[-1][nombre] = valor

    def obtener_variable(self, nombre):
        """Busca una variable en los ámbitos actuales."""
        for scope in reversed(self.scope_stack):
            if nombre in scope:
                return scope[nombre]
        raise SyntaxError(f"Variable no definida: {nombre}")

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
            if self.error == 0:
                print("Análisis sintáctico completado con éxito")
            else:
                print(f"Análisis completado con {self.error} errores")

        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            self.error += 1
            if self.error > 10:  # Límite de errores
                print("Demasiados errores. Deteniendo el análisis.")
                return

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

        # Crear un nuevo ámbito para la función
        self.entrar_ambito()

        # Analizar el cuerpo de la función
        self.analizar_cuerpo_funcion()

        # Verificar el cierre del bloque de código '}'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '}':
            raise SyntaxError(f"Se esperaba '}}', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Salir del ámbito de la función
        self.salir_ambito()

    def analizar_cuerpo_funcion(self):
        while self.idx < len(self.tokens):
            # Buscar que la función termine correctamente
            if self.tokens[self.idx].tipo == '[DELIMITER]' and self.tokens[self.idx].valor == '}':
                break  # Fin de la función

            # Analizar declaraciones de variables con 'var'
            elif self.tokens[self.idx].tipo == '[KEYWORD]' and self.tokens[self.idx].valor == 'var':
                self.analizar_declaracion_variable()

            # Analizar declaraciones de variables con ':='
            elif self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.idx + 1 < len(self.tokens) and self.tokens[self.idx + 1].valor == ':=':
                self.analizar_declaracion_corta_variable()

            # Analizar llamadas a funciones como 'Printf' o 'Println'
            elif self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.tokens[self.idx].valor == 'fmt':
                self.analizar_llamada_funcion()

            # Analizar ciclos for
            elif self.tokens[self.idx].tipo == '[KEYWORD]' and self.tokens[self.idx].valor == 'for':
                self.analizar_ciclo_for()

            # Analizar expresiones aritméticas
            elif self.tokens[self.idx].tipo == '[INTEGER]' or self.tokens[self.idx].tipo == '[FLOAT]' or self.tokens[self.idx].tipo == '[DELIMITER]':
                resultado = self.analizar_expresion()
                print(f"Resultado de la expresión: {resultado}")

            # Analizar otras estructuras (bucles, condicionales, etc.)
            else:
                raise SyntaxError(f"Error sintáctico inesperado: {self.tokens[self.idx]}")

    def analizar_llamada_funcion(self):
        # Verificar que el token actual sea 'fmt'
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'fmt':
            raise SyntaxError(f"Se esperaba 'fmt', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el siguiente token sea '.'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '.':
            raise SyntaxError(f"Se esperaba '.', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar si es 'Printf' o 'Println'
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor not in ['Printf', 'Println']:
            raise SyntaxError(f"Se esperaba 'Printf' o 'Println', pero se encontró: {self.tokens[self.idx]}")
        funcion = self.tokens[self.idx].valor
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar que el siguiente token sea '('
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '(':
            raise SyntaxError(f"Se esperaba '(', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Analizar los argumentos según la función
        if funcion == 'Println':
            self.analizar_argumentos_println()
        elif funcion == 'Printf':
            self.analizar_argumentos_printf()

        # Verificar que el token final sea ')'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != ')':
            raise SyntaxError(f"Se esperaba ')', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token
    
    def analizar_ciclo_for(self):
        # Verificar la palabra clave 'for'
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'for':
            raise SyntaxError(f"Se esperaba 'for', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar la condición del ciclo
        if self.tokens[self.idx].tipo != '[IDENTIFIER]':
            raise SyntaxError(f"Se esperaba un identificador para la condición, pero se encontró: {self.tokens[self.idx]}")
        variable_condicion = self.tokens[self.idx].valor
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el operador de comparación
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor not in ('<=', '>=', '<', '>', '==', '!='):
            raise SyntaxError(f"Se esperaba un operador de comparación, pero se encontró: {self.tokens[self.idx]}")
        operador = self.tokens[self.idx].valor
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el valor de comparación
        if self.tokens[self.idx].tipo != '[INTEGER]' and self.tokens[self.idx].tipo != '[FLOAT]':
            raise SyntaxError(f"Se esperaba un valor numérico para la comparación, pero se encontró: {self.tokens[self.idx]}")
        valor_comparacion = self.tokens[self.idx].valor
        self.idx += 1  # Avanzamos al siguiente token

        # Verificar el inicio del bloque de código '{'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '{':
            raise SyntaxError(f"Se esperaba '{{', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Crear un nuevo ámbito para el ciclo
        self.entrar_ambito()

        # Analizar el cuerpo del ciclo
        while self.tokens[self.idx].valor != '}':
            # Analizar las declaraciones dentro del ciclo
            if self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.tokens[self.idx].valor == 'fmt':
                self.analizar_llamada_funcion()
            elif self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.tokens[self.idx + 1].valor == '++':
                # Manejar el incremento de la variable (ejemplo: j++)
                variable_incremento = self.tokens[self.idx].valor
                self.idx += 2  # Avanzamos más allá del '++'
                # Simular el incremento de la variable
                valor_actual = self.obtener_variable(variable_incremento)
                self.definir_variable(variable_incremento, valor_actual + 1)
            else:
                raise SyntaxError(f"Error sintáctico inesperado en el cuerpo del ciclo: {self.tokens[self.idx]}")

        # Verificar el cierre del bloque de código '}'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '}':
            raise SyntaxError(f"Se esperaba '}}', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzamos al siguiente token

        # Salir del ámbito del ciclo
        self.salir_ambito()    
    
    def analizar_expresion(self):
        # E → T { (+ | -) T }
        resultado = self.T()  # Evalúa el primer término
        while self.idx < len(self.tokens) and self.tokens[self.idx].tipo == '[OPERATOR]' and self.tokens[self.idx].valor in ('+', '-'):
            operador = self.tokens[self.idx].valor
            self.idx += 1  # Avanzar al siguiente término
            termino = self.T()
            if operador == '+':
                resultado += termino
            elif operador == '-':
                resultado -= termino
        return resultado

    def T(self):
        # T → F { (* | /) F }
        resultado = self.F()  # Evalúa el primer factor
        while self.idx < len(self.tokens) and self.tokens[self.idx].tipo == '[OPERATOR]' and self.tokens[self.idx].valor in ('*', '/'):
            operador = self.tokens[self.idx].valor
            self.idx += 1  # Avanzar al siguiente factor
            factor = self.F()
            if operador == '*':
                resultado *= factor
            elif operador == '/':
                resultado /= factor  # Si necesitas división entera usa //
        return resultado

    def F(self):
        # F → ( E ) | número | identificador
        if self.tokens[self.idx].valor == '(':
            self.idx += 1
            resultado = self.analizar_expresion()
            if self.tokens[self.idx].valor != ')':
                raise SyntaxError("Se esperaba ')'")
            self.idx += 1
            return resultado
        elif self.tokens[self.idx].tipo == '[INTEGER]':
            resultado = int(self.tokens[self.idx].valor)
            self.idx += 1
            return resultado
        elif self.tokens[self.idx].tipo == '[FLOAT]':
            resultado = float(self.tokens[self.idx].valor)
            self.idx += 1
            return resultado
        elif self.tokens[self.idx].tipo == '[IDENTIFIER]':
            nombre_variable = self.tokens[self.idx].valor
            self.idx += 1
            return self.obtener_variable(nombre_variable)  # Buscar la variable en los ámbitos
        else:
            raise SyntaxError(f"Se esperaba un número, identificador o '(', pero se encontró: {self.tokens[self.idx]}")
        
    def analizar_declaracion_corta_variable(self):
        # Obtener el nombre de la variable
        nombre_variable = self.tokens[self.idx].valor
        self.idx += 1  # Avanzar al operador ':='

        # Verificar que el siguiente token sea ':=' 
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor != ':=':
            raise SyntaxError(f"Se esperaba ':=', pero se encontró: {self.tokens[self.idx]}")
        self.idx += 1  # Avanzar al valor o expresión

        # Evaluar la expresión o valor
        valor_variable = self.analizar_expresion()

        # Almacenar la variable en el ámbito actual
        self.scope_stack[-1][nombre_variable] = valor_variable

    def analizar_declaracion_variable(self):
        self.idx += 1  # Avanza al identificador de la variable (ej. 'num1')
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]':
            raise SyntaxError("Se esperaba un identificador de variable")
        nombre_variable = self.tokens[self.idx].valor
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[KEYWORD]' or (self.tokens[self.idx].valor != 'int' and  self.tokens[self.idx].valor != 'string'):
            raise SyntaxError("Se esperaba tipo 'int' o 'string' para la variable")
        tipo_variable = self.tokens[self.idx].valor
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor != '=':
            raise SyntaxError("Se esperaba '=' en la declaración de la variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[INTEGER]' and self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError("Se esperaba un valor entero o cadena para la variable")
        valor_variable = self.tokens[self.idx].valor
        self.idx += 1

        # Almacenar la variable en el ámbito actual
        if tipo_variable == 'int':
            self.scope_stack[-1][nombre_variable] = int(valor_variable)
        else:
            self.scope_stack[-1][nombre_variable] = valor_variable

    def analizar_argumento(self):
        # Si el argumento es un string, devolver su valor
        if self.tokens[self.idx].tipo == '[STRING]':
            valor = self.tokens[self.idx].valor
            self.idx += 1
            return valor

        # Si el argumento es un número, devolver su valor
        elif self.tokens[self.idx].tipo == '[INTEGER]':
            valor = int(self.tokens[self.idx].valor)
            self.idx += 1
            return valor

        # Si el argumento es un identificador (variable), devolver su valor
        elif self.tokens[self.idx].tipo == '[IDENTIFIER]':
            nombre_variable = self.tokens[self.idx].valor
            self.idx += 1
            return self.obtener_variable(nombre_variable)  # Buscar la variable en los ámbitos

        # Si el argumento es una expresión aritmética, evaluarla
        else:
            return self.analizar_expresion()  # Evaluar la expresión y devolver su valor
            

    def analizar_argumentos_println(self):
        while self.tokens[self.idx].valor != ')':
            # Evaluar el argumento (puede ser una expresión aritmética, un string, un número o una variable)
            argumento = self.analizar_argumento()
            print(f"Argumento de Println: {argumento}")  # Simulación de impresión

            # Si hay más argumentos, deben estar separados por ',' 
            if self.tokens[self.idx].valor == ',':
                self.idx += 1  # Avanzamos al siguiente argumento

    def analizar_argumentos_printf(self):
        # El primer argumento debe ser un string (el formato)
        if self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError(f"Se esperaba un string de formato, pero se encontró: {self.tokens[self.idx]}")
        formato = self.tokens[self.idx].valor
        print(f"Formato de Printf: {formato}")  # Simulación de impresión
        self.idx += 1  # Avanzamos al siguiente token

        # Si hay más argumentos, deben estar separados por ','
        while self.tokens[self.idx].valor != ')':
            if self.tokens[self.idx].valor == ',':
                self.idx += 1  # Avanzamos al siguiente argumento

            # Evaluar el argumento (puede ser una expresión aritmética, un número o una variable)
            argumento = self.analizar_argumento()
            print(f"Argumento de Printf: {argumento}")  # Simulación de impresión
            
class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = []
        self.variables = set()
        self.idx = 0  # Índice para recorrer tokens

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instruction):
        self.code.append(instruction)

    def peek_next(self):
        """Mira el siguiente token sin avanzar el índice."""
        if self.idx + 1 < len(self.tokens):
            return self.tokens[self.idx + 1].valor
        return None

    def generate_tac(self, tokens):
        """Genera TAC para ciclos for, if-else y asignaciones."""
        self.tokens = tokens
        self.idx = 0
        while self.idx < len(self.tokens):
            self.parse_statement()
        return self.code

    def parse_statement(self):
        if self.idx >= len(self.tokens):
            return

        token = self.tokens[self.idx]
        
        # Asignación con :=
        if token.tipo == '[IDENTIFIER]' and self.peek_next() == ':=':
            self.parse_assignment()
        
        # Condicional if
        elif token.tipo == '[KEYWORD]' and token.valor == 'if':
            self.parse_if()
        
        # Ciclo for
        elif token.tipo == '[KEYWORD]' and token.valor == 'for':
            self.parse_for()
        
        # Incremento (i++)
        elif token.tipo == '[IDENTIFIER]' and self.peek_next() == '++':
            var = token.valor
            self.emit(f"{var} = {var} + 1")
            self.idx += 2
        
        # Asignación normal (x = 5)
        elif token.tipo == '[IDENTIFIER]' and self.peek_next() == '=':
            var = token.valor
            self.idx += 2  # Saltar '='
            value = self.tokens[self.idx].valor
            self.emit(f"{var} = {value}")
            self.idx += 1
        
        # Ignorar delimitadores
        elif token.tipo == '[DELIMITER]' and token.valor in ['{', '}', '(', ')', ';']:
            self.idx += 1
        
        else:
            self.idx += 1

    # --- Métodos para asignaciones ---
    def parse_assignment(self):
        var = self.tokens[self.idx].valor
        self.idx += 2  # Saltar ':='
        
        if self.tokens[self.idx].tipo in ('[INTEGER]', '[FLOAT]'):
            value = self.tokens[self.idx].valor
            self.emit(f"{var} = {value}")
            self.idx += 1

    # --- Métodos para if-else ---
    def parse_if(self):
        self.idx += 1  # Saltar 'if'
        
        left = self.tokens[self.idx].valor
        op = self.tokens[self.idx + 1].valor
        right = self.tokens[self.idx + 2].valor
        self.idx += 3
        
        false_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"t1 = {left} {op} {right}")
        self.emit(f"if t1 == False goto {false_label}")
        
        # Saltar '{'
        while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '{':
            self.idx += 1
        self.idx += 1
        
        # Bloque if
        while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '}':
            self.parse_statement()
        self.idx += 1  # Saltar '}'
        
        # Manejar else
        if self.idx < len(self.tokens) and self.tokens[self.idx].valor == 'else':
            self.emit(f"goto {end_label}")
            self.emit(f"{false_label}:")
            self.idx += 1
            
            # Saltar '{'
            while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '{':
                self.idx += 1
            self.idx += 1
            
            # Bloque else
            while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '}':
                self.parse_statement()
            self.idx += 1  # Saltar '}'
            
            self.emit(f"{end_label}:")
        else:
            self.emit(f"{false_label}:")

    # --- Métodos para for ---
    def parse_for(self):
        self.idx += 1  # Saltar 'for'
        
        left = self.tokens[self.idx].valor
        op = self.tokens[self.idx + 1].valor
        right = self.tokens[self.idx + 2].valor
        self.idx += 3
        
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"{start_label}:")
        self.emit(f"t1 = {left} {op} {right}")
        self.emit(f"if t1 == False goto {end_label}")
        
        # Saltar '{'
        while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '{':
            self.idx += 1
        self.idx += 1
        
        # Cuerpo del for
        while self.idx < len(self.tokens) and self.tokens[self.idx].valor != '}':
            self.parse_statement()
        self.idx += 1  # Saltar '}'
        
        # Volver a evaluar condición
        self.emit(f"t1 = {left} {op} {right}")
        self.emit(f"goto {start_label}")
        self.emit(f"{end_label}:")
# -------------------- Función principal --------------------
def main():
    
    codigo_ejemplo = """
    package main

    func main() {
       i := 1
       for i <= 1 {
           
           i++
       }
    }
    """
    
    
    
    codigo_ejemplo = """
    package main

    func main() {
        x := 10
        if x >= 5 {
            x = x - 1
        } else {
            x = x + 1
        }
    }
    """
    
    
    codigo_ejemplo = """
     package main

     func main() {
         x := 10
         if x >= 5 {
             i := 1
             if x>=2{
                 i:=1
             }
             for i <= 2 {
                 x = x - 1
             }
         } else {
             x = x + 1
         }
     }
    """
    
    
    lexer = Lexer(codigo_ejemplo)
    lexer.analizar()
    
    if lexer.error == 0:
        print("Análisis léxico completado con éxito")
        parser = Parser(lexer.tokens)
        parser.analizar()
        # Generar TAC
        print("\nCódigo de Tres Direcciones (TAC):")
        tac_generator = TACGenerator()
        tac_code = tac_generator.generate_tac(lexer.tokens)
        for instruction in tac_code:
            print(instruction)
    else:
        print(f"Se encontraron {lexer.error} errores léxicos")

if __name__ == "__main__":
    main()