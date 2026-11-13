"""Run a real, non-destructive feasibility check for GetOwnedGames.

Usage (PowerShell):
  Copy-Item .env.example .env
  # set the two values in .env, then:
  python scripts/test_steam_api.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.steam_api import SteamApiError, SteamWebApiClient, validate_steam_id64  # noqa: E402


def main() -> int:
    # Windows legacy console encodings cannot print some Steam game titles (for
    # example trademark symbols).  UTF-8 keeps a successful API probe from
    # being reported as a false failure.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("STEAM_WEB_API_KEY", "")
    steam_id64 = os.getenv("STEAM_TEST_STEAM_ID64", "")
    if not api_key:
        print("未执行网络请求：缺少 STEAM_WEB_API_KEY。请通过 .env 或环境变量配置，切勿提交密钥。")
        return 2
    try:
        steam_id64 = validate_steam_id64(steam_id64)
    except ValueError as exc:
        print(f"未执行网络请求：{exc}")
        return 2

    try:
        result = SteamWebApiClient(api_key).get_owned_games(steam_id64)
    except (ValueError, SteamApiError) as exc:
        print(f"可行性验证失败：{exc}")
        print("注意：空结果、无权限和 API 故障都不能被解释为‘未购买’。")
        return 1

    print("可行性验证成功：Steam 已返回可读取的库存响应。")
    print("SteamID64：已配置（为保护账号信息，不在输出中显示）")
    print(f"API game_count：{result.game_count}")
    print(f"实际 games 条目：{len(result.games)}")
    print("前 10 个游戏（仅显示 AppID 与名称）：")
    for game in result.games[:10]:
        print(f"- appid={game.get('appid')}  name={game.get('name', '<API 未返回名称>')}")
    if result.game_count == 0:
        print("警告：API 返回空库存。请人工检查资料/游戏详情可见性；不能将其当作没有游戏。")
    if any(not game.get("name") for game in result.games):
        print("警告：至少一个条目没有名称；后续阶段需用元数据服务补全。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
