# Open WebUI + LiteLLM 安裝指南

> **定位**:本地 AI 介面。透過 LiteLLM 兼容層接 Anthropic Claude API,原生接本機 Ollama,做多模型並排對話。
>
> **為什麼要 LiteLLM**:Open WebUI 原生支援 Ollama,但接 Anthropic 要透過 OpenAI 兼容 API。LiteLLM 當代理層,把 Anthropic / OpenAI / Gemini 等不同廠商統一轉成 OpenAI 格式,Open WebUI 只要連一個 endpoint 就搞定。
>
> **這份文件怎麼用**:
> - 第一次安裝:從「完整安裝流程」開始,照做即可
> - 重灌後重建:跳到「重建流程」
> - 遇到奇怪錯誤:先看「踩坑紀錄」三個核心坑

---

## 架構總覽

```
┌──────────────────────────────────────────────────────────┐
│                       瀏覽器                              │
│              http://localhost:8080                       │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│              Open WebUI(port 8080)                      │
│              .venv Python 3.11                            │
│              D:\Work\OpenWebUI\                           │
└──────────────┬───────────────────────────┬───────────────┘
               │                           │
               ▼                           ▼
   ┌─────────────────────┐     ┌───────────────────────────┐
   │  Ollama(本地)      │     │  LiteLLM proxy(port 4000)│
   │  http://localhost:  │     │  .venv Python 3.11        │
   │  11434              │     │  D:\Work\LiteLLM\         │
   │  qwen3:32b 等本地   │     └───────────┬───────────────┘
   │  模型               │                 │
   └─────────────────────┘                 ▼
                          ┌──────────────────────────────┐
                          │  Anthropic API(雲端)        │
                          │  claude-sonnet-4-5 等        │
                          └──────────────────────────────┘
```

---

## 關鍵版本鎖定(⚠️ 不要亂升級)

| 套件 | 版本 | 為什麼 |
|---|---|---|
| Python | **3.11** | Open WebUI 官方建議 |
| Open WebUI | 最新穩定版 | - |
| **LiteLLM** | **1.55.10** | **不要用 1.83.12**,踩坑紀錄 #1 |
| uv | 最新版 | 用它管理 Python 版本 |

---

## 完整安裝流程

### Step 1:建立兩個獨立目錄 + venv

**重要**:Open WebUI 和 LiteLLM **必須分開 venv**,不能共用(踩坑紀錄 #2)。

```powershell
# Open WebUI
New-Item -ItemType Directory -Path "D:\Work\OpenWebUI\data" -Force
cd D:\Work\OpenWebUI
uv python install 3.11
uv init --python 3.11 --no-workspace
uv add open-webui

# LiteLLM
New-Item -ItemType Directory -Path "D:\Work\LiteLLM" -Force
cd D:\Work\LiteLLM
uv init --python 3.11 --no-workspace
uv add "litellm[proxy]==1.55.10"
```

### Step 2:建立 LiteLLM config

LiteLLM 需要一份 `config.yaml` 告訴它「哪個模型名對應哪個 API」。

**重要(寫檔)**:YAML 和 .env 檔**必須用無 BOM 的 UTF-8**(踩坑紀錄 #3)。

**重要(內容)**:**config 內容一律純 ASCII**,不寫中文註解或中文字串值(踩坑紀錄 #4)。中文說明寫進本 MD 文件,不寫進 config 本體。

**範例 vs 實機**:下面的範例是**推薦配置**(Claude 三大模型 sonnet / opus / haiku 都列),實機 config 可能跟範例不同步:

- 是否實裝 opus、是否加新模型(deepseek 等)看實機 model_list 為準
- `model:` 用 alias(如 `anthropic/claude-sonnet-4-5`)跨版本自動跟最新版,適合長期維護;改成 explicit version(如 `anthropic/claude-sonnet-4-5-20250929`)鎖死特定快照也可,看需求
- 主規劃窗口接班時應對齊實機 config,而非把範例當實機真相

```powershell
cd D:\Work\LiteLLM

$configContent = @"
model_list:
  - model_name: claude-sonnet-4-5
    litellm_params:
      model: anthropic/claude-sonnet-4-5
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-opus-4-7
    litellm_params:
      model: anthropic/claude-opus-4-7
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-haiku-4-5
    litellm_params:
      model: anthropic/claude-haiku-4-5
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  drop_params: true
  set_verbose: false

general_settings:
  master_key: sk-litellm-local-$(Get-Random)
"@

# 關鍵:無 BOM UTF-8 寫檔
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\config.yaml", $configContent, $utf8NoBom)

# 額外驗證:整檔 ASCII 掃描(踩坑 #4)
$bytes = [System.IO.File]::ReadAllBytes("$PWD\config.yaml")
"Non-ASCII byte count: $(($bytes | Where-Object { $_ -gt 127 }).Count)  (期望:0)"
```

擴充更多 model(NIM 等)→ 見後段「**擴充:接入 NVIDIA NIM**」。

### Step 3:建立 LiteLLM 的 .env

```powershell
cd D:\Work\LiteLLM

$envContent = @"
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
"@

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\.env", $envContent, $utf8NoBom)

# .gitignore
@"
.venv/
__pycache__/
*.pyc
.env
"@ | Out-File -FilePath .gitignore -Encoding ascii
```

### Step 4:建立 Open WebUI 的 .env

```powershell
cd D:\Work\OpenWebUI

$envContent = @"
# Ollama(本地,直連)
OLLAMA_BASE_URL=http://localhost:11434

# LiteLLM proxy(OpenAI 兼容格式,轉 Anthropic)
OPENAI_API_BASE_URL=http://localhost:4000/v1
OPENAI_API_KEY=sk-litellm-local-xxxxx

# 資料目錄
DATA_DIR=D:\Work\OpenWebUI\data

# 關閉帳號註冊(第一個使用者註冊後建議關)
# ENABLE_SIGNUP=false
"@

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\.env", $envContent, $utf8NoBom)

# .gitignore
@"
.venv/
__pycache__/
*.pyc
.env
data/
"@ | Out-File -FilePath .gitignore -Encoding ascii
```

**注意**:`OPENAI_API_KEY` 要跟 LiteLLM 的 `master_key` 一致(Step 2 產生的那串)。

### Step 5:啟動 LiteLLM proxy(先)

開一個 PowerShell 視窗:

```powershell
cd D:\Work\LiteLLM
uv run litellm --config config.yaml --port 4000
```

看到類似訊息代表啟動成功:
```
LiteLLM: Proxy initialized with Config, Set models:
#01 claude-sonnet-4-5
#02 claude-opus-4-7
...
INFO:     Uvicorn running on http://0.0.0.0:4000
```

**驗證**(另開 PowerShell):

```powershell
curl http://localhost:4000/v1/models
```

應該回傳所有 Claude 模型的 JSON 清單。

### Step 6:啟動 Open WebUI(另開視窗)

```powershell
cd D:\Work\OpenWebUI
uv run open-webui serve
```

看到類似訊息:
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

### Step 7:瀏覽器開 http://localhost:8080

- 註冊第一個使用者(**自動成為 admin**)
- Settings → Connections:
  - Ollama:自動偵測 `http://localhost:11434`,應看到 qwen3:32b
  - OpenAI Compatible:應自動抓到 LiteLLM 提供的 Claude 模型
- 新對話 → 左上選擇模型 → 驗證 Claude 和 Ollama 都能用
- 並排模式:對話內點「+」增加一個模型同時對話

---

## 日常啟動流程(裝好之後)

兩個 PowerShell 視窗:

**視窗 1 — LiteLLM**:
```powershell
cd D:\Work\LiteLLM
uv run litellm --config config.yaml --port 4000
```

**視窗 2 — Open WebUI**:
```powershell
cd D:\Work\OpenWebUI
uv run open-webui serve
```

瀏覽器開 http://localhost:8080

---

## 擴充:接入 NVIDIA NIM(deepseek-v4 系列)

DeepSeek V4 系列(1.6T 參數,~865 GB)本地跑不了(`../ai-models/local-models.md` 已駁回段),透過 NVIDIA NIM API 雲端呼叫。LiteLLM 1.55.10 原生支援 `nvidia_nim` provider,加進 model_list 即可。

### 前置條件

- NVIDIA Build 帳號 + nvapi- key(從 https://build.nvidia.com 取得)
- key 寫入 `D:\Work\LiteLLM\.env`,行格式:`NVIDIA_API_KEY=nvapi-...`(只一個 `nvapi-` 前綴,Notepad 編輯後跑 BOM 三 byte 驗證)
- LiteLLM 1.55.10 `nvidia_nim` provider 預檢:

  ```powershell
  cd D:\Work\LiteLLM
  uv run python -c "import litellm; print([p for p in litellm.provider_list if 'nvidia' in p.lower()])"
  ```

  list 含 `nvidia_nim` → 走原生 provider(下面 model_list 寫法);沒有 → fallback 走 OpenAI 兼容 + 自訂 `api_base: https://integrate.api.nvidia.com/v1`

### model_list 加兩條

在現有 model_list 末尾 append。**注意 LiteLLM nvidia_nim provider 預設讀 `NVIDIA_NIM_API_KEY` 環境變數**,但 .env 用 `NVIDIA_API_KEY`,所以要顯式 `api_key: os.environ/NVIDIA_API_KEY` 做改名映射:

```yaml
  - model_name: deepseek-v4-pro
    litellm_params:
      model: nvidia_nim/deepseek-ai/deepseek-v4-pro
      api_key: os.environ/NVIDIA_API_KEY

  - model_name: deepseek-v4-flash
    # NIM upstream may pause occasionally for high-traffic models.
    # Status: https://build.nvidia.com/deepseek-ai/deepseek-v4-flash
    litellm_params:
      model: nvidia_nim/deepseek-ai/deepseek-v4-flash
      api_key: os.environ/NVIDIA_API_KEY
```

config 編輯紀律不變:.NET API 寫檔 + BOM 三 byte 驗證 + ASCII 掃描(踩坑 #3 / #4)。

### 啟動驗證(三層)

重啟 proxy 後三層都過才算對接成功:

1. **proxy model 列表**:`curl http://localhost:4000/v1/models` JSON 看到新 model
2. **啟動 log 載入計數**:LiteLLM startup log 顯示 model 數量符合 model_list 條目數
3. **真打 NIM(這層不能跳)**:對 proxy `/v1/chat/completions` 帶新 model name,回應 content 真的拿到內容(不是只 LiteLLM 端 200)

NIM 端 timeout / 靜默 hang → 先去 https://build.nvidia.com/<model_id> 看是不是 service banner「We'll Be Right Back」(高流量服務性下線);不是再懷疑技術原因。

### v4-flash reasoning_effort 待驗

`deepseek-ai/deepseek-v4-flash` NIM docs 顯示預設 `reasoning_effort=high` + `max_tokens=16384`,可能即使簡短問句也先生成大量 reasoning trace 才給 final answer。對話框打 `/v1/chat/completions` 若反覆 timeout,試帶 `reasoning_effort: "none"`(LiteLLM 是否 forward 此 param 至 nvidia_nim provider 待驗)。

---

## ⚠️ 踩坑紀錄(這幾個坑一定要記住)

### 坑 #1:LiteLLM 1.83.12 + uv + Windows → CLI 讀不到 `--config`

**症狀**:
用 `litellm --config config.yaml` 啟動時,LiteLLM 不會讀你指定的 config,改成讀它自己的預設(會報找不到 model 或 API key)。

**原因**:
LiteLLM 1.83.12 的 CLI parsing 在 Windows + uv 環境下有 bug,`--config` 旗標被當成其他東西。這是特定版本 + 特定平台的組合問題。

**解法**:
鎖定到 **1.55.10**:

```powershell
cd D:\Work\LiteLLM
uv remove litellm
uv add "litellm[proxy]==1.55.10"
```

**未來處理**:
每半年檢查一次 LiteLLM 更新,**實測過 `--config` 能正常讀取**再升版。不要盲目升。

### 坑 #2:Open WebUI 和 LiteLLM 不能共用 venv(uvicorn 版本衝突)

**症狀**:
如果圖方便把 Open WebUI + LiteLLM 裝同一個 venv,會遇到:
```
ERROR: Cannot install open-webui and litellm[proxy] because these package versions have conflicting dependencies
Requires uvicorn==0.41.0 ...
```

**原因**:
- Open WebUI 鎖定 `uvicorn` 某個版本
- LiteLLM 1.55.10 鎖定另一個版本(特別是 `uvicorn==0.41.0` 或附近)
- 兩個都用 FastAPI + uvicorn,版本相互不相容

**解法**:
**分開兩個完全獨立的資料夾**,各自 `uv init` 建自己的 venv:
- `D:\Work\OpenWebUI\.venv\` ← uv 自動建立
- `D:\Work\LiteLLM\.venv\` ← uv 自動建立

啟動時兩個 PowerShell 視窗各自 `uv run`,各走各的環境,互不干擾。

**為什麼不用全域安裝一勞永逸**:違反系統架構「per-project venv」原則,而且會讓 uv 和 pip 混用出怪問題。

### 坑 #3:PowerShell `Out-File -Encoding utf8` 有 BOM → YAML 和 .env 解析失敗

**症狀**:
config.yaml 或 .env 用 `Out-File -Encoding utf8` 寫出來,LiteLLM 啟動時:
- YAML 可能讀不到第一個 key
- .env 可能讀不到 `ANTHROPIC_API_KEY`(變成 `\ufeffANTHROPIC_API_KEY`)
- 錯誤訊息模糊,很難 debug

**原因**:
PowerShell 5.x 的 `Out-File -Encoding utf8` 預設寫入 **UTF-8 with BOM**(開頭三個 byte `EF BB BF`)。YAML / dotenv 解析器不認 BOM,把它當成 key 的一部分。

**解法**:
用 .NET 的 `UTF8Encoding` 建構子明確指定**無 BOM**:

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\config.yaml", $content, $utf8NoBom)
```

**驗證無 BOM**:
```powershell
$bytes = [System.IO.File]::ReadAllBytes("config.yaml")[0..2]
$bytes -join ","
# 無 BOM: 輸出 "35,10,109"(ASCII 的 "#\nm" 之類,看 config 第一行)
# 有 BOM: 輸出 "239,187,191"
```

**替代方案**(如果不想記 .NET 語法):
- 用 **Notepad++** 存檔時選「UTF-8 without BOM」
- 或用 VS Code 右下角切換「UTF-8 with BOM」→「UTF-8」

**PowerShell 7 的差異**:
PS 7 的 `Out-File -Encoding utf8` 已改為預設無 BOM,如果全用 PS 7 可以直接用。但混用 PS 5 / PS 7 時,**用 `[System.IO.File]::WriteAllText` 最保險**,不管哪版都對。

### 坑 #4:LiteLLM 1.55.10 在 Windows 繁中系統讀含中文註解的 config → `UnicodeDecodeError`

**症狀**:
`litellm_config.yaml` 加任何中文註解(即使無 BOM、UTF-8 編碼正確),啟動 proxy 立即 crash:

```
UnicodeDecodeError: 'cp950' codec can't decode byte 0x9a in position 513:
illegal multibyte sequence
```

**原因**:
LiteLLM 1.55.10 `proxy_server.py` 用 `yaml.safe_load(open(config))` 開檔,**沒帶 `encoding='utf-8'`**。Python `open()` 預設 `locale.getpreferredencoding()` = Windows 繁中系統的 `cp950`。檔案是無 BOM UTF-8(寫對了),但讀檔端用 cp950 解碼 UTF-8 多 byte 中文序列 → 炸。

**這跟坑 #3 的差別**:坑 #3 是**寫檔**端的 BOM 問題(自家 PowerShell 行為),這條是**讀檔**端的 encoding 問題(第三方工具 LiteLLM 行為)。**寫檔再正確也救不了讀檔端的盲點**。

**解法**:
config 內**所有註解、字串值一律純 ASCII**(英文)。中文說明寫進本 MD 文件,不寫進 config 本體。

寫完 config 跑整檔 ASCII 掃描:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("$PWD\litellm_config.yaml")
($bytes | Where-Object { $_ -gt 127 }).Count    # 期望 0
```

非 0 → 有非 ASCII byte 沒清,啟動會炸,先抓出來看是哪行。

**升版 LiteLLM 可能解嗎**:可能。新版若 LiteLLM 上游補上 `open(config, encoding='utf-8')` 就解。但 1.55.10 鎖版理由(坑 #1)不變,等未來 LiteLLM 整體升版時再驗。

**適用範圍延伸**:
這條不只 LiteLLM。Windows 繁中系統下任何 Python 1.x 第三方工具讀 config 都可能踩(Open WebUI、CrewAI 等)。**Sysadmin 教訓 5 已記**(`../SYSADMIN_BRIEFING.md`),config 類檔保持 ASCII 是最穩的下限。

---

## 重建流程(未來重灌後)

照順序跑:

```powershell
# 1. 確認 Python 3.11 + uv 可用
uv python install 3.11

# 2. clone 或手動建立兩個資料夾(如果有 Git 備份的話)
# 或重新照「完整安裝流程」建立

# 3. API keys 從 NAS / 密碼管理器複製回來
#    - ANTHROPIC_API_KEY
#    - LiteLLM master_key(重新產生也行)

# 4. 啟動兩個服務驗證
```

---

## API keys 管理

**`.env` 絕對不進 Git**。管理方式選一個:

### 選項 A:NAS 加密資料夾

```
NAS:\secrets\
├── openwebui.env
└── litellm.env
```

重灌後從 NAS 拖回來。

### 選項 B:密碼管理器(Bitwarden / 1Password)

把 `.env` 檔內容貼到 Secure Note。重灌後複製貼上。

### 選項 C:兩者並用(最穩)

這份規劃偏好 A + 備查用 B。

---

## 成本控制提醒

Open WebUI 的介面讓你很容易**不小心跑很多 token**:

- 並排對話 = 同一訊息送多個模型 = token 成本 ×N
- 上傳文件 = 全文進 context,開銷比直接聊天大
- 長對話 = 每次都帶完整歷史

**建議習慣**:
- 日常瑣事用 Ollama(本地免費)
- 需要高品質才用 Claude API
- 定期看 LiteLLM 的 `/spend/logs` endpoint 查開銷

Anthropic console 也可以設**月開銷上限**,避免失控。

---

## 跟系統架構的關係

這份安裝符合 `context.md` 的規劃:

- ✅ 程式本體在 `D:\Work\`(符合 Work 目錄慣例)
- ✅ Per-project venv(不污染全域)
- ✅ API keys 走 `.env` + NAS 備份(不進 Git)
- ✅ Python 用 uv 管理(跟其他專案一致)
- ✅ 端口配置:8080(Open WebUI)、4000(LiteLLM)、11434(Ollama)、8188(ComfyUI)—— 互不衝突

---

## 待決事項

- [ ] 是否 push 到 private GitHub(包含 pyproject.toml + uv.lock,不含 .env 和 data)
- [ ] 是否設為開機自動啟動(建議不設,手動控制更乾淨)
- [ ] LiteLLM 成本追蹤 dashboard 要不要開(它有內建 UI)

---

**最後更新**:2026-04-20
