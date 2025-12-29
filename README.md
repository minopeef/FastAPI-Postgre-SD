# FastAPI PostgreSQL Application

A RESTful API application built with FastAPI and PostgreSQL, implementing a user management system with purchases and photo uploads.

## Project Overview

This application provides a complete backend API for managing users, their purchases, and photos. It uses SQLAlchemy ORM for database operations and follows a repository pattern for data access.

## Features

- User management (CRUD operations)
- Purchase tracking per user
- Photo upload and management
- RESTful API endpoints
- PostgreSQL database integration
- SQLAlchemy ORM with declarative models

## Project Structure

```
FastAPI-Postgre-SD/
├── api.py                 # Main FastAPI application and route definitions
├── orm/
│   ├── config.py         # Database configuration and session management
│   ├── modelos.py        # SQLAlchemy database models
│   ├── esquemas.py       # Pydantic schemas for request/response validation
│   └── repo.py           # Repository pattern implementation for database operations
├── sql/
│   └── basedatos.sql     # Database schema and initial data
├── pyproject.toml        # Poetry dependency management configuration
└── poetry.lock           # Locked dependency versions
```

## Database Models

### Usuario (User)
- id: Primary key
- nombre: User name
- edad: Age
- domicilio: Address
- email: Email address (unique)
- password: Password
- fecha_registro: Registration timestamp

### Compra (Purchase)
- id: Primary key
- id_usuario: Foreign key to Usuario
- producto: Product name
- precio: Price

### Foto (Photo)
- id: Primary key
- id_usuario: Foreign key to Usuario
- titulo: Photo title
- descripcion: Photo description
- ruta: File path

## API Endpoints

### User Endpoints

GET / - Health check endpoint
- Returns a simple greeting message

GET /usuarios - List all users
- Returns all users in the database

GET /usuarios/{id} - Get user by ID
- Returns user information for the specified ID

POST /usuarios - Create new user
- Request body: UsuarioBase schema (nombre, edad, domicilio, email, password)
- Returns the created user

PUT /usuario/{id} - Update user
- Request body: UsuarioBase schema
- Returns updated user information

DELETE /usuario/{id} - Delete user
- Deletes user and all associated purchases and photos
- Returns confirmation message

GET /usuarios/{id}/compras - Get user purchases
- Returns all purchases for the specified user

GET /usuarios/{id}/fotos - Get user photos
- Returns all photos for the specified user

### Purchase Endpoints

GET /compras/{id} - Get purchase by ID
- Returns purchase information

GET /compras?id_usuario={id}&precio={p} - Get purchases by user and minimum price
- Query parameters: id_usuario (required), precio (required)
- Returns purchases matching the criteria

### Photo Endpoints

GET /fotos - List all photos
- Returns all photos in the database

GET /fotos/{id} - Get photo by ID
- Returns photo information

POST /fotos - Upload photo
- Form data: titulo (optional), descripcion (required), foto (file, required)
- Saves photo to user's home directory under fotos-ejemplo folder
- Returns photo metadata

## Technology Stack

- Python 3.11.5
- FastAPI 0.115.4
- SQLAlchemy 2.0.23
- PostgreSQL (via psycopg2-binary)
- Uvicorn 0.32.0
- Poetry (dependency management)

## Installation

### Prerequisites

- Python 3.11.5 or higher
- Poetry package manager
- PostgreSQL database (optional, defaults to SQLite if not configured)

### Setup Steps

1. Install Poetry if not already installed

2. Install project dependencies:
   ```
   poetry install
   ```

3. Configure database connection:
   - Set the `db_uri` environment variable for PostgreSQL connection
   - Format: `postgresql://usuario:password@host:port/database`
   - If not set, the application defaults to SQLite (bd_ejemplo.db)

4. Initialize database (if using PostgreSQL):
   - Run the SQL script in `sql/basedatos.sql` to create tables and insert sample data
   - The application will automatically create tables if using SQLite

5. Run the application:
   ```
   poetry run uvicorn api:app --reload
   ```

   Or activate the virtual environment first:
   ```
   poetry shell
   uvicorn api:app --reload
   ```

## Configuration

### Database Configuration

The database connection is configured in `orm/config.py`. The application supports:

- PostgreSQL: Set `db_uri` environment variable
- SQLite: Default fallback if `db_uri` is not set

### Photo Storage

Uploaded photos are stored in the user's home directory under `fotos-ejemplo/`. Each photo is saved with a unique UUID-based filename to prevent conflicts.

## Development

### Code Organization

- **api.py**: Contains all FastAPI route handlers and endpoint definitions
- **orm/modelos.py**: SQLAlchemy model classes representing database tables
- **orm/esquemas.py**: Pydantic models for request/response validation
- **orm/repo.py**: Repository functions for database queries and operations
- **orm/config.py**: Database engine configuration and session management

### Database Session Management

The application uses dependency injection to manage database sessions. Each endpoint receives a session through FastAPI's `Depends` mechanism, ensuring proper session lifecycle management.

## Notes

- The application includes sample data in the SQL script for testing
- User deletion cascades to associated purchases and photos
- Photo uploads require multipart/form-data encoding
- All timestamps are stored with timezone information

