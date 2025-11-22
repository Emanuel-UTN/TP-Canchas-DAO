from models.Validaciones import Validaciones

class Servicio:
    def __init__(self, servicio :  str, costo : float):
        self.servicio = Validaciones.esTextoValido(servicio, "Servicio")
        self.costo = Validaciones.esNumeroPositivo(costo, "Costo")

    def __str__(self):
        return f"Servicio: {self.servicio}, Costo: {self.costo}"