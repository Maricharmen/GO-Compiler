package main

import "fmt"

func entero() {
	// Declaración de variables
	a := 10
	b := 5
	c := 2

	// Expresiones aritméticas
	resultado1 := a + b*c
	resultado2 := (a + b) * c
	resultado3 := a/c + b

	// Imprimir resultados
	fmt.Println("Resultado 1:", resultado1)
	fmt.Println("Resultado 2:", resultado2)
	fmt.Println("Resultado 3:", resultado3)
}
