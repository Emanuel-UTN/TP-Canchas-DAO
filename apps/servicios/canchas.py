from flask import Blueprint, jsonify, request
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from models.Cancha.Cancha import Cancha
from models.Cancha.TipoCancha import TipoCancha

bp_canchas = Blueprint('canchas', __name__, url_prefix='/api/canchas')

@bp_canchas.route('/', methods=['GET'])
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

@bp_canchas.route('/', methods=['POST'])
def agregar_cancha():
    try:
        data = request.json
        cancha = Cancha(
            nro_cancha=None,
            tipo_cancha=TipoCancha(""),
            costo_hora=data.get('costo_por_hora', 0)
        )
        cancha.id_tipo = data.get('id_tipo')
        cancha.costo_por_hora = data.get('costo_por_hora')
        CanchaDAO.agregar_cancha(cancha)
        return jsonify({'mensaje': 'Cancha agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_canchas.route('/<int:nro_cancha>', methods=['PUT'])
def modificar_cancha(nro_cancha):
    try:
        data = request.json
        cancha = Cancha(
            nro_cancha=nro_cancha,
            tipo_cancha=TipoCancha(""),
            costo_hora=data.get('costo_por_hora', 0)
        )
        cancha.id_tipo = data.get('id_tipo')
        cancha.costo_por_hora = data.get('costo_por_hora')
        CanchaDAO.modificar_cancha(cancha)
        return jsonify({'mensaje': 'Cancha modificada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_canchas.route('/<int:nro_cancha>', methods=['DELETE'])
def eliminar_cancha(nro_cancha):
    try:
        CanchaDAO.eliminar_cancha(nro_cancha)
        return jsonify({'mensaje': 'Cancha eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
