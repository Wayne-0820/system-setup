# tools/ — system-setup 周邊腳本

放 repo 下的 Python 小工具,處理「不該寫進主流程、但跨對話會重複用到」的雜事。

> 最後同步:2026-04-30

---

## 目錄索引

| 腳本 | 用途 | 依賴 |
|---|---|---|
| `png_to_ico.py` | PNG → 多尺寸 ICO,內建亮度閾值去背 | Pillow(ComfyUI portable 內建,免裝) |
| `workflow_submit.py` 🧪 | ComfyUI frontend workflow JSON → API 格式 + POST `/prompt` | stdlib(ComfyUI portable Python 也行) |
| `build_wan22_workflow.py` | 產出 Wan 2.2 A14B T2V/I2V 合一 workflow JSON(720P 81幀 4 步 Lightx2v 版本)。輸出到 `comfyui-workflows\Wan2.2_A14B_T2V-I2V合一_720P_81幀_4步.json` | stdlib |

---

## png_to_ico.py

### 用途

PNG → 多尺寸 ICO 轉換,內建亮度閾值去背演算法。專門用於把生成式 AI 出的圖示底圖轉成 Windows 桌面捷徑可用的 ICO。

### 依賴

**Pillow**。ComfyUI portable 的 `python_embeded` 已內建,**不需建獨立 venv**。

### 呼叫範例

```powershell
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" `
  "D:\Work\system-setup\tools\png_to_ico.py" `
  "<input.png>" "<output.ico>" `
  --threshold-min 15 --threshold-max 90
```

### 參數

| 參數 | 用途 |
|---|---|
| `<input.png>` | 來源 PNG 路徑(必填) |
| `<output.ico>` | 輸出 ICO 路徑(必填) |
| `--threshold-min` | 亮度 < 此值 → alpha = 0(去背) |
| `--threshold-max` | 亮度 > 此值 → alpha = 255(保留) |

中間值線性羽化(漸進透明度)。

### 輸出尺寸

7 種:**16 / 24 / 32 / 48 / 64 / 128 / 256**。Windows 在不同 UI 場景會自動挑合適尺寸。

---

## workflow_submit.py

**狀態**:🧪 實驗性(目前驗證 Workflow #3b,#3a 嘗試已 deprecated)

### 用途

ComfyUI workflow JSON 有兩種格式:**frontend**(GUI 用,有 nodes/links/widgets_values/座標)+ **API**(`/prompt` 用,以 node id 為 key、inputs 是 dict)。
本工具將 frontend JSON 轉成 API 格式並 POST 到 ComfyUI HTTP `/prompt`,**避開 GUI 載入時的 widget 嚴格校驗 + LoadImage dropdown cache 兩個雷**(詳見 `comfyui/setup.md` 重要踩坑 SOP §11)。

### 依賴

純 stdlib(`json` / `urllib.request` / `argparse` / `uuid` / `time`)。系統 Python 或 ComfyUI `python_embeded` 都可跑。ComfyUI 必須在 8188 listen。

### 呼叫範例

```powershell
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" `
  "D:\Work\system-setup\tools\workflow_submit.py" `
  "D:\Work\system-setup\comfyui-workflows\<some_workflow>.json" `
  --label "smoke_test"
```

### 參數

| 參數 | 用途 |
|---|---|
| `<workflow_json_path>` | frontend workflow JSON 絕對路徑(必填,positional) |
| `--label` | 印 log 用的標籤,任意字串(選填,預設空) |

### 行為

1. POST `/prompt` 拿 `prompt_id`
2. 每 2 秒 poll `/queue` + `/history` 直到完成
3. 印出 `status` + `outputs`(SaveImage 寫入的檔名清單)

### 已知 hidden widget 處理

ComfyUI 有些 node 在 widgets_values 多塞 frontend-only 資訊(node 不註冊但 GUI 顯示):

- KSampler / KSamplerAdvanced: `control_after_generate` 在 `seed` / `noise_seed` 之後
- LoadImage: `image` upload-mode marker 在 `image` 之後

當前 hardcoded 在 `HIDDEN_AFTER` set,未來踩到新 hidden widget 要 patch。

### Caveat

- 其他 workflow 若有不同 hidden widget,可能轉錯(目前只驗證 Workflow #3b)
- 觸發升級條件:Workflow #4 以後煙測踩到新 hidden widget → 派工 generalize + 補測試

### 檔名變動史

- 2026-04-29:從 `D:\tmp\submit_smoke.py`(階段 1 staging)升至 tools/(原樣 copy + docstring 路徑/檔名 update,沒 generalize logic)

---

## ⚠️ 限制與設計約束

### 亮度閾值去背的適用範圍

亮度閾值法**只適用於**:

- ✅ **純黑底 + 高對比主體**(發光 / 高飽和)
- ✅ **純白底 + 高對比主體**

**不適用於**:

- ❌ 漸層背景
- ❌ 寫實風格(背景與主體亮度接近)
- ❌ 任何複雜背景

複雜背景請改用 **RemBG / SAM**,不要拿這隻腳本硬套(會破)。

### ICO 用底圖的 Prompt 設計規則

**為了讓亮度去背能用 + 16px 縮圖也看得懂**,生底圖的 prompt 階段就要鎖死:

1. **底色**:純黑或純白,**禁止**漸層、霧化、bokeh
2. **主體對比**:跟底色亮度差距要大(發光、高飽和、強反差)
3. **元素數量**:**≤ 4 個視覺元素**
   - 過多元素 16px 縮圖會糊成光點,LANCZOS 演算法救不了
   - 例:8 條放射線 + 細電路紋這種設計在 16px 會壞
   - 規則:「即使縮成 16px 也能看懂的形狀辨識度」
4. **構圖**:置中、留邊,不要把元素塞滿到邊緣

### 跑出來不滿意怎麼辦

順序:

1. **先調 `--threshold-min` / `--threshold-max`** 給定的閾值,看去背結果是否正確
2. **若閾值法救不了** → 回去改 prompt(降元素數、提高對比、換純底)
3. **若 prompt 也救不了** → 換用 RemBG,別硬撐閾值法

---

## 為什麼選 ComfyUI 內建 Python 跑

ComfyUI portable 的 `python_embeded` 已經有:

- `Pillow`
- `numpy`
- `opencv-contrib-python`

寫 ComfyUI 周邊小工具時優先吃這個 Python,**省掉建獨立 venv 的麻煩**,也不污染系統 Python。

但**不要拿它去裝額外套件**,那會混進 ComfyUI 自己的環境,出狀況難 debug。要裝額外依賴的工具請自建 venv。

---

## 加新工具的規範

往 `tools/` 加新腳本時:

1. **腳本內 docstring** 寫清楚用途、參數、回傳
2. **本 README** 加一條到「目錄索引」表格 + 一個獨立小節
3. **依賴選擇**:
   - 純 stdlib → 用系統 Python
   - 用 Pillow / numpy / opencv → 用 ComfyUI `python_embeded`
   - 其他套件 → 自建 venv,且在文件中註明
4. **不要**寫成需要互動式輸入的腳本 — 全部走 CLI 參數,方便日後 batch 處理

---

**最後更新**:2026-04-30
