class MetodoPago:
    def __init__(self, metodo):
        self._validar_metodo(metodo)
        self.metodo = metodo.strip()

    def _validar_metodo(self, metodo):
        if metodo is None:
            raise ValueError("El método de pago no puede ser nulo")
        metodo_limpio = metodo.strip()
        if len(metodo_limpio) < 3:
            raise ValueError("El método de pago debe tener al menos 3 caracteres")
        if len(metodo_limpio) > 50:
            raise ValueError("El método de pago no puede superar 50 caracteres")

    def procesar_pago(self, monto):
        print(f"Procesando pago de {monto} a través del método {self.metodo}")