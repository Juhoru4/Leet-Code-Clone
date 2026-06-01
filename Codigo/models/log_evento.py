from app.extensions import db
from datetime import datetime


class LogEvento(db.Model):
    __tablename__ = 'logs_eventos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    usuario_id = db.Column(db.String(36), db.ForeignKey('perfiles.id'), nullable=True)
    nombre_usuario = db.Column(db.String(100), nullable=True)  # copia para no depender del JOIN
    tipo_evento = db.Column(db.String(50), nullable=False)

    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    detalle = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<LogEvento {self.tipo_evento} - {self.nombre_usuario} - {self.fecha_hora}>'

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'nombre_usuario': self.nombre_usuario or 'Desconocido',
            'tipo_evento': self.tipo_evento,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'detalle': self.detalle,
        }