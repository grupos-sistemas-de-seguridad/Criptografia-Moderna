
# ALGORITMO RSA 

import math


# FUNCIÓN 1: Verificar si un número es primo

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# FUNCIÓN 2: Calcular el inverso modular de e respecto a phi
# (Buscamos d tal que: e * d ≡ 1 mod phi)

def inverso_modular(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None


# FUNCIÓN 3: Generar claves pública y privada

def generar_claves(p, q):

    # Paso 1: Calcular el módulo n
    n = p * q
    print(f"\n  n = {p} × {q} = {n}")

    # Paso 2: Calcular el Totiente de Euler
    phi = (p - 1) * (q - 1)
    print(f"  phi(n) = ({p}-1) × ({q}-1) = {phi}")

    # Paso 3: Calcular e (buscar el primer valor coprimo con phi)
    e = 2
    while e < phi:
        if math.gcd(e, phi) == 1:   # mcd(e, phi) = 1 → son coprimos
            break
        e += 1
    print(f"  e = {e}  →  mcd({e}, {phi}) = {math.gcd(e, phi)}")

    # Paso 4: Calcular d (inverso modular de e)
    d = inverso_modular(e, phi)
    print(f"  d = {d}  →  ({e} × {d}) mod {phi} = {(e * d) % phi}")

    clave_publica  = (n, e)
    clave_privada  = (n, d)
    return clave_publica, clave_privada


# FUNCIÓN 4: Cifrar   →   C = M^e mod n

def cifrar(M, clave_publica):
    n, e = clave_publica
    C = pow(M, e, n)
    return C


# FUNCIÓN 5: Descifrar   →   M = C^d mod n

def descifrar(C, clave_privada):
    n, d = clave_privada
    M = pow(C, d, n)
    return M


print("ALGORITMO RSA")

# Ingresar los números primos p y q
print("\nIngresa dos números primos:")
p = int(input("  p = "))
q = int(input("  q = "))

# Validar que sean primos y distintos
if not es_primo(p) or not es_primo(q):
    print("\n  ERROR: p y q deben ser números primos.")
elif p == q:
    print("\n  ERROR: p y q deben ser distintos.")
else:
    # Generar claves 
    print("\nGENERACIÓN DE CLAVES")
    publica, privada = generar_claves(p, q)
    print(f"\n  Clave Pública  (n, e) = {publica}")
    print(f"  Clave Privada  (n, d) = {privada}")

    # Ingresar el mensaje 
    n = publica[0]
    print(f"\nCIFRADO Y DESCIFRADO")
    print(f"  (El mensaje debe ser un número entre 1 y {n - 1})")
    M = int(input("  Mensaje original M = "))

    if M <= 0 or M >= n:
        print(f"\n  ERROR: El mensaje debe estar entre 1 y {n - 1}.")
    else:
        # Cifrar
        C = cifrar(M, publica)
        print(f"\n  Cifrando:    C = {M}^{publica[1]} mod {n} = {C}")

        # --- Descifrar ---
        M_recuperado = descifrar(C, privada)
        print(f"  Descifrando: M = {C}^{privada[1]} mod {n} = {M_recuperado}")

        # Resultado final
        print(f"  Mensaje original:  {M}")
        print(f"  Mensaje cifrado:   {C}")
        print(f"  Mensaje descifrado:{M_recuperado}")
        if M == M_recuperado:
            print(" El mensaje fue recuperado correctamente.")