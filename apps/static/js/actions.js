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