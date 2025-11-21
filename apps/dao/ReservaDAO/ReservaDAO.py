from dao.conexion import ConexionDB
from models.Reserva.Reserva import Reserva

class ReservaDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reserva (
                nro_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora_inicio DATETIME,
                horas INTEGER,
                nro_cancha INTEGER,
                dni_cliente INTEGER,
                id_pago INTEGER,
                id_estado INTEGER,
                
                FOREIGN KEY (nro_cancha) REFERENCES Cancha(nro_cancha)
                FOREIGN KEY (dni_cliente) REFERENCES Cliente(dni_cliente)
                FOREIGN KEY (id_pago) REFERENCES Pago(id_pago)
                FOREIGN KEY (id_estado) REFERENCES EstadoReserva(id_estado)
                )
        ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_reserva(reserva: Reserva):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Reserva (fecha_hora_inicio, horas, nro_cancha, dni_cliente, id_pago, id_estado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (reserva.fecha_hora_inicio, reserva.horas, reserva.nro_cancha, reserva.dni_cliente, reserva.id_pago, reserva.id_estado))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_reserva(nro_reserva: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Reserva WHERE nro_reserva = ?''', (nro_reserva,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_reservas():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        reservas = []
        cursor.execute('''SELECT nro_reserva, fecha_hora_inicio, horas, nro_cancha, dni_cliente, id_pago, id_estado FROM Reserva''')
        filas = cursor.fetchall()
        for fila in filas:
            reserva = Reserva(
                nro_reserva=fila[0],
                fecha_hora_inicio=fila[1],
                horas=fila[2],
                nro_cancha=fila[3],
                dni_cliente=fila[4],
                id_pago=fila[5],
                id_estado=fila[6]
            )
            reservas.append(reserva)
        cursor.close()
        return reservas
    
    @staticmethod
    def modificar_reserva(reserva: Reserva):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Reserva
            SET fecha_hora_inicio = ?, horas = ?, nro_cancha = ?, dni_cliente = ?, id_pago = ?, id_estado = ?
            WHERE nro_reserva = ?
        ''', (reserva.fecha_hora_inicio, reserva.horas, reserva.nro_cancha, reserva.dni_cliente, reserva.id_pago, reserva.id_estado, reserva.nro_reserva))
        conexion.commit()
        cursor.close()
    
    