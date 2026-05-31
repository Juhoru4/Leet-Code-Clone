// Backend inyecta el ID del problema en el HTML.
const PROBLEMA_ID = window.PROBLEMA_ID;

    let codigoBasePorLenguaje = {};
    let codigoBaseActual = null;

    //cuando termina de cargar la página, pedimos los datos del problema y los casos de prueba
    window.addEventListener('DOMContentLoaded', () => {
        cargarProblema();
        cargarCasosPrueba();
        const selector = document.getElementById('selector-lenguaje');
        selector.addEventListener('change', () => {
            aplicarCodigoBase(selector.value);
        });
    });

    function aplicarCodigoBase(lenguaje) {
        const editor = document.getElementById('editor');
        const nuevoCodigo = codigoBasePorLenguaje[lenguaje] || '';

        if (!editor) return;

        if (!editor.value.trim() || editor.value === codigoBaseActual) {
            editor.value = nuevoCodigo;
            codigoBaseActual = nuevoCodigo;
        }
    }

    async function cargarProblema() {
        try {
            // Llamada a la API para obtener el enunciado completo del problema.
            const res = await fetch('/api/problems/' + encodeURIComponent(PROBLEMA_ID));
            if (!res.ok) throw new Error('No se pudo obtener el problema');
            const p = await res.json();

            // Con los datos de la API llenamos el panel izquierdo de la vista.
            document.getElementById('titulo-problema').textContent = p.titulo || 'Sin título';
            document.getElementById('descripcion').innerHTML = p.descripcion || '';
            document.getElementById('categoria').textContent = p.categoria || '—';
            document.getElementById('dificultad').textContent = (p.dificultad || '—');
            document.getElementById('restricciones').textContent = p.restricciones || '—';
            document.getElementById('ejemplo_entrada').textContent = p.ejemplo_entrada || '—';
            document.getElementById('ejemplo_salida').textContent = p.ejemplo_salida || '—';

            codigoBasePorLenguaje = {
                python: p.codigo_base_python || '',
                java: p.codigo_base_java || '',
                cpp: p.codigo_base_cpp || '',
            };

            aplicarCodigoBase(document.getElementById('selector-lenguaje').value);

        } catch (err) {
            // Si falla la API, mostramos un estado de error legible en vez de dejar la vista vacía.
            document.getElementById('titulo-problema').textContent = 'No se encontró el problema';
            document.getElementById('descripcion').textContent = '';
        }
    }

    async function cargarCasosPrueba() {
        const contenedor = document.getElementById('casos-prueba-lista');
        try {
            // Esta ruta entrega los casos públicos que se usan para validar la solución.
            const res = await fetch('/api/problems/' + encodeURIComponent(PROBLEMA_ID) + '/test-cases');
            if (!res.ok) throw new Error('No se pudieron cargar los casos');
            const data = await res.json();
            const casos = data.casos || [];

            // Si no hay casos, informamos explícitamente al usuario.
            if (!casos.length) {
                contenedor.textContent = 'No hay casos de prueba públicos para este problema.';
                return;
            }

            // Renderizamos cada caso en HTML para que el usuario pueda revisar entradas y salidas esperadas.
            contenedor.innerHTML = casos.map((caso) => `
                <div class="caso-item">
                    <strong>${caso.descripcion || ('Caso ' + caso.orden)}</strong>
                    <div><b>Entrada:</b></div>
                    <pre>${caso.entrada || '—'}</pre>
                    <div><b>Salida esperada:</b></div>
                    <pre>${caso.salida_esperada || '—'}</pre>
                </div>
            `).join('');
        } catch (err) {
            contenedor.textContent = 'No se pudieron cargar los casos de prueba.';
        }
    }

    async function probar() {
        const codigo = document.getElementById("editor").value;
        const lenguaje = document.getElementById("selector-lenguaje").value;
        const btn = document.getElementById("btn-probar");
        const resultadoDiv = document.getElementById("resultado");
        const estadoDiv = document.getElementById("estado-ejecucion");

        if (!codigo.trim()) {
            resultadoDiv.className = "advertencia";
            resultadoDiv.textContent = "⚠ Escribe algún código antes de probar.";
            return;
        }

        btn.disabled = true;
        btn.textContent = "⏳ Probando...";
        estadoDiv.className = "ejecutando";
        estadoDiv.textContent = "Ejecutando contra casos de prueba...";
        resultadoDiv.className = "";
        resultadoDiv.textContent = "";

        try {
            const response = await fetch("/api/submissions/preview", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    problema_id: PROBLEMA_ID,
                    language: lenguaje,
                    source_code: codigo
                })
            });

            const resultado = await response.json();
                if (!response.ok) {
                    estadoDiv.className = "error";
                    estadoDiv.textContent = resultado.error || "No se pudo probar.";
                    return;
                }

            estadoDiv.className = "correcto";
            estadoDiv.textContent = `Pruebas completadas: ${resultado.casos_pasados}/${resultado.total_casos} aprobados.`;
            mostrarResultado(resultado);

        } 
        
        catch (e) {
            estadoDiv.className = "error";
            estadoDiv.textContent = "❌ No se pudo conectar con el servidor.";
        } 

        finally {
            btn.disabled = false;
            btn.textContent = "🧪 Probar previo a envío";
        }
}

    async function ejecutar() {
        // Tomamos el código escrito por el usuario y el lenguaje seleccionado.
        const codigo = document.getElementById("editor").value;
        const lenguaje = document.getElementById("selector-lenguaje").value;
        const btn = document.getElementById("btn-ejecutar");
        const resultadoDiv = document.getElementById("resultado");
        const estadoDiv = document.getElementById("estado-ejecucion");

        // Evitamos hacer una llamada vacía al backend.
        if (!codigo.trim()) {
            resultadoDiv.className = "advertencia";
            resultadoDiv.textContent = "⚠ Escribe algún código antes de ejecutar.";
            return;
        }

        // Deshabilitamos el botón mientras corre la evaluación para evitar múltiples envíos.
        btn.disabled = true;
        btn.textContent = "⏳ Evaluando...";
        estadoDiv.className = "ejecutando";
        estadoDiv.textContent = "Ejecutando contra casos de prueba...";
        resultadoDiv.className = "";
        resultadoDiv.textContent = "";

        try {
            // Esta es la llamada clave: enviamos código + lenguaje al endpoint de pruebas.
            const response = await fetch("/api/submissions/test-run", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    problema_id: PROBLEMA_ID,
                    language: lenguaje,
                    source_code: codigo
                })
            });

            // Si el backend detecta que el usuario ya tiene una ejecución en curso,
            // respondemos con un mensaje específico para no confundirlo con un error genérico.
            if (response.status === 409) {
                const conflicto = await response.json();
                estadoDiv.className = "advertencia";
                estadoDiv.textContent = "Ya hay una ejecución en curso para este usuario.";
                resultadoDiv.className = "advertencia";
                resultadoDiv.textContent = conflicto.error || "Ya hay una ejecución en curso.";
                return;
            }

            // Convertimos la respuesta JSON en una estructura que luego renderiza mostrarResultado().
            const resultado = await response.json();
            if (!response.ok) {
                estadoDiv.className = "error";
                estadoDiv.textContent = resultado.error || "No se pudo evaluar el código.";
                resultadoDiv.className = "error";
                resultadoDiv.textContent = resultado.error || "No se pudo evaluar el código.";
                return;
            }

            // Si todo salió bien, resumimos cuántas pruebas pasaron.
            estadoDiv.className = "correcto";
            estadoDiv.textContent = `Pruebas completadas: ${resultado.casos_pasados}/${resultado.total_casos} aprobados.`;
            mostrarResultado(resultado);

            // Solo habilitamos el envío final si la solución aprobó todos los casos.
            const btnEnviar = document.getElementById('btn-enviar');
            if (resultado.casos_pasados === resultado.total_casos) {
                btnEnviar.style.display = 'inline-block';
                btnEnviar.disabled = false;
                // Guardamos el resultado para reutilizarlo al confirmar el envío.
                btnEnviar.dataset.payload = JSON.stringify(resultado);
            } else {
                btnEnviar.style.display = 'none';
            }

        } catch (e) {
            // Si falla la red o el backend, mostramos un error de conexión claro.
            estadoDiv.className = "error";
            estadoDiv.textContent = "No se pudo completar la evaluación.";
            resultadoDiv.className = "error";
            resultadoDiv.textContent = "❌ No se pudo conectar con el servidor.";
        } finally {
            // Rehabilitamos el botón siempre, haya funcionado o no.
            btn.disabled = false;
            btn.textContent = "▶ Ejecutar";
        }
    }

    async function enviarIntento() {
        // Reutilizamos el resultado previo de la prueba para enviar solo si fue aprobado.
        const btn = document.getElementById('btn-enviar');
        const estadoDiv = document.getElementById('estado-ejecucion');
        const resultadoDiv = document.getElementById('resultado');

        const payload = btn.dataset.payload ? JSON.parse(btn.dataset.payload) : null;
        if (!payload) {
            estadoDiv.className = 'error';
            estadoDiv.textContent = 'No hay resultados para enviar.';
            return;
        }

        // Bloqueamos el botón mientras se persiste el intento.
        btn.disabled = true;
        btn.textContent = '📤 Enviando...';

        try {
            // Este endpoint guarda el intento ya validado y lo asocia al usuario autenticado.
            const response = await fetch('/api/submissions/submit', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problema_id: PROBLEMA_ID,
                    language: document.getElementById('selector-lenguaje').value,
                    source_code: document.getElementById('editor').value,
                    resultados: payload.resultado || payload.result
                })
            });

            // El backend confirma si el guardado fue correcto o devuelve un mensaje de error.
            const data = await response.json();
            if (!response.ok) {
                estadoDiv.className = 'error';
                estadoDiv.textContent = data.error || 'No se pudo enviar el intento.';
                resultadoDiv.className = 'error';
                resultadoDiv.textContent = data.error || 'No se pudo enviar el intento.';
                return;
            }

            // Si el envío se guardó, ocultamos el botón para evitar duplicados.
            estadoDiv.className = 'correcto';
            estadoDiv.textContent = 'Intento enviado correctamente.';
            resultadoDiv.className = 'correcto';
            resultadoDiv.textContent = '✅ Envío guardado: ' + (data.submission_id || 'ok');
            btn.style.display = 'none';

        } catch (err) {
            // Error de red o servidor al intentar persistir el envío.
            estadoDiv.className = 'error';
            estadoDiv.textContent = 'Error enviando el intento.';
            resultadoDiv.className = 'error';
            resultadoDiv.textContent = 'No se pudo conectar con el servidor.';
        } finally {
            // Dejamos el botón listo por si el usuario vuelve a intentar.
            btn.disabled = false;
            btn.textContent = '📤 Enviar intento';
        }
    }

    function mostrarResultado(resultado) {
        // Esta función traduce la respuesta del backend a un mensaje legible en pantalla.
        const div = document.getElementById("resultado");

        // Ordenamos los casos especiales primero: timeout, compilación, ejecución o error del sistema.
        if (resultado.timeout || resultado.supero_tiempo_limite) {
            div.className = "advertencia";
            div.textContent = "⏱ Tiempo límite excedido. Revisa si tienes un bucle infinito.";
        } else if (resultado.tipo_error === "compilacion") {
            div.className = "error";
            div.textContent = "🔴 Error de compilación:\n\n" + (resultado.stderr || resultado.error || '');
        } else if (resultado.tipo_error === "ejecucion") {
            div.className = "error";
            div.textContent = "🟠 Error de ejecución:\n\n" + (resultado.stderr || resultado.error || '');
        } else if (resultado.tipo_error === "sistema") {
            div.className = "error";
            div.textContent = "⚙️ " + (resultado.stderr || resultado.error || '');
        } else if (Array.isArray(resultado.resultado)) {
            // Si el backend devuelve un desglose por caso, lo mostramos caso por caso.
            let html = "";
            for (const caso of resultado.resultado) {
                const color = caso.estado === "Aprobado" ? "green" : "red";
                const icono = caso.estado === "Aprobado" ? "✅" : "❌";
                const etiquetaError = caso.tipo_error ? ", tipo de error: " + caso.tipo_error : "";
                html += `
                <div style="border:1px solid ${color}; border-radius:6px; padding:8px; margin:6px 0; color:${color}">
                    ${icono} <strong>${caso.descripcion || "Caso " + caso.caso_id}</strong>: ${caso.estado}${etiquetaError}
                    <br><small style="color:#555">Esperado: <code>${caso.esperado}</code> — Obtenido: <code>${caso.output}</code></small>
                </div>`;
            }
            div.className = "";
            div.innerHTML = html;
        } else {
            // Si no hay desglose, asumimos salida correcta simple y mostramos stdout/output.
            div.className = "correcto";
            div.textContent = "✅ Correcto:\n\n" + (resultado.stdout || resultado.output || "(sin salida)");
        }
    }