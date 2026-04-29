# 本地模型分工指南

> 這份文件反映**實際運行**的模型分工(不是探索清單)。
>
> 最後同步:2026-04-29
>
> 三大本地推理工具:**Ollama**(LLM)、**ComfyUI**(影像生成)、**ComfyUI 內 LLM 節點**(JoyCaption 圖像理解)。

---

## 硬體限制(決策天花板)

- RTX 5090 Laptop **24GB VRAM**(Blackwell sm_120)
- 64GB DDR5 RAM
- 24GB VRAM 是所有本地模型的決策天花板

**重要**:同時跑大型 LLM(qwen3:32b)+ 大型 Diffusion(Klein 9B Base)會爆 VRAM。**二選一**。

---

## 角色分工總覽

| 工具 | 角色 | 模型範例 | VRAM 用量 |
|---|---|---|---|
| **Ollama** | 文字 LLM(對話、推理、Code) | qwen3:32b | ~20 GB |
| **ComfyUI(Diffusion)** | 圖像生成 | FLUX.2 Klein 4B/9B、SDXL、FLUX.1 | 6-21 GB |
| **ComfyUI(LLM 節點)** | 圖像理解、反推 prompt | JoyCaption Beta1 nf4 | ~5 GB |
| **雲端 API**(對比參考) | 高品質、長 context | Claude Sonnet/Opus 4.7 | 0 GB(雲端) |

---

## Ollama 部分

### 安裝路徑

- **程式本體**:C 槽預設(`C:\Users\Wayne\AppData\Local\Programs\Ollama\`)
- **模型權重**:`D:\Models\ollama\`(透過環境變數 `OLLAMA_MODELS` 指定)

### 已下載模型

| 模型 | 量化 | 大小 | 用途 | VRAM |
|---|---|---|---|---|
| `qwen3:32b` | Q4_K_M | ~20 GB | 日常文字推理、Code 生成、Agent backbone | ~20 GB |

### 為什麼選 32B 不選 14B(Wayne 的決定)

24GB VRAM 跑 32B 偏吃緊,但 Wayne 評估後選擇:
- 偏好**單次品質**而非 agent 長對話
- 接受 5-10 tok/s 的速度(夠用)
- 24GB 仍能塞入(雖然餘裕只剩 ~3.5 GB)
- 同時跑 ComfyUI 大模型時,**這時候才切到雲端 Sonnet**

如果未來發現 agent 工作流 / 高頻需求多,可以**補下 14B**,兩個並存 29 GB,空間無感。

### 啟動方式

- 預設:Ollama 服務隨 Windows 啟動(系統匣羊駝圖示)
- 可以選擇關閉自動啟動,需要時手動跑 `ollama serve`

### 連線 endpoint

```
http://localhost:11434
```

被以下工具使用:
- Open WebUI(直連)
- LiteLLM(可加為 OpenAI 兼容後端)
- 未來 CrewAI(透過 `ollama/qwen3:32b` model 名)

---

## ComfyUI Diffusion 模型

詳見 `../comfyui/setup.md` 完整模型清單。簡述:

### 主力模型分工

| 場景 | 模型 | 速度 | 品質 | VRAM |
|---|---|---|---|---|
| 對比基準(2023) | SDXL 1.0 Base | ~10 秒 | 中 | ~7 GB |
| 快速試 prompt | FLUX.2 Klein 4B NVFP4 | 1.3 秒 | 高 | ~6 GB |
| 4K 大圖出稿 | Klein 4B + UltraSharp 4× | ~5 秒 | 高 | ~7 GB |
| **最終定稿(SOTA)** | **FLUX.2 Klein 9B Base + Qwen3 8B** | **41 秒** | **頂級** | **~21 GB** |
| 整合測試 | FLUX.1 Dev fp8 | ~30 秒 | 高 | ~16 GB |
| **物品移除(inpaint)** | **FLUX.1 Fill OneReward fp8 + Turbo-Alpha + Removal LoRA** | **93.68 秒** | **高** | **~24 GB 高峰** |

### 關鍵 Mapping(不可違反)

| Klein | 必配 CLIP | 維度 |
|---|---|---|
| Klein 4B | Qwen3 4B FP4 | 7680 |
| Klein 9B | Qwen3 8B FP8 mixed | 12288 |

混用會炸:`mat1 mat2 shapes cannot be multiplied`。

---

## ComfyUI LLM 節點(圖像理解)

### JoyCaption Beta1

**位置**:`D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\LLavacheckpoints\llama-joycaption-beta-one-hf-llava\`

**為什麼放 ComfyUI 內部**:LLM 節點 hardcode 路徑,不吃 `extra_model_paths.yaml`。

**用途**:
- 看圖、隨手反推內容(用快速反推 workflow)
- LoRA 訓練資料集反推(用訓練反推 workflow,11 個 Extra Options)

**VRAM**:nf4 量化下 ~5 GB(24GB 甜蜜帶)

**速度**:第一次推理 10-20 秒(載入),同 session 後續快取後快。

---

## 雲端 API(參考分工)

雖然不是本地,但常跟本地對比使用,記錄在這:

| API | 適用情境 | 為什麼用 |
|---|---|---|
| **Claude Sonnet 4.5/4.6/4.7** | 創造性 / 結構化輸出 / 長 context | 品質碾壓本地,token 不貴 |
| Claude Opus 4.7 | 最高品質決策、長文寫作 | 真的需要時才用 |
| Claude Haiku 4.5 | 高頻簡單任務 | 便宜快速 |
| **DeepSeek V4-Pro**(透過 NVIDIA NIM) | 高階推理、長 context、coding | 1.6T 參數、本地跑不了(見「已駁回」段) |
| DeepSeek V4-Flash(透過 NVIDIA NIM) | 快速推理(預設 reasoning_effort=high) | v4-pro 的輕量版,延遲較低 |

接入方式:
- 透過 LiteLLM(`D:\Work\LiteLLM\`)轉成 OpenAI 兼容 API
- Anthropic 走 `anthropic/...` provider;NVIDIA NIM 走 `nvidia_nim/...` provider(設定見 `../openwebui/setup.md` 「擴充:接入 NVIDIA NIM」段)
- Open WebUI 並排對話用
- CrewAI Agent backbone 用(Writer / Art Director 等需要創造性的角色)

---

## 同時運行限制

### 可以同時跑的組合

| 組合 | VRAM 估算 | OK? |
|---|---|---|
| Ollama qwen3:32b + ComfyUI 不啟動 | 20 GB | ✅ |
| ComfyUI Klein 4B + Ollama 暫停 | 6 GB | ✅ |
| ComfyUI Klein 9B Base + Ollama 暫停 | 21 GB | ✅(極限) |
| ComfyUI JoyCaption(nf4) + Ollama qwen3:32b | 5 + 20 = 25 GB | ❌ 爆 |
| ComfyUI Klein 9B + Ollama qwen3:32b | 21 + 20 = 41 GB | ❌ 大爆 |

### 切換策略

**方案 A:工作型態切換**(目前做法)
- 寫文 / Code / Agent → 啟動 Ollama
- 出圖 / 反推 → 暫停 Ollama,啟動 ComfyUI
- 用 `Stop-Service / Start-Service` 手動切

**方案 B:雙模式分工**
- Ollama 配 14B(9 GB)→ 留 15 GB 給 ComfyUI 同跑
- 但目前只有 32B,沒這個彈性

**方案 C:切雲端**
- 需要文字推理時用 Claude API
- 完全跳過本地 LLM 衝突
- 適合需要兩邊同時動的情境

---

## 待決事項

### 是否補下 14B

**現況**:只有 32B,雙模式跑會爆。

**何時觸發補下**:
- 開始正式跑 CrewAI agent 多 agent 工作流
- 發現「需要寫 code 同時生圖」變高頻
- 願意接受 9 GB 額外空間佔用

**補下指令**:
```powershell
ollama pull qwen3:14b
```

### CrewAI 模型分配規劃

未來 `D:\Work\creative-pipeline\` 用 CrewAI 編排時,初步分工:

| Agent | 後端 | 為什麼 |
|---|---|---|
| Writer(劇本) | Claude Sonnet API | 創造性 |
| Art Director(分鏡 + prompt) | Claude Sonnet API | 結構化 + 創造 |
| Image Gen Coordinator(呼叫 ComfyUI) | 本地 qwen3 14B(若補) / 32B | tool call 為主 |
| Video Gen Coordinator | 本地 LLM | 同上 |
| Voice / Editor | 本地 LLM | 同上 |

關鍵路徑用雲端、tool call 用本地,**避免 24GB VRAM 衝突**。

---

## 已駁回的選項

> 評估過、決定不採用的方案。寫在這避免日後重複討論、追溯駁回理由。
> 如果未來條件改變(硬體升級、模型行為更新),可重新評估。

### DeepSeek V4-Pro 本地化

**評估日期**:2026-04 月某次討論

**Wayne 的提議**:本地跑 DeepSeek V4-Pro,當主力 LLM。

**駁回**:本地不可行。

**理由**:
- 1.6T 參數規模
- 原始權重 ~865 GB
- Q4 量化後仍需 ~400 GB VRAM
- 24GB VRAM(5090 Laptop)差兩個數量級,連 offload 都救不回來

**替代方案(已接入)**:**透過 NVIDIA NIM API 雲端呼叫**(2026-04-28 完成,設定見 `../openwebui/setup.md` 「擴充:接入 NVIDIA NIM」段):

| 模型 | proxy 對外 model_name | 狀態 |
|---|---|---|
| DeepSeek V4-Pro | `deepseek-v4-pro` | ✓ 已通(三層驗證過) |
| DeepSeek V4-Flash | `deepseek-v4-flash` | ⏸ NIM upstream 高流量服務性下線,config 已就位待復服 |

v4-flash 復服後直接重打 `/v1/chat/completions` 即可,無需改 config。NIM 端服務狀態看 https://build.nvidia.com/deepseek-ai/deepseek-v4-flash 。

**重新評估觸發**(本地化方向):
- 個人硬體升級到 200 GB+ VRAM(短期不會)
- DeepSeek 釋出更激進的量化版本(< 24 GB)讓 5090 能塞

### Qwen3.6-27B 取代 qwen3:32b

**評估日期**:2026-04-24(Ollama 當天才登記支援 Qwen3.6 系列)

**Wayne 的提議**:用 qwen3.6:27b 取代 qwen3:32b 當 Ollama 主力(更新版本、更小)。

**駁回**:**取代不採用**,但模型保留供實驗用。

**理由**:
- **不支援 `/no_think` 標籤**:Qwen3.6 系列每次推理都會經過 thinking 階段
- 對 debug 場景影響大:thinking 過程會吃 5-30 秒等待時間,Wayne 偏好的「快速問答 + 觀察輸出」工作流被打斷
- qwen3:32b 支援 `/no_think`,可隨需求切換 thinking on/off,實用性更高

**現況**:
- Qwen3.6-27B 已下載成功,留在 `D:\Models\ollama\`
- 不刪除(供實驗、對比、特定 thinking-required 場景用)
- 主力依舊是 `qwen3:32b`

**重新評估觸發**:
- Qwen 上游補上 `/no_think` 支援(關注 release notes)
- 找到 Ollama 端 workaround 強制跳過 thinking

---

## 模型下載 SOP

### HuggingFace 下載

**標準做法**:用 `huggingface_hub` 或 web 下載。

**踩坑**:某些 repo(`fancyfeast/*` 等)強制走 xet bridge,卡 0 byte 即使 `HF_HUB_DISABLE_XET=1` + `hf_transfer` 都無效。

**繞過解法**:用 `curl.exe` 4 路並行下載(實測穩定 11 MB/s)。

詳見 `../comfyui/setup.md` 的踩坑 SOP 章節。

### Ollama 下載

直接 `ollama pull <模型名>`,自動下載到 `OLLAMA_MODELS` 指定目錄。

### Token 安全

**HF Token / API Key 規則**:
- 永遠不貼進 Claude Code / Open WebUI / 任何 AI 對話框
- 只放 PowerShell 環境變數(`$env:HF_TOKEN` / `$env:ANTHROPIC_API_KEY`)
- 在同一視窗啟動子程序讓它繼承
- 持久化:寫入 `.env`(該專案目錄,gitignored)+ NAS 加密備份

---

## 相關文件

- **`../comfyui/setup.md`**:ComfyUI 完整配置,所有 SD / FLUX 模型詳情
- **`../comfyui/sageattention-patches.md`**:讓 ComfyUI 加速 17% 的關鍵 patches
- **`../openwebui/setup.md`**:Open WebUI + LiteLLM 多模型介面(接 Ollama + Claude API)
- **`../davinci/pipeline.md`**:AI 影像 pipeline 整體規劃

---

**最後更新**:2026-04-29
