from flask import Blueprint, jsonify
from app.auth import require_auth
from services.problemas import get_casos_prueba_publicos, get_problema_por_id
from models.problema import Problema

problems_bp = Blueprint("problemas", __name__)


@problems_bp.route("/<problema_id>", methods=["GET"])
def obtener_problema(problema_id):
    # First try to load from the SQLAlchemy model (production DB)
    try:
        p = Problema.query.get(problema_id)
        if p:
            return jsonify(p.to_dict()), 200
    except Exception:
        # If DB not available or query fails, fall back to the mock provider
        p = None

    # fallback to the mock service
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