# Steam API 可行性验证（阶段一）

## 当前结论

代码已具备对 Steam `IPlayerService/GetOwnedGames` 的真实、只读验证能力。2026-11-13 已使用本地配置的一个账号完成验证：API 返回 `game_count=116`，且实际 `games` 条目为 116；响应含 AppID 与游戏名称。未在仓库、日志或本文档保存 API Key、SteamID64 或完整游戏清单。

## 运行

1. 复制 `.env.example` 为 `.env`，填写 `STEAM_WEB_API_KEY` 与 `STEAM_TEST_STEAM_ID64`。
2. 安装依赖：`python -m pip install -r requirements.txt`
3. 执行：`python scripts/test_steam_api.py`

脚本不会输出 API Key，也不会写入或删除任何库存数据。

## 官方接口与判读

Steam 官方文档列明 `GetOwnedGames` 需要 Web API Key、目标 `steamid`，并可请求 `include_appinfo`；它仅在目标玩家的拥有游戏/详情对调用方可见时返回游戏列表。该接口默认排除免费游戏，脚本显式请求 `include_played_free_games=true`，因此它仍不等同于完整的许可证或 DLC 清单。

- HTTP 401/403：密钥、隐私或访问权限不满足，状态应标为“无法通过 API 获取”。
- 网络/5xx：同步失败；绝不能清空既有记录。
- 正常 200 但 `games` 为空：只能标为“待核实/部分同步”，需人工检查隐私可见性，不能标为未购买。
- 成功响应含 `appid` 和通常的名称；名称缺失或本地化不完整时，后续通过官方商店元数据和人工别名补全。

## 替代与补充路径

| 方法 | 覆盖范围 | 限制 |
|---|---|---|
| Steam Web API | 可见的拥有游戏及部分 AppID/名称 | 受密钥和隐私限制；不应推断未返回项目未购买 |
| 账号所有者将资料/游戏详情设为可见后 API 同步 | 同上，适合可管理账号 | 需要账号所有者配合；仍需处理免费游戏、DLC、Demo、Playtest |
| 管理员上传从 Steam 客户端或可信来源导出的清单 | 导出实际覆盖到的条目 | Steam 客户端没有通用的完整官方库存导出格式；须记录来源与核验状态 |
| Excel/CSV 手工导入与补录 | 管理员明确提供的 AppID/游戏 | 覆盖取决于输入质量，应标记来源，不能覆盖 API/人工确认记录 |

## 下一步门槛

在至少一个满足隐私与 Key 条件的账号上运行成功后，保存不含敏感数据的验证结论（日期、返回数量、是否含名称、限制），再进入数据库与账号管理阶段。
