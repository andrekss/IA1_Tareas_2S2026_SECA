# Tarea 03

**Universidad de San Carlos de Guatemala**  
**Facultad de Ingeniería**  
**Escuela de Ingeniería en Ciencias y Sistemas (ECYS / FIUSAC / Cococys)**  

* **PONDERACIÓN:** 2 pts
* **Tiempo estimado:** 8 horas

---

## 1. MARCO FORMATIVO

### 1.1. Valores

| Nombre del valor | ¿Cómo se aplica en tu laboratorio? |
| :--- | :--- |
| **Responsabilidad** | La responsabilidad implica asumir con compromiso las actividades asignadas, cumpliendo en tiempo y forma con lo solicitado, tanto en el aula como en el desarrollo de ejercicios prácticos. |

### 1.2. Competencia(s)

| Tipo de Competencia | Descripción |
| :--- | :--- |
| **Competencia General** | Integra fundamentos de lógica, realidad aumentada y simulación robótica mediante el uso de entornos de desarrollo para resolver problemas relacionados a inferencia, interacción digital y simulación de comportamientos autónomos. |
| **Competencia Específica** | Desarrolla hechos, reglas, expresiones y predicados recursivos mediante el uso de cláusulas, ciclos, listas, unificación y cortes en Prolog para modelar bases de conocimiento y resolver problemas de inferencia lógica. |

### 1.3. Objetivo SMART

| SMART | Definición | Objetivo redactado |
| :--- | :--- | :--- |
| **Específico (¿Qué?)** | El objetivo es concreto y tangible. | Los estudiantes sepan sobre inteligencia artificial. |
| **Medible (¿Cuánto?)** | El objetivo tiene una medida objetiva de éxito. | Lograr que el 100% de las consultas planteadas generen resultados correctos. |
| **Alcanzable (¿Cómo?)** | El objetivo debe ser posible con los recursos disponibles. | Siendo autodidactas para encontrar información. |
| **Realista (¿Para qué?)** | El objetivo contribuye a metas más amplias. | Desarrollar pensamiento lógico y comprensión de sistemas basados en conocimiento. |
| **A Tiempo (¿Cuándo?)** | El objetivo tiene fecha límite o mejor aún un cronograma de hitos de progreso. | Completar y entregar el ejercicio dentro de la semana asignada. |

---

## 2. Actividad a desarrollar

### 2.1. Herramientas
* Conferencia del curso
* Repositorio del curso
* Editor de código: VSCode, Jupyter Notebook o similar
* Telegram
* BotFather

### 2.2. Descripción de la actividad
Los grupos ya establecidos deberán desarrollar un bot de Telegram interactivo utilizando **Python** y variables de entorno.

El bot deberá permitir la interacción mediante comandos, recibir parámetros, mostrar un menú interactivo y manejar correctamente entradas inválidas.

El bot deberá responder, como mínimo, a los siguientes comandos:
* `/hola`: deberá saludar al usuario utilizando su nombre de Telegram.
* `/hora`: deberá mostrar la fecha y hora actual obtenida dinámicamente.
* `/contacto`: deberá mostrar información de contacto definida por el grupo.
* `/integrantes`: deberá mostrar el nombre y carnet de los integrantes del grupo.
* `/ayuda`: deberá mostrar la lista de comandos disponibles y una breve descripción de cada uno.
* `/menu`: deberá mostrar un menú interactivo utilizando botones de Telegram.
* `/calcular <numero1> <operador> <numero2>`: deberá realizar operaciones de suma, resta, multiplicación y división.
* `/tabla <numero>`: deberá mostrar la tabla de multiplicar del número ingresado, desde 1 hasta 10.
* `/convertir <cantidad> <unidad_origen> <unidad_destino>`: deberá realizar la conversión entre unidades de longitud. Como mínimo deberá soportar las unidades `cm`, `m`, `km`, `mi` y `ft`.
* `/aleatorio <min> <max>`: deberá generar un número entero aleatorio dentro del rango indicado.

El bot deberá contar con un menú interactivo mediante botones de Telegram, desde el cual el usuario pueda conocer y acceder a las diferentes opciones disponibles.

El bot deberá encontrarse desplegado en la nube y disponible durante el período de calificación. Se recuerda que la evaluación será realizada por el auxiliar durante el fin de semana, por lo que es responsabilidad de cada grupo garantizar que el bot permanezca activo, accesible y funcionando correctamente. **Si al momento de la evaluación el bot no se encuentra disponible o no responde a los comandos, la tarea tendrá una calificación de 0 puntos.**

Todos los comandos que reciban parámetros deberán validar que la información ingresada sea correcta. En caso de recibir parámetros inválidos, incompletos o un comando inexistente, el bot deberá responder con un mensaje indicando el error y, cuando corresponda, mostrar la forma correcta de utilizar el comando.

### 2.3. Entrega
Cada grupo deberá entregar:
* Link del mismo repositorio de GitHub utilizado para la Tarea #2 (Solo usar un repositorio). Dentro del repositorio deberán crear una carpeta con el nombre `Tarea#3`, en la cual deberán colocar todos los archivos correspondientes a esta actividad.

El repositorio debe incluir:
* Código fuente del bot de Telegram.
* Link del chat, grupo o canal de Telegram.
* Archivo `requirements.txt`.
* Archivo `.env.example`.
* Archivo `README.md` con:
  * Integrantes (nombre y carnet).
  * Descripción del bot.
  * Instrucciones para instalar y ejecutar el bot.
  * Lista de comandos implementados y descripción de cada uno.
  * Detalle de qué integrante realizó cada parte de la tarea.

---

## 3. Rúbrica de Calificación

### Requisitos para optar a la calificación
* El bot deberá encontrarse disponible y funcionando al momento de realizar la calificación.
* El enlace del grupo de Telegram deberá permitir el acceso para realizar las pruebas.
* El código fuente deberá encontrarse en la carpeta `Tarea#3` del mismo repositorio utilizado para la Tarea #2.

### Detalle de la Calificación

| Criterio | Descripción | Puntos Máximos |
| :--- | :--- | :--- |
| `/hola` | Saluda correctamente al usuario utilizando su nombre de Telegram. | 0.1 |
| `/hora` | Muestra correctamente la fecha y hora actual de forma dinámica. | 0.1 |
| `/contacto` | Muestra correctamente la información de contacto definida por el grupo. | 0.1 |
| `/integrantes` | Muestra correctamente los nombres y carnets de los integrantes. | 0.1 |
| `/ayuda` | Muestra los comandos disponibles y su descripción. | 0.1 |
| `/menu` | Presenta un menú interactivo y funcional mediante botones de Telegram. | 0.25 |
| `/calcular` | Realiza correctamente las operaciones solicitadas y valida entradas incorrectas. | 0.2 |
| `/tabla` | Genera correctamente la tabla de multiplicar solicitada. | 0.1 |
| `/convertir` | Realiza correctamente conversiones entre cm, m, km, mi y ft. | 0.2 |
| `/aleatorio` | Genera correctamente un número entero dentro del rango solicitado. | 0.1 |
| **Manejo de errores** | Maneja comandos inexistentes, parámetros faltantes o valores inválidos sin detener el bot. | 0.15 |
| **Detalle del grupo** | El `README.md` detalla correctamente qué realizó cada integrante del grupo. | 0.2 |
| **Documentación y estructura** | Incluye los archivos solicitados y las instrucciones necesarias para ejecutar el bot. | 0.2 |
| **TOTAL** | | **2.00 pts** |

### Detalle de penalizaciones

| Penalización | Descripción | Descuento |
| :--- | :--- | :--- |
| **No entregar en UEDI y/o classroom** | No realizar la entrega correspondiente en la plataforma UEDI dentro del período establecido. | 100% |
| **Bot no disponible** | El bot no se encuentra activo o accesible en Telegram al momento de realizar la calificación. | 100% |
| **Bot sin funcionamiento** | El bot se encuentra en el grupo de Telegram, pero ninguno de los comandos responde correctamente. | 100% |
| **No utilizar Python** | La solución fue desarrollada utilizando un lenguaje diferente al solicitado. | 100% |
| **Utilizar la API de Telegram** | La solución utiliza la API de Telegram para implementar el funcionamiento solicitado. | 100% |
| **No entregar código fuente** | No se encuentra el código correspondiente a la Tarea #3 en el repositorio indicado. | 100% |
| **Token expuesto en GitHub** | El `TELEGRAM_TOKEN` fue incluido directamente en el código fuente o publicado en el repositorio. | 30% |
| **Comandos incompletos** | Por cada comando obligatorio que no haya sido implementado. | 10% c/u |
| **Comando implementado pero no funcional** | El comando existe, pero genera errores o no realiza correctamente la funcionalidad solicitada. | 5% c/u |
| **Sin menú interactivo** | No se implementó el menú mediante botones de Telegram solicitado. | 15% |
