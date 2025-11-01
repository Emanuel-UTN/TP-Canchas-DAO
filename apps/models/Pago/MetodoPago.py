class MetodoPago:
    def __init__(self, metodo):
        self.metodo = metodo

    def procesar_pago(self, monto):
        print(f"Procesando pago de {monto} a través del método {self.metodo}")