"""Endpoints para previsualizar y evaluar envios."""

import uuid
from flask import Blueprint, jsonify, request
from app.auth import require_auth
from app.extensions import db
from services.ejecucion.ejecutor import ejecutar_codigo
from models.envio import Envio
from models.caso_prueba import CasoPrueba
from models.resultado_envio import ResultadoEnvio


submissions_bp = Blueprint("submissions", __name__)

def normalizar_salida_booleana(valor: str) -> str:
    limpio = (valor or "").strip()
    lower = limpio.lower()
    if lower in ("true", "false"):
        return lower
    return limpio

def inyectar_stdin(codigo, lenguaje, entrada):
    if lenguaje == "python":
        return (
            f"import sys\n"
            f"sys.stdin = __import__('io').StringIO({repr(entrada.strip())})\n\n"
        ) + codigo   # ← de vuelta al INICIO

    elif lenguaje in ("java", "cpp"):
        return codigo

    return codigo

@submissions_bp.route("/test-run", methods=["POST"])
@require_auth
def test_run():
    # El frontend nos manda el problema, el lenguaje y el código del usuario.
    datos = request.get_json()

    problema_id = datos.get("problema_id")
    lenguaje = datos.get("language")
    codigo = datos.get("source_code")

    # Si falta cualquiera de los campos mínimos, no podemos evaluar nada.
    if not all([problema_id, lenguaje, codigo]):
        return jsonify({
            "error": "Faltan campos: problema_id, language, source_code"
        }), 400

    # Traemos solo los casos públicos para este problema; son los que ve y usa el usuario.
    casos = CasoPrueba.query.filter_by(
        problema_id=problema_id,
        es_publico=True
    ).order_by(CasoPrueba.orden).all()

    # Sin casos no hay contra qué comparar la solución.
    if not casos:
        return jsonify({
            "error": "No hay casos de prueba para este problema"
        }), 404

    # Creamos un ID único para guardar luego este intento y su resultado.
    submission_id = str(uuid.uuid4())

    resultados = []

    # Recorremos cada caso de prueba para ejecutar el código del usuario con esa entrada.
    for caso in casos:
        
        print(f"DEBUG caso '{caso.descripcion}': entrada={repr(caso.entrada)}")  # ← agrega esto
        codigo_con_input = inyectar_stdin(codigo, lenguaje, caso.entrada or "")
    
    
        codigo_con_input = inyectar_stdin(
            codigo,
            lenguaje,
            caso.entrada or ""
        )

        resultado = ejecutar_codigo(
            codigo_con_input,
            lenguaje
        )

        output_obtenido = (
            resultado.get("stdout") or ""
        ).strip()

        salida_esperada = (
            caso.salida_esperada or ""
        ).strip()

        # Si el ejecutor reporta un error, el caso falla aunque haya salida parcial.
        tipo_error = None
        if resultado.get("tipo_error"):
            estado_caso = "Fallo"
            tipo_error = resultado.get("tipo_error")
            detalle_error = (
                resultado.get("stderr")
                or resultado.get("error")
                or "Error de ejecución"
            )
            output_obtenido = detalle_error

        elif normalizar_salida_booleana(output_obtenido).replace(" ", "") == normalizar_salida_booleana(salida_esperada).replace(" ", ""):
            estado_caso = "Aprobado"

        else:
            estado_caso = "Fallo"

        # Guardamos el detalle por caso para devolverlo al frontend y poder mostrar el desglose.
        resultados.append({
            "caso_id": caso.id,
            "descripcion": caso.descripcion,
            "estado": estado_caso,
            "tipo_error": tipo_error,
            "output": output_obtenido,
            "esperado": salida_esperada,
            "tiempo_ejecucion_ms": resultado.get("time_ms"),
            "mensaje_error": resultado.get("stderr")
        })

    casos_pasados = sum(
        1 for r in resultados
        if r["estado"] == "Aprobado"
    )

    # Crear envío principal
    envio = Envio(
        id=submission_id,
        problema_id=problema_id,
        lenguaje=lenguaje,
        codigo_fuente=codigo,
        estado="Completado",
        total_casos=len(casos),
        casos_pasados=casos_pasados
    )

    db.session.add(envio)

    # Guardar resultados individuales
    for r in resultados:
        resultado_envio = ResultadoEnvio(
            id=str(uuid.uuid4()),
            envio_id=submission_id,
            caso_prueba_id=r["caso_id"],
            estado=r["estado"],
            salida_real=r["output"],
            tiempo_ejecucion_ms=r["tiempo_ejecucion_ms"],
            mensaje_error=r["mensaje_error"]
        )

        db.session.add(resultado_envio)

    # Guardar todo en DB
    db.session.commit()
    
    # HU5: registrar envío de solución
    from routes.auditoria import registrar_evento
    registrar_evento(
        tipo_evento='envio_solucion',
        usuario_id=str(envio.usuario_id) if hasattr(envio, 'usuario_id') else None,
        nombre_usuario=None,
        detalle=f'Problema: {problema_id} | Lenguaje: {lenguaje} | Casos pasados: {casos_pasados}/{len(casos)}'
    )

    # Respuesta final que consume el frontend para pintar el resultado.
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

    envio = db.session.get(Envio, submission_id)

    if envio is None:
        return jsonify({
            "error": "Envío no encontrado"
        }), 404

    return jsonify({
        **envio.to_dict(),
        "resultados": [
            resultado.to_dict()
            for resultado in envio.resultados
        ]
    }), 200
    
@submissions_bp.route("/preview", methods=["POST"])
@require_auth
def preview_run():
    datos = request.get_json()
    problema_id = datos.get("problema_id")
    lenguaje = datos.get("language")
    codigo = datos.get("source_code")

    if not all([problema_id, lenguaje, codigo]):
        return jsonify({"error": "Faltan campos"}), 400

    casos = CasoPrueba.query.filter_by(
        problema_id=problema_id,
        es_publico=True
    ).order_by(CasoPrueba.orden).all()

    if not casos:
        return jsonify({"error": "No hay casos de prueba"}), 404

    resultados = []
    for caso in casos:
        codigo_con_input = inyectar_stdin(codigo, lenguaje, caso.entrada or "")
        resultado = ejecutar_codigo(codigo_con_input, lenguaje)

        output_obtenido = (resultado.get("stdout") or "").strip()
        salida_esperada = (caso.salida_esperada or "").strip()

        tipo_error = None
        if resultado.get("tipo_error"):
            estado_caso = "Fallo"
            tipo_error = resultado.get("tipo_error")
            detalle_error = resultado.get("stderr") or "Error de ejecución"
            output_obtenido = detalle_error
        elif normalizar_salida_booleana(output_obtenido).replace(" ", "") == normalizar_salida_booleana(salida_esperada).replace(" ", ""):
            estado_caso = "Aprobado"
        else:
            estado_caso = "Fallo"

        resultados.append({
            "caso_id": caso.id,
            "descripcion": caso.descripcion,
            "estado": estado_caso,
            "tipo_error": tipo_error,
            "output": output_obtenido,
            "esperado": salida_esperada,
        })

    casos_pasados = sum(1 for r in resultados if r["estado"] == "Aprobado")

    # NO guarda en Supabase, solo retorna resultados
    return jsonify({
        "casos_pasados": casos_pasados,
        "total_casos": len(casos),
        "resultado": resultados
    }), 200