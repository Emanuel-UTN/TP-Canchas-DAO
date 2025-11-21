// Funciones de carga de datos y configuración de endpoints
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