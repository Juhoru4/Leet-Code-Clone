import uuid
from threading import Lock
from flask import Blueprint, request, jsonify, session, render_template, g
from services.ejecutor import ejecutar_codigo
from app.extensions import db
from models.envio import Envio
from Codigo.app.auth import require_auth

ejecucion_bp = Blueprint("ejecucion", __name__)
_ejecuciones_activas = set()
_lock_ejecuciones = Lock()

# Mapeo de tipo_error del executor → estado del modelo
ESTADOS = {
    None:          "correcto",
    "compilacion": "error_compilacion",
    "ejecucion":   "error_ejecucion",
    "timeout":     "timeout",
    "sistema":     "error_sistema",
}


@ejecucion_bp.route("/ejecutar", methods=["GET"])
def ver_ejecutar():
    return render_template("problema.html")

@ejecucion_bp.route("/ejecutar", methods=["POST"])
@require_auth
def ejecutar():
    """Ejecuta código con autenticación Supabase."""
    datos = request.get_json()

    codigo      = datos.get("codigo", "")
    lenguaje    = datos.get("lenguaje", "")
    problema_id = datos.get("problema_id")

    if not codigo or not lenguaje or not problema_id:
        return jsonify({"error": "Faltan datos"}), 400

    # Obtener usuario_id desde g.current_user (del decorador require_auth)
    usuario_id = g.current_user.id

    with _lock_ejecuciones:
        if usuario_id in _ejecuciones_activas:
            return jsonify({
                "error": "Ya hay una ejecución en curso para este usuario.",
                "estado": "ejecutando"
            }), 409
        _ejecuciones_activas.add(usuario_id)

    try:
        # Ejecutar el código
        resultado = ejecutar_codigo(codigo, lenguaje)

        # Traducir tipo_error a estado
        tipo_error = resultado.get("tipo_error")
        if resultado.get("supero_tiempo_limite"):
            tipo_error = "timeout"
        estado = ESTADOS.get(tipo_error, "error_sistema")

        # Guardar el envío usando el modelo de tu compañero
        envio = Envio(
            id              = str(uuid.uuid4()),
            usuario_id      = usuario_id,
            problema_id     = problema_id,
            lenguaje        = lenguaje,
            codigo_fuente   = codigo,
            estado          = estado,
            mensaje_error   = resultado.get("error") or None,
            total_casos     = None,  # se llenará cuando implementes casos de prueba
            casos_pasados   = None,
            tiempo_ejecucion_ms = None,
            memoria_usada_kb    = None,
        )
        db.session.add(envio)
        db.session.commit()

        # Agregar el estado al resultado para que el HTML lo muestre
        resultado["estado"] = estado
        return jsonify(resultado)
    finally:
        with _lock_ejecuciones:
            _ejecuciones_activas.discard(usuario_id)