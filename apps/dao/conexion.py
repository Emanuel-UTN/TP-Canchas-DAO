import sqlite3

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._conexion = sqlite3.connect("bd_canchas.db")
            cls._instancia._conexion.row_factory = sqlite3.Row
        return cls._instancia

    def obtener_conexion(self):
        return self._conexion

    def cerrar_conexion(self):
        if self._conexion:
            self._conexion.close()
            ConexionDB._instancia = None
