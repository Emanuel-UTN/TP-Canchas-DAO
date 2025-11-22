(function(){
    let torneoId;

    async function loadDetalle(){
        // cargar detalle del torneo
        const res = await fetch(`/api/torneos/detalle/${torneoId}`);
        const data = await res.json();
        if (data.error) {
            const meta = document.getElementById('torneo-meta');
            if (meta) meta.innerText = 'Error: ' + data.error;
            return;
        }

        // meta
        const metaEl = document.getElementById('torneo-meta');
        if (metaEl) metaEl.innerHTML = `
            <strong>Inicio:</strong> ${data.fecha_inicio} &nbsp; 
            <strong>Fin:</strong> ${data.fecha_fin} &nbsp; 
            <strong>Costo:</strong> $${data.costo_inscripcion} &nbsp; 
            <strong>Premio:</strong> $${data.premio} &nbsp; 
            <strong>Equipos:</strong> ${data.tabla.length}
        `;

        // tabla de posiciones
        const tablaContainer = document.getElementById('tabla-posiciones');
        if (!Array.isArray(data.tabla) || data.tabla.length === 0) {
            if (tablaContainer) tablaContainer.innerHTML = '<div>No hay equipos inscriptos</div>';
        } else if (tablaContainer) {
            let html = '<table class="table table-striped table-sm"><thead><tr><th>Pos</th><th>Equipo</th><th>Pts</th><th>PJ</th><th>GF</th><th>GC</th></tr></thead><tbody>';
            data.tabla.forEach(row => {
                html += `<tr>
                    <td>${row.posicion}</td>
                    <td>${row.nombre}</td>
                    <td>${row.puntos}</td>
                    <td>${row.partidos_jugados}</td>
                    <td>${row.goles_a_favor}</td>
                    <td>${row.goles_en_contra}</td>
                </tr>`;
            });
            html += '</tbody></table>';
            tablaContainer.innerHTML = html;
        }

        // proximos partidos agrupados por fecha
        const partidosContainer = document.getElementById('proximos-partidos');
        if (!Array.isArray(data.partidos) || data.partidos.length === 0) {
            if (partidosContainer) partidosContainer.innerHTML = '<div>No hay partidos programados</div>';
        } else if (partidosContainer) {
            // agrupar por fecha (solo día)
            const groups = {};
            data.partidos.forEach(p => {
                const fecha = (p.fecha_hora || '').split('T')[0] || p.fecha_hora.split(' ')[0];
                if (!groups[fecha]) groups[fecha] = [];
                groups[fecha].push(p);
            });
            let html = '';
            for (const fecha of Object.keys(groups)) {
                html += `<h6>${fecha}</h6><ul class="list-group mb-3">`;
                groups[fecha].forEach(p => {
                    const hora = (p.fecha_hora || '').split('T')[1] || p.fecha_hora.split(' ')[1] || '';
                    html += `<li class="list-group-item d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${p.equipo1_nombre}</strong> vs <strong>${p.equipo2_nombre}</strong><br>
                            <small>Cancha: ${p.nro_cancha} (${p.cancha_tipo || '—'})</small>
                        </div>
                        <div class="text-end">
                            <small>${hora}</small>
                        </div>
                    </li>`;
                });
                html += '</ul>';
            }
            partidosContainer.innerHTML = html;
        }

        const mensajeEquipo = document.getElementById('mensaje-equipo');
        if (mensajeEquipo) mensajeEquipo.innerText = '';

        // cargar clientes para el datalist de delegado
        try {
            const resp = await fetch('/api/clientes');
            if (resp.ok) {
                const clientes = await resp.json();
                // cachear para uso global (igual que en navegacion.js)
                window._clientesCache = clientes;
                const dl = document.getElementById('clientes-list-torneo');
                if (dl) dl.innerHTML = '';
                if (Array.isArray(clientes)) {
                    clientes.forEach(cl => {
                        const opt = document.createElement('option');
                        opt.value = `${cl.nombre} ${cl.apellido} — ${cl.dni}`;
                        dl.appendChild(opt);
                    });
                }
            }
        } catch (err) {
            // eslint-disable-next-line no-console
            console.error('Error cargando clientes para datalist:', err);
        }
    }

    // Todas las interacciones con el DOM se inicializan en DOMContentLoaded
    document.addEventListener('DOMContentLoaded', async () => {
        // obtener torneoId desde el elemento oculto en la plantilla
        const root = document.getElementById('torneo-root');
        torneoId = root ? root.dataset.torneoId : undefined;

        const delegadoInput = document.getElementById('equipo-delegado-input');
        const delegadoHidden = document.getElementById('equipo-delegado-dni');
        const sugContainer = document.getElementById('clientes-suggestions-torneo');

        const resolverDelegadoDesdeValor = (val) => {
            if (Array.isArray(window._clientesCache)) {
                const found = window._clientesCache.find(c => `${c.nombre} ${c.apellido} — ${c.dni}` === val);
                if (found) {
                    if (delegadoHidden) delegadoHidden.value = found.dni;
                    return;
                }
            }
            const m = (val || '').match(/(\d{6,})$/);
            if (m && delegadoHidden) delegadoHidden.value = m[1];
            else if (delegadoHidden) delegadoHidden.value = '';
        };

        if (delegadoInput) {
            delegadoInput.addEventListener('input', (e) => resolverDelegadoDesdeValor(e.target.value));
            delegadoInput.addEventListener('change', (e) => resolverDelegadoDesdeValor(e.target.value));
            delegadoInput.addEventListener('blur', (e) => { if (delegadoHidden && !delegadoHidden.value) resolverDelegadoDesdeValor(e.target.value); });
        }

        // dropdown visible y filtrable
        if (sugContainer && delegadoInput) {
            let activeIndex = -1;
            const clearSuggestions = () => { sugContainer.innerHTML = ''; sugContainer.style.display = 'none'; activeIndex = -1; };
            const renderSuggestions = async (query) => {
                // asegurar que la lista de clientes esté cargada
                if (!Array.isArray(window._clientesCache)) {
                    try {
                        const resp = await fetch('/api/clientes');
                        if (resp.ok) {
                            const clientes = await resp.json();
                            window._clientesCache = clientes;
                            const dl = document.getElementById('clientes-list-torneo');
                            if (dl) dl.innerHTML = '';
                            if (Array.isArray(clientes)) {
                                clientes.forEach(cl => {
                                    const opt = document.createElement('option');
                                    opt.value = `${cl.nombre} ${cl.apellido} — ${cl.dni}`;
                                    dl.appendChild(opt);
                                });
                            }
                        }
                    } catch (err) {
                        console.error('Error cargando clientes:', err);
                    }
                }
                const clientes = Array.isArray(window._clientesCache) ? window._clientesCache : [];
                const q = (query || '').toLowerCase().trim();
                sugContainer.innerHTML = '';
                const matches = !q ? clientes.slice(0,10) : clientes.filter(c => (`${c.nombre} ${c.apellido} ${c.dni}`).toLowerCase().includes(q)).slice(0,10);
                if (!matches || matches.length === 0) { clearSuggestions(); return; }
                // asegurar estilos visibles y posicionamiento relativo al input
                sugContainer.classList.add('bg-white','shadow','rounded');
                sugContainer.style.maxHeight = '240px';
                sugContainer.style.overflow = 'auto';
                sugContainer.style.position = 'absolute';
                sugContainer.style.left = '0px';
                // dejar un pequeño espacio para que el input no quede tapado por la lista
                sugContainer.style.top = (delegadoInput.offsetHeight + 30) + 'px';
                sugContainer.style.zIndex = '2000';
                activeIndex = -1;
                matches.forEach((m, idx) => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'list-group-item list-group-item-action';
                    btn.textContent = `${m.nombre} ${m.apellido} — ${m.dni}`;
                    btn.dataset.dni = m.dni;
                    btn.addEventListener('click', () => {
                        delegadoInput.value = btn.textContent;
                        if (delegadoHidden) delegadoHidden.value = btn.dataset.dni;
                        clearSuggestions();
                    });
                    sugContainer.appendChild(btn);
                });
                sugContainer.style.display = 'block';
            };

            delegadoInput.addEventListener('input', (e) => { renderSuggestions(e.target.value).catch(err=>console.error(err)); });
            delegadoInput.addEventListener('focus', (e) => { renderSuggestions(e.target.value).catch(err=>console.error(err)); });
            delegadoInput.addEventListener('blur', (e) => setTimeout(clearSuggestions, 150));
            delegadoInput.addEventListener('keydown', (e) => {
                const items = Array.from(sugContainer.querySelectorAll('.list-group-item'));
                if (!items.length) return;
                if (e.key === 'ArrowDown') { e.preventDefault(); activeIndex = Math.min(activeIndex+1, items.length-1); items.forEach((it,i)=>it.classList.toggle('active', i===activeIndex)); items[activeIndex].scrollIntoView({block:'nearest'}); }
                else if (e.key === 'ArrowUp') { e.preventDefault(); activeIndex = Math.max(activeIndex-1, 0); items.forEach((it,i)=>it.classList.toggle('active', i===activeIndex)); items[activeIndex].scrollIntoView({block:'nearest'}); }
                else if (e.key === 'Enter') { if (activeIndex>=0 && items[activeIndex]) { e.preventDefault(); items[activeIndex].click(); } }
            });
        }

        // submit form
        const btnAgregar = document.getElementById('btn-agregar-equipo');
        if (btnAgregar) btnAgregar.addEventListener('click', async function(e){
            e.preventDefault();
            const nombreEl = document.getElementById('equipo-nombre');
            const nombre = nombreEl ? nombreEl.value.trim() : '';
            const dni = delegadoHidden ? delegadoHidden.value.trim() : '';
            const mensajeEl = document.getElementById('mensaje-equipo');
            if (!nombre || !dni) {
                if (mensajeEl) mensajeEl.innerText = 'Completar nombre y DNI';
                return;
            }
            try {
                const res = await fetch(`/api/torneos/${torneoId}/equipos`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({nombre: nombre, dni_delegado: dni})
                });
                const r = await res.json();
                if (!res.ok) {
                    if (mensajeEl) mensajeEl.innerText = r.error || 'Error al agregar equipo';
                } else {
                    if (mensajeEl) mensajeEl.innerText = 'Equipo agregado correctamente';
                    // limpiar form
                    if (nombreEl) nombreEl.value = '';
                    if (delegadoHidden) delegadoHidden.value = '';
                    const input = document.getElementById('equipo-delegado-input'); if (input) input.value = '';
                    // recargar detalle
                    await loadDetalle();
                }
            } catch (err) {
                if (mensajeEl) mensajeEl.innerText = 'Error: ' + err.message;
            }
        });
        // cargar datos iniciales
        try {
            await loadDetalle();
        } catch (err) {
            const meta = document.getElementById('torneo-meta');
            if (meta) meta.innerText = 'Error al cargar: ' + err.message;
        }
    });
})();
