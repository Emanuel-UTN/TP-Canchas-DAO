class Servicio:
    def __init__(self, servicio :  str, costo : float):
        self.servicio = self._validar_nombre_servicio(servicio)
        self.costo = self._validar_costo(costo)
    
    @staticmethod
    def _validar_nombre_servicio(servicio):
        """Valida el nombre del servicio y retorna el valor limpio si es válido."""
        if not servicio or not str(servicio).strip():
            raise ValueError("El nombre del servicio es obligatorio")
        
        servicio_limpio = str(servicio).strip()
        
        if len(servicio_limpio) < 2:
            raise ValueError("El nombre del servicio debe tener al menos 2 caracteres")
        
        if len(servicio_limpio) > 100:
            raise ValueError("El nombre del servicio no puede exceder 100 caracteres")
        
        return servicio_limpio
    
    @staticmethod
    def _validar_costo(costo):
        """Valida el costo del servicio y retorna el valor si es válido."""
        try:
            costo_num = float(costo)
        except (ValueError, TypeError):
            raise ValueError("El costo debe ser un número válido")
        
        if costo_num <= 0:
            raise ValueError("El costo debe ser un número positivo")
        
        return costo_num

    def __str__(self):
        return f"Servicio: {self.servicio}, Costo: {self.costo}"