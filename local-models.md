# 本地模型探索指南

**定位**:重灌後本地模型**用途尚未定案**。這份文件提供硬體規劃、框架選擇、初始模型候選,等系統建好再決定實際用途。

---

## 硬體限制:RTX 5090 = 24GB VRAM

| 尺寸 | Q4 體積 | 在 24GB 上 | 速度 |
|---|---|---|---|
| 70B | ~40GB | 嚴重溢出 | 慢(<5 tok/s) |
| 32B | ~18-20GB | 塞得下但吃緊 | 中 |
| **14B** | **~8-10GB** | **甜蜜點** | **快(20+ tok/s)** |
| 7-8B | ~5GB | 極寬裕 | 極快 |

**24GB 上 32B 模型做 agent 長 context 會有壓力**,14B 才是穩定主力。

---

## 框架選擇

### Ollama(主要,必裝)

- 指令列輕量:`ollama pull` / `run` / `list`
- HTTP API:`http://localhost:11434`
- CrewAI、LangChain、LiteLLM 等原生支援

### LM Studio(選用)

- GUI 方便瀏覽模型、測效能、看 VRAM 用量
- 24GB 使用者認真挑模型時很有用
- OpenAI 相容 server:`http://localhost:1234/v1`

**建議**:先只裝 Ollama。LM Studio 要認真挑模型時再說。

---

## 模型儲存規劃

```powershell
# Ollama 模型目錄
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'D:\Models\ollama', 'User')
```

LM Studio 啟動後 Settings → Models directory → `D:\Models\lmstudio`。

### 容量配置(`D:\Models\` 建議)

用途未定,**先留 150 GB 彈性空間**:

- 2-3 個 14B 模型(Q5/Q8 高品質)≈ 40 GB
- 1-2 個 32B 模型(Q4)≈ 40 GB
- 小模型試驗(7B 以下)≈ 20 GB
- embedding / 特殊用途 ≈ 10 GB
- 留白 ≈ 40 GB

**不要**一開始下 70B 級模型,24GB 跑那尺寸是折磨。

---

## 初始試水模型候選

這是**探索清單**不是生產架構。實際留哪些用過再決定。

| 模型 | 尺寸 | 適合探索 |
|---|---|---|
| **Qwen2.5-Coder 14B** | Q6 ~12GB | 程式助理、24GB 舒服 |
| **Qwen2.5 14B** | Q6 ~12GB | 通用對話、中文強 |
| Qwen2.5-Coder 32B | Q4 ~18GB | 品質上限,短對話 OK |
| Llama 3.3 8B | Q8 ~9GB | 英文通用 |
| Phi-4 14B | Q6 ~12GB | 推理強 |
| Nomic Embed / BGE-M3 | <1GB | RAG / 向量檢索 |

**第一個拉的建議**:

```powershell
ollama pull qwen2.5-coder:14b
```

> 模型版本更新快,下載前到 `ollama.com/library` 看當下 tag。

---

## 使用情境候選

重灌好後可評估:

- **Claude Code 批次輔助**:低敏感任務(註解、格式化、重構)走本地,關鍵路徑用 Claude API
- **creative-pipeline 成本優化**:CrewAI 某些 agent 走本地模型,降 token 成本
- **資料處理 pipeline**:分類、摘要、向量化
- **實驗 agent 框架**:本地模型當便宜後端
- **離線工作**:保密 / 斷網備援

**不建議**:當 Ldbot 執行期元件(已決定單走 Claude Code)。

---

## 重灌後執行順序

1. `winget install Ollama.Ollama`
2. `[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'D:\Models\ollama', 'User')`
3. 重開 PowerShell,確認 `echo $env:OLLAMA_MODELS` 指到 D 槽
4. `ollama pull qwen2.5-coder:14b` 試水
5. 實際用一陣子再決定留哪些、要不要裝 LM Studio
