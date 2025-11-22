from flask import Blueprint, jsonify, request
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from models.Cancha.Cancha import Cancha
from models.Cancha.TipoCancha import TipoCancha

bp_canchas = Blueprint('canchas', __name__, url_prefix='/api/canchas')

@bp_canchas.route('/', methods=['GET'])
def obtener_canchas():
    try:
        canchas = CanchaDAO.obtener_canchas()
        return jsonify([{
            'nro_cancha': c.nro_cancha,
            'tipo': c.tipo_cancha.tipo,
            'costo_por_hora': c.costo_hora,
            'servicios': [s.servicio for s in c.servicios]
        } for c in canchas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_canchas.route('/', methods=['POST'])
def agregar_cancha():
    try:
        data = request.json
        cancha = Cancha(
            nro_cancha=None,
            tipo_cancha=TipoCancha(data.get('tipo', 'cancha')),
            costo_hora=data.get('costo_por_hora', 0)
        )
        cancha.servicios.extend(ServicioDAO.obtener_servicios_por_nombres(data.get('servicios', [])))
    
        # insertar cancha y obtener id generado
        nro_cancha = CanchaDAO.agregar_cancha(cancha)

        return jsonify({'mensaje': 'Cancha agregada exitosamente', 'nro_cancha': nro_cancha}), 201
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_canchas.route('/<int:nro_cancha>', methods=['PUT'])
def modificar_cancha(nro_cancha):
    try:
        data = request.json
        cancha = Cancha(
            nro_cancha=nro_cancha,
            tipo_cancha=TipoCancha(data.get('tipo_cancha', '')),
            costo_hora=data.get('costo_por_hora', 0),
        )
        cancha.servicios.extend(ServicioDAO.obtener_servicios_por_nombres(data.get('servicios', [])))
        CanchaDAO.modificar_cancha(cancha)
        return jsonify({'mensaje': 'Cancha modificada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp_canchas.route('/<int:nro_cancha>', methods=['GET'])
def obtener_cancha(nro_cancha):
    try:
        cancha = CanchaDAO.obtener_cancha_por_nro(nro_cancha)
        if not cancha:
            return jsonify({'error': 'Cancha no encontrada'}), 404
        return jsonify({
            'nro_cancha': cancha.nro_cancha,
            'tipo': cancha.tipo_cancha.tipo if cancha.tipo_cancha else None,
            'costo_por_hora': cancha.costo_hora,
            'servicios': [s.servicio if hasattr(s, 'servicio') else (s.nombre if hasattr(s, 'nombre') else str(s)) for s in cancha.servicios]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_canchas.route('/<int:nro_cancha>', methods=['DELETE'])
def eliminar_cancha(nro_cancha):
    try:
        CanchaDAO.eliminar_cancha(nro_cancha)
        return jsonify({'mensaje': 'Cancha eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
