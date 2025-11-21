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
        }// validar que los minutos sean cero
        else if (fechaObj.getMinutes() !== 0) {
            return `${nombreCampo} debe tener los minutos en 00`;
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
    
    esFechaDentroDeRango: (fecha, nombreCampo, mesesMaximos) => {
        const error = Validaciones.esFechaFutura(fecha, nombreCampo);
        if (error) return error;
        
        const fechaObj = new Date(fecha);
        const ahora = new Date();
        const fechaMaxima = new Date();
        fechaMaxima.setMonth(ahora.getMonth() + mesesMaximos);
        
        if (fechaObj > fechaMaxima) {
            return `${nombreCampo} no puede ser superior a ${mesesMaximos} meses desde hoy`;
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