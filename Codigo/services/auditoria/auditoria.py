from flask import Blueprint, jsonify, request
from models.log_evento import LogEvento
from models.usuario import Usuario
from datetime import datetime
from functools import wraps
from app.extensions import db


def registrar_evento(tipo_evento, usuario_id=None, nombre_usuario=None, detalle=None):
    try:
        log = LogEvento(
            usuario_id=usuario_id,
            nombre_usuario=nombre_usuario,
            tipo_evento=tipo_evento,
            fecha_hora=datetime.utcnow(),
            detalle=detalle,
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[auditoria] Error registrando evento '{tipo_evento}': {e}")


auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/api/admin')


def require_admin(f):
    """RF-05.4: Solo administradores pueden acceder."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            from app.auth import _to_dict, admin_client
            token = request.cookies.get('access_token')
            if not token:
                return jsonify({'error': 'Sin autenticación.'}), 401

            user_response = admin_client.auth.get_user(token)
            user_dict = _to_dict(getattr(user_response, 'user', user_response))
            user_id = user_dict.get('id') if isinstance(user_dict, dict) else None

            if not user_id:
                return jsonify({'error': 'Token inválido.'}), 401

            usuario = Usuario.query.get(user_id)
            if not usuario or usuario.rol != 'admin':
                return jsonify({'error': 'Acceso denegado.'}), 403

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'No autorizado.', 'detalle': str(e)}), 403
    return wrapper


@auditoria_bp.route('/logs', methods=['GET'])
@require_admin
def get_logs():
    filtro_usuario = request.args.get('usuario')
    filtro_tipo    = request.args.get('tipo')
    filtro_desde   = request.args.get('desde')
    filtro_hasta   = request.args.get('hasta')

    query = LogEvento.query

    if filtro_usuario:
        query = query.filter(LogEvento.nombre_usuario.ilike(f'%{filtro_usuario}%'))
    if filtro_tipo:
        query = query.filter_by(tipo_evento=filtro_tipo)
    if filtro_desde:
        try:
            query = query.filter(LogEvento.fecha_hora >= datetime.strptime(filtro_desde, '%Y-%m-%d'))
        except ValueError:
            pass
    if filtro_hasta:
        try:
            query = query.filter(LogEvento.fecha_hora <= datetime.strptime(filtro_hasta, '%Y-%m-%d'))
        except ValueError:
            pass

    logs = query.order_by(LogEvento.fecha_hora.desc()).limit(500).all()
    return jsonify([log.to_dict() for log in logs]), 200


@auditoria_bp.route('/logs/tipos', methods=['GET'])
@require_admin
def get_tipos_evento():
    tipos = ['inicio_sesion', 'cierre_sesion', 'registro',
             'envio_solucion', 'creacion_problema']
    return jsonify(tipos), 200