from app.extensions import db
from models.log_evento import LogEvento
from datetime import datetime


def registrar_evento(tipo_evento, usuario_id=None, nombre_usuario=None, detalle=None):

    try:
        log = LogEvento(
            usuario_id=usuario_id,
            nombre_usuario=nombre_usuario,
            tipo_evento=tipo_evento,
            fecha_hora=datetime.utcnow(),
            detalle=detalle,
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        # Si falla el log no debe romper la app principal
        db.session.rollback()
        print(f"[auditoria] Error registrando evento '{tipo_evento}': {e}")