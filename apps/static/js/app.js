// Inicialización de la aplicación
window.onload = function() {
    // Determinar qué página estamos viendo basándonos en el contenedor visible
    const containers = [
        'clientes-table-container',
        'canchas-table-container',
        'reservas-table-container',
        'pagos-table-container',
        'torneos-table-container',
        'tipos-cancha-table-container',
        'servicios-table-container',
        'metodos-pago-table-container'
    ];
    
    // Buscar el contenedor que existe en la página actual
    for (let containerId of containers) {
        const container = document.getElementById(containerId);
        if (container) {
            // Extraer el nombre de la página del ID del contenedor
            const tabName = containerId.replace('-table-container', '');
            loadTabData(tabName);
            break;
        }
    }
};