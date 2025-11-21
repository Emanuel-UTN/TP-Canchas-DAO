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

// Variable to store the element that had focus before the modal opened
let previouslyFocusedElement = null;

async function editarCliente(dni) {
    try {
        const res = await fetch(`/api/clientes/${dni}`);
        if (!res.ok) {
            const error = await res.json();
            alert('Error: ' + (error.error || 'No se pudo obtener el cliente'));
            return;
        }
        const cliente = await res.json();
        
        // Store the currently focused element
        previouslyFocusedElement = document.activeElement;
        
        // Mostrar modal
        const modal = document.getElementById("modal-editar");
        modal.style.display = "block";

        // Cargar datos
        document.getElementById("edit-dni").value = cliente.dni;
        document.getElementById("edit-nombre").value = cliente.nombre;
        document.getElementById("edit-apellido").value = cliente.apellido;
        document.getElementById("edit-telefono").value = cliente.telefono;
        
        // Set focus to the first editable field
        setTimeout(() => {
            document.getElementById("edit-nombre").focus();
        }, 100);
        
        // Remove any existing listener before adding to prevent duplicates
        modal.removeEventListener('keydown', handleModalKeydown);
        // Add keyboard event listener for Escape key
        modal.addEventListener('keydown', handleModalKeydown);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function cerrarModalEditar() {
    const modal = document.getElementById("modal-editar");
    modal.style.display = "none";
    
    // Remove keyboard event listener
    modal.removeEventListener('keydown', handleModalKeydown);
    
    // Restore focus to the previously focused element
    if (previouslyFocusedElement) {
        previouslyFocusedElement.focus();
        previouslyFocusedElement = null;
    }
}

function handleModalKeydown(event) {
    const modal = document.getElementById("modal-editar");
    
    // Close modal on Escape key
    if (event.key === 'Escape') {
        event.preventDefault();
        cerrarModalEditar();
        return;
    }
    
    // Focus trap - keep focus within modal
    if (event.key === 'Tab') {
        const focusableElements = modal.querySelectorAll(
            'input:not([readonly]):not([disabled]), button:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
        );
        
        // Check if there are any focusable elements
        if (focusableElements.length === 0) return;
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (event.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstElement) {
                event.preventDefault();
                lastElement.focus();
            }
        } else {
            // Tab
            if (document.activeElement === lastElement) {
                event.preventDefault();
                firstElement.focus();
            }
        }
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
        cerrarModalEditar();
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