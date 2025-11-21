from models.Cancha.Cancha import Cancha
from models.Cliente.Cliente import Cliente
from models.Reserva.Reserva import Reserva
from models.Pago.Pago import Pago
from models.Torneo.Torneo import Torneo

class GestorReservas:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.reservas = []
        self.canchas = []
        self.torneos = []
        self.hora_abre = 8  # Hora de apertura (8 AM)
        self.hora_cierra = 22  # Hora de cierre (10 PM)

    def crear_reserva(self, cliente: Cliente, cancha: Cancha, fecha_hora_inicio, horas: int, pago: Pago):
        nro_reserva = len(self.reservas) + 1
        reserva = Reserva(nro_reserva, cliente, cancha, fecha_hora_inicio, horas, pago)
        self.reservas.append(reserva)
        return reserva

    def crear_torneo(self, fecha_inicio, fecha_fin, costo_inscripcion: float, premio: float):
        torneo = Torneo(fecha_inicio, fecha_fin, costo_inscripcion, premio)
        self.torneos.append(torneo)
        return torneo
    
    def agregar_cancha(self, cancha: Cancha):
        self.canchas.append(cancha)

    def obtener_reservas(self):
        return self.reservas

    def obtener_torneos(self):
        return self.torneos
    
    def obtener_canchas(self):
        return self.canchas