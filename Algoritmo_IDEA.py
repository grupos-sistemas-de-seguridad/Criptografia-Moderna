def multiplicacion_modular(a, b):
    mod = 2**16 + 1
    if a == 0:
        a = 1
    if b == 0:
        b = 1
    resultado = (a * b) % mod
    if resultado == 0:
        resultado = 1
    return resultado

def suma_modular(a, b):
    return (a + b) % 2**16

def cifrar_bloque(entrada, subclaves):
    # entrada es una lista/tupla de 4 valores de 16 bits
    x1, x2, x3, x4 = entrada

    for i in range(8): # 8 rondas
        x1 = multiplicacion_modular(x1, subclaves[6*i])
        x2 = suma_modular(x2, subclaves[6*i + 1])
        x3 = suma_modular(x3, subclaves[6*i + 2])
        x4 = multiplicacion_modular(x4, subclaves[6*i + 3])

        x5 = x1 ^ x3
        x6 = x2 ^ x4

        x7 = multiplicacion_modular(x5, subclaves[6*i + 4])
        x8 = suma_modular(x6, x7)

        x9 = multiplicacion_modular(x8, subclaves[6*i + 5])
        x10 = suma_modular(x7, x9)

        x1 = x1 ^ x9
        x4 = x4 ^ x9
        x2 = x2 ^ x10
        x3 = x3 ^ x10
    
    # Media ronda final
    x1 = multiplicacion_modular(x1, subclaves[48])
    x2 = suma_modular(x2, subclaves[49])
    x3 = suma_modular(x3, subclaves[50])
    x4 = multiplicacion_modular(x4, subclaves[51])

    return [x1, x3, x2, x4] # orden de salida diferente
