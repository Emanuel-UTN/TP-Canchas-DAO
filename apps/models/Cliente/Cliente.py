from models.Validaciones import Validaciones

class Cliente:
    def __init__(self, dni, nombre, apellido, telefono):
        self.dni = Validaciones.esDNIValido(dni)
        self.nombre = Validaciones.esTextoValido(nombre, "Nombre")
        self.apellido = Validaciones.esTextoValido(apellido, "Apellido")
        self.telefono = Validaciones.esTelefonoValido(telefono)

    def atualizar_telefono(self, novo_telefono):
        """Actualiza el teléfono después de validarlo."""
        self.telefono = Validaciones.esTelefonoValido(novo_telefono)

    def __str__(self):
        return f"Cliente(dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, telefono={self.telefono})"