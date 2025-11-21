// Funciones de navegación y UI
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