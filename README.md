# Steam Library Manager

Steam 多账号游戏库存内部管理平台。当前仓库处于**阶段一：Steam Web API 可行性验证**，尚未实现账号与库存管理 UI。

## 本地启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## 进行真实 Steam API 验证

```powershell
Copy-Item .env.example .env
# 编辑 .env，只在本机填写真实 STEAM_WEB_API_KEY 与 STEAM_TEST_STEAM_ID64
python scripts/test_steam_api.py
```

详见 [阶段一可行性报告](docs/steam_api_feasibility.md)。密钥、账户信息、数据库和表格均被 `.gitignore` 排除。
