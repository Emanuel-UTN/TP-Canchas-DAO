from flask import Blueprint, jsonify, request
import sqlite3
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from models.Cancha.TipoCancha import TipoCancha

bp_tipos = Blueprint('tipos_cancha', __name__, url_prefix='/api/tipos-cancha')

@bp_tipos.route('/', methods=['GET'])
def obtener_tipos_cancha():
    try:
        tipos = TipoCanchaDAO.obtener_tipos_cancha()
        return jsonify([{'tipo': t.tipo} for t in tipos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_tipos.route('/', methods=['POST'])
def agregar_tipo_cancha():
    try:
        data = request.json
        tipo_cancha = TipoCancha(tipo=data['tipo'])
        TipoCanchaDAO.agregar_tipo_cancha(tipo_cancha)
        return jsonify({'mensaje': 'Tipo de cancha agregado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El tipo de cancha ya existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_tipos.route('/<string:nombre_tipo>', methods=['GET'])
def obtener_tipo_cancha(nombre_tipo):
    try:
        tipo = TipoCanchaDAO.obtener_tipo_cancha_por_nombre(nombre_tipo)
        if not tipo:
            return jsonify({'error': 'Tipo de cancha no encontrado'}), 404
        return jsonify({'tipo': tipo.tipo})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_tipos.route('/<string:nombre_tipo>', methods=['PUT'])
def modificar_tipo_cancha(nombre_tipo):
    try:
        data = request.json
        TipoCanchaDAO.modificar_tipo_cancha_por_nombre(nombre_tipo, data['tipo'])
        return jsonify({'mensaje': 'Tipo de cancha modificado exitosamente'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El nuevo nombre de tipo ya existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_tipos.route('/<string:nombre_tipo>', methods=['DELETE'])
def eliminar_tipo_cancha(nombre_tipo):
    try:
        TipoCanchaDAO.eliminar_tipo_cancha_por_nombre(nombre_tipo)
        return jsonify({'mensaje': 'Tipo de cancha eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400