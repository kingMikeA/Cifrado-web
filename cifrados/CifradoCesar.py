# Archivo: CifradoCesar.py (LÓGICA COMPLETA Y FINAL)

# --- FUNCIONES DE CIFRADO CÉSAR ---

def cifrar_cesar(texto_plano, clave):
    """Cifra un texto usando el Cifrado César (A=0, Z=25)."""
    texto_cifrado = ""
    k = clave % 26 
    
    for caracter in texto_plano:
        if 'A' <= caracter <= 'Z':
            posicion_P = ord(caracter) - ord('A')
            posicion_C = (posicion_P + k) % 26
            texto_cifrado += chr(posicion_C + ord('A'))
        elif 'a' <= caracter <= 'z':
            posicion_P = ord(caracter) - ord('a')
            posicion_C = (posicion_P + k) % 26
            texto_cifrado += chr(posicion_C + ord('a'))
        else:
            texto_cifrado += caracter
            
    return texto_cifrado

def descifrar_cesar(texto_cifrado, clave):
    """Descifra un texto usando el Cifrado César (A=0, Z=25)."""
    texto_descifrado = ""
    k = clave % 26 
    
    for caracter in texto_cifrado:
        if 'A' <= caracter <= 'Z':
            posicion_C = ord(caracter) - ord('A')
            posicion_P = (posicion_C - k + 26) % 26
            texto_descifrado += chr(posicion_P + ord('A'))
        elif 'a' <= caracter <= 'z':
            posicion_C = ord(caracter) - ord('a')
            posicion_P = (posicion_C - k + 26) % 26
            texto_descifrado += chr(posicion_P + ord('a'))
        else:
            texto_descifrado += caracter
            
    return texto_descifrado

# --- FUNCIONES DE CIFRADO VIGENÈRE ---

def cifrar_vigenere(texto_plano, clave):
    """Cifra un texto usando Vigenère (A=0, Z=25) con frase clave."""
    texto_cifrado = ""
    clave = clave.upper()
    indice_clave = 0  
    
    for caracter in texto_plano:
        k = 0
        
        if 'A' <= caracter <= 'Z':
            letra_clave = clave[indice_clave % len(clave)]
            k = ord(letra_clave) - ord('A')
            posicion_P = ord(caracter) - ord('A')
            posicion_C = (posicion_P + k) % 26
            texto_cifrado += chr(posicion_C + ord('A'))
            indice_clave += 1
            
        elif 'a' <= caracter <= 'z':
            letra_clave = clave[indice_clave % len(clave)]
            k = ord(letra_clave) - ord('A')
            posicion_P = ord(caracter) - ord('a')
            posicion_C = (posicion_P + k) % 26
            texto_cifrado += chr(posicion_C + ord('a'))
            indice_clave += 1
            
        else:
            texto_cifrado += caracter
            
    return texto_cifrado

def descifrar_vigenere(texto_cifrado, clave):
    """Descifra un texto usando Vigenère (A=0, Z=25) con frase clave."""
    texto_descifrado = ""
    clave = clave.upper()
    indice_clave = 0
    
    for caracter in texto_cifrado:
        k = 0
        
        if 'A' <= caracter <= 'Z':
            letra_clave = clave[indice_clave % len(clave)]
            k = ord(letra_clave) - ord('A')
            posicion_C = ord(caracter) - ord('A')
            posicion_P = (posicion_C - k + 26) % 26
            texto_descifrado += chr(posicion_P + ord('A'))
            indice_clave += 1
            
        elif 'a' <= caracter <= 'z':
            letra_clave = clave[indice_clave % len(clave)]
            k = ord(letra_clave) - ord('A')
            posicion_C = ord(caracter) - ord('a')
            posicion_P = (posicion_C - k + 26) % 26
            texto_descifrado += chr(posicion_P + ord('a'))
            indice_clave += 1
            
        else:
            texto_descifrado += caracter
            
    return texto_descifrado