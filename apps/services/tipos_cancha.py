from flask import Blueprint, jsonify, request
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from models.Cancha.TipoCancha import TipoCancha

bp_tipos = Blueprint('tipos_cancha', __name__, url_prefix='/api/tipos-cancha')

@bp_tipos.route('/', methods=['GET'])
def obtener_tipos_cancha():
    try:
        tipos = TipoCanchaDAO.obtener_tipos_cancha()
        return jsonify([{
            'tipo': t.tipo
        } for t in tipos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_tipos.route('/', methods=['POST'])
def agregar_tipo_cancha():
    try:
        data = request.json
        tipo_cancha = TipoCancha(tipo=data['tipo'])
        TipoCanchaDAO.agregar_tipo_cancha(tipo_cancha)
        return jsonify({'mensaje': 'Tipo de cancha agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
