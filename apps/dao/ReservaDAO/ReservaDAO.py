from datetime import datetime, timedelta
from dao.conexion import ConexionDB
from models.Reserva.Reserva import Reserva
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.ClienteDAO.ClienteDAO import ClienteDAO
from dao.PagoDAO.PagoDAO import PagoDAO
from dao.ReservaDAO.EstadoReservaDAO import EstadoReservaDAO

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
        ''', (reserva.fecha_hora_inicio, reserva.horas, reserva.cancha.nro_cancha, reserva.cliente.dni, None, EstadoReservaDAO.obtener_id_estado_reserva_por_nombre("Pendiente")))
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
            reservas.append(ReservaDAO.obtener_reserva(fila))
        cursor.close()
        return reservas
    
    @staticmethod
    def obtener_reserva_por_cancha_y_fecha(nro_cancha: int, fecha_hora_inicio: datetime, fecha_hora_fin: datetime):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        fecha_dia_inicio = fecha_hora_inicio - timedelta(hours=5)  # margen para reservas que empiezan antes pero terminan dentro del rango
        fecha_dia_fin = fecha_hora_fin  # margen para reservas que empiezan dentro pero terminan después del rango
        cursor.execute('''SELECT nro_reserva, fecha_hora_inicio, horas, nro_cancha, dni_cliente, id_pago, id_estado FROM Reserva WHERE nro_cancha = ? AND fecha_hora_inicio BETWEEN ? AND ?''', (nro_cancha, fecha_dia_inicio, fecha_dia_fin))
        fila = cursor.fetchall()
        cursor.close()
        reservas = []
        for reserva_fila in fila:
            reservas.append(ReservaDAO.obtener_reserva(reserva_fila))
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
    

    @staticmethod
    def obtener_reserva(fila):
        reserva = Reserva(
            nro_reserva=fila[0],
            fecha_hora_inicio=fila[1],
            horas=fila[2],
            cancha=CanchaDAO.obtener_cancha_por_nro(fila[3]),
            cliente=ClienteDAO.obtener_cliente_por_dni(fila[4]),
            pago=PagoDAO.obtener_pago_por_id(fila[5])
        )
        reserva.estado = EstadoReservaDAO.obtener_estado_reserva_por_id(fila[6])
        return reserva  
    