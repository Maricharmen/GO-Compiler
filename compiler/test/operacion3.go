package main

import "fmt"

func flotante() {
	// Declaración de variables
	a := 10.5
	b := 5.5
	c := 2.5

	// Expresiones aritméticas
	resultado1 := a + b*c
	resultado2 := (a + b) * c
	resultado3 := c/a + b

	// Imprimir resultados
	fmt.Println("Resultado 1:", resultado1)
	fmt.Println("Resultado 2:", resultado2)
	fmt.Println("Resultado 3:", resultado3)
}
