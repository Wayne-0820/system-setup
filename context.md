# Context

> 本文件給 Claude Code 讀。它說明硬體、使用情境、個人偏好,讓後續所有決策有共同基礎。

---

## 硬體

- **GPU**:NVIDIA RTX 5090(24GB VRAM,筆電版)
- **CPU**:Intel Core Ultra 9 275HX(Arrow Lake-HX,24 核)
- **RAM**:64GB
- **儲存**:
  - **C 槽**:Gen4 NVMe 2TB(系統 + 軟體本體)
  - **D 槽**:Gen5 NVMe 2TB(工作區 + 快取 + 模型 + 素材)

## 磁碟策略

C 槽只放作業系統與軟體執行檔,極簡。D 槽結構:

```
D:\
├── Work\           # Git repos 與大型生成工具
│   ├── Ldbot\
│   ├── Forge\              # SD WebUI Forge(若裝)
│   ├── ComfyUI_portable\   # ComfyUI portable 解壓位置
│   └── creative-pipeline\  # CrewAI 編排專案
├── Models\         # 模型權重
│   ├── ollama\             # OLLAMA_MODELS 指到這
│   ├── lmstudio\           # LM Studio 模型(若裝)
│   └── sd\                 # SDXL / Flux / FramePack 共用
├── Cache\          # 軟體快取
│   └── Resolve\            # DaVinci 快取 / 資料庫 / Gallery
├── Emulator\       # LDPlayer
├── Media\          # 影片素材、AI 生成、DaVinci 輸出(詳見 `media-structure.md`)
│   ├── Projects\              # 當前進行中的剪輯專案
│   ├── Archive\               # 已結案封存
│   ├── Assets\                # 跨專案共用資源(Music / SFX / Fonts / LUTs / Logos)
│   └── AI_Raw\                # AI 生成原始池(ComfyUI / FramePack / Voice / Music)
├── Sync-Wayne\     # Synology Drive(你的)
├── Sync-Wife\      # Synology Drive(老婆的)
├── Games\          # 遊戲
│   ├── Steam\              # Steam Library(在 Steam 設定加入)
│   └── Standalone\         # 官網下載的獨立遊戲
├── Licenses\       # 軟體序號備份(DaVinci 等)
└── Recovery\       # 重灌 manifest + Hasleo 映像相關
```

## 使用情境優先序(高到低)

1. **AI 影像生產 pipeline**(新主軸):Claude Code + CrewAI 編排,DaVinci Studio 組裝,ComfyUI + FramePack 生成影片。詳見 `davinci-pipeline.md`
2. **Ldbot 收尾維護**:核心已完成,偶爾修 bug。詳見 `ldbot-checklist.md`
3. **DaVinci 一般剪輯**(非 AI 流程)
4. 一般生產力:Office、瀏覽器、通訊
5. 休閒娛樂:Steam 遊戲 / 獨立遊戲(裝 D 槽)

## 現役專案

### Ldbot(收尾階段)

- LDPlayer 模擬器手遊自動化
- 核心已完成,task-b 與 worktree 已在舊系統合併結案
- 影像比對**只依賴解析度**,其他設定全部可隨時重建
- 開發工具:Claude Code 單一入口
- **舊系統路徑**:`C:\Users\Wayne\Ldbot` → **新系統路徑**:`D:\Work\Ldbot`
- 4 個 gitignored 檔案(Firebase 密鑰、帳號、config、user settings)走 NAS 備份,詳見 `ldbot-checklist.md`

### AI 影像生產 pipeline(新主力)

- 目標:半自動產出劇本 → 分鏡圖 → 影片段 → 組裝成片
- 編排:Claude Code + CrewAI(Python)
- 組裝台:DaVinci Resolve Studio(Python 腳本控制,需 Python 3.10)
- 生成工具:**ComfyUI**(主力,含 FramePack 首尾幀)+ 雲端 API 選擇性補強

## 個人偏好

- **不污染全域 PATH**:只放核心工具(Git、Node、uv、Claude Code)
- **Per-project 環境**:Python 用 uv,每個專案獨立 `.venv`
- **多 Python 版本並存**:DaVinci 腳本要 3.10、Ldbot 用 3.12,uv 能管
- **符號連結保守使用**:優先用軟體原生路徑設定
- **本次重灌不保留任何舊設定檔**:clean slate
- **ComfyUI 乾淨重來策略**:portable 版 + Manager 管 custom node,隨時可砍重建
- **敏感資料**:不進 Git,走 `.env` + NAS 整包備份

## 資料保存策略

- **程式碼**:GitHub(主)+ NAS 整包備份(副)
- **Ldbot 的 gitignored 機敏檔案**(4 個):`D:\Ldbot-secrets\` → NAS
- **敏感資料(`.env` 等)**:NAS(NAS 本身有帳密保護)
- **大型素材、模型備份**:NAS
- **重灌 manifest**:GitHub(這個 repo)

## 何時搜尋最新資訊

Claude Code 執行時,以下情況**應該上網查**,不要憑記憶回答:

- 工具版本、下載連結、安裝指令(版本常變)
- 具體套件的最新 API、參數(pip/npm 包更新快)
- ComfyUI custom node 的 repo 位置(node 生態變動頻繁)
- 本地模型的最新推薦與 tag
