# Estudiante: Jorge Cespedes Calderon
# Saga: A28030-5
# Guía Técnica del Código: Algoritmo Merkle-Hellman

Este documento explica el funcionamiento interno del script de Python que implementa el criptosistema de la mochila (Merkle-Hellman). El código está dividido en tres bloques principales: el motor matemático, las validaciones de seguridad y la interfaz de usuario.

## 1. El Motor Matemático (Core)
Estas tres funciones son el corazón del algoritmo. Realizan las operaciones criptográficas puras.

* **`generar_clave_publica(w, q, r)`**
  * **Qué hace:** Transforma la mochila privada (supercreciente) en una mochila pública (desordenada).
  * **Cómo funciona:** Utiliza una técnica de Python llamada "list comprehension" para recorrer cada elemento (`peso`) de la lista privada `w`. A cada elemento lo multiplica por el multiplicador `r` y le saca el residuo (`% q`). Retorna la nueva lista enmascarada.

* **`cifrar(mensaje_bits, clave_publica)`**
  * **Qué hace:** Oculta el mensaje binario usando la clave pública.
  * **Cómo funciona:** Utiliza la función nativa `zip()` para emparejar cada bit del mensaje con su peso correspondiente en la clave pública (ej. empareja el primer bit con el primer peso). Si el bit es `1`, suma ese peso al total; si es `0`, suma cero. Retorna un único número entero (`cifrado`).

* **`descifrar(texto_cifrado, w, q, r)`**
  * **Qué hace:** Revierte el proceso matemático para recuperar el mensaje original usando la clave privada.
  * **Cómo funciona:** 1. Calcula el inverso modular usando la función optimizada de Python `pow(r, -1, q)`.
    2. Limpia el texto cifrado multiplicándolo por el inverso y aplicándole el módulo `q`.
    3. Aplica el **Algoritmo Voraz (Greedy):** Un bucle `for` recorre la mochila privada en reversa (de mayor a menor). Si el peso actual cabe en el "mensaje limpio", anota un `1` en esa posición y resta el peso. Si no cabe, lo deja en `0`.

## 2. Sistema de Validación (Prevención de Errores)
Para garantizar que el algoritmo no falle por errores matemáticos o de tipeo del usuario, se implementaron bucles `while True` combinados con bloques `try-except`.

* **`ingresar_clave_privada()`**
  * Asegura que el usuario ingrese la cantidad correcta de elementos.
  * **Validación estricta:** Al pedir cada número, suma los valores anteriores en la variable `suma_actual`. Si el usuario ingresa un número que NO es mayor a esa suma, el sistema arroja un error (`RECHAZADO`) y le vuelve a pedir el dato para esa misma posición, garantizando que la lista sea 100% **supercreciente**.

* **`ingresar_parametros(suma_total)`**
  * **Validación del Módulo ($q$):** Comprueba que el número ingresado sea estrictamente mayor a la `suma_total` de la mochila.
  * **Validación del Multiplicador ($r$):** Utiliza la librería matemática de Python (`math.gcd(r, q)`) para verificar el Máximo Común Divisor. Si el resultado no es `1` (lo que significa que comparten divisores y no son coprimos), rechaza el número.

* **`ingresar_mensaje_binario(longitud)`**
  * Garantiza que el mensaje a cifrar tenga exactamente la misma longitud que la mochila.
  * Asegura que la cadena de texto ingresada solo contenga los caracteres `0` y `1`. Si pasa la prueba, convierte esa cadena de texto en una lista de enteros `[1, 0, 1...]` lista para ser procesada.

## 3. Interfaz de Usuario (Menú)
* **`menu_principal()`**
  * Es el orquestador del programa. Mantiene el script corriendo en la terminal mediante un bucle infinito hasta que el usuario elige la opción de salir (`3`). 
  * Simula los dos lados de la comunicación asimétrica: la **Opción 1** orquesta el flujo de cifrado (pidiendo los parámetros para generar la clave pública y luego el mensaje a enviar), y la **Opción 2** orquesta el flujo de descifrado (pidiendo la clave privada del usuario y el número interceptado para revelar el texto original).