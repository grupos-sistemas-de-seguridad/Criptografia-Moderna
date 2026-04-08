import math
import random

def is_prime(n):
    """número primo."""
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def extended_gcd(a, b):
    """el inverso modular."""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(a, m):
    """inverso modular eficiente"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def L_function(u, n):
    
    return (u - 1) // n

class Paillier:
    def __init__(self, p, q):
        if not (is_prime(p) and is_prime(q)):
            raise ValueError("Ambos números deben ser primos.")
        if p == q:
            raise ValueError("p y q deben ser primos distintos.")
            
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.n_sq = self.n * self.n
        self.lam = math.lcm(self.p - 1, self.q - 1)
        self.g = self.n + 1
        
        #(clave privada auxiliar)
        g_pow_lam = pow(self.g, self.lam, self.n_sq)
        l_val = L_function(g_pow_lam, self.n)
        
        inv = mod_inverse(l_val, self.n)
        if inv is None:
            raise Exception("No se pudo calcular el inverso modular. Esto sucede si MCD(L(g^lambda), n) != 1.")
        
        self.mu = inv

    def encrypt(self, m, r=None):
        
        if m >= self.n:
            raise ValueError(f"El mensaje debe ser menor que n ({self.n})")
        
        if r is None:
            r = random.randint(2, self.n - 1)
            while math.gcd(r, self.n) != 1:
                r = random.randint(2, self.n - 1)
        
        c = (pow(self.g, m, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
        return c, r

    def decrypt(self, c):
    
        u = pow(c, self.lam, self.n_sq)
        l_c = L_function(u, self.n)
        m = (l_c * self.mu) % self.n
        return m

def main():
    print("="*55)
    print("   CRIPTOSISTEMA DE PAILLIER - MODO INTERACTIVO SEGURO")
    print("="*55)
    
    cipher = None
    
    while cipher is None:
        try:
            print("\n[Paso 0] Generación de Claves")
            p_input = input("Ingrese el primer número primo (p) [Sugerencia: 17, 61, 101]: ")
            q_input = input("Ingrese el segundo número primo (q) [Sugerencia: 19, 67, 103]: ")
            
            if not p_input.isdigit() or not q_input.isdigit():
                print(">> Error: Por favor, ingrese solo números enteros.")
                continue
                
            p = int(p_input)
            q = int(q_input)
            
            cipher = Paillier(p, q)
            print(f"\n Claves generadas exitosamente!")
            print(f"Pública (n): {cipher.n}")
            print(f"Privada (lambda): {cipher.lam}")
            print(f"Privada (mu): {cipher.mu}")
            
        except ValueError as ve:
            print(f"\n ERROR MATEMÁTICO: {ve}")
            print("Consejo: Asegúrese de que AMBOS sean números PRIMOS y que NO sean iguales.")
        except Exception as e:
            print(f"\n ERROR DE INVERSO: {e}")
            print("Consejo técnico: El MCD de los valores derivados no es 1. Intente con otros primos.")
            print("Sugerencia de pares seguros: (17, 19), (61, 67), (101, 103)")
            cipher = None

    try:
        
        print("\n" + "-"*30)
        print("[Paso 1] Cifrado")
        msg_val = input(f"Ingrese un número para cifrar (0 a {cipher.n - 1}): ")
        while not msg_val.isdigit() or int(msg_val) >= cipher.n:
            print(f">> Error: Debe ser un número entero entre 0 y {cipher.n - 1}")
            msg_val = input(f"Reintente mensaje: ")
            
        msg = int(msg_val)
        c, r = cipher.encrypt(msg)
        print(f"Texto cifrado (c): {c}")
        print(f"Valor aleatorio (r) generado automáticamente: {r}")
        
        # 2. Descifrado
        print("\n" + "-"*30)
        print("[Paso 2] Descifrado")
        input("Presione Enter para aplicar la llave privada y descifrar...")
        original = cipher.decrypt(c)
        print(f"Mensaje recuperado: {original}")
        
        # 3. Demostración Homomórfica
        print("\n" + "-"*30)
        print("[Paso 3] Demostración Homomórfica (Suma)")
        msg2_val = input(f"Ingrese otro número para sumar al anterior ({msg}): ")
        while not msg2_val.isdigit():
            msg2_val = input("Por favor, ingrese un número válido: ")
            
        msg2 = int(msg2_val)
        c2, r2 = cipher.encrypt(msg2)
        
        # Operación homomórfica:
        c_sum = (c * c2) % cipher.n_sq
        print(f"Multiplicando cifrados en el canal seguro... Resultado: {c_sum}")
        
        res_sum = cipher.decrypt(c_sum)
        print(f"Descifrando el resultado acumulado...")
        print(f"Resultado final: {res_sum}")
        print(f"Verificación: ¿{msg} + {msg2} = {res_sum}? {' SÍ' if res_sum == (msg + msg2) % cipher.n else '❌ NO'}")

    except Exception as e:
        print(f"\nOcurrió un error inesperado durante el proceso: {e}")

if __name__ == "__main__":
    main()
