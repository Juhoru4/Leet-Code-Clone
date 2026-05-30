const DIFICULTAD_LABELS = { facil: 'Fácil', medio: 'Medio', dificil: 'Difícil' };
    const ORDEN_DIFICULTAD  = { facil: 0, medio: 1, dificil: 2 };

    // RF-02.6: restaurar filtro guardado al cargar la página
    window.addEventListener('DOMContentLoaded', () => {
      const filtroGuardado = sessionStorage.getItem('filtro-dificultad') || '';
      document.getElementById('filtro-dificultad').value = filtroGuardado;
      cargarProblemas(filtroGuardado);
    });

    // RF-02.6: guardar filtro y recargar lista
    function guardarYCargar() {
      const dificultad = document.getElementById('filtro-dificultad').value;
      sessionStorage.setItem('filtro-dificultad', dificultad);
      cargarProblemas(dificultad);
    }

    // RF-02.7: actualización dinámica sin recargar la página
    async function cargarProblemas(dificultad) {
      const tbody    = document.getElementById('cuerpo-tabla');
      const errorDiv = document.getElementById('error-msg');
      const contador = document.getElementById('contador');

      tbody.innerHTML = '<tr><td colspan="5" id="loading">Cargando…</td></tr>';
      errorDiv.style.display = 'none';

      let url = '/api/problems';
      if (dificultad) url += '?difficulty=' + dificultad;

      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('Error del servidor: ' + res.status);
        const problemas = await res.json();

        // RF-02.10: solo mostrar disponibles (esta_activo=true)
        const disponibles = problemas.filter(p => p.esta_activo !== false);

        if (disponibles.length === 0) {
          tbody.innerHTML = '<tr><td colspan="5" id="empty-msg">No hay problemas con ese filtro.</td></tr>';
          contador.textContent = '';
          return;
        }

        contador.textContent = disponibles.length + ' problema(s)';

        // RF-02.2: agrupar por categoría, luego ordenar por dificultad dentro de cada grupo
        const porCategoria = {};
        disponibles.forEach(p => {
          const cat = p.categoria || 'Sin categoría';
          if (!porCategoria[cat]) porCategoria[cat] = [];
          porCategoria[cat].push(p);
        });

        Object.values(porCategoria).forEach(grupo => {
          grupo.sort((a, b) => (ORDEN_DIFICULTAD[a.dificultad] ?? 99) - (ORDEN_DIFICULTAD[b.dificultad] ?? 99));
        });

        let filas = '';
        let contador_global = 1;

        Object.entries(porCategoria).forEach(([categoria, grupo]) => {
          // fila de encabezado de categoría
          filas += `
            <tr class="categoria-header">
              <td colspan="5">${escapeHtml(categoria)}</td>
            </tr>`;

          grupo.forEach(p => {
            const badgeClass   = 'badge-' + (p.dificultad || '');
            const label        = DIFICULTAD_LABELS[p.dificultad] || p.dificultad || '—';
            const estadoClass  = p.esta_activo ? 'badge-disponible' : 'badge-nodisponible';
            const estadoLabel  = p.esta_activo ? 'Disponible' : 'No disponible';

            filas += `
              <tr>
                <td style="color:#6b7280">${contador_global++}</td>
                <td><a class="problem-link" href="/problems/${encodeURIComponent(p.id)}/ui">${escapeHtml(p.titulo)}</a></td>
                <td><span class="categoria-tag">${escapeHtml(p.categoria || '—')}</span></td>
                <td><span class="badge ${badgeClass}">${label}</span></td>
                <td><span class="badge ${estadoClass}">${estadoLabel}</span></td>
              </tr>`;
          });
        });

        tbody.innerHTML = filas;

      } catch (err) {
        errorDiv.textContent = 'No se pudo cargar la lista de problemas. Verifica que el servidor esté corriendo. (' + err.message + ')';
        errorDiv.style.display = 'block';
        tbody.innerHTML = '';
        contador.textContent = '';
      }
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    }