import numpy as np

# Paso 1: Definir las ecuaciones de consumo de alimentos por cada especie
A = np.array([
    [1, 3, 2],    # Ecuación para alimento 1: 1x + 3y + 2z = 25000
    [1, 4, 1],    # Ecuación para alimento 2: 1x + 4y + 1z = 20000
    [2, 5, 5]     # Ecuación para alimento 3: 2x + 5y + 5z = 55000
])

# Los suministros de alimentos disponibles
B = np.array([25000, 20000, 55000])

# Paso 2: Mostrar las ecuaciones originales
print("Ecuaciones originales:")
print(f"1x + 3y + 2z = 25000")
print(f"1x + 4y + 1z = 20000")
print(f"2x + 5y + 5z = 55000")
print()

# Paso 3: Mostrar la matriz de coeficientes y el vector de suministros
print("Matriz de coeficientes A (consumo de alimentos por especie):")
print(A)
print("\nVector B (suministro de alimentos):")
print(B)
print()

# Comprobar si la matriz A es singular (determinante == 0)
det_A = np.linalg.det(A)
print(f"Determinante de A: {det_A}")

if det_A == 0:
    print("La matriz A es singular. No se puede resolver el sistema de ecuaciones.")
else:
    # Paso 4: Resolver el sistema de ecuaciones directamente usando np.linalg.solve
    print("Resolviendo el sistema de ecuaciones...\n")

    # Resolver el sistema de ecuaciones
    solucion = np.linalg.solve(A, B)

    # Paso 5: Mostrar el resultado final
    print("El resultado de la solución es:")
    print(f"Especie 1 (x): {int(solucion[0])} peces")
    print(f"Especie 2 (y): {int(solucion[1])} peces")
    print(f"Especie 3 (z): {int(solucion[2])} peces")
