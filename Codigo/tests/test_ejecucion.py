import pytest
from app import create_app
from app.extensions import db
from models.envio import Envio


@pytest.fixture(autouse=True)
def mock_ejecutor(monkeypatch):
    def fake_ejecutar_codigo(codigo, lenguaje):
        if lenguaje == "ruby":
            return {
                "output": "",
                "error": "Lenguaje 'ruby' no soportado",
                "tipo_error": "sistema",
                "supero_tiempo_limite": False,
            }

        if lenguaje == "java":
            return {
                "output": "",
                "error": "error: ';' expected",
                "tipo_error": "compilacion",
                "supero_tiempo_limite": False,
            }

        if "while True" in codigo:
            return {
                "output": "",
                "error": "Tiempo límite excedido (3 segundos)",
                "tipo_error": None,
                "supero_tiempo_limite": True,
            }

        if "1/0" in codigo:
            return {
                "output": "",
                "error": "ZeroDivisionError: division by zero",
                "tipo_error": "ejecucion",
                "supero_tiempo_limite": False,
            }

        return {
            "output": "hola\n",
            "error": "",
            "tipo_error": None,
            "supero_tiempo_limite": False,
        }

    monkeypatch.setattr("routes.ejecucion_endpoint.ejecutar_codigo", fake_ejecutar_codigo)

@pytest.fixture
def cliente():
    app = create_app(database_uri="sqlite:///:memory:")
    app.config["TESTING"] = True
    
    with app.app_context():
        db.create_all()
        # Mantener el app context durante todo el test
        client = app.test_client()
        yield client
        db.drop_all()

PROBLEMA_ID = "00000000-0000-0000-0000-000000000099"

# ── Tests del executor ──────────────────────────────────────────

def test_ejecucion_correcta(cliente):
    respuesta = cliente.post("/ejecutar", json={
        "codigo": "print('hola')",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["estado"] == "correcto"
    assert "hola" in datos["output"]

def test_error_compilacion_java(cliente):
    codigo_roto = """
    public class Solution {
        public static void main(String[] args) {
            System.out.println("hola")
        }
    }
    """
    respuesta = cliente.post("/ejecutar", json={
        "codigo": codigo_roto,
        "lenguaje": "java",
        "problema_id": PROBLEMA_ID
    })
    datos = respuesta.get_json()

    assert datos["estado"] == "error_compilacion"
    assert datos["output"] == ""

def test_error_ejecucion_python(cliente):
    respuesta = cliente.post("/ejecutar", json={
        "codigo": "print(1/0)",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })
    datos = respuesta.get_json()

    assert datos["estado"] == "error_ejecucion"
    assert "ZeroDivisionError" in datos["error"]

def test_timeout(cliente):
    respuesta = cliente.post("/ejecutar", json={
        "codigo": "while True: pass",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })
    datos = respuesta.get_json()

    assert datos["estado"] == "timeout"

def test_lenguaje_no_soportado(cliente):
    respuesta = cliente.post("/ejecutar", json={
        "codigo": "puts 'hola'",
        "lenguaje": "ruby",
        "problema_id": PROBLEMA_ID
    })
    datos = respuesta.get_json()

    assert "error" in datos

def test_faltan_datos(cliente):
    respuesta = cliente.post("/ejecutar", json={
        "codigo": "print('hola')"
    })
    assert respuesta.status_code == 400

# ── Tests de persistencia ───────────────────────────────────────

def test_envio_se_guarda_en_bd(cliente):
    cliente.post("/ejecutar", json={
        "codigo": "print('hola')",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })

    with cliente.application.app_context():
        envios = Envio.query.all()
        assert len(envios) == 1
        assert envios[0].lenguaje == "python"
        assert envios[0].estado == "correcto"
        assert envios[0].codigo_fuente == "print('hola')"

def test_envio_guarda_estado_error(cliente):
    cliente.post("/ejecutar", json={
        "codigo": "print(1/0)",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })

    with cliente.application.app_context():
        envio = Envio.query.first()
        assert envio.estado == "error_ejecucion"
        assert envio.mensaje_error is not None

def test_envio_tiene_uuid(cliente):
    """Verifica que cada envío recibe un UUID único."""
    cliente.post("/ejecutar", json={
        "codigo": "print('a')",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })
    cliente.post("/ejecutar", json={
        "codigo": "print('b')",
        "lenguaje": "python",
        "problema_id": PROBLEMA_ID
    })

    with cliente.application.app_context():
        envios = Envio.query.all()
        ids = [e.id for e in envios]
        assert len(ids) == 2
        assert ids[0] != ids[1]  # los UUIDs son únicos