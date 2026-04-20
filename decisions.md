# Decisions

所有已拍板的決策。Claude Code 照這份執行,不用重新問。

---

## Python 管理:uv

- 最快、最乾淨、無全域污染
- 能管多個 Python 版本(DaVinci 腳本要 3.10、其他專案可用 3.12)
- 工作流:`uv init` → `uv add <pkg>` → `uv run python script.py`
- 特殊場景:`uv python install 3.10` → `uv init --python 3.10`

## Node.js:LTS 主版

- 用途:Claude Code、前端工具、npm 生態
- `winget install OpenJS.NodeJS.LTS`

## Agent 工具鏈

- **Claude Code**(主力,CLI):日常開發唯一入口
- **CrewAI**(per-project):AI 影像生產 pipeline 的編排層,在該專案 `uv add crewai "crewai[tools]"`,**不裝全域**
- **IDE**:VS Code(Claude Code 是 CLI 驅動,IDE 穩定就好)

## 本地模型框架:Ollama 為主

- `winget install Ollama.Ollama`
- 設環境變數 `OLLAMA_MODELS` = `D:\Models\ollama`
- LM Studio 作為選用,要認真挑模型時再裝
- 詳見 `local-models.md`

## ComfyUI:Portable 版

- 下 `ComfyUI_windows_portable_nvidia.7z` 解壓到 `D:\Work\ComfyUI_portable`
- **不裝系統版**,隨時可砍可重建
- 第一個也是唯一手動裝的 custom node:**ComfyUI Manager**
- 詳見 `comfyui-setup.md`

## Shell

- PowerShell 7 + Windows Terminal
- WSL2:暫不裝,真需要 Linux 工具鏈時再說

## 環境變數策略

### 全域 PATH(精簡)

Git / Node / uv / Claude Code / NVIDIA 驅動(自動)

### PowerShell `$PROFILE` 自定義 function

- `work`:`cd D:\Work`,按需載入 ffmpeg 等零散工具
- `ldbot`:切 Ldbot 專案、顯示 LDPlayer 實例狀態
- `models`:列出 `D:\Models\` 現有模型

### 關鍵環境變數(裝完對應軟體後設定)

```powershell
# Ollama
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'D:\Models\ollama', 'User')

# DaVinci Scripting(裝 DaVinci 後設,具體路徑照實際安裝位置)
[Environment]::SetEnvironmentVariable('RESOLVE_SCRIPT_API', 'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting', 'User')
[Environment]::SetEnvironmentVariable('RESOLVE_SCRIPT_LIB', 'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll', 'User')
```

---

## Winget 批次安裝

裝完 NVIDIA Studio Driver、手動裝 Git + Node 之後,執行以下批次。

### 核心開發工具

```
Git.Git
OpenJS.NodeJS.LTS
astral-sh.uv
Microsoft.VisualStudioCode
Microsoft.WindowsTerminal
Microsoft.PowerShell
Microsoft.PowerToys
GitHub.cli
jqlang.jq
```

### 日常應用

```
7zip.7zip
Notepad++.Notepad++
VideoLAN.VLC
Adobe.Acrobat.Reader.64-bit
Discord.Discord
Line.Line
TeamViewer.TeamViewer
Valve.Steam
```

### 本地模型

```
Ollama.Ollama
```

> LM Studio 選用,需要時再 `winget install LMStudio.LMStudio`

### 批次安裝後

```powershell
npm i -g @anthropic-ai/claude-code
```

---

## 手動安裝(NAS / 官網)

**安裝順序很重要**,由上至下:

| 順序 | 軟體 | 裝哪 | 備註 |
|---|---|---|---|
| 1 | NVIDIA Studio Driver | C | **最優先**,裝任何東西之前 |
| 2 | Armoury Crate(ASUS 工具) | C | NVIDIA 之後、開發工具之前。裝完關掉不必要的背景服務(GameFirst、Aura 若無 RGB 周邊),關自動更新 |
| 3 | Google Chrome | C | winget 批次之前就要有瀏覽器(撈 NAS 檔案、看文件) |
| 4 | Office 2021 企業增強版 | C | NAS 來源。裝完用 ODT 砍 Teams / Outlook / Publisher / Access / OneDrive / Groove / Lync(見 `logs/odt-*.log`)。Teams 等 app 有雙版本(Office bundled + Windows 11 預裝 MSIX Store),ODT 只砍 Office 那版,Store 版要另外 `winget uninstall` |
| 5 | DaVinci Resolve Studio | C | 裝完進 Preferences 改 Database / Cache / Gallery → `D:\Cache\Resolve`;設 `RESOLVE_SCRIPT_API` / `RESOLVE_SCRIPT_LIB` 環境變數 |
| 6 | LDPlayer | `D:\Emulator\LDPlayer` | 重建實例時**解析度一定要跟 Ldbot config 對齊**,其他隨意 |
| 7 | Synology Drive Client | C | 同步目標 → `D:\Sync` |
| 8 | ComfyUI portable | `D:\Work\ComfyUI_portable` | 從 GitHub release 下 7z,`extra_model_paths.yaml` 指到 `D:\Models\sd` |
| - | Stable Diffusion WebUI Forge(選用) | `D:\Work\Forge` | 若裝,模型目錄也指到 `D:\Models\sd` |

## 資料夾結構

見 `context.md` 的 D 槽結構。
