"""Minimal, defensive Steam Web API client used by the feasibility check."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"


class SteamApiError(RuntimeError):
    """A safe, user-facing error returned by Steam or the network."""


@dataclass(frozen=True)
class OwnedGamesResult:
    steam_id64: str
    game_count: int
    games: list[dict[str, Any]]
    raw_response_keys: list[str]


def validate_steam_id64(value: str) -> str:
    candidate = str(value or "").strip()
    if not (candidate.isdigit() and len(candidate) == 17 and candidate.startswith("765")):
        raise ValueError("SteamID64 必须是以 765 开头的 17 位数字；好友代码不能直接代替 SteamID64。")
    return candidate


class SteamWebApiClient:
    def __init__(self, api_key: str, timeout_seconds: float = 20.0) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("未配置 STEAM_WEB_API_KEY。")
        self._api_key = api_key.strip()
        self._timeout = timeout_seconds

    def get_owned_games(self, steam_id64: str) -> OwnedGamesResult:
        steam_id64 = validate_steam_id64(steam_id64)
        params = {
            "key": self._api_key,
            "steamid": steam_id64,
            "include_appinfo": "true",
            "include_played_free_games": "true",
            "format": "json",
        }
        try:
            response = requests.get(OWNED_GAMES_URL, params=params, timeout=self._timeout)
        except requests.RequestException as exc:
            raise SteamApiError(f"无法连接 Steam Web API：{exc.__class__.__name__}") from exc

        if response.status_code in (401, 403):
            raise SteamApiError("Steam 拒绝访问：请检查 API Key、目标资料隐私设置及该 Key 的访问权限。")
        if response.status_code != 200:
            raise SteamApiError(f"Steam Web API 返回 HTTP {response.status_code}。")
        try:
            payload = response.json()
        except ValueError as exc:
            raise SteamApiError("Steam 返回的内容不是有效 JSON。") from exc
        if not isinstance(payload, dict):
            raise SteamApiError("Steam 返回了无法识别的数据结构。")

        body = payload.get("response")
        if not isinstance(body, dict):
            raise SteamApiError("Steam 没有返回 response 对象；可能是 API Key 或访问权限问题。")
        games = body.get("games", [])
        if not isinstance(games, list):
            raise SteamApiError("Steam 返回的 games 字段格式异常。")
        count = body.get("game_count")
        if not isinstance(count, int):
            count = len(games)
        return OwnedGamesResult(steam_id64, count, games, sorted(payload.keys()))
