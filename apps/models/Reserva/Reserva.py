from models.Cancha.Cancha import Cancha
from models.Cliente.Cliente import Cliente
from models.Pago.Pago import Pago
from models.Reserva.EstadoReserva import EstadoReserva

class Reserva:
    def __init__(self, nro_reserva, cliente: Cliente, cancha: Cancha, fecha_hora_inicio, horas: int, pago: Pago):
        self.nro_reserva = nro_reserva
        self.fecha_hora_inicio = fecha_hora_inicio
        self.horas = horas
        self.cliente = cliente
        self.cancha = cancha
        self.estado = EstadoReserva.PENDIENTE
        self.pago = pago

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