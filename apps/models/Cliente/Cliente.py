import re

class Cliente:
    def __init__(self, dni, nombre, apellido, telefono):
        self.dni = self._validar_dni(dni)
        self.nombre = self._validar_nombre(nombre)
        self.apellido = self._validar_apellido(apellido)
        self.telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_dni(dni):
        """Valida el DNI y retorna el valor si es válido."""
        if not dni:
            raise ValueError("El DNI es obligatorio")
        
        dni_str = str(dni).strip().replace('.', '')
        
        if not dni_str.isdigit():
            raise ValueError("El DNI debe contener solo números")
        
        if len(dni_str) < 7 or len(dni_str) > 8:
            raise ValueError("El DNI debe tener entre 7 y 8 dígitos")
        
        if dni_str == "0" * len(dni_str):
            raise ValueError("El DNI no puede ser un número inválido")
        
        return int(dni_str)
    
    @staticmethod
    def _validar_nombre(nombre):
        """Valida el nombre y retorna el valor limpio si es válido."""
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre es obligatorio")
        
        nombre_limpio = str(nombre).strip()
        
        if len(nombre_limpio) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        
        if len(nombre_limpio) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_limpio):
            raise ValueError("El nombre solo puede contener letras y espacios")
        
        return nombre_limpio
    
    @staticmethod
    def _validar_apellido(apellido):
        """Valida el apellido y retorna el valor limpio si es válido."""
        if not apellido or not str(apellido).strip():
            raise ValueError("El apellido es obligatorio")
        
        apellido_limpio = str(apellido).strip()
        
        if len(apellido_limpio) < 2:
            raise ValueError("El apellido debe tener al menos 2 caracteres")
        
        if len(apellido_limpio) > 100:
            raise ValueError("El apellido no puede exceder 100 caracteres")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido_limpio):
            raise ValueError("El apellido solo puede contener letras y espacios")
        
        return apellido_limpio
    
    @staticmethod
    def _validar_telefono(telefono):
        """Valida el teléfono y retorna el valor si es válido."""
        if not telefono:
            raise ValueError("El teléfono es obligatorio")
        
        telefono_limpio = str(telefono).replace(' ', '').replace('-', '')
        
        if not re.match(r'^[0-9]{7,15}$', telefono_limpio):
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos")
        
        return telefono_limpio

    def atualizar_telefono(self, novo_telefono):
        """Actualiza el teléfono después de validarlo."""
        self.telefono = self._validar_telefono(novo_telefono)

    def __str__(self):
        return f"Cliente(dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, telefono={self.telefono})"