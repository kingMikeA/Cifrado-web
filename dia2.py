nombre = input ("ingresar tu nombre")
print(nombre)
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consola de Cifrado (César y Vigenère) - Memoria</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <link rel="stylesheet" href="style.css"> 

    <style>
        /* Importación de la fuente retro */
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        /* Estilos base: Fondo oscuro y degradado. CENTRADO CORREGIDO */
        body {
            font-family: 'VT323', monospace;
            background: linear-gradient(145deg, #0f0a28 0%, #1a0f40 100%);
            /* SE ELIMINA display: flex, justify-content: center, align-items: center */
            min-height: 100vh; 
            padding: 20px;
            /* Color de texto base (casi blanco) */
            color: #f7f0f0; 
        }

        /* Estilos de la caja principal (el "Monitor"). AHORA SOLO ESTO SE CENTRA */
        #app {
            /* Fondo más negro para mayor contraste */
            background: rgba(5, 5, 15, 0.95);
            /* Borde Rojo Intenso */
            border: 2px solid #e70f0f; 
            /* Sombra Roja/Púrpura */
            box-shadow: 0 0 20px rgba(108, 92, 231, 0.7); 
            
            /* AÑADIDO: Centra la consola horizontalmente */
            margin-left: auto;
            margin-right: auto;
        }

        /* Efecto de neón en el título h1 (sombra ROJA en CSS) */
        #app h1 {
            text-shadow: 0 0 7px #eb0c0c, 0 0 15px #f30d0d; 
        }

        /* Efecto de borde de neón en los inputs y textareas */
        .neon-input {
            background-color: rgba(20, 15, 45, 0.8);
            border: 1px solid #4a4175;
            /* Color de texto rojo neón */
            color: #f00b0b; 
            /* Sombra de texto rojo/azul */
            text-shadow: 0 0 5px #011214; 
        }
        .neon-input:focus {
            /* Color de foco púrpura/azul */
            border-color: #a29bfe;
            box-shadow: 0 0 10px rgba(162, 155, 254, 0.9);
        }

        /* Estilos para el botón principal (EJECUTAR) */
        .btn-neon-primary {
            background-color: #6c5ce7; /* Púrpura base */
            text-shadow: 0 0 5px #a29bfe;
            box-shadow: 0 0 10px rgba(162, 155, 254, 0.8), inset 0 0 5px #a29bfe;
            transition: all 0.2s ease;
        }
        .btn-neon-primary:hover {
            background-color: #a29bfe;
            box-shadow: 0 0 20px rgba(162, 155, 254, 1), inset 0 0 10px #6c5ce7;
            color: #000;
        }

        /* Estilo para el área de resultado (Salida de la Consola - amarillo) */
        #resultadoOutput {
            color: #fafa00; /* Neón amarillo brillante */
            text-shadow: 0 0 7px #fafa00;
            border: 1px dashed #fafa00;
            background-color: rgba(10, 5, 30, 0.8);
            /* Ajuste de altura para mostrar múltiples resultados del brute-force */
            min-height: 8rem;
            max-height: 25rem; 
            overflow-y: auto;
            white-space: pre-wrap; /* Mantiene saltos de línea y formateo */
        }

        /* Estilos de los radios (Selector de modo) */
        .neon-radio:checked {
            background-color: #a29bfe;
            border-color: #a29bfe;
        }
        .neon-radio:checked + span {
            color: #a29bfe;
            text-shadow: 0 0 5px #a29bfe;
        }

        /* Ajustes de tipografía para mantener la estética monospace */
        .text-xl, .text-2xl, .text-lg, p, label {
            letter-spacing: 1px;
        }

        /* Estilos para el mensaje flotante (para notificaciones de éxito/error) */
        #mensajeFlotante {
            z-index: 1000;
            font-size: 1.5rem; /* Ajuste para VT323 */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.8); /* Sombra predeterminada */
        }

        /* --- Estilos para la Firma en la Esquina (Footer) --- */
        .footer-esquina {
            /* Fija el elemento a la ventana del navegador */
            position: fixed; 
            
            /* Lo ancla a la parte inferior y a la derecha con un margen de 20px */
            bottom: 20px;
            right: 20px;
            
            /* Asegura que no sea demasiado ancho */
            max-width: 300px; 
            
            /* Color de fondo sutil para que se vea */
            background-color: rgba(0, 0, 0, 0.4); 
            
            /* Relleno interno para que el texto no toque el borde */
            padding: 10px; 
            
            /* Z-index alto para que esté encima de otros elementos */
            z-index: 1000; 
            
            /* Alineación de texto */
            text-align: right;
            border-radius: 4px; /* Opcional: bordes redondeados */
        }
    </style>
</head>
<body>

<div id="app" class="w-full max-w-xl rounded-xl p-8 transition-all duration-300">
    <h1 class="text-4xl font-extrabold text-center text-cyan-400 mb-2 tracking-widest uppercase">
        Cifrado César y Vigenère
    </h1>
    <p class="text-center text-lg text-gray-400 mb-8 tracking-wider">Consola de Cifrado - Memoria Activa</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        
        <div class="p-4 border-b border-purple-800">
            <label class="block text-lg font-bold text-purple-400 mb-3">TIPO DE CIFRADO</label>
            <div class="flex flex-col space-y-2">
                <label class="inline-flex items-center cursor-pointer">
                    <input type="radio" name="cifrado" value="cesar" checked onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">César</span>
                </label>
                <label class="inline-flex items-center cursor-pointer">
                    <input type="radio" name="cifrado" value="vigenere" onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">Vigenère</span>
                </label>
            </div>
        </div>

        <div class="p-4 border-b border-purple-800">
            <label class="block text-lg font-bold text-purple-400 mb-3">ACCIÓN A EJECUTAR</label>
            <div class="flex flex-col space-y-2">
                <label class="inline-flex items-center cursor-pointer">
                    <input type="radio" name="modo" value="cifrar" checked onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">CIFRAR</span>
                </label>
                <label class="inline-flex items-center cursor-pointer">
                    <input type="radio" name="modo" value="descifrar-memoria" onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">DESCIFRAR</span>
                </label>
            </div>
        </div>
    </div>
    
    <div id="entradaContainer" class="mb-6">
        <label for="textoEntrada" class="block text-lg font-semibold text-purple-300 mb-2">TEXTO DE ENTRADA</label>
        <textarea id="textoEntrada" rows="6" placeholder="Escribe tu mensaje aquí..."
                  class="w-full p-3 rounded-md focus:outline-none transition-all neon-input text-2xl"></textarea>
    </div>

    <div id="claveContainer" class="mb-8 transition-opacity duration-300">
        <label id="claveLabel" for="claveInput" class="block text-lg font-semibold text-purple-300 mb-2">
            CLAVE: SOLO NÚMEROS ENTEROS (César)
        </label>
        <input type="text" id="claveInput" placeholder="Clave numérica para César (Ej: 3)"
               class="w-full p-3 rounded-md focus:outline-none transition-all neon-input text-xl">
    </div>

    <div class="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4 mb-8">
        
        <div class="relative flex-1">
            <button id="ejecutarBtn" onclick="ejecutarCifrado()"
                    class="w-full px-8 py-4 text-white font-bold rounded-lg uppercase tracking-widest btn-neon-primary transition-all duration-300">
                EJECUTAR 
            </button>
        </div>

        <button id="descargarBtn" onclick="exportarTablaAExcel()"
                class="px-6 py-4 bg-green-700 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200 hidden">
            DESCARGAR TABLA (.xlsx)
        </button>

        <button onclick="limpiarTodo()"
                class="px-6 py-4 bg-gray-700 text-gray-300 font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
            ELIMINAR
        </button>
    </div>

    <div class="p-4 rounded-md">
        <label class="block text-xl font-bold text-yellow-400 mb-2">RESULTADO:</label>
        
        <div id="tablaResultadoContainer" class="mb-4">
            </div>
        
        <pre id="resultadoOutput" class="break-words min-h-[4rem] p-3 rounded-md text-2xl">// ESPERANDO DATOS...</pre>
        
        <div id="mensajeFlotante" class="fixed top-5 left-1/2 -translate-x-1/2 p-3 rounded-md text-white shadow-xl hidden transition-all duration-300 opacity-0"></div>
    </div>

</div> <footer class="mt-10 p-4 border-t border-purple-900 footer-esquina">
    <p class="text-right text-sm text-gray-500 font-mono tracking-wide">
        &copy; 2025 Consola de Cifrado César y Vigenère | Desarrollado por Miguel Angel Arias
    </p>
    <p class="text-right text-xs text-gray-600 mt-1">
        Proyecto Académico de Criptografía.
    </p>
</footer>

<script src="app.js"></script>

</body>
</html>