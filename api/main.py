try:
    from .app.main import app  # type: ignore
except ImportError:
    # Supports `uvicorn main:app --reload` from within `api/`.
    from app.main import app
