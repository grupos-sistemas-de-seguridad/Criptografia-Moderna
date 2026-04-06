import math
def generar_clave_publica(w, q, r):
    return [(peso * r) % q for peso in w]

def cifrar(mensaje_bits, clave_publica):
    cifrado = 0
    for bit, peso_publico in zip(mensaje_bits, clave_publica):
        cifrado += bit * peso_publico
    return cifrado

def descifrar(texto_cifrado, w, q, r):
    inverso_modular = pow(r, -1, q)
    mensaje_limpio = (texto_cifrado * inverso_modular) % q
    mensaje_descifrado = [0] * len(w)
    
    for i in range(len(w) - 1, -1, -1):
        peso_actual = w[i]
        if peso_actual <= mensaje_limpio:
            mensaje_descifrado[i] = 1
            mensaje_limpio -= peso_actual
            
    return mensaje_descifrado

def ingresar_clave_privada():
    print("\n--- CONFIGURACIÓN DE LA CLAVE PRIVADA ---")
    while True:
        try:
            n = int(input("¿Cuántos elementos tendrá la mochila?: "))
            if n > 0: break
            print("Error: Debe ser un número mayor a 0.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")

    w = []
    suma_actual = 0
    
    print("\nIngresa los elementos uno por uno (Regla: debe ser supercreciente).")
    for i in range(n):
        while True:
            try:
                if i == 0:
                    val = int(input(f"Elemento {i+1}: "))
                    if val > 0:
                        w.append(val)
                        suma_actual += val
                        break
                    else:
                        print("Error: El primer elemento debe ser mayor a 0.")
                else:
                    val = int(input(f"Elemento {i+1} (Debe ser MAYOR a {suma_actual}): "))
                    if val > suma_actual:
                        w.append(val)
                        suma_actual += val
                        break
                    else:
                        print(f"  -> RECHAZADO: {val} no es mayor a la suma anterior ({suma_actual}). Intenta de nuevo.")
            except ValueError:
                print("Error: Ingrese un número entero.")
                
    return w, suma_actual

def ingresar_parametros(suma_total):
    print("\n--- CONFIGURACIÓN DE PARÁMETROS MODULARES ---")
    
    while True: # Validar q
        try:
            q = int(input(f"Ingrese el módulo 'q' (Debe ser MAYOR a la suma total de {suma_total}): "))
            if q > suma_total:
                break
            else:
                print(f"  -> RECHAZADO: El módulo debe ser estrictamente mayor a {suma_total}.")
        except ValueError:
            print("Error: Ingrese un número entero.")
            
    while True: # Validar r
        try:
            r = int(input(f"Ingrese el multiplicador 'r' (Debe ser coprimo con {q}): "))
            if math.gcd(r, q) == 1:
                break
            else:
                print(f"  -> RECHAZADO: {r} y {q} comparten divisores. Su MCD es {math.gcd(r, q)}, debe ser 1.")
        except ValueError:
            print("Error: Ingrese un número entero.")
            
    return q, r

def ingresar_mensaje_binario(longitud):
    while True:
        msg = input(f"\nIngrese el mensaje en binario (exactamente {longitud} bits, ej: 1011): ")
        if len(msg) == longitud and all(c in '01' for c in msg):
            return [int(c) for c in msg]
        print(f"  -> ERROR: Debe ingresar una cadena de exactamente {longitud} ceros y unos.")

def menu_principal():
    print("==================================================")
    print("  BIENVENIDO AL SISTEMA MERKLE-HELLMAN (KNAPSACK) ")
    print("==================================================")
    
    while True:
        print("\n¿Qué acción deseas realizar?")
        print("1. Cifrar un mensaje")
        print("2. Descifrar un mensaje")
        print("3. Salir")
        
        opcion = input("Elige una opción (1/2/3): ")
        
        if opcion == '1':
            print("\n>>> INICIANDO PROCESO DE CIFRADO <<<")
            w, suma_total = ingresar_clave_privada()
            q, r = ingresar_parametros(suma_total)
            
            b = generar_clave_publica(w, q, r)
            print(f"\n[+] Clave Pública generada: {b}")
            
            mensaje_bits = ingresar_mensaje_binario(len(w))
            criptograma = cifrar(mensaje_bits, b)
            
            print("\n--------------------------------------------------")
            print(f"RESULTADO: El texto cifrado a enviar es: {criptograma}")
            print("--------------------------------------------------")
            
        elif opcion == '2':
            print("\n>>> INICIANDO PROCESO DE DESCIFRADO <<<")
            w, suma_total = ingresar_clave_privada()
            q, r = ingresar_parametros(suma_total)
            
            while True:
                try:
                    criptograma = int(input("\nIngrese el número cifrado que recibió: "))
                    break
                except ValueError:
                    print("Error: Ingrese un número entero válido.")
                    
            mensaje_descifrado = descifrar(criptograma, w, q, r)
            mensaje_str = "".join(str(bit) for bit in mensaje_descifrado)
            
            print("\n--------------------------------------------------")
            print(f"RESULTADO: El mensaje binario original es: {mensaje_str}")
            print("--------------------------------------------------")
            
        elif opcion == '3':
            print("\nSaliendo del sistema... ¡Éxito en la presentación!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()