from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def realizar_operacion_aes():
    print("--- PROCESADOR AES (EJECUCIÓN ÚNICA) ---")
    
    datos_entrada = input("\nIngrese el texto (Mensaje para cifrar o Código HEX para descifrar): ")
    clave = input("Ingrese su clave (16, 24 o 32 caracteres): ")

    if len(clave) not in [16, 24, 32]:
        print(f"\n[!] ERROR: La clave debe tener 16, 24 o 32 caracteres (pusiste {len(clave)}).")
        return

    print("\n¿Qué desea realizar?")
    print("1. Cifrar")
    print("2. Descifrar")
    opcion = input("Seleccione (1 o 2): ")

    key_bytes = clave.encode()
    backend = default_backend()

    try:
        if opcion == "1":
            # --- PROCESO DE CIFRADO ---
            padder = padding.PKCS7(128).padder()
            data_padded = padder.update(datos_entrada.encode()) + padder.finalize()
            
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
            encryptor = cipher.encryptor()
            resultado = encryptor.update(data_padded) + encryptor.finalize()
            
            tipo_tarea = "CIFRADO"
            resultado_final = resultado.hex()

        elif opcion == "2":
            
            texto_cifrado_bytes = bytes.fromhex(datos_entrada)
            
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
            decryptor = cipher.decryptor()
            data_decrypted_padded = decryptor.update(texto_cifrado_bytes) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            data_decrypted = unpadder.update(data_decrypted_padded) + unpadder.finalize()
            
            tipo_tarea = "DESCIFRADO"
            resultado_final = data_decrypted.decode()
        else:
            print("Opción no válida.")
            return

        
        print("\n" + "="*40)
        print(f"RESUMEN DE OPERACIÓN: {tipo_tarea}")
        print("="*40)
        print(f"CLAVE UTILIZADA: {clave}")
        print(f"DATOS DE ENTRADA: {datos_entrada}")
        print(f"RESULTADO FINAL: {resultado_final}")
        print("="*40)

    except Exception as e:
        print(f"\n[!] Error en el proceso: {e}")
        print("Asegúrese de que el código HEX y la clave sean correctos.")

if __name__ == "__main__":
    realizar_operacion_aes()