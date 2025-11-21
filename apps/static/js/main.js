// Validaciones reutilizables
const Validaciones = {
    esNumeroPositivo: (valor, nombreCampo) => {
        const num = parseFloat(valor);
        if (isNaN(num) || num <= 0) {
            return `${nombreCampo} debe ser un número positivo`;
        }
        return null;
    },
    
    esEnteroPositivo: (valor, nombreCampo) => {
        const num = parseInt(valor);
        if (isNaN(num) || num <= 0 || !Number.isInteger(num)) {
            return `${nombreCampo} debe ser un número entero positivo`;
        }
        return null;
    },
    
    esDNIValido: (dni) => {
        const num = parseInt(dni);
        if (isNaN(num) || num < 1000000 || num > 99999999) {
            return 'El DNI debe tener entre 7 y 8 dígitos';
        }
        return null;
    },
    
    esTelefonoValido: (telefono) => {
        const regex = /^[0-9]{7,15}$/;
        if (!regex.test(telefono.replace(/[\s-]/g, ''))) {
            return 'El teléfono debe contener entre 7 y 15 dígitos';
        }
        return null;
    },
    
    esTextoValido: (texto, nombreCampo, minLength = 2, maxLength = 100) => {
        const trimmed = texto.trim();
        if (trimmed.length < minLength) {
            return `${nombreCampo} debe tener al menos ${minLength} caracteres`;
        }
        if (trimmed.length > maxLength) {
            return `${nombreCampo} no puede exceder ${maxLength} caracteres`;
        }
        if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(trimmed)) {
            return `${nombreCampo} solo puede contener letras y espacios`;
        }
        return null;
    },
    
    esFechaValida: (fecha, nombreCampo) => {
        if (!fecha) {
            return `${nombreCampo} es requerida`;
        }
        const fechaObj = new Date(fecha);
        if (isNaN(fechaObj.getTime())) {
            return `${nombreCampo} no es válida`;
        }
        return null;
    },
    
    esFechaFutura: (fecha, nombreCampo) => {
        const error = Validaciones.esFechaValida(fecha, nombreCampo);
        if (error) return error;
        
        const fechaObj = new Date(fecha);
        const ahora = new Date();
        if (fechaObj < ahora) {
            return `${nombreCampo} debe ser una fecha futura`;
        }
        return null;
    },
    
    esFechaPosterior: (fechaInicio, fechaFin) => {
        const inicio = new Date(fechaInicio);
        const fin = new Date(fechaFin);
        if (fin <= inicio) {
            return 'La fecha de fin debe ser posterior a la fecha de inicio';
        }
        return null;
    },
    
    mostrarErrores: (errores) => {
        if (errores.length > 0) {
            alert('Errores de validación:\n\n' + errores.join('\n'));
            return true;
        }
        return false;
    }
};

// Funciones de navegación
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

function showForm(type) {
    document.getElementById(`form-${type}`).style.display = 'block';
}

function cancelarForm(type) {
    document.getElementById(`form-${type}`).style.display = 'none';
    document.getElementById(`form-${type}`).querySelector('form').reset();
}

// Funciones de carga de datos
async function loadTabData(tabName) {
    const endpoints = {
        'clientes': '/api/clientes',
        'canchas': '/api/canchas',
        'reservas': '/api/reservas',
        'pagos': '/api/pagos',
        'torneos': '/api/torneos',
        'tipos-cancha': '/api/tipos-cancha',
        'servicios': '/api/servicios',
        'metodos-pago': '/api/metodos-pago'
    };

    const containers = {
        'clientes': 'clientes-table-container',
        'canchas': 'canchas-table-container',
        'reservas': 'reservas-table-container',
        'pagos': 'pagos-table-container',
        'torneos': 'torneos-table-container',
        'tipos-cancha': 'tipos-cancha-table-container',
        'servicios': 'servicios-table-container',
        'metodos-pago': 'metodos-pago-table-container'
    };

    const renderers = {
        'clientes': renderClientes,
        'canchas': renderCanchas,
        'reservas': renderReservas,
        'pagos': renderPagos,
        'torneos': renderTorneos,
        'tipos-cancha': renderTiposCancha,
        'servicios': renderServicios,
        'metodos-pago': renderMetodosPago
    };

    try {
        const response = await fetch(endpoints[tabName]);
        const data = await response.json();
        const container = document.getElementById(containers[tabName]);
        renderers[tabName](data, container);
    } catch (error) {
        document.getElementById(containers[tabName]).innerHTML = 
            `<div class="empty-state">Error al cargar datos: ${error.message}</div>`;
    }
}

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
    let html = '<table><thead><tr><th>Nro. Cancha</th><th>ID Tipo</th><th>Costo por Hora</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(cancha => {
        html += `<tr>
            <td>${cancha.nro_cancha}</td>
            <td>${cancha.id_tipo}</td>
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
    let html = '<table><thead><tr><th>Nro. Reserva</th><th>Fecha Inicio</th><th>Horas</th><th>Cancha</th><th>Cliente</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>';
    data.forEach(reserva => {
        html += `<tr>
            <td>${reserva.nro_reserva}</td>
            <td>${reserva.fecha_hora_inicio}</td>
            <td>${reserva.horas}</td>
            <td>${reserva.nro_cancha}</td>
            <td>${reserva.dni_cliente}</td>
            <td>${reserva.id_estado}</td>
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
    let html = '<table><thead><tr><th>ID Pago</th><th>Método</th><th>Fecha</th><th>Monto</th></tr></thead><tbody>';
    data.forEach(pago => {
        html += `<tr>
            <td>${pago.id_pago}</td>
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
    let html = '<table><thead><tr><th>ID</th><th>Tipo</th></tr></thead><tbody>';
    data.forEach(tipo => {
        html += `<tr>
            <td>${tipo.id_tipo}</td>
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
    let html = '<table><thead><tr><th>ID</th><th>Servicio</th><th>Costo</th></tr></thead><tbody>';
    data.forEach(servicio => {
        html += `<tr>
            <td>${servicio.id_servicio}</td>
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
    let html = '<table><thead><tr><th>ID</th><th>Método</th></tr></thead><tbody>';
    data.forEach(metodo => {
        html += `<tr>
            <td>${metodo.id_metodo_pago}</td>
            <td>${metodo.metodo}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

// Funciones de guardado
async function guardarCliente(event) {
    event.preventDefault();
    
    const dni = document.getElementById('cliente-dni').value;
    const nombre = document.getElementById('cliente-nombre').value;
    const apellido = document.getElementById('cliente-apellido').value;
    const telefono = document.getElementById('cliente-telefono').value;
    
    const errores = [];
    
    const errorDNI = Validaciones.esDNIValido(dni);
    if (errorDNI) errores.push(errorDNI);
    
    const errorNombre = Validaciones.esTextoValido(nombre, 'Nombre');
    if (errorNombre) errores.push(errorNombre);
    
    const errorApellido = Validaciones.esTextoValido(apellido, 'Apellido');
    if (errorApellido) errores.push(errorApellido);
    
    const errorTelefono = Validaciones.esTelefonoValido(telefono);
    if (errorTelefono) errores.push(errorTelefono);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        dni: parseInt(dni),
        nombre: nombre.trim(),
        apellido: apellido.trim(),
        telefono: telefono.replace(/[\s-]/g, '')
    };
    try {
        const response = await fetch('/api/clientes', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Cliente agregado exitosamente');
            cancelarForm('cliente');
            loadTabData('clientes');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarCancha(event) {
    event.preventDefault();
    
    const idTipo = document.getElementById('cancha-id-tipo').value;
    const costo = document.getElementById('cancha-costo').value;
    
    const errores = [];
    
    const errorIdTipo = Validaciones.esEnteroPositivo(idTipo, 'ID del tipo de cancha');
    if (errorIdTipo) errores.push(errorIdTipo);
    
    const errorCosto = Validaciones.esNumeroPositivo(costo, 'Costo por hora');
    if (errorCosto) errores.push(errorCosto);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        id_tipo: parseInt(idTipo),
        costo_por_hora: parseFloat(costo)
    };
    try {
        const response = await fetch('/api/canchas', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Cancha agregada exitosamente');
            cancelarForm('cancha');
            loadTabData('canchas');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarReserva(event) {
    event.preventDefault();
    
    const fecha = document.getElementById('reserva-fecha').value;
    const horas = document.getElementById('reserva-horas').value;
    const nroCancha = document.getElementById('reserva-cancha').value;
    const dniCliente = document.getElementById('reserva-cliente').value;
    const idPago = document.getElementById('reserva-pago').value;
    const idEstado = document.getElementById('reserva-estado').value;
    
    const errores = [];
    
    const errorFecha = Validaciones.esFechaFutura(fecha, 'Fecha y hora de inicio');
    if (errorFecha) errores.push(errorFecha);
    
    const errorHoras = Validaciones.esEnteroPositivo(horas, 'Cantidad de horas');
    if (errorHoras) errores.push(errorHoras);
    else if (parseInt(horas) > 12) errores.push('La cantidad de horas no puede exceder 12');
    
    const errorCancha = Validaciones.esEnteroPositivo(nroCancha, 'Número de cancha');
    if (errorCancha) errores.push(errorCancha);
    
    const errorCliente = Validaciones.esDNIValido(dniCliente);
    if (errorCliente) errores.push(errorCliente);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        fecha_hora_inicio: fecha,
        horas: parseInt(horas),
        nro_cancha: parseInt(nroCancha),
        dni_cliente: parseInt(dniCliente),
        id_pago: idPago ? parseInt(idPago) : null,
        id_estado: idEstado ? parseInt(idEstado) : 1
    };
    try {
        const response = await fetch('/api/reservas', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Reserva agregada exitosamente');
            cancelarForm('reserva');
            loadTabData('reservas');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarPago(event) {
    event.preventDefault();
    
    const idMetodo = document.getElementById('pago-metodo').value;
    const fecha = document.getElementById('pago-fecha').value;
    const monto = document.getElementById('pago-monto').value;
    
    const errores = [];
    
    const errorMetodo = Validaciones.esEnteroPositivo(idMetodo, 'ID del método de pago');
    if (errorMetodo) errores.push(errorMetodo);
    
    const errorFecha = Validaciones.esFechaValida(fecha, 'Fecha y hora del pago');
    if (errorFecha) errores.push(errorFecha);
    
    const errorMonto = Validaciones.esNumeroPositivo(monto, 'Monto');
    if (errorMonto) errores.push(errorMonto);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        id_metodo_pago: parseInt(idMetodo),
        fecha_hora: fecha,
        monto: parseFloat(monto)
    };
    try {
        const response = await fetch('/api/pagos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Pago agregado exitosamente');
            cancelarForm('pago');
            loadTabData('pagos');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarTorneo(event) {
    event.preventDefault();
    
    const fechaInicio = document.getElementById('torneo-inicio').value;
    const fechaFin = document.getElementById('torneo-fin').value;
    const costoInscripcion = document.getElementById('torneo-costo').value;
    const premio = document.getElementById('torneo-premio').value;
    
    const errores = [];
    
    const errorInicio = Validaciones.esFechaFutura(fechaInicio, 'Fecha de inicio');
    if (errorInicio) errores.push(errorInicio);
    
    const errorFin = Validaciones.esFechaValida(fechaFin, 'Fecha de fin');
    if (errorFin) errores.push(errorFin);
    
    if (!errorInicio && !errorFin) {
        const errorPosterior = Validaciones.esFechaPosterior(fechaInicio, fechaFin);
        if (errorPosterior) errores.push(errorPosterior);
    }
    
    const errorCosto = Validaciones.esNumeroPositivo(costoInscripcion, 'Costo de inscripción');
    if (errorCosto) errores.push(errorCosto);
    
    const errorPremio = Validaciones.esNumeroPositivo(premio, 'Premio');
    if (errorPremio) errores.push(errorPremio);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
        costo_inscripcion: parseFloat(costoInscripcion),
        premio: parseFloat(premio)
    };
    try {
        const response = await fetch('/api/torneos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Torneo agregado exitosamente');
            cancelarForm('torneo');
            loadTabData('torneos');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarTipoCancha(event) {
    event.preventDefault();
    
    const tipo = document.getElementById('tipo-cancha-nombre').value;
    
    const errores = [];
    
    const errorTipo = Validaciones.esTextoValido(tipo, 'Tipo de cancha', 3, 50);
    if (errorTipo) errores.push(errorTipo);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        tipo: tipo.trim()
    };
    try {
        const response = await fetch('/api/tipos-cancha', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Tipo de cancha agregado exitosamente');
            cancelarForm('tipo-cancha');
            loadTabData('tipos-cancha');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarServicio(event) {
    event.preventDefault();
    
    const servicio = document.getElementById('servicio-nombre').value;
    const costo = document.getElementById('servicio-costo').value;
    
    const errores = [];
    
    const errorServicio = Validaciones.esTextoValido(servicio, 'Nombre del servicio', 3, 100);
    if (errorServicio) errores.push(errorServicio);
    
    const errorCosto = Validaciones.esNumeroPositivo(costo, 'Costo');
    if (errorCosto) errores.push(errorCosto);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        servicio: servicio.trim(),
        costo: parseFloat(costo)
    };
    try {
        const response = await fetch('/api/servicios', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Servicio agregado exitosamente');
            cancelarForm('servicio');
            loadTabData('servicios');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function guardarMetodoPago(event) {
    event.preventDefault();
    
    const metodo = document.getElementById('metodo-pago-nombre').value;
    
    const errores = [];
    
    const errorMetodo = Validaciones.esTextoValido(metodo, 'Método de pago', 3, 50);
    if (errorMetodo) errores.push(errorMetodo);
    
    if (Validaciones.mostrarErrores(errores)) return;
    
    const data = {
        metodo: metodo.trim()
    };
    try {
        const response = await fetch('/api/metodos-pago', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Método de pago agregado exitosamente');
            cancelarForm('metodo-pago');
            loadTabData('metodos-pago');
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

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

// Cargar datos iniciales
window.onload = function() {
    loadTabData('clientes');
};