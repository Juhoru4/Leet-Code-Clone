from app.extensions import db
from datetime import datetime


class ResultadoEnvio(db.Model):
    __tablename__ = 'resultados_envio'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    envio_id = db.Column(db.String(36), db.ForeignKey('envios.id'), nullable=True)  # UUID
    caso_prueba_id = db.Column(db.String(36), db.ForeignKey('casos_prueba.id'), nullable=True)  # UUID
    estado = db.Column(db.String(30), nullable=True)  # 'aprobado', 'fallido', 'error', etc.
    salida_real = db.Column(db.Text, nullable=True)
    tiempo_ejecucion_ms = db.Column(db.Integer, nullable=True)
    mensaje_error = db.Column(db.Text, nullable=True)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relaciones
    envio = db.relationship('Envio', back_populates='resultados')
    caso_prueba = db.relationship('CasoPrueba', back_populates='resultados')
    
    def __repr__(self):
        return f'<ResultadoEnvio envio_id={self.envio_id} estado={self.estado}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'envio_id': self.envio_id,
            'caso_prueba_id': self.caso_prueba_id,
            'estado': self.estado,
            'tiempo_ejecucion_ms': self.tiempo_ejecucion_ms,
            'creado_el': self.creado_el.isoformat() if self.creado_el else None,
        }
