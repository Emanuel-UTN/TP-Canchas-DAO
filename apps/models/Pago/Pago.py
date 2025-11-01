import MetodoPago

class Pago:
    def __init__(self, metodo_pago: MetodoPago.MetodoPago, fecha_hora, monto):
        self.metodo_pago = metodo_pago
        self.fecha_hora = fecha_hora
        self.monto = monto

    def procesar_pago(self):
        self.metodo_pago.procesar_pago(self.monto)