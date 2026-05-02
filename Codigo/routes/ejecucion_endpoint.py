from flask import Blueprint, request, jsonify
from services.ejecutor import ejecutar_codigo

ejecucion_bp = Blueprint("ejecucion", __name__)

@ejecucion_bp.route("/ejecutar", methods=["POST"])
def ejecutar():
    datos = request.get_json()

    codigo = datos.get("codigo", "")
    lenguaje = datos.get("lenguaje", "")

    if not codigo or not lenguaje:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = ejecutar_codigo(codigo, lenguaje)
    return jsonify(resultado)