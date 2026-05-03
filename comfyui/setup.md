# ComfyUI 配置指南

> **這份文件反映實際運行狀態**(不是規劃)。
>
> 最後同步:2026-04-30
>
> ComfyUI 是這台機器的主要生成工具,配 SageAttention 3 跑 SDXL / FLUX.1 / FLUX.2 Klein 系列。

---

## 環境基線

```yaml
ComfyUI:
  版本: 0.19.3 (revision 150 [30860264], 2026-04-17 release)
  類型: portable
  路徑: D:\Work\ComfyUI_portable\ComfyUI_windows_portable\
  Python: 3.13.12 embedded(內建在 python_embeded\)
  PyTorch: 2.11.0+cu130
  CUDA Toolkit: 13.2(在 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2\)
  Visual Studio: 2022 17.14.31 Build Tools(C++ Desktop workload)
  Attention: SageAttention 3 Blackwell(編譯時間 2026-04-25,詳見 sageattention-patches.md)
```

**結構不拍平**:`ComfyUI_portable\ComfyUI_windows_portable\` 這層保留,跟官方範例對齊。

---

## 路徑配置

### 模型統一目錄

ComfyUI 透過 `extra_model_paths.yaml` 讀 `D:\Models\diffusion\`(避免重複下載):

```
D:\Models\diffusion\                # 模型主目錄
├── checkpoints\             # SDXL / FLUX.1 all-in-one 整合模型
├── diffusion_models\        # FLUX.2 / Klein 分離 UNET
├── clip\                    # text encoders(Qwen3, T5)
├── clip_vision\             # image encoders
├── vae\
├── loras\
│   └── wan22-lightning\        # Wan 2.2 Lightx2v 4-step Lightning LoRA(子目錄隔離)
├── controlnet\
├── upscale_models\
└── embeddings\
```

### 例外:LLM 類模型(寫死路徑,不能搬)

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\
└── LLavacheckpoints\        # JoyCaption / Llama 等 LLM
    └── llama-joycaption-beta-one-hf-llava\
```

**為什麼要寫死**:LLM 節點(如 JoyCaption)在程式碼裡 hardcode 這個路徑,不吃 `extra_model_paths.yaml`。**不要搬到 D:\Models\**。

### 輸出目錄

```
D:\Media\AI_Raw\ComfyUI_Output\    # 透過 --output-directory 指定
```

不放在預設的 `ComfyUI\output\`,因為:
- 預設位置在 portable 巢狀目錄裡,不好找
- 出圖屬於 D:\Media\ 範疇,跟其他 AI 輸出統一管理

### 編譯暫存

```
D:\tmp\
└── SageAttention\           # source 保留(233 MB,以後重編用)
```

---

## 啟動配置

**主啟動檔**:

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\run_nvidia_gpu.bat
```

**啟動參數**:

```bat
--windows-standalone-build
--output-directory "D:\Media\AI_Raw\ComfyUI_Output"
--use-sage-attention
```

備份檔:`run_nvidia_gpu.bat.before_sageattention.bak`(SageAttention 加上前的版本)

### 雙擊啟動工具

**檔案**:`D:\Work\system-setup\start_comfyui.bat`

```bat
@echo off
title ComfyUI Launcher (SageAttention)
powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location 'D:\Work\ComfyUI_portable\ComfyUI_windows_portable'; & '.\run_nvidia_gpu.bat'"
```

**行為**:開新 PowerShell(`-NoExit` 保留 log)→ cd 到 ComfyUI 目錄 → 跑啟動 bat。

桌面捷徑與自訂 ICO 已完成。ICO 工作路徑 `D:\Work\system-setup\assets\comfyui.ico`,**不入 repo**(備份位於 NAS)。重灌恢復步驟見 `../reinstall-manifest.md`。

---

## 已下載模型清單

### Checkpoints(`D:\Models\diffusion\checkpoints\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `sd_xl_base_1.0.safetensors` | 6.46 GB | SDXL 1.0 基準參考(2023 標竿) |
| `flux1-dev-fp8.safetensors` | 16.06 GB | FLUX.1 Dev all-in-one |
| `SUPIR-v0Q.ckpt` | 4.96 GB | SUPIR 商業級升頻(custom node 已裝,workflow 未搭) |

### Diffusion Models(`D:\Models\diffusion\diffusion_models\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `flux-2-klein-4b-nvfp4.safetensors` | 2.29 GB | Klein 4B 快速草稿(4 步) |
| `flux-2-klein-9b-fp8.safetensors` | 8.79 GB | Klein 9B distilled(4 步) |
| `flux-2-klein-base-9b-fp8.safetensors` | ~9 GB | Klein 9B Base(20 步,SOTA) |
| `flux.1-fill-dev-OneReward-fp8.safetensors` | 11.085 GB | FLUX.1 Fill OneReward fp8(萬物移除主模型,Workflow #2) |
| `flux1-dev.safetensors` | 23.80 GB | FLUX.1 Dev fp16 全精度(BFL gated repo,Workflow #3b 用,UNETLoader weight_dtype=fp8_e4m3fn 載入時轉 fp8 省 VRAM) |
| `flux1-dev-kontext_fp8_scaled.safetensors` | 11.09 GB | FLUX.1 Kontext fp8 scaled(Comfy-Org repackage,Workflow #3a 嘗試後 deprecated 留 disk 待未來重評,詳 conflicts 段「歷史紀錄」) |
| `qwen_image_edit_2509_fp8_e4m3fn.safetensors` | 19.03 GB | Qwen Image Edit 2509 主模型(fp8 e4m3fn 量化,Workflow #3a-v2「保留人物改姿勢」核心) |
| `Wan2_2-T2V-A14B_HIGH_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 T2V A14B HIGH noise(fp8 e4m3fn scaled,Kijai;**注意:T2V HIGH 用 underscore `_HIGH`,LOW 用 hyphen `-LOW`,是 Kijai 歷史命名遺跡**) |
| `Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 T2V A14B LOW noise(fp8 e4m3fn scaled,Kijai) |
| `Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 I2V A14B HIGH noise(fp8 e4m3fn scaled,Kijai;**KJ wrapper 路線專用,state_dict 跟 ComfyUI core 不對齊**) |
| `Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 I2V A14B LOW noise(fp8 e4m3fn scaled,Kijai;同上) |
| `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | 14.29 GB(13.32 GiB)| Wan 2.2 I2V A14B HIGH noise(fp8 e4m3fn scaled,Comfy-Org/Wan_2.2_ComfyUI_Repackaged,SHA256 `6122e79d...8d5e6a42`;**ComfyUI core native 路線專用**)|
| `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | 14.29 GB(13.32 GiB)| Wan 2.2 I2V A14B LOW noise(fp8 e4m3fn scaled,Comfy-Org repackage,SHA256 `5471a457...fffc21e`;同上)|

### CLIP / Text Encoders(`D:\Models\diffusion\clip\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `qwen_3_4b_fp4_flux2.safetensors` | 3.85 GB | 給 Klein 4B 用(Qwen3 4B FP4,維度 7680) |
| `qwen_3_8b_fp8mixed.safetensors` | 8.07 GB | 給 Klein 9B 用(Qwen3 8B FP8 mixed,維度 12288) |
| `clip_l.safetensors` | 0.229 GB | FLUX 配套 CLIP-L(Workflow #2 / 未來 FLUX 系列共用) |
| `t5xxl_fp8_e4m3fn.safetensors` | 4.558 GB | FLUX 配套 T5-XXL fp8(Workflow #2 / 未來 FLUX 系列共用) |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | 8.74 GB | Qwen 2.5 VL 7B(fp8 scaled,Workflow #3a-v2 / 未來 Qwen Edit / Qwen Image 系列共用)— **注意路徑紀律:Comfy-Org repo URL 標 `split_files/text_encoders/`,本機 yaml 只映射 `clip:`,規範一律落 `clip\` 子目錄(2026-04-29 派工 v1 第 6 個 bug 訂正)** |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | 6.27 GB | Wan 2.x text encoder(UMT5-XXL fp8 e4m3fn,Kijai/WanVideo_comfy;**KJ wrapper 路線專用,跟 ComfyUI core CLIPLoader state_dict 不對齊不可混用,實證見踩坑 #19**)|
| `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | 6.27 GB(6.27 GiB)| Wan 2.x text encoder(UMT5-XXL fp8 e4m3fn scaled,Comfy-Org/Wan_2.1_ComfyUI_repackaged,SHA256 `c3355d30...651204f68`;**ComfyUI core CLIPLoader 專用**)|

### VAE(`D:\Models\diffusion\vae\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `flux2-vae.safetensors` | ? | 給 4B / FLUX.1 用 |
| `full_encoder_small_decoder.safetensors` | ~250 MB | 給 Klein 9B 用(專用) |
| `ae.safetensors` | 0.312 GB | FLUX 配套 ae VAE(Workflow #2,源自 Comfy-Org/z_image_turbo split_files/vae/) |
| `qwen_image_vae.safetensors` | 0.236 GB | Qwen Image VAE(Workflow #3a-v2 / 未來 Qwen 系列共用) |
| `Wan2_1_VAE_bf16.safetensors` | 0.24 GB | Wan 2.1/2.2 VAE bf16(Kijai/WanVideo_comfy;Wan 2.2 T2V/I2V 標準 workflow 用這個) |

### LoRA(`D:\Models\diffusion\loras\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `Flux-Turbo-Alpha.safetensors` | 0.646 GB | alimama 8-step distilled LoRA(加速,Workflow #2) |
| `removal_timestep_alpha-2-1740.safetensors` | 0.086 GB | lrzjason ObjectRemovalFluxFill v2(物品移除,Workflow #2) |
| `qwen-image\Qwen-Image-Lightning-8steps-V1.1-bf16.safetensors` | 0.791 GB | lightx2v Qwen Image Lightning 8 步加速 LoRA(子目錄 `loras\qwen-image\`,Workflow #3a-v2 用,推 sampler=euler / scheduler=simple / cfg=1.0)|
| `consistence_edit_v2.safetensors` | 0.571 GB | lrzjason Qwen Edit「保留人物」核心 LoRA(strength=0.4,Workflow #3a-v2 用;HF mirror `hoveyc/comfyui-models`,SHA256 跟 CivitAI 主來源一致)|
| `wan22-lightning\Wan22_A14B_T2V_HIGH_Lightning_4steps_lora_250928_rank128_fp16.safetensors` | 1.227 GB | Wan 2.2 T2V 4-step Lightning LoRA HIGH(2025-09-28 新版,asymmetric rank128,Workflow #3c 用,cfg=1.0)|
| `wan22-lightning\Wan22_A14B_T2V_LOW_Lightning_4steps_lora_250928_rank64_fp16.safetensors` | 0.614 GB | Wan 2.2 T2V 4-step Lightning LoRA LOW(rank64,2025-09-28 新版)|
| `wan22-lightning\Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors` | 0.614 GB | Wan 2.2 I2V 4-step Lightning LoRA HIGH(rank64,Kijai/old 版本,HF 未釋出 I2V 新版,從 `LoRAs/Wan22-Lightning/old/` 下載;**KJ wrapper 路線專用**)|
| `wan22-lightning\Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors` | 0.614 GB | Wan 2.2 I2V 4-step Lightning LoRA LOW(rank64,/old/ 版本;同上)|
| `wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors` | 1.14 GB | Wan 2.2 I2V 4-step lightx2v Lightning LoRA HIGH(Comfy-Org/Wan_2.2_ComfyUI_Repackaged v1,SHA256 `d176c808...deff11e`;**ComfyUI core native 路線專用**;Workflow #3c-v2 用,LoRA strength=1.0)|
| `wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors` | 1.14 GB | Wan 2.2 I2V 4-step lightx2v Lightning LoRA LOW(Comfy-Org repackage v1,SHA256 `024f21de...0d8aab7f9`;同上)|

### ControlNet(`D:\Models\diffusion\controlnet\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `FLUX.1-dev-ControlNet-Union-Pro-2.0\diffusion_pytorch_model.safetensors` | 3.99 GB | Shakker-Labs FLUX.1-dev ControlNet Union Pro 2.0(支援 pose / depth / hed / canny 等多模式,Workflow #3b 用) |

### Upscale(`D:\Models\diffusion\upscale_models\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `4x-UltraSharp.pth` | 67 MB | 4K 升頻(實測 1024→4096 約 3-4 秒) |
| `RealESRGAN_x4plus.pth` | 67 MB | 備用升頻 |

### LLM(`ComfyUI\models\LLavacheckpoints\`)

| 模型 | 大小 | 用途 |
|---|---|---|
| `llama-joycaption-beta-one-hf-llava\`(4 shards) | 15.81 GB | JoyCaption Beta1 圖像反推(SHA256 全綠) |

---

## Wan 2.2 模型 distribution 區分(Kijai vs Comfy-Org repackage)

Wan 2.x 系列主模型 / Lightning LoRA / CLIP 在不同 source 有不同 repackage,**state_dict key naming 不對齊,不可混用**(2026-05-03 candidate B 煙測實證,踩坑 #19)。

| 類型 | Kijai 版(KJ wrapper 路線專用) | Comfy-Org repackage(ComfyUI core native 路線專用) | 對應 loader node |
|---|---|---|---|
| 主模型 | `Wan2_2-I2V-A14B-HIGH/LOW_fp8_e4m3fn_scaled_KJ.safetensors`(Kijai/WanVideo_comfy)| `wan2.2_i2v_high/low_noise_14B_fp8_scaled.safetensors`(Comfy-Org/Wan_2.2_ComfyUI_Repackaged)| KJ:`WanVideoModelLoader` / native:`UNETLoader` |
| Lightning LoRA | `wan22-lightning\Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH/LOW_fp16.safetensors`(Kijai/old)| `wan2.2_i2v_lightx2v_4steps_lora_v1_high/low_noise.safetensors`(Comfy-Org repackage v1)| KJ:`WanVideoLoraSelect` / native:`LoraLoaderModelOnly` |
| Text Encoder | `umt5-xxl-enc-fp8_e4m3fn.safetensors`(Kijai/WanVideo_comfy)| `umt5_xxl_fp8_e4m3fn_scaled.safetensors`(Comfy-Org/Wan_2.1_ComfyUI_repackaged,Wan 2.x 共用)| KJ:`LoadWanVideoT5TextEncoder` / native:`CLIPLoader` |
| VAE | `Wan2_1_VAE_bf16.safetensors`(Kijai/WanVideo_comfy)| (Comfy-Org repackage `wan_2.1_vae.safetensors` 未實機驗證 state_dict 對齊性)| KJ:`WanVideoVAELoader` / native:`VAELoader` |

**實證**(2026-05-03,Wan 2.2 #3c candidate B):Kijai 版 `umt5-xxl-enc-fp8_e4m3fn.safetensors` 餵 ComfyUI core `CLIPLoader` 撞 `NotImplementedError: Cannot copy out of meta tensor; no data!`(stack: `comfy/sd1_clip.py:213` → `comfy/ops.py:151` → `comfy/model_management.py:1287`)— state_dict key naming 不對齊,部分 weight load fail 留 meta tensor。改用 Comfy-Org repackage 後跑通(execution 217.7s,跟 wrapper 路線合一檔 baseline 14.17 min/segment 比快 3.9×)。

**紀律(規則 12 (B) cross-verify 教訓)**:supporting model patch 前 cross-verify state_dict 對齊性(safetensors header inspection 取 keys 比對 / ComfyUI 試 load 看 partial load warning),不靠檔名假設「同 base model 不同 repackage = 純命名差」。

---

## 關鍵 Mapping(不可違反!)

**Klein 系列跟 Qwen3 必須配對**,維度不對會報 `mat1 mat2 shapes cannot be multiplied`:

| Klein 模型 | 必配 CLIP | 維度 |
|---|---|---|
| Klein 4B | Qwen3 4B FP4 | 7680 |
| Klein 9B(distilled & Base) | Qwen3 8B FP8 mixed | 12288 |

**不可混用**。Klein 4B 配 Qwen3 8B 會炸,反之亦然。

---

## 已裝 Custom Nodes

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\
├── ComfyUI-Manager                    # V3.39.2(必裝,套件管理)
├── ComfyUI_LayerStyle                 # 主 repo
├── ComfyUI_LayerStyle_Advance         # 含 JoyCaption2 + JoyCaptionBeta1
├── ComfyUI-SUPIR                      # SUPIR 商業級升頻(workflow 未搭)
├── ComfyUI-Custom-Scripts             # pythongosssss(Show Text 🐍 等介面增強)
├── ComfyUI_Custom_Nodes_AlekPet       # 含 GoogleTranslateTextNode
├── ComfyUI-KJNodes                    # kijai(v1.3.9,Flux-fill 萬物移除 workflow 用)
├── comfyui_controlnet_aux             # Fannovel16(2026-04-29 裝,64 節點,Workflow #3b 用 AIO_Preprocessor / DWPreprocessor)
├── rgthree-comfy                      # rgthree(v1.0.260407001,架構前已裝、2026-04-28 補入記錄,utility 工具集,0 衝突)
├── Comfyui-QwenEditUtils              # lrzjason / 小志Jason(2026-04-29 裝,14 節點,Workflow #3a-v2 用 TextEncodeQwenImageEditPlus_lrzjason;事實上 C 方案 KSampler 走內建路徑,本 pack 留作未來 #5/#6 Qwen 系列候選)
├── ComfyUI-WanVideoWrapper            # kijai(2026-04-30 裝,142 節點,Wan 2.2 T2V/I2V 影片生成;FantasyPortrait sub-pack 需另裝 onnx)
└── websocket_image_save.py            # 內建
```

### 安裝方式統一規則

**透過 ComfyUI Manager 介面安裝**,不要手動 `pip install`。
Manager 會自動處理:
- Git clone repo
- 處理 requirements.txt
- 第一次啟動時 pip 安裝依賴

**例外**:某些節點需要修復 opencv 衝突等,看具體節點文件。

### Manager 搜尋踩坑

Manager 搜尋以「**包名 (repo 名)**」為主,**不是節點名**。以節點名搜常會搜到付費替代品而非真正想要的開源版:

| 你想要的節點 | 直接搜「節點名」會發生什麼 | 正確搜法 |
|---|---|---|
| Show Text 🐍(pysssss) | 搜「ShowText」→ 跳付費雲端節點,搜不到 | 搜 `Custom-Scripts` 或認作者 ID `pythongosssss` |
| JoyCaption | 搜「JoyCaption」→ 搜不到正確包 | 搜 `LayerStyle Advance`(節點包在 LayerStyle 裡) |

**規則**:確認正確 repo 名再搜,不要用節點名硬找。

### AlekPet 自動 pip 安裝(已處理)

第一次啟用 GoogleTranslateTextNode 時,會自動裝:
- `googletrans`
- `deep-translator`

走 Google 公開 endpoint,**無需 API key**,但偶爾會被 rate limit(這時切 DeepTranslatorTextNode 用 MyMemory)。

---

## 裝新 custom node 流程

ComfyUI 節點生態混亂,不同 pack 經常衝突。任何新 pack 安裝走以下流程,**避免覆蓋現有節點導致 workflow 行為偏差**。

衝突資料庫架構:

- **`conflicts.md`** — 主索引(已安裝 pack 總表、active 反向節點索引、解決決策表、SOP、風險分級標準)
- **`conflicts-{pack}.md`** — 每個 pack 的衝突明細(per-pack)。命名規則:**pack 名小寫去 `ComfyUI-` 前綴**(例:`ComfyUI-KJNodes` → `kjnodes`、`ComfyUI_LayerStyle` → `layerstyle`、`was-node-suite-comfyui` → `was`)

### 執行窗口流程(裝 pack 的窗口)

#### Step 1:安裝前查詢

1. 在 ComfyUI Manager 點 Install,**先看 conflicts 數字,不要直接按下去**
2. 若 >0,點開列表,**逐一比對 `conflicts.md` 的「反向節點索引」**
3. 對每個衝突節點判斷:
   - 該節點不在反向索引 → 風險低,可裝(會新增衝突 row,但無 active 撞擊)
   - 該節點在反向索引但**沒在 workflow 用到** → 仍可裝,記錄
   - 該節點**正在 workflow 使用中** → 慎重決策(放棄這個 pack,或接受 active 改為新 pack)

#### Step 2:安裝

正常透過 Manager 安裝。

#### Step 3:產 per-pack 檔(裝完馬上做)

執行窗口直接產 `conflicts-{pack}.md` 完整檔案,template 參考 [`conflicts-kjnodes.md`](conflicts-kjnodes.md)(KJNodes 第一份)。標準段落:

1. **Header** — pack 名 / 版本 / 安裝日 / 狀態 / 引用主索引
2. **TL;DR** — 安裝原因 / 衝突數 / 是否安全 / 重點 active 衝突
3. **ComfyUI 衝突機制(原理回顧)** — 標準段,各檔重複沒關係,讓單一檔可獨立讀
4. **衝突分組**(按風險):
   - 群組 1:同 fork / 抄襲 pack(風險零)
   - 群組 2:多重衝突
   - 群組 3:單一衝突
5. **對 system-setup 下一階段規劃的影響** — 對照本檔下方「下一階段規劃」逐項評估
6. **做的決策** — 本 pack 安裝決策 + 連帶決策(例如「Swwan 永不安裝」)
7. **相關文件**

#### Step 4:把 per-pack 檔貼給主窗口

**執行窗口只產 per-pack 檔,不直接改主索引,不直接 commit**。把完整 per-pack 檔貼給主窗口整合。

### 主窗口流程(整合的窗口)

接到 per-pack 檔後,**更新 `conflicts.md` 的三處**:

1. **「已安裝 pack 總表」** — append 一行新 pack(連結到 per-pack 檔)
2. **「反向節點索引(active)」** — 新 active 衝突節點按字母順序插入(該節點若已存在 row 則 append 新 pack 到「提供 pack」欄)
3. **「解決決策表」** — 重大決策一行(中以上風險才寫)

更新「最後更新」日期 + TL;DR 統計 → 把更新後的主索引 + per-pack 檔一起給 Wayne 下載 → Wayne 放回 repo + commit + push。

### 風險分級標準

見 [`conflicts.md`](conflicts.md) 的「風險分級標準」段(零 / 低 / 中 / 高 / 致命五級)。

### 反例(別這樣)

- ❌ 直接 Install 不看 conflicts 數字(會覆蓋現有節點而不自知)
- ❌ 看到 conflicts 數字大就跳過 pack(很多衝突源是不會裝的冷門 pack,實際無風險)
- ❌ 多窗口同時改 `conflicts.md`(只有主窗口寫,執行窗口讀)
- ❌ 執行窗口直接 commit per-pack 檔到 repo(要先過主窗口整合,確保主索引同步更新)
- ❌ 把衝突報告貼進本檔(`setup.md` 只放流程,不放資料)

---

## 已建立 Workflow

存放位置:`D:\Work\system-setup\comfyui-workflows\`(中文「用途定位派」命名)

### 圖像生成系列

| Workflow | 模型組合 | 步數 | 用途 |
|---|---|---|---|
| `SDXL_1.0_基準參考.json` | sd_xl_base_1.0 | 20 | 對比基準 |
| `Klein_4B_快速草稿_4步.json` | klein-4b-nvfp4 + qwen3-4b-fp4 | 4 (cfg=1) | 快速試 prompt(1.3 秒/張) |
| `Klein_4B_4K大圖出稿.json` | 同上 + UltraSharp 4× | 4 + 升頻 | 大圖輸出(4096×4096) |
| `Klein_9B_Base_頂級定稿_20步.json` | klein-base-9b-fp8 + qwen3-8b-fp8mixed + full_encoder_small_decoder | 20 (cfg=5) | 最終定稿(41 秒/張) |
| `flux2_klein_9b_t2i_official.json` | 官方 ComfyUI Klein 9B 範本 | - | 38.1 KB,參考用 |

### 圖像反推系列

| Workflow | 用途 | 節點數 | 主要節點 |
|---|---|---|---|
| `JoyCaption_Beta1_快速反推.json` | 看圖、隨手反推 | 6 | JoyCaption Beta One + GoogleTranslate(英→中) |
| `JoyCaption_Beta1_訓練反推.json` | LoRA 訓練資料集反推 | 6 | JoyCaption Beta One(純英文,11 個 Extra Options) |

**規則**:訓練版**不接翻譯節點**,輸出保持英文。

### Workflow 架構特性

**Klein 9B Base 用 ComfyUI Subgraph 格式**(2025+ 新標準):
- 內部封裝 UNETLoader / CLIPLoader / VAELoader / Flux2Scheduler / CFGGuider / KSamplerSelect / EmptyFlux2LatentImage / RandomNoise / SamplerCustomAdvanced
- 雙擊節點進入內部
- 模型路徑包在內部(不在外面看得到的層)

---

## VRAM 實測數據

關鍵參考(在 5090 Laptop 24GB 上實測):

| 場景 | VRAM 使用 | 餘裕 |
|---|---|---|
| Klein 4B NVFP4 | ~6 GB | 18 GB |
| Klein 9B FP8 distilled | ~13-15 GB(估) | 9-11 GB |
| Klein 9B Base + Qwen3 8B | 20,400 MiB | ~3.5 GB |
| **Klein 9B Base + Qwen3 8B + UltraSharp 4K 升頻** | **20,962 MiB 高峰** | **~3.5 GB(極限)** |

**結論**:Klein 9B Base + 4K 升頻在 5090 Laptop 24GB **可跑**,靠 ComfyUI dynamic VRAM offload。

**建議**:同時跑 ComfyUI(Klein 9B)+ Ollama(qwen3:32b)會爆,二選一。

---

## 速度實測(SageAttention 加速效果)

| Workflow | 未開 SageAttention | 開 SageAttention | 加速 |
|---|---|---|---|
| Klein 9B Base 20 步 | 50 秒 | 41 秒 | ~17% |

**注意**:bf16 + FP4 path 有 CUDA misaligned address bug(SageAttention issue #357),所以 Klein 9B Base 走 bf16 沒享受到 100% FP4 加速。fp16 path 完全正常。

---

## JoyCaption Beta1 使用慣例

### 量化選擇

- **nf4 量化** 是 24GB VRAM 的甜蜜帶(實際 ~5GB VRAM)
- 第一次推理載入 ~5GB 進 VRAM,耗時 10-20 秒
- 同 session 內後續推理快取,速度快

### 主節點參數(預設)

- `caption_type`: Descriptive
- `caption_length`: any
- `max_new_tokens`: 512
- `top_p`: 0.90
- `top_k`: 0
- `temperature`: 0.60

### Extra Options 使用情境

**快速反推 4 個**(看圖用):
- exclude_image_resolution
- do_not_include_artist_name_or_title
- avoid_meta_descriptive_phrases
- exclude_sexual

**訓練反推 11 個**(完整 SD prompt):
- exclude_image_resolution
- do_not_include_artist_name_or_title
- avoid_meta_descriptive_phrases
- do_not_use_ambiguous_language
- include_lighting
- specify_lighting_sources
- include_camera_angle
- include_camera_shot_type
- include_camera_vantage_height
- specify_depth_field
- include_composition_style

### 翻譯節點接法規則

| Workflow | 翻譯節點 | 輸出語言 | 理由 |
|---|---|---|---|
| 快速反推 | ✅ 接 GoogleTranslateTextNode(英→繁中) | 中英對照 | 看圖、人類讀取 |
| 訓練反推 | ❌ **不接** | 純英文 | LoRA 訓練要保英文 caption,中翻會破 SD prompt 結構 |

**Rate limit fallback**:AlekPet `GoogleTranslateTextNode` 走 Google 公開 endpoint,台灣連線偶爾被擋,fallback 切 `DeepTranslatorTextNode` + MyMemory backend。

---

## ComfyUI 輸入圖落點紀律

`LoadImage` node widget 只認 `D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\input\` 子樹。custom node pack 自帶的測試圖(例 Kijai 的 `custom_nodes\ComfyUI-WanVideoWrapper\example_workflows\example_inputs\human.png`)要餵給 LoadImage,**必須先 copy 到 `ComfyUI\input\`**,不能直接讀 pack 內路徑。

派工指具體輸入檔名前先 verify 機器真相;不行就寫「pack 自帶測試圖任一張(對應場景優先)」這種留判斷給執行端的措辭。

---

## 重要踩坑 SOP

### 1. PowerShell 中文路徑

**症狀**:`Get-ChildItem -Filter` 在中文路徑回空結果
**解法**:用 `cmd /c dir /b` 替代

### 2. HuggingFace xet bridge 卡 0 byte

**症狀**:某些 repo(例如 `fancyfeast/*`)強制走 xet,`huggingface_hub` 會卡 0 byte,即使 `HF_HUB_DISABLE_XET=1` + `hf_transfer` 都無效
**解法**:直接用 4 路 `curl.exe` 並行繞過(實測 11 MB/s 穩定)

### 3. HF Token 安全

**規則**:Token 永遠不貼進 Claude Code 對話框(會進雲端對話歷史)
**做法**:只放 PowerShell 環境變數 `$env:HF_TOKEN`,在同一視窗啟動 `claude --dangerously-skip-permissions` 讓子進程繼承

### 4. Gated repo 同意

每個 BFL FLUX repo 要分別到瀏覽器點 Agree(yemwei / Wayne0820 帳號)。

### 5. ComfyUI Subgraph 格式

2025+ 新格式:模型路徑包在內部,雙擊節點進入內部。**不要被「看不到模型載入節點」嚇到**。

### 6. 修改 ComfyUI portable 內部檔需文件記錄

包括 PyTorch site-packages 的任何改動。**升級會被覆蓋**。詳見 `sageattention-patches.md`。

### 7. Custom Nodes 安裝後要整個重啟

不是刷新頁面,是整個 ComfyUI server 重啟。第一次啟動會自動 pip 裝依賴,看 console 紅字判斷成敗。

### 8. opencv 衝突(LayerStyle guidedFilter,2026-04-26 首修 / 2026-04-30 擴充)

**症狀**:LayerStyle 的 guidedFilter 節點報錯 `Cannot import name 'guidedFilter' from 'cv2.ximgproc'`

**根本原因**:LayerStyle 需要 `opencv-contrib-python`(含 ximgproc)。任何把 `opencv-python` 列為 requirement 的 custom node 安裝後,Manager prestartup 自動裝 `opencv-python` → 覆蓋 contrib → guidedFilter 壞。

**已知會觸發的 pack**:`ComfyUI-WanVideoWrapper`(requirements.txt 含 `opencv-python`)。其他含 cv 的 pack 裝前先 grep requirements.txt。

**修復 SOP**(2026-04-30 訂正,純 uninstall 不夠):

```powershell
# Step 1: 卸掉污染源
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip uninstall opencv-python opencv-python-headless -y

# Step 2: force-reinstall contrib(純 uninstall opencv-python 會損壞 cv2 共用檔案,必須 force-reinstall 才能修復)
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip install --force-reinstall --no-deps opencv-contrib-python==4.13.0.92

# Step 3: 驗證
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -c "import cv2; print(cv2.__version__); from cv2 import ximgproc; print('guidedFilter OK')"
```

**長期解:pip_overrides.json(ComfyUI-Manager 官方機制)**

Manager 支援 `pip_overrides.json`,可把 `opencv-python` 的安裝請求重導向 `opencv-contrib-python`。設定後 Manager 偵測 requirements 滿足時自動跳過裝 opencv-python。詳見 [`conflicts-wanvideowrapper.md`](./conflicts-wanvideowrapper.md)「pip_overrides 設定」段。

**⚠️ 2026-04-30 補注**:純 uninstall `opencv-python` 不夠。因為 opencv-python 和 opencv-contrib-python 共用 cv2 module 命名空間,uninstall 時把共用檔案也清了,contrib metadata 還在但實體 cv2 檔案損壞。**必須 force-reinstall opencv-contrib-python** 才能完整修復。

### 9. ArgosTranslate sub-node 在繁中系統 cp950 install fail(2026-04-29)

**症狀**:啟動 ComfyUI console:
```
Failed to import module ArgosTranslateNode because
UnicodeDecodeError: 'cp950' codec can't decode byte 0xe2 in position 1009: illegal multibyte sequence
```
alekpet 自動 disable 該 sub-node,2 個節點(`ArgosTranslateCLIPTextEncodeNode` / `ArgosTranslateTextNode`)未 register。

**原因**:argos-translate 的 `setup.py` 用 `open()` 不指定 `encoding=`,Windows 11 繁中系統 `locale.getpreferredencoding()` 回 `cp950`,讀檔內 UTF-8 byte 炸 → wheel build fail。**這是 user-level CLAUDE.md 教訓 5 的 in-the-wild 實證**(非 yaml/json/.env 而是 Python wheel build)。

**解法**:不修(暫無 ArgosTranslate offline 翻譯需求,Google + Deep 已涵蓋線上場景)。詳 [`conflicts-alekpet.md`](./conflicts-alekpet.md)。

**未來注意**:若需要 ArgosTranslate offline 翻譯,要 patch upstream `setup.py` 加 `encoding='utf-8'`,或在 `chcp 65001` + `PYTHONIOENCODING=utf-8` 環境下 reinstall。

### 10. ComfyUI 啟動到背景用 Start-Process pattern(2026-04-29)

**症狀**:`cmd /c "start /B run_nvidia_gpu.bat > log 2>&1"` 啟動到背景,log 檔不被建立,8188 也不 listen。

**原因**:`start /B` detach 後新 process 的 stdout 不繼承 redirect。執行 PowerShell tool 跑完該 cmd 立刻 exit,但 ComfyUI process 沒被 spawn 出來。

**解法**:用 `Start-Process -PassThru`:

```powershell
Start-Process -WorkingDirectory "D:\Work\ComfyUI_portable\ComfyUI_windows_portable" `
  -FilePath "powershell.exe" `
  -ArgumentList "-Command","& '.\run_nvidia_gpu.bat' *> D:\tmp\comfyui.log" `
  -WindowStyle Hidden -PassThru
```

`-PassThru` 拿 PID,主 PowerShell 立刻 return,ComfyUI process 在 background 跑,stdout/stderr 都進 log 檔。

### 11. ComfyUI workflow widget 嚴格校驗(2026-04-29)

**症狀 A**:GUI 載入 workflow JSON 後,`ControlNetLoader` 節點標紅「缺少模型」,即使 widget value 字串跟 `/object_info` dropdown options 完全一樣(byte-identical)。GUI 點 dropdown 重選同一個檔即恢復綠。

**症狀 B**:GUI 載入 workflow 後,`LoadImage` 的 image dropdown 在啟動後新增的圖檔不在列表(ComfyUI 啟動時 cache `input/` 目錄掃描,後加的檔不 refresh)。widget value 字串雖然檔案存在 disk,但 dropdown 沒列 → widget 靜默 reset 為空 → 跑時 `FileNotFoundError`。

**原因**:
- 症狀 A:ComfyUI frontend 對 COMBO type widget 的 value validation 在 load 時走 strict normalization 比對。**path separator 是常見成因**:RH cloud workflow JSON 用 forward slash(`FLUX.1-dev-...-Pro-2.0/diffusion_pytorch_model.safetensors`),Windows ComfyUI 內部用 backslash(`FLUX.1-dev-...-Pro-2.0\diffusion_pytorch_model.safetensors`)
- 症狀 B:LoadImage dropdown 用啟動時 cache,需手動 refresh

**⚠️ 訂正**:不能靠改走 HTTP `/prompt` API bypass 這個校驗。**ComfyUI server 端 `execution.py` 在 prompt validation 階段也跑 dropdown 值校驗**,API 跟 GUI 都會撞同一個雷(回 `node_errors[N] type=value_not_in_list`)。

**解法**(只兩條):
- 任何含子目錄路徑的 dropdown widget(ControlNet / **LoraLoaderModelOnly 含子目錄 LoRA**(2026-04-29 #3a-v2 實證 Workflow `qwen-image/Qwen-Image-Lightning-8steps-V1.1-bf16.safetensors` forward slash 版撞同雷)/ 其他 model loader)path:GUI 點 dropdown 重選一次(canonical 字串寫回),或**手動 patch JSON widget value 為 backslash 版本**
- LoadImage 缺檔:GUI drag-drop 圖進 LoadImage 節點(自動 copy 進 `input/` + refresh)

**Python patch backslash escape 紀律**(2026-04-29 #3a-v2 踩到):用 `replace('/', chr(92))` 或 `replace('/', os.sep)` 比 `replace('/', '\\\\')` 安全 — 後者在 PowerShell here-string + Python source + JSON dump 三層 escape 中容易算錯一層,寫成 2-backslash chars 而非 1。Verify 用 `len(new) == len(old)`(替換前後字數應該一致 if separator 一致)。

**自動化路線**:GUI 互動以外,可用 `tools/workflow_submit.py` POST `/prompt`(跳過 GUI widget reset / dropdown cache 兩個 GUI 雷,但**path separator 雷仍要先解**)。詳 [`../tools/README.md`](../tools/README.md)。

### 12. Wan 2.2 14B + sageattn fp8 + torch.compile inductor 反而拖慢(2026-04-30)

**症狀**:加 `WanVideoTorchCompileSettings (backend=inductor, mode=default, compile_transformer_blocks_only=True)`,每 step 從 sageattn baseline ~2 分鐘變 ~5 分鐘。run #1 21.1 分鐘 / run #2 process 內 cache reuse 20.4 分鐘,只差 44 秒。

**原因**:推測 inductor default mode codegen 出來的 kernel 比 sageattn 既有 fused attention kernel 慢;`compile_transformer_blocks_only=True` 把每個 transformer block 重 lower 蓋掉 sageattn 優化。也可能是 fp8_e4m3fn_scaled + Compute Capability 12.0 (Blackwell) 還沒被 inductor 完整支援。

**解法**:**不要加 torch.compile**。純 sageattn + Lightx2v 4-step LoRA 已達 12.91 分鐘 / 4 步。

**未來注意**:要再試 torch.compile 的話先試 `mode=max-autotune` / `mode=reduce-overhead`,或關 `compile_transformer_blocks_only` 改 full graph compile。但當前 baseline 不靠 torch.compile 就達標,沒急迫性。

### 13. ComfyUI prompt graph + seed 全相同會 cache execution(2026-04-30)

**症狀**:第二次提交完全一樣的 prompt + 同 seed,0.37 秒就 `execution_success`,所有節點 `execution_cached`,sampler 沒實際跑。

**原因**:ComfyUI 執行端 cache 比對 prompt graph 雜湊 + seed,完全相同就直接回上次輸出。

**解法**:煙測腳本支援 `--seed` 參數,每次跑改 seed 強制重執行。

### 14. Bash run_in_background 子進程 cwd 漂到 C 槽,`/tmp` 解析錯誤(2026-04-30)

**症狀**:`run_in_background` 跑 Python 寫死 `/tmp/foo.json` → `FileNotFoundError: 'C:/Users/Wayne/AppData/Local/Temp/foo.json'`,但檔案實際在 `D:/tmp/`。

**原因**:Python on Windows 把 `/tmp/...` 解析成「當前 drive 的 \tmp\」。Bash tool 互動模式 cwd 在 D:,但 `run_in_background` 子進程 cwd 改到 C: → `/tmp` 變 `C:\tmp\`(不存在)。

**解法**:Bash run_in_background 跑的 Python script,檔案路徑用絕對 `D:/...`,不用 `/tmp/` 或相對路徑。

### 15. SaveAnimatedWEBP 寫出檔 frame duration=None(2026-04-30)

**症狀**:ComfyUI `SaveAnimatedWEBP` widget `fps=16.0` 設了,但寫出的 .webp 81 frame 每個 `duration=None`。VLC / ffprobe 當壞檔 reject;Chrome / Edge / Firefox 只顯示第一 frame;Image viewer 用瀏覽器 default 100ms (10 fps)。

**原因**:ComfyUI / Pillow 的 SaveAnimatedWEBP 邏輯沒把 fps widget 轉成 per-frame duration chunk 寫進 webp。

**解法**:別用 SaveAnimatedWEBP 出片給播放器看。改 `SaveVideo` (comfy-core) 或 VHS pack 任一條,走 ffmpeg mux 路徑自動帶 frame_rate metadata。

**未來注意**:任何 ComfyUI 影片 workflow 都該驗 `PIL.Image.info['duration']` 不為 None,否則 .webp 等同壞檔。

### 16. ComfyUI process 收尾後 model cache 不自動 unload(2026-04-30)

**症狀**:T2V 煙測完隔幾分鐘,VRAM 仍佔 16 GB(free 只剩 8 GB),新 prompt 提交踩 OOM 或 token swap 拖慢。

**原因**:ComfyUI 為下次同 model 快速復用,cache 模型在 VRAM,不主動 release。

**解法**:每次煙測前 `curl -X POST http://127.0.0.1:8188/free -d '{"unload_models": true, "free_memory": true}'`(比 stop ComfyUI process 重啟省 model 重 load 時間)。

**未來注意**:煙測腳本 / 派工 SOP 加進前置步驟,特別是切換 T2V↔I2V 或不同 model loader 之間。

### 17. system 沒裝 ffmpeg → ffprobe 不在 PATH(2026-04-30)

**症狀**:I2V 煙測派工要 ffprobe 驗 .webp,`ffprobe: command not found`。

**原因**:未走 `winget install Gyan.FFmpeg` 或對等管道裝 ffmpeg。

**解法**:`winget install Gyan.FFmpeg`(2026-04-30 已裝)。

**未來注意**:影片相關任務 ffmpeg / ffprobe 是基線工具,不該等到要用才裝。decisions.md winget 清單已加。

### 18. Wan 2.2 14B I2V sage3 升級 walking back(2026-05-03,ε 系列收尾)

**症狀**:嘗試把 Wan 2.2 A14B I2V workflow 的 self-attn + cross-attn 兩條路徑都從 sage2 升 sage3 fp4 kernel(API JSON / 合一檔 `attention_mode` 從 `sageattn` 改成 `sageattn_3`),sampler 在 step 0 立刻 `Fatal Python error: Aborted`。

**原因**:跑 9 輪 ε 系列派工(ε-1a → ε-9),確認 layered failure **至少 3 層**,前兩層各自有 patch 驗證有效但**第 3 層未解**。

| 層 | 機制 | finding 輪 | 解法狀態 |
|---|---|---|---|
| (a) | model 在 cpu — WanVideoWrapper LoRA merge 後 `nodes_model_loading.py:1797` 強制 `model.to(offload_device)` + sampler 入口 `load_weights` 條件 `patcher.model["sd"] is not None` 不滿足沒 fire 拉回 cuda → forward cross-device → driver Aborted | ε-7 print(`param_cpu=1095, param_cuda=0`)| **ε-8 patch** 驗證有效:`nodes_sampler.py` line 873(`gc.collect()` 後)加 `transformer.to(device)`,VRAM sampling 階段 15.5 GB used 證明 model 拉回 cuda |
| (b) | cross-attn 走 sdpa — `model.py:925` cross_attn 創建點 missing `attention_mode` kwarg → 走 `attention.py:117` SDPA fallback → seq_len 75600 SDPA 在 cuda 仍 Fatal Aborted | ε-2 vendor source debug print | **ε-3 patch** 驗證有效:`model.py:925` 加 `attention_mode=self.attention_mode` kwarg(對齊 self_attn 行為),stack trace 不再命中 attention.py:117 |
| (c) | FFN `ffn_chunked` 內 activation forward Aborted — stack `activation.py:816 → container.py:253 → model.py:998 ffn_chunked → block.forward(line 1388) → WanModel.forward(line 3274)`,跟 model device / attention path 都無關 | ε-9 暴露(ε-3 + ε-8 兩 patch 疊加後仍 Abort)| **未解**,獨立 root cause |

**解法**:**walking back 到 sage2 baseline v8**(2026-04-30,14.17 min/segment)。合一檔 + API JSON `sageattn_3` 4 hits 改回 `sageattn`(2026-05-03 ε-final 完成)。Vendor source 不留任何 patch 殘留(`model.py` SHA256 = `90A3CE73...` / `nodes_sampler.py` SHA256 = `BDD0BE10...` / `attention.py` SHA256 = `13A5DFBB...`,均對齊 baseline)。

**關鍵 finding**(避免未來重蹈):
1. `--disable-dynamic-vram` 是 ComfyUI core flag,**不控制 WanVideoWrapper 內部 offload 邏輯**(ε-4 verify)
2. WanVideoWrapper sampler 不走 ComfyUI ModelPatcher 標準流程(0 個 `mm.load_models_gpu` / `patch_model` 呼叫),完全脫離主框架(ε-6 audit)
3. WanVideoModelLoader `load_device` widget default `"offload_device"`;`merge_loras` 從 LoRA dict 內取 default True;`nodes_model_loading.py:1797` LoRA merge 後**無條件** `model.to(offload_device)` fire(ε-5 audit)
4. WanModel **0 buffer**(全用 `nn.Parameter`,沒 `register_buffer`)→ ε-6 audit 「buffer 漏網」假設 falsified(ε-7 verify)
5. ε-3 progress report (C 分支) 當時把 FFN Aborted 歸因「offload mode」**不準確** — ε-9 證明即使 model 在 cuda + cross-attn 走 sage3,FFN 仍 Abort

**未來「sage3 重啟」決策依據**:
- WanVideoWrapper upstream 修了第 3 層(`ffn_chunked` activation forward 在 sage3 路徑下的 fail mode)→ 可重新嘗試(GitHub issues / PRs 追蹤)
- ε-3 / ε-8 兩 patch 各自仍可立刻 apply(預期 patched SHA256:`model.py` = `27EB2D3BB46798D52453218A9029E6F3A3FE623B661CF390396EFD158397D671`,`nodes_sampler.py` = `60EA92C84083436C307E300BCEAE996B521BC0F5EDBE30DBAD82EAED319F2483`)
- 走 ε-9 路線(兩 patch 疊加煙測)直接 verify 第 3 層是否解
- 若仍 Abort,接受 sage3 在 Wan 2.2 14B I2V 不 ready,sage2 baseline 維持

**累積投入**:ε-1a → ε-9 共 9 輪派工(每輪 15-30 min,加主視窗整合 + 中性 raise),~3-4 小時累積。Sage3 vs sage2 性能差異**未驗證**(因為從未跑通完整鏈),即使跑通收益不確定。Walking back 對齊投入產出比評估。

**(A) 路線實證落地**(2026-05-03,Wan 2.2 #3c candidate B 煙測):
- candidate B(Comfy-Org official subgraph,純 native ComfyUI core 路線)720×720 81f 4-step 整段 execution **217.7s**(=3.63 min)
- vs 合一檔 wrapper 路線 baseline 14.17 min/segment(850s)
- **快 ~3.9×**
- 對 finding 2「WanVideoWrapper sampler 0 個 `mm.load_models_gpu` 呼叫,完全脫離主框架」獲得實證 corroboration — wrapper 跳脫 ComfyUI 標準 ModelPatcher 框架是性能瓶頸 root cause
- Wan 2.2 #3c root cause 8 輪可結

### 19. supporting model state_dict key naming 跟檔名分離(2026-05-03)

**症狀**:Wan 2.2 #3c candidate B 煙測,把 ComfyUI core native 路線的 CLIPLoader widget patch 指向 Kijai 版 `umt5-xxl-enc-fp8_e4m3fn.safetensors`(同 base model UMT5-XXL,同 fp8 e4m3fn 量化精度,只差檔名命名)後 POST /prompt 通過 validation,但 execution 階段 CLIPTextEncode 撞 `NotImplementedError: Cannot copy out of meta tensor; no data!`(stack: `comfy/sd1_clip.py:213` → `comfy/ops.py:151` → `comfy/model_management.py:1287`)。

**原因**:Kijai 版 supporting model 的 state_dict key naming 跟 ComfyUI core loader 預期不對齊。Kijai 版 `umt5-xxl-enc-fp8_e4m3fn.safetensors` 專為 KJ wrapper 自家 `LoadWanVideoT5TextEncoder` 設計;ComfyUI core `CLIPLoader` 預期 Comfy-Org repackage 命名 `umt5_xxl_fp8_e4m3fn_scaled.safetensors`。檔名雖然檔名都標 fp8_e4m3fn,但 state_dict key naming 不同 → 部分 weight load fail 留在 meta tensor → forward 時 `cast_to_gathered` 在 meta 上 `copy_` 撞 NotImplementedError。

**解法**:下載 Comfy-Org repackage `umt5_xxl_fp8_e4m3fn_scaled.safetensors`(`Comfy-Org/Wan_2.1_ComfyUI_repackaged/split_files/text_encoders/`,SHA256 `c3355d30...651204f68`,6.27 GB),patch CLIPLoader widget 指 Comfy-Org 命名後跑通。

**紀律(規則 12 (B) cross-verify 教訓)**:supporting model patch 前 cross-verify state_dict 對齊性(safetensors header inspection 取 keys 比對 / ComfyUI 試 load 看 partial load warning),不靠檔名假設「同 base model 不同 repackage = 純命名差」。對應 SYSADMIN_BRIEFING.md 規則 12 (B)。

**未來注意**:Wan 2.x 系列 Kijai 版 vs Comfy-Org repackage **主模型 + Lightning LoRA 預期同樣分歧**(雖然 candidate B 直接用 Comfy-Org 4 檔沒實證 Kijai 主模型/LoRA 餵給 native loader 是否也撞);未來如要混用要先 cross-verify state_dict。

---

## 下一階段規劃

### 中國 Workflow 重建

已盤點 14+ 個中國 workflow,優先做 7 個全開源可重建的:

| 優先 | Workflow | 節點數 | 主要技術 |
|---|---|---|---|
| 1 | JoyCaption Beta1 反推 ✅ | 6 | 圖像反推 prompt(2026-04-26 完成) |
| 2 | Flux-fill OneReward 萬物移除 ✅ | 18 | FLUX.1 Fill + LoRA(2026-04-29 完成) |
| ~~3a~~ | ~~Kontext + ControlNet 改姿態(保留人物)~~ | ~~24~~ | ❌ **Deprecated** — Kontext ReferenceLatent 結構性壓 ControlNet,實證不適合此任務(2026-04-29) |
| 3a-v2 | Qwen Edit 2509 改姿態保留人物 | TBD | Qwen image-edit + consistence LoRA(規劃中) |
| 3b | FLUX + ControlNet 純 pose 生人物 ✅ | 20 | FLUX.1 Dev + Pro 2.0 + DWPose(2026-04-29 完成,作為 #3a 副產品) |
| 3c | Wan 2.2 T2V/I2V 720P 81幀 4步 ✅ | TBD | Wan 2.2 A14B + Lightx2v 4-step LoRA(2026-04-30 wrapper T2V 煙測 12.91 min;2026-05-03 native I2V candidate B 落地 217.7s,**(A) 路線結論:wrapper 是性能瓶頸 root cause,native 路線快 3.9×**,#3c root cause 8 輪可結)|
| 4 | Qwen3 TTS 聲音克隆 | 7 | Qwen3 TTS 1.7B + Whisper Large v3 |
| 5 | Qwen image 擴圖 | 28 | Qwen Image + Inpainting |
| 6 | 智能多角度生成 | 21 | Qwen-Image-Edit 2511 + 多角度 LoRA |
| 7 | Qwen3 TTS 聲音設計 | 14 | Qwen3 TTS + LLM 描述 |

### 中國 Workflow 私有節點對應規則

- `RH_*`(RunningHub)→ 雲端付費 API,直接刪掉改本地對應
- `Wuji*` → 中國商業節點,用標準 KSampler 替代
- `Dapao*` / `孤海*` / `TD*` → 找 GitHub 公開版或自寫等價邏輯
- `LayerUtility:*` → ✅ 開源(`chflame163/ComfyUI_LayerStyle` / `_Advance`),已裝

### 預估下載量

新階段約 100-150 GB:
- FLUX.1 Fill 12 GB
- Kontext 12 GB
- Qwen-Image-Edit 14 GB
- Qwen3 TTS 4 GB
- Whisper Large v3 3 GB
- Wan 2.2 系列 30 GB
- 其他模型若干

---

## 待辦

### 短期(下次回來)

(目前無短期待辦。下一步從「中國 Workflow 重建」優先 2-7 任選一個,Wayne 拍板。)

### 中期

1. 重建中國 workflow 路線:Flux-fill / Qwen3 TTS / Kontext + ControlNet 三選一開始
2. SageAttention issue #357 追蹤,等修復後重編享受 100% FP4 加速

### 長期

1. 跟 CrewAI(creative-pipeline 專案)整合,讓 agent 能呼叫 ComfyUI HTTP API
2. 建立 workflow 庫,跟 DaVinci Python API 對接做完整 AI 影像 pipeline

---

## 相關文件

- **`conflicts.md`**:Custom node 衝突主索引(反向節點查表 + 解決決策日誌 + 風險分級)
- **`conflicts-kjnodes.md`**:KJNodes 衝突明細(per-pack template,以後其他 pack 比照命名 `conflicts-{pack}.md`)
- **`conflicts-rgthree.md`**:rgthree-comfy 衝突明細(架構前已裝、catch-up 進入)
- **`sageattention-patches.md`**:🚨 6 個 PyTorch patches 完整紀錄,救命用
- **`../ai-models/local-models.md`**:本地模型分工(ComfyUI / Ollama / 雲端 API)
- **`../davinci/pipeline.md`**:後段 DaVinci 整合規劃
- **`../reinstall-manifest.md`**:重灌時的還原步驟
- **`../tools/README.md`**:system-setup 周邊腳本工具(含 png_to_ico.py)

---

**最後更新**:2026-05-03
