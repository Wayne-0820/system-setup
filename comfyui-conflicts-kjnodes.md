# ComfyUI-KJNodes 衝突明細

> Pack:**ComfyUI-KJNodes** by kijai
> 版本:v1.3.9
> 安裝日:2026-04-27
> 狀態:✅ active
>
> 主索引:[`comfyui-conflicts.md`](./comfyui-conflicts.md)
> 風險分級標準見主索引。
>
> 最後更新:2026-04-27

---

## TL;DR

| 結論 | 說明 |
|---|---|
| **裝這個 pack 的原因** | `Flux-fill OneReward 萬物移除` workflow 需要 `ImageAndMaskPreview` 節點 |
| **Manager 標示衝突數** | 61 |
| **裝了沒問題** | 61 衝突中 57 個來自 `ComfyUI_Swwan`(疑似 fork / 抄襲的冷門 pack,不會裝) |
| **真正要記住的 4 個 active 衝突** | `AudioConcatenate` / `Sleep` / `SplitImageChannels` / `WanVideoNAG`(已 promote 到主索引反向表) |
| **同 pack 群衝突 57 個** | 暫不污染主索引,只在本檔記錄;Swwan 真被裝才升級 |

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 KJNodes 的版本,實際跑的是另一個 pack 的同名節點 → 行為不一致 → 除錯地獄

**範例**:`ImageConcatMulti` 同時存在於 KJNodes 和 Swwan,字母序 K < S,所以 Swwan 會覆蓋 KJNodes 版本。

---

## 衝突分類總表

### 🟢 群組 1:與 `ComfyUI_Swwan` 衝突(57 個,風險零)

`ComfyUI_Swwan` 是極冷門 pack(GitHub 星數極少),節點清單跟 KJNodes 高度重疊,像是 fork 或抄襲。
**決策:Swwan 永不安裝**(已寫入主索引決策表 2026-04-27)。
**未來看到 Manager 推薦這個 pack,直接跳過**。

> 群組 1 完整列表(57 個節點):
>
> AddLabel, ColorMatch, CrossFadeImages, CrossFadeImagesMulti, DrawMaskOnImage, FastPreview, GetImageRangeFromBatch, GetImageSizeAndCount, GetImagesFromBatchIndexed, GetLatentRangeFromBatch, GetLatentSizeAndCount, ImageAddMulti, **ImageAndMaskPreview**, ImageBatchExtendWithOverlap, ImageBatchFilter, ImageBatchJoinWithTransition, ImageBatchRepeatInterleaving, ImageBatchTestPattern, ImageConcanate, ImageConcatFromBatch, ImageConcatMulti, ImageCropByMask, ImageCropByMaskAndResize, ImageCropByMaskBatch, ImageGrabPIL, ImageGridComposite2x2, ImageGridComposite3x3, ImageGridtoBatch, ImageNormalize_Neg1_To_1, ImagePadForOutpaintMasked, ImagePadForOutpaintTargetSize, ImagePadKJ, ImagePass, ImagePrepForICLora, ImageResizeKJ, ImageResizeKJv2, ImageTensorList, ImageUncropByMask, ImageUpscaleWithModelBatched, InsertImagesToBatchIndexed, LoadAndResizeImage, LoadImagesFromFolderKJ, LoadVideosFromFolder, MergeImageChannels, PadImageBatchInterleaved, PreviewAnimation, RemapImageRange, ReplaceImagesInBatch, ReverseImageBatch, SaveImageKJ, SaveImageWithAlpha, SaveStringKJ, ShuffleImageBatch, TransitionImagesInBatch, TransitionImagesMulti, WebcamCaptureCV2
>
> (粗體 `ImageAndMaskPreview` 是 Flux-fill 萬物移除工作流會用到的節點)

---

### 🟡 群組 2:多重衝突(3 個,中低風險)

| KJNodes 節點 | 衝突 pack | 風險 | 評估 |
|---|---|---|---|
| `AudioConcatenate` | MW-ComfyUI_AudioTools, Image Processing Suite for ComfyUI | 🟡 中 | 兩個都是中度活躍 audio pack。**Qwen3 TTS workflow 階段裝 audio pack 前必須回查** |
| `ImageBatchMulti` | ComfyUI_Swwan, ComfyUI_JomaNodes | 🟢 低 | JomaNodes 是小型 pack,Swwan 不裝 |
| `SplitImageChannels` | ComfyUI_Swwan, cspnodes | 🟢 低 | cspnodes 冷門,Swwan 不裝 |

---

### 🟡 群組 3:單一衝突(其他)(2 個,中低風險)

| KJNodes 節點 | 衝突 pack | 風險 | 評估 |
|---|---|---|---|
| `Sleep` | ComfyUI Functional | 🟢 低 | Functional 是 utility pack,流程控制可能撞 |
| `WanVideoNAG` | Yaser-nodes for ComfyUI | 🟡 中 | **Wan 2.2 系列階段裝 Wan 相關 pack 前必須回查** |

---

## 對 system-setup 下一階段規劃的影響

對照 `comfyui-setup.md` 的「下一階段規劃」:

| 規劃 workflow | 可能影響的衝突 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 | `ImageAndMaskPreview`(Swwan) | ✅ Swwan 不裝,**安全** |
| Kontext + ControlNet 姿態改變 | 無 | — |
| Qwen3 TTS 聲音克隆 / 設計 | `AudioConcatenate` | ⚠️ 裝 audio pack 前回查本檔 + 主索引 |
| Qwen image 擴圖 | 無 | — |
| 智能多角度生成 | 無 | — |
| Wan 2.2 系列 | `WanVideoNAG` | ⚠️ 裝 Wan 相關 pack 前回查本檔 + 主索引 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 2026-04-27 | 安裝 KJNodes v1.3.9 | Flux-fill 萬物移除 workflow 必需節點 `ImageAndMaskPreview` 由此 pack 提供 |
| 2026-04-27 | Swwan 永不安裝 | KJNodes 是上游正主,Swwan 疑似 fork;57 個節點衝突全部由 KJNodes 接管 |

---

## 相關文件

- [`comfyui-conflicts.md`](./comfyui-conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`comfyui-setup.md`](./comfyui-setup.md) — ComfyUI 配置全貌(含 Custom Nodes 安裝規則)
- [`comfyui-workflows.md`](./comfyui-workflows.md) — Workflow 清單(Flux-fill 萬物移除是 ImageAndMaskPreview 唯一使用者)

---

**最後更新**:2026-04-27

**同步來源**:
- ComfyUI Manager v3.39.2 conflicts UI(2026-04-27 取得 61 條原始記錄)
- KJNodes v1.3.9
