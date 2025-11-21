from models.Pago.MetodoPago import MetodoPago
from datetime import datetime

class Pago:
    def __init__(self, metodo_pago: MetodoPago, fecha_hora, monto):
        self.metodo_pago = metodo_pago
        self.fecha_hora = self._validar_fecha_hora(fecha_hora)
        self.monto = self._validar_monto(monto)
    
    @staticmethod
    def _validar_fecha_hora(fecha_hora):
        """Valida la fecha y hora del pago."""
        if not fecha_hora:
            raise ValueError("La fecha y hora del pago es requerida")
        
        try:
            if isinstance(fecha_hora, str):
                fecha_str = fecha_hora.replace('Z', '+00:00')
                fecha_obj = datetime.fromisoformat(fecha_str)
            else:
                fecha_obj = fecha_hora
        except (ValueError, AttributeError):
            raise ValueError("La fecha y hora del pago no es válida")
        
        if fecha_obj.minute != 0:
            raise ValueError("La fecha y hora del pago debe tener los minutos en 00")
        
        return fecha_hora
    
    @staticmethod
    def _validar_monto(monto):
        """Valida el monto del pago."""
        try:
            monto_num = float(monto)
        except (ValueError, TypeError):
            raise ValueError("El monto debe ser un número válido")
        
        if monto_num <= 0:
            raise ValueError("El monto debe ser un número positivo")
        
        return monto_num

    def procesar_pago(self):
        self.metodo_pago.procesar_pago(self.monto)