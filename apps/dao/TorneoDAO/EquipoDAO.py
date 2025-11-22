from dao.conexion import ConexionDB
from models.Torneo.Equipo import Equipo
from dao.ClienteDAO.ClienteDAO import ClienteDAO

class EquipoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Equipo (
                id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
                dni_delegado INTEGER NOT NULL,
                nombre VARCHAR(50) NOT NULL CHECK(length(trim(nombre)) >= 2),
                FOREIGN KEY (dni_delegado) REFERENCES Cliente(dni)
                )
            ''')
    
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_equipo(equipo: Equipo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Equipo (dni_delegado, nombre)
            VALUES (?, ?)
        ''', (equipo.delegado.dni, equipo.nombre))
        conexion.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    
    @staticmethod
    def eliminar_equipo(id_equipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Equipo WHERE id_equipo = ?''', (id_equipo,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_equipos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        equipos = []
        cursor.execute('''SELECT id_equipo, dni_delegado, nombre FROM Equipo''')
        filas = cursor.fetchall()
        for fila in filas:
            equipo = Equipo(
                delegado=ClienteDAO.obtener_cliente_por_dni(fila[1]),
                nombre=fila[2]
            )
            equipos.append(equipo)
        cursor.close()
        return equipos
    
    @staticmethod
    def obtener_equipo_por_id(id_equipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_equipo, dni_delegado, nombre FROM Equipo WHERE id_equipo = ?''', (id_equipo,))
        fila = cursor.fetchone()
        equipo = None
        if fila:
            equipo = Equipo(
                delegado=ClienteDAO.obtener_cliente_por_dni(fila[1]),
                nombre=fila[2]
            )
        cursor.close()
        return equipo
    
    @staticmethod
    def obtener_equipo_por_nombre_y_delegado(nombre: str, dni_delegado: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_equipo, dni_delegado, nombre FROM Equipo WHERE nombre = ? AND dni_delegado = ?''', (nombre, dni_delegado))
        fila = cursor.fetchone()
        equipo = None
        if fila:
            equipo = Equipo(
                delegado=ClienteDAO.obtener_cliente_por_dni(fila[1]),
                nombre=fila[2]
            )
        cursor.close()
        return equipo, fila[0] if fila else None
    
    @staticmethod
    def modificar_equipo(equipo: Equipo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Equipo
            SET dni_delegado = ?, nombre = ?
            WHERE id_equipo = ?
        ''', (equipo.dni_delegado, equipo.nombre, equipo.id_equipo))
        conexion.commit()
        cursor.close()