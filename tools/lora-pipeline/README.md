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
├── flux_kontext.py      # 路線2:Flux Kontext(in-context 編輯,native 保身份)
├── tag_wd14.py          # 打標:WD14 onnx -> Danbooru caption(standalone,不驅動 ComfyUI)
├── make_contactsheet.py # 共用工具:出圖夾組帶編號聯絡表(需 Pillow)
├── config.sdxl.json     # 路線1 旋鈕(純 ASCII)
├── config.flux.json     # 路線2 旋鈕(純 ASCII)
├── config.tagger.json   # 打標旋鈕(純 ASCII)
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

## 用法(Flux Kontext 路線)

前提:ComfyUI 已啟動、Kontext 模型就位(`flux1-dev-kontext_fp8_scaled` + `clip_l` + `t5xxl_fp8_e4m3fn` + `ae.safetensors`)。Flux 12B,比 SDXL 慢 ~3 倍、吃 VRAM 緊。

```
# 冒煙測試
python flux_kontext.py --config config.flux.json --limit 1 --wait

# 跑整個矩陣
python flux_kontext.py --config config.flux.json --wait
```

重點:Kontext 是 **in-context 編輯**、native 保住參考圖的主體身份(**不靠 IPAdapter**),所以保的是**原始參考那個男孩**(不像 SDXL route 會因 prompt 漂移)。

config 旋鈕(`config.flux.json`):
- **`models.unet / clip_l / clip_t5 / vae`** — 全可變動(換別的 Flux/Kontext 模型直接改)。
- **`kontext.guidance`** — FluxGuidance,2.5 起手(調高更貼指令、調低更自由)。
- **`canvas.mode`** — `reference`(預設,強保留、框構接近參考)/ `empty`(配 width/height,框構自由度高 → 想要全身/大幅換姿勢時用,是變化槓桿)。
- **`prompt.instruction_template` + `variations`** — **自然語言編輯指令**(不是 booru tag)。`{variation}` 會被每條 variation 取代。

> 取捨:Kontext 身份保持最強,但「從胸上半身參考生全身/大幅換姿勢」的自由度可能不如 SDXL route;`canvas: empty` + 指令明寫 full body 是槓桿,實測為準。

---

## 打標(WD14 -> caption)

生成 + 篩好資料集後,對那個資料夾跑 WD14 tagger 產 Danbooru 標籤 caption(訓練用)。**standalone,不驅動 ComfyUI** —— 用 embedded python 已有的 onnxruntime 跑 onnx,只共用 `comfy_common.load_config`。首次自動下載 tagger 模型(~1.2GB,公開免 token)。

```
# 先在 config.tagger.json 設 dataset_dir + trigger_word + strip_tags,再批量打標
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe tag_wd14.py --config config.tagger.json

# 單張試打(只印不寫檔)
... tag_wd14.py --config config.tagger.json --smoke <one_image>
```

每張圖寫同名 `.txt`:`<trigger_word>, <tags...>`。

config 旋鈕(`config.tagger.json`):
- **`tagger.model_repo`** — 預設 `SmilingWolf/wd-eva02-large-tagger-v3`(最準);要快/小可換 `wd-v1-4-moat-tagger-v2`。
- **`tagger.general_threshold` / `character_threshold`** — 標籤門檻(0.35 / 0.85 起手)。
- **`trigger_word`** — 每張 caption 開頭的罕見觸發詞。
- **`strip_tags`** — 要烤進 trigger 的**身份外觀**標籤(髮色/瞳色/髮型);結構標籤(`1boy`/`solo`)留著別 strip。

> 註:onnxruntime 的 CUDA provider 需 CUDA 12.x/cuDNN9;本機 CUDA 13 不合會自動退 CPU(一次性打標夠用)。

---

## 注意

- config 純 ASCII(遵守 config-ASCII 規則),中文說明只在本 MD。
- HF token 等 secret 不進 config;gated 模型下載走環境變數 / WCopilot 下載器。
