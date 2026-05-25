from flask import Blueprint, jsonify, request
from app.auth import require_auth
from models.log_evento import LogEvento
from models.usuario import Usuario
from datetime import datetime
from functools import wraps

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/api/admin')


def require_admin(f):
    """Verifica si el usuario autenticado tiene rol de administrador."""
    @require_auth
    @wraps(f)
    def wrapper(g=None, *args, **kwargs):
        try:
            from app.auth import _to_dict
            user_dict = _to_dict(g)
            user_id = user_dict.get('id')  or user_dict.get('user_id')
            usuario = Usuario.query.get(user_id)
            if not usuario or usuario.rol not in ('admin', 'administrador'):
                return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
            return f(*args, **kwargs)
        except Exception:
            return jsonify({'error': 'No autorizado.'}), 403
    return wrapper

@auditoria_bp.route('/logs', methods=['GET'])
@require_admin
def get_logs(g=None):
    filtro_usuario = request.args.get('usuario')
    filtro_tipo = request.args.get('tipo')
    filtro_desde = request.args.get('desde')
    filtro_hasta = request.args.get('hasta')

    query = LogEvento.query

    # Filtrar por usuario
    if filtro_usuario:
        query = query.filter(
            LogEvento.nombre_usuario.ilike(f'%{filtro_usuario}%')
        )

    # Filtrar por tipo de evento
    if filtro_tipo:
        query = query.filter_by(tipo_evento=filtro_tipo)

    # Filtrar desde fecha
    if filtro_desde:
        try:
            desde = datetime.strptime(filtro_desde, '%Y-%m-%d')
            query = query.filter(LogEvento.fecha_hora >= desde)
        except ValueError:
            pass

    # Filtrar hasta fecha
    if filtro_hasta:
        try:
            hasta = datetime.strptime(filtro_hasta, '%Y-%m-%d')
            query = query.filter(LogEvento.fecha_hora <= hasta)
        except ValueError:
            pass

    # RF-05.5: orden cronológico descendente (más reciente primero)
    logs = query.order_by(LogEvento.fecha_hora.desc()).limit(500).all()

    return jsonify([log._to_dict() for log in logs]), 200


@auditoria_bp.route('/logs/tipos', methods=['GET'])
@require_admin
def get_tipos_evento(g=None):
    tipos = [
        'inicio_sesion',
        'cierre_sesion',
        'registro',
        'envio_solucion',
        'creacion_problema'
    ]

    return jsonify(tipos), 200