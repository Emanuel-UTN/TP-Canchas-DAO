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