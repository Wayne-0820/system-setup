# ComfyUI Workflows 完整描述

> 已建立的 7 個 workflow 完整描述 + 設計理由 + 使用場景。
>
> 存放路徑:`D:\Work\system-setup\comfyui-workflows\`
>
> 命名風格:**用途定位派**(中文,看名字就知道幹嘛用)
>
> 最後同步:2026-04-26

---

## Workflow 索引

### 圖像生成系列(5 個)

| 名稱 | 模型 | 步數 | 速度 | 用途 |
|---|---|---|---|---|
| `SDXL_1.0_基準參考.json` | SDXL 1.0 | 20 | ~10 秒 | 對比基準 |
| `Klein_4B_快速草稿_4步.json` | Klein 4B NVFP4 | 4 | 1.3 秒 | 快速試 prompt |
| `Klein_4B_4K大圖出稿.json` | Klein 4B + UltraSharp | 4 + 升頻 | ~5 秒 | 4K 大圖輸出 |
| `Klein_9B_Base_頂級定稿_20步.json` | Klein 9B Base + Qwen3 8B | 20 | 41 秒 | 最終定稿(SOTA) |
| `flux2_klein_9b_t2i_official.json` | 官方範本(38.1 KB) | - | - | 參考用 |

### 圖像反推系列(2 個)

| 名稱 | 用途 | 節點數 | 翻譯 |
|---|---|---|---|
| `JoyCaption_Beta1_快速反推.json` | 看圖、隨手反推 | 6 | ✅ 接 GoogleTranslate(英→中) |
| `JoyCaption_Beta1_訓練反推.json` | LoRA 訓練資料集 | 6 | ❌ 純英文 |

---

## 圖像生成 Workflow 詳述

### 1. SDXL_1.0_基準參考

**檔案**:`SDXL_1.0_基準參考.json`

**用途**:對比基準。當你不知道某張圖用 Klein / FLUX 算出來夠不夠好,跑 SDXL 1.0 看看 2023 年標竿水準是什麼樣子。

**模型組合**:
- Checkpoint:`sd_xl_base_1.0.safetensors`(內建 CLIP-L / CLIP-G + VAE)
- 不需要外部 CLIP 或 VAE

**節點結構**(標準):
- CheckpointLoaderSimple
- CLIPTextEncode × 2(positive + negative)
- KSampler(20 步, cfg=7, dpmpp_2m, karras)
- VAEDecode
- SaveImage

**參數**:
- Sampler:`dpmpp_2m`
- Scheduler:`karras`
- Steps:20
- CFG:7
- Resolution:1024×1024

**速度**:~10 秒/張(5090 Laptop)

**VRAM**:~7 GB

---

### 2. Klein_4B_快速草稿_4步

**檔案**:`Klein_4B_快速草稿_4步.json`

**用途**:**快速試 prompt 神器**。1.3 秒生成一張,用來:
- 快速迭代 prompt 寫法
- 試構圖、配色、人物動作
- 確認方向後,複製 prompt 跑 9B Base 出最終稿

**模型組合**:
- UNET:`flux-2-klein-4b-nvfp4.safetensors`(2.29 GB)
- CLIP:**`qwen_3_4b_fp4_flux2.safetensors`(維度 7680)** ← 必須是 4B!
- VAE:`flux2-vae.safetensors`

**節點結構**(分離式):
- UNETLoader
- CLIPLoader
- VAELoader
- CLIPTextEncode
- Flux2Scheduler / EmptyFlux2LatentImage
- KSamplerSelect / RandomNoise / SamplerCustomAdvanced
- VAEDecode
- SaveImage

**參數**:
- Steps:4
- CFG:1(Klein distilled 系列特性)
- Sampler:euler / dpm
- Resolution:1024×1024

**速度**:1.3 秒/張(這是真的快)

**VRAM**:~6 GB

**關鍵 Mapping 警告**:
- Klein 4B **必須**配 Qwen3 4B FP4
- 配錯成 8B → `mat1 mat2 shapes cannot be multiplied`(維度衝突)

---

### 3. Klein_4B_4K大圖出稿

**檔案**:`Klein_4B_4K大圖出稿.json`

**用途**:Klein 4B 跑出 1024 後,接 UltraSharp 升頻到 4096×4096 大圖輸出。用於:
- 印刷 / 大尺寸顯示
- 細節保留要求高的場景(草稿 + 升頻 比直接生 4K 快 10 倍)

**模型組合**:
- 同 Klein 4B 快速草稿
- 升頻:`4x-UltraSharp.pth`(67 MB)

**節點結構**:
1. Klein 4B 完整生成流(同上)→ 1024 圖
2. ImageUpscaleWithModel(UltraSharp 4×) → 4096 圖
3. SaveImage(自動命名 `_upscaled`)

**速度**:
- 生圖:1.3 秒
- 升頻:3-4 秒
- **總計約 5 秒**

**VRAM**:~7 GB(升頻不額外吃太多)

---

### 4. Klein_9B_Base_頂級定稿_20步

**檔案**:`Klein_9B_Base_頂級定稿_20步.json`

**用途**:**SOTA 頂級定稿**。當 prompt 已經試好(用 Klein 4B 確認),最終出片用這個。

**模型組合**:
- UNET:`flux-2-klein-base-9b-fp8.safetensors`(~9 GB)
- CLIP:**`qwen_3_8b_fp8mixed.safetensors`(維度 12288)** ← 必須是 8B!
- VAE:**`full_encoder_small_decoder.safetensors`(~250 MB,9B 專用)**

**Workflow 架構特性**:**ComfyUI Subgraph 格式**(2025+ 新標準):
- 整個生成邏輯封裝在一個 Subgraph 節點裡
- 雙擊 Subgraph 節點才看得到內部
- 內部節點:UNETLoader / CLIPLoader / VAELoader / Flux2Scheduler / CFGGuider / KSamplerSelect / EmptyFlux2LatentImage / RandomNoise / SamplerCustomAdvanced

**參數**:
- Steps:20
- CFG:5(Base 版才能用真實 CFG,distilled 版只能用 1)
- Sampler:euler / dpm
- Resolution:1024×1024

**速度**:**41 秒/張**(開 SageAttention,未開 ~50 秒)

**VRAM**:**20,400 MiB**(逼近 24 GB 上限)

**警告**:
- 跑這個 workflow 時**不要同時跑 Ollama qwen3:32b**,會爆 VRAM
- 4K 升頻時 VRAM 高峰到 **20,962 MiB**,只剩 3.5 GB 緩衝

---

### 5. flux2_klein_9b_t2i_official

**檔案**:`flux2_klein_9b_t2i_official.json`(38.1 KB)

**用途**:**官方 ComfyUI Klein 9B t2i 範本**。保留下來當參考,排查問題時對照官方寫法。

**注意**:這個是純官方範本,可能跟你實際使用的 Klein_9B_Base_頂級定稿_20步.json 在參數上有出入。**不要直接拿來生產用**,當 reference 即可。

---

## 圖像反推 Workflow 詳述

兩個都用 **JoyCaption Beta1** 模型(15.81 GB,在 `ComfyUI\models\LLavacheckpoints\llama-joycaption-beta-one-hf-llava\`)。

### 6. JoyCaption_Beta1_快速反推

**檔案**:`JoyCaption_Beta1_快速反推.json`

**用途**:看圖、隨手反推內容。
- 收到一張圖,想知道它畫了什麼 → 跑這個
- 用中英對照看更直觀

**節點結構**(6 節點):
1. `LoadImage`(讀圖)
2. `LayerUtility: Load JoyCaption Beta One Model (Advance)`(載入模型)
3. `LayerUtility: JoyCaption Beta One Extra Options (Advance)`(選項)
4. `LayerUtility: JoyCaption Beta One (Advance)`(主推理)
5. `Show Text 🐍`(英文輸出)
6. `GoogleTranslateTextNode → Show Text 🐍`(中文輸出)

**主推理參數**:
- `caption_type`: Descriptive
- `caption_length`: any
- `max_new_tokens`: 512
- `top_p`: 0.90
- `top_k`: 0
- `temperature`: 0.60

**Extra Options(4 個啟用)**:
- `exclude_image_resolution`
- `do_not_include_artist_name_or_title`
- `avoid_meta_descriptive_phrases`
- `exclude_sexual`

**翻譯設定**:
- `from_translate`: auto
- `to_translate`: zh-TW

**速度**:
- 第一次推理:10-20 秒(載入 5GB 進 VRAM)
- 同 session 後續:幾秒

**VRAM**:~5 GB(nf4 量化)

**注意**:Google translate 偶爾被 rate limit,這時切 `DeepTranslatorTextNode` 改用 MyMemory backend。

---

### 7. JoyCaption_Beta1_訓練反推

**檔案**:`JoyCaption_Beta1_訓練反推.json`

**用途**:**LoRA 訓練資料集反推**。產出完整 SD prompt(含 lighting / camera / composition),給訓練腳本當 caption。

**跟快速反推的差別**:
- **不接翻譯節點**(訓練資料集要保持英文)
- **更多 Extra Options**(11 個 vs 快速版 4 個),產出更完整的 prompt

**節點結構**(6 節點):
1. `LoadImage`
2. `LayerUtility: Load JoyCaption Beta One Model (Advance)`
3. `LayerUtility: JoyCaption Beta One Extra Options (Advance)`
4. `LayerUtility: JoyCaption Beta One (Advance)`
5. `Show Text 🐍`(純英文輸出)

**主推理參數**:同快速反推

**Extra Options(11 個啟用)**:
- `exclude_image_resolution`
- `do_not_include_artist_name_or_title`
- `avoid_meta_descriptive_phrases`
- `do_not_use_ambiguous_language`
- `include_lighting`
- `specify_lighting_sources`
- `include_camera_angle`
- `include_camera_shot_type`
- `include_camera_vantage_height`
- `specify_depth_field`
- `include_composition_style`

**輸出範例**(訓練版):
```
A photorealistic medium shot of a woman with red hair sitting in a cafe.
Soft natural light from a window on her left, creating a gentle rim lighting on her hair.
Shallow depth of field with the background blurred. Eye-level camera angle.
Composition uses rule of thirds with subject on the right third.
```

**規則**:訓練版**絕對不接翻譯節點**,輸出保持英文。Caption 的英文 prompt 直接餵給 SD 訓練流程。

---

## Workflow 設計通用原則

### 1. 命名:用途定位派

不用 `wf_001.json` / `experiment_v3.json` 這種看不出用途的命名。
用「主模型 + 用途 + 關鍵參數」例如:
- ✅ `Klein_4B_快速草稿_4步.json`
- ✅ `Klein_9B_Base_頂級定稿_20步.json`
- ❌ `klein_workflow_v2.json`(看不出用什麼模型、做什麼)

### 2. 一個 workflow 一個職責

不要把「快速試 prompt」和「4K 大圖出稿」塞進同一個 workflow 用 switch 切換。
分開兩個檔案:
- 快速版只生 1024
- 4K 版接升頻

職責單一,維護簡單,不會誤跑。

### 3. Workflow 跟模型 mapping 寫死

Klein 4B 配 Qwen3 4B、Klein 9B 配 Qwen3 8B,這個 mapping **不要做動態切換**。
直接在 workflow 裡寫死。混用會炸,根本沒有好處。

### 4. 輸出位置統一

所有 workflow 用 ComfyUI 預設 SaveImage,輸出走 `--output-directory` 指定的 `D:\Media\AI_Raw\ComfyUI_Output\`。
不要在某個 workflow 自訂特殊輸出路徑。

---

## 待建立 Workflow

### 中國 Workflow 重建(優先 7 個)

| 優先 | Workflow | 節點數 | 主要技術 |
|---|---|---|---|
| 1 | JoyCaption Beta1 反推 ✅ | 6 | 已完成 |
| 2 | Flux-fill OneReward 萬物移除 | 18 | FLUX.1 Fill + LoRA |
| 3 | Kontext + ControlNet 姿態改變 | 24 | FLUX Kontext + ControlNet |
| 4 | Qwen3 TTS 聲音克隆 | 7 | Qwen3 TTS 1.7B + Whisper Large v3 |
| 5 | Qwen image 擴圖 | 28 | Qwen Image + Inpainting |
| 6 | 智能多角度生成 | 21 | Qwen-Image-Edit 2511 + 多角度 LoRA |
| 7 | Qwen3 TTS 聲音設計 | 14 | Qwen3 TTS + LLM 描述 |

### 私有節點對應規則(別忘了)

- `RH_*`(RunningHub)→ 雲端付費,刪掉改本地
- `Wuji*` → 用標準 KSampler 替代
- `Dapao*` / `孤海*` / `TD*` → 找 GitHub 公開版或自寫
- `LayerUtility:*` → ✅ 已開源,已裝

---

## 相關文件

- `setup.md` — ComfyUI 完整配置、模型清單、踩坑
- `sageattention-patches.md` — 加速 17% 的 6 個 patches
- `huggingface-download-tricks.md` — 下載這些 workflow 用到的模型時的繞道技巧
- `../ai-models/local-models.md` — 模型分工、VRAM 限制

---

**最後更新**:2026-04-26
