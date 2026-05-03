from flask import Blueprint, jsonify
from app.auth import require_auth
from services.problema import get_casos_prueba_publicos, get_problema_por_id

problems_bp = Blueprint("problemas", __name__)


@problems_bp.route("/<problema_id>", methods=["GET"])
@require_auth
def obtener_problema(problema_id):
    problema = get_problema_por_id(problema_id)
    if problema is None:
        return jsonify({"error": "Problema no encontrado"}), 404
    return jsonify(problema), 200


@problems_bp.route("/<problema_id>/test-cases", methods=["GET"])
@require_auth
def obtener_casos_prueba(problema_id):
    casos = get_casos_prueba_publicos(problema_id)
    if casos is None:
        return jsonify({"error": "Problema no encontrado"}), 404
    return jsonify(casos), 200