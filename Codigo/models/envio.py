from app.extensions import db
from datetime import datetime


class Envio(db.Model):
    __tablename__ = 'envios'

    id = db.Column(db.String(36), primary_key=True)
    usuario_id = db.Column(db.String(36), db.ForeignKey('perfiles.id'), nullable=True)
    problema_id = db.Column(db.String(36), db.ForeignKey('problemas.id'), nullable=True)
    lenguaje = db.Column(db.String(20), nullable=True)
    codigo_fuente = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(30), nullable=True)
    total_casos = db.Column(db.Integer, nullable=True)
    casos_pasados = db.Column(db.Integer, nullable=True)
    tiempo_ejecucion_ms = db.Column(db.Integer, nullable=True)
    memoria_usada_kb = db.Column(db.Integer, nullable=True)
    mensaje_error = db.Column(db.Text, nullable=True)
    enviado_el = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    usuario = db.relationship('Usuario', back_populates='envios')
    problema = db.relationship('Problema', back_populates='envios')
    resultados = db.relationship('ResultadoEnvio', back_populates='envio', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Envio usuario_id={self.usuario_id} problema_id={self.problema_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'problema_id': self.problema_id,
            'lenguaje': self.lenguaje,
            'estado': self.estado,
            'casos_pasados': self.casos_pasados,
            'total_casos': self.total_casos,
            'enviado_el': self.enviado_el.isoformat() if self.enviado_el else None,
        }


# ---- Mock temporal (se elimina cuando se conecte la BD real) ----

ENVIOS_MOCK = []


def guardar_envio(submission_id, problema_id, lenguaje_programacion, codigo):
    envio = {
        "id": submission_id,
        "problema_id": problema_id,
        "lenguaje_programacion": lenguaje_programacion,
        "codigo": codigo,
        "estado": "en cola",
        "resultado": []
    }
    ENVIOS_MOCK.append(envio)
    return envio


def obtener_envio(submission_id):
    for envio in ENVIOS_MOCK:
        if envio["id"] == submission_id:
            return envio
    return None


def actualizar_resultados(submission_id, resultado):
    envio = obtener_envio(submission_id)
    if envio is not None:
        envio["estado"] = "Completado"
        envio["resultado"] = resultado
    return envio
