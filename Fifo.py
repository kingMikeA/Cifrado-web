from collections import deque

# 1. Definir Capacidad y Secuencia
capacidad = 3
paginas_virtuales = ['A', 'B', 'C', 'A', 'D', 'E', 'A', 'B', 'C']

# 2. Inicializar Memoria y Contador
memoria_fisica = deque()
fallos = 0

print("--- Simulación Paginación FIFO (Capacidad: 3) ---")

# 3. Procesar la Secuencia
for pagina in paginas_virtuales:
    # 3a. Verificar si hay un Fallo de Página
    if pagina not in memoria_fisica:
        fallos += 1
        
        # 3b. Aplicar Reemplazo FIFO si la memoria está llena
        if len(memoria_fisica) == capacidad:
            memoria_fisica.popleft() # Elimina la página más antigua (el primero que entró)
            
        # 3c. Cargar la nueva página
        memoria_fisica.append(pagina)
    
    # Mostrar el estado después de cada solicitud
    print(f"Página: {pagina} -> Memoria actual: {list(memoria_fisica)}")

# 4. Mostrar el Resultado Final
print("------------------------------------------------")
print("Total de fallos de página:", fallos)