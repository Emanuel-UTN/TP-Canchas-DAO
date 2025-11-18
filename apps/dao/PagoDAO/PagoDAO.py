from dao.conexion import ConexionDB
from models.Pago.Pago import Pago
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO

class PagoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pago (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_metodo_pago INTEGER,
                fecha_hora DATETIME,
                monto REAL,
                FOREIGN KEY (id_metodo_pago) REFERENCES MetodoPago(id_metodo_pago)
                )
            ''')

        conexion.commit()
        cursor.close()
    
    @staticmethod
    def agregar_pago(pago: Pago):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Pago (id_metodo_pago, fecha_hora, monto)
            VALUES (?, ?, ?)
        ''', (pago.id_metodo_pago, pago.fecha_hora, pago.monto))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_pago(id_metodo_pago: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Pago WHERE id_pago = ?''', (id_metodo_pago,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_pagos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        pagos = []
        cursor.execute('''SELECT id_pago, id_metodo_pago, fecha_hora, monto FROM Pago''')
        filas = cursor.fetchall()
        for fila in filas:
            pago = Pago(
                metodo_pago=MetodoPagoDAO.obtener_metodo_pago_por_id(fila[1]),
                fecha_hora=fila[2],
                monto=fila[3]
            )
            pagos.append(pago)
        cursor.close()
        return pagos
    
    @staticmethod
    def obtener_pago_por_id(id_pago: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_pago, id_metodo_pago, fecha_hora, monto FROM Pago WHERE id_pago = ?''', (id_pago,))
        fila = cursor.fetchone()
        pago = None
        if fila:
            pago = Pago(
                metodo_pago=MetodoPagoDAO.obtener_metodo_pago_por_id(fila[1]),
                fecha_hora=fila[2],
                monto=fila[3]
            )
        cursor.close()
        return pago
    
    @staticmethod
    def modificar_pago(pago: Pago):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Pago
            SET id_metodo_pago = ?, fecha_hora = ?, monto = ?
            WHERE id_pago = ?
        ''', (pago.id_metodo_pago, pago.fecha_hora, pago.monto, pago.id_pago))
        conexion.commit()
        cursor.close()
