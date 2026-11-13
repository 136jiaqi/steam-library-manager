from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
def _database_url() -> str:
    """Prefer Streamlit Cloud Secrets, then local environment/.env."""
    try:
        import streamlit as st
        value = st.secrets.get("DATABASE_URL")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv("DATABASE_URL", "sqlite:///steam_library_manager.db")

DATABASE_URL = _database_url()
# The project uses psycopg v3. Accept Supabase's copied postgresql:// URL too.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL.removeprefix("postgresql://")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
