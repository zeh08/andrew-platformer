# Andrew Platformer

一个用 Python + Pygame 编写的迷你平台跳跃游戏（类超级玛丽）。已包含音效、简单 UI、关卡切换与存档。

## 功能
- 平台跳跃：行走、跳跃、基础碰撞
- UI：主菜单、顶部 HUD（关卡名/坐标）、通关界面
- 声音：跳跃、过关、死亡、点击（使用合成音，无需额外素材）
- 关卡：到达终点 G 自动切换到下一关
- 存档：自动保存当前关卡至 `save.json`（已被 `.gitignore` 忽略）

## 操作
- 左/右：A/D 或 ←/→
- 跳跃：W / ↑ / 空格
- 退出到菜单：Esc（会自动保存）

## 快速开始
### 方式一：VS Code 一键运行（推荐）
- 在 VS Code 按 `Ctrl + Shift + B` 运行默认任务“Run Game”
- 任务会自动创建虚拟环境、安装依赖并启动游戏

### 方式二：PowerShell 手动运行
> Windows PowerShell（无需激活 venv，直接使用 venv 的 Python）

```powershell
# 可选：若还没有虚拟环境
py -m venv .venv

# 安装依赖
.\.venv\Scripts\python -m pip install -r requirements.txt

# 运行
.\.venv\Scripts\python src\main.py
```

如果你希望使用脚本激活虚拟环境但遇到策略阻止，可在“当前用户”范围设置：
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 关卡编辑
- 地块：`X`
- 玩家出生点：`P`
- 终点：`G`
- 关卡文件位于 `levels/`。新增关卡后，把文件路径加入 `src/main.py` 的 `LEVEL_FILES` 列表即可。

## 项目结构
```
.
├─ levels/
│  ├─ level1.txt
│  └─ level2.txt
├─ src/
│  ├─ main.py        # 入口、菜单/通关 UI、音效、关卡切换与存档
│  ├─ level.py       # 地图加载、绘制、相机、HUD、胜负判定
│  ├─ player.py      # 玩家移动/跳跃、缓冲与土狼时间、碰撞
│  ├─ tiles.py       # Tile 与 Goal（G）
│  └─ settings.py    # 分辨率、物理、颜色配置
├─ requirements.txt  # 依赖（pygame, numpy）
├─ .vscode/tasks.json# 一键运行任务
├─ .gitignore
└─ README.md
```

## 故障排除
- 无法激活 venv：使用上面的“方式二”绕过执行策略；或设置 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- 无声卡或初始化失败：`pygame.mixer.init()` 报错时，确保设备可用；或暂时将音量改低/禁用 mixer
- 黑屏/无渲染：请确认窗口未被最小化，且 `pygame.display.flip()` 正常执行
- 跳跃手感：可在 `src/settings.py` 调整 `JUMP_SPEED`、`GRAVITY`

## 开发
- 运行任务：在 VS Code 使用 `Ctrl + Shift + B` 触发“Run Game”
- 代码风格：保持简单直观，必要时再抽象

## 许可
本项目已添加 LICENSE 文件，详情请查阅仓库中的 `LICENSE` 文件。
