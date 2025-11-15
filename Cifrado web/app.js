// =============================================================================
// I. CONSTANTES Y VARIABLES GLOBALES
// =============================================================================

const BASE_UPPER = 'A'.charCodeAt(0); // 65
const BASE_LOWER = 'a'.charCodeAt(0); // 97
const ALPHABET_SIZE = 26; // 26 letras en el alfabeto

// ** VARIABLE DE MEMORIA GLOBAL **
let _memoriaCifrado = ""; 
let _datosTabla = []; // Almacena los datos detallados de la última operación para exportar a Excel

// ** ELEMENTOS DEL DOM (para fácil acceso)**
const textoEntrada = document.getElementById('textoEntrada');
const claveInput = document.getElementById('claveInput');
const resultadoOutput = document.getElementById('resultadoOutput');
const tablaContainer = document.getElementById('tablaResultadoContainer');
const descargarBtn = document.getElementById('descargarBtn');


// =============================================================================
// II. LÓGICA DE CIFRADO Y RECOLECCIÓN DE DATOS
// =============================================================================

/** Obtiene el valor del radio button seleccionado por su nombre. */
function getRadioValue(name) {
    const selector = `input[name="${name}"]:checked`; 
    const element = document.querySelector(selector);
    return element ? element.value : null;
}

/** Cifra un texto utilizando el Cifrado César y devuelve los pasos detallados. */
function cifrarCesar(textoPlano, clave) {
    let textoCifrado = "";
    const k = clave % ALPHABET_SIZE; 
    const pasosDetallados = []; // Array para guardar cada paso
    
    for (let i = 0; i < textoPlano.length; i++) {
        let caracter = textoPlano[i];
        let code = caracter.charCodeAt(0);
        let letraCifrada = caracter;
        let valorP = null;
        let valorC = null;
        let esLetra = false;

        // Mayúsculas
        if (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE) {
            valorP = code - BASE_UPPER;
            valorC = (valorP + k) % ALPHABET_SIZE;
            letraCifrada = String.fromCharCode(valorC + BASE_UPPER);
            esLetra = true;
        }
        // Minúsculas
        else if (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE) {
            valorP = code - BASE_LOWER;
            valorC = (valorP + k) % ALPHABET_SIZE;
            letraCifrada = String.fromCharCode(valorC + BASE_LOWER);
            esLetra = true;
        }
        
        textoCifrado += letraCifrada;
        
        // Registro del paso (solo si es letra)
        if (esLetra) {
             pasosDetallados.push({
                original: caracter.toUpperCase(),
                valorOriginal: valorP,
                claveLetra: 'K',
                claveValor: k,
                suma: valorP + k,
                valorMod26: valorC,
                cifrada: letraCifrada.toUpperCase(),
                descifradoValor: null, 
                descifrada: null
            });
        }
    }
    // Devolver objeto con resultado y pasos
    return { resultado: textoCifrado, pasos: pasosDetallados };
}

/** Descifra un texto utilizando el Cifrado César y devuelve los pasos detallados. */
function descifrarCesar(textoCifrado, clave) {
    let textoDescifrado = "";
    const k = ((clave % ALPHABET_SIZE) + ALPHABET_SIZE) % ALPHABET_SIZE; 
    const pasosDetallados = [];
    
    for (let i = 0; i < textoCifrado.length; i++) {
        let caracter = textoCifrado[i];
        let code = caracter.charCodeAt(0);
        let letraDescifrada = caracter;
        let valorC = null;
        let valorP = null;
        let esLetra = false;

        // Mayúsculas
        if (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE) {
            valorC = code - BASE_UPPER;
            valorP = (valorC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
            letraDescifrada = String.fromCharCode(valorP + BASE_UPPER);
            esLetra = true;
        }
        // Minúsculas
        else if (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE) {
            valorC = code - BASE_LOWER;
            valorP = (valorC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
            letraDescifrada = String.fromCharCode(valorP + BASE_LOWER);
            esLetra = true;
        }
        
        textoDescifrado += letraDescifrada;
        
        // Registro del paso
        if (esLetra) {
             pasosDetallados.push({
                original: caracter.toUpperCase(), // Letra Cifrada (Entrada)
                valorOriginal: valorC, // Valor de la Cifrada
                claveLetra: 'K',
                claveValor: k,
                suma: valorC - k, // Se registra la resta (C - K)
                valorMod26: valorP, // P = (C - K + 26) mod 26
                cifrada: caracter.toUpperCase(), // La letra cifrada de entrada
                descifradoValor: valorP, 
                descifrada: letraDescifrada.toUpperCase()
            });
        }
    }
    // Devolver objeto con resultado y pasos
    return { resultado: textoDescifrado, pasos: pasosDetallados };
}

/** Cifra un texto utilizando el Cifrado Vigenère y devuelve los pasos detallados. */
function cifrarVigenere(textoPlano, clave) {
    let textoCifrado = "";
    const claveMayus = clave.toUpperCase().replace(/[^A-Z]/g, ''); 
    let indiceClave = 0; 
    const pasosDetallados = [];
    
    if (claveMayus.length === 0) {
        throw new Error("La clave de Vigenère no puede estar vacía o contener solo caracteres no alfabéticos.");
    }

    for (let i = 0; i < textoPlano.length; i++) {
        let caracter = textoPlano[i];
        let code = caracter.charCodeAt(0);
        let letraCifrada = caracter;
        let valorP = null;
        let valorC = null;
        let esMayuscula = (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE);
        let esMinuscula = (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE);

        if (esMayuscula || esMinuscula) {
            let letraClave = claveMayus[indiceClave % claveMayus.length];
            let k = letraClave.charCodeAt(0) - BASE_UPPER; 
            let base = esMayuscula ? BASE_UPPER : BASE_LOWER;
            
            valorP = code - base;
            valorC = (valorP + k) % ALPHABET_SIZE;
            letraCifrada = String.fromCharCode(valorC + base);
            
            // Registro del paso
             pasosDetallados.push({
                original: caracter.toUpperCase(),
                valorOriginal: valorP,
                claveLetra: letraClave,
                claveValor: k,
                suma: valorP + k,
                valorMod26: valorC,
                cifrada: letraCifrada.toUpperCase(),
                descifradoValor: null, 
                descifrada: null
            });
            
            indiceClave++;
        }
        textoCifrado += letraCifrada;
    }
    return { resultado: textoCifrado, pasos: pasosDetallados };
}

/** Descifra un texto utilizando el Cifrado Vigenère y devuelve los pasos detallados. */
function descifrarVigenere(textoCifrado, clave) {
    let textoDescifrado = "";
    const claveMayus = clave.toUpperCase().replace(/[^A-Z]/g, ''); 
    let indiceClave = 0; 
    const pasosDetallados = [];

    if (claveMayus.length === 0) {
        throw new Error("La clave de Vigenère no puede estar vacía o contener solo caracteres no alfabéticos.");
    }

    for (let i = 0; i < textoCifrado.length; i++) {
        let caracter = textoCifrado[i];
        let code = caracter.charCodeAt(0);
        let letraDescifrada = caracter;
        let valorC = null;
        let valorP = null;
        let esMayuscula = (code >= BASE_UPPER && code < BASE_UPPER + ALPHABET_SIZE);
        let esMinuscula = (code >= BASE_LOWER && code < BASE_LOWER + ALPHABET_SIZE);

        if (esMayuscula || esMinuscula) {
            let letraClave = claveMayus[indiceClave % claveMayus.length];
            let k = letraClave.charCodeAt(0) - BASE_UPPER; 
            let base = esMayuscula ? BASE_UPPER : BASE_LOWER;
            
            valorC = code - base;
            valorP = (valorC - k + ALPHABET_SIZE) % ALPHABET_SIZE; 
            letraDescifrada = String.fromCharCode(valorP + base);
            
            // Registro del paso
             pasosDetallados.push({
                original: caracter.toUpperCase(), // Letra Cifrada (Entrada)
                valorOriginal: valorC, // Valor de la Cifrada
                claveLetra: letraClave,
                claveValor: k,
                suma: valorC - k, // Se registra la resta (C - K)
                valorMod26: valorP, // P = (C - K + 26) mod 26
                cifrada: caracter.toUpperCase(), // La letra cifrada de entrada
                descifradoValor: valorP, 
                descifrada: letraDescifrada.toUpperCase()
            });

            indiceClave++;
        }
        textoDescifrado += letraDescifrada; 
    }
    return { resultado: textoDescifrado, pasos: pasosDetallados };
}


// =============================================================================
// III. MANEJO DEL DOM, TABLA Y EXPORTACIÓN
// =============================================================================

/** Muestra un mensaje flotante temporal. (SIN CAMBIOS) */
function mostrarMensaje(msg, type) {
    const mf = document.getElementById('mensajeFlotante');
    mf.textContent = msg;
    
    mf.classList.remove('bg-green-600', 'bg-red-600', 'bg-gray-600', 'opacity-100');
    
    if (type === 'green') {
        mf.classList.add('bg-green-600');
        mf.style.boxShadow = '0 0 10px rgba(0, 255, 0, 0.8)';
    } else if (type === 'red') {
        mf.classList.add('bg-red-600');
        mf.style.boxShadow = '0 0 10px rgba(251, 255, 255, 0.8)';
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

/** Muestra el resultado simple (Solo para errores o al limpiar). (SIN CAMBIOS) */
function mostrarResultado(mensaje, tipo = 'ok') {
    resultadoOutput.classList.remove('hidden'); // Asegura que el <pre> esté visible si es un error
    tablaContainer.innerHTML = ''; // Limpia la tabla
    descargarBtn.classList.add('hidden'); // Oculta descarga
    
    resultadoOutput.style.textShadow = 'none';
    resultadoOutput.classList.remove('text-red-500', 'text-yellow-400');
    resultadoOutput.classList.add('text-yellow-400');
    resultadoOutput.style.whiteSpace = 'pre-wrap';
    
    if (tipo === 'error') {
        resultadoOutput.textContent = `// ERROR:: ${mensaje}`;
        resultadoOutput.classList.remove('text-yellow-400');
        resultadoOutput.classList.add('text-red-500');
        resultadoOutput.style.textShadow = '0 0 7px #ef4444';
    } else { // 'ok' o default
        resultadoOutput.textContent = mensaje;
        resultadoOutput.style.textShadow = '0 0 7px #fafa00';
    }
}

/** * FUNCIÓN FINAL: Genera y muestra la tabla detallada letra por letra.
 * La estructura se adapta a los diseños específicos y nombres exactos de César y Vigenère.
 */
function generarTablaDetalladaHTML(pasos, resultadoFinal, operacion, tipoCifrado) {
    // Verificar si hay pasos válidos para generar la tabla
    if (pasos.length === 0) {
        mostrarResultado(`El texto ingresado solo contiene caracteres no alfabéticos.`, 'error');
        return;
    }

    // Ocultar el resultado simple <pre>
    resultadoOutput.classList.add('hidden');
    
    let headers = [];
    let datosTablaHtml = [];

    // =========================================================================
    // 1. DEFINICIÓN DE ESTRUCTURA Y DATOS
    // =========================================================================

    if (tipoCifrado === 'cesar') {
        // Estructura de César (Basado en image_bbb7be.png) - 9 columnas
        headers = [
            'Usuario original', 'Valor', 'Clave', 'Suma', 'Mensaje de cifrado', 
            'valor', 'Clave', 'Resta', 'Mensaje original'
        ];
        
        datosTablaHtml = pasos.map(p => {
            // Se asume que el objeto 'p' contiene la información completa 
            // de cifrado (cifrada, valorMod26) y descifrado (descifradoValor, descifrada).

            return [
                // Lado Cifrado (Columnas 1-5)
                p.original,             // 1. Usuario original (letra P)
                p.valorOriginal,        // 2. Valor (valor de P)
                p.claveValor,           // 3. Clave (valor de K)
                p.suma,                 // 4. Suma (P + K)
                p.cifrada,              // 5. Mensaje de cifrado (letra C)
                
                // Lado Descifrado (Columnas 6-9)
                p.valorMod26,           // 6. valor (valor de C)
                p.claveValor,           // 7. Clave (valor de K)
                p.descifradoValor,      // 8. Resta (El valor de P después de C - K)
                p.descifrada            // 9. Mensaje original (letra P)
            ];
        });

    } else if (tipoCifrado === 'vigenere') {
        // Estructura de Vigenère (Basado en image_bade5e.png) - 12 columnas
        headers = [
            'Mensaje original', 'Valor', 'KEY', 'Clave Valor', 'Suma', 'Mod 26', 'Mensaje cifrado', 
            'clave', 'Resta', 'Modulo', 'SUMA', 'Descifrado'
        ];
        
        datosTablaHtml = pasos.map(p => {
            // Se asume que el objeto 'p' contiene todos los pasos intermedios para Vigenère
            
            return [
                // Lado Cifrado (Columnas 1-7)
                p.original,        // 1. Mensaje original
                p.valorOriginal,   // 2. Valor
                p.claveLetra,      // 3. KEY
                p.claveValor,      // 4. Clave Valor
                p.suma,            // 5. Suma (P + K)
                p.valorMod26,      // 6. Mod 26 (Valor de C)
                p.cifrada,         // 7. Mensaje cifrado
                
                // Lado Descifrado (Columnas 8-12)
                p.claveLetra,      // 8. clave (letra de la clave)
                p.suma,            // 9. Resta (C - K) - Se usa el valor almacenado en p.suma, asumiendo que el backend lo reutiliza.
                ALPHABET_SIZE,     // 10. Modulo (siempre 26)
                p.descifradoValor, // 11. SUMA (El valor de P)
                p.descifrada       // 12. Descifrado (la letra final)
            ];
        });
    }

    // 2. Almacenar datos para Excel
    _datosTabla = [headers].concat(datosTablaHtml); 
    
    // 3. CONSTRUCCIÓN DEL HTML
    
    // Contenedor con scroll si es muy largo
    let html = `<div class="max-h-80 overflow-y-auto w-full"><table id="tablaResultado" class="w-full text-left border-collapse rounded-md overflow-hidden shadow-lg border border-purple-800">`;
    
    // Encabezados
    html += '<thead><tr class="bg-purple-800 text-yellow-400 text-sm uppercase sticky top-0">';
    headers.forEach(h => {
        // Ajuste visual de columnas para que quepan (min-w y salto de línea)
        html += `<th class="p-2 border-b border-purple-700 min-w-[50px]">${h.replace(' ', '<br>')}</th>`;
    });
    html += '</tr></thead>';

    // Cuerpo (las filas de datos)
    html += '<tbody>';
    datosTablaHtml.forEach(fila => {
        html += `<tr class="bg-gray-900 text-gray-200 text-xl hover:bg-gray-800 transition duration-150">`;
        fila.forEach((dato, index) => {
            let estilo = '';
            
            if (tipoCifrado === 'cesar') {
                // Columna de salida clave: Mensaje de cifrado (index 4) y Mensaje original (index 8)
                if (index === 4 || index === 8) { estilo = 'text-red-400 font-bold'; }
            } else if (tipoCifrado === 'vigenere') {
                 // Columna de salida clave: Mensaje cifrado (index 6) y Descifrado (index 11)
                 if (index === 6 || index === 11) { estilo = 'text-red-400 font-bold'; }
            }

            html += `<td class="p-2 border-b border-purple-900 break-words ${estilo}">${dato === null ? '-' : dato}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table></div>';

    // Mostrar el resultado final debajo de la tabla
    html += `<p class="mt-4 text-xl text-yellow-400">RESULTADO FINAL: <span class="text-red-400 font-bold">${resultadoFinal}</span></p>`;
    
    tablaContainer.innerHTML = html;
    
    // Mostrar el botón de descarga
    descargarBtn.classList.remove('hidden');
}
/** * NUEVA FUNCIÓN: Exporta los datos almacenados en _datosTabla a un archivo Excel (.xlsx) 
 * Carga dinámicamente las librerías necesarias.
 */
function exportarTablaAExcel() {
    if (_datosTabla.length <= 1) { // 1 porque la fila 0 es de encabezados
        mostrarMensaje('No hay datos válidos para exportar.', 'red');
        return;
    }

    // Cargar librerías CDN
    const cdnXLSX = "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js";
    const cdnFileSaver = "https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js";

    // Función para asegurar que un script se carga antes de continuar
    function loadScript(url, callback) {
        if (document.querySelector(`script[src="${url}"]`)) {
            callback();
            return;
        }
        const script = document.createElement('script');
        script.src = url;
        script.onload = callback;
        document.head.appendChild(script);
    }

    mostrarMensaje('Preparando descarga...', 'gray');

    loadScript(cdnXLSX, () => {
        loadScript(cdnFileSaver, () => {
            if (typeof XLSX === 'undefined' || typeof saveAs === 'undefined') {
                mostrarMensaje('Error: Librerías de Excel no cargadas. Intenta de nuevo.', 'red');
                return;
            }
            
            // Usar _datosTabla que ya tiene el formato AoA (Array of Arrays)
            const ws = XLSX.utils.aoa_to_sheet(_datosTabla);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "PasosCifrado");
            
            // Generar el archivo binario
            const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });

            // Función auxiliar para convertir String a ArrayBuffer
            function s2ab(s) {
                const buf = new ArrayBuffer(s.length);
                const view = new Uint8Array(buf);
                for (let i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
                return buf;
            }

            saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), 'Resultado_Cifrado_Detallado.xlsx');
            mostrarMensaje('Tabla descargada con éxito.', 'green');
        });
    });
}


/** Actualiza la interfaz de usuario basándose en el modo y cifrado seleccionados. (SIN CAMBIOS) */
function toggleUIMode() {
    const tipoCifrado = getRadioValue('cifrado');
    const modo = getRadioValue('modo');
    const claveLabel = document.getElementById('claveLabel');
    const claveInput = document.getElementById('claveInput');
    const claveContainer = document.getElementById('claveContainer');
    const entradaContainer = document.getElementById('entradaContainer');
    
    if (modo === 'descifrar-memoria') {
        entradaContainer.classList.add('hidden', 'opacity-0');
        claveContainer.classList.remove('hidden', 'opacity-0');
    }
    else { 
        entradaContainer.classList.remove('hidden', 'opacity-0');
        claveContainer.classList.remove('hidden', 'opacity-0');

        if (tipoCifrado === 'cesar') {
            claveLabel.textContent = "CLAVE: SOLO NÚMEROS ENTEROS (César)";
            claveInput.placeholder = "Clave numérica para César (Ej: 3)";
        } else if (tipoCifrado === 'vigenere') {
            claveLabel.textContent = "CLAVE: SOLO LETRAS (Vigenère)";
            claveInput.placeholder = "Palabra clave para Vigenère (Ej: SECRETO)";
        }
    }
}

/** Ejecuta el procedimiento de cifrado/descifrado por memoria. (AJUSTADO PARA LA TABLA DETALLADA) */
function ejecutarCifrado() {
    const tipoCifrado = getRadioValue('cifrado');
    const modo = getRadioValue('modo');
    let texto = textoEntrada.value.trim();
    const claveStr = claveInput.value.trim();

    mostrarResultado('// PROCESANDO...', 'ok');

    let resultadoObj;

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
        
        // 2. Validación de Clave
        if (!claveStr) {
            mostrarResultado("Falta la [CLAVE]. Por favor, ingrésala.", 'error');
            return;
        }


        // 3. Ejecución del Cifrado/Descifrado (CAPTURA DEL OBJETO DE RESULTADO)
        if (tipoCifrado === 'cesar') {
            const claveNum = parseInt(claveStr, 10);
            
            if (isNaN(claveNum) || !Number.isInteger(claveNum)) {
                mostrarResultado("La [CLAVE] para César debe ser un valor numérico entero.", 'error');
                return;
            }
            
            if (modo === 'cifrar') {
                resultadoObj = cifrarCesar(texto, claveNum);
                _memoriaCifrado = resultadoObj.resultado; // **GUARDAR EN MEMORIA**
                mostrarMensaje('Cifrado completado y guardado en memoria.', 'green');
            } else if (modo === 'descifrar-memoria') {
                resultadoObj = descifrarCesar(texto, claveNum);
                mostrarMensaje('Descifrado completado. Texto original recuperado.', 'green');
            }
        } 
        else if (tipoCifrado === 'vigenere') {
            if (!/^[a-zA-Z]+$/.test(claveStr)) {
                mostrarResultado("La [CLAVE] para Vigenère debe contener solo letras (A-Z).", 'error'); 
                return;
            }
            
            if (modo === 'cifrar') {
                resultadoObj = cifrarVigenere(texto, claveStr);
                _memoriaCifrado = resultadoObj.resultado; // **GUARDAR EN MEMORIA**
                mostrarMensaje('Cifrado completado y guardado en memoria.', 'green');
            } else if (modo === 'descifrar-memoria') {
                resultadoObj = descifrarVigenere(texto, claveStr);
                mostrarMensaje('Descifrado completado. Texto original recuperado.', 'green');
            }
        }
        
        // 4. GENERAR LA TABLA DETALLADA
        const operacion = modo === 'cifrar' ? 'CIFRADO' : 'DESCIFRADO';
        generarTablaDetalladaHTML(resultadoObj.pasos, resultadoObj.resultado, operacion, tipoCifrado);

    } catch (e) {
        console.error("Error en la ejecución:", e);
        mostrarResultado(`EXCEPCIÓN CRÍTICA: ${e.message.toUpperCase()}`, 'error');
        mostrarMensaje('ERROR: Revisa la clave o el texto.', 'red');
    }
}

/** Limpia todos los campos y restablece la interfaz. (AJUSTADO PARA LA TABLA) */
function limpiarTodo() {
    textoEntrada.value = '';
    claveInput.value = '';
    _memoriaCifrado = ''; 
    _datosTabla = []; // Limpia los datos de la tabla

    // Limpieza de UI de tabla/resultado
    tablaContainer.innerHTML = '';
    resultadoOutput.classList.remove('hidden');
    descargarBtn.classList.add('hidden');
    mostrarResultado('// ESPERANDO DATOS...', 'ok');
    
    // Restablece los radios a César y Cifrar
    document.querySelector('input[name="cifrado"][value="cesar"]').checked = true;
    document.querySelector('input[name="modo"][value="cifrar"]').checked = true;
    
    // Restablece la UI de clave/botón
    toggleUIMode();

    mostrarMensaje('Memoria y campos ELIMINADOS. Consola reiniciada.', 'gray');
}

// Inicialización de la UI al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    toggleUIMode();
});