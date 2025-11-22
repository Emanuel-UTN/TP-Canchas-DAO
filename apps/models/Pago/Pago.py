from models.Pago.MetodoPago import MetodoPago
from datetime import datetime
from models.Validaciones import Validaciones

class Pago:
    def __init__(self, metodo_pago: MetodoPago, fecha_hora, monto):
        self.metodo_pago = metodo_pago
        self.fecha_hora = Validaciones.esFechaValida(fecha_hora, "Fecha y hora del pago")
        self.monto = Validaciones.esNumeroPositivo(monto, "Monto del pago")

    def procesar_pago(self):
        self.metodo_pago.procesar_pago(self.monto)