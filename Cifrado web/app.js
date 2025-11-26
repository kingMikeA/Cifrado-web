// ==========================================================
// VARIABLES GLOBALES Y UTILIDADES
// ==========================================================
const ALPHABET_SIZE = 26;
const A_CODE = 'A'.charCodeAt(0);

let _datosTabla = []; // Para la exportación de la tabla (CSV)
let _memoriaCifrado = ""; // Almacena el último texto cifrado

// Obtener referencias del DOM (asegúrate de que estas IDs coinciden con index.html)
const textoEntrada = document.getElementById('textoEntrada');
const claveInput = document.getElementById('claveInput');
const tablaContainer = document.getElementById('tablaContainer');
const descargarBtn = document.getElementById('descargarBtn');
const resultadoContainer = document.getElementById('resultadoContainer');
const resultadoMensaje = document.getElementById('resultadoMensaje');
const resultadoOutput = document.getElementById('resultadoOutput');

const claveLabel = document.getElementById('claveLabel');
const ejecutarBtn = document.getElementById('ejecutarBtn');
const entradaContainer = document.getElementById('entradaContainer');

/**
 * Obtiene el valor seleccionado de un grupo de radio buttons.
 * @param {string} name Nombre del grupo de radio buttons.
 * @returns {string} Valor seleccionado.
 */
function getRadioValue(name) {
    const radios = document.getElementsByName(name);
    for (const radio of radios) {
        if (radio.checked) {
            return radio.value;
        }
    }
    return '';
}

/**
 * Muestra mensajes de estado y error.
 * @param {string} msg Mensaje a mostrar.
 * @param {string} type Tipo de mensaje ('error', 'success' o 'info').
 */
function mostrarResultado(msg, type) {
    resultadoContainer.classList.remove('hidden');
    resultadoOutput.classList.add('hidden');
    resultadoMensaje.textContent = msg;
    resultadoContainer.className = 'p-4 mt-6 rounded-lg text-sm'; // Reset container styles
    resultadoMensaje.className = 'font-semibold'; // Reset styles

    if (type === 'error') {
        resultadoContainer.classList.add('bg-red-900/20', 'border-red-600');
        resultadoMensaje.classList.add('text-red-400');
    } else if (type === 'success') {
        resultadoContainer.classList.add('bg-green-900/20', 'border-green-600');
        resultadoMensaje.classList.add('text-green-400');
    } else if (type === 'info') {
        resultadoContainer.classList.add('bg-purple-900/20', 'border-purple-600');
        resultadoMensaje.classList.add('text-purple-400');
    }
    
    if (type !== 'success') {
        tablaContainer.innerHTML = ''; // Limpia la tabla
        descargarBtn.classList.add('hidden');
    }
}

/**
 * Muestra un resultado final formateado y el mensaje de éxito.
 * @param {string} msg Mensaje principal.
 * @param {string} outputText El texto final (cifrado/descifrado).
 */
function mostrarMensajeFinal(msg, outputText) {
    mostrarResultado(msg, 'success');
    resultadoOutput.classList.remove('hidden');
    resultadoOutput.textContent = `> ${outputText}`;
}


// ==========================================================
// LÓGICA DE CIFRADO CÉSAR
// ==========================================================

/**
 * Cifra un texto usando el método César y genera los pasos detallados.
 * @param {string} textoPlano Texto a cifrar.
 * @param {number} clave Clave numérica (0-25).
 * @returns {{resultado: string, pasos: Array<Object>}} Resultado y pasos.
 */
function cifrarCesar(textoPlano, clave) {
    let resultado = '';
    const pasos = [];
    const textoUpper = textoPlano.toUpperCase();

    for (let i = 0; i < textoUpper.length; i++) {
        const P_letra = textoUpper[i];

        if (P_letra >= 'A' && P_letra <= 'Z') {
            const P_valor = P_letra.charCodeAt(0) - A_CODE;
            const Suma_PK = P_valor + clave;
            const C_valor_mod = Suma_PK % ALPHABET_SIZE;
            const C_letra = String.fromCharCode(C_valor_mod + A_CODE);

            pasos.push({
                P_letra: P_letra,
                P_valor: P_valor,
                K: clave, // Clave de cifrado
                Suma_PK: Suma_PK,
                C_valor_mod: C_valor_mod,
                C_letra: C_letra,
                // Valores de descifrado (Vacíos para 'cifrar-only' view)
                K_Rep: '',
                Resta_CK: '',
                P_final: ''
            });
            resultado += C_letra;
        } else {
            resultado += P_letra; // Mantener caracteres no alfabéticos
        }
    }

    return { resultado: resultado, pasos: pasos };
}

/**
 * Descifra un texto usando el método César y genera los pasos detallados completos.
 * @param {string} textoCifrado Texto a descifrar.
 * @param {number} clave Clave numérica (0-25).
 * @returns {{resultado: string, pasos: Array<Object>}} Resultado y pasos.
 */
function descifrarCesar(textoCifrado, clave) {
    let resultado = '';
    const pasos = [];
    const textoUpper = textoCifrado.toUpperCase();

    for (let i = 0; i < textoUpper.length; i++) {
        const C_letra = textoUpper[i];

        if (C_letra >= 'A' && C_letra <= 'Z') {
            const C_valor_input = C_letra.charCodeAt(0) - A_CODE;
            const K_descifrado = clave; 
            
            // Cálculo de la resta (C - K) mod 26
            let Resta_CK = C_valor_input - K_descifrado;
            if (Resta_CK < 0) {
                Resta_CK += ALPHABET_SIZE; 
            }

            const P_final_valor = Resta_CK % ALPHABET_SIZE; 
            const P_final = String.fromCharCode(P_final_valor + A_CODE);
            
            pasos.push({
                // Columnas de Cifrado (para tabla completa)
                P_letra: P_final, 
                P_valor: P_final_valor,
                K: clave, 
                Suma_PK: (P_final_valor + clave), 
                C_valor_mod: C_valor_input, 
                C_letra: C_letra,

                // Columnas de Descifrado
                K_Rep: K_descifrado, // K Valor (Descifrado)
                Resta_CK: Resta_CK, // Resta (C-K)
                P_final: P_final, // P Final (Usuario Original)
            });
            resultado += P_final;
        } else {
            resultado += C_letra; 
        }
    }

    return { resultado: resultado, pasos: pasos };
}


// ==========================================================
// LÓGICA DE CIFRADO VIGENÈRE
// ==========================================================

/**
 * Cifra un texto usando el método Vigenère y genera los pasos detallados.
 * @param {string} textoPlano Texto a cifrar.
 * @param {string} clave Clave alfabética.
 * @returns {{resultado: string, pasos: Array<Object>}} Resultado y pasos.
 */
function cifrarVigenere(textoPlano, clave) {
    let resultado = '';
    const pasos = [];
    const textoUpper = textoPlano.toUpperCase();
    let claveIndex = 0;

    for (let i = 0; i < textoUpper.length; i++) {
        const P_letra = textoUpper[i];

        if (P_letra >= 'A' && P_letra <= 'Z') {
            const K_letra = clave[claveIndex % clave.length];
            const P_valor = P_letra.charCodeAt(0) - A_CODE;
            const K_valor = K_letra.charCodeAt(0) - A_CODE;
            
            const Suma = P_valor + K_valor;
            const C_valor_mod = Suma % ALPHABET_SIZE;
            const C_letra = String.fromCharCode(C_valor_mod + A_CODE);

            pasos.push({
                P_letra: P_letra,
                P_valor: P_valor,
                K_letra: K_letra,
                K_valor: K_valor,
                Suma: Suma,
                C_valor_mod: C_valor_mod,
                C_letra: C_letra,
                // Valores de descifrado (Vacíos)
                C_valor_input: '', Resta: '', Resta_Mod: '', P_final: ''
            });
            resultado += C_letra;
            claveIndex++;
        } else {
            resultado += P_letra;
        }
    }
    return { resultado: resultado, pasos: pasos };
}

/**
 * Descifra un texto usando el método Vigenère y genera los pasos detallados completos (12 columnas).
 * @param {string} textoCifrado Texto a descifrar.
 * @param {string} clave Clave alfabética.
 * @returns {{resultado: string, pasos: Array<Object>}} Resultado y pasos.
 */
function descifrarVigenere(textoCifrado, clave) {
    let resultado = '';
    const pasos = [];
    const textoUpper = textoCifrado.toUpperCase();
    let claveIndex = 0;

    for (let i = 0; i < textoUpper.length; i++) {
        const C_letra = textoUpper[i];

        if (C_letra >= 'A' && C_letra <= 'Z') {
            const K_letra = clave[claveIndex % clave.length];
            const C_valor_input = C_letra.charCodeAt(0) - A_CODE; // Valor del caracter Cifrado (Input)
            const K_valor = K_letra.charCodeAt(0) - A_CODE;
            
            // P = (C - K) mod 26
            const Resta = C_valor_input - K_valor;
            
            let Resta_Mod = Resta % ALPHABET_SIZE;
            if (Resta_Mod < 0) {
                Resta_Mod += ALPHABET_SIZE; 
            }
            
            const P_final = String.fromCharCode(Resta_Mod + A_CODE); // P Final (Usuario Original)
            
            pasos.push({
                // Columnas de Cifrado (para tabla completa)
                P_letra: P_final, 
                P_valor: Resta_Mod,
                K_letra: K_letra, 
                K_valor: K_valor,
                Suma: Resta_Mod + K_valor,
                C_valor_mod: C_valor_input, 
                C_letra: C_letra, 
                
                // Columnas de Descifrado
                C_valor_input: C_valor_input, 
                Resta: Resta,
                Resta_Mod: Resta_Mod,
                P_final: P_final
            });
            resultado += P_final;
            claveIndex++;
        } else {
            resultado += C_letra; 
        }
    }
    return { resultado: resultado, pasos: pasos };
}

// ==========================================================
// LÓGICA DE VISUALIZACIÓN Y MANEJO DE LA APP
// ==========================================================

/**
 * Genera la tabla HTML detallada del proceso de cifrado/descifrado y la muestra.
 * @param {Array<Object>} pasos Array de objetos con los pasos.
 * @param {string} resultadoFinal El texto resultante (cifrado o descifrado).
 * @param {string} modo 'cifrar' o 'descifrar-memoria'.
 * @param {string} tipoCifrado 'cesar' o 'vigenere'.
 */
function generarTablaDetalladaHTML(pasos, resultadoFinal, modo, tipoCifrado) {
    const isDescifrando = modo.startsWith('descifrar');

    let fullHeaders, fullDataMap, displayHeaders, displayDataMap;

    if (tipoCifrado === 'vigenere') {
        
        // Estructura COMPLETA de 12 columnas (Cifrado + Descifrado)
        fullHeaders = [
            'P Letra', 'P Valor', 'K Letra', 'K Valor', 'Suma (P+K)', 'C Valor (Mod 26)', 'C Letra', 
            'C Valor (Input)', 'K Valor (Descifrado)', 'Resta (C-K)', 'Suma (Mod 26) solo si hay negativos', 
            'P Final (Usuario Original)'
        ];
        
        fullDataMap = pasos.map(p => {
            return [
                { value: p.P_letra, key: 'P_letra' },       
                { value: p.P_valor, key: 'P_valor' },       
                { value: p.K_letra, key: 'K_letra' },       
                { value: p.K_valor, key: 'K_valor' },       
                { value: p.Suma, key: 'Suma' },             
                { value: p.C_valor_mod, key: 'C_valor_mod' }, 
                { value: p.C_letra, key: 'C_letra' },       
                
                { value: p.C_valor_input || p.C_valor_mod, key: 'C_valor_input' }, 
                { value: p.K_valor, key: 'K_valor_dec' },    
                { value: p.Resta, key: 'Resta' },            
                { value: p.Resta_Mod, key: 'Resta_Mod' },    
                { value: p.P_final, key: 'P_final' }        
            ];
        });

        const cifradoHeaders = ['P Letra', 'P Valor', 'K Letra', 'K Valor', 'Suma (P+K)', 'C Valor (Mod 26)', 'C Letra'];
        const cifradoDataKeys = ['P_letra', 'P_valor', 'K_letra', 'K_valor', 'Suma', 'C_valor_mod', 'C_letra'];

        const datosParaExportar = fullDataMap.map(row => row.map(cell => cell.value));
        _datosTabla = [fullHeaders, ...datosParaExportar];

        if (isDescifrando) {
            displayHeaders = fullHeaders; 
            displayDataMap = fullDataMap;
        } else { 
            displayHeaders = cifradoHeaders; 
            displayDataMap = pasos.map(p => {
                return cifradoDataKeys.map(key => ({ 
                    value: p[key] !== undefined ? p[key] : '', 
                    key: key 
                }));
            });
        }

    } else { // CIFRADO CÉSAR
        
        // Estructura COMPLETA de 10 columnas
        fullHeaders = [
            'P Letra', 'P Valor', 'K Valor (Cifrado)', 'Suma (P+K)', 'C Valor (Mod 26)', 'C Letra', 
            'C Valor (Input)', 'K Valor (Descifrado)', 'Resta (C-K)', 
            'P Final (Usuario Original)' 
        ];

        fullDataMap = pasos.map(p => {
            const C_valor_mod_display = p.C_valor_mod !== undefined ? p.C_valor_mod : (p.C_letra.charCodeAt(0) - A_CODE);
            const C_valor_input_display = isDescifrando ? (p.C_letra.charCodeAt(0) - A_CODE) : p.C_valor_mod;

            return [
                { value: p.P_letra, key: 'P_letra' },     
                { value: p.P_valor, key: 'P_valor' },     
                { value: p.K, key: 'K' },                 
                { value: p.Suma_PK, key: 'Suma_PK' },     
                { value: C_valor_mod_display, key: 'C_valor_mod' }, 
                { value: p.C_letra, key: 'C_letra' },     
                
                { value: C_valor_input_display, key: 'C_valor_input' }, 
                { value: p.K_Rep, key: 'K_Rep' },         
                { value: p.Resta_CK, key: 'Resta_CK' },   
                { value: p.P_final, key: 'P_final' }      
            ];
        });
        
        const cifradoHeaders = ['P Letra', 'P Valor', 'K Valor (Cifrado)', 'Suma (P+K)', 'C Valor (Mod 26)', 'C Letra'];
        const cifradoDataKeys = ['P_letra', 'P_valor', 'K', 'Suma_PK', 'C_valor_mod', 'C_letra'];

        const datosParaExportar = fullDataMap.map(row => row.map(cell => cell.value));
        _datosTabla = [fullHeaders, ...datosParaExportar];

        if (isDescifrando) {
            displayHeaders = fullHeaders; 
            displayDataMap = fullDataMap;
        } else { 
            displayHeaders = cifradoHeaders; 
            displayDataMap = pasos.map(p => {
                return cifradoDataKeys.map(key => ({ 
                    value: p[key] !== undefined ? p[key] : '', 
                    key: key 
                }));
            });
        }
    }

    // 2. GENERACIÓN DEL HTML DE LA TABLA
    const operacionDisplay = isDescifrando ? 'DESCIFRADO COMPLETO' : 'CIFRADO PRINCIPAL';
    const modoDisplay = modo.includes('memoria') ? 'MEMORIA' : 'NUEVO';

    let tablaHTML = `
        <div class="text-xs font-bold text-white mb-4 uppercase tracking-wider">
            [ LOG DE PROCESOS - ${tipoCifrado.toUpperCase()} - ${operacionDisplay} ]
        </div>
        <div class="overflow-x-auto w-full border border-cyan-800 shadow-xl shadow-cyan-900/50">
            <table id="tablaExportable" class="text-sm text-center text-gray-300 w-full">
                <thead class="text-xs uppercase bg-cyan-900/50 text-cyan-300 whitespace-nowrap">
                    <tr>
                        ${displayHeaders.map(h => `<th scope="col" class="py-2 px-3 border border-gray-900">${h}</th>`).join('')}
                    </tr>
                </thead>
                <tbody class="whitespace-nowrap">
                    ${displayDataMap.map(row => {
                        return `
                            <tr class="table-row-style border-b border-gray-900">
                                ${row.map(cell => `
                                    <td class="py-2 px-3 font-mono border border-gray-900">
                                        ${cell.value}
                                    </td>
                                `).join('')}
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        </div>
    `;

    // 3. ACTUALIZAR DOM Y ESTADO
    tablaContainer.innerHTML = tablaHTML;
    descargarBtn.classList.remove('hidden'); 

    // Mostrar resultado en la consola de output
    mostrarMensajeFinal(`Proceso ${isDescifrando ? 'DESCIFRADO' : 'CIFRADO'} completado.`, resultadoFinal);
}


/** Expone la función principal al botón Ejecutar. */
window.ejecutarCifrado = function() {
    try {
        const tipoCifrado = getRadioValue('cifrado');
        const modo = getRadioValue('modo');
        let texto = textoEntrada.value.trim();
        const claveStr = claveInput.value.trim();
        let clave;
        let resultadoObj = { resultado: "", pasos: [] };

        // 1. VALIDACIÓN
        if (modo === 'cifrar' && !texto) {
            mostrarResultado('ERROR: Introduce texto para cifrar.', 'error');
            return;
        }

        // 2. EJECUCIÓN 
        
        if (modo === 'cifrar') {
            // --- MODO CIFRAR (Original) ---
            
            // Validar la clave en modo Cifrar
            if (tipoCifrado === 'cesar') {
                clave = parseInt(claveStr, 10);
                if (isNaN(clave) || clave < 0 || clave > 25) {
                    mostrarResultado('ERROR: Para César, la clave debe ser un número entero en el rango [0, 25].', 'error');
                    return;
                }
                resultadoObj = cifrarCesar(texto, clave);
            } else { // vigenere
                clave = claveStr.toUpperCase().replace(/[^A-Z]/g, '');
                if (!clave) {
                    mostrarResultado('ERROR: Para Vigenère, la clave debe ser una palabra (solo letras).', 'error');
                    return;
                }
                resultadoObj = cifrarVigenere(texto, clave);
            }
            
            // Guardar en memoria el texto cifrado
            _memoriaCifrado = resultadoObj.resultado;
            claveInput.dataset.ultimaClave = claveStr; // Guardar la clave tal como se introdujo
            claveInput.dataset.ultimoCifrado = tipoCifrado;
            
            // Mostrar pasos detallados del cifrado (Solo columnas de Cifrado)
            generarTablaDetalladaHTML(resultadoObj.pasos, resultadoObj.resultado, 'cifrar', tipoCifrado);
            
        } else { // modo === 'descifrar-memoria'
            // --- MODO DESCIFRAR DESDE MEMORIA (Actualizado) ---
            
            if (!_memoriaCifrado) {
                mostrarResultado('ERROR: No hay texto cifrado guardado en la memoria. Cifra un texto primero.', 'error');
                return;
            }
            texto = _memoriaCifrado; // Usamos el texto de la memoria

            // Usar la clave de la interfaz. Si está vacía, intentar usar la última clave guardada.
            let claveDescifrarStr = claveStr || claveInput.dataset.ultimaClave;
            let tipoCifradoMemoria = claveInput.dataset.ultimoCifrado;
            
            if (!claveDescifrarStr) {
                mostrarResultado('ERROR: No se ha encontrado una clave para descifrar. Introduce la clave.', 'error');
                return;
            }

            // Adaptar la clave para la función de descifrado
            if (tipoCifradoMemoria === 'cesar') {
                let claveDescifrar = parseInt(claveDescifrarStr, 10);
                
                // VALIDACIÓN ESTRICTA DEL RANGO DE CLAVE [0, 25] AL DESCIFRAR
                if (isNaN(claveDescifrar) || claveDescifrar < 0 || claveDescifrar > 25) {
                    mostrarResultado('ERROR: La clave de descifrado César debe ser un número positivo en el rango de 0 a 25.', 'error');
                    return;
                }
                
                resultadoObj = descifrarCesar(texto, claveDescifrar);

            } else { // vigenere
                let claveDescifrar = claveDescifrarStr.toUpperCase().replace(/[^A-Z]/g, '');
                if (!claveDescifrar) {
                    mostrarResultado('ERROR: La clave de descifrado Vigenère no es una palabra válida.', 'error');
                    return;
                }
                resultadoObj = descifrarVigenere(texto, claveDescifrar);
            }
            
            // Mostrar pasos detallados del descifrado (Todas las columnas)
            generarTablaDetalladaHTML(resultadoObj.pasos, resultadoObj.resultado, 'descifrar-memoria', tipoCifradoMemoria);
        }

    } catch (e) {
        console.error("Error en ejecutarCifrado:", e);
        mostrarResultado(`Error interno: ${e.message}`, 'error');
    }
}


/** Limpia todos los campos, la memoria y el resultado. */
window.limpiarTodo = function() {
    textoEntrada.value = '';
    claveInput.value = '';
    _memoriaCifrado = '';
    _datosTabla = [];
    claveInput.dataset.ultimaClave = ''; // Limpiar también la última clave guardada
    claveInput.dataset.ultimoCifrado = ''; 
    tablaContainer.innerHTML = '';
    descargarBtn.classList.add('hidden');
    
    // Resetear el modo a Cifrar César y actualizar la UI
    document.querySelector('input[name="cifrado"][value="cesar"]').checked = true;
    document.querySelector('input[name="modo"][value="cifrar"]').checked = true;
    toggleUIMode();

    // Mensaje final de reinicio (Corregido para usar 'info')
    mostrarResultado('// SISTEMA REINICIADO.', 'info');
}


/** Alterna la UI para César vs Vigenère y para Cifrar vs Descifrar-Memoria. */
window.toggleUIMode = function() {
    const tipoCifrado = getRadioValue('cifrado');
    const modo = getRadioValue('modo');
    
    // 1. Ajustar placeholder y label según el tipo de cifrado
    if (tipoCifrado === 'cesar') {
        claveLabel.textContent = 'CLAVE: SOLO NÚMEROS ENTEROS ';
        claveInput.placeholder = 'Clave numérica para César (Rango: 0-25)';
    } else { // vigenere
        claveLabel.textContent = 'CLAVE: SOLO LETRAS ';
        claveInput.placeholder = 'Clave de palabra para Vigenère (Ej: SECRETO)';
    }

    // 2. Ajustar UI según el modo
    if (modo === 'cifrar') {
        ejecutarBtn.textContent = `CIFRAR`;
        // Habilitar la caja de texto y la clave
        entradaContainer.classList.remove('opacity-30', 'pointer-events-none');
        claveInput.disabled = false;
        
        // Estilo de botón - Primario (Morado)
        ejecutarBtn.classList.add('btn-neon-execute');
        ejecutarBtn.classList.remove('btn-neon-descifrar');
    } else { // modo === 'descifrar-memoria'
        ejecutarBtn.textContent = `DESCIFRAR `;
        // Deshabilitar/opacar la caja de texto (se usará la memoria)
        entradaContainer.classList.add('opacity-30', 'pointer-events-none'); 
        
        // La clave se puede introducir manualmente para descifrar.
        claveInput.disabled = false;
        
        // Estilo de botón - Secundario (Verde Azulado)
        ejecutarBtn.classList.remove('btn-neon-execute');
        ejecutarBtn.classList.add('btn-neon-descifrar'); 
    }
}

/**
 * Descarga los datos de la tabla de pasos detallados como un archivo CSV.
 */
window.descargarTablaCSV = function() {
    if (_datosTabla.length === 0) {
        mostrarResultado('ERROR: No hay datos para exportar. Ejecuta una operación primero.', 'error');
        return;
    }

    // Convertir el array de arrays a formato CSV
    // Se utiliza map(e => `"${e}"`) para manejar comas o caracteres especiales dentro de las celdas.
    const csvContent = _datosTabla.map(row => row.map(e => `"${e}"`).join(',')).join('\n');
    
    const tipoCifrado = getRadioValue('cifrado');
    const modo = getRadioValue('modo');
    const filename = `pasos_${tipoCifrado}_${modo}_${new Date().toISOString().slice(0, 10)}.csv`;

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    if (link.download !== undefined) { 
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Inicializar la UI al cargar
document.addEventListener('DOMContentLoaded', () => {
    toggleUIMode();
    mostrarResultado('// CONSOLA INICIADA. Esperando instrucción.', 'info');
});