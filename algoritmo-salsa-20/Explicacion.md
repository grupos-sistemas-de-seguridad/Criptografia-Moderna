
___
**Est Elmer Alcides Apaza Mamani**
___
# Algoritmo Salsa20 - Explicación

Este documento explica paso a paso la implementación en Python del algoritmo **Salsa20**, un cifrador de flujo (stream cipher) diseñado por Daniel J. Bernstein. Es conocido por ser extremadamente rápido, altamente seguro y por no estar sujeto a patentes.  

## 1. ¿Qué es un cifrador de flujo?

A diferencia de los cifradores de bloque (como AES) que cifran datos en bloques fijos, un cifrador de flujo genera una secuencia pseudoaleatoria de bits llamada **keystream** (flujo de clave). Este *keystream* se combina directamente con el mensaje en claro utilizando la operación matemática **XOR** (`^`) para producir el texto cifrado.

## 2. Operaciones Principales (ARX)

Salsa20 basa su seguridad en un diseño conocido como **ARX**, que significa:

- **A**ddition (Suma modular +)

- **R**otation (Rotación circular de bits)

- **X**OR (Operación OR exclusiva ^)

Al no usar multiplicaciones complejas ni tablas de sustitución, el algoritmo esquiva cierto tipo de ataques y es muy rápido en procesadores comunes.

### ROTL (Rotación Circular)

```python

def ROTL(a, b):

    return ((a << b) & 0xFFFFFFFF) | (a >> (32 - b))

```

Toma un número `a` (de 32 bits) y desplaza sus bits hacia la izquierda `b` posiciones. Los bits que "se caen" por la izquierda vuelven a entrar por la derecha. La máscara `0xFFFFFFFF` asegura que el tamaño se mantenga en 32 bits.


### QR (Quarter Round / Cuarto de Ronda)

```python

def QR(x, a, b, c, d):

...

```

Es el "batidor" principal del algoritmo. Toma 4 elementos de la matriz de estado y los mezcla fuertemente usando el patrón ARX. Cada elemento se actualiza en base a la suma y rotación de otros dos.

## 3. La Matriz de Estado (State Matrix)

Salsa20 opera sobre un estado de 64 bytes, que se representa como una cuadrícula (matriz) de 4x4, donde cada celda contiene un número de 32 bits (4 bytes).

En el estado inicial (`entrada`), esos 16 números se distribuyen así:

- **4 palabras de Constante:** Para la versión de clave de 256 bits, es la frase ascii "expand 32-byte k".

- **8 palabras de Clave Especial:** La llave secreta del sistema.

- **2 palabras de Nonce:** Un número que solo se usa una vez (Number Used Once).

- **2 palabras de Contador:** Se incrementa para cifrar cadenas largas de datos (permite acceso aleatorio).

  
## 4. Las Rondas de Mezcla (`ROUNDS = 20`)

El algoritmo ejecuta 20 rondas sobre la matriz inicial:

1. **Rondas Impares:** Aplican la función `QR` sobre las **columnas** de la matriz. Mezclan los datos verticalmente.

2. **Rondas Pares:** Aplican la función `QR` sobre las **filas** de la matriz. Mezclan los datos horizontalmente.
  

### Feedforward (Suma Final)

Después de las 20 rondas de alteración radical, la matriz resultante se suma palabra por palabra con la matriz original. Esto asegura que el proceso sea completamente irreversible (no se puede deshacer simplemente invirtiendo las operaciones).

## 5. Conversión a Bytes (Little-Endian)

```python

keystream = struct.pack('<16I', *salida)

```

La salida de las rondas son dieciséis bloques numéricos de 32 bits. Para cifrar un texto, estos bloques gigantes se "desarman" en 64 bytes individuales (de 8 bits cada uno) leyendo primero el byte menos significativo (Little-Endian). Esto nos da 64 letras/símbolos de flujo de clave listos para usarse.

## 6. Proceso de Cifrado y Descifrado

El cifrado se realiza con una operación XOR simple byte a byte:

`MensajeCifrado = MensajeOriginal XOR Keystream`

Lo brillante es que, gracias a las propiedades matemáticas del XOR, la operación para descifrar es **exactamente la misma**:

`MensajeDescifrado = MensajeCifrado XOR Keystream`

Si usas el mismo flujo de clave (originado por tener la misma clave, constante, nonce, y contador), el mensaje cifrado vuelve a su estado original al aplicarle XOR por segunda vez.