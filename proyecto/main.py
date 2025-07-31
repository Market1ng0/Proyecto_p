"""Punto de entrada principal para la API de FastAPI."""

from fastapi import FastAPI, Depends
from app.core.database import Base, engine # Importa la base y el motor de la DB
from app.routers import auth, item # Importa tus routers
from app.dependencies import get_current_active_user # Importa la dependencia para proteger rutas

# Crea las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de CRUD Protegido con FastAPI y JWT",
    description=(
        "Una API de ejemplo con autenticación completa y un CRUD protegido por token de acceso, "
        "siguiendo la arquitectura MVC."
    ),
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    # Esta es la configuración estándar y correcta para que Swagger UI muestre el campo Bearer
    openapi_extra={
        "components": {
            "securitySchemes": {
                "BearerAuth": { # Este es el nombre que aparecerá en el botón "Authorize"
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": (
                        "Introduce tu token JWT con el prefijo 'Bearer ' "
                        "(ej: Bearer tu_token_aqui)"
                    )
                }
            }
        },
        # Aplicamos la seguridad globalmente a TODOS los endpoints por defecto.
        # Esto hará que el candado aparezca en todos los endpoints.
        "security": [{"BearerAuth": []}]
    }
)

# Incluye los routers en tu aplicación, asignándoles el prefijo /api/v1
app.include_router(auth.router, prefix="/api/v1")

# El router de ítems SÍ necesita que todas sus rutas estén protegidas por un token válido.
app.include_router(item.router, prefix="/api/v1", dependencies=[Depends(get_current_active_user)])

@app.get("/api/v1", tags=["Root"])
async def root():
    """Endpoint de bienvenida de la API."""
    return {"message": "¡Bienvenido a la API Protegida con FastAPI!"}

