class Servicio:
    def __init__(self, servicio :  str, costo : float):
        self.servicio = servicio
        self.costo = costo

    def __str__(self):
        return f"Servicio: {self.servicio}, Costo: {self.costo}"