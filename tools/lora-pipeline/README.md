# 角色 LoRA bootstrap pipeline(config 驅動)

從「1 張參考圖」擴成一致的角色資料集,驅動實機 ComfyUI 出圖,給 LoRA 訓練用。
**腳本零寫死模型** —— checkpoint / vae / ipadapter / 取樣 / 解析度 / prompt 矩陣全在 config。

> 背景與驗證配方:`D:\Work\system-setup\progress-reports\2026-06-27_character-lora-poc.md`

---

## 架構原則:分離 pipeline、共用 plumbing

不同生成路線(SDXL IPAdapter bootstrap / Flux Kontext)是**根本不同的 pipeline**(graph、conditioning 機制、打標格式都不同),所以**各自一支腳本**(= 之後 WCopilot 固化時的兩顆按鈕),不用「一支腳本內 if 切換」(會變 leaky abstraction、改一邊動到另一邊)。它們只**共用 transport 層**(`comfy_common.py`),boilerplate 只寫一次。

```
tools\lora-pipeline\
├── comfy_common.py      # 共用水管:送單 / 輪詢 / reference staging(stdlib only)
├── sdxl_bootstrap.py    # 路線1:SDXL IPAdapter bootstrap(純 SDXL,無 arch 分支)
├── flux_kontext.py      # 路線2:Flux/Kontext —— 之後做
├── make_contactsheet.py # 共用工具:出圖夾組帶編號聯絡表(需 Pillow)
├── config.sdxl.json     # SDXL 路線的全部旋鈕(純 ASCII)
└── README.md            # 本檔
```

---

## 用法(SDXL 路線)

前提:ComfyUI 已啟動(預設 `http://127.0.0.1:8188`)、`ComfyUI_IPAdapter_plus` 已裝、IPAdapter/CLIP-ViT-H 模型已就位。

```
# 冒煙測試(只出 1 張,驗證 config + 連線)
python sdxl_bootstrap.py --config config.sdxl.json --limit 1 --wait

# 跑整個矩陣(32 姿勢 x seeds_per_prompt)
python sdxl_bootstrap.py --config config.sdxl.json --wait

# 出圖夾組聯絡表(用 embedded python,因為要 Pillow)
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe make_contactsheet.py --dir "<comfy_output>\charlora_batch"
```

出圖落在 ComfyUI 的 output 目錄底下、`output_prefix` 指定的子夾(本機 ComfyUI output 被導到 `D:\Media\AI_Raw\ComfyUI_Output`,所以是 `D:\Media\AI_Raw\ComfyUI_Output\charlora_batch\`)。

---

## config 旋鈕(`config.sdxl.json`)

- **`models.checkpoint`** — 換底模就改這行(同為 SDXL/Illustrious 架構直接換,例 PDXL/NoobAI)。
- **`models.vae`** — 留空 = 用 checkpoint 內建 VAE;填檔名 = 用 `vae/` 裡那顆覆寫。
- **`models.ipadapter_preset`** — `PLUS (high strength)` 對應 `ip-adapter-plus_sdxl_vit-h` + 自動配 ViT-H clip vision。
- **`ipadapter.weight` / `weight_type`** — **驗證過的甜蜜點:0.5 + `style and composition`**。`linear` / `strong style transfer` 會爆髮色,別用。
- **`reference_image`** — 絕對路徑(腳本自動複製進 ComfyUI input)或已在 input 的檔名。
- **`prompt.id_core`** — 角色定裝描述(身份主槓桿)。**改角色就改這裡**(髮型/年齡/特徵)。
- **`prompt.poses / scenes / outfits`** — 多樣性矩陣,腳本交叉組合。

---

## 之後做 Flux/Kontext 路線(`flux_kontext.py`)

另開一支、import 同一個 `comfy_common.py`。重點:Kontext 是 in-context 編輯、native 保身份、**不靠 IPAdapter**;graph、prompt 形式、打標都跟 SDXL 不同 —— 所以是獨立腳本而非 SDXL 的分支。屆時配 `config.flux.json`。

---

## 注意

- config 純 ASCII(遵守 config-ASCII 規則),中文說明只在本 MD。
- HF token 等 secret 不進 config;gated 模型下載走環境變數 / WCopilot 下載器。
