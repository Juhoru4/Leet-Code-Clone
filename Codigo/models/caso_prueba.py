from app.extensions import db
from datetime import datetime


class CasoPrueba(db.Model):
    __tablename__ = 'casos_prueba'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    problema_id = db.Column(db.String(36), db.ForeignKey('problemas.id'), nullable=True)  # UUID
    entrada = db.Column(db.Text, nullable=True)
    salida_esperada = db.Column(db.Text, nullable=True)
    descripcion = db.Column(db.String(200), nullable=True)
    es_publico = db.Column(db.Boolean, default=False)
    orden = db.Column(db.Integer, nullable=True)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    problema = db.relationship('Problema', back_populates='casos_prueba')
    resultados = db.relationship('ResultadoEnvio', back_populates='caso_prueba', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CasoPrueba problema_id={self.problema_id} orden={self.orden}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'problema_id': self.problema_id,
            'entrada': self.entrada,
            'salida_esperada': self.salida_esperada,
            'descripcion': self.descripcion,
            'es_publico': self.es_publico,
            'orden': self.orden,
            'creado_el': self.creado_el.isoformat() if self.creado_el else None,
        }
