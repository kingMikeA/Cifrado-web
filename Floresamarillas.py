import math
import turtle

# Configuración inicial
turtle.bgcolor("black")  # Fondo de la pantalla negro
turtle.shape("turtle")    # Forma de la tortuga
turtle.speed(0)           # Velocidad máxima
turtle.fillcolor("brown") # Color de la tortuga (marrón)

# Dibuja el tallo
turtle.penup()
turtle.goto(0, -200)  # Mueve la tortuga a la posición inicial
turtle.pendown()
turtle.setheading(90)  # Dirección hacia arriba
turtle.fillcolor("green")  # Color verde para el tallo
turtle.begin_fill()
turtle.forward(200)   # Dibuja el tallo
turtle.left(90)
turtle.forward(20)    # Dibuja el grosor del tallo
turtle.left(90)
turtle.forward(200)   # Dibuja el tallo
turtle.end_fill()

# Dibuja el centro del girasol
turtle.penup()
turtle.goto(0, -180)  # Coloca la tortuga en el centro del girasol
turtle.fillcolor("#8B4513")  # Color marrón claro
turtle.begin_fill()
turtle.circle(0)      # Dibuja un círculo de tamaño 0 (es solo el centro)
turtle.end_fill()
# Código del girasol (usando espiral para las semillas)
phi = 137.508 * (math.pi / 180.0)  # Ángulo áureo
for i in range(160 + 40):  # 160 + 40 = 200 pétalos
    r = 4 * math.sqrt(i)  # Radio de la espiral
    theta = i * phi       # Ángulo del espiral
    x = r * math.cos(theta)  # Coordenada x
    y = r * math.sin(theta)  # Coordenada y
    turtle.penup()
    turtle.goto(x, y)     # Mueve la tortuga a la posición calculada
    turtle.setheading(i * 137.508)  # Apunta en la dirección correcta
    turtle.pendown()
    if i < 160:  # Si es parte de las semillas
        turtle.stamp()  # Sella la tortuga en la posición
    else:  # Dibuja los pétalos
        turtle.fillcolor("yellow")  # Color amarillo
        turtle.begin_fill()
        turtle.right(20)
        turtle.forward(70)     # Dibuja un pétalo
        turtle.left(40)
        turtle.forward(70)     # Dibuja otro pétalo
        turtle.left(140)
        turtle.forward(70)     # Dibuja otro pétalo
        turtle.left(40)
        turtle.forward(70)     # Dibuja el último pétalo
        turtle.end_fill()

# Escribe "una flor para otra flor" en la parte superior del girasol
turtle.penup()
turtle.goto(0, 200)  # Ajusta la posición vertical según sea necesario
turtle.color("Red")  # Color rojo para el texto
turtle.write("", align="center", font=("Arial", 24, "bold"))

# Oculta la tortuga antes de salir
turtle.hideturtle()

# Cierra la ventana al hacer clic
turtle.exitonclick()
