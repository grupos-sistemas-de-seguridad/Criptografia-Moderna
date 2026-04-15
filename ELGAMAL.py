import random

# 🔹 Verificar si un número es primo
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 🔹 Inverso modular
def inverso_modular(a, p):
    return pow(a, p-2, p)

# 🔹 Verificar generador
def es_generador(g, p):
    valores = set()
    for i in range(1, p):
        valores.add(pow(g, i, p))
    return len(valores) == p-1

# 🔹 PROGRAMA PRINCIPAL
print("=== ELGAMAL CON VALIDACIÓN ===")

# Entrada de datos
p = int(input("Ingrese p (primo): "))
g = int(input("Ingrese g (generador): "))
x = int(input("Ingrese x (clave privada): "))
k = int(input("Ingrese k (aleatorio): "))
M = int(input("Ingrese mensaje M: "))

# 🔍 VALIDACIONES

# Validar p primo
if not es_primo(p):
    print("❌ ERROR: p no es primo. Cambie p.")
    exit()

# Validar g
if g <= 1 or g >= p:
    print("❌ ERROR: g debe estar entre 1 y p.")
    exit()

if not es_generador(g, p):
    print("❌ ERROR: g NO es generador válido. Cambie g.")
    exit()

# Validar x
if x <= 0 or x >= p:
    print("❌ ERROR: x debe estar entre 1 y p-1.")
    exit()

# Validar k
if k <= 0 or k >= p:
    print("❌ ERROR: k debe estar entre 1 y p-1.")
    exit()

# Validar mensaje
if M >= p:
    print("❌ ERROR: M debe ser menor que p.")
    exit()

print("\n✔ Datos válidos\n")

# 🔐 GENERACIÓN DE CLAVE
A = pow(g, x, p)
print("Clave pública (p, g, A):", (p, g, A))
print("Clave privada x:", x)

# 🔒 CIFRADO
C1 = pow(g, k, p)
C2 = (M * pow(A, k, p)) % p

print("\nMensaje cifrado (C1, C2):", (C1, C2))

# 🔓 DESCIFRADO
S = pow(C1, x, p)
S_inv = inverso_modular(S, p)
M_recuperado = (C2 * S_inv) % p

print("\nMensaje recuperado:", M_recuperado)
