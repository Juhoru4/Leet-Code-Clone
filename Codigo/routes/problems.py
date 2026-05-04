from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from models.problema import Problema

problems_bp = Blueprint('problems', __name__)




@problems_bp.route('/problems/ui')
def index():
    """Página principal: lista de problemas (HU2)."""
    return render_template('problems.html')


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