from dao.conexion import ConexionDB
from models.Cancha.Cancha import Cancha
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from dao.CanchaDAO.ServicioCanchaDAO import ServicioCanchaDAO
from dao.CanchaDAO.ServicioDAO import ServicioDAO

class CanchaDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cancha (
                nro_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tipo INTEGER NOT NULL,
                costo_por_hora REAL NOT NULL CHECK(costo_por_hora > 0),
                FOREIGN KEY (id_tipo) REFERENCES TipoCancha(id_tipo)
                )
            ''')
        conexion.commit()
        cursor.close()
        
    @staticmethod
    def agregar_cancha(cancha: Cancha):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        # Insertar cancha
        cursor.execute('''
            INSERT INTO Cancha (id_tipo, costo_por_hora)
            VALUES (?, ?)
        ''', (TipoCanchaDAO.obtener_id_tipo_cancha_por_tipo(cancha.tipo_cancha.tipo), cancha.costo_hora))

        # obtener id generado y commitear para que otras conexiones lo vean
        nro_generado = cursor.lastrowid
        conexion.commit()
        cursor.close()
        
        # vincular servicios seleccionados (si vienen)
        for s in cancha.servicios:
            id_serv = ServicioDAO.obtener_id_servicio_por_nombre(s.servicio)
            if id_serv is not None:
                try:
                    ServicioCanchaDAO.agregar_servicio_cancha(id_serv, nro_generado)
                except Exception:
                    # ignorar errores individuales de vinculación
                    pass

        return nro_generado
    
    @staticmethod
    def eliminar_cancha(nro_cancha: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Cancha WHERE nro_cancha = ?''', (nro_cancha,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_canchas():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        canchas = []
        cursor.execute('''SELECT nro_cancha, id_tipo, costo_por_hora FROM Cancha''')
        filas = cursor.fetchall()
        for fila in filas:
            cancha = Cancha(
                nro_cancha=fila[0],
                tipo_cancha=TipoCanchaDAO.obtener_tipo_cancha_por_id(fila[1]),
                costo_hora=fila[2]
            )
            cancha.servicios = ServicioCanchaDAO.obtener_servicios_por_cancha(cancha.nro_cancha)
            canchas.append(cancha)
        cursor.close()
        return canchas
    
    @staticmethod
    def obtener_cancha_por_nro(nro_cancha: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT nro_cancha, id_tipo, costo_por_hora FROM Cancha WHERE nro_cancha = ?''', (nro_cancha,))
        fila = cursor.fetchone()
        cancha = None
        if fila:
            cancha = Cancha(
                nro_cancha=fila[0],
                tipo_cancha=TipoCanchaDAO.obtener_tipo_cancha_por_id(fila[1]),
                costo_hora=fila[2]
            )
            cancha.servicios = ServicioCanchaDAO.obtener_servicios_por_cancha(cancha.nro_cancha)
        cursor.close()
        return cancha

    @staticmethod
    def modificar_cancha(cancha: Cancha):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Cancha
            SET id_tipo = ?, costo_por_hora = ?
            WHERE nro_cancha = ?
        ''', (TipoCanchaDAO.obtener_id_tipo_cancha_por_tipo(cancha.tipo_cancha.tipo), cancha.costo_hora, cancha.nro_cancha))
        conexion.commit()
        cursor.close()

