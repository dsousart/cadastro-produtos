from fastapi import FastAPI

from .api.routes.generation_jobs import router as generation_jobs_router
from .api.routes.health import router as health_router
from .api.routes.products import router as products_router
from .core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Cadastro de Produtos Premium API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(products_router)
    app.include_router(generation_jobs_router)
    return app


app = create_app()
