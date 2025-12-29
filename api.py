# FastAPI application with optimized endpoints
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
import mimetypes
from pathlib import Path

import orm.repo as repo
import orm.esquemas as esquemas
from orm.config import generador_sesion

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI PostgreSQL Application",
    description="RESTful API for user, purchase, and photo management",
    version="1.0.0"
)

# Configuration
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", os.path.expanduser("~") + "/fotos-ejemplo"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


# ============ Health Check ============

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"mensaje": "API funcionando correctamente", "status": "ok"}


# ============ User Endpoints ============

@app.get("/usuarios", response_model=list[esquemas.UsuarioResponse], tags=["Usuarios"])
def lista_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sesion: Session = Depends(generador_sesion)
):
    """Get all users with pagination"""
    return repo.devuelve_usuarios(sesion, skip=skip, limit=limit)


@app.get("/usuarios/{id}", response_model=esquemas.UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(id: int, sesion: Session = Depends(generador_sesion)):
    """Get user by ID"""
    usuario = repo.usuario_por_id(sesion, id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@app.post("/usuarios", response_model=esquemas.UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(usuario: esquemas.UsuarioCreate, sesion: Session = Depends(generador_sesion)):
    """Create a new user"""
    return repo.guardar_usuario(sesion, usuario)


@app.put("/usuarios/{id}", response_model=esquemas.UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(
    id: int,
    info_usuario: esquemas.UsuarioUpdate,
    sesion: Session = Depends(generador_sesion)
):
    """Update user information"""
    return repo.actualiza_usuario(sesion, id, info_usuario)


@app.delete("/usuarios/{id}", tags=["Usuarios"])
def borrar_usuario(id: int, sesion: Session = Depends(generador_sesion)):
    """Delete user and all associated data"""
    return repo.borra_usuario_por_id(sesion, id)


@app.get("/usuarios/{id}/fotos", response_model=list[esquemas.FotoResponse], tags=["Usuarios"])
def obtener_fotos_usuario(id: int, sesion: Session = Depends(generador_sesion)):
    """Get all photos for a user"""
    # Verify user exists
    usuario = repo.usuario_por_id(sesion, id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return repo.fotos_por_id_usuario(sesion, id)


@app.get("/usuarios/{id}/compras", response_model=list[esquemas.CompraResponse], tags=["Usuarios"])
def obtener_compras_usuario(id: int, sesion: Session = Depends(generador_sesion)):
    """Get all purchases for a user"""
    # Verify user exists
    usuario = repo.usuario_por_id(sesion, id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return repo.compras_por_id_usuario(sesion, id)


# ============ Purchase Endpoints ============

@app.get("/compras/{id}", response_model=esquemas.CompraResponse, tags=["Compras"])
def obtener_compra(id: int, sesion: Session = Depends(generador_sesion)):
    """Get purchase by ID"""
    compra = repo.compra_por_id(sesion, id)
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compra no encontrada"
        )
    return compra


@app.get("/compras", response_model=list[esquemas.CompraResponse], tags=["Compras"])
def lista_compras(
    id_usuario: Optional[int] = Query(None, description="Filter by user ID"),
    precio_min: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sesion: Session = Depends(generador_sesion)
):
    """Get purchases with optional filters"""
    if id_usuario and precio_min is not None:
        return repo.devuelve_compras_por_usuario_precio(sesion, id_usuario, precio_min)
    elif id_usuario:
        return repo.compras_por_id_usuario(sesion, id_usuario)
    else:
        return repo.devuelve_compras(sesion, skip=skip, limit=limit)


@app.post("/compras", response_model=esquemas.CompraResponse, status_code=status.HTTP_201_CREATED, tags=["Compras"])
def crear_compra(compra: esquemas.CompraCreate, sesion: Session = Depends(generador_sesion)):
    """Create a new purchase"""
    return repo.guardar_compra(sesion, compra)


# ============ Photo Endpoints ============

@app.get("/fotos/{id}", response_model=esquemas.FotoResponse, tags=["Fotos"])
def obtener_foto(id: int, sesion: Session = Depends(generador_sesion)):
    """Get photo by ID"""
    foto = repo.foto_por_id(sesion, id)
    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )
    return foto


@app.get("/fotos", response_model=list[esquemas.FotoResponse], tags=["Fotos"])
def lista_fotos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sesion: Session = Depends(generador_sesion)
):
    """Get all photos with pagination"""
    return repo.devuelve_fotos(sesion, skip=skip, limit=limit)


@app.post("/fotos", response_model=esquemas.FotoResponse, status_code=status.HTTP_201_CREATED, tags=["Fotos"])
async def guardar_foto(
    id_usuario: int = Form(..., description="User ID"),
    titulo: Optional[str] = Form(None, max_length=100),
    descripcion: str = Form(..., min_length=1, max_length=100),
    foto: UploadFile = File(...),
    sesion: Session = Depends(generador_sesion)
):
    """Upload and save a photo"""
    # Validate file extension
    file_ext = Path(foto.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    contenido = await foto.read()
    
    # Validate file size
    if len(contenido) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Archivo demasiado grande. Tamaño máximo: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Generate unique filename
    nombre_archivo = uuid.uuid4().hex
    ruta_imagen = UPLOAD_DIR / f"{nombre_archivo}{file_ext}"
    
    # Save file
    try:
        with open(ruta_imagen, "wb") as archivo:
            archivo.write(contenido)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo: {str(e)}"
        )
    
    # Save photo metadata to database
    foto_data = esquemas.FotoCreate(
        id_usuario=id_usuario,
        titulo=titulo,
        descripcion=descripcion
    )
    
    return repo.guardar_foto(sesion, foto_data, str(ruta_imagen))


# ============ Error Handlers ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
