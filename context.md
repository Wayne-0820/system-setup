# Context — 系統脈絡與規劃

> 給 Claude / Claude Code 的單一真相來源。第一次對話時讀這份。
> 最後更新:2026-04-26

---

## 硬體

- 筆電 ASUS ROG
- CPU:Intel Core Ultra 9 275HX(Arrow Lake-HX, 24 cores)
- GPU:NVIDIA RTX 5090 Laptop **24GB VRAM**(Blackwell sm_120)
- RAM:64GB DDR5
- C 槽:系統 Gen4 2TB
- D 槽:工作 Gen5 2TB
- OS:Windows 11 Pro

**24GB VRAM 是所有 AI 決策的天花板**。同時跑大模型(qwen3:32b + Klein 9B Base 等)會爆。

---

## 磁碟策略

C 槽只放作業系統與軟體執行檔,極簡。D 槽結構:

```
D:\
├── Work\           # Git repos 與大型生成工具
│   ├── Ldbot\
│   ├── ComfyUI_portable\         # ComfyUI portable 解壓位置
│   │   └── ComfyUI_windows_portable\  # 巢狀不拍平,跟官方範例對齊
│   ├── OpenWebUI\                # Python 3.11
│   ├── LiteLLM\                  # Python 3.11(獨立 venv,跟 OpenWebUI 分開)
│   ├── system-setup\             # 規劃文件 repo(本文件就在這)
│   │   ├── comfyui-workflows\    # ComfyUI workflow JSON(中文「用途定位派」命名)
│   │   ├── sageattention_build_notes\  # SageAttention 編譯完整紀錄
│   │   ├── *.patched             # PyTorch patches 備份
│   │   └── *.md                  # 各份規劃文件
│   └── creative-pipeline\        # CrewAI 編排專案(規劃中)
│
├── Models\         # 模型權重
│   ├── ollama\               # OLLAMA_MODELS 指到這
│   └── sd\                   # SDXL / FLUX / Klein 系列共用(extra_model_paths.yaml 指向)
│       ├── checkpoints\
│       ├── diffusion_models\
│       ├── clip\
│       ├── vae\
│       ├── loras\
│       ├── controlnet\
│       ├── upscale_models\
│       ├── embeddings\
│       └── clip_vision\
│
├── Cache\          # 軟體快取
│   └── Resolve\              # DaVinci 快取 / 資料庫 / Gallery
│
├── Emulator\       # LDPlayer
│
├── Media\          # 影片素材、AI 生成、DaVinci 輸出(詳見 `media-structure.md`)
│   ├── Projects\             # 當前進行中的剪輯專案
│   ├── Archive\              # 已結案封存
│   ├── Assets\               # 跨專案共用資源(Music / SFX / Fonts / LUTs / Logos)
│   └── AI_Raw\               # AI 生成原始池(ComfyUI / FramePack / Voice / Music)
│
├── tmp\            # 編譯暫存
│   └── SageAttention\        # source 保留(233 MB,以後重編用)
│
├── Sync-Wayne\     # Synology Drive(你的)
├── Sync-Wife\      # Synology Drive(老婆的)
├── Games\          # 遊戲
│   ├── Steam\                # Steam Library(在 Steam 設定加入)
│   └── Standalone\           # 官網下載的獨立遊戲
├── Licenses\       # 軟體序號備份(DaVinci 等)
└── Recovery\       # 重灌 manifest + Hasleo 映像相關
```

### 重要例外:LLM 類模型寫死路徑

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\
└── LLavacheckpoints\         # JoyCaption / Llama(節點 hardcode 路徑,不能搬)
```

LLM 節點(如 JoyCaption)在程式碼裡寫死路徑,**不吃 `extra_model_paths.yaml`**。維持在 ComfyUI 內部。

---

## 使用情境優先序(高到低)

1. **AI 影像生產 pipeline**(主軸):Claude Code + CrewAI 編排,DaVinci Studio 組裝,ComfyUI(Klein / FLUX) + FramePack 生成影片。詳見 `davinci-pipeline.md`、`comfyui-setup.md`
2. **Ldbot 收尾維護**:核心已完成,偶爾修 bug。詳見 `ldbot-checklist.md`
3. **DaVinci 一般剪輯**(非 AI 流程)
4. 一般生產力:Office、瀏覽器、通訊
5. 休閒娛樂:Steam 遊戲 / 獨立遊戲(裝 D 槽)

---

## 工具偏好(不可違反)

### Python
- **uv** per-project venv(不用 conda / pyenv / 全域 pip)
- DaVinci scripting 綁 Python 3.10
- Open WebUI / LiteLLM 用 3.11
- Ldbot 用 3.12
- ComfyUI portable 用 3.13.12 embedded(不要動)

### 環境變數
- **絕對路徑寫死**,不要用 `%VAR%`(PowerShell User scope 不展開)
- 已設好的:`OLLAMA_MODELS`、`RESOLVE_SCRIPT_API`、`RESOLVE_SCRIPT_LIB`、`PYTHONPATH`

### Secret 管理
- API keys 走 `.env` + `.gitignore`
- HF Token 不貼進 AI 對話框,只放 PowerShell 環境變數
- 持久化:NAS 加密備份

### 端口配置
- **8080**:Open WebUI
- **4000**:LiteLLM proxy
- **11434**:Ollama
- **8188**:ComfyUI

新服務不要搶這幾個埠。

---

## 已完成的階段

### 系統建置(2026-04-19/20 重灌)
- Windows 11 Pro + 全驅動 + Armoury Crate
- 開發工具:Git / Node / uv / Claude Code / VS Code / PowerToys 等
- DaVinci Resolve Studio 20(Working Folders 全 D 槽,Default Preset 已存)
- LDPlayer 9
- Synology Drive(Wayne + Wife 雙任務)
- Office 2021 精簡(砍 Outlook / Publisher / Access / Teams / OneDrive / Groove / Lync)
- Ollama + qwen3:32b
- ComfyUI portable + Manager
- Open WebUI + LiteLLM(三個踩坑文件化)

### ComfyUI 工程(2026-04-25/26)
- CUDA Toolkit 13.2 + Visual Studio 2022 Build Tools 安裝
- SageAttention 3 Blackwell 編譯成功(9 次嘗試,6 個 patches)
- Klein 系列模型完整下載(4B / 9B distilled / 9B Base + 對應 Qwen3 CLIP)
- JoyCaption Beta1 下載(15.81 GB)
- 5 個 workflow 中文命名建立完成
- 4K 升頻流程驗證(Klein 9B Base + UltraSharp = 20.9 GB VRAM 極限)

---

## 待推進階段

### 短期
1. Hasleo Rescue USB + 第一次 System Backup(golden image)
2. ComfyUI 啟動圖示底圖生成 + 桌面捷徑
3. 開始重建中國 workflow(Flux-fill / Qwen3 TTS / Kontext + ControlNet 三選一)

### 中期
1. SageAttention issue #357 修復後重編,享受完整 FP4 加速
2. 下載 FLUX.1 Fill / Kontext / Qwen-Image-Edit / Qwen3 TTS / Whisper / Wan 2.2 系列(約 100-150 GB)
3. 建 `D:\Work\creative-pipeline\` 跑 CrewAI

### 長期
1. CrewAI agent 編排:Writer(Sonnet API)→ Art Director → ComfyUI / FramePack / Voice → DaVinci 組裝
2. 完整 AI 影像 pipeline 跑通

---

## 文件導航

詳見 `README.md`。每份文件用途、何時讀:

- 通用先讀:`context.md`(本文件) + `decisions.md`
- 新對話 onboarding:`START_HERE.md`(精簡版,給執行窗口讀)
- 任務結束時:用 `PROGRESS_TEMPLATE.md` 格式產進度報告

---

**最後更新**:2026-04-26
