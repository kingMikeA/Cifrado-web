# Archivo: MainCesar.py (VERSIÓN FINAL Y PROFESIONAL CON LABELFRAMES)

import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de que CifradoCesar.py contenga las 4 funciones
from CifradoCesar import cifrar_cesar, descifrar_cesar, cifrar_vigenere, descifrar_vigenere 

def ejecutar_cifrado():
    """Maneja la lógica de cifrado/descifrado al presionar el botón, 
    obteniendo los datos de la GUI y mostrando el resultado."""
    
    tipo_cifrado = cifrado_var.get().lower()
    modo = modo_var.get().lower()
    texto = texto_input.get("1.0", tk.END).strip()
    clave = clave_input.get().strip()

    if not texto or not clave:
        messagebox.showerror("Error", "Debes introducir el texto y la clave.")
        resultado_output.set("Error: Introduce el texto y la clave.")
        return

    try:
        resultado = ""
        
        if tipo_cifrado == 'cesar':
            k = int(clave) 
            if modo == 'cifrar':
                resultado = cifrar_cesar(texto, k)
            elif modo == 'descifrar':
                resultado = descifrar_cesar(texto, k)
                
        elif tipo_cifrado == 'vigenere':
            if clave.isdigit(): 
                messagebox.showwarning("Advertencia", "La clave de Vigenère debe ser una FRASE (letras), no un número.")
                return
            if modo == 'cifrar':
                resultado = cifrar_vigenere(texto, clave)
            elif modo == 'descifrar':
                resultado = descifrar_vigenere(texto, clave)
                
        resultado_output.set(resultado)

    except ValueError:
        if tipo_cifrado == 'cesar':
            messagebox.showerror("Error", "La clave de César debe ser un NÚMERO entero.")
        else:
            messagebox.showerror("Error", "Problema con la clave.")
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}")
        resultado_output.set(f"Error inesperado: {e}")

def limpiar_todo():
    """Limpia todos los campos de la interfaz y restablece los valores por defecto."""
    texto_input.delete("1.0", tk.END)
    clave_input.delete(0, tk.END)
    resultado_output.set("")
    cifrado_var.set('Cesar')
    modo_var.set('Cifrar')
    actualizar_label_clave() 

def copiar_resultado():
    """Copia el resultado actual al portapapeles del sistema."""
    resultado = resultado_output.get()
    if resultado:
        root.clipboard_clear()
        root.clipboard_append(resultado)
        root.update()
        messagebox.showinfo("Copiado", "Resultado copiado al portapapeles.")
    else:
        messagebox.showwarning("Advertencia", "No hay resultado para copiar.")

def actualizar_label_clave(*args):
    """Cambia el texto de la etiqueta de la clave según el cifrado seleccionado (César/Vigenère)."""
    if cifrado_var.get() == 'Cesar':
        clave_label.config(text="Clave (César): NÚMERO de desplazamiento")
    elif cifrado_var.get() == 'Vigenere':
        clave_label.config(text="Clave (Vigenère): FRASE clave (solo letras)")

# -----------------------------------------------------------------
# Configuración de la Ventana Principal (GUI)
# -----------------------------------------------------------------

root = tk.Tk()
root.title("Cifrado (César y Vigenère)")
root.geometry("650x750") 
style = ttk.Style()
style.theme_use('vista') 

# --- Variables de Control ---
cifrado_var = tk.StringVar(value='Cesar')
modo_var = tk.StringVar(value='Cifrar')
resultado_output = tk.StringVar()
cifrado_var.trace_add('write', actualizar_label_clave)

# --- Frame Principal ---
main_frame = ttk.Frame(root, padding="30 30 30 30")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# 1. Título
ttk.Label(main_frame, text="CIFRADO", font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

# --- Contenedores LabelFrame para Opciones (Mejora N°1) ---

# Frame para Tipo de Cifrado
cifrado_frame = ttk.LabelFrame(main_frame, text="Tipo de Cifrado", padding="10")
cifrado_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=10)

ttk.Radiobutton(cifrado_frame, text="César", variable=cifrado_var, value='Cesar').grid(row=0, column=0, sticky=tk.W, padx=5)
ttk.Radiobutton(cifrado_frame, text="Vigenère", variable=cifrado_var, value='Vigenere').grid(row=0, column=1, sticky=tk.W, padx=5)

# Frame para Acción (Cifrar/Descifrar)
modo_frame = ttk.LabelFrame(main_frame, text="Acción", padding="10")
modo_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)

ttk.Radiobutton(modo_frame, text="Cifrar", variable=modo_var, value='Cifrar').grid(row=0, column=0, sticky=tk.W, padx=5)
ttk.Radiobutton(modo_frame, text="Descifrar", variable=modo_var, value='Descifrar').grid(row=0, column=1, sticky=tk.W, padx=5)

# 4. Área de Texto
ttk.Label(main_frame, text="Introduce Texto:", font=('Helvetica', 11, 'bold')).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
texto_input = tk.Text(main_frame, height=8, width=60, font=('Arial', 12))
texto_input.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

# 5. Campo de Clave (Etiqueta Dinámica)
clave_label = ttk.Label(main_frame, text="Clave:", font=('Helvetica', 11, 'bold'))
clave_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
clave_input = ttk.Entry(main_frame, width=50, font=('Arial', 10))
clave_input.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
actualizar_label_clave() 

# 6. Botones de Ejecución y Limpieza
ttk.Button(main_frame, text="EJECUTAR CIFRADO", command=ejecutar_cifrado).grid(row=6, column=0, pady=20, sticky=tk.W)
ttk.Button(main_frame, text="ELIMINAR", command=limpiar_todo).grid(row=6, column=0, columnspan=2, pady=20) # Centro el botón Limpiar
ttk.Button(main_frame, text="COPIAR RESULTADO", command=copiar_resultado).grid(row=6, column=1, pady=20, sticky=tk.E)

# 7. Área de Resultado
ttk.Label(main_frame, text="RESULTADO:", font=('Helvetica', 12, 'bold')).grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
ttk.Label(main_frame, textvariable=resultado_output, wraplength=590, anchor="w", justify=tk.LEFT, background="#e0e0e0", relief=tk.SUNKEN, padding=10, font=('Arial', 10)).grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E))


# -----------------------------------------------------------------
# INICIO DE LA APLICACIÓN
# -----------------------------------------------------------------6

root.mainloop()