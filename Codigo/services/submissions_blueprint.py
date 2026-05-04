import uuid
from flask import Blueprint, jsonify, request
from app.auth import require_auth
from models.envio import guardar_envio, obtener_envio

submissions_bp = Blueprint("submissions", __name__)

@submissions_bp.route("/test-run", methods=["POST"])
@require_auth
def test_run():
    datos = request.get_json()

    problema_id = datos.get("problema_id")
    lenguaje = datos.get("language")
    codigo = datos.get("source_code")

    if not all([problema_id, lenguaje, codigo]):
        return jsonify({"error": "Faltan campos: problema_id, language, source_code"}), 400

    submission_id = str(uuid.uuid4())
    guardar_envio(submission_id, problema_id, lenguaje, codigo)

    #Para luego:  Aquí irá el .delay() de Celery cuando esté configurado 
    return jsonify({
        "submission_id": submission_id,
        "status": "queued"
    }), 202


@submissions_bp.route("/<submission_id>/results", methods=["GET"])
@require_auth
def obtener_resultados(submission_id):
    envio = obtener_envio(submission_id)
    if envio is None:
        return jsonify({"error": "Envío no encontrado"}), 404
    return jsonify(envio), 200