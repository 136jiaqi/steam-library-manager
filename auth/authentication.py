from __future__ import annotations
import bcrypt
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import AdminUser, Base
from database.connection import engine

def initialize_database() -> None: Base.metadata.create_all(engine)
def create_initial_admin(username: str, password: str) -> tuple[bool, str]:
    with SessionLocal() as db:
        if db.scalar(select(AdminUser).limit(1)): return False, "管理员已存在"
        if len(password) < 12: return False, "密码至少需要 12 个字符"
        db.add(AdminUser(username=username.strip(), password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), role="admin")); db.commit()
    return True, "管理员已创建"
def authenticate(username: str, password: str):
    with SessionLocal() as db:
        user = db.scalar(select(AdminUser).where(AdminUser.username == username.strip(), AdminUser.is_active.is_(True)))
        return user if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()) else None
