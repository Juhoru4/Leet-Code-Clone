// ── ESTADO GLOBAL ──
    let problemaEnEdicion = null; // ID del problema siendo editado

    // ── NAV ──
    function showSection(id) {
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.getElementById('sec-' + id).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    // ── SUBSECCIONES ──
    function mostrarSubseccion(id) {
        document.querySelectorAll('.subsection').forEach(s => s.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('subsec-' + id).classList.add('active');
        
        // Activar el botón correspondiente
        const btns = document.querySelectorAll('.tab-btn');
        btns.forEach((btn, idx) => {
            if ((idx === 0 && id === 'crear') || (idx === 1 && id === 'editar')) {
                btn.classList.add('active');
            }
        });
        
        if (id === 'editar') {
            cargarListaProblemas();
        }
    }

    // ── CARGAR LISTA DE PROBLEMAS PARA EDITAR ──
    async function cargarListaProblemas() {
        const contenedor = document.getElementById('lista-problemas-editar');
        contenedor.innerHTML = '<p style="text-align:center; color:#6b7280;">Cargando problemas…</p>';
        
        try {
            const res = await fetch('/api/problems');
            if (!res.ok) throw new Error('Error al cargar problemas');
            const problemas = await res.json();
            
            if (problemas.length === 0) {
                contenedor.innerHTML = '<p style="text-align:center; color:#6b7280;">No hay problemas para editar.</p>';
                return;
            }
            
            let html = `
                <table class="problemas-tabla">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Categoría</th>
                            <th>Dificultad</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            problemas.forEach(p => {
                const badgeClass = 'badge-' + (p.dificultad || '');
                const dificultadLabel = p.dificultad ? 
                    p.dificultad.charAt(0).toUpperCase() + p.dificultad.slice(1) : '—';
                const estadoLabel = p.esta_activo ? 'Activo' : 'Inactivo';
                const estadoClass = p.esta_activo ? 'badge-disponible' : 'badge-nodisponible';
                
                html += `
                    <tr>
                        <td>${escapeHtml(p.titulo)}</td>
                        <td>${escapeHtml(p.categoria || '—')}</td>
                        <td><span class="badge ${badgeClass}">${dificultadLabel}</span></td>
                        <td><span class="badge ${estadoClass}">${estadoLabel}</span></td>
                        <td>
                            <div class="problema-acciones">
                                <button class="btn-edit-problema" onclick="editarProblema('${p.id}')">
                                    Editar
                                </button>
                                <button class="btn-delete-problema" onclick="eliminarProblema('${p.id}', '${escapeHtml(p.titulo).replace(/'/g, "\\'")}')">Eliminar</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            html += `
                    </tbody>
                </table>
            `;
            
            contenedor.innerHTML = html;
        } catch (err) {
            contenedor.innerHTML = '<p style="text-align:center; color:#f87171;">Error al cargar problemas: ' + err.message + '</p>';
        }
    }

    async function editarProblema(id) {
        try {
            const res = await fetch(`/api/problems/${id}`);
            if (!res.ok) throw new Error('Problema no encontrado');
            const problema = await res.json();
            
            // Cargar datos en el formulario
            document.getElementById('titulo').value = problema.titulo;
            document.getElementById('descripcion').value = problema.descripcion;
            document.getElementById('categoria_id').value = problema.categoria_id || '';
            document.getElementById('dificultad').value = problema.dificultad || '';
            document.getElementById('restricciones').value = problema.restricciones || '';
            document.getElementById('ejemplo_entrada').value = problema.ejemplo_entrada || '';
            document.getElementById('ejemplo_salida').value = problema.ejemplo_salida || '';
            document.getElementById('codigo_base_python').value = problema.codigo_base_python || '';
            document.getElementById('codigo_base_java').value = problema.codigo_base_java || '';
            document.getElementById('codigo_base_cpp').value = problema.codigo_base_cpp || '';
            document.getElementById('limite_tiempo_ms').value = problema.limite_tiempo_ms || '';
            document.getElementById('limite_memoria_mb').value = problema.limite_memoria_mb || '';
            document.getElementById('esta_activo').checked = problema.esta_activo;
            document.getElementById('toggle-label-text').textContent = problema.esta_activo ? 'Activo' : 'Inactivo';
            
            // Cargar casos de prueba
            document.getElementById('casos-list').innerHTML = '';
            casosCount = 0;
            (problema.casos_prueba || []).forEach(caso => {
                agregarCasoConDatos(caso);
            });
            
            // Cambiar botón y estado
            problemaEnEdicion = id;
            const btn = document.getElementById('btn-guardar');
            btn.textContent = 'Actualizar problema';
            
            // Cambiar a tab crear/formulario
            mostrarSubseccion('crear');
            
            toast('Problema cargado para edición', 'ok');
        } catch (e) {
            toast('Error al cargar el problema: ' + e.message, 'err');
        }
    }
    
    function agregarCasoConDatos(casoData) {
        casosCount++;
        const n = casosCount;
        const lista = document.getElementById('casos-list');

        const div = document.createElement('div');
        div.className = 'caso-item';
        div.id = `caso-${n}`;
        
        const isPublico = casoData.es_publico ? 'pub' : 'priv';
        const badgeText = casoData.es_publico ? 'PÚBLICO' : 'PRIVADO';
        
        div.innerHTML = `
            <div class="caso-header">
                <span class="caso-num">CASO #${n}</span>
                <div class="caso-actions">
                    <button class="badge-publico ${isPublico}" onclick="togglePublico(this)" title="Click para cambiar visibilidad">
                        ${badgeText}
                    </button>
                    <button class="btn-remove-caso" onclick="eliminarCaso(${n})">✕ Eliminar</button>
                </div>
            </div>
            <div class="caso-grid">
                <div class="field">
                    <label>Descripción</label>
                    <input type="text" placeholder="Ej: Caso básico" data-caso="${n}" data-field="descripcion" value="${escapeHtml(casoData.descripcion || '')}">
                </div>
                <div class="field">
                    <label>Entrada *</label>
                    <textarea rows="2" placeholder="Valor de stdin" data-caso="${n}" data-field="entrada">${escapeHtml(casoData.entrada || '')}</textarea>
                </div>
                <div class="field">
                    <label>Salida esperada *</label>
                    <textarea rows="2" placeholder="Salida exacta esperada" data-caso="${n}" data-field="salida_esperada">${escapeHtml(casoData.salida_esperada || '')}</textarea>
                </div>
            </div>
        `;
        lista.appendChild(div);
    }

    async function eliminarProblema(id, titulo) {
        if (!confirm(`¿Estás seguro de que deseas eliminar el problema "${titulo}"? Esta acción no se puede deshacer.`)) {
            return;
        }

        try {
            const res = await fetch(`/api/problems/${id}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await res.json();

            if (!res.ok) {
                toast(data.error || 'Error al eliminar', 'err');
                return;
            }

            toast('✓ Problema eliminado correctamente', 'ok');
            cargarListaProblemas();

        } catch (e) {
            toast('No se pudo conectar con el servidor', 'err');
        }
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    // ── TOGGLE LABEL ──
    document.getElementById('esta_activo').addEventListener('change', function () {
        document.getElementById('toggle-label-text').textContent = this.checked ? 'Activo' : 'Inactivo';
    });

    // ── CARGAR CATEGORÍAS ──
    async function cargarCategorias() {
        try {
            const res = await fetch('/api/categories');
            if (!res.ok) return;
            const data = await res.json();
            const sel = document.getElementById('categoria_id');
            (data.categorias || data).forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat.id;
                opt.textContent = cat.nombre;
                sel.appendChild(opt);
            });
        } catch (_) {}
    }

    cargarCategorias();

    // ── CASOS DE PRUEBA ──
    let casosCount = 0;

    function agregarCaso() {
        casosCount++;
        const n = casosCount;
        const lista = document.getElementById('casos-list');

        const div = document.createElement('div');
        div.className = 'caso-item';
        div.id = `caso-${n}`;
        div.innerHTML = `
            <div class="caso-header">
                <span class="caso-num">CASO #${n}</span>
                <div class="caso-actions">
                    <button class="badge-publico pub" onclick="togglePublico(this)" title="Click para cambiar visibilidad">
                        PÚBLICO
                    </button>
                    <button class="btn-remove-caso" onclick="eliminarCaso(${n})">✕ Eliminar</button>
                </div>
            </div>
            <div class="caso-grid">
                <div class="field">
                    <label>Descripción</label>
                    <input type="text" placeholder="Ej: Caso básico" data-caso="${n}" data-field="descripcion">
                </div>
                <div class="field">
                    <label>Entrada *</label>
                    <textarea rows="2" placeholder="Valor de stdin" data-caso="${n}" data-field="entrada"></textarea>
                </div>
                <div class="field">
                    <label>Salida esperada *</label>
                    <textarea rows="2" placeholder="Salida exacta esperada" data-caso="${n}" data-field="salida_esperada"></textarea>
                </div>
            </div>
        `;
        lista.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function togglePublico(btn) {
        const esPublico = btn.classList.contains('pub');
        btn.classList.toggle('pub', !esPublico);
        btn.classList.toggle('priv', esPublico);
        btn.textContent = esPublico ? 'PRIVADO' : 'PÚBLICO';
    }

    function eliminarCaso(n) {
        const el = document.getElementById(`caso-${n}`);
        if (el) el.remove();
    }

    // ── LEER CASOS ──
    function leerCasos() {
        const casos = [];
        document.querySelectorAll('.caso-item').forEach((item, idx) => {
            const n = item.id.replace('caso-', '');
            const get = (field) => {
                const el = item.querySelector(`[data-caso="${n}"][data-field="${field}"]`);
                return el ? el.value.trim() : '';
            };
            const badge = item.querySelector('.badge-publico');
            casos.push({
                descripcion: get('descripcion'),
                entrada: get('entrada'),
                salida_esperada: get('salida_esperada'),
                es_publico: badge ? badge.classList.contains('pub') : true,
                orden: idx + 1,
            });
        });
        return casos;
    }

    // ── GUARDAR ──
    async function guardarProblema() {
        const titulo = document.getElementById('titulo').value.trim();
        const descripcion = document.getElementById('descripcion').value.trim();

        if (!titulo) { toast('El título es obligatorio', 'err'); return; }
        if (!descripcion) { toast('La descripción es obligatoria', 'err'); return; }

        const casos = leerCasos();
        for (let i = 0; i < casos.length; i++) {
            if (!casos[i].entrada || !casos[i].salida_esperada) {
                toast(`El caso #${i + 1} necesita entrada y salida esperada`, 'err');
                return;
            }
        }

        const payload = {
            titulo,
            descripcion,
            categoria_id: document.getElementById('categoria_id').value || null,
            dificultad: document.getElementById('dificultad').value || null,
            restricciones: document.getElementById('restricciones').value.trim() || null,
            ejemplo_entrada: document.getElementById('ejemplo_entrada').value.trim() || null,
            ejemplo_salida: document.getElementById('ejemplo_salida').value.trim() || null,
            codigo_base_python: document.getElementById('codigo_base_python').value.trim() || null,
            codigo_base_java: document.getElementById('codigo_base_java').value.trim() || null,
            codigo_base_cpp: document.getElementById('codigo_base_cpp').value.trim() || null,
            limite_tiempo_ms: parseInt(document.getElementById('limite_tiempo_ms').value) || null,
            limite_memoria_mb: parseInt(document.getElementById('limite_memoria_mb').value) || null,
            esta_activo: document.getElementById('esta_activo').checked,
            casos_prueba: casos,
        };

        const btn = document.getElementById('btn-guardar');
        btn.disabled = true;
        btn.textContent = 'Guardando…';

        try {
            // Detectar si es creación o actualización
            const isEditing = problemaEnEdicion !== null;
            const endpoint = isEditing ? `/api/problems/${problemaEnEdicion}` : '/api/problems/crear';
            const method = isEditing ? 'PUT' : 'POST';
            
            const res = await fetch(endpoint, {
                method: method,
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const data = await res.json();

            if (!res.ok) {
                toast(data.error || 'Error al guardar', 'err');
                return;
            }

            const msg = isEditing ? '✓ Problema actualizado correctamente' : '✓ Problema guardado correctamente';
            toast(msg, 'ok');
            limpiarForm();

        } catch (e) {
            toast('No se pudo conectar con el servidor', 'err');
        } finally {
            btn.disabled = false;
            btn.textContent = problemaEnEdicion ? 'Actualizar problema' : 'Guardar problema';
        }
    }

    // ── LIMPIAR ──
    function limpiarForm() {
        ['titulo','descripcion','restricciones','ejemplo_entrada','ejemplo_salida','codigo_base_python','codigo_base_java','codigo_base_cpp'].forEach(id => {
            document.getElementById(id).value = '';
        });
        document.getElementById('categoria_id').value = '';
        document.getElementById('dificultad').value = '';
        document.getElementById('limite_tiempo_ms').value = '';
        document.getElementById('limite_memoria_mb').value = '';
        document.getElementById('esta_activo').checked = true;
        document.getElementById('toggle-label-text').textContent = 'Activo';
        document.getElementById('casos-list').innerHTML = '';
        casosCount = 0;
        
        // Limpiar estado de edición
        problemaEnEdicion = null;
        document.getElementById('btn-guardar').textContent = 'Guardar problema';
    }

    // ── TOAST ──
    function toast(msg, type = 'ok') {
        const el = document.getElementById('toast');
        el.textContent = msg;
        el.className = `show ${type}`;
        clearTimeout(el._t);
        el._t = setTimeout(() => { el.className = ''; }, 3000);
    }