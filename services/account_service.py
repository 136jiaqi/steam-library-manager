from __future__ import annotations
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import SteamAccount
from services.steam_api import validate_steam_id64

def list_accounts():
    with SessionLocal() as db: return list(db.scalars(select(SteamAccount).where(SteamAccount.is_deleted.is_(False)).order_by(SteamAccount.id)))
def save_account(data: dict, account_id: int | None = None):
    steam_id = (data.get("steam_id64") or "").strip() or None
    if steam_id: steam_id = validate_steam_id64(steam_id)
    with SessionLocal() as db:
        obj = db.get(SteamAccount, account_id) if account_id else SteamAccount(account_alias=data["account_alias"].strip())
        if not obj: raise ValueError("账号不存在")
        for key in ("account_alias","steam_login_name","friend_code","region","account_type","engine_type","family_share_supported","notes"):
            setattr(obj, key, (data.get(key) or None) if key not in ("account_type","family_share_supported") else data.get(key))
        obj.steam_id64 = steam_id
        db.add(obj); db.commit()
def soft_delete(account_id: int):
    with SessionLocal() as db:
        obj=db.get(SteamAccount, account_id)
        if obj: obj.is_deleted=True; db.commit()
