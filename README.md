# FastAPI PostgreSQL Application

A RESTful API application built with FastAPI and PostgreSQL, implementing a user management system with purchases and photo uploads.

## Project Overview

This application provides a complete backend API for managing users, their purchases, and photos. It uses SQLAlchemy ORM for database operations and follows a repository pattern for data access.

## Features

- User management (CRUD operations) with password hashing
- Purchase tracking per user
- Photo upload and management with file validation
- RESTful API endpoints with proper error handling
- PostgreSQL database integration with connection pooling
- SQLAlchemy 2.0 ORM with relationships and indexes
- Input validation and data sanitization
- Pagination support for list endpoints
- Comprehensive error handling with HTTP status codes

## Project Structure

```
FastAPI-Postgre-SD/
├── api.py                 # Main FastAPI application and route definitions
├── orm/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Database configuration and session management
│   ├── modelos.py        # SQLAlchemy database models with relationships
│   ├── esquemas.py       # Pydantic schemas for request/response validation
│   ├── repo.py           # Repository pattern implementation for database operations
│   └── utils.py          # Utility functions (password hashing)
├── sql/
│   └── basedatos.sql     # Database schema and initial data
├── pyproject.toml        # Poetry dependency management configuration
└── poetry.lock           # Locked dependency versions
```

## Database Models

### Usuario (User)
- id: Primary key (indexed)
- nombre: User name (required)
- edad: Age (required, validated)
- domicilio: Address (required)
- email: Email address (unique, indexed, validated)
- password: Hashed password using bcrypt (required)
- fecha_registro: Registration timestamp (auto-generated)
- Relationships: compras (purchases), fotos (photos)

### Compra (Purchase)
- id: Primary key (indexed)
- id_usuario: Foreign key to Usuario (indexed, cascade delete)
- producto: Product name (required)
- precio: Price (required, validated)
- Relationship: usuario (user)

### Foto (Photo)
- id: Primary key (indexed)
- id_usuario: Foreign key to Usuario (indexed, cascade delete)
- titulo: Photo title (optional)
- descripcion: Photo description (required)
- ruta: File path (required, full path stored)
- Relationship: usuario (user)

## API Endpoints

### User Endpoints

GET / - Health check endpoint
- Returns a simple greeting message

GET /usuarios - List all users
- Query parameters: skip (default: 0), limit (default: 100, max: 1000)
- Returns paginated list of users

GET /usuarios/{id} - Get user by ID
- Returns user information for the specified ID

POST /usuarios - Create new user
- Request body: UsuarioCreate schema (nombre, edad, domicilio, email, password)
- Password is automatically hashed using bcrypt
- Email must be unique and valid format
- Returns the created user (without password)

PUT /usuarios/{id} - Update user
- Request body: UsuarioUpdate schema (all fields optional)
- Only provided fields will be updated
- Password is automatically hashed if provided
- Returns updated user information

DELETE /usuarios/{id} - Delete user
- Deletes user and all associated purchases and photos (cascade delete)
- Returns confirmation message

GET /usuarios/{id}/compras - Get user purchases
- Returns all purchases for the specified user

GET /usuarios/{id}/fotos - Get user photos
- Returns all photos for the specified user

### Purchase Endpoints

GET /compras/{id} - Get purchase by ID
- Returns purchase information

GET /compras - Get purchases with filters
- Query parameters:
  - id_usuario (optional): Filter by user ID
  - precio_min (optional): Minimum price filter
  - skip (default: 0): Pagination offset
  - limit (default: 100, max: 1000): Results per page
- Returns purchases matching the criteria

POST /compras - Create new purchase
- Request body: CompraCreate schema (id_usuario, producto, precio)
- Returns the created purchase

### Photo Endpoints

GET /fotos - List all photos
- Query parameters: skip (default: 0), limit (default: 100, max: 1000)
- Returns paginated list of photos

GET /fotos/{id} - Get photo by ID
- Returns photo information

POST /fotos - Upload photo
- Form data: id_usuario (required), titulo (optional), descripcion (required), foto (file, required)
- File validation: Only JPG, JPEG, PNG, GIF, WEBP allowed
- File size limit: 10MB maximum
- Saves photo to configured upload directory (default: ~/fotos-ejemplo/)
- Generates unique filename using UUID
- Saves photo metadata to database
- Returns photo information with file path

## Technology Stack

- Python 3.11.5
- FastAPI 0.115.4
- SQLAlchemy 2.0.23 (using modern select() syntax)
- PostgreSQL (via psycopg2-binary) or SQLite
- Uvicorn 0.32.0
- Poetry (dependency management)
- Passlib with bcrypt (password hashing)
- Email-validator (email format validation)

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

## Optimizations Implemented

### Security
- Password hashing using bcrypt (passlib)
- Input validation with Pydantic schemas
- Email format validation
- File upload validation (type and size)
- SQL injection protection via SQLAlchemy ORM
- Proper error handling without exposing sensitive information

### Performance
- Database indexes on foreign keys and frequently queried fields
- Connection pooling for PostgreSQL
- Pagination support for all list endpoints
- SQLAlchemy 2.0 modern syntax (select() instead of query())
- Efficient relationship loading with back_populates

### Code Quality
- Consistent route naming (/usuarios instead of /usuario)
- Proper HTTP status codes (201, 404, 400, etc.)
- Comprehensive error handling with HTTPException
- Response models for all endpoints
- Type hints throughout the codebase
- Removed duplicate function names
- Cleaned up unused code and imports
- Database relationships properly defined
- Transaction rollback on errors

### Database
- Cascade delete configured at database level
- Proper foreign key constraints
- Indexes for performance optimization
- Relationships defined for efficient joins
- Server-side timestamp generation

## Notes

- The application includes sample data in the SQL script for testing
- User deletion cascades to associated purchases and photos (handled by database)
- Photo uploads require multipart/form-data encoding
- All timestamps are stored with timezone information
- Passwords are never returned in API responses
- File uploads are validated for type and size before processing

