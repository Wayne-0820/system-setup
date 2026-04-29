# AI 影像生產 Pipeline

**目標**:Claude Code + CrewAI 編排,結合本地生成工具(ComfyUI + FramePack)與選用雲端 API,以 DaVinci Resolve Studio 當組裝台,半自動產出成片(故事短片、動畫、混合風格)。

---

## 架構全景

```
                    [ Claude Code ]         ← 開發與控制入口
                          │
                          ▼
             [ CrewAI 編排層 (Python) ]     ← 多 agent 任務分工
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   [ 劇本 agent ]    [ 生圖 agent ]   [ 生影片 agent ]
   Claude Sonnet     ComfyUI API      ComfyUI + FramePack
   (API)             (本地)           + Kling / Runway(選)
                          │
                          ▼
                  [ 素材整理 ]
                          │
                          ▼
            [ DaVinci Studio Python API ]
            自動建專案、匯入、上時間軸、輸出
                          │
                          ▼
                     成片輸出
```

---

## 首尾幀問題的答案

**DaVinci Resolve Studio 本身不能生成首尾幀影片**。它是剪輯 / 調色 / 合成台。

**ComfyUI + FramePack 可以,而且你 24GB VRAM 綽綽有餘**(FramePack 官方最低要求 6GB)。

路徑:

| 方式 | 方法 | 適合情境 |
|---|---|---|
| **ComfyUI + Kijai FramePack 節點** | 社群有現成首尾幀 workflow | 長期用、可客製化 |
| **雲端 API(Kling、Runway)** | 付費,品質高 | 不想本地跑時 |

**實測參考**:24GB VRAM 跑 FramePack FP16 版,5 秒影片大約 2-5 分鐘。

---

## 各階段工具選擇

### 1. 劇本 / 分鏡 / 敘事結構

**Claude API(Sonnet 主力)**,透過 CrewAI 當「劇本 agent」,輸出 JSON 結構(scene list、duration、dialogue、visual prompts)。

### 2. 靜態圖(角色、場景、keyframe)

**ComfyUI 主力**(已在 `decisions.md` 決定)。模型放 `D:\Models\diffusion\`:

```
D:\Models\diffusion\
├── checkpoints\     # SDXL、Flux、Pony 等底模
├── loras\
├── vae\
├── controlnet\
├── embeddings\
├── clip_vision\
└── diffusion_models\   # FramePack 的 model 放這
```

### 3. 影片生成

**本地主力**:ComfyUI + FramePack(Kijai 節點)。首尾幀、分鐘級影片。

**雲端補強**(候選,不需要全上):

| 服務 | 強項 |
|---|---|
| **Kling AI** | 首尾幀強、寫實風格 |
| **Runway Gen-3/4** | 生態成熟 |
| **Luma Dream Machine** | keyframe 控制友善 |
| **Google Veo** | 新、品質高 |

建議先只上一個付費(Kling 或 Runway),用一陣子再決定要不要加。

### 4. 語音(對白、旁白)

- **ElevenLabs API**:中英文都強、聲音 clone 佳、零設定
- **本地替代**:F5-TTS、XTTS v2(ComfyUI 有節點)

### 5. 配樂

- **Suno AI**:最簡單,prompt 產歌
- **Udio**:替代
- **免版稅庫**:Epidemic Sound、Artlist

### 6. 字幕 / 轉錄

- **faster-whisper**(本地,吃 GPU 輕)
- 可接進 DaVinci 當字幕軌

### 7. 組裝 / 輸出

**DaVinci Resolve Studio + Python API**

關鍵限制:

- 必須用 **Python 3.10**(DaVinci scripting 綁這版)
- DaVinci 要**運行中**腳本才能連
- 環境變數:`RESOLVE_SCRIPT_API`、`RESOLVE_SCRIPT_LIB`、`PYTHONPATH`
- Windows Script 目錄:`%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\`

能做:建專案、匯入媒體、時間軸操作、調色預設、批次輸出、Fusion 合成。

限制:動態文字要預先做 template、某些參數唯讀、細微調色曲線需 GUI。

---

## CrewAI 專案結構建議

```
D:\Work\creative-pipeline\
├── pyproject.toml
├── .env.example       # API keys 範本(進 Git)
├── .env               # 真實 keys(NOT 進 Git)
├── agents\
│   ├── writer.py      # 劇本 agent → Claude API
│   ├── art_director.py
│   ├── image_gen.py   # 呼叫 ComfyUI API
│   ├── video_gen.py   # 呼叫 FramePack / Kling
│   ├── voice.py
│   └── editor.py      # DaVinci Python API
├── tasks\
├── crew.py            # 編排邏輯
└── outputs\
    └── [project_name]\
```

---

## 漸進建立順序(重灌後)

**第 1 天**:裝 Claude Code、DaVinci、ComfyUI portable、Ollama。不寫任何程式。手動跑一次 ComfyUI 最基本 t2i(7 節點),確認環境 OK。

**第 2-3 天**:在 ComfyUI 載入 FramePack workflow,手動跑通首尾幀。Claude Code 在旁邊解釋節點連接。

**第 4-5 天**:寫 DaVinci Python 腳本 hello world(建專案、匯入 clip、輸出)。確認 scripting API 通。

**第 2 週**:建 `creative-pipeline` 專案,`uv add crewai`,寫第一個劇本 agent + 單一 task,純文字輸出。

**第 3-4 週**:接上 ComfyUI API,讓分鏡圖能自動生成。

**第 2 個月**:整合影片生成 agent,完整跑通「劇本 → 圖 → 影片段 → DaVinci 組裝」。

**之後**:加雲端 API、語音、配樂。

---

## 待決事項

等開始實作時再拍板:

- [ ] 雲端影片 API 先試哪家(Kling / Runway / Luma 選一)
- [ ] 語音本地(省錢)vs ElevenLabs(省事)
- [ ] DaVinci 腳本寫到多細
