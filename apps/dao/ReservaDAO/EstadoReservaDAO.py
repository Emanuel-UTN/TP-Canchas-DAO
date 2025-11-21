from dao.conexion import ConexionDB
from models.Reserva.EstadoReserva import EstadoReserva

class EstadoReservaDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS EstadoReserva (
                id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
                estado VARCHAR(50)
                )
            ''')

        conexion.commit()
        cursor.close()
    
    @staticmethod
    def agregar_estado_reserva(estado_reserva: EstadoReserva):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO EstadoReserva (estado)
            VALUES (?)
        ''', (estado_reserva.estado,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_estado_reserva(id_estado: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM EstadoReserva WHERE id_estado = ?''', (id_estado,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_estados_reserva():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        estados_reserva = []
        cursor.execute('''SELECT id_estado, estado FROM EstadoReserva''')
        filas = cursor.fetchall()
        for fila in filas:
            estado_reserva = EstadoReservaDAO.obtenerEstadoPorNombre(fila[1])
            estados_reserva.append(estado_reserva)
        cursor.close()
        return estados_reserva
    
    @staticmethod
    def obtener_estado_reserva_por_id(id_estado: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_estado, estado FROM EstadoReserva WHERE id_estado = ?''', (id_estado,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            estado_reserva = EstadoReservaDAO.obtenerEstadoPorNombre(fila[1])
            return estado_reserva
        return None

    @staticmethod
    def modificar_estado_reserva(estado_reserva: EstadoReserva):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE EstadoReserva
            SET estado = ?
            WHERE id_estado = ?
        ''', (estado_reserva.estado, estado_reserva.id_estado))
        conexion.commit()
        cursor.close()
    
    def obtenerEstadoPorNombre(nombre_estado: str):
        if nombre_estado == EstadoReserva.PENDIENTE:
            return EstadoReserva.PENDIENTE
        elif nombre_estado == EstadoReserva.CONFIRMADA:
            return EstadoReserva.CONFIRMADA
        elif nombre_estado == EstadoReserva.CANCELADA:
            return EstadoReserva.CANCELADA
        elif nombre_estado == EstadoReserva.COMPLETADA:
            return EstadoReserva.COMPLETADA