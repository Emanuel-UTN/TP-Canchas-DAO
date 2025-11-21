from models.Cliente.Cliente import Cliente

class Equipo:
    def __init__(self, nombre: str, delegado: Cliente):
        self.nombre = nombre
        self.delegado = delegado

    def obtener_delegado(self):
        return self.delegado