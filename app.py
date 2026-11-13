import streamlit as st
from sqlalchemy import select
from auth.authentication import authenticate, create_initial_admin, initialize_database
from database.connection import SessionLocal
from database.models import AdminUser
from services.account_service import list_accounts, save_account

st.set_page_config(page_title="Steam Library Manager", page_icon="🎮", layout="wide")
initialize_database()
if "user" not in st.session_state:
    with SessionLocal() as db:
        has_user = bool(db.scalar(select(AdminUser.id).limit(1)))
    st.title("Steam Library Manager")
    if not has_user:
        st.info("首次使用：创建管理员账户。密码只保存安全哈希。")
        with st.form("setup"):
            user = st.text_input("管理员用户名")
            password = st.text_input("密码（至少 12 位）", type="password")
            if st.form_submit_button("创建管理员"):
                ok, message = create_initial_admin(user, password)
                (st.success if ok else st.error)(message)
    else:
        with st.form("login"):
            user = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            if st.form_submit_button("登录"):
                record = authenticate(user, password)
                if record:
                    st.session_state.user = {"name": record.username, "role": record.role}
                    st.rerun()
                st.error("用户名或密码错误。")
    st.stop()
st.sidebar.caption(f"已登录：{st.session_state.user['name']}")
if st.sidebar.button("退出登录"):
    del st.session_state.user; st.rerun()
page = st.sidebar.radio("导航", ["Steam 账号管理", "游戏搜索（即将推出）"])
st.title(page)
if page == "Steam 账号管理":
    with st.form("account", clear_on_submit=True):
        alias = st.text_input("账号别名 *")
        steam_id64 = st.text_input("SteamID64（可选，必须为 17 位）")
        region = st.text_input("地区")
        if st.form_submit_button("保存账号"):
            try:
                save_account({"account_alias": alias, "steam_id64": steam_id64, "region": region, "account_type": "普通账号", "family_share_supported": "未知"})
                st.success("账号已保存"); st.rerun()
            except Exception as exc: st.error(f"无法保存：{exc}")
    st.dataframe([{"别名": a.account_alias, "SteamID64": a.steam_id64 or "待补充", "地区": a.region or "-", "状态": a.sync_status} for a in list_accounts()], use_container_width=True, hide_index=True)
else:
    st.info("完成账号和库存同步后开放搜索。")
