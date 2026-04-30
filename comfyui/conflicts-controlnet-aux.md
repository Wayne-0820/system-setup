# comfyui_controlnet_aux 衝突明細

> Pack:**comfyui_controlnet_aux** by Fannovel16
> 版本:repo HEAD(透過 `cm-cli install` 安裝)
> 安裝日:2026-04-29
> 狀態:✅ active
>
> 主索引:[`conflicts.md`](./conflicts.md)
> 風險分級標準見主索引。
>
> 最後更新:2026-04-29

---

## TL;DR

| 結論 | 說明 |
|---|---|
| **裝這個 pack 的原因** | Workflow #3b(FLUX + ControlNet 純 pose 生人物)需要 `AIO_Preprocessor`(`OpenposePreprocessor` mode 抽 pose 骨架),未來 #3a-v2 / #3b-v2 / Pose 自由系列會用 `DWPreprocessor` / `DepthAnythingPreprocessor` / `HEDPreprocessor` 等 |
| **Manager UI 衝突數** | 0(透過結構性比對驗證,cm-cli 無 conflicts UI,詳「ComfyUI Manager cm-cli 限制」段) |
| **裝了沒問題** | 64 個節點全部前綴獨佔(`AIO_Preprocessor` / `*Preprocessor` / `DepthAnything*` / `Image*Detector` 等),跟既有 active 4 條反向索引 + KJNodes 234 節點 + rgthree 24 節點 + alekpet 16 節點 0 交集 |
| **依賴自動裝** | 第一次 ComfyUI 啟動時自動 pip 裝 `yacs` / `trimesh[easy]` / `manifold3d` / `lxml` / `svg.path` / `pycollada` / `colorlog` 等 |
| **第一次跑時下** | OpenposePreprocessor 第一次跑會自動從 HF `lllyasviel/Annotators` 下 ~200 MB(`body_pose.pth` / `hand_pose.pth` / `facenet.pth`),DWPreprocessor 同理下 `dw-ll_ucoco_384_bs5.torchscript.pt` + `yolox_l.onnx` |

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄

**comfyui_controlnet_aux 在本機完全規避了這個機制**:64 個節點全部以 preprocessor 任務命名(`AIO_Preprocessor` / `OpenposePreprocessor` / `DWPreprocessor` / `DepthAnythingPreprocessor` / `HEDPreprocessor` / `CannyEdgePreprocessor` / `LineartStandardPreprocessor` 等),無其他 pack 採用相同命名空間。

---

## 衝突分類

**無衝突。**

結構性比對(因 `cm-cli` 無 conflicts UI,需走 HTTP `/object_info` 結構比對)結果:
- 跟 KJNodes v1.3.9(234 節點)0 交集
- 跟 rgthree-comfy v1.0.260407001(24 節點)0 交集
- 跟 ComfyUI_Custom_Nodes_AlekPet(16 節點)0 交集
- 跟主索引「反向節點索引」4 條 active(`AudioConcatenate` / `Sleep` / `SplitImageChannels` / `WanVideoNAG`)0 交集

---

## ComfyUI Manager cm-cli 限制(2026-04-29 訂正)

執行窗口透過 `cm-cli.py install` 安裝新 pack 時,**沒有等價於 GUI Manager 的 conflicts UI 數字**。cm-cli 僅提供 install / uninstall / show-list 等基本操作,conflicts UI 是 Manager web frontend 的 feature。

**結構性比對 SOP**(派工模板未來引用):
1. ComfyUI 啟動後 HTTP `GET /object_info`
2. 按 `python_module` 分組,對新 pack 的節點集合 vs 既有 pack 集合做交集
3. 0 交集 = 結構性 0 衝突

**派工模板「看 Manager conflicts 數字」這條紀律**要區分:
- **GUI 派工**(Wayne 親手在 ComfyUI Manager web UI 操作):看 Manager 數字
- **執行端派工**(Claude Code 用 cm-cli 自動化):走結構性比對(本檔寫法)

---

## comfyui_controlnet_aux 提供的節點(類型概覽)

來源:HTTP `/object_info` filter `python_module` = `comfyui_controlnet_aux.*`(2026-04-29 取得)

| 類別 | 範例節點 | 計數 |
|---|---|---|
| AIO 整合 | `AIO_Preprocessor`(可切 OpenPose / DWPose / Canny / Depth 等 mode) | 1 |
| Pose 系列 | `OpenposePreprocessor` / `DWPreprocessor` / `AnimalPosePreprocessor` / `MediaPipe-FaceMeshPreprocessor` 等 | ~8 |
| Edge 系列 | `CannyEdgePreprocessor` / `HEDPreprocessor` / `FakeScribblePreprocessor` / `LineartStandardPreprocessor` / `LineartAnimePreprocessor` 等 | ~10 |
| Depth 系列 | `DepthAnythingPreprocessor` / `Zoe-DepthMapPreprocessor` / `MiDaS-DepthMapPreprocessor` / `LeresDepthMapPreprocessor` 等 | ~8 |
| Normal / Surface | `NormalBaePreprocessor` / `MeshGraphormer-DepthMapPreprocessor` 等 | ~5 |
| Segmentation | `SemSegPreprocessor` / `UniFormer-SemSegPreprocessor` / `OneFormer-COCO-SemSegPreprocessor` 等 | ~6 |
| Color / Tile | `TilePreprocessor` / `ColorPreprocessor` 等 | ~4 |
| Reference / Helpers | `ImageGenResolutionFromImage` / `ImageGenResolutionFromLatent` / `PixelPerfectResolution` 等 | ~5 |
| 其他 inpaint / shuffle | `ShufflePreprocessor` / `InpaintPreprocessor` 等 | ~2 |

**總計 ~64 節點**(具體數字以實機 `/object_info` filter 為準)。

---

## 對 system-setup 下一階段規劃的影響

對照 `setup.md` 的「下一階段規劃」:

| 規劃 workflow | 用到 controlnet_aux 哪些節點 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 ✅ | 無 | — |
| Kontext + ControlNet 改姿態 ❌ Deprecated | (曾用 AIO_Preprocessor) | 已棄 |
| **3a-v2 Qwen Edit 改姿態** | 規劃中,可能用 `AIO_Preprocessor` 或 `DWPreprocessor` | 規劃時對照 |
| **3b FLUX + ControlNet 純 pose ✅** | `AIO_Preprocessor` (`OpenposePreprocessor` mode) | 已用 |
| Qwen3 TTS 聲音克隆 / 設計 | 不會 | — |
| Qwen image 擴圖 | 可能用 inpaint / depth preprocessor | 規劃時對照 |
| 智能多角度生成 | 可能用 depth + pose | 規劃時對照 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 2026-04-29 | 安裝 comfyui_controlnet_aux(repo HEAD) | Workflow #3b 必需節點 `AIO_Preprocessor`(`OpenposePreprocessor` mode);上游 Fannovel16 活躍維護(非 archived);結構性 0 衝突 |
| 2026-04-29 | 透過 `cm-cli install` 而非 Manager web UI | 執行端自動化派工流程不走 GUI;走 HTTP `/object_info` 結構性比對替代 conflicts UI |

---

## 相關文件

- [`conflicts.md`](./conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`setup.md`](./setup.md) — ComfyUI 配置全貌(本 pack 在「已裝 Custom Nodes」清單)
- [`workflows.md`](./workflows.md) — Workflow #3b 詳述(`AIO_Preprocessor` 唯一使用者)
- [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) — KJNodes 衝突明細(per-pack template 來源)

---

**最後更新**:2026-04-29

**同步來源**:
- HTTP `/object_info` filter `python_module = 'comfyui_controlnet_aux.*'`(2026-04-29 取得 64 節點清單)
- `cm-cli install https://github.com/Fannovel16/comfyui_controlnet_aux`(2026-04-29 安裝紀錄)
- 結構性比對 vs KJNodes / rgthree / alekpet / 主索引反向表(2026-04-29 全綠)
