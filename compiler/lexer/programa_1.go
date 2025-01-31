package main

import "fmt"

// Funcion que suma dos enteros y devuelve el resultado
func Sumar(a int, b int) int {
	return a + b
}

func main() {
	// Declaracion de las dos variables
	var num1 int = 5
	var num2 int = 7

	// Llamada a la funcion Sumar para obtener el resultado
	resultado := Sumar(num1, num2)

	// Mostrar el resultado de la suma
	fmt.Printf("La suma de %d y %d es: %d\n", num1, num2, resultado)
}
