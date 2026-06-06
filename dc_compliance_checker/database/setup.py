"""
database/setup.py
=================
Database initialization and a couple of small CRUD helpers.

For the proof-of-concept we try the configured PostgreSQL `DATABASE_URL` first;
if the connection fails (no Postgres on the dev machine) we transparently fall
back to an in-memory SQLite database so the whole pipeline still runs end-to-end.
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from database.models import Base, RuleORM
from engine.rules import Rule


def _make_engine() -> Engine:
    """
    Create the SQLAlchemy engine.

    Tries the Postgres URL from the environment; on any connection error it
    falls back to an in-memory SQLite engine (useful for demos/CI).
    """
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://dc_user:dc_password@localhost:5432/dc_compliance",
    )
    try:
        engine = create_engine(url, future=True)
        # Force a real connection so we can detect failure now, not later.
        with engine.connect():
            pass
        print(f"[db] Connected to PostgreSQL: {url.split('@')[-1]}")
        return engine
    except (OperationalError, SQLAlchemyError, Exception) as exc:  # noqa: BLE001
        print(f"[db] Postgres unavailable ({exc.__class__.__name__}); "
              f"falling back to in-memory SQLite.")
        return create_engine("sqlite:///:memory:", future=True)


def init_db() -> sessionmaker:
    """
    Initialise the database, create tables and return a session factory.
    """
    engine = _make_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)


def save_rules(session_factory: sessionmaker, rules: list[Rule]) -> int:
    """Persist a list of Pydantic Rules. Returns the number stored."""
    with session_factory() as session:  # type: Session
        session.add_all(RuleORM.from_pydantic(r) for r in rules)
        session.commit()
    return len(rules)


def load_rules(session_factory: sessionmaker) -> list[Rule]:
    """Load all rules back out as Pydantic Rule objects."""
    with session_factory() as session:  # type: Session
        rows = session.query(RuleORM).all()
        return [row.to_pydantic() for row in rows]
