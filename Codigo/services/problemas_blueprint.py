import uuid
from flask import Blueprint, jsonify, request, g
from app.auth import require_auth
from models.envio import guardar_envio, obtener_envio, actualizar_resultados
from services.ejecutor import ejecutar_codigo
from models.caso_prueba import CasoPrueba

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

    casos = CasoPrueba.query.filter_by(
        problema_id=problema_id,
        es_publico=True
    ).order_by(CasoPrueba.orden).all()

    if not casos:
        return jsonify({"error": "No hay casos de prueba para este problema"}), 404

    submission_id = str(uuid.uuid4())
    resultados = []

    for caso in casos:
        resultado = ejecutar_codigo(codigo, lenguaje, stdin=caso.entrada)

        output_obtenido = (resultado.get("stdout") or "").strip()
        salida_esperada = (caso.salida_esperada or "").strip()

        if resultado.get("tipo_error"):
            estado_caso = "Fallo"
            output_obtenido = resultado.get("stderr") or resultado.get("error") or "Error de ejecución"
        elif output_obtenido == salida_esperada:
            estado_caso = "Aprobado"
        else:
            estado_caso = "Fallo"

        resultados.append({
            "caso_id": caso.id,
            "descripcion": caso.descripcion,
            "estado": estado_caso,
            "output": output_obtenido,
            "esperado": salida_esperada
        })

    casos_pasados = sum(1 for r in resultados if r["estado"] == "Aprobado")

    guardar_envio(submission_id, problema_id, lenguaje, codigo)
    actualizar_resultados(submission_id, resultados)

    return jsonify({
        "submission_id": submission_id,
        "status": "Completado",
        "estado": "Completado",
        "casos_pasados": casos_pasados,
        "total_casos": len(casos),
        "resultado": resultados
    }), 200


@submissions_bp.route("/<submission_id>/results", methods=["GET"])
@require_auth
def obtener_resultados(submission_id):
    envio = obtener_envio(submission_id)
    if envio is None:
        return jsonify({"error": "Envío no encontrado"}), 404
    return jsonify(envio), 200