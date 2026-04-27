# Decisions

所有已拍板的決策。Claude Code 照這份執行,不用重新問。

---

## Python 管理:uv(專案)+ 系統級 Python 3.14(daily driver)

### uv:專案層級首選

- 最快、最乾淨、無全域污染
- 能管多個 Python 版本(DaVinci 腳本要 3.10、Ldbot 鎖 3.12、其他專案可用更新版本)
- 工作流:`uv init` → `uv add <pkg>` → `uv run python script.py`
- 特殊場景:`uv python install 3.10` → `uv init --python 3.10`

### 系統級 Python 3.14:daily driver

雖然 uv 能管 Python,**仍要裝一份系統級 Python 3.14 到 PATH**。理由:

1. **`python` 直接打就動**:跑 `tools/` 下的小腳本、`python -m http.server`、`pip install` 測個套件之類臨時用途,不用先進 venv
2. **IDE 整合直觀**:VSCode / Cursor 預設找系統 Python,不用每個專案都手動指定 uv interpreter
3. **不衝突**:系統 Python、uv 管的 Python(在 `~/.local/share/uv/python/`)、ComfyUI portable 的 `python_embeded` 各管各的,不互相污染

**版本選擇**:**3.14 系列最新穩定版**(2026-04 採用 3.14.4)。挑 3.14 的理由:

- 3.14 是當前 active bugfix 版本(stable + 還在維護)
- 3.13 也在維護,但既然要升就一次到位
- **不挑 3.15 alpha**:experimental,生態相容性差,PyInstaller 等工具未支援
- **不挑 3.12**:已進 security-fixes-only,系統級裝舊版意義不大

**Ldbot 不跟著升**:Ldbot 由 uv 鎖在 3.12.13(`pyproject.toml` 的 `requires-python`),走 `uv run python ...` 跑。系統 3.14 跟 uv 3.12 完全並存,互不干涉。

**安裝來源**:**python.org 官方安裝包**,**不要用** Microsoft Store(stub 攔截坑詳見 `reinstall-manifest.md` → Windows 基礎段)。

**安裝順序與勾選**(順序不可逆):
1. **先**關 MS Store 別名(Win+I → 應用程式 → 進階應用程式設定 → 應用程式執行別名 → `python.exe` / `python3.exe` 兩個 toggle 關)
2. **再**裝 python.org 安裝包
3. 安裝畫面:
   - ☑ Add python.exe to PATH(**必勾**)
   - ☑ Use admin privileges when installing py.exe(裝 `py` launcher,日後切版本用)
4. Advanced Options:
   - ☐ Install Python 3.14 for all users(**不勾**,單一 user 機器走 user-scope 即可)
   - ☐ Download free-threaded binaries(**絕對不勾**,experimental,生態相容性差)
   - ✅ Add Python to environment variables、Associate files with Python、Create shortcuts(預設勾即可)
5. 安裝完成畫面點 **Disable path length limit**(解除 260 字元 MAX_PATH 限制)

**驗證**:新開 PowerShell → `python --version` + `where.exe python`,**第一行**必須是 `C:\Users\<user>\AppData\Local\Programs\Python\Python314\python.exe`,**不是** WindowsApps。

### 三套 Python 的角色分工

| 來源 | 路徑 | 角色 | 何時用 |
|---|---|---|---|
| 系統級(python.org) | `C:\Users\Wayne\AppData\Local\Programs\Python\Python314\` | daily driver | 直接打 `python`、IDE 預設、臨時 `python -m http.server` |
| uv 管理(各專案) | `~\.local\share\uv\python\` | 專案隔離 | Ldbot(鎖 3.12.13)、CrewAI 等需要鎖版本的專案,走 `uv run` |
| ComfyUI portable | `D:\Work\ComfyUI_portable\...\python_embeded\` | ComfyUI 內建 | 只給 ComfyUI 自己跟它的 custom nodes 用,**不要混用** |

**重要紀律**:**Ldbot 永遠走 `uv run python ...`,不打系統 `python`**。系統 3.14 不裝 Ldbot 主環境的依賴(memory、ADB 操控套件、easyocr 等),硬打會踩 ImportError;就算當下能跑(例如 admin_tool.py 只用 stdlib),版本不一致也會在未來踩坑。

---

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
- 詳見 `ai-models/local-models.md`

## ComfyUI:Portable 版

- 下 `ComfyUI_windows_portable_nvidia.7z` 解壓到 `D:\Work\ComfyUI_portable`
- **不裝系統版**,隨時可砍可重建
- 第一個也是唯一手動裝的 custom node:**ComfyUI Manager**
- 詳見 `comfyui/setup.md`

## Shell

- PowerShell 7 + Windows Terminal
- WSL2:暫不裝,真需要 Linux 工具鏈時再說

## 環境變數策略

### 全域 PATH(精簡)

Git / Node / uv / Claude Code / **Python 3.14** / NVIDIA 驅動(自動)

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
| 4 | **Python 3.14.x**(系統級) | C(user-scope) | **先關 MS Store python 別名再裝**(踩坑詳見 `reinstall-manifest.md` → Windows 基礎)。python.org 抓 3.14 系列最新穩定版,勾「Add python.exe to PATH」。預設裝到 `C:\Users\<user>\AppData\Local\Programs\Python\Python314\`(per-user)。**Ldbot 不跟著升,由 uv 鎖在 3.12**。驗證 `where.exe python` 第一行不是 WindowsApps |
| 5 | Office 2021 企業增強版 | C | NAS 來源。裝完用 ODT 砍 Teams / Outlook / Publisher / Access / OneDrive / Groove / Lync(見 `logs/odt-*.log`)。Teams 等 app 有雙版本(Office bundled + Windows 11 預裝 MSIX Store),ODT 只砍 Office 那版,Store 版要另外 `winget uninstall` |
| 6 | DaVinci Resolve Studio | C | 裝完進 Preferences 改 Database / Cache / Gallery → `D:\Cache\Resolve`;設 `RESOLVE_SCRIPT_API` / `RESOLVE_SCRIPT_LIB` 環境變數 |
| 7 | LDPlayer | `D:\Emulator\LDPlayer` | 重建實例時**解析度一定要跟 Ldbot config 對齊**,其他隨意 |
| 8 | Synology Drive Client | C | 同步目標 → `D:\Sync` |
| 9 | ComfyUI portable | `D:\Work\ComfyUI_portable` | 從 GitHub release 下 7z,`extra_model_paths.yaml` 指到 `D:\Models\sd` |
| - | Stable Diffusion WebUI Forge(選用) | `D:\Work\Forge` | 若裝,模型目錄也指到 `D:\Models\sd` |

## 資料夾結構

見 `context.md` 的 D 槽結構。

---

**最後更新**:2026-04-27
