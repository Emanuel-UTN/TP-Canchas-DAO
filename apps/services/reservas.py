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
            'fecha_hora_inicio': r.fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(r.fecha_hora_inicio, datetime) else str(r.fecha_hora_inicio),
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

        # Normalizar y validar tipos
        if 'fecha_hora_inicio' not in data:
            return jsonify({'error': 'Campo fecha_hora_inicio faltante'}), 400
        raw_fecha = data['fecha_hora_inicio']
        # soportar sufijo Z
        if isinstance(raw_fecha, str) and raw_fecha.endswith('Z'):
            raw_fecha = raw_fecha.replace('Z', '+00:00')
        try:
            fecha_reserva = datetime.fromisoformat(raw_fecha)
        except Exception:
            return jsonify({'error': 'Formato de fecha inválido, use YYYY-MM-DDTHH:MM'}), 400

        # horas: forzar entero
        try:
            horas = int(data.get('horas'))
        except Exception:
            return jsonify({'error': 'Cantidad de horas inválida'}), 400

        fecha_maxima = datetime.now() + timedelta(days=90)  # 3 meses = 90 días aproximadamente

        if fecha_reserva > fecha_maxima:
            return jsonify({'error': 'No se pueden hacer reservas con más de 3 meses de anticipación'}), 400
        elif fecha_reserva < datetime.now():
            return jsonify({'error': 'No se pueden hacer reservas en fechas pasadas'}), 400

        cliente = ClienteDAO.obtener_cliente_por_dni(data['dni_cliente'])
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
            
        cancha = CanchaDAO.obtener_cancha_por_nro(data['nro_cancha'])
        if not cancha:
            return jsonify({'error': 'Cancha no encontrada'}), 404
        hora_inicio_nueva = fecha_reserva
        hora_fin_nueva = hora_inicio_nueva + timedelta(hours=horas)
        reservas = ReservaDAO.obtener_reserva_por_cancha_y_fecha(data['nro_cancha'], hora_inicio_nueva, hora_fin_nueva)
        for r in reservas:
            # r.fecha_hora_inicio puede ser string o datetime; normalizar
            if isinstance(r.fecha_hora_inicio, str):
                fr = r.fecha_hora_inicio
                if fr.endswith('Z'):
                    fr = fr.replace('Z', '+00:00')
                hora_inicio_existente = datetime.fromisoformat(fr)
            else:
                hora_inicio_existente = r.fecha_hora_inicio
            hora_fin_existente = hora_inicio_existente + timedelta(hours=int(r.horas))
            hora_inicio_nueva = fecha_reserva
            hora_fin_nueva = hora_inicio_nueva + timedelta(hours=horas)
            
            # Verificar si hay solapamiento de horarios
            if (hora_inicio_nueva == hora_inicio_existente or hora_fin_nueva == hora_fin_existente or # Que alguna de las dos horas coincida
                (hora_inicio_existente < hora_inicio_nueva < hora_fin_existente) or # La nueva empieza dentro de una existente
                (hora_inicio_existente < hora_fin_nueva < hora_fin_existente) or # La nueva termina dentro de una existente
                (hora_inicio_nueva < hora_inicio_existente and hora_fin_nueva > hora_fin_existente)): # La nueva engloba a una existente
                return jsonify({'error': 'La cancha ya está reservada en el horario solicitado'}), 409
            
        
        reserva = Reserva(
            nro_reserva=None,
            cliente=cliente,
            cancha=cancha,
            fecha_hora_inicio=fecha_reserva,
            horas=horas,
            pago=None
        )
        ReservaDAO.agregar_reserva(reserva)
        
        return jsonify({'mensaje': 'Reserva agregada exitosamente'}), 201
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_reservas.route('/<int:nro_reserva>', methods=['PUT'])
def modificar_reserva(nro_reserva):
    try:
        data = request.json
        
        cliente_placeholder = Cliente(0, "", "", "")
        cancha_placeholder = Cancha(0, TipoCancha(""), 0)
        pago_placeholder = Pago(MetodoPago(""), "", 0)
        
        # La validación de fecha y horas se hace en el constructor de Reserva
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
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_reservas.route('/<int:nro_reserva>', methods=['DELETE'])
def eliminar_reserva(nro_reserva):
    try:
        ReservaDAO.eliminar_reserva(nro_reserva)
        return jsonify({'mensaje': 'Reserva eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@bp_reservas.route('/cancelar/<int:nro_reserva>', methods=['PUT'])
def cancelar_reserva(nro_reserva):
    try:
        ReservaDAO.cancelar_reserva(nro_reserva)
        return jsonify({'mensaje': 'Reserva cancelada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
