import pygame
import sys

# Solicita el peso del usuario
peso = float(input("Ingresa tu peso: "))

# Inicializa Pygame
pygame.init()
2
# Configuración de la ventana
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Imagen Rotando")

# Carga y ajusta la imagen
imagen = pygame.image.load("C:/Users/mikea/Downloads/logos.jpeg")
imagen = pygame.transform.scale(imagen, (400, 400))
rect = imagen.get_rect(center=(300, 200))

# Inicializa variables
angulo = 0
reloj = pygame.time.Clock()

# Reproduce la música
pygame.mixer.music.load("C:\\Users\\mikea\\Downloads\\Oye gelda escuchate esto tiktok baile de tiktok.mp3")
pygame.mixer.music.play(-1)  # Repite la música indefinidamente

# Fuente para mostrar el texto
fuente = pygame.font.SysFont(None, 36)

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Asegura que el programa se cierre correctamente

    # Incrementar el ángulo de rotación
    angulo += 1
    imagen_rotada = pygame.transform.rotate(imagen, angulo)
    rect_rotado = imagen_rotada.get_rect(center=rect.center)

    # Rellenar la pantalla con blanco
    screen.fill((255, 255, 255))

    # Dibujar la imagen rotada
    screen.blit(imagen_rotada, rect_rotado.topleft)

    # Mostrar el peso en la pantalla
    texto = fuente.render(f"Tu peso es: {peso} kg", True, (0, 0, 0))  # Texto en negro
    screen.blit(texto, (20, 20))  # Posición en la parte superior izquierda

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la tasa de fotogramas
    reloj.tick(60)
