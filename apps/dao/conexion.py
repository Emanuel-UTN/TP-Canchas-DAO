import sqlite3
import os

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            
            # Obtener la ruta absoluta del directorio donde está este archivo (apps/dao)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Subir un nivel para llegar a la carpeta 'apps' (donde está la BD)
            apps_dir = os.path.dirname(current_dir)
            
            # Construir la ruta completa a la base de datos
            db_path = os.path.join(apps_dir, "bd_canchas.db")
            
            # Imprimir para depuración (puedes borrarlo después)
            print(f"Conectando a base de datos en: {db_path}")

            cls._instancia._conexion = sqlite3.connect(db_path, check_same_thread=False)
            cls._instancia._conexion.row_factory = sqlite3.Row
        return cls._instancia

    def obtener_conexion(self):
        return self._conexion

    def cerrar_conexion(self):
        if self._conexion:
            self._conexion.close()
            ConexionDB._instancia = None