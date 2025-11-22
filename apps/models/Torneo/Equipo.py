from models.Cliente.Cliente import Cliente
from models.Validaciones import Validaciones

class Equipo:
    def __init__(self, nombre: str, delegado: Cliente):
        self.nombre = Validaciones.esTextoValido(nombre, "Nombre del equipo")
        self.delegado = delegado

    def obtener_delegado(self):
        return self.delegado