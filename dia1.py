<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consola de Cifrado (César y Vigenère) - Memoria</title>
    
    <!-- Carga de Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Estilos de Consola Retro y Fuente VT323 -->
    <style>
        /* Importación de la fuente retro */
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        /* Estilos base: Fondo oscuro y degradado, centrado */
        body {
            font-family: 'VT323', monospace;
            background: linear-gradient(145deg, #0f0a28 0%, #1a0f40 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            /* Color de texto base (casi blanco) */
            color: #f7f0f0; 
        }

        /* Estilos de la caja principal (el "Monitor") */
        #app {
            /* Fondo más negro para mayor contraste */
            background: rgba(5, 5, 15, 0.95);
            /* Borde Rojo Intenso */
            border: 2px solid #e70f0f; 
            /* Sombra Roja/Púrpura */
            box-shadow: 0 0 20px rgba(108, 92, 231, 0.7); 
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
    </style>
</head>
<body>

<div id="app" class="w-full max-w-xl rounded-xl p-8 transition-all duration-300">
    <!-- TÍTULO -->
    <h1 class="text-4xl font-extrabold text-center text-cyan-400 mb-2 tracking-widest uppercase">
        Cifrado César y Vigenère
    </h1>
    <p class="text-center text-lg text-gray-400 mb-8 tracking-wider">Consola de Cifrado - Memoria Activa</p>

    <!-- Opciones de Cifrado y Modo -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        
        <!-- Selector de Cifrado -->
        <div class="p-4 border-b border-purple-800">
            <label class="block text-lg font-bold text-purple-400 mb-3">TIPO DE CIFRADO</label>
            <div class="flex flex-col space-y-2">
                <label class="inline-flex items-center cursor-pointer">
                    <!-- Se llama a toggleAutoDecryptUI al cambiar -->
                    <input type="radio" name="cifrado" value="cesar" checked onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">César</span>
                </label>
                <label class="inline-flex items-center cursor-pointer">
                    <!-- Se llama a toggleAutoDecryptUI al cambiar -->
                    <input type="radio" name="cifrado" value="vigenere" onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">Vigenère</span>
                </label>
            </div>
        </div>

        <!-- Selector de Acción -->
        <div class="p-4 border-b border-purple-800">
            <label class="block text-lg font-bold text-purple-400 mb-3">ACCIÓN A EJECUTAR</label>
            <div class="flex flex-col space-y-2">
                <label class="inline-flex items-center cursor-pointer">
                    <!-- Se llama a toggleUIMode al cambiar -->
                    <input type="radio" name="modo" value="cifrar" checked onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">CIFRAR</span>
                </label>
                <!-- Opcion de descifrado (ahora usa solo memoria) -->
                <label class="inline-flex items-center cursor-pointer">
                    <!-- Se llama a toggleUIMode al cambiar -->
                    <input type="radio" name="modo" value="descifrar-memoria" onchange="toggleUIMode()" class="form-radio h-4 w-4 text-purple-400 border-gray-600 neon-radio">
                    <span class="ml-2 text-xl text-gray-300">DESCIFRAR</span>
                </label>
            </div>
        </div>
    </div>
    
    <!-- Área de Texto de Entrada -->
    <div id="entradaContainer" class="mb-6">
        <label for="textoEntrada" class="block text-lg font-semibold text-purple-300 mb-2">TEXTO DE ENTRADA</label>
        <textarea id="textoEntrada" rows="6" placeholder="Escribe tu mensaje aquí..."
                  class="w-full p-3 rounded-md focus:outline-none transition-all neon-input text-2xl"></textarea>
    </div>

    <!-- Campo de Clave (Ocultable) -->
    <div id="claveContainer" class="mb-8 transition-opacity duration-300">
        <label id="claveLabel" for="claveInput" class="block text-lg font-semibold text-purple-300 mb-2">
            CLAVE: SOLO NÚMEROS ENTEROS (César)
        </label>
        <input type="text" id="claveInput" placeholder="Clave numérica para César (Ej: 3)"
               class="w-full p-3 rounded-md focus:outline-none transition-all neon-input text-xl">
    </div>

    <!-- Botones de Acción -->
    <div class="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4 mb-8">
        
        <!-- Contenedor para la ACCIÓN PRINCIPAL -->
        <div class="relative flex-1">
            <!-- Botón de Ejecución -->
            <button id="ejecutarBtn" onclick="ejecutarCifrado()"
                    class="w-full px-8 py-4 text-white font-bold rounded-lg uppercase tracking-widest btn-neon-primary transition-all duration-300">
                EJECUTAR PROCEDIMIENTO
            </button>
            
            <!-- Botón de Descifrado Automático (ELIMINADO: Ya no hay modo manual) -->
        </div>

        <!-- Botón 3: Eliminar -->
        <button onclick="limpiarTodo()"
                class="px-6 py-4 bg-gray-700 text-gray-300 font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
            ELIMINAR
        </button>
    </div>

    <!-- Área de Resultado -->
    <div class="p-4 rounded-md">
        <label class="block text-xl font-bold text-yellow-400 mb-2">// RESULTADO::SALIDA</label>
        <pre id="resultadoOutput" class="break-words min-h-[4rem] p-3 rounded-md text-2xl">// ESPERANDO DATOS...</pre>
        <!-- Mensaje flotante para notificaciones -->
        <div id="mensajeFlotante" class="fixed top-5 left-1/2 -translate-x-1/2 p-3 rounded-md text-white shadow-xl hidden transition-all duration-300 opacity-0"></div>
    </div>

</div>

<!-- Lógica JavaScript para el cifrado y manejo de la interfaz -->
<script>
    // Constantes
    const BASE_UPPER = 'A'.charCodeAt(0); // 65
    const BASE_LOWER = 'a'.charCodeAt(0); // 97
    const ALPHABET_SIZE = 26; // 26 letras en el alfabeto
    
    // ** VARIABLE DE MEMORIA GLOBAL **
    let _memoriaCifrado = ""; 


    // =============================================================================
    // 1. LÓGICA DE CIFRADO (Funciones Core)
    // =============================================================================

    /** Obtiene el valor del radio button seleccionado por su nombre. */
    function getRadioValue(name) {
        const selector = `input[name="${name}"]:checked`; 
        const element = document.querySelector(selector);
        return element ? element.value : null;
    }

    /** Cifra un texto utilizando el Cifrado César. */
    function cifrarCesar(textoPlano, clave) {
        let textoCifrado = "";
        const k = clave % ALPHABET_SIZE; 
        
        for (let i = 0; i < textoPlano.length; i++) {
            let caracter = textoPlano[i];
            let code = caracter.charCodeAt(0);

            // Mayúsculas
            if (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE) {
                let posicionP = code - BASE_UPPER;
                let posicionC = (posicionP + k) % ALPHABET_SIZE;
                textoCifrado += String.fromCharCode(posicionC + BASE_UPPER);
            }
            // Minúsculas
            else if (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE) {
                let posicionP = code - BASE_LOWER;
                let posicionC = (posicionP + k) % ALPHABET_SIZE;
                textoCifrado += String.fromCharCode(posicionC + BASE_LOWER);
            }
            // Conservar otros caracteres
            else {
                textoCifrado += caracter;
            }
        }
        return textoCifrado;
    }

    /** Descifra un texto utilizando el Cifrado César. */
    function descifrarCesar(textoCifrado, clave) {
        let textoDescifrado = "";
        // Se asegura que la clave sea positiva y esté en rango [0, 25]
        const k = ((clave % ALPHABET_SIZE) + ALPHABET_SIZE) % ALPHABET_SIZE; 
        
        for (let i = 0; i < textoCifrado.length; i++) {
            let caracter = textoCifrado[i];
            let code = caracter.charCodeAt(0);

            // Mayúsculas
            if (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE) {
                let posicionC = code - BASE_UPPER;
                // Fórmula: P = (C - k + 26) mod 26
                let posicionP = (posicionC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
                textoDescifrado += String.fromCharCode(posicionP + BASE_UPPER);
            }
            // Minúsculas
            else if (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE) {
                let posicionC = code - BASE_LOWER;
                let posicionP = (posicionC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
                textoDescifrado += String.fromCharCode(posicionP + BASE_LOWER);
            }
            // Conservar otros caracteres
            else {
                textoDescifrado += caracter;
            }
        }
        return textoDescifrado;
    }

    /** Cifra un texto utilizando el Cifrado Vigenère. */
    function cifrarVigenere(textoPlano, clave) {
        let textoCifrado = "";
        const claveMayus = clave.toUpperCase().replace(/[^A-Z]/g, ''); 
        let indiceClave = 0; 
        
        if (claveMayus.length === 0) {
            throw new Error("La clave de Vigenère no puede estar vacía o contener solo caracteres no alfabéticos.");
        }

        for (let i = 0; i < textoPlano.length; i++) {
            let caracter = textoPlano[i];
            let code = caracter.charCodeAt(0);
            let esMayuscula = (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE);
            let esMinuscula = (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE);

            if (esMayuscula || esMinuscula) {
                let letraClave = claveMayus[indiceClave % claveMayus.length];
                let k = letraClave.charCodeAt(0) - BASE_UPPER; 

                let base = esMayuscula ? BASE_UPPER : BASE_LOWER;
                let posicionP = code - base;
                
                let posicionC = (posicionP + k) % ALPHABET_SIZE;
                textoCifrado += String.fromCharCode(posicionC + base);
                
                indiceClave++;
            } else {
                textoCifrado += caracter;
            }
        }
        return textoCifrado;
    }

    /** Descifra un texto utilizando el Cifrado Vigenère. */
    function descifrarVigenere(textoCifrado, clave) {
        let textoDescifrado = "";
        const claveMayus = clave.toUpperCase().replace(/[^A-Z]/g, ''); 
        let indiceClave = 0; 

        if (claveMayus.length === 0) {
            throw new Error("La clave de Vigenère no puede estar vacía o contener solo caracteres no alfabéticos.");
        }

        for (let i = 0; i < textoCifrado.length; i++) {
            let caracter = textoCifrado[i];
            let code = caracter.charCodeAt(0);
            let esMayuscula = (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE);
            let esMinuscula = (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE);

            if (esMayuscula || esMinuscula) {
                let letraClave = claveMayus[indiceClave % claveMayus.length];
                let k = letraClave.charCodeAt(0) - BASE_UPPER; 

                let base = esMayuscula ? BASE_UPPER : BASE_LOWER;
                let posicionC = code - base;
                
                let posicionP = (posicionC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
                textoDescifrado += String.fromCharCode(posicionP + base);
                
                indiceClave++;
            } else {
                textoDescifrado += caracter; 
            }
        }
        return textoDescifrado;
    }


    // =============================================================================
    // 2. MANEJO DEL DOM Y UTILIDADES
    // =============================================================================

    /** Muestra un mensaje flotante temporal. */
    function mostrarMensaje(msg, type) {
        const mf = document.getElementById('mensajeFlotante');
        mf.textContent = msg;
        
        mf.classList.remove('bg-green-600', 'bg-red-600', 'bg-gray-600', 'opacity-100');
        
        if (type === 'green') {
            mf.classList.add('bg-green-600');
            mf.style.boxShadow = '0 0 10px rgba(0, 255, 0, 0.8)';
        } else if (type === 'red') {
            mf.classList.add('bg-red-600');
            mf.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.8)';
        } else {
            mf.classList.add('bg-gray-600');
            mf.style.boxShadow = '0 0 10px rgba(128, 128, 128, 0.5)';
        }

        mf.classList.remove('hidden', 'opacity-0');
        setTimeout(() => { mf.classList.add('opacity-100'); }, 10); 

        setTimeout(() => {
            mf.classList.remove('opacity-100');
            mf.classList.add('opacity-0');
            setTimeout(() => {
                mf.classList.add('hidden');
                mf.style.boxShadow = 'none';
            }, 300);
        }, 3000);
    }

    /** Muestra el resultado de la operación en el área de salida. */
    function mostrarResultado(mensaje, tipo = 'ok') {
        const outputElement = document.getElementById('resultadoOutput');
        outputElement.style.textShadow = 'none';
        
        // Limpia estilos previos y aplica el estilo de consola base
        outputElement.classList.remove('text-red-500', 'text-yellow-400');
        outputElement.classList.add('text-yellow-400');
        outputElement.style.whiteSpace = 'pre-wrap'; // Por defecto para resultados múltiples
        
        if (tipo === 'error') {
            outputElement.textContent = `// ERROR:: ${mensaje}`;
            outputElement.classList.remove('text-yellow-400');
            outputElement.classList.add('text-red-500');
            outputElement.style.textShadow = '0 0 7px #ef4444';
        } else if (tipo === 'brute-force') {
            // Este modo fue eliminado, pero el código se deja por si acaso
            outputElement.textContent = mensaje;
            outputElement.style.textShadow = '0 0 7px #fafa00';
            outputElement.style.whiteSpace = 'pre'; // Asegura formato de múltiples líneas
        } else { // 'ok' o default
            outputElement.textContent = mensaje;
            outputElement.style.textShadow = '0 0 7px #fafa00';
        }
    }

    /** * Actualiza la interfaz de usuario basándose en el modo y cifrado seleccionados.
     * Ahora solo maneja CIFRAR y DESCIFRAR (Memoria).
     */
    function toggleUIMode() {
        const tipoCifrado = getRadioValue('cifrado');
        const modo = getRadioValue('modo');
        const claveLabel = document.getElementById('claveLabel');
        const claveInput = document.getElementById('claveInput');
        const claveContainer = document.getElementById('claveContainer');
        const entradaContainer = document.getElementById('entradaContainer');
        
        // Se asegura de que el botón de ejecución esté siempre visible (ya que el de Brute Force fue eliminado del HTML)
        
        if (modo === 'descifrar-memoria') {
            // Modo DESCIFRAR: Ocultar la entrada de texto, solo se necesita la clave
            entradaContainer.classList.add('hidden', 'opacity-0');
            claveContainer.classList.remove('hidden', 'opacity-0');
        }
        else { // Modo CIFRAR
            // Mostrar la entrada de texto y la clave
            entradaContainer.classList.remove('hidden', 'opacity-0');
            claveContainer.classList.remove('hidden', 'opacity-0');

            // 2. Actualización de la etiqueta de la clave
            if (tipoCifrado === 'cesar') {
                claveLabel.textContent = "CLAVE: SOLO NÚMEROS ENTEROS (César)";
                claveInput.placeholder = "Clave numérica para César (Ej: 3)";
            } else if (tipoCifrado === 'vigenere') {
                claveLabel.textContent = "CLAVE: SOLO LETRAS (Vigenère)";
                claveInput.placeholder = "Palabra clave para Vigenère (Ej: SECRETO)";
            }
        }
    }

    /** Ejecuta el procedimiento de cifrado/descifrado por memoria. */
    function ejecutarCifrado() {
        const tipoCifrado = getRadioValue('cifrado');
        const modo = getRadioValue('modo');
        let texto = document.getElementById('textoEntrada').value.trim();
        const claveStr = document.getElementById('claveInput').value.trim();

        mostrarResultado('// PROCESANDO...', 'ok');

        let resultado = "";

        try {
            // 1. Manejo del texto de entrada (Si es descifrar, toma de la memoria)
            if (modo === 'descifrar-memoria') {
                if (!_memoriaCifrado) {
                    mostrarResultado("No hay texto cifrado almacenado en [MEMORIA]. Cifra un mensaje primero.", 'error');
                    return;
                }
                texto = _memoriaCifrado;
            } else if (!texto) {
                mostrarResultado("Falta el [TEXTO] de entrada.", 'error');
                return;
            }
            
            // 2. Validación de Clave (Necesaria para ambos modos)
            if (!claveStr) {
                mostrarResultado("Falta la [CLAVE]. Por favor, ingrésala.", 'error');
                return;
            }


            // 3. Ejecución del Cifrado/Descifrado
            if (tipoCifrado === 'cesar') {
                const claveNum = parseInt(claveStr, 10);
                
                if (isNaN(claveNum) || !Number.isInteger(claveNum)) {
                    mostrarResultado("La [CLAVE] para César debe ser un valor numérico entero.", 'error');
                    return;
                }
                
                if (modo === 'cifrar') {
                    resultado = cifrarCesar(texto, claveNum);
                    _memoriaCifrado = resultado; // **GUARDAR EN MEMORIA**
                    mostrarMensaje('Cifrado completado y guardado en memoria.', 'green');
                } else if (modo === 'descifrar-memoria') {
                    resultado = descifrarCesar(texto, claveNum);
                    mostrarMensaje('Descifrado completado. Texto original recuperado.', 'green');
                }
            } 
            else if (tipoCifrado === 'vigenere') {
                if (!/^[a-zA-Z]+$/.test(claveStr)) {
                    mostrarResultado("La [CLAVE] para Vigenère debe contener solo letras (A-Z).", 'error'); 
                    return;
                }
                
                if (modo === 'cifrar') {
                    resultado = cifrarVigenere(texto, claveStr);
                    _memoriaCifrado = resultado; // **GUARDAR EN MEMORIA**
                    mostrarMensaje('Cifrado completado y guardado en memoria.', 'green');
                } else if (modo === 'descifrar-memoria') {
                    resultado = descifrarVigenere(texto, claveStr);
                    mostrarMensaje('Descifrado completado. Texto original recuperado.', 'green');
                }
            }

            mostrarResultado(resultado, 'ok');
            
        } catch (e) {
            console.error("Error en la ejecución:", e);
            mostrarResultado(`EXCEPCIÓN CRÍTICA: ${e.message.toUpperCase()}`, 'error');
            mostrarMensaje('ERROR: Revisa la clave o el texto.', 'red');
        }
    }

    /** Limpia todos los campos y restablece la interfaz. */
    function limpiarTodo() {
        document.getElementById('textoEntrada').value = '';
        document.getElementById('claveInput').value = '';
        _memoriaCifrado = ''; // Limpia la memoria
        mostrarResultado('// ESPERANDO DATOS...', 'ok');
        
        // Restablece los radios a César y Cifrar
        document.querySelector('input[name="cifrado"][value="cesar"]').checked = true;
        document.querySelector('input[name="modo"][value="cifrar"]').checked = true;
        
        // Restablece la UI de clave/botón
        toggleUIMode();

        mostrarMensaje('Memoria y campos ELIMINADOS. Consola reiniciada.', 'gray');
    }

    // Se ejecuta una vez que el DOM está completamente cargado.
    document.addEventListener('DOMContentLoaded', () => {
        // Inicializa la UI al cargar la página
        toggleUIMode();
    });
</script>

</body>
</html>