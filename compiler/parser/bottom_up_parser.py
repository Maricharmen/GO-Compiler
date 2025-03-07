from compiler.lexer.tokens import Token

class Parser:
    def __init__(self, tokens):
        """
        Constructor del Parser.

        Args:
            tokens (list): Lista de tokens generados por el Lexer.
        """
        self.tokens = tokens
        self.pila = []  # Pila para el análisis bottom-up
        self.errores = 0  # Contador de errores sintácticos
        self.variables = {}  # Diccionario para almacenar variables y sus valores

    def analizar(self):
        """
        Realiza el análisis sintáctico bottom-up y ejecuta las operaciones aritméticas.
        """
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            # Manejo de declaraciones de variables
            if token.tipo == '[KEYWORD]' and token.valor == 'var':
                self.procesar_declaracion_variable(i)
                i += 4  # Saltar los tokens de la declaración (var a int = 10)
                continue

            # Manejo de asignaciones (suma := a + b)
            if token.tipo == '[IDENTIFIER]' and i + 1 < len(self.tokens) and self.tokens[i + 1].valor == ':=':
                self.procesar_asignacion(i)
                i += 4  # Saltar los tokens de la asignación (suma := a + b)
                continue

            # Manejo de llamadas a funciones (fmt.Println)
            if token.tipo == '[IDENTIFIER]' and token.valor == 'fmt':
                self.procesar_llamada_funcion(i)
                i += 6  # Saltar los tokens de la llamada (fmt.Println(...))
                continue

            i += 1

        # Imprimir el estado final de las variables
        print("Estado final de las variables:", self.variables)

    def procesar_declaracion_variable(self, index):
        """
        Procesa la declaración de una variable (var a int = 10).
        """
        nombre_variable = self.tokens[index + 1].valor
        valor_variable = int(self.tokens[index + 4].valor)
        self.variables[nombre_variable] = valor_variable
        print(f"El valor de {nombre_variable} es: {valor_variable}")

    def procesar_asignacion(self, index):
        """
        Procesa una asignación (suma := a + b).
        """
        nombre_variable = self.tokens[index].valor
        operando1 = self.variables.get(self.tokens[index + 2].valor, 0)
        operando2 = self.variables.get(self.tokens[index + 4].valor, 0)
        operador = self.tokens[index + 3].valor

        if operador == '+':
            resultado = operando1 + operando2
        elif operador == '-':
            resultado = operando1 - operando2
        elif operador == '*':
            resultado = operando1 * operando2
        elif operador == '/':
            resultado = operando1 / operando2
        else:
            self.errores += 1
            print(f"Error sintáctico: operador no reconocido {operador}")
            return

        self.variables[nombre_variable] = resultado
        print(f"El resultado de {nombre_variable} es: {resultado}")

    def procesar_llamada_funcion(self, index):
        """
        Procesa una llamada a función (fmt.Println(...)).
        """
        if self.tokens[index + 1].valor == 'Println':
            mensaje = self.tokens[index + 3].valor
            if mensaje.startswith('"') and mensaje.endswith('"'):
                print(mensaje[1:-1])  # Eliminar las comillas
            else:
                valor = self.variables.get(mensaje, "undefined")
                print(f"El valor de {mensaje} es: {valor}")