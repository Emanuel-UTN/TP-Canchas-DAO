// Funciones de guardado de formularios
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