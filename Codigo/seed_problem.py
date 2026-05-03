"""
seed_problems.py  —  HU2 / RF-02.1
Inserta categorías y al menos 3 problemas predefinidos en la base de datos.

Uso:
    cd Codigo
    python seed_problems.py
"""

import sys
import os
import uuid

# Asegura que los imports internos funcionen desde Codigo/
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from models.categoria import Categoria
from models.problema import Problema


# ─── Datos predefinidos ───────────────────────────────────────────────────────

CATEGORIAS = [
    {"nombre": "Arreglos",         "slug": "arreglos",         "descripcion": "Problemas con listas y arreglos."},
    {"nombre": "Cadenas",          "slug": "cadenas",          "descripcion": "Problemas con texto y cadenas de caracteres."},
    {"nombre": "Matemáticas",      "slug": "matematicas",      "descripcion": "Problemas de razonamiento matemático."},
]

PROBLEMAS = [
    # ── Fácil ─────────────────────────────────────────────────────────────────
    {
        "titulo":            "Suma de dos números",
        "descripcion":       (
            "Dado un arreglo de enteros y un valor objetivo, "
            "encuentra los índices de dos números que sumen el objetivo.\n\n"
            "Puedes asumir que cada entrada tiene exactamente una solución "
            "y no puedes usar el mismo elemento dos veces."
        ),
        "dificultad":        "facil",
        "categoria_slug":    "arreglos",
        "restricciones":     "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9",
        "ejemplo_entrada":   "nums = [2, 7, 11, 15], objetivo = 9",
        "ejemplo_salida":    "[0, 1]  # porque nums[0] + nums[1] == 9",
        "limite_tiempo_ms":  1000,
        "limite_memoria_mb": 128,
    },
    {
        "titulo":            "Palíndromo",
        "descripcion":       (
            "Dada una cadena de texto, determina si es un palíndromo "
            "(se lee igual de izquierda a derecha que de derecha a izquierda). "
            "Considera solo caracteres alfanuméricos e ignora mayúsculas."
        ),
        "dificultad":        "facil",
        "categoria_slug":    "cadenas",
        "restricciones":     "1 <= s.length <= 2 * 10^5",
        "ejemplo_entrada":   's = "A man, a plan, a canal: Panama"',
        "ejemplo_salida":    "True",
        "limite_tiempo_ms":  1000,
        "limite_memoria_mb": 128,
    },
    # ── Medio ─────────────────────────────────────────────────────────────────
    {
        "titulo":            "Número de islas",
        "descripcion":       (
            "Dado un mapa 2D compuesto por '1' (tierra) y '0' (agua), "
            "cuenta el número de islas. Una isla está rodeada de agua "
            "y se forma conectando tierras adyacentes de forma horizontal o vertical."
        ),
        "dificultad":        "medio",
        "categoria_slug":    "arreglos",
        "restricciones":     "1 <= m, n <= 300\ngrid[i][j] es '0' o '1'",
        "ejemplo_entrada":   (
            'grid = [\n'
            '  ["1","1","0","0","0"],\n'
            '  ["1","1","0","0","0"],\n'
            '  ["0","0","1","0","0"],\n'
            '  ["0","0","0","1","1"]\n'
            ']'
        ),
        "ejemplo_salida":    "3",
        "limite_tiempo_ms":  2000,
        "limite_memoria_mb": 256,
    },
    {
        "titulo":            "Anagramas en grupo",
        "descripcion":       (
            "Dado un arreglo de cadenas, agrupa los anagramas juntos. "
            "Puedes retornar el resultado en cualquier orden. "
            "Un anagrama es una palabra formada reorganizando las letras de otra."
        ),
        "dificultad":        "medio",
        "categoria_slug":    "cadenas",
        "restricciones":     "1 <= strs.length <= 10^4\n0 <= strs[i].length <= 100",
        "ejemplo_entrada":   'strs = ["eat","tea","tan","ate","nat","bat"]',
        "ejemplo_salida":    '[["bat"], ["nat","tan"], ["ate","eat","tea"]]',
        "limite_tiempo_ms":  2000,
        "limite_memoria_mb": 256,
    },
    # ── Difícil ───────────────────────────────────────────────────────────────
    {
        "titulo":            "Ventana mínima",
        "descripcion":       (
            "Dadas dos cadenas s y t, encuentra la subcadena más corta de s "
            "que contenga todos los caracteres de t. "
            "Si no existe tal subcadena, retorna la cadena vacía."
        ),
        "dificultad":        "dificil",
        "categoria_slug":    "cadenas",
        "restricciones":     "1 <= m, n <= 10^5\ns y t solo contienen letras inglesas",
        "ejemplo_entrada":   's = "ADOBECODEBANC", t = "ABC"',
        "ejemplo_salida":    '"BANC"',
        "limite_tiempo_ms":  3000,
        "limite_memoria_mb": 256,
    },
]


# ─── Lógica de inserción ─────────────────────────────────────────────────────

def seed():
    app = create_app()

    with app.app_context():
        # 1. Crear categorías (solo si no existen)
        cat_map = {}  # slug -> Categoria
        for cat_data in CATEGORIAS:
            existing = Categoria.query.filter_by(slug=cat_data["slug"]).first()
            if existing:
                cat_map[cat_data["slug"]] = existing
                print(f"  [skip] Categoría ya existe: {cat_data['nombre']}")
            else:
                nueva = Categoria(
                    id=str(uuid.uuid4()),
                    nombre=cat_data["nombre"],
                    slug=cat_data["slug"],
                    descripcion=cat_data["descripcion"],
                )
                db.session.add(nueva)
                cat_map[cat_data["slug"]] = nueva
                print(f"  [+] Categoría creada: {cat_data['nombre']}")

        db.session.flush()  # Persiste categorías antes de usarlas como FK

        # 2. Crear problemas (solo si no existen por título)
        insertados = 0
        for prob_data in PROBLEMAS:
            existing = Problema.query.filter_by(titulo=prob_data["titulo"]).first()
            if existing:
                print(f"  [skip] Problema ya existe: {prob_data['titulo']}")
                continue

            cat = cat_map.get(prob_data["categoria_slug"])
            nuevo = Problema(
                id=str(uuid.uuid4()),
                titulo=prob_data["titulo"],
                descripcion=prob_data["descripcion"],
                dificultad=prob_data["dificultad"],
                categoria_id=cat.id if cat else None,
                restricciones=prob_data.get("restricciones"),
                ejemplo_entrada=prob_data.get("ejemplo_entrada"),
                ejemplo_salida=prob_data.get("ejemplo_salida"),
                limite_tiempo_ms=prob_data.get("limite_tiempo_ms"),
                limite_memoria_mb=prob_data.get("limite_memoria_mb"),
                esta_activo=True,
            )
            db.session.add(nuevo)
            insertados += 1
            print(f"  [+] Problema creado: {prob_data['titulo']} ({prob_data['dificultad']})")

        db.session.commit()
        print(f"\n✓ Seed completo. {insertados} problema(s) insertado(s).")


if __name__ == '__main__':
    seed()