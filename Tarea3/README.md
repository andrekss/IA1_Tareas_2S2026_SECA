### Integrante 4: Modulo Matematico
* **Responsable:** José Emanuel Monzén Lémus (202300539)
* **Comandos implementados:**
  * `/calcular <numero1> <operador> <numero2>`: Evaluacion aritmetica de suma, resta, multiplicacion y division.
  * `/tabla <numero>`: Generacion de tabla de multiplicar del 1 al 10.
* **Validaciones y robustez aplicadas:**
  * Validacion estricta de cantidad de argumentos (rechaza parametros insuficientes o en exceso con sintaxis esperada).
  * Validacion de tipos numericos para operandos tanto enteros como de punto flotante.
  * Validacion de operadores aritmeticos admitidos (`+`, `-`, `*`, `x`, `X`, `/`).
  * Prevencion y control estricto de indeterminacion por division entre cero (`ZeroDivisionError`).
  * Mensajes de respuesta claros indicando el tipo de error y ejemplos de sintaxis correcta de acuerdo con las especificaciones.
  * Desacoplamiento total: funciones generales independientes de la libreria de Telegram con suite de pruebas unitarias locales.