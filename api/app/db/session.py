from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Iterator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..core.config import get_settings


def _build_engine():
    settings = get_settings()
    if not settings.database_url:
        return None
    return create_engine(settings.database_url, pool_pre_ping=True)


ENGINE = _build_engine()
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False) if ENGINE else None


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL nao configurada")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_db_configured() -> bool:
    return SessionLocal is not None


@contextmanager
def session_scope_optional() -> Iterator[Optional[Session]]:
    if SessionLocal is None:
        yield None
        return

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
