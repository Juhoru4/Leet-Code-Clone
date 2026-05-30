"""Endpoints para listar problemas y obtener su informacion."""

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, g
from app.auth import require_auth
from models.problema import Problema
from models.caso_prueba import CasoPrueba
from models.categoria import Categoria
import uuid
from app.extensions import db

problems_bp = Blueprint('problems', __name__)

# Mientras no exista menú principal, la raíz redirige al login/registro.
@problems_bp.route('/')
def home():
    return redirect(url_for('auth.ui'))


@problems_bp.route('/problems/ui')
def index():
    """Página principal: lista de problemas (HU2)."""
    return render_template('problems.html')


@problems_bp.route('/problems/<problema_id>/ui')
def resolver_ui(problema_id):
    """Renderiza la UI de resolución de un problema específico."""
    return render_template('resolver_problema.html', problema_id=problema_id)


@problems_bp.route('/api/problems', methods=['GET'])
def get_problems():
    """
    RF-02: Retorna la lista de problemas activos.
    RF-02.4 / RF-02.5: Acepta ?difficulty=facil|medio|dificil para filtrar.
    """
    difficulty = request.args.get('difficulty')

    query = Problema.query.filter_by(esta_activo=True)

    if difficulty:
        query = query.filter_by(dificultad=difficulty)

    # RF-02.2: ordenar primero por dificultad (facil->medio->dificil), luego por título
    orden = {'facil': 0, 'medio': 1, 'dificil': 2}
    problemas = query.order_by(Problema.titulo).all()
    problemas.sort(key=lambda p: orden.get(p.dificultad, 99))

    return jsonify([p.to_dict() for p in problemas])

@problems_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """Retorna todas las categorías disponibles."""
    categorias = Categoria.query.all()
    return jsonify({
        "categorias": [cat.to_dict() for cat in categorias]
    }), 200

@problems_bp.route('/api/problems/<problema_id>', methods=['GET'])
def get_problem(problema_id):
    """Retorna un problema específico por su ID con sus casos de prueba."""
    problema = Problema.query.get(problema_id)
    if problema is None:
        return jsonify({"error": "Problema no encontrado"}), 404
    
    problema_dict = problema.to_dict()
    
    # Incluir todos los casos de prueba (públicos y privados) para edición
    casos = CasoPrueba.query.filter_by(problema_id=problema_id).order_by(CasoPrueba.orden).all()
    problema_dict['casos_prueba'] = [
        {
            'id': caso.id,
            'descripcion': caso.descripcion,
            'entrada': caso.entrada,
            'salida_esperada': caso.salida_esperada,
            'es_publico': caso.es_publico,
            'orden': caso.orden
        }
        for caso in casos
    ]
    
    return jsonify(problema_dict), 200


@problems_bp.route('/api/problems/<problema_id>/test-cases', methods=['GET'])
@require_auth
def get_test_cases(problema_id):
    """Retorna los casos de prueba públicos de un problema."""
    problema = Problema.query.get(problema_id)
    if problema is None:
        return jsonify({"error": "Problema no encontrado"}), 404

    casos = CasoPrueba.query.filter_by(
        problema_id=problema_id,
        es_publico=True
    ).order_by(CasoPrueba.orden).all()

    return jsonify({
        "problema_id": problema_id,
        "casos": [
            {
                "id": caso.id,
                "descripcion": caso.descripcion,
                "entrada": caso.entrada,
                "salida_esperada": caso.salida_esperada,
                "orden": caso.orden,
            }
            for caso in casos
        ]
    }), 200
    
@problems_bp.route('/api/problems/crear', methods=['POST'])
@require_auth
def crear_problema():
    data = request.get_json()

    nuevo_problema = Problema(
        id=str(uuid.uuid4()),
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        dificultad=data.get('dificultad'),
        categoria_id=data.get('categoria_id'),
        restricciones=data.get('restricciones'),
        ejemplo_entrada=data.get('ejemplo_entrada'),
        ejemplo_salida=data.get('ejemplo_salida'),
        codigo_base_python=data.get('codigo_base_python'),
        codigo_base_java=data.get('codigo_base_java'),
        codigo_base_cpp=data.get('codigo_base_cpp'),
        limite_tiempo_ms=data.get('limite_tiempo_ms'),
        limite_memoria_mb=data.get('limite_memoria_mb'),
        esta_activo=data.get('esta_activo', True),
        creado_por=g.current_user_id
    )

    db.session.add(nuevo_problema)
    db.session.flush()  # Para obtener el ID antes de hacer commit

    # Crear los casos de prueba
    casos_prueba = data.get('casos_prueba', [])
    for caso_data in casos_prueba:
        caso = CasoPrueba(
            id=str(uuid.uuid4()),
            problema_id=nuevo_problema.id,
            descripcion=caso_data.get('descripcion'),
            entrada=caso_data.get('entrada'),
            salida_esperada=caso_data.get('salida_esperada'),
            es_publico=caso_data.get('es_publico', True),
            orden=caso_data.get('orden', 1)
        )
        db.session.add(caso)

    db.session.commit()

    return jsonify({
        "mensaje": "Problema creado",
        "problema": nuevo_problema.to_dict()
    }), 201


@problems_bp.route('/api/problems/<problema_id>', methods=['PUT'])
@require_auth
def actualizar_problema(problema_id):
    """Actualiza un problema existente y sus casos de prueba."""
    problema = Problema.query.get(problema_id)
    if problema is None:
        return jsonify({"error": "Problema no encontrado"}), 404
    
    data = request.get_json()
    
    try:
        # Actualizar campos del problema
        problema.titulo = data.get('titulo')
        problema.descripcion = data.get('descripcion')
        problema.dificultad = data.get('dificultad')
        problema.categoria_id = data.get('categoria_id')
        problema.restricciones = data.get('restricciones')
        problema.ejemplo_entrada = data.get('ejemplo_entrada')
        problema.ejemplo_salida = data.get('ejemplo_salida')
        problema.codigo_base_python = data.get('codigo_base_python')
        problema.codigo_base_java = data.get('codigo_base_java')
        problema.codigo_base_cpp = data.get('codigo_base_cpp')
        problema.limite_tiempo_ms = data.get('limite_tiempo_ms')
        problema.limite_memoria_mb = data.get('limite_memoria_mb')
        problema.esta_activo = data.get('esta_activo', True)
        
        db.session.flush()
        
        # Actualizar casos de prueba
        # Primero, eliminar los casos existentes
        CasoPrueba.query.filter_by(problema_id=problema_id).delete()
        
        # Luego, crear los nuevos casos
        casos_prueba = data.get('casos_prueba', [])
        for caso_data in casos_prueba:
            caso = CasoPrueba(
                id=str(uuid.uuid4()),
                problema_id=problema_id,
                descripcion=caso_data.get('descripcion'),
                entrada=caso_data.get('entrada'),
                salida_esperada=caso_data.get('salida_esperada'),
                es_publico=caso_data.get('es_publico', True),
                orden=caso_data.get('orden', 1)
            )
            db.session.add(caso)
        
        db.session.commit()
        
        return jsonify({
            "mensaje": "Problema actualizado correctamente",
            "problema": problema.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar: {str(e)}"}), 500


@problems_bp.route('/api/problems/<problema_id>', methods=['DELETE'])
@require_auth
def eliminar_problema(problema_id):
    """Elimina un problema y todos sus casos de prueba asociados."""
    problema = Problema.query.get(problema_id)
    if problema is None:
        return jsonify({"error": "Problema no encontrado"}), 404

    try:
        # Los casos de prueba se eliminan automáticamente por cascade
        db.session.delete(problema)
        db.session.commit()
        return jsonify({"mensaje": "Problema eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar: {str(e)}"}), 500