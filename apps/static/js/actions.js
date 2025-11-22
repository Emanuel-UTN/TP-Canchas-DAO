// Funciones de eliminación
async function eliminarCliente(dni) {
    if (!confirm('¿Está seguro de eliminar este cliente?')) return;
    try {
        const response = await fetch(`/api/clientes/${dni}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Cliente eliminado exitosamente');
            loadTabData('clientes');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function editarCliente(dni) {
    try {
        const res = await fetch(`/api/clientes/${dni}`);
        if (!res.ok) {
            const error = await res.json();
            alert('Error: ' + (error.error || 'No se pudo obtener el cliente'));
            return;
        }
        const cliente = await res.json();
        // Mostrar modal
        document.getElementById("modal-editar").style.display = "block";

        // Cargar datos
        document.getElementById("edit-dni").value = cliente.dni;
        document.getElementById("edit-nombre").value = cliente.nombre;
        document.getElementById("edit-apellido").value = cliente.apellido;
        document.getElementById("edit-telefono").value = cliente.telefono;
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarCambiosCliente() {
    const dni = document.getElementById("edit-dni").value;
    const nombre = document.getElementById("edit-nombre").value;
    const apellido = document.getElementById("edit-apellido").value;
    const telefono = document.getElementById("edit-telefono").value;

    const errores = [];
    const errorNombre = Validaciones.esTextoValido(nombre, 'Nombre');
    if (errorNombre) errores.push(errorNombre);
    const errorApellido = Validaciones.esTextoValido(apellido, 'Apellido');
    if (errorApellido) errores.push(errorApellido);
    const errorTelefono = Validaciones.esTelefonoValido(telefono);
    if (errorTelefono) errores.push(errorTelefono);

    if (Validaciones.mostrarErrores(errores)) return;

    const data = {
        nombre: nombre,
        apellido: apellido,
        telefono: telefono,
    };

    try {
        const response = await fetch(`/api/clientes/${dni}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            alert('Error: ' + error.error);
            return;
        }
        document.getElementById("modal-editar").style.display = "none";
        loadTabData('clientes');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ---- Cancha  ----
async function editarCancha(nro){
    try{
        const res = await fetch(`/api/canchas/${nro}`);
        if (!res.ok) {
            const error = await res.json();
            alert('Error: ' + (error.error || 'No se pudo obtener la cancha'));
            return;
        }
        const cancha = await res.json();
        // Mostrar modal
        document.getElementById("modal-editar-cancha").style.display = "block";

        // Cargar datos
        document.getElementById("edit-cancha-costo").value = cancha.costo_por_hora;
        document.getElementById("edit-nro").value = cancha.nro_cancha
        
        const serviciosSelect = document.getElementById('edit-cancha-servicios');
        if (serviciosSelect) {
            // limpiar opciones previas
            serviciosSelect.querySelectorAll('option').forEach(o => o.remove());
            try {
                const resp = await fetch('/api/servicios');
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const servicios = await resp.json();
                if (Array.isArray(servicios) && servicios.length > 0) {
                    // preparar conjunto con los servicios ya asociados a la cancha
                    const existentes = Array.isArray(cancha.servicios) ? cancha.servicios.map(x => (typeof x === 'string' ? x : (x.servicio ?? x.nombre ?? ''))) : [];
                    servicios.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.servicio;
                        opt.textContent = `$${s.costo} — ${s.servicio ?? s.nombre ?? 'Servicio'}`;
                        // marcar como seleccionado si está en la lista de la cancha
                        if (existentes.includes(opt.value)) opt.selected = true;
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
    }catch(error){
        alert('Error: ' + error.message);
    }
}

async function guardarCambiosCancha() {
    const costo = document.getElementById('edit-cancha-costo').value;
    const nro = document.getElementById("edit-nro").value;
    // obtener servicios seleccionados (multi-select)
    const serviciosSelect = document.getElementById('edit-cancha-servicios');
    const serviciosSeleccionados = [];
    if (serviciosSelect) {
        Array.from(serviciosSelect.selectedOptions).forEach(opt => {
            if (opt.value) serviciosSeleccionados.push(opt.value);
        });
    }
    
    const errores = [];
    
    const errorCosto = Validaciones.esNumeroPositivo(costo, 'Costo por hora');
    if (errorCosto) errores.push(errorCosto);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        nro_cancha: nro,
        costo_por_hora: parseFloat(costo),
        servicios: serviciosSeleccionados
    };
    try {
        const response = await fetch(`/api/canchas/${nro}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Cancha editada exitosamente');
            cerrarModalEditarCancha();
            loadTabData('canchas');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function cerrarModalEditarCancha() {
    document.getElementById('modal-editar-cancha').style.display = 'none';
}

async function eliminarCancha(nro) {
    if (!confirm('¿Está seguro de eliminar esta cancha?')) return;
    try {
        const response = await fetch(`/api/canchas/${nro}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Cancha eliminada exitosamente');
            loadTabData('canchas');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function eliminarReserva(nro) {
    if (!confirm('¿Está seguro de eliminar esta reserva?')) return;
    try {
        const response = await fetch(`/api/reservas/${nro}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Reserva eliminada exitosamente');
            loadTabData('reservas');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function eliminarTorneo(id) {
    if (!confirm('¿Está seguro de eliminar este torneo?')) return;
    try {
        const response = await fetch(`/api/torneos/${id}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Torneo eliminado exitosamente');
            loadTabData('torneos');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ---- Tipos de Cancha (CRUD por nombre) ----
async function eliminarTipoCancha(nombre_tipo) {
    const decoded = decodeURIComponent(nombre_tipo);
    if (!confirm(`¿Eliminar tipo de cancha "${decoded}"?`)) return;
    try {
        const response = await fetch(`/api/tipos-cancha/${encodeURIComponent(decoded)}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Tipo de cancha eliminado');
            loadTabData('tipos-cancha');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function editarTipoCancha(nombre_tipo) {
    const decoded = decodeURIComponent(nombre_tipo);
    try {
        const res = await fetch(`/api/tipos-cancha/${encodeURIComponent(decoded)}`);
        if (!res.ok) {
            const error = await res.json();
            alert('Error: ' + (error.error || 'No se pudo obtener el tipo'));
            return;
        }
        const tipo = await res.json();
        document.getElementById('modal-editar-tipo').style.display = 'block';
        document.getElementById('edit-tipo-actual').value = decoded;
        document.getElementById('edit-tipo-nombre').value = tipo.tipo;
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

function cerrarModalEditarTipo() {
    document.getElementById('modal-editar-tipo').style.display = 'none';
}

async function guardarCambiosTipoCancha() {
    const actual = document.getElementById('edit-tipo-actual').value;
    const nuevo = document.getElementById('edit-tipo-nombre').value;
    const errorTipo = Validaciones.esTextoValido(nuevo, 'Tipo de cancha', 3, 50);
    if (errorTipo) { Validaciones.mostrarErrores([errorTipo]); return; }
    try {
        const res = await fetch(`/api/tipos-cancha/${encodeURIComponent(actual)}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({tipo: nuevo.trim()})
        });
        if (res.ok) {
            cerrarModalEditarTipo();
            loadTabData('tipos-cancha');
        } else {
            const err = await res.json();
            alert('Error: ' + err.error);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

// ---- Servicios (CRUD por nombre) ----
async function eliminarServicio(nombre_servicio) {
    const decoded = decodeURIComponent(nombre_servicio);
    if (!confirm(`¿Eliminar servicio "${decoded}"?`)) return;
    try {
        const response = await fetch(`/api/servicios/${encodeURIComponent(decoded)}`, {method: 'DELETE'});
        if (response.ok) {
            alert('Servicio eliminado');
            loadTabData('servicios');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

async function editarServicio(nombre_servicio) {
    const decoded = decodeURIComponent(nombre_servicio);
    try {
        const res = await fetch(`/api/servicios/${encodeURIComponent(decoded)}`);
        if (!res.ok) {
            const error = await res.json();
            alert('Error: ' + (error.error || 'No se pudo obtener el servicio'));
            return;
        }
        const servicio = await res.json();
        document.getElementById('modal-editar-servicio').style.display = 'block';
        document.getElementById('edit-servicio-actual').value = decoded;
        document.getElementById('edit-servicio-nombre').value = servicio.servicio;
        document.getElementById('edit-servicio-costo').value = servicio.costo;
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

function cerrarModalEditarServicio() {
    document.getElementById('modal-editar-servicio').style.display = 'none';
}

async function guardarCambiosServicio() {
    const actual = document.getElementById('edit-servicio-actual').value;
    const nuevo = document.getElementById('edit-servicio-nombre').value;
    const costo = document.getElementById('edit-servicio-costo').value;
    const errores = [];
    const errNombre = Validaciones.esTextoValido(nuevo, 'Servicio', 3, 100);
    if (errNombre) errores.push(errNombre);
    const errCosto = Validaciones.esNumeroPositivo(costo, 'Costo');
    if (errCosto) errores.push(errCosto);
    if (Validaciones.mostrarErrores(errores)) return;
    try {
        const res = await fetch(`/api/servicios/${encodeURIComponent(actual)}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({servicio: nuevo.trim(), costo: parseFloat(costo)})
        });
        if (res.ok) {
            cerrarModalEditarServicio();
            loadTabData('servicios');
        } else {
            const err = await res.json();
            alert('Error: ' + err.error);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }
}