"""Phase-one entry point for Steam Library Manager."""
import streamlit as st

st.set_page_config(page_title="Steam Library Manager", page_icon="🎮", layout="wide")
st.title("Steam Library Manager")
st.caption("阶段一：Steam Web API 可行性验证")
st.info(
    "项目基础结构已建立。请先在 .env 或 Streamlit Secrets 配置 "
    "STEAM_WEB_API_KEY 和一个 SteamID64，然后运行 scripts/test_steam_api.py。"
)
st.markdown("后续阶段会在完成真实 API 验证后添加认证、账号管理和库存页面。")
