class Cliente:
    def __init__(self, dni, nombre, apellido, telefono):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def atualizar_telefono(self, novo_telefono):
        self.telefono = novo_telefono

    def __str__(self):
        return f"Cliente(dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, telefono={self.telefono})"