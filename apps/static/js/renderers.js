// Renderizadores de tablas
function renderClientes(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay clientes registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>DNI</th><th>Nombre</th><th>Apellido</th><th>Teléfono</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(cliente => {
        html += `<tr>
            <td>${cliente.dni}</td>
            <td>${cliente.nombre}</td>
            <td>${cliente.apellido}</td>
            <td>${cliente.telefono}</td>
            <td><button class="btn btn-danger" onclick="eliminarCliente(${cliente.dni})">Eliminar</button></td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderCanchas(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay canchas registradas</div>';
        return;
    }
    let html = '<table><thead><tr><th>Nro. Cancha</th><th>Tipo</th><th>Servicios</th><th>Costo por Hora</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(cancha => {
        // preparar listado de servicios (puede ser array de strings o array de objetos)
        let serviciosText = '';
        if (Array.isArray(cancha.servicios) && cancha.servicios.length > 0) {
            serviciosText = cancha.servicios.map(s => {
                if (typeof s === 'string') return s;
                if (s && typeof s === 'object') return s.servicio ?? s.nombre ?? '';
                return '';
            }).filter(Boolean).join(', ');
        } else {
            serviciosText = '—';
        }

        html += `<tr>
            <td>${cancha.nro_cancha}</td>
            <td>${cancha.tipo}</td>
            <td>${serviciosText}</td>
            <td>$${cancha.costo_por_hora}</td>
            <td><button class="btn btn-danger" onclick="eliminarCancha(${cancha.nro_cancha})">Eliminar</button></td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderReservas(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay reservas registradas</div>';
        return;
    }

    function formatDate(d){
        const pad = n => String(n).padStart(2, '0');
        let fechaFormateada = 'Fecha inválida';
        if (!isNaN(d)) {
            fechaFormateada = `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
        }
        return fechaFormateada
    }

    let html = '<table><thead><tr><th>Nro. Reserva</th><th>Fecha Inicio</th><th>Horas</th><th>Cancha</th><th>Cliente</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(reserva => {
        html += `<tr>
            <td>${reserva.nro_reserva}</td>
            <td>${formatDate(new Date(reserva.fecha_hora_inicio))}</td>
            <td>${reserva.horas}</td>
            <td>${reserva.cancha.nro_cancha} - ${reserva.cancha.tipo}</td>
            <td>${reserva.cliente.nombre} ${reserva.cliente.apellido}</td>
            <td>${reserva.estado}</td>
            <td><button class="btn btn-danger" onclick="eliminarReserva(${reserva.nro_reserva})">Eliminar</button></td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderPagos(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay pagos registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>Método</th><th>Fecha</th><th>Monto</th></tr></thead><tbody>';
    data.forEach(pago => {
        html += `<tr>
            <td>${pago.id_metodo_pago}</td>
            <td>${pago.fecha_hora}</td>
            <td>$${pago.monto}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderTorneos(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay torneos registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>ID</th><th>Fecha Inicio</th><th>Fecha Fin</th><th>Costo Inscripción</th><th>Premio</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(torneo => {
        html += `<tr>
            <td>${torneo.id}</td>
            <td>${torneo.fecha_inicio}</td>
            <td>${torneo.fecha_fin}</td>
            <td>$${torneo.costo_inscripcion}</td>
            <td>$${torneo.premio}</td>
            <td><button class="btn btn-danger" onclick="eliminarTorneo(${torneo.id})">Eliminar</button></td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderTiposCancha(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay tipos de cancha registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>Tipo</th></tr></thead><tbody>';
    data.forEach(tipo => {
        html += `<tr>
            <td>${tipo.tipo}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderServicios(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay servicios registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>Servicio</th><th>Costo</th></tr></thead><tbody>';
    data.forEach(servicio => {
        html += `<tr>
            <td>${servicio.servicio}</td>
            <td>$${servicio.costo}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderMetodosPago(data, container) {
    if (!Array.isArray(data)) {
        container.innerHTML = `<div class="empty-state">Error: ${data.error || 'Formato de datos inválido'}</div>`;
        return;
    }
    if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay métodos de pago registrados</div>';
        return;
    }
    let html = '<table><thead><tr><th>Método</th></tr></thead><tbody>';
    data.forEach(metodo => {
        html += `<tr>
            <td>${metodo.metodo}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}