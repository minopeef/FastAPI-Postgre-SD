from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Request schemas
class UsuarioBase(BaseModel):
    """Base user schema for creation and updates"""
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., gt=0, le=150)
    domicilio: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UsuarioCreate(UsuarioBase):
    """Schema for creating a new user"""
    pass


class UsuarioUpdate(BaseModel):
    """Schema for updating a user (all fields optional)"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    edad: Optional[int] = Field(None, gt=0, le=150)
    domicilio: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)


# Response schemas
class UsuarioResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    nombre: str
    edad: int
    domicilio: str
    email: str
    fecha_registro: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CompraBase(BaseModel):
    """Base purchase schema"""
    producto: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0)


class CompraCreate(CompraBase):
    """Schema for creating a purchase"""
    id_usuario: int


class CompraResponse(CompraBase):
    """Schema for purchase response"""
    id: int
    id_usuario: int
    
    model_config = ConfigDict(from_attributes=True)


class FotoBase(BaseModel):
    """Base photo schema"""
    titulo: Optional[str] = Field(None, max_length=100)
    descripcion: str = Field(..., min_length=1, max_length=100)


class FotoCreate(FotoBase):
    """Schema for creating a photo"""
    id_usuario: int


class FotoResponse(FotoBase):
    """Schema for photo response"""
    id: int
    id_usuario: int
    ruta: str
    
    model_config = ConfigDict(from_attributes=True)