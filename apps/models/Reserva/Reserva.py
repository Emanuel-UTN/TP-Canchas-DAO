from models.Cancha.Cancha import Cancha
from models.Cliente.Cliente import Cliente
from models.Pago.Pago import Pago
from models.Reserva.EstadoReserva import EstadoReserva
from datetime import datetime, timedelta

class Reserva:
    def __init__(self, nro_reserva, cliente: Cliente, cancha: Cancha, fecha_hora_inicio, horas: int, pago: Pago):
        self.nro_reserva = nro_reserva
        self.fecha_hora_inicio = self._validar_fecha_hora_inicio(fecha_hora_inicio)
        self.horas = self._validar_horas(horas)
        self.cliente = cliente
        self.cancha = cancha
        self.estado = EstadoReserva.PENDIENTE
        self.pago = pago
    
    @staticmethod
    def _validar_fecha_hora_inicio(fecha_hora_inicio):
        """Valida la fecha y hora de inicio de la reserva."""
        if not fecha_hora_inicio:
            raise ValueError("La fecha y hora de inicio es requerida")
        
        try:
            if isinstance(fecha_hora_inicio, str):
                fecha_str = fecha_hora_inicio.replace('Z', '+00:00')
                fecha_obj = datetime.fromisoformat(fecha_str)
            else:
                fecha_obj = fecha_hora_inicio
        except (ValueError, AttributeError):
            raise ValueError("La fecha y hora de inicio no es válida")
        
        if fecha_obj.minute != 0:
            raise ValueError("La fecha y hora de inicio debe tener los minutos en 00")
        
        ahora = datetime.now()
        if fecha_obj < ahora:
            raise ValueError("La fecha y hora de inicio debe ser una fecha futura")
        
        fecha_maxima = ahora + timedelta(days=90)
        if fecha_obj > fecha_maxima:
            raise ValueError("No se pueden hacer reservas con más de 3 meses de anticipación")
        
        return fecha_hora_inicio
    
    @staticmethod
    def _validar_horas(horas):
        """Valida la cantidad de horas de la reserva."""
        try:
            horas_int = int(horas)
        except (ValueError, TypeError):
            raise ValueError("La cantidad de horas debe ser un número entero válido")
        
        if horas_int <= 0:
            raise ValueError("La cantidad de horas debe ser un número entero positivo")
        
        if horas_int > 6:
            raise ValueError("La cantidad de horas no puede exceder 6")
        
        return horas_int

    def confirmar_reserva(self):
        if self.estado == EstadoReserva.PENDIENTE:
            self.estado = EstadoReserva.CONFIRMADA
    
    def cancelar_reserva(self):
        if self.estado in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]:
            self.estado = EstadoReserva.CANCELADA
    
    def procesar_pago(self):
        if self.pago.realizar_pago():
            self.confirmar_reserva()

    def completar_reserva(self):
        if self.estado == EstadoReserva.CONFIRMADA:
            self.estado = EstadoReserva.COMPLETADA
    
    def get_estado(self):
        if self.estado == EstadoReserva.PENDIENTE:
            return "Pendiente"
        elif self.estado == EstadoReserva.CONFIRMADA:
            return "Confirmada"
        elif self.estado == EstadoReserva.CANCELADA:
            return "Cancelada"
        elif self.estado == EstadoReserva.COMPLETADA:
            return "Completada"
        else:
            return "Desconocido"
