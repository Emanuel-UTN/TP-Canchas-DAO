from flask import Blueprint, jsonify, request
import sqlite3
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from models.Cancha.Servicio import Servicio

bp_servicios = Blueprint('servicios', __name__, url_prefix='/api/servicios')

@bp_servicios.route('/', methods=['GET'])
def obtener_servicios():
    try:
        servicios = ServicioDAO.obtener_servicios()
        return jsonify([
            {
                'servicio': s.servicio,
                'costo': s.costo
            } for s in servicios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_servicios.route('/', methods=['POST'])
def agregar_servicio():
    try:
        data = request.json
        servicio = Servicio(
            servicio=data['servicio'],
            costo=data['costo']
        )
        ServicioDAO.agregar_servicio(servicio)
        return jsonify({'mensaje': 'Servicio agregado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El servicio ya existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_servicios.route('/<string:nombre_servicio>', methods=['GET'])
def obtener_servicio(nombre_servicio):
    try:
        servicio = ServicioDAO.obtener_servicio_por_nombre(nombre_servicio)
        if not servicio:
            return jsonify({'error': 'Servicio no encontrado'}), 404
        return jsonify({'servicio': servicio.servicio, 'costo': servicio.costo})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_servicios.route('/<string:nombre_servicio>', methods=['PUT'])
def modificar_servicio(nombre_servicio):
    try:
        data = request.json
        ServicioDAO.modificar_servicio_por_nombre(nombre_servicio, data['servicio'], data['costo'])
        return jsonify({'mensaje': 'Servicio modificado exitosamente'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El nuevo nombre de servicio ya existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_servicios.route('/<string:nombre_servicio>', methods=['DELETE'])
def eliminar_servicio(nombre_servicio):
    try:
        ServicioDAO.eliminar_servicio_por_nombre(nombre_servicio)
        return jsonify({'mensaje': 'Servicio eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
