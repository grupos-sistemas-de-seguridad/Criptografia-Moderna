# INVESTIGACIÓN DE CRIPTOGRAFÍA ALGORITMO IDEA

Estudiante Denis Patzi Canaviri  
Carrera Ingeniería de Sistemas  
Semestre 7mo Semestre  
Escuela Militar de Ingeniería (EMI)  

---
## 1. Implementación del Sistema Criptográfico (Código Fuente)

### 1.1 Código Fuente (Python)
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

### 1.2 Explicación del Código Paso a Paso
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

