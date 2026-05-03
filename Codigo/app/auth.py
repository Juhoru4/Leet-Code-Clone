from flask import Blueprint, request, jsonify, g, make_response, render_template
from Codigo.services.supabase_client import get_client, get_admin_client, SUPABASE_URL, SUPABASE_ANON_KEY
import httpx
import os
from flask import current_app
import traceback
from app.extensions import db
from models import Usuario
from datetime import datetime
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

client = get_client()
admin_client = get_admin_client()


def _to_dict(obj):
    """Normalize various Supabase/pydantic responses to a plain dict."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    # pydantic v2
    if hasattr(obj, 'model_dump'):
        try:
            return obj.model_dump()
        except Exception:
            pass
    # pydantic v1 or other objects
    if hasattr(obj, 'dict'):
        try:
            return obj.dict()
        except Exception:
            pass
    # some supabase responses have a `user` attribute
    if hasattr(obj, 'user'):
        try:
            return _to_dict(getattr(obj, 'user'))
        except Exception:
            pass
    # fallback to vars()
    try:
        return vars(obj)
    except Exception:
        return {'value': str(obj)}


def build_unique_username(base_username):
    candidate = (base_username or '').strip()
    if not candidate:
        return candidate

    if Usuario.query.filter_by(nombre_usuario=candidate).first() is None:
        return candidate

    suffix = 1
    while True:
        next_candidate = f'{candidate}_{suffix}'
        if Usuario.query.filter_by(nombre_usuario=next_candidate).first() is None:
            return next_candidate
        suffix += 1


def normalize_role(raw_role):
    role = (raw_role or '').strip().lower()
    if role in {'admin', 'administrador', 'profesor'}:
        return 'administrador'
    if role == 'estudiante':
        return 'estudiante'
    return 'estudiante'


def extract_session_tokens(res):
    session_data = _to_dict(res)
    if not isinstance(session_data, dict):
        return None, None, None

    if 'session' in session_data and isinstance(session_data.get('session'), dict):
        session_data = session_data['session']

    access_token = session_data.get('access_token')
    refresh_token = session_data.get('refresh_token')
    expires_at = session_data.get('expires_at')
    return access_token, refresh_token, expires_at


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name') or data.get('nombre_completo')
    username = (data.get('username') or data.get('nombre_usuario') or data.get('user_name') or (email.split('@')[0] if email else None))
    role = normalize_role(data.get('role', 'estudiante'))

    if not email or not password or not username:
        return jsonify({'error': 'email, password and username required'}), 400

    username = build_unique_username(username)

    metadata = {
        'nombre_usuario': username,
        'username': username,
        'user_name': username,
        'name': username,
        'nickname': username,
        'display_name': username,
        'nombre_completo': full_name,
        'full_name': full_name,
        'rol': role,
    }

    # Crear usuario con Admin API para evitar el rate limit del email de confirmación
    try:
        res = admin_client.auth.admin.create_user(
            {
                'email': email,
                'password': password,
                'email_confirm': True,
                'data': metadata,
            }
        )
    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('Supabase admin create_user failed: %s\n%s', str(e), tb)
        return jsonify({'error': 'supabase signup failed', 'detail': str(e), 'trace': tb}), 500

    res_dict = _to_dict(res)
    # res_dict may contain a nested 'user' key depending on client version
    user = res_dict.get('user') if isinstance(res_dict, dict) and 'user' in res_dict else res_dict
    user_dict = _to_dict(user)
    user_id = None
    if isinstance(user_dict, dict):
        user_id = user_dict.get('id') or user_dict.get('user_id')
    if not user_id:
        return jsonify({'error': 'could not create user', 'detail': res_dict}), 400

    # Crear o actualizar perfil en la tabla perfiles sin romper el flujo si ya existe.
    try:
        existing = Usuario.query.get(user_id)
        if existing:
            existing.nombre_usuario = username
            existing.nombre_completo = full_name
            existing.rol = role
            existing.actualizado_el = datetime.utcnow()
        else:
            perfil = Usuario(
                id=user_id,
                nombre_usuario=username,
                nombre_completo=full_name,
                rol=role,
                creado_el=datetime.utcnow(),
                actualizado_el=datetime.utcnow(),
            )
            db.session.add(perfil)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'warning': 'user created in auth but profile creation failed', 'detail': str(e)}), 201

    try:
        admin_client.auth.admin.update_user_by_id(user_id, {'email_confirm': True})
    except Exception:
        pass

    try:
        session_res = client.auth.sign_in_with_password({'email': email, 'password': password})
        access_token, refresh_token, _expires_at = extract_session_tokens(session_res)
        if access_token:
            resp = make_response(jsonify({'ok': True, 'user_id': user_id, 'auto_login': True}))
            secure_cookie = request.is_secure
            resp.set_cookie('access_token', access_token, httponly=True, secure=secure_cookie, samesite='Lax', path='/')
            if refresh_token:
                resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=secure_cookie, samesite='Lax', path='/')
            return resp, 201
    except Exception as e:
        current_app.logger.warning('Auto-login after registration failed: %s', str(e))

    return jsonify({'ok': True, 'user_id': user_id, 'auto_login': False}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    try:
        res = client.auth.sign_in_with_password({'email': email, 'password': password})
    except Exception as e:
        return jsonify({'error': 'supabase signin failed', 'detail': str(e)}), 500

    access_token, refresh_token, expires_at = extract_session_tokens(res)

    if not access_token:
        return jsonify({'error': 'could not retrieve access token', 'detail': res}), 500

    resp = make_response(jsonify({'ok': True}))
    secure_cookie = request.is_secure
    # Set HttpOnly cookies for access and refresh tokens
    resp.set_cookie('access_token', access_token, httponly=True, secure=secure_cookie, samesite='Lax', path='/')
    if refresh_token:
        resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=secure_cookie, samesite='Lax', path='/')
    return resp, 200


@bp.route('/logout', methods=['POST'])
def logout():
    # Clear auth cookies
    resp = make_response(jsonify({'ok': True}))
    resp.set_cookie('access_token', '', expires=0, httponly=True, path='/')
    resp.set_cookie('refresh_token', '', expires=0, httponly=True, path='/')
    return resp, 200


def require_auth(f):
    def wrapper(*args, **kwargs):
        # Try Authorization header first, then cookie
        token = None
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
        else:
            token = request.cookies.get('access_token')

        if not token:
            return jsonify({'error': 'missing token'}), 401

        try:
            user = admin_client.auth.get_user(token)
        except Exception:
            return jsonify({'error': 'invalid token'}), 401

        g.current_user = user
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@bp.route('/me', methods=['GET'])
@require_auth
def me():
    user = g.current_user
    user_info = _to_dict(user)

    profile = None
    try:
        user_id = None
        if isinstance(user_info, dict):
            user_id = user_info.get('id') or user_info.get('user_id')
        perfil = Usuario.query.get(user_id)
        if perfil:
            profile = {
                'id': perfil.id,
                'nombre_usuario': perfil.nombre_usuario,
                'nombre_completo': perfil.nombre_completo,
                'rol': perfil.rol,
            }
    except Exception:
        profile = None

    return jsonify({'user': user_info, 'profile': profile}), 200


@bp.route('/ui', methods=['GET'])
def ui():
    return render_template('auth.html')
