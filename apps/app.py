from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

# Agregar el directorio apps al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bd_canchas import crear_tablas
from dao.ClienteDAO.ClienteDAO import ClienteDAO
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from dao.ReservaDAO.ReservaDAO import ReservaDAO
from dao.ReservaDAO.EstadoReservaDAO import EstadoReservaDAO
from dao.PagoDAO.PagoDAO import PagoDAO
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO
from dao.TorneoDAO.TorneoDAO import TorneoDAO

from models.Cliente.Cliente import Cliente
from models.Cancha.Cancha import Cancha
from models.Cancha.TipoCancha import TipoCancha
from models.Cancha.Servicio import Servicio
from models.Reserva.Reserva import Reserva
from models.Reserva.EstadoReserva import EstadoReserva
from models.Pago.Pago import Pago
from models.Pago.MetodoPago import MetodoPago
from models.Torneo.Torneo import Torneo

app = Flask(__name__)
CORS(app)

# Inicializar tablas al iniciar
crear_tablas()

# ========== CLIENTES ==========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = ClienteDAO.obtener_clientes()
        return jsonify([{
            'dni': c.dni,
            'nombre': c.nombre,
            'apellido': c.apellido,
            'telefono': c.telefono
        } for c in clientes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def agregar_cliente():
    try:
        data = request.json
        cliente = Cliente(
            dni=data['dni'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono']
        )
        ClienteDAO.agregar_cliente(cliente)
        return jsonify({'mensaje': 'Cliente agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/clientes/<int:dni>', methods=['PUT'])
def modificar_cliente(dni):
    try:
        data = request.json
        cliente = Cliente(
            dni=dni,
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono']
        )
        ClienteDAO.modificar_cliente(cliente)
        return jsonify({'mensaje': 'Cliente modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/clientes/<int:dni>', methods=['DELETE'])
def eliminar_cliente(dni):
    try:
        ClienteDAO.eliminar_cliente(dni)
        return jsonify({'mensaje': 'Cliente eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== CANCHAS ==========
@app.route('/api/canchas', methods=['GET'])
def obtener_canchas():
    try:
        canchas = CanchaDAO.obtener_canchas()
        return jsonify([{
            'nro_cancha': c.nro_cancha,
            'id_tipo': c.id_tipo,
            'costo_por_hora': c.costo_por_hora
        } for c in canchas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/canchas', methods=['POST'])
def agregar_cancha():
    try:
        data = request.json
        # Crear objeto cancha con valores mínimos y luego asignar atributos
        cancha = Cancha(
            nro_cancha=None,
            tipo_cancha=TipoCancha(""),  # Placeholder
            costo_hora=data['costo_por_hora']
        )
        cancha.id_tipo = data['id_tipo']
        cancha.costo_por_hora = data['costo_por_hora']
        CanchaDAO.agregar_cancha(cancha)
        return jsonify({'mensaje': 'Cancha agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/canchas/<int:nro_cancha>', methods=['PUT'])
def modificar_cancha(nro_cancha):
    try:
        data = request.json
        cancha = Cancha(
            nro_cancha=nro_cancha,
            tipo_cancha=TipoCancha(""),  # Placeholder
            costo_hora=data['costo_por_hora']
        )
        cancha.id_tipo = data['id_tipo']
        cancha.costo_por_hora = data['costo_por_hora']
        CanchaDAO.modificar_cancha(cancha)
        return jsonify({'mensaje': 'Cancha modificada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/canchas/<int:nro_cancha>', methods=['DELETE'])
def eliminar_cancha(nro_cancha):
    try:
        CanchaDAO.eliminar_cancha(nro_cancha)
        return jsonify({'mensaje': 'Cancha eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== TIPOS DE CANCHA ==========
@app.route('/api/tipos-cancha', methods=['GET'])
def obtener_tipos_cancha():
    try:
        tipos = TipoCanchaDAO.obtener_tipos_cancha()
        return jsonify([{
            'id_tipo': t.id_tipo,
            'tipo': t.tipo
        } for t in tipos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tipos-cancha', methods=['POST'])
def agregar_tipo_cancha():
    try:
        data = request.json
        # El DAO espera un objeto con atributo 'tipo'
        tipo_cancha = TipoCancha(tipo=data['tipo'])
        TipoCanchaDAO.agregar_tipo_cancha(tipo_cancha)
        return jsonify({'mensaje': 'Tipo de cancha agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== SERVICIOS ==========
@app.route('/api/servicios', methods=['GET'])
def obtener_servicios():
    try:
        servicios = ServicioDAO.obtener_servicios()
        return jsonify([{
            'id_servicio': s.id_servicio,
            'servicio': s.servicio,
            'costo': s.costo
        } for s in servicios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servicios', methods=['POST'])
def agregar_servicio():
    try:
        data = request.json
        servicio = Servicio(
            servicio=data['servicio'],
            costo=data['costo']
        )
        ServicioDAO.agregar_servicio(servicio)
        return jsonify({'mensaje': 'Servicio agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== RESERVAS ==========
@app.route('/api/reservas', methods=['GET'])
def obtener_reservas():
    try:
        reservas = ReservaDAO.obtener_reservas()
        return jsonify([{
            'nro_reserva': r.nro_reserva,
            'fecha_hora_inicio': r.fecha_hora_inicio,
            'horas': r.horas,
            'nro_cancha': r.nro_cancha,
            'dni_cliente': r.dni_cliente,
            'id_pago': r.id_pago,
            'id_estado': r.id_estado
        } for r in reservas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservas', methods=['POST'])
def agregar_reserva():
    try:
        data = request.json
        # Crear objetos placeholder para el constructor
        cliente_placeholder = Cliente(0, "", "", "")
        cancha_placeholder = Cancha(0, TipoCancha(""), 0)
        pago_placeholder = Pago(MetodoPago(""), "", 0)
        
        reserva = Reserva(
            nro_reserva=None,
            cliente=cliente_placeholder,
            cancha=cancha_placeholder,
            fecha_hora_inicio=data['fecha_hora_inicio'],
            horas=data['horas'],
            pago=pago_placeholder
        )
        reserva.nro_cancha = data['nro_cancha']
        reserva.dni_cliente = data['dni_cliente']
        reserva.id_pago = data.get('id_pago')
        reserva.id_estado = data.get('id_estado', 1)  # Por defecto pendiente
        ReservaDAO.agregar_reserva(reserva)
        return jsonify({'mensaje': 'Reserva agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/reservas/<int:nro_reserva>', methods=['PUT'])
def modificar_reserva(nro_reserva):
    try:
        data = request.json
        cliente_placeholder = Cliente(0, "", "", "")
        cancha_placeholder = Cancha(0, TipoCancha(""), 0)
        pago_placeholder = Pago(MetodoPago(""), "", 0)
        
        reserva = Reserva(
            nro_reserva=nro_reserva,
            cliente=cliente_placeholder,
            cancha=cancha_placeholder,
            fecha_hora_inicio=data['fecha_hora_inicio'],
            horas=data['horas'],
            pago=pago_placeholder
        )
        reserva.nro_cancha = data['nro_cancha']
        reserva.dni_cliente = data['dni_cliente']
        reserva.id_pago = data.get('id_pago')
        reserva.id_estado = data.get('id_estado')
        ReservaDAO.modificar_reserva(reserva)
        return jsonify({'mensaje': 'Reserva modificada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/reservas/<int:nro_reserva>', methods=['DELETE'])
def eliminar_reserva(nro_reserva):
    try:
        ReservaDAO.eliminar_reserva(nro_reserva)
        return jsonify({'mensaje': 'Reserva eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== ESTADOS DE RESERVA ==========
@app.route('/api/estados-reserva', methods=['GET'])
def obtener_estados_reserva():
    try:
        estados = EstadoReservaDAO.obtener_estados_reserva()
        return jsonify([{
            'id_estado': e.id_estado,
            'estado': e.estado
        } for e in estados])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== PAGOS ==========
@app.route('/api/pagos', methods=['GET'])
def obtener_pagos():
    try:
        pagos = PagoDAO.obtener_pagos()
        return jsonify([{
            'id_pago': p.id_pago,
            'id_metodo_pago': p.id_metodo_pago,
            'fecha_hora': p.fecha_hora,
            'monto': p.monto
        } for p in pagos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pagos', methods=['POST'])
def agregar_pago():
    try:
        data = request.json
        metodo_placeholder = MetodoPago("")
        pago = Pago(
            metodo_pago=metodo_placeholder,
            fecha_hora=data['fecha_hora'],
            monto=data['monto']
        )
        pago.id_metodo_pago = data['id_metodo_pago']
        pago.id_pago = None
        PagoDAO.agregar_pago(pago)
        return jsonify({'mensaje': 'Pago agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== MÉTODOS DE PAGO ==========
@app.route('/api/metodos-pago', methods=['GET'])
def obtener_metodos_pago():
    try:
        metodos = MetodoPagoDAO.obtener_metodos_pago()
        return jsonify([{
            'id_metodo_pago': m.id_metodo_pago,
            'metodo': m.metodo
        } for m in metodos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metodos-pago', methods=['POST'])
def agregar_metodo_pago():
    try:
        data = request.json
        metodo_pago = MetodoPago(metodo=data['metodo'])
        MetodoPagoDAO.agregar_metodo_pago(metodo_pago)
        return jsonify({'mensaje': 'Método de pago agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== TORNEOS ==========
@app.route('/api/torneos', methods=['GET'])
def obtener_torneos():
    try:
        torneos = TorneoDAO.obtener_torneos()
        return jsonify([{
            'id': t.id,
            'fecha_inicio': t.fecha_inicio,
            'fecha_fin': t.fecha_fin,
            'costo_inscripcion': t.costo_inscripcion,
            'premio': t.premio
        } for t in torneos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/torneos', methods=['POST'])
def agregar_torneo():
    try:
        data = request.json
        torneo = Torneo(
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            costo_inscripcion=data['costo_inscripcion'],
            premio=data['premio']
        )
        TorneoDAO.agregar_torneo(torneo)
        return jsonify({'mensaje': 'Torneo agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/torneos/<int:id>', methods=['PUT'])
def modificar_torneo(id):
    try:
        data = request.json
        torneo = Torneo(
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            costo_inscripcion=data['costo_inscripcion'],
            premio=data['premio']
        )
        torneo.id = id
        TorneoDAO.modificar_torneo(torneo)
        return jsonify({'mensaje': 'Torneo modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/torneos/<int:id>', methods=['DELETE'])
def eliminar_torneo(id):
    try:
        TorneoDAO.eliminar_torneo(id)
        return jsonify({'mensaje': 'Torneo eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

