from models.Validaciones import Validaciones

class TipoCancha:
    def __init__(self, tipo: str):
        self.tipo = Validaciones.esTextoValido(tipo, "Tipo de Cancha")

    def __str__(self):
        return f"TipoCancha(tipo={self.tipo})"