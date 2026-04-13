import math

def obtener_raices_rabin(c, p, q):
    """Calcula las 4 raíces cuadradas modulares usando el Teorema del Resto Chino."""
    n = p * q
    # Raíces parciales en p y q
    r = pow(c, (p + 1) // 4, p)
    s = pow(c, (q + 1) // 4, q)

    # Inversos modulares
    yp = pow(p, -1, q)
    yq = pow(q, -1, p)

    # Combinación para obtener raíces en n
    a = (r * q * yq) % n
    b = (s * p * yp) % n

    return [
        (a + b) % n,
        (n - (a + b) % n),
        (a - b) % n,
        (n - (a - b) % n)
    ]

def ejecutar_programa():
    print("--- CRIPTOSISTEMA RABIN (MANUAL) ---")
    opcion = input("1. Cifrar\n2. Descifrar\nSeleccione opción: ")

    p = int(input("Ingrese primo p (ej. 7): "))
    q = int(input("Ingrese primo q (ej. 11): "))
    n = p * q
    print(f"Módulo calculado n = {n}")

    # Definición manual de la redundancia
    print("\n--- Definición de la Condición de Redundancia ---")
    divisor = int(input("Ingrese el divisor (m mod X): "))
    residuo = int(input(f"Ingrese el residuo esperado (m mod {divisor} = Y): "))

    if opcion == "1":
        palabra = input("\nIngrese la palabra a cifrar: ").lower()
        cifrado = []
        
        print("\nDetalle del cifrado:")
        for letra in palabra:
            if 'a' <= letra <= 'z':
                m = ord(letra) - 96
                # Verificar si la letra cumple la condición antes de cifrar
                if m % divisor != residuo:
                    print(f"(!) La letra '{letra}' ({m}) NO cumple la condición {m} % {divisor} = {residuo}")
                
                c = pow(m, 2, n)
                cifrado.append(c)
                print(f"Letra '{letra}': m={m} -> c={c}")
        
        print(f"\nMensaje cifrado final: {cifrado}")

    elif opcion == "2":
        entrada = input("\nIngrese los valores cifrados (separados por comas): ")
        lista_c = [int(x.strip()) for x in entrada.split(",")]
        
        mensaje_recuperado = ""
        print("\nProceso de descifrado:")
        
        for c in lista_c:
            raices = obtener_raices_rabin(c, p, q)
            encontrado = False
            
            for r in raices:
                # La raíz debe estar en el rango alfabético (1-26) 
                # Y cumplir la condición manual de redundancia
                if 1 <= r <= 26 and (r % divisor == residuo):
                    letra = chr(r + 96)
                    mensaje_recuperado += letra
                    print(f"C={c}: Raíces {raices} -> Elegida: {r} ('{letra}')")
                    encontrado = True
                    break
            
            if not encontrado:
                mensaje_recuperado += "?"
                print(f"C={c}: No se encontró ninguna raíz que cumpla la condición.")

        print(f"\nMensaje final recuperado: {mensaje_recuperado}")

if __name__ == "__main__":
    ejecutar_programa()