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
                fecha_hora_inicio DATETIME NOT NULL,
                horas INTEGER NOT NULL CHECK(horas > 0 AND horas <= 6),
                nro_cancha INTEGER NOT NULL,
                dni_cliente INTEGER NOT NULL,
                id_pago INTEGER,
                id_estado INTEGER NOT NULL,
                
                FOREIGN KEY (nro_cancha) REFERENCES Cancha(nro_cancha),
                FOREIGN KEY (dni_cliente) REFERENCES Cliente(dni_cliente),
                FOREIGN KEY (id_pago) REFERENCES Pago(id_pago),
                FOREIGN KEY (id_estado) REFERENCES EstadoReserva(id_estado)
                )
        ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_reserva(reserva: Reserva):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        fecha_val = reserva.fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(reserva.fecha_hora_inicio, datetime) else str(reserva.fecha_hora_inicio)
        horas_val = int(reserva.horas)
        cursor.execute('''
            INSERT INTO Reserva (fecha_hora_inicio, horas, nro_cancha, dni_cliente, id_pago, id_estado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fecha_val, horas_val, reserva.cancha.nro_cancha, reserva.cliente.dni, None, EstadoReservaDAO.obtener_id_estado_reserva_por_nombre("Pendiente")))
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
        # Incluir margen: buscar reservas que empiecen hasta 5 horas antes
        fecha_dia_inicio = fecha_hora_inicio - timedelta(hours=5)
        # Convertir las fechas al mismo formato ISO usado al guardar en la BD
        # (guardamos como 'YYYY-MM-DDTHH:MM:SS'), así la comparación BETWEEN funciona correctamente.
        fecha_dia_inicio_str = fecha_dia_inicio.strftime('%Y-%m-%dT%H:%M:%S')
        fecha_dia_fin_str = fecha_hora_fin.strftime('%Y-%m-%dT%H:%M:%S')
        cursor.execute('''
                       SELECT nro_reserva, fecha_hora_inicio, horas, nro_cancha, dni_cliente, id_pago, id_estado 
                       FROM Reserva 
                       WHERE 
                            nro_cancha = ? 
                            AND fecha_hora_inicio BETWEEN ? AND ?''', 
                        (nro_cancha, fecha_dia_inicio_str, fecha_dia_fin_str))
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
        fecha_val = reserva.fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(reserva.fecha_hora_inicio, datetime) else str(reserva.fecha_hora_inicio)
        horas_val = int(reserva.horas)
        cursor.execute('''
            UPDATE Reserva
            SET fecha_hora_inicio = ?, horas = ?, nro_cancha = ?, dni_cliente = ?, id_pago = ?, id_estado = ?
            WHERE nro_reserva = ?
        ''', (fecha_val, horas_val, reserva.nro_cancha, reserva.dni_cliente, reserva.id_pago, reserva.id_estado, reserva.nro_reserva))
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
    