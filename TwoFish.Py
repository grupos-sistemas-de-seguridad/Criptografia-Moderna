import struct

# --- UTILIDADES DE BITS ---
def rotl32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def rotr32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

class TwofishEdu:
    def __init__(self, key_str):
        # Generamos subclaves deterministas basadas en tu clave
        # En Twofish real, esto usa una matriz Reed-Solomon
        self.key_bytes = key_str.encode().ljust(16, b'\0')[:16]
        self.K = [struct.unpack("<I", self.key_bytes[i:i+4])[0] for i in range(0, 16, 4)] * 10

    def f_function(self, r0, r1, round_idx):
        # Representación de S-Boxes + PHT
        t0 = r0 
        t1 = rotl32(r1, 8)
        
        # PHT: Pseudo-Hadamard Transform
        f0 = (t0 + t1) % (2**32)
        f1 = (t0 + 2 * t1) % (2**32)
        
        # Adición de llaves de ronda
        f0 ^= self.K[8 + 2 * round_idx]
        f1 ^= self.K[9 + 2 * round_idx]
        return f0, f1

    def encrypt(self, plaintext):
        # Padding a 16 bytes (128 bits)
        data = plaintext.encode().ljust(16, b'\0')[:16]
        words = list(struct.unpack("<4I", data))

        # 1. Input Whitening
        for i in range(4): words[i] ^= self.K[i]

        # 2. 16 Rondas de Feistel
        for r in range(16):
            f0, f1 = self.f_function(words[0], words[1], r)
            
            # Aplicar a la mitad derecha
            words[2] = rotr32(words[2] ^ f0, 1)
            words[3] = rotl32(words[3], 1) ^ f1
            
            # Swap (Intercambio)
            words = [words[2], words[3], words[0], words[1]]

        # 3. Output Whitening
        words = [words[2], words[3], words[0], words[1]] # Swap final
        for i in range(4): words[i] ^= self.K[i+4]
        
        return struct.pack("<4I", *words)

    def decrypt(self, ciphertext):
        words = list(struct.unpack("<4I", ciphertext))

        # 1. Input Whitening (Inverso)
        for i in range(4): words[i] ^= self.K[i+4]

        # 2. 16 Rondas Inversas
        for r in range(15, -1, -1):
            # Swap inicial de la ronda inversa
            words = [words[2], words[3], words[0], words[1]]
            
            f0, f1 = self.f_function(words[0], words[1], r)
            
            # Deshacer rotación y XOR
            words[2] = rotl32(words[2], 1) ^ f0
            words[3] = rotr32(words[3] ^ f1, 1)

        # 3. Output Whitening (Inverso)
        words = [words[2], words[3], words[0], words[1]] # Swap final
        for i in range(4): words[i] ^= self.K[i]
        
        return struct.pack("<4I", *words).decode().strip('\0')

# --- INTERFAZ DE USUARIO ---
def main():
    print("=== LABORATORIO CRIPTOGRÁFICO TWOFISH ===")
    key = input("Ingresa una clave secreta: ")
    word = input("Ingresa la frase a cifrar (máx 16 caracteres): ")

    cipher_engine = TwofishEdu(key)

    # CIFRADO
    encrypted_bytes = cipher_engine.encrypt(word)
    
    print("\n--- RESULTADO DEL CIFRADO ---")
    print(f"HEXADECIMAL: {encrypted_bytes.hex().upper()}")
    print(f"BINARIO:     {' '.join(format(b, '08b') for b in encrypted_bytes)}")

    # DESCIFRADO
    decrypted_word = cipher_engine.decrypt(encrypted_bytes)
    
    print("\n--- RESULTADO DEL DESCIFRADO ---")
    print(f"PALABRA RECUPERADA: {decrypted_word}")

if __name__ == "__main__":
    main()