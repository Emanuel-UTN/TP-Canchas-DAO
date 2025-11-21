
function editarCliente(dni) {
    fetch(`/clientes/${dni}`)
        .then(res => res.json())
        .then(cliente => {
            // abrir modal
            document.getElementById("modal-editar").style.display = "block";

            // cargar datos en inputs
            document.getElementById("edit-dni").value = cliente.dni;
            document.getElementById("edit-nombre").value = cliente.nombre;
            document.getElementById("edit-apellido").value = cliente.apellido;
            document.getElementById("edit-telefono").value = cliente.telefono;
        });
}

function guardarCambiosCliente() {
    const data = {
        nombre: document.getElementById("edit-nombre").value,
        apellido: document.getElementById("edit-apellido").value,
        telefono: document.getElementById("edit-telefono").value,
    };

    fetch(`/clientes/${data.dni}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(() => actualizarTablaClientes());
}