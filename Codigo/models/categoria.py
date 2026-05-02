from app.extensions import db
from datetime import datetime


class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    nombre = db.Column(db.String(100), nullable=False, index=True)
    slug = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    problemas = db.relationship('Problema', back_populates='categoria', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'slug': self.slug,
            'descripcion': self.descripcion,
            'creado_el': self.creado_el.isoformat() if self.creado_el else None,
        }
