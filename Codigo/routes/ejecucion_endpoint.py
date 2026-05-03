import uuid
from flask import Blueprint, request, jsonify, session
from services.ejecutor import ejecutar_codigo
from app.extensions import db
from models.envio import Envio

ejecucion_bp = Blueprint("ejecucion", __name__)

# Mapeo de tipo_error del executor → estado del modelo
ESTADOS = {
    None:          "correcto",
    "compilacion": "error_compilacion",
    "ejecucion":   "error_ejecucion",
    "timeout":     "timeout",
    "sistema":     "error_sistema",
}

@ejecucion_bp.route("/ejecutar", methods=["POST"])
def ejecutar():
    datos = request.get_json()

    codigo      = datos.get("codigo", "")
    lenguaje    = datos.get("lenguaje", "")
    problema_id = datos.get("problema_id")

    if not codigo or not lenguaje or not problema_id:
        return jsonify({"error": "Faltan datos"}), 400

    # Cuando el login esté listo reemplaza esto por:
    # usuario_id = session.get("usuario_id")
    # if not usuario_id:
    #     return jsonify({"error": "No autenticado"}), 401
    usuario_id = "00000000-0000-0000-0000-000000000001"  # ← temporal

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