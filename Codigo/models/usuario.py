from app.extensions import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = 'perfiles'  # Tabla de perfiles en Supabase
    
    id = db.Column(db.String(36), primary_key=True)  # UUID - FK a auth.users.id
    nombre_usuario = db.Column(db.String(50), nullable=False, index=True)
    nombre_completo = db.Column(db.String(150), nullable=True)
    rol = db.Column(db.String(20), default='estudiante', nullable=False)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_el = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    envios = db.relationship('Envio', back_populates='usuario', cascade='all, delete-orphan')
    problemas_creados = db.relationship('Problema', back_populates='autor', foreign_keys='Problema.creado_por')
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'nombre_completo': self.nombre_completo,
            'rol': self.rol,
            'creado_el': self.creado_el.isoformat() if self.creado_el else None,
        }
