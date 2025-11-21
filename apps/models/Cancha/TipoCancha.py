class TipoCancha:
    def __init__(self, tipo: str):
        self.tipo = self._validar_tipo(tipo)
    
    @staticmethod
    def _validar_tipo(tipo):
        """Valida el tipo de cancha y retorna el valor limpio si es válido."""
        if not tipo or not str(tipo).strip():
            raise ValueError("El tipo de cancha es obligatorio")
        
        tipo_limpio = str(tipo).strip()
        
        if len(tipo_limpio) < 2:
            raise ValueError("El tipo de cancha debe tener al menos 2 caracteres")
        
        if len(tipo_limpio) > 50:
            raise ValueError("El tipo de cancha no puede exceder 50 caracteres")
        
        return tipo_limpio

    def __str__(self):
        return f"TipoCancha(tipo={self.tipo})"