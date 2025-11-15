import time
import sys
# Importa la librería colorama para los colores de terminal
from colorama import Fore, Style, init

# Inicializa colorama (esencial para que funcione en Windows)
init(autoreset=True)

# --- Configuración de la letra y los colores ---
# Usamos las constantes de Fore para colorama
# Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.RED
versos = [
    # (Verso, pausa al final, emoji, pausa del emoji, color del emoji)
    ("Dime lo que sientes", 0.0, "", 0.0, ""),
    ("Yo me muero por decirte lo que siento", 0.04, "🚨", 0.0, Fore.RED),
    ("Ma, ponte cómoda, mejor toma asiento", 0.05, "🪑", 0.0, Fore.RED),
    ("Lo que diré viene con mucho sentimiento", 0.05, "✨", 0.0, Fore.RED),
    ("Es que me gusta tu cuerpo y tu pelo", 0.02, "💛", 0.0, Fore.YELLOW), # cambié a YELLOW para el emoji
    ("Tus labios, tus ojos tan tiernos", 0.04, "👀", 0.0, Fore.RED),
    ("La sencillez con la que me hablas", 0.05, "💬", 0.0, Fore.RED),
    ("Si sigo sobran las palabras, mami", 0.06, "🎧", 0.0, Fore.RED)
]

# Colores disponibles para alternar por letra
colores_letras = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW]

# --- Función para mostrar los versos ---
def mostrar_versos():
    """
    Imprime cada verso con colores, emojis y pausas para un efecto de animación.
    """
    # Itera sobre cada verso
    for i, (linea, pausa, emoji, pausa_emoji, color_emoji) in enumerate(versos):
        
        # 1. Imprime la línea letra por letra
        for j, letra in enumerate(linea):
            # Obtiene el color de la lista, alternando basado en el índice 'j'
            color = colores_letras[j % len(colores_letras)]
            
            # Imprime la letra con el color, sin salto de línea
            # sys.stdout.write y sys.stdout.flush son necesarios para imprimir inmediatamente
            sys.stdout.write(color + letra + Style.RESET_ALL)
            sys.stdout.flush()
            
            # Pausa breve entre letras para el efecto de escritura a máquina
            time.sleep(pausa)

        # 2. Imprime el emoji al final del verso
        # Usa el color del emoji y luego restablece el estilo
        sys.stdout.write(color_emoji + emoji + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(pausa_emoji)
        
        # 3. Finaliza la línea y añade una pausa
        print() # Imprime un salto de línea
        time.sleep(0.5)

# --- Ejecución principal del código ---
if __name__ == "__main__":
    mostrar_versos()