# ComfyUI 配置指南

> **這份文件反映實際運行狀態**(不是規劃)。
>
> 最後同步:2026-04-26
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

ComfyUI 透過 `extra_model_paths.yaml` 讀 `D:\Models\sd\`(避免重複下載):

```
D:\Models\sd\                # 模型主目錄
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

未來可建桌面捷徑指向此 BAT,並自訂 .ico 圖示。

---

## 已下載模型清單

### Checkpoints(`D:\Models\sd\checkpoints\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `sd_xl_base_1.0.safetensors` | 6.46 GB | SDXL 1.0 基準參考(2023 標竿) |
| `flux1-dev-fp8.safetensors` | 16.06 GB | FLUX.1 Dev all-in-one |
| `SUPIR-v0Q.ckpt` | 4.96 GB | SUPIR 商業級升頻(custom node 已裝,workflow 未搭) |

### Diffusion Models(`D:\Models\sd\diffusion_models\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `flux-2-klein-4b-nvfp4.safetensors` | 2.29 GB | Klein 4B 快速草稿(4 步) |
| `flux-2-klein-9b-fp8.safetensors` | 8.79 GB | Klein 9B distilled(4 步) |
| `flux-2-klein-base-9b-fp8.safetensors` | ~9 GB | Klein 9B Base(20 步,SOTA) |

### CLIP / Text Encoders(`D:\Models\sd\clip\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `qwen_3_4b_fp4_flux2.safetensors` | 3.85 GB | 給 Klein 4B 用(Qwen3 4B FP4,維度 7680) |
| `qwen_3_8b_fp8mixed.safetensors` | 8.07 GB | 給 Klein 9B 用(Qwen3 8B FP8 mixed,維度 12288) |

### VAE(`D:\Models\sd\vae\`)

| 檔名 | 大小 | 用途 |
|---|---|---|
| `flux2-vae.safetensors` | ? | 給 4B / FLUX.1 用 |
| `full_encoder_small_decoder.safetensors` | ~250 MB | 給 Klein 9B 用(專用) |

### Upscale(`D:\Models\sd\upscale_models\`)

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
└── websocket_image_save.py            # 內建
```

### 安裝方式統一規則

**透過 ComfyUI Manager 介面安裝**,不要手動 `pip install`。
Manager 會自動處理:
- Git clone repo
- 處理 requirements.txt
- 第一次啟動時 pip 安裝依賴

**例外**:某些節點需要修復 opencv 衝突等,看具體節點文件。

### AlekPet 自動 pip 安裝(已處理)

第一次啟用 GoogleTranslateTextNode 時,會自動裝:
- `googletrans`
- `deep-translator`

走 Google 公開 endpoint,**無需 API key**,但偶爾會被 rate limit(這時切 DeepTranslatorTextNode 用 MyMemory)。

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

### 8. opencv 衝突(LayerStyle guidedFilter,2026-04-26 已修)

**症狀**:LayerStyle 的 guidedFilter 節點報錯
**解法**:卸 `opencv-python` + `opencv-python-headless`,純裝 `opencv-contrib-python` 4.13.0

```powershell
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip uninstall opencv-python opencv-python-headless -y
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip install opencv-contrib-python==4.13.0
```

---

## 下一階段規劃

### 中國 Workflow 重建

已盤點 14+ 個中國 workflow,優先做 7 個全開源可重建的:

| 優先 | Workflow | 節點數 | 主要技術 |
|---|---|---|---|
| 1 | JoyCaption Beta1 反推(進行中)✅ | 6 | 圖像反推 prompt |
| 2 | Flux-fill OneReward 萬物移除 | 18 | FLUX.1 Fill + LoRA |
| 3 | Kontext + ControlNet 姿態改變 | 24 | FLUX Kontext + ControlNet |
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

1. 用現有 workflow 生成 ComfyUI 啟動圖示底圖
2. 轉 `.ico` 多尺寸(16/32/48/256)
3. 套用到 `start_comfyui.bat` 桌面捷徑

### 中期

1. 重建中國 workflow 路線:Flux-fill / Qwen3 TTS / Kontext + ControlNet 三選一開始
2. SageAttention issue #357 追蹤,等修復後重編享受 100% FP4 加速

### 長期

1. 跟 CrewAI(creative-pipeline 專案)整合,讓 agent 能呼叫 ComfyUI HTTP API
2. 建立 workflow 庫,跟 DaVinci Python API 對接做完整 AI 影像 pipeline

---

## 相關文件

- **`sageattention-patches.md`**:🚨 6 個 PyTorch patches 完整紀錄,救命用
- **`local-models.md`**:本地模型分工(ComfyUI / Ollama / 雲端 API)
- **`davinci-pipeline.md`**:後段 DaVinci 整合規劃
- **`reinstall-manifest.md`**:重灌時的還原步驟

---

**最後更新**:2026-04-26
