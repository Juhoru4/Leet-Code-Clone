import pytest

from app import create_app
from app.extensions import db
from models.caso_prueba import CasoPrueba
from models.envio import ENVIOS_MOCK


PROBLEMA_ID = "00000000-0000-0000-0000-000000000099"
USUARIO_ID = "11111111-1111-1111-1111-111111111111"
CASO_ID = "22222222-2222-2222-2222-222222222222"


@pytest.fixture(autouse=True)
def mock_auth_and_ejecutor(monkeypatch):
    def fake_get_user(token):
        return {"id": USUARIO_ID, "email": "test@example.com"}

    def fake_ejecutar_codigo(codigo, lenguaje, timeout_ms=None, memory_mb=None):
        if lenguaje == "ruby":
            return {
                "stdout": "",
                "stderr": "Lenguaje 'ruby' no soportado",
                "tipo_error": "sistema",
                "supero_tiempo_limite": False,
                "timeout": False,
            }

        if lenguaje == "java":
            return {
                "stdout": "",
                "stderr": "error: ';' expected",
                "tipo_error": "compilacion",
                "supero_tiempo_limite": False,
                "timeout": False,
            }

        if "while True" in codigo:
            return {
                "stdout": "",
                "stderr": "Tiempo límite excedido (3 segundos)",
                "tipo_error": "timeout",
                "supero_tiempo_limite": True,
                "timeout": True,
            }

        if "1/0" in codigo:
            return {
                "stdout": "",
                "stderr": "ZeroDivisionError: division by zero",
                "tipo_error": "ejecucion",
                "supero_tiempo_limite": False,
                "timeout": False,
            }

        return {
            "stdout": "hola\n",
            "stderr": "",
            "tipo_error": None,
            "supero_tiempo_limite": False,
            "timeout": False,
        }

    monkeypatch.setattr("app.auth.admin_client.auth.get_user", fake_get_user)
    monkeypatch.setattr("services.submissions_blueprint.ejecutar_codigo", fake_ejecutar_codigo)


@pytest.fixture
def cliente():
    app = create_app(database_uri="sqlite:///:memory:")
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        ENVIOS_MOCK.clear()
        db.session.add(
            CasoPrueba(
                id=CASO_ID,
                problema_id=PROBLEMA_ID,
                entrada="",
                salida_esperada="hola",
                descripcion="Caso público básico",
                es_publico=True,
                orden=1,
            )
        )
        db.session.commit()

        client = app.test_client()
        yield client

        ENVIOS_MOCK.clear()
        db.drop_all()


def _auth_headers():
    return {"Authorization": "Bearer test-token"}


def _post_ejecucion(cliente, codigo, lenguaje):
    return cliente.post(
        "/api/submissions/test-run",
        json={
            "codigo": codigo,
            "language": lenguaje,
            "problema_id": PROBLEMA_ID,
            "source_code": codigo,
        },
        headers=_auth_headers(),
    )


def test_ejecucion_correcta(cliente):
    respuesta = _post_ejecucion(cliente, "print('hola')", "python")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["estado"] == "Completado"
    assert datos["casos_pasados"] == 1
    assert datos["total_casos"] == 1
    assert datos["resultado"][0]["estado"] == "Aprobado"


def test_error_compilacion_java(cliente):
    codigo_roto = """
    public class Solution {
        public static void main(String[] args) {
            System.out.println("hola")
        }
    }
    """
    respuesta = _post_ejecucion(cliente, codigo_roto, "java")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["resultado"][0]["estado"] == "Fallo"
    assert "error: ';' expected" in datos["resultado"][0]["output"]


def test_error_ejecucion_python(cliente):
    respuesta = _post_ejecucion(cliente, "print(1/0)", "python")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["resultado"][0]["estado"] == "Fallo"
    assert "ZeroDivisionError" in datos["resultado"][0]["output"]


def test_timeout(cliente):
    respuesta = _post_ejecucion(cliente, "while True: pass", "python")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["resultado"][0]["estado"] == "Fallo"
    assert "Tiempo límite excedido" in datos["resultado"][0]["output"]


def test_lenguaje_no_soportado(cliente):
    respuesta = _post_ejecucion(cliente, "puts 'hola'", "ruby")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert datos["resultado"][0]["estado"] == "Fallo"
    assert "Lenguaje 'ruby' no soportado" in datos["resultado"][0]["output"]


def test_faltan_datos(cliente):
    respuesta = cliente.post(
        "/api/submissions/test-run",
        json={
            "codigo": "print('hola')",
            "language": "python",
            "problema_id": PROBLEMA_ID,
        },
        headers=_auth_headers(),
    )

    assert respuesta.status_code == 400


def test_no_hay_casos_publicos(cliente):
    with cliente.application.app_context():
        CasoPrueba.query.delete()
        db.session.commit()

    respuesta = _post_ejecucion(cliente, "print('hola')", "python")
    datos = respuesta.get_json()

    assert respuesta.status_code == 404
    assert "No hay casos de prueba" in datos["error"]


def test_requiere_autenticacion(cliente):
    respuesta = cliente.post(
        "/api/submissions/test-run",
        json={
            "codigo": "print('hola')",
            "language": "python",
            "problema_id": PROBLEMA_ID,
            "source_code": "print('hola')",
        },
    )

    assert respuesta.status_code == 401


def test_envio_se_guarda_en_memoria(cliente):
    respuesta = _post_ejecucion(cliente, "print('hola')", "python")
    datos = respuesta.get_json()

    with cliente.application.app_context():
        assert len(ENVIOS_MOCK) == 1
        assert ENVIOS_MOCK[0]["problema_id"] == PROBLEMA_ID
        assert ENVIOS_MOCK[0]["lenguaje_programacion"] == "python"
        assert ENVIOS_MOCK[0]["codigo"] == "print('hola')"
        assert ENVIOS_MOCK[0]["resultado"] == datos["resultado"]


def test_envio_guarda_estado_error(cliente):
    respuesta = _post_ejecucion(cliente, "print(1/0)", "python")

    with cliente.application.app_context():
        assert len(ENVIOS_MOCK) == 1
        assert ENVIOS_MOCK[0]["estado"] == "Completado"
        assert ENVIOS_MOCK[0]["resultado"][0]["estado"] == "Fallo"
        assert ENVIOS_MOCK[0]["resultado"][0]["output"] == "ZeroDivisionError: division by zero"


def test_envio_tiene_uuid(cliente):
    """Verifica que cada envío recibe un UUID único."""
    respuesta1 = _post_ejecucion(cliente, "print('a')", "python")
    respuesta2 = _post_ejecucion(cliente, "print('b')", "python")

    ids = [respuesta1.get_json()["submission_id"], respuesta2.get_json()["submission_id"]]
    assert len(ids) == 2
    assert ids[0] != ids[1]


def test_consulta_resultados_previos(cliente):
    respuesta = _post_ejecucion(cliente, "print('hola')", "python")
    submission_id = respuesta.get_json()["submission_id"]

    consulta = cliente.get(
        f"/api/submissions/{submission_id}/results",
        headers=_auth_headers(),
    )

    assert consulta.status_code == 200
    datos = consulta.get_json()
    assert datos["id"] == submission_id
    assert datos["resultado"][0]["estado"] == "Aprobado"