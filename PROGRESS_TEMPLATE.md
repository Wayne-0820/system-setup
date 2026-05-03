# PROGRESS_TEMPLATE — 進度報告範本

> **這份範本給「執行窗口的 Claude」用**。任務結束時,照這個格式產出報告。
> Wayne 會把報告貼給主規劃窗口,主窗口會把變更整合進 system-setup repo。

---

## 使用方式

任務結束時,Claude 主動產出以下格式報告(不用 Wayne 開口要)。
所有欄位都要填,沒變更的填「無」。

---

# 進度報告

**日期**:YYYY-MM-DD(實機執行當天,規則 15)
**對話主題**:[一句話標題,例如「ComfyUI Klein 9B Base workflow 建立」]
**執行 Claude 模型**:[Sonnet 4.6 / Opus 4.7 / 其他]
**對話總長**:[幾小時 / 幾個 turn,大概就好]

---

## 1. 變更摘要

[用 1-3 句話總結這次做了什麼,不要列點,寫成段落]

---

## 2. 環境變更

> ⚠️ **列「新增」前先對照** system-setup 既有 MD(尤其 `comfyui/setup.md` / `decisions.md` / `reinstall-manifest.md` / `tools/README.md`),**釐清「前次對話已建立」 vs 「本次新增」**。不能只憑這次對話脈絡推斷,否則會誤把既有檔案標成新增,主窗口整合時會出錯。

### 新增 / 修改的檔案

格式:`絕對路徑 — 動作 — 說明`

範例:
- `D:\Work\ComfyUI_portable\...\custom_nodes\ComfyUI_LayerStyle_Advance` — 新增 — 透過 Manager 安裝,啟用 JoyCaption 節點
- `D:\Work\system-setup\comfyui-workflows\JoyCaption_Beta1_快速反推.json` — 新增 — 6 節點反推 workflow
- `D:\Work\ComfyUI_portable\...\python_embeded\Lib\site-packages\opencv-python` — 移除 — 跟 contrib 衝突

### 新增 / 修改的環境變數

[路徑、值、scope(User/System)]

### 新增 / 修改的設定檔

[config.yaml、.env、bat 檔之類的改動]

---

## 3. 新增 / 修改的功能

### 新工具 / 套件

| 名稱 | 版本 | 安裝路徑 | 用途 |
|---|---|---|---|
| 例:JoyCaption Beta1 | - | D:\Work\...\LLavacheckpoints\ | 圖像反推 prompt |

### 新模型

| 類型 | 路徑 | 大小 | 用途 |
|---|---|---|---|
| Diffusion | D:\Models\diffusion\diffusion_models\xxx | 9 GB | Klein 9B Base |

### 新指令 / 啟動方式

```bash
# 範例
D:\Work\system-setup\start_comfyui.bat
```

---

## 4. 學到的踩坑

格式:**症狀 / 原因 / 解法 / 未來注意**

範例:
### LiteLLM 1.83.12 + uv + Windows → CLI 讀不到 --config
- **症狀**:啟動時不讀指定 config,改讀預設
- **原因**:CLI parsing 在 Windows + uv 有 bug
- **解法**:鎖定到 1.55.10
- **未來注意**:升版前實測 `--config` 能讀

(若無則填「無」)

---

## 5. 對 system-setup 文件的影響

請主規劃窗口協助更新以下文件:

### 必須更新(資訊不對,影響重灌恢復)

- `comfyui/setup.md` — 補上 SageAttention shim 段落
- `ai-models/local-models.md` — 補 Klein 系列、Qwen3 配對表

### 建議更新(增加完整度)

- `context.md` — D 槽結構補 D:\tmp\
- `README.md` — 索引加新文件

### 建議新增

- `comfyui/sageattention-patches.md`(獨立文件,內容包含 6 個 patches)

---

## 6. 待辦(下次回來)

格式:**項目 / 優先 / 預估時間**

- [ ] 用 Klein 9B Base 生 workflow 圖示底圖 — 中 — 30 分鐘
- [ ] 轉 .ico 多尺寸 — 低 — 15 分鐘
- [ ] 開始下一個中國 workflow 重建 — 高 — 2 小時起跳

---

## 7. 風險 / 警告

[如果有發現可能在重灌時造成問題的地方,記在這]

例:
- PyTorch 升級會覆蓋 6 個 SageAttention patches,升級前必須先讀 comfyui/sageattention-patches.md
- xet bridge 繞過用的 curl 並行下載沒有自動化腳本,重灌後要手動跑

---

## 8. 自評

[這次任務的完成度、品質、Wayne 滿意度,簡短 2-3 句]

例:
> 完成 4 個 workflow 的 GUI 構建,2 個成功跑通(SDXL / Klein 4B)。Klein 9B Base 第一次跑遇到 Subgraph 格式不熟,花了 1 小時學新格式但最終跑通。下次接觸新格式應該先查官方範本而不是猜。

---

**範本結束**

---

**最後更新**:2026-05-04
