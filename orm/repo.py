# Repository pattern implementation for database operations
import orm.modelos as modelos
import orm.esquemas as esquemas
import orm.utils as utils
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status


# ============ User Operations ============

def usuario_por_id(sesion: Session, id_usuario: int) -> Optional[modelos.Usuario]:
    """Get user by ID"""
    stmt = select(modelos.Usuario).where(modelos.Usuario.id == id_usuario)
    result = sesion.execute(stmt)
    return result.scalar_one_or_none()


def usuario_por_email(sesion: Session, email: str) -> Optional[modelos.Usuario]:
    """Get user by email"""
    stmt = select(modelos.Usuario).where(modelos.Usuario.email == email)
    result = sesion.execute(stmt)
    return result.scalar_one_or_none()


def devuelve_usuarios(sesion: Session, skip: int = 0, limit: int = 100) -> List[modelos.Usuario]:
    """Get all users with pagination"""
    stmt = select(modelos.Usuario).offset(skip).limit(limit)
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def guardar_usuario(sesion: Session, usr_nuevo: esquemas.UsuarioCreate) -> modelos.Usuario:
    """Create a new user with hashed password"""
    # Check if email already exists
    existing = usuario_por_email(sesion, usr_nuevo.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    usr_bd = modelos.Usuario(
        nombre=usr_nuevo.nombre,
        edad=usr_nuevo.edad,
        domicilio=usr_nuevo.domicilio,
        email=usr_nuevo.email,
        password=utils.hash_password(usr_nuevo.password)
    )
    
    try:
        sesion.add(usr_bd)
        sesion.commit()
        sesion.refresh(usr_bd)
        return usr_bd
    except IntegrityError:
        sesion.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


def actualiza_usuario(sesion: Session, id_usuario: int, usr_esquema: esquemas.UsuarioUpdate) -> modelos.Usuario:
    """Update user information"""
    usr_bd = usuario_por_id(sesion, id_usuario)
    if not usr_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update only provided fields
    update_data = usr_esquema.model_dump(exclude_unset=True)
    
    # Hash password if provided
    if "password" in update_data:
        update_data["password"] = utils.hash_password(update_data["password"])
    
    # Check email uniqueness if email is being updated
    if "email" in update_data and update_data["email"] != usr_bd.email:
        existing = usuario_por_email(sesion, update_data["email"])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    for field, value in update_data.items():
        setattr(usr_bd, field, value)
    
    try:
        sesion.commit()
        sesion.refresh(usr_bd)
        return usr_bd
    except IntegrityError:
        sesion.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


def borra_usuario_por_id(sesion: Session, id_usuario: int) -> dict:
    """Delete user and all associated data (cascade handled by database)"""
    usr = usuario_por_id(sesion, id_usuario)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    sesion.delete(usr)
    sesion.commit()
    return {"mensaje": "Usuario eliminado correctamente"}


# ============ Photo Operations ============

def fotos_por_id_usuario(sesion: Session, id_usuario: int) -> List[modelos.Foto]:
    """Get all photos for a user"""
    stmt = select(modelos.Foto).where(modelos.Foto.id_usuario == id_usuario)
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def foto_por_id(sesion: Session, id_foto: int) -> Optional[modelos.Foto]:
    """Get photo by ID"""
    stmt = select(modelos.Foto).where(modelos.Foto.id == id_foto)
    result = sesion.execute(stmt)
    return result.scalar_one_or_none()


def devuelve_fotos(sesion: Session, skip: int = 0, limit: int = 100) -> List[modelos.Foto]:
    """Get all photos with pagination"""
    stmt = select(modelos.Foto).offset(skip).limit(limit)
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def guardar_foto(sesion: Session, foto_data: esquemas.FotoCreate, ruta: str) -> modelos.Foto:
    """Save photo metadata to database"""
    # Verify user exists
    usuario = usuario_por_id(sesion, foto_data.id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    foto_bd = modelos.Foto(
        id_usuario=foto_data.id_usuario,
        titulo=foto_data.titulo,
        descripcion=foto_data.descripcion,
        ruta=ruta
    )
    
    sesion.add(foto_bd)
    sesion.commit()
    sesion.refresh(foto_bd)
    return foto_bd


# ============ Purchase Operations ============

def compras_por_id_usuario(sesion: Session, id_usuario: int) -> List[modelos.Compra]:
    """Get all purchases for a user"""
    stmt = select(modelos.Compra).where(modelos.Compra.id_usuario == id_usuario)
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def compra_por_id(sesion: Session, id_compra: int) -> Optional[modelos.Compra]:
    """Get purchase by ID"""
    stmt = select(modelos.Compra).where(modelos.Compra.id == id_compra)
    result = sesion.execute(stmt)
    return result.scalar_one_or_none()


def devuelve_compras(sesion: Session, skip: int = 0, limit: int = 100) -> List[modelos.Compra]:
    """Get all purchases with pagination"""
    stmt = select(modelos.Compra).offset(skip).limit(limit)
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def devuelve_compras_por_usuario_precio(sesion: Session, id_usr: int, precio_min: float) -> List[modelos.Compra]:
    """Get purchases by user and minimum price"""
    stmt = select(modelos.Compra).where(
        and_(
            modelos.Compra.id_usuario == id_usr,
            modelos.Compra.precio >= precio_min
        )
    )
    result = sesion.execute(stmt)
    return list(result.scalars().all())


def guardar_compra(sesion: Session, compra_data: esquemas.CompraCreate) -> modelos.Compra:
    """Save a new purchase"""
    # Verify user exists
    usuario = usuario_por_id(sesion, compra_data.id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    compra_bd = modelos.Compra(
        id_usuario=compra_data.id_usuario,
        producto=compra_data.producto,
        precio=compra_data.precio
    )
    
    sesion.add(compra_bd)
    sesion.commit()
    sesion.refresh(compra_bd)
    return compra_bd