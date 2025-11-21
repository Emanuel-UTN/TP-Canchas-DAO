from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from dao.ReservaDAO.ReservaDAO import ReservaDAO
from models.Reserva.Reserva import Reserva
from models.Cliente.Cliente import Cliente
from models.Cancha.Cancha import Cancha
from models.Cancha.TipoCancha import TipoCancha
from models.Pago.Pago import Pago
from models.Pago.MetodoPago import MetodoPago

from dao.ClienteDAO.ClienteDAO import ClienteDAO
from dao.CanchaDAO.CanchaDAO import CanchaDAO

bp_reservas = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@bp_reservas.route('/', methods=['GET'])
def obtener_reservas():
    try:
        reservas = ReservaDAO.obtener_reservas()
        return jsonify([{
            'nro_reserva': r.nro_reserva,
            'fecha_hora_inicio': r.fecha_hora_inicio,
            'horas': r.horas,
            'cancha':{
                'nro_cancha': r.cancha.nro_cancha,
                'tipo': r.cancha.tipo_cancha.tipo
            },
            'cliente':{
                'dni': r.cliente.dni,
                'nombre': r.cliente.nombre,
                'apellido': r.cliente.apellido
            },
            'estado': r.get_estado()
        } for r in reservas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_reservas.route('/', methods=['POST'])
def agregar_reserva():
    try:
        data = request.json
        
        # Validar que la reserva no sea más de 3 meses en el futuro
        fecha_reserva = datetime.fromisoformat(data['fecha_hora_inicio'].replace('Z', '+00:00'))
        fecha_maxima = datetime.now() + timedelta(days=90)  # 3 meses = 90 días aproximadamente
        
        if fecha_reserva > fecha_maxima:
            return jsonify({'error': 'No se pueden hacer reservas con más de 3 meses de anticipación'}), 400
        
        cliente = ClienteDAO.obtener_cliente_por_dni(data['dni_cliente'])
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
            
        cancha = CanchaDAO.obtener_cancha_por_nro(data['nro_cancha'])
        if not cancha:
            return jsonify({'error': 'Cancha no encontrada'}), 404
        
        reserva = Reserva(
            nro_reserva=None,
            cliente=cliente,
            cancha=cancha,
            fecha_hora_inicio=data['fecha_hora_inicio'],
            horas=data['horas'],
            pago=None
        )
        ReservaDAO.agregar_reserva(reserva)
        
        return jsonify({'mensaje': 'Reserva agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_reservas.route('/<int:nro_reserva>', methods=['PUT'])
def modificar_reserva(nro_reserva):
    try:
        data = request.json
        
        # Validar que la reserva no sea más de 3 meses en el futuro
        fecha_reserva = datetime.fromisoformat(data['fecha_hora_inicio'].replace('Z', '+00:00'))
        fecha_maxima = datetime.now() + timedelta(days=90)  # 3 meses = 90 días aproximadamente
        
        if fecha_reserva > fecha_maxima:
            return jsonify({'error': 'No se pueden hacer reservas con más de 3 meses de anticipación'}), 400
        
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

@bp_reservas.route('/<int:nro_reserva>', methods=['DELETE'])
def eliminar_reserva(nro_reserva):
    try:
        ReservaDAO.eliminar_reserva(nro_reserva)
        return jsonify({'mensaje': 'Reserva eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
