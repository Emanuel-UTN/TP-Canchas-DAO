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

    // Si es el formulario de reserva, cargar canchas y clientes
    else if (type === 'reserva') {
        // cargar canchas
        const canchasSelect = document.getElementById('reserva-cancha');
        if (canchasSelect) {
            canchasSelect.querySelectorAll('option:not([value=""])').forEach(o => o.remove());
            try {
                const resp = await fetch('/api/canchas');
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const canchas = await resp.json();
                if (Array.isArray(canchas) && canchas.length > 0) {
                    canchas.forEach(c => {
                        const opt = document.createElement('option');
                        opt.value = c.nro_cancha;
                        opt.textContent = `${c.nro_cancha} — ${c.tipo ?? ''}`;
                        canchasSelect.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement('option');
                    opt.value = '';
                    opt.disabled = true;
                    opt.textContent = 'No hay canchas disponibles';
                    canchasSelect.appendChild(opt);
                }
            } catch (err) {
                console.error('Error cargando canchas:', err);
                const opt = document.createElement('option');
                opt.value = '';
                opt.disabled = true;
                opt.textContent = 'Error al cargar canchas';
                canchasSelect.appendChild(opt);
            }
        }

        // cargar clientes y preparar datalist
        const clientesDatalist = document.getElementById('clientes-list');
        const clienteInput = document.getElementById('reserva-cliente-nombre');
        const clienteHidden = document.getElementById('reserva-cliente');
        if (clientesDatalist && clienteInput && clienteHidden) {
            // limpiar
            clientesDatalist.innerHTML = '';
            try {
                const resp = await fetch('/api/clientes');
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const clientes = await resp.json();
                // cachear en scope global para resolver selección
                window._clientesCache = clientes;
                if (Array.isArray(clientes) && clientes.length > 0) {
                    clientes.forEach(cl => {
                        const opt = document.createElement('option');
                        // mostrar texto nombre apellido — DNI
                        opt.value = `${cl.nombre} ${cl.apellido} — ${cl.dni}`;
                        clientesDatalist.appendChild(opt);
                    });
                }

                // cuando el usuario seleccione/tipee un valor del datalist, rellenar el campo oculto con el DNI
                const resolverClienteDesdeValor = (val) => {
                    if (Array.isArray(window._clientesCache)) {
                        const found = window._clientesCache.find(c => `${c.nombre} ${c.apellido} — ${c.dni}` === val);
                        if (found) {
                            clienteHidden.value = found.dni;
                            return;
                        }
                    }
                    const m = (val || '').match(/(\d{6,})$/);
                    if (m) clienteHidden.value = m[1];
                    else clienteHidden.value = '';
                };

                // asignar listeners para cubrir selección por datalist y escritura manual
                clienteInput.addEventListener('input', (e) => resolverClienteDesdeValor(e.target.value));
                clienteInput.addEventListener('change', (e) => resolverClienteDesdeValor(e.target.value));
                clienteInput.addEventListener('blur', (e) => {
                    if (!clienteHidden.value) resolverClienteDesdeValor(e.target.value);
                });

            } catch (err) {
                console.error('Error cargando clientes:', err);
            }
        }

        // preseleccionar la próxima hora redondeada al abrir el formulario
        const fechaInput = document.getElementById('reserva-fecha');
        if (fechaInput && !fechaInput.value) {
            const now = new Date();
            // redondear hacia arriba a la siguiente hora
            if (now.getMinutes() > 0 || now.getSeconds() > 0 || now.getMilliseconds() > 0) {
                now.setHours(now.getHours() + 1);
            }
            now.setMinutes(0, 0, 0);
            const pad = (n) => n.toString().padStart(2, '0');
            const localIso = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:00`;
            fechaInput.value = localIso;
        }
    }

    formEl.style.display = 'block';
}

function cancelarForm(type) {
    document.getElementById(`form-${type}`).style.display = 'none';
    document.getElementById(`form-${type}`).querySelector('form').reset();
}