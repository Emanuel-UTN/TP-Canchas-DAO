from flask import Blueprint, jsonify, request
from dao.TorneoDAO.TorneoDAO import TorneoDAO
from models.Torneo.Torneo import Torneo
from models.Torneo.Equipo import Equipo
from dao.TorneoDAO.EquipoDAO import EquipoDAO
from dao.TorneoDAO.TorneoEquipoDAO import TorneoEquipoDAO
from dao.ClienteDAO.ClienteDAO import ClienteDAO


bp_torneos = Blueprint('torneos', __name__, url_prefix='/api/torneos')

@bp_torneos.route('/', methods=['GET'])
def obtener_torneos():
    try:
        torneos = TorneoDAO.listar_torneos_con_cantidad_equipos()
        return jsonify(torneos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_torneos.route('/', methods=['POST'])
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
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_torneos.route('/<int:id>', methods=['PUT'])
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
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_torneos.route('/<int:id>', methods=['DELETE'])
def eliminar_torneo(id):
    try:
        TorneoDAO.eliminar_torneo(id)
        return jsonify({'mensaje': 'Torneo eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp_torneos.route('/detalle/<int:id>', methods=['GET'])
def obtener_detalle_torneo(id):
    try:
        torneo = TorneoDAO.obtener_detalle_torneo(id)
        if torneo is None:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        # Torneo es una instancia de modelo; serializar a dict antes de jsonify
        if hasattr(torneo, 'to_dict'):
            return jsonify(torneo.to_dict())
        # fallback: intentar convertir atributos manualmente
        return jsonify({
            'id': getattr(torneo, 'id', None),
            'fecha_inicio': getattr(torneo, 'fecha_inicio', None),
            'fecha_fin': getattr(torneo, 'fecha_fin', None),
            'costo_inscripcion': getattr(torneo, 'costo_inscripcion', None),
            'premio': getattr(torneo, 'premio', None),
            'tabla': getattr(torneo, 'tabla', []),
            'partidos': getattr(torneo, 'partidos', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_torneos.route('/<int:id>/equipos', methods=['GET'])
def listar_equipos_torneo(id):
    try:
        torneo = TorneoDAO.obtener_torneo_por_id(id)
        if torneo is None:
            return jsonify({'error': 'Torneo no encontrado'}), 404

        # obtener tabla con id_equipo y puntos
        tabla = TorneoEquipoDAO.obtener_tabla_por_torneo(id)
        equipos = []
        for row in tabla:
            equipo = EquipoDAO.obtener_equipo_por_id(row['id_equipo'])
            if equipo:
                equipos.append({
                    'id_equipo': row['id_equipo'],
                    'nombre': equipo.nombre,
                    'delegado': equipo.delegado.dni if equipo.delegado else None,
                    'puntos': row['puntos']
                })
        return jsonify(equipos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_torneos.route('/<int:id>/equipos', methods=['POST'])
def agregar_equipo_a_torneo(id):
    try:
        data = request.json
        nombre = data.get('nombre')
        dni_delegado = data.get('dni_delegado')
        if not nombre or not dni_delegado:
            return jsonify({'error': 'Faltan campos requeridos (nombre, dni_delegado)'}), 400

        # validar torneo
        torneo = TorneoDAO.obtener_torneo_por_id(id)
        if torneo is None:
            return jsonify({'error': 'Torneo no encontrado'}), 404

        # validar delegado existente
        delegado = ClienteDAO.obtener_cliente_por_dni(int(dni_delegado))
        if delegado is None:
            return jsonify({'error': 'Delegado (cliente) no encontrado'}), 400

        # crear equipo
        equipo = Equipo(nombre=nombre, delegado=delegado)
        nuevo_id = EquipoDAO.agregar_equipo(equipo)

        # vincular al torneo con 0 puntos iniciales
        TorneoEquipoDAO.agregar_torneo_equipo(id, nuevo_id, 0)

        return jsonify({'mensaje': 'Equipo agregado al torneo', 'id_equipo': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
