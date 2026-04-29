# ComfyUI Workflows 完整描述

> 已建立的 7 個 workflow 完整描述 + 設計理由 + 使用場景。
>
> 存放路徑:`D:\Work\system-setup\comfyui-workflows\`
>
> 命名風格:**用途定位派**(中文,看名字就知道幹嘛用)
>
> 最後同步:2026-04-29

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

### 圖像編輯 / 條件控制系列(3 個)

| 名稱 | 模型 | 步數 | 速度 | VRAM | 用途 |
|---|---|---|---|---|---|
| `Flux-fill_OneReward_萬物移除_10步.json` | FLUX.1 Fill OneReward fp8 + Turbo-Alpha LoRA + Removal LoRA | 10 | 93.68 秒 | 24,088 MB | 圖像物品移除(inpaint) |
| `FLUX_ControlNet_純pose生人物_20步.json` | FLUX.1 Dev fp16 + ControlNet Union Pro 2.0 + DWPose | 20 | 78 秒 cold / 26 秒 warm | 23,793 MiB | 從 pose 骨架圖生新人物 |
| `Qwen_Edit_2509_保留人物改姿勢_8步.json` | Qwen Image Edit 2509 fp8 + Lightning 8steps + consistence_edit_v2 + Qwen 2.5 VL 7B fp8 | 8 | 92.8 秒 cold(首次含載 5 model)| 23,832 MiB | 保留人物特徵 + 改姿勢 |

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

## 圖像編輯 Workflow 詳述

### 8. Flux-fill_OneReward_萬物移除_10步

**檔案**:`Flux-fill_OneReward_萬物移除_10步.json`

**用途**:**圖像物品移除(inpaint)**。給一張圖 + 畫 mask 標出要移除的物品,AI 根據周圍環境推斷該位置應該長什麼樣子,把物品消掉。

**模型組合**:
- UNET:`flux.1-fill-dev-OneReward-fp8.safetensors`(11.085 GB,FLUX.1 Fill 系列 + ByteDance OneReward 微調)
- LoRA(加速):`Flux-Turbo-Alpha.safetensors`(0.646 GB,讓 FLUX 4-10 步出圖)
- LoRA(移除):`removal_timestep_alpha-2-1740.safetensors`(0.086 GB,lrzjason ObjectRemovalFluxFill v2)
- CLIP:`clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors`(FLUX 標準雙編碼器)
- VAE:`ae.safetensors`(FLUX 配套)

**節點結構**(18 節點):
- LoadImage(右鍵 MaskEditor 畫 mask)
- DualCLIPLoader / UNETLoader / VAELoader
- LoraLoaderModelOnly × 2(疊兩個 LoRA)
- DifferentialDiffusion + InpaintModelConditioning
- LayerUtility: ImageScaleByAspectRatio V2(尺寸對齊)
- **GrowMaskWithBlur**(KJNodes,等價 WAS Mask Fill Holes,參數 `expand=0, blur_radius=0, fill_holes=True`)
- CLIPTextEncode + ConditioningZeroOut + FluxGuidance
- KSampler(10 步,euler / beta scheduler,cfg=1)
- VAEDecode
- ImageAndMaskPreview + Image Comparer (rgthree)
- SaveImage

**參數**:
- Steps:10
- CFG:1(LoRA 加速搭配)
- Sampler:euler
- Scheduler:beta
- FluxGuidance:35

**速度**:**93.68 秒/張**(實測,有畫 mask 的真實跑通)

**VRAM**:**24,088 MB 高峰**(逼近 5090 Laptop 24 GB 物理上限)

**警告**:
- 跑這個 workflow **必須先停掉 Ollama**,否則直接爆 VRAM
- 不要同時跑其他 GPU 任務(包括 4K 升頻 / 其他 ComfyUI 視窗)
- mask 必須畫 — 沒畫 mask 直接按 Run 會跑出無意義圖

**為什麼用 KJNodes `GrowMaskWithBlur` 替代 WAS `Mask Fill Holes`**:
原 RunningHub workflow 用 `Mask Fill Holes`,該節點屬於 `was-node-suite-comfyui` pack;但該 pack 2025-06 已被作者 archived(GitHub 上游不再維護)。為了單一節點裝整 archived pack 維護負擔不對等,改用 KJNodes(已裝)等價節點 `GrowMaskWithBlur`(設 `expand=0, blur_radius=0, fill_holes=True`,底層都用 `scipy.ndimage.binary_fill_holes`,行為等價)。詳見 `conflicts.md` 的「替代節點對照」段。

**測試圖建議**:
有縫隙的物品(鏤空椅子 / 戒指 / 眼鏡 / 網狀購物袋)能驗到 `fill_holes` 是否真的等價;實心物品(水瓶 / 紙箱)只測到 inpaint 主流程,fill_holes 行為驗不到。

---

### 9. FLUX_ControlNet_純pose生人物_20步

**檔案**:`FLUX_ControlNet_純pose生人物_20步.json`

**用途**:**從 pose 骨架圖生新人物**。給一張 pose 參考圖(從照片自動抽骨架,或直接給骨架圖),AI 生出擺著該姿勢的全新人物。
不保留特定人物視覺特徵 — 想要「保留人物 + 改姿勢」走 #3a-v2(Qwen Edit,規劃中)。

**模型組合**:
- UNET:`flux1-dev.safetensors`(BFL fp16 全精度,UNETLoader weight_dtype=fp8_e4m3fn 載入轉 fp8 省 VRAM)
- ControlNet:`FLUX.1-dev-ControlNet-Union-Pro-2.0\diffusion_pytorch_model.safetensors`(Shakker-Labs)
- Pose preprocessor:`AIO_Preprocessor` (`OpenposePreprocessor` mode)
- CLIP:`clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors`
- VAE:`ae.safetensors`

**節點結構**(20 節點):
- LoadImage(pose 參考圖)
- DualCLIPLoader / UNETLoader / VAELoader / ControlNetLoader
- AIO_Preprocessor(抽 pose 骨架)
- CLIPTextEncode(prompt 描述新人物)
- ControlNetApplySD3(strength=1.5, start=0, end=1.0,**未 tune**,跑得通即可)
- KSampler(20 步, fp8_e4m3fn, denoise=1)
- VAEDecode
- ImageConcanate(拼接 pose 骨架 + 生成結果做對照)
- SaveImage × 2(KSampler 純結果 + 拼接對比)

**參數**:
- Steps:20
- Sampler:euler / scheduler simple
- Resolution:見 EmptySD3LatentImage(隨 pose 圖比例)

**速度**:
- Cold(含 OpenposePreprocessor 第一次跑下載 `lllyasviel/Annotators/{body_pose,hand_pose,facenet}.pth`):**78.77 秒**
- Warm(連跑):**26.24 秒**

**VRAM**:**23,793 MiB**(逼近 24 GB 上限,剩 783 MB 緩衝)

**警告**:
- 跑這個 workflow **必須先停 Ollama**,否則直接爆 VRAM
- ControlNet 模型 path 在 ComfyUI Windows 內部用 backslash,workflow JSON 從 RunningHub 載來常用 forward slash → GUI 載入會標紅,詳 setup.md 踩坑 #11
- 第一次跑 OpenposePreprocessor 會自動從 HF `lllyasviel/Annotators` 下載 ~200 MB 模型權重

**為什麼是 #3a 副產品而非獨立規劃**:Workflow #3 原任務是「Kontext + ControlNet 改姿態保留人物」(#3a),執行端做時拆出 #3b 作為「沒 Kontext 的純 pose 生人物」對照組驗證 ControlNet 機制本身有效。結果 #3a 因 Kontext ReferenceLatent 結構性壓 ControlNet 失敗(deprecated),#3b 反而獨立可用,留下成為實際交付。「保留人物 + 改姿勢」需求由 #3a-v2(Qwen Edit 路線)接棒。

**自動化提交**:可用 `tools/workflow_submit.py` 跳過 GUI 互動,直接 POST `/prompt`(注意 ControlNet path separator 雷需先 patch,詳 setup.md 踩坑 #11)。

---

### 10. Qwen_Edit_2509_保留人物改姿勢_8步

**檔案**:`Qwen_Edit_2509_保留人物改姿勢_8步.json`

**用途**:**保留人物特徵(臉 / 髮 / 衣物 / 場景)+ 改姿勢**。輸入兩張圖:
- 角色圖(node 15 LoadImage,本輪實證 `boa_cosplay.jpg`)→ 走 VAEEncode → KSampler latent_image,作為「保留」基準
- pose 參考圖(node 40 LoadImage,本輪 `boa_figure.png`)→ AIO_Preprocessor (`OpenposePreprocessor` mode) 抽骨架 → 作為「改姿勢」目標

跟 #3b(純 pose 生人物)的差別:#3b 不保留特定人物視覺特徵,#3a-v2 用 model-native 編輯(Qwen Edit 2509)+ consistence_edit LoRA 保留度大幅提升。

**模型組合**:
- UNET:`qwen_image_edit_2509_fp8_e4m3fn.safetensors`(19.03 GB)
- CLIP / Text Encoder:`qwen_2.5_vl_7b_fp8_scaled.safetensors`(8.74 GB,**注意落 `clip\` 子目錄不是 `text_encoders\`**,詳 setup.md text encoders 段)
- VAE:`qwen_image_vae.safetensors`(236 MB)
- LoRA × 2(C 方案 unbypass):
  - `qwen-image\Qwen-Image-Lightning-8steps-V1.1-bf16.safetensors`(0.791 GB,strength=1)— 8 步加速
  - `consistence_edit_v2.safetensors`(0.571 GB,strength=0.4)— 保留人物核心
- Custom node pack:`Comfyui-QwenEditUtils`(裝但 KSampler 不真正消費,詳「C 方案不動 link 設計」段)

**節點結構**(22 節點):
- LoadImage × 2(角色 + pose 參考)
- LayerUtility: ImageScaleByAspectRatio V2 × 2(尺寸對齊)
- AIO_Preprocessor(OpenposePreprocessor mode)+ PreviewImage
- ImageConcatMulti + ImageStitch(對照圖拼接)
- UNETLoader / CLIPLoader / VAELoader
- LoraLoaderModelOnly × 2(Lightning + consistence_edit,**JSON 預設 mode=4 bypass,C 方案 patch 為 0 啟用**)
- VAEEncode(角色圖 latent)
- **TextEncodeQwenImageEditPlus**(node 45,**ComfyUI 0.3.x 內建**,KSampler positive 走這條 — **不是** lrzjason 客製版)
- TextEncodeQwenImageEditPlus_lrzjason(node 44,JSON 預設 mode=4,C 方案 unbypass 但下游送 ConditioningZeroOut 廢棄,事實上沒被 KSampler 消費)
- PrimitiveStringMultiline(node 35,**comfy-core 內建,替代 was-node-suite-comfyui `Text Multiline`**,prompt 來源)
- ConditioningZeroOut(negative 接 zero)
- KSampler(8 步,euler,simple scheduler,cfg=2.5,denoise=1)
- VAEDecode
- SaveImage × 2(主圖 `Qwen_Edit_2509_*.png` / 對照圖 `ComfyUI_*.png`)

**參數**:
- Steps:**8**(JSON 預設 20,C 方案 patch)
- CFG:2.5(JSON 預設,Lightning distilled 一般推 1.0,本輪未 tune,後續評估)
- Sampler:euler
- Scheduler:**simple**(JSON 預設 beta57,C 方案改 simple 對齊 lightx2v 上游 Lightning 8 步推薦值)
- Denoise:1
- Resolution:見 LayerUtility:ImageScaleByAspectRatio V2(scale_to_length=1024 longest)

**速度**:
- Cold(首次含載 5 model,~28 GB 進 VRAM):**92.8 秒**
- Warm(連跑同 model)預估:30-50 秒(尚未實證,跟 Klein 9B Base 41 秒同量級)

**VRAM**:**23,832 MiB 高峰**(逼近 24 GB 上限,剩 168 MB 緩衝)

**警告**:
- 跑這個 workflow **必須先停 Ollama / DaVinci 等 GPU 任務**,否則直接爆 VRAM
- LoraLoaderModelOnly 子目錄 LoRA path 在 ComfyUI Windows 內部用 backslash,**workflow JSON 從網路載來常用 forward slash → server validation `value_not_in_list` → workflow 跑廢**(本輪實證,詳 setup.md 踩坑 #11 LoRA 補強段)
- 第一次跑 OpenposePreprocessor 會自動從 HF `lllyasviel/Annotators` 下載 ~200 MB 模型權重(同 #3b)

**C 方案不動 link 設計**(主窗口 2026-04-29 拍板):

派工模板 v1 目標寫「Lightning 8 步 + Consistence Edit v2 + lrzjason」,但 JSON 預設三節點(node 4 / 34 / 44)mode=4(bypass)+ KSampler positive 接 node 45(內建)而非 node 44(lrzjason)。執行端揭露後攤 A(字面跑廢)/ B(動 link 重接 KSampler positive 到 lrzjason)/ C(unbypass 三節點但不動 link)三選項。

主窗口拍 C 理由:
- A 跑普通 Qwen Edit 20 步,雙 LoRA / lrzjason 三大關鍵元件全沒生效,handoff §2.2 估算 50-65% 達標失效
- B 動 link 是結構性 patch,派工 patch 表沒列,風險高
- C 折衷:雙 LoRA 載入(影響 KSampler model)生效 + 8 步生效;lrzjason 雖 enable 但下游送 ConditioningZeroOut 廢棄,**事實上 #3a-v2 跑通靠的是 ComfyUI 內建 `TextEncodeQwenImageEditPlus` + 雙 LoRA**,QwenEditUtils 在本輪沒被 KSampler 真正消費

C 方案的代價清單:
1. lrzjason 客製 prompt instruction(JSON line 1130,~250 字英文)沒生效 — 結果 prompt 走純 Text Multiline 文字(`让image1中的模特改变为image2的姿势,保持人物一致性,保持背景一致性。`)
2. node 44 lrzjason 載入後算力浪費(輸出去 ConditioningZeroOut 廢棄)
3. 命名「Qwen_Edit_2509_保留人物改姿勢_**8步**」對齊 8 步生效,但 lrzjason 沒生效這層 nuance 不在檔名

未來 #3a-v2 tune 候選:
- 改 B 方案重接 link node 45 → node 44(若品質不夠)
- 跑 cfg=1.0(對齊 Lightning distilled 推薦值)
- 把 prompt 拓成多行多細節(內建 TextEncodeQwenImageEditPlus 對 prompt 細節容量比 Text Multiline 字串 widget 大)

**Text Multiline 替代節點選擇**(2026-04-29 Wayne 拍 a):

原 JSON node 35 `Text Multiline` 來自 was-node-suite-comfyui(archived 2025-06,本機決策不裝)。執行端 verify 三來源:
- a. ComfyUI 內建 `PrimitiveStringMultiline`(`comfy_extras.nodes_primitive`)— 純 STRING multiline → STRING output passthrough
- b. KJNodes `StringConstantMultiline` — 多 `strip_newlines=true` 預設行為差異
- c. rgthree-comfy — 無對等純文字節點

Wayne 拍 a(comfy-core 內建,無 pack 依賴 / 行為跟 was 完全等價 / 未來多行 prompt 不會被 strip)。詳 conflicts.md 替代節點對照表 +1 row。

**自動化提交**:用 `tools/workflow_submit.py` POST `/prompt`(本輪實證跑通)。**注意 LoRA path separator 雷必須先 patch JSON 為 backslash 版本**(setup.md 踩坑 #11 LoRA 補強段)+ **`workflow_submit.py` 不攔 node_errors 非空缺陷**(server validation 部分失敗仍走 fallback 跑廢圖,需手動看 response 確認 `node_errors=={}`,詳 tools/README.md / 階段 2 升級候選)。

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

| 優先 | Workflow | 節點數 | 主要技術 | 狀態 |
|---|---|---|---|---|
| 1 | JoyCaption Beta1 反推 | 6 | 圖像反推 prompt | ✅ 2026-04-26 |
| 2 | Flux-fill OneReward 萬物移除 | 18 | FLUX.1 Fill + LoRA | ✅ 2026-04-29 |
| ~~3a~~ | ~~Kontext + ControlNet 改姿態(保留人物)~~ | ~~24~~ | ❌ Kontext 結構性不適合 | ❌ Deprecated 2026-04-29 |
| 3a-v2 | Qwen Edit 2509 改姿態保留人物 | 22 | Qwen image-edit + Lightning 8 步 + consistence LoRA + 內建 TextEncodeQwenImageEditPlus | ✅ 2026-04-29 |
| 3b | FLUX + ControlNet 純 pose 生人物 | 20 | FLUX.1 Dev + Pro 2.0 + DWPose | ✅ 2026-04-29(#3a 副產品) |
| 4 | Qwen3 TTS 聲音克隆 | 7 | Qwen3 TTS 1.7B + Whisper Large v3 | 待建 |
| 5 | Qwen image 擴圖 | 28 | Qwen Image + Inpainting | 待建 |
| 6 | 智能多角度生成 | 21 | Qwen-Image-Edit 2511 + 多角度 LoRA | 待建 |
| 7 | Qwen3 TTS 聲音設計 | 14 | Qwen3 TTS + LLM 描述 | 待建 |

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

**最後更新**:2026-04-29
