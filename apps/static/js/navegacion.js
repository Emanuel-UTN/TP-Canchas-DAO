// Funciones de navegación y UI
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Cargar datos al cambiar de tab
    loadTabData(tabName);
}

async function showForm(type) {
    const formEl = document.getElementById(`form-${type}`);
    if (!formEl) return;

    // Si es el formulario de cancha, cargar tipos de cancha en el select
    if (type === 'cancha') {
        const select = document.getElementById('cancha-tipo');
        if (select) {
            // limpiar opciones excepto la primera (placeholder)
            select.querySelectorAll('option:not([value=""])').forEach(o => o.remove());
            try {
                const resp = await fetch('/api/tipos-cancha');
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const tipos = await resp.json();
                if (Array.isArray(tipos) && tipos.length > 0) {
                    tipos.forEach(t => {
                        const opt = document.createElement('option');
                        opt.value = t.tipo;
                        opt.textContent = t.tipo;
                        select.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement('option');
                    opt.value = '';
                    opt.disabled = true;
                    opt.textContent = 'No hay tipos disponibles';
                    select.appendChild(opt);
                }
            } catch (err) {
                console.error('Error cargando tipos de cancha:', err);
                const opt = document.createElement('option');
                opt.value = '';
                opt.disabled = true;
                opt.textContent = 'Error al cargar tipos';
                select.appendChild(opt);
            }
        }
        // Cargar servicios disponibles en multi-select
        const serviciosSelect = document.getElementById('cancha-servicios');
        if (serviciosSelect) {
            // limpiar opciones previas
            serviciosSelect.querySelectorAll('option').forEach(o => o.remove());
            try {
                const resp = await fetch('/api/servicios');
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const servicios = await resp.json();
                if (Array.isArray(servicios) && servicios.length > 0) {
                    servicios.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.servicio;
                        opt.textContent = `$${s.costo} — ${s.servicio ?? s.nombre ?? 'Servicio'}`;
                        serviciosSelect.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement('option');
                    opt.value = '';
                    opt.disabled = true;
                    opt.textContent = 'No hay servicios disponibles';
                    serviciosSelect.appendChild(opt);
                }
            } catch (err) {
                console.error('Error cargando servicios:', err);
                const opt = document.createElement('option');
                opt.value = '';
                opt.disabled = true;
                opt.textContent = 'Error al cargar servicios';
                serviciosSelect.appendChild(opt);
            }
        }
    }

    formEl.style.display = 'block';
}

function cancelarForm(type) {
    document.getElementById(`form-${type}`).style.display = 'none';
    document.getElementById(`form-${type}`).querySelector('form').reset();
}