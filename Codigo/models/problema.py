from app.extensions import db
from datetime import datetime


class Problema(db.Model):
    __tablename__ = 'problemas'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    titulo = db.Column(db.String(200), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=False)
    dificultad = db.Column(db.String(10), nullable=True)
    categoria_id = db.Column(db.String(36), db.ForeignKey('categorias.id'), nullable=True)  # UUID
    restricciones = db.Column(db.Text, nullable=True)
    ejemplo_entrada = db.Column(db.Text, nullable=True)
    ejemplo_salida = db.Column(db.Text, nullable=True)
    limite_tiempo_ms = db.Column(db.Integer, nullable=True)
    limite_memoria_mb = db.Column(db.Integer, nullable=True)
    esta_activo = db.Column(db.Boolean, default=True)
    creado_por = db.Column(db.String(36), db.ForeignKey('perfiles.id'), nullable=True)  # UUID - admin que creó
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_el = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    categoria = db.relationship('Categoria', back_populates='problemas')
    envios = db.relationship('Envio', back_populates='problema', cascade='all, delete-orphan')
    autor = db.relationship('Usuario', back_populates='problemas_creados', foreign_keys=[creado_por])
    casos_prueba = db.relationship('CasoPrueba', back_populates='problema', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Problema {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'dificultad': self.dificultad,
            'categoria_id': self.categoria_id,
            'esta_activo': self.esta_activo,
            'creado_el': self.creado_el.isoformat() if self.creado_el else None,
        }
