import uuid
from app import create_app
from app.extensions import db
from models.problema import Problema
from models.categoria import Categoria

app = create_app()

with app.app_context():
    
    def get_or_create_categoria(nombre, slug):
        cat = Categoria.query.filter_by(slug=slug).first()
        if not cat:
            cat = Categoria(id=str(uuid.uuid4()), nombre=nombre, slug=slug)
            db.session.add(cat)
            db.session.flush()
        return cat

    cat1 = get_or_create_categoria("Arreglos", "arreglos")
    cat2 = get_or_create_categoria("Strings", "strings")
    cat3 = get_or_create_categoria("Recursión", "recursion")

    # Crear problemas
    problemas = [
        Problema(
            id=str(uuid.uuid4()),
            titulo="Dos Sumas",
            descripcion="Dado un arreglo de enteros, retorna los índices de los dos números que suman el objetivo.",
            dificultad="facil",
            categoria_id=cat1.id,
            esta_activo=True,
        ),
        Problema(
            id=str(uuid.uuid4()),
            titulo="Invertir String",
            descripcion="Escribe una función que invierta un string dado.",
            dificultad="facil",
            categoria_id=cat2.id,
            esta_activo=True,
        ),
        Problema(
            id=str(uuid.uuid4()),
            titulo="Suma de Subconjuntos",
            descripcion="Dado un arreglo y un objetivo, determina si existe algún subconjunto que sume el objetivo.",
            dificultad="medio",
            categoria_id=cat3.id,
            esta_activo=True,
        ),
        Problema(
            id=str(uuid.uuid4()),
            titulo="Árbol Binario de Búsqueda",
            descripcion="Implementa la inserción y búsqueda en un árbol binario de búsqueda.",
            dificultad="dificil",
            categoria_id=cat1.id,
            esta_activo=True,
        ),
    ]
    db.session.add_all(problemas)
    db.session.commit()
    print(f"{len(problemas)} problemas insertados correctamente")