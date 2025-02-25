
class Parser:
    
    def __init__(self, tokens):

        self.tokens = tokens
        self.idx = 0  # Índice para recorrer la lista de tokens
        self.error = 0

    def analizar(self):
        try:
            # Comienza analizando la estructura de 'package main'
            self.analizar_package_main()
            #self.analizar_importaciones()
            # Luego verifica la definición de la función 'main'
            self.analizar_func_main()

            # Ahora, analiza el cuerpo de la función
            self.analizar_cuerpo_funcion()

            # Si todo es correcto, imprimimos que el análisis sintáctico es exitoso
            print("\nAnálisis sintáctico completado con éxito.")
        
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            self.error += 1
    
    def analizar_package_main(self):
        
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'package':
            raise SyntaxError("Se esperaba 'package' al inicio")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'main':
            raise SyntaxError("Se esperaba 'main' después de 'package'")
        self.idx += 1
        
        
    def analizar_func_main(self):
       
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor != 'func':
            raise SyntaxError("Se esperaba 'func' para declarar la función")
        self.idx += 1

        if self.tokens[self.idx].tipo != '[IDENTIFIER]' or self.tokens[self.idx].valor != 'main':
            raise SyntaxError("Se esperaba el identificador 'main' para la función")
        self.idx += 1
        if(self.tokens[self.idx].tipo != '[DELIMITER]') or self.tokens[self.idx].valor != '(':
            raise SyntaxError ("se esperaba() luego de declar una funcion")
        self.idx+=1
        if(self.tokens[self.idx].tipo != '[DELIMITER]') or self.tokens[self.idx].valor != ')':
            raise SyntaxError ("se esperaba() luego de declar una funcion")
        self.idx+=1
        # Verificar apertura de la función con '{'
        if self.tokens[self.idx].tipo != '[DELIMITER]' or self.tokens[self.idx].valor != '{':
            raise SyntaxError("Se esperaba '{' al inicio del cuerpo de la función")
        self.idx += 1
    def analizar_importaciones (self):
        if(self.tokens.valor== 'func'):
            return
        if self.tokens[self.idx].tipo != '[KEYWORD]' or self.tokens[self.idx].valor !='import':
            raise SyntaxError("Se espera un import entre main y func")
        self.idx+=1
        if self.tokens[self.idx].tipo != '[STRING]' or self.tokens[self.idx].valor !='"fmt"':
            raise SyntaxError ("se espera un paquete valido despues de import")
        self.idx+=1
    def analizar_cuerpo_funcion(self):
        
        while self.idx < len(self.tokens):
            if self.tokens[self.idx].tipo == '[KEYWORD]' and self.tokens[self.idx].valor == 'var':
                self.analizar_declaracion_variable()
            elif self.tokens[self.idx].tipo == '[IDENTIFIER]' and self.tokens[self.idx].valor == 'resultado':
                self.analizar_operacion_resultado()
            elif self.tokens[self.idx].tipo == '[DELIMITER]' and self.tokens[self.idx].valor == '}':
                # Fin del cuerpo de la función
                self.idx += 1
                break
            else:
                raise SyntaxError(f"Error sintáctico inesperado: {self.tokens[self.idx].valor}")

    def analizar_declaracion_variable(self):
        
        self.idx += 1  # Avanza al identificador de la variable (ej. 'num1')
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]':
            raise SyntaxError("Se esperaba un identificador de variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[KEYWORD]' or (self.tokens[self.idx].valor != 'int' and  self.tokens[self.idx].valor != 'string'):
            raise SyntaxError("Se esperaba tipo 'int' para la variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor != '=':
            raise SyntaxError("Se esperaba '=' en la declaración de la variable")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[INTEGER]' and self.tokens[self.idx].tipo != '[STRING]':
            raise SyntaxError("Se esperaba un valor entero para la variable")
        self.idx += 1
        
    def analizar_operacion_resultado(self):
        
        self.idx += 1  # Avanza al ':='

        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor != ':=':
            raise SyntaxError("Se esperaba ':=' para la asignación")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' and self.tokens[self.idx].tipo != '[INTEGER]':
            raise SyntaxError("Se esperaba 'num1' en la operación")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[OPERATOR]' or self.tokens[self.idx].valor == '=':
            raise SyntaxError("Se esperaba el operador ")
        self.idx += 1
        
        if self.tokens[self.idx].tipo != '[IDENTIFIER]' and self.tokens[self.idx].tipo != '[INTEGER]':
            raise SyntaxError("Se esperaba 'num2' en la operación")
        self.idx += 1