import struct

# ROTACIÓN CIRCULAR (Operación de difusión)
# Mueve los bits hacia la izquierda y los que "caen", los vuelve a meter por la derecha.
def ROTL(a, b):
    return ((a << b) & 0xFFFFFFFF) | (a >> (32 - b))

# QUARTER ROUND (El "Batidor" o Mezcla Principal)
# Aplica el patrón ARX: Suma (Add), Rotación (Rotate) y XOR sobre 4 elementos.
def QR(x, a, b, c, d):
    x[b] ^= ROTL((x[a] + x[d]) & 0xFFFFFFFF, 7)
    x[c] ^= ROTL((x[b] + x[a]) & 0xFFFFFFFF, 9)
    x[d] ^= ROTL((x[c] + x[b]) & 0xFFFFFFFF, 13)
    x[a] ^= ROTL((x[d] + x[c]) & 0xFFFFFFFF, 18)

# Estándar validado que equilibra seguridad y rendimiento
ROUNDS = 20

# Transforma una entrada de 64 bytes en un bloque de flujo de clave
def salsa20_block(out_arr, in_arr):
    x = [0] * 16

    # Copiar el estado inicial (la matriz 4x4 a un arreglo lineal)
    for i in range(16):
        x[i] = in_arr[i]

    # Aplicar las 20 rondas de mezcla (10 pares de rondas)
    for i in range(0, ROUNDS, 2):
        # Rondas Impares: Mezcla vertical (Columnas)
        QR(x,  0,  4,  8, 12) # Columna 1
        QR(x,  5,  9, 13,  1) # Columna 2
        QR(x, 10, 14,  2,  6) # Columna 3
        QR(x, 15,  3,  7, 11) # Columna 4

        # Rondas Pares: Mezcla horizontal (Filas)
        QR(x,  0,  1,  2,  3) # Fila 1
        QR(x,  5,  6,  7,  4) # Fila 2
        QR(x, 10, 11,  8,  9) # Fila 3
        QR(x, 15, 12, 13, 14) # Fila 4

    # Feedforward (Suma final)
    # Suma la matriz original con la mezclada para hacer el algoritmo irreversible
    for i in range(16):
        out_arr[i] = (x[i] + in_arr[i]) & 0xFFFFFFFF


if __name__ == "__main__":
    
    # MATRIZ DE ESTADO INICIAL
    # Contiene: Constantes fijas ("expand 32-byte k"), Llave secreta, Nonce y Contador
    entrada = [
        0x61707865, 0x01234567, 0x89abcdef, 0x01234567, # Fila 1
        0x89abcdef, 0x3320646e, 0x00000000, 0x00000000, # Fila 2
        0x00000000, 0x00000000, 0x79622d32, 0x01234567, # Fila 3
        0x89abcdef, 0x01234567, 0x89abcdef, 0x6b206574  # Fila 4
    ]

    salida = [0] * 16
    
    # Generamos el bloque de 16 enteros (números grandotes de 32 bits)
    salsa20_block(salida, entrada)

    # CONVERSIÓN A BYTES (Little-Endian)
    # Desarmamos los 16 números de 32 bits en 64 "letras" de 8 bits para operar con el texto.
    keystream = struct.pack('<16I', *salida)
    
    """ 
    # Alternativa manual para convertir a bytes (sin usar la librería struct):
    keystream = bytearray()
    for numero in salida:
        keystream.append((numero      ) & 0xFF)
        keystream.append((numero >>  8) & 0xFF)
        keystream.append((numero >> 16) & 0xFF)
        keystream.append((numero >> 24) & 0xFF) 
    """

    # Función auxiliar para visualizar los bytes como 8 ceros y unos en pantalla
    def a_binario(datos_bytes):
        return " ".join(f"{b:08b}" for b in datos_bytes)
    
    # Preparamos el mensaje a cifrar
    mensaje_texto = "hola"
    mensaje_bytes = mensaje_texto.encode('utf-8')
    
    # Solo tomamos del keystream la cantidad exacta de bytes que mide el mensaje
    keystream_usado = keystream[:len(mensaje_bytes)]

    print("--- 1. MENSAJE ORIGINAL ---")
    print(f"Texto  : '{mensaje_texto}'")
    print(f"Binario: {a_binario(mensaje_bytes)}")

    print("\n--- 2. KEYSTREAM (FLUJO DE CLAVE SALSA20) ---")
    print(f"Binario: {a_binario(keystream_usado)}")

    # CIFRADO: Operación XOR (^) entre cada byte del mensaje y el keystream
    mensaje_cifrado = bytearray()
    for i in range(len(mensaje_bytes)):
        mensaje_cifrado.append(mensaje_bytes[i] ^ keystream_usado[i])

    print("\n--- 3. MENSAJE CIFRADO ---")
    print(f"Binario: {a_binario(mensaje_cifrado)}")

    # DESCIFRADO: El XOR es reversible. Al aplicar el mismo keystream al texto cifrado, recuperamos el original.
    mensaje_descifrado = bytearray()
    for i in range(len(mensaje_cifrado)):
        mensaje_descifrado.append(mensaje_cifrado[i] ^ keystream_usado[i])

    print("\n--- 4. MENSAJE DESCIFRADO ---")
    print(f"Binario: {a_binario(mensaje_descifrado)}")
    print(f"Texto  : '{mensaje_descifrado.decode('utf-8')}'")