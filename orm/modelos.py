# SQLAlchemy models for database tables
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import datetime

# Base class for all models (SQLAlchemy 2.0 style)
BaseClass = declarative_base()


class Usuario(BaseClass):
    """User model with relationships to purchases and photos"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    domicilio = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # Increased for hashed passwords
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    compras = relationship("Compra", back_populates="usuario", cascade="all, delete-orphan")
    fotos = relationship("Foto", back_populates="usuario", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_usuario_email', 'email'),
    )


class Compra(BaseClass):
    """Purchase model linked to users"""
    __tablename__ = "compras"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    producto = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    
    # Relationship
    usuario = relationship("Usuario", back_populates="compras")
    
    __table_args__ = (
        Index('idx_compra_usuario', 'id_usuario'),
    )


class Foto(BaseClass):
    """Photo model linked to users"""
    __tablename__ = "fotos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(100))
    descripcion = Column(String(100), nullable=False)
    ruta = Column(String(255), nullable=False)  # Increased length for full paths
    
    # Relationship
    usuario = relationship("Usuario", back_populates="fotos")
    
    __table_args__ = (
        Index('idx_foto_usuario', 'id_usuario'),
    )