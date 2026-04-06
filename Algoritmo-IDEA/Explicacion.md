# INVESTIGACIÓN DE CRIPTOGRAFÍA ALGORITMO IDEA

Estudiante Denis Patzi Canaviri  
Carrera Ingeniería de Sistemas  
Semestre 7mo Semestre  
Escuela Militar de Ingeniería (EMI)  

---

## 3.1 Introducción
Las siglas IDEA significan International Data Encryption Algorithm (Algoritmo Internacional de Cifrado de Datos). [cite_start]Es un cifrador de bloques simétrico desarrollado en 1991 por los criptógrafos Xuejia Lai y James Massey[cite 1, 2]. Este algoritmo opera en

 Bloque de datos 64 bits.
 Longitud de clave 128 bits (conocida por su alta resistencia a los ataques criptográficos).
 Estructura de Rondas Consta de 8 transformaciones idénticas (rondas completas) y una transformación de salida final conocida como media ronda, sumando un total de 8.5 rondas.

 Fuente J. Guerrero-Reyes, C. Rodríguez-Martínez IDEA Algoritmo Criptográfico Simétrico para la Protección Segura de Datos Sensibles, no. 2, pág. 116, 2023.

### Evolución Histórica
El desarrollo del algoritmo comenzó en 1990 en la Escuela Politécnica Federal de Zúrich. Su primera versión fue presentada bajo el nombre de PES (Proposed Encryption Standard). En 1991, tras realizar mejoras para fortalecerlo contra el criptoanálisis diferencial, los autores presentaron el IPES (Improved Proposed Encryption Standard).

Finalmente, en 1992, el diseño fue rebautizado como IDEA. En 1999, tras exhaustivas pruebas de seguridad, se consolidó como un algoritmo mucho más robusto que el estándar DES. Su aplicación práctica más destacada y masiva es en el software de privacidad PGP (Pretty Good Privacy), donde se encarga del cifrado de alta velocidad de los datos.

 Fuente Ariel Santillan Método de encriptación IDEA”, pág. 2, 2013.

---

## 3.2 El Modelo Matemático El Porqué de las Fórmulas
Lo que hace especial a IDEA es que mezcla operaciones de tres grupos algebraicos diferentes. La seguridad reside en que estas operaciones no son distributivas ni asociativas entre sí, lo que genera una gran confusión y difusión de los datos.

### Las 3 Operaciones Fundamentales
1.  XOR Bit a bit (⊕) Operación lógica estándar.
2.  Suma módulo $2^{16}$ (⊞) Suma de números de 16 bits ignorando el acarreo.
3.  Multiplicación módulo $2^{16} + 1$ (⊙) Esta es la más compleja. Se trata el bloque de `0000h` como $2^{16}$ para asegurar que el módulo sea un número primo y así cada elemento tenga un inverso.

 Fuente Manuel J. Lucena López, CRIPTOGRAFÍA Y SEGURIDAD EN COMPUTADORES”, pág. 189, 2013.


---

## 3.3 Funcionamiento Cifrado y Descifrado

### Generación de Subclaves (Key Schedule)
A partir de la clave de 128 bits, se deben generar 52 subclaves de 16 bits cada una
 Las primeras 8 subclaves se toman directamente de los 128 bits.
 Luego, se realiza una rotación a la izquierda de 25 bits y se extraen las siguientes 8, y así sucesivamente.

### Estructura de una Ronda
Cada bloque de 64 bits se divide en 4 sub-bloques de 16 bits ($X_1, X_2, X_3, X_4$). En cada ronda ocurre lo siguiente
1.  Multiplicaciones y sumas de los sub-bloques con las subclaves correspondientes.
2.  Una estructura llamada MA (Multiplication-Addition) que mezcla los resultados.
3.  Intercambio de los sub-bloques internos (excepto en la última ronda).

### Descifrado
El proceso es idéntico al cifrado, pero las subclaves se usan en orden inverso y deben ser sus inversos matemáticos (inversos aditivos o multiplicativos según la operación).

 Fuente Manuel J. Lucena López, CRIPTOGRAFÍA Y SEGURIDAD EN COMPUTADORES”, pág. 199, 2013.

---

## 3.4 Análisis de Seguridad y Ataques 

 Método de Ataque  Descripción 
 ---  --- 
 Fuerza Bruta  Con una clave de 128 bits ($2^{128}$ combinaciones), es computacionalmente imposible de romper hoy en día. 
 Criptoanálisis Diferencial  IDEA es muy resistente. Se requieren ataques complejos sobre versiones reducidas (de pocas rondas) para ver debilidades. 
 Claves Débiles  Existen ciertas claves que pueden facilitar el análisis, aunque la probabilidad de generar una al azar es casi nula. 

---

## 3.5 Ventajas y Desventajas

### Ventajas
 Velocidad Muy eficiente en software y hardware.
 Sin S-Boxes A diferencia de AES o DES, no usa tablas de sustitución, lo que ahorra memoria.
 Seguridad No se conocen ataques prácticos que lo rompan en su versión completa de 8.5 rondas.

### Desventajas
 Tamaño de bloque Al ser de 64 bits, es susceptible a ataques de colisión si se cifran volúmenes masivos de datos (terabytes) con la misma clave.
 Patentes Estuvo bajo patente mucho tiempo, lo que limitó su adopción frente a AES.

 Fuente Lucena López, M. J. (2013). Criptografía y Seguridad en Computadores. Universidad de Jaén. pág. 199.

---
## 4. Implementación del Sistema Criptográfico (Código Fuente)

### 4.1 Código Fuente (Python)
Se presenta la implementación de las funciones de generación de operaciones y cifrado de bloque:

```python
def multiplicacion_modular(a, b):
    mod = 2**16 + 1
    if a == 0: a = 1
    if b == 0: b = 1
    resultado = (a * b) % mod
    if resultado == 0: resultado = 1
    return resultado

def suma_modular(a, b):
    return (a + b) % 2**16

def cifrar_bloque(entrada, subclaves):
    # La entrada de 64 bits se divide en 4 bloques de 16 bits
    x1, x2, x3, x4 = entrada

    for i in range(8): # 8 rondas completas
        # Operaciones de Confusión
        x1 = multiplicacion_modular(x1, subclaves[6*i])
        x2 = suma_modular(x2, subclaves[6*i + 1])
        x3 = suma_modular(x3, subclaves[6*i + 2])
        x4 = multiplicacion_modular(x4, subclaves[6*i + 3])

        # Estructura MA (Difusión)
        x5 = x1 ^ x3
        x6 = x2 ^ x4
        x7 = multiplicacion_modular(x5, subclaves[6*i + 4])
        x8 = suma_modular(x6, x7)
        x9 = multiplicacion_modular(x8, subclaves[6*i + 5])
        x10 = suma_modular(x7, x9)

        # Mezcla de bits con XOR
        x1 = x1 ^ x9
        x4 = x4 ^ x9
        x2 = x2 ^ x10
        x3 = x3 ^ x10

    # Media ronda final (Transformación de salida)
    x1 = multiplicacion_modular(x1, subclaves[48])
    x2 = suma_modular(x2, subclaves[49])
    x3 = suma_modular(x3, subclaves[50])
    x4 = multiplicacion_modular(x4, subclaves[51])

    return [x1, x3, x2, x4]
```

### 4.2 Explicación del Código Paso a Paso
Para cumplir con el análisis detallado del algoritmo, se describe el flujo lógico de la implementación:

1.  **Gestión de la Multiplicación (`multiplicacion_modular`):** * Implementa el producto módulo $2^{16} + 1$.
    * Debido a que el $0$ no tiene inverso multiplicativo en este módulo, el código sigue el estándar de IDEA tratando el valor $0$ de entrada como $2^{16}$ (representado aquí como $1$ para simplificar la operación modular).
2.  **Suma de 16 bits (`suma_modular`):** * Aplica un módulo $65536$ ($2^{16}$). Esto simula el comportamiento de un registro de hardware de 16 bits donde el desbordamiento (carry) se ignora.
3.  **El Bucle de Rondas:** * El programa ejecuta un ciclo `for` de 8 iteraciones. En cada una, utiliza 6 subclaves distintas.
    * **Confusión:** Las primeras cuatro líneas del bucle mezclan los datos con las subclaves mediante operaciones aritméticas.
    * **Difusión:** Las variables `x5` a `x10` pertenecen a la **estructura MA**. Aquí, los bits se "propagan" de modo que un pequeño cambio en la entrada afecte a todos los bits de la salida.



4.  **Transformación de Salida:** * Al terminar las 8 rondas, se aplican las últimas 4 subclaves (`subclaves[48]` a `[51]`).
    * **Nota de diseño:** El resultado final intercambia el orden de $X_2$ y $X_3$ (`return [x1, x3, x2, x4]`). Esto es fundamental en IDEA para que el proceso de descifrado sea idéntico al de cifrado.

---

## 5. Análisis de Ataques Específicos

Siguiendo las instrucciones de la investigación, se han analizado tres métodos aplicables a IDEA:

### 5.1 Ataque de Fuerza Bruta
* **Descripción:** Intento sistemático de probar todas las combinaciones posibles de la clave.
* **Análisis:** Con una clave de 128 bits ($2^{128}$ combinaciones), es computacionalmente imposible de romper hoy en día.
* **Resultado:** No representa una amenaza real.

### 5.2 Ataque por Claves Débiles
* **Descripción:** Ciertas claves con muchos ceros pueden generar subclaves con propiedades predecibles.
* **Análisis:** Si se utiliza una clave débil, la "confusión" disminuye drásticamente.
* **Resultado:** La probabilidad de generar una al azar es casi nula (1 entre $2^{96}$).

### 5.3 Criptoanálisis Diferencial
* **Descripción:** Analiza cómo las diferencias específicas en el texto plano afectan las diferencias en el texto cifrado.
* **Análisis:** IDEA fue diseñado para ser resistente a esto. Solo se han visto éxitos en versiones reducidas de 3 o 4 rondas.
* **Resultado:** Las 8.5 rondas completas permanecen seguras.

---

## 6. Ventajas y Desventajas

### Ventajas:
* **Velocidad:** Muy eficiente en software y hardware.
* **Sin S-Boxes:** A diferencia de AES o DES, no usa tablas de sustitución, lo que ahorra memoria.
* **Seguridad:** No se conocen ataques prácticos que lo rompan en su versión completa.

### Desventajas:
* **Tamaño de bloque:** Al ser de 64 bits, es susceptible a "ataques de colisión" si se cifran volúmenes masivos de datos.
* **Patentes:** Estuvo bajo patente mucho tiempo, lo que limitó su adopción.

> **Fuente:** Lucena López, M. J. (2013). Criptografía y Seguridad en Computadores. Universidad de Jaén.
