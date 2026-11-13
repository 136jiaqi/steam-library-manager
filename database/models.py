from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass
class SteamAccount(Base):
    __tablename__ = "steam_accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_alias: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    steam_login_name: Mapped[str | None] = mapped_column(String(120))
    steam_id64: Mapped[str | None] = mapped_column(String(17), unique=True, index=True)
    friend_code: Mapped[str | None] = mapped_column(String(32))
    region: Mapped[str | None] = mapped_column(String(50))
    account_type: Mapped[str] = mapped_column(String(30), default="普通账号")
    engine_type: Mapped[str | None] = mapped_column(String(50))
    family_share_supported: Mapped[str] = mapped_column(String(12), default="未知")
    notes: Mapped[str | None] = mapped_column(Text)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime)
    sync_status: Mapped[str] = mapped_column(String(30), default="从未同步")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
class AdminUser(Base):
    __tablename__ = "admin_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(16), default="admin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class SteamGame(Base):
    __tablename__ = "steam_games"
    app_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_en: Mapped[str | None] = mapped_column(String(300))
class AccountGame(Base):
    __tablename__ = "account_games"; __table_args__ = (UniqueConstraint("account_id", "app_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("steam_accounts.id"))
    app_id: Mapped[int] = mapped_column(ForeignKey("steam_games.app_id"))
