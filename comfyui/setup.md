# ComfyUI 配置指南

> **這份文件反映實際運行狀態**(不是規劃)。
>
> 最後同步:2026-04-29
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
| `Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 I2V A14B HIGH noise(fp8 e4m3fn scaled,Kijai) |
| `Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors` | 14.0 GB | Wan 2.2 I2V A14B LOW noise(fp8 e4m3fn scaled,Kijai) |

### CLIP / Text Encoders(`D:\Models\diffusion\clip\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `qwen_3_4b_fp4_flux2.safetensors` | 3.85 GB | 給 Klein 4B 用(Qwen3 4B FP4,維度 7680) |
| `qwen_3_8b_fp8mixed.safetensors` | 8.07 GB | 給 Klein 9B 用(Qwen3 8B FP8 mixed,維度 12288) |
| `clip_l.safetensors` | 0.229 GB | FLUX 配套 CLIP-L(Workflow #2 / 未來 FLUX 系列共用) |
| `t5xxl_fp8_e4m3fn.safetensors` | 4.558 GB | FLUX 配套 T5-XXL fp8(Workflow #2 / 未來 FLUX 系列共用) |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | 8.74 GB | Qwen 2.5 VL 7B(fp8 scaled,Workflow #3a-v2 / 未來 Qwen Edit / Qwen Image 系列共用)— **注意路徑紀律:Comfy-Org repo URL 標 `split_files/text_encoders/`,本機 yaml 只映射 `clip:`,規範一律落 `clip\` 子目錄(2026-04-29 派工 v1 第 6 個 bug 訂正)** |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | 6.27 GB | Wan 2.2 text encoder(UMT5-XXL fp8 e4m3fn,Kijai/WanVideo_comfy) |

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

**最後更新**:2026-04-29
