# ComfyUI 乾淨重來策略

**立場**:不要「一次學會 ComfyUI」。**建立一個可以隨時砍掉重來的環境**,然後慢慢加東西。搞壞了 5 分鐘可以回來。

---

## 安裝方式:Portable 版

**只用 portable,不用系統版**。理由:

- 自帶獨立 Python 環境(放在資料夾裡,不碰系統 Python、不碰 uv)
- 整個是一個資料夾,想砍就砍
- 依賴地獄時直接砍資料夾重來

**下載**:`https://github.com/comfyanonymous/ComfyUI/releases`(找 `ComfyUI_windows_portable_nvidia.7z`)

**解壓到**:`D:\Work\ComfyUI_portable`

**啟動**:執行 `run_nvidia_gpu.bat`

---

## 最小化初始設定

### 1. 模型目錄共用

編輯 `D:\Work\ComfyUI_portable\ComfyUI\extra_model_paths.yaml`(把 `.example` 複製改名):

```yaml
comfyui:
    base_path: D:\Models\sd\

    checkpoints: checkpoints/
    loras: loras/
    vae: vae/
    controlnet: controlnet/
    embeddings: embeddings/
    upscale_models: upscale_models/
    clip: clip/
    clip_vision: clip_vision/
    diffusion_models: diffusion_models/
```

這樣 Forge(如果未來裝)可以共用同一套模型,不重複下載。

### 2. 裝唯一一個必要的 custom node:ComfyUI Manager

```powershell
cd D:\Work\ComfyUI_portable\ComfyUI\custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

重啟 ComfyUI,右上會出現 "Manager" 按鈕。以後缺任何節點:

- 載入 workflow → 報 "Missing node" → 點 Manager → "Install Missing Custom Nodes" → 它自己去抓

### 3. 不要急著裝其他 custom node

只有在「載入某 workflow 才缺」時才裝。不要看到 YouTube 推薦就裝一堆。

---

## 節點連線核心規則(兩分鐘看懂)

每個節點有左右兩側:

- **左邊 = 輸入**(需要什麼才能運作)
- **右邊 = 輸出**(產出什麼)

連線 = 某節點的輸出 → 另一節點的輸入,**兩端顏色必須一樣**:

| 顏色 | 型別 | 是什麼 |
|---|---|---|
| 紫 | MODEL | 底模載入後的主模型 |
| 黃 | CLIP | 文字編碼器 |
| 紅 | VAE | 影像編碼/解碼器 |
| 橘 | CONDITIONING | prompt 編碼後結果 |
| 粉 | LATENT | 擴散過程的半成品張量 |
| 藍 | IMAGE | 實際像素圖 |

連不上 = 型別不合。記住這個就不會迷路。

---

## 最基本的 t2i workflow(7 節點)

重灌完**親手建這個一次**,不要載別人的:

```
[Load Checkpoint]
    │ MODEL ──────────────────────┐
    │ CLIP ──┬─────────────┐      │
    │ VAE ───┼─────┐       │      │
    │        │     │       │      │
    ▼        ▼     │       ▼      ▼
[CLIP Text Encode(正向)]──────►[KSampler]───► LATENT
[CLIP Text Encode(負向)]──────►         ▲
                                            │
[Empty Latent Image]────► LATENT ──────────┘
                                            │
                                    [VAE Decode]
                                            │
                                            ▼
                                    [Save Image]
```

步驟:

1. 右鍵 → Add Node → loaders → **Load Checkpoint**(選一個 SDXL 底模)
2. conditioning → **CLIP Text Encode (Prompt)** 兩個(正向、負向)
3. latent → **Empty Latent Image**
4. sampling → **KSampler**
5. latent → **VAE Decode**
6. image → **Save Image**
7. 照圖連線

跑通 = 掌握 ComfyUI 基本結構。

---

## 載入別人 workflow 的 SOP

1. 拖 workflow JSON 進 ComfyUI 視窗
2. 看哪些節點是紅框(代表缺)
3. Manager → Install Missing Custom Nodes → 一鍵裝
4. 重啟 ComfyUI
5. 檢查模型是否都在 `D:\Models\sd\`(缺的去 Civitai / HuggingFace 抓)
6. 先跑一次看能不能出圖
7. **不懂的節點**:丟給 Claude Code 問

---

## Claude Code × ComfyUI 用法

在 `D:\Work\ComfyUI_portable\ComfyUI` 打開 Claude Code:

- **解析 workflow**:「讀 workflows/framepack_test.json,逐節點解釋在做什麼」
- **查 missing node**:「我載入 workflow 說少了 `XXXSampler`,幫我查來自哪個 repo」
- **修 custom node 錯誤**:「`custom_nodes/xxx` 啟動時 ImportError,幫我看哪裡出問題」
- **寫自己的節點**:「寫一個 custom node,輸入 IMAGE 輸出平均亮度 FLOAT」
- **API 整合**:「寫 Python client 透過 ComfyUI /prompt endpoint 非同步送 workflow」

---

## 災難復原

**Level 1(custom node 壞了)**:砍 `custom_nodes/<壞掉的>`,重啟

**Level 2(Python 依賴打架)**:砍 `python_embeded/`,解壓 portable 7z 蓋回來,保留 `custom_nodes/` 和模型設定

**Level 3(整包爛掉)**:砍 `D:\Work\ComfyUI_portable\` 整個,重解壓 7z。模型在 `D:\Models\sd\` 不受影響,1-2 小時可以回來

---

## 學習節奏建議

- **第 1 天**:裝 portable、Manager、建最基礎 t2i。出第一張圖
- **第 2-3 天**:加 LoRA、ControlNet
- **第 4-5 天**:img2img、inpaint
- **第 2 週**:裝 FramePack 節點,跑首尾幀
- **第 3 週起**:CrewAI 透過 API 呼叫 ComfyUI

全程讓 Claude Code 在旁邊解釋。不懂就問。
