# Comfyui-QwenEditUtils 衝突明細

> Pack:**Comfyui-QwenEditUtils** by lrzjason / xiaozhijason / 小志Jason
> 版本:repo HEAD(2026-04-29 git clone,~640 stars)
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
| **裝這個 pack 的原因** | Workflow #3a-v2(Qwen Edit 2509 改姿態保留人物)需要 `TextEncodeQwenImageEditPlus_lrzjason`(客製 conditioning,作者跟 `consistence_edit_v2` LoRA 同一人 lrzjason,配套設計);未來 #5 Qwen Image 擴圖 / #6 智能多角度 等 Qwen 系列 workflow 也可能用其他 lrzjason 變種節點 |
| **Manager UI 衝突數** | 0(透過結構性 `/object_info` 比對驗證,cm-cli 無 conflicts UI,詳 conflicts-controlnet-aux.md 的「ComfyUI Manager cm-cli 限制」段沿用)|
| **裝了沒問題** | 14 個節點全部 lrzjason 自家命名空間(7 個 `*_lrzjason` 後綴 + 7 個 `QwenEdit*` / 其他前綴),跟既有 active 5 條反向索引 + KJNodes 234 + rgthree 24 + alekpet 16 + controlnet_aux 64 = 0 重疊 |
| **依賴自動裝** | 無 — `requirements.txt` 不存在,`__init__.py` + `nodes.py`(64 KB)只 import comfy / torch / numpy / PIL,全部已存在於 ComfyUI portable 環境 |
| **GPU 額外下載** | 無 — 14 個節點都是 conditioning / config / image utility,不下載額外 model 權重 |

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄

**Comfyui-QwenEditUtils 在本機完全規避了這個機制**:14 個節點全部以 `*_lrzjason` 後綴 + `QwenEdit*` / `CropWithPadInfo` / `LoadImageReturnFilename` 命名空間,跟既有 5 個 active pack(KJNodes / rgthree / controlnet_aux / alekpet / 即將新增的 QwenEditUtils)0 命名空間重疊。

---

## 衝突分類

**無衝突。**

結構性比對(2026-04-29 install 當下實證):
- pre-install `/object_info`:1282 nodes
- post-install `/object_info`:1296 nodes
- **delta = +14**(全部新增,**0 個 same-name override / 0 個 removed**)
- 跟主索引「反向節點索引」5 條 active(`AudioConcatenate` / `Sleep` / `SplitImageChannels` / `WanVideoNAG` + 略)0 交集
- 跟 KJNodes / rgthree / controlnet_aux / alekpet 全清單 0 交集

---

## QwenEditUtils 提供的節點清單

來源:HTTP `/object_info` filter `python_module = 'custom_nodes.Comfyui-QwenEditUtils'`(2026-04-29 取得 14 節點)

| 類別 | 節點 | 用途 |
|---|---|---|
| TextEncode lrzjason 變種 | `TextEncodeQwenImageEdit_lrzjason` | Qwen Image Edit 客製 conditioning(基本版)|
| | `TextEncodeQwenImageEditPlus_lrzjason` | **Plus 版**(本輪 #3a-v2 用,雙圖 + prompt + custom instruction)|
| | `TextEncodeQwenImageEditPlusAdvance_lrzjason` | Advanced 版(更多控制參數)|
| | `TextEncodeQwenImageEditPlusCustom_lrzjason` | Custom 版(完全客製)|
| | `TextEncodeQwenImageEditPlusPro_lrzjason` | Pro 版 |
| Config / Parser | `QwenEditConfigPreparer` | 準備 Qwen Edit 通用 config |
| | `QwenEditConfigJsonParser` | 解析 config JSON |
| Output / List 處理 | `QwenEditOutputExtractor` | 從 Qwen Edit 輸出抽欄位 |
| | `QwenEditListExtractor` | List 抽欄位 |
| 圖像對齊 | `QwenEditAdaptiveLongestEdge` | 長邊自適應 resize |
| | `CropWithPadInfo` | 裁切 + pad 資訊 |
| 其他 | `QwenEditAny2Image` | 任意輸入轉 image |
| | `QwenEditAny2Latent` | 任意輸入轉 latent |
| | `LoadImageReturnFilename` | LoadImage 變種,額外回傳 filename |

**總計 14 節點**(2026-04-29 實證,跟派工 §1.1 預期 ~10 個有出入 — 派工低估了 lrzjason 變種數 4 個)。

---

## 對 system-setup 下一階段規劃的影響

對照 `setup.md` 的「下一階段規劃」:

| 規劃 workflow | 用到 QwenEditUtils 哪些節點 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 ✅ | 無 | — |
| ~~Kontext + ControlNet 改姿態~~ ❌ | (曾規劃用 lrzjason 但路線已棄)| — |
| **3a-v2 Qwen Edit 改姿態 ✅(2026-04-29)** | `TextEncodeQwenImageEditPlus_lrzjason`(C 方案 unbypass 但不被 KSampler 消費,事實上效果靠內建 `TextEncodeQwenImageEditPlus`)| 已用 |
| 3b FLUX + ControlNet 純 pose ✅ | 無 | — |
| Qwen3 TTS(#4 / #7)| 不會 | — |
| **#5 Qwen Image 擴圖**(待建) | 可能用 `QwenEditAdaptiveLongestEdge` / `QwenEditAny2Image` | 規劃時對照 |
| **#6 智能多角度生成**(待建) | 可能用 `QwenEditConfigPreparer` 等 config 系列 | 規劃時對照 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 2026-04-29 | 安裝 Comfyui-QwenEditUtils(repo HEAD)| Workflow #3a-v2 需 `TextEncodeQwenImageEditPlus_lrzjason`;作者 lrzjason 跟 `consistence_edit_v2` LoRA 同一人,配套設計;結構性 0 衝突;~640 stars 活躍維護 |
| 2026-04-29 | 透過 `git clone` 而非 cm-cli | 工具一致性(本 pack 在 cm-cli show-list 沒登錄,直接 git clone repo HEAD)|
| 2026-04-29 | C 方案不動 link 但 unbypass node 44 lrzjason | 主窗口拍板 — node 44 enable 後輸出去 ConditioningZeroOut 廢棄,KSampler positive 仍走 node 45 內建。lrzjason 客製 prompt instruction 沒生效,**事實上 #3a-v2 跑通靠的是 ComfyUI 內建 `TextEncodeQwenImageEditPlus` + 雙 LoRA(Lightning + consistence_edit)**,QwenEditUtils 在本輪只是「裝著但沒被 KSampler 真正消費」 |

---

## 相關文件

- [`conflicts.md`](./conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`setup.md`](./setup.md) — ComfyUI 配置全貌(本 pack 在「已裝 Custom Nodes」清單)
- [`workflows.md`](./workflows.md) — Workflow #3a-v2 詳述(`TextEncodeQwenImageEditPlus_lrzjason` 唯一使用者,本輪 unbypass 但事實上 KSampler 走內建路徑)
- [`conflicts-controlnet-aux.md`](./conflicts-controlnet-aux.md) — 結構性比對 SOP 來源(本檔沿用)
- [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) — KJNodes 衝突明細(per-pack template 來源)

---

**最後更新**:2026-04-29

**同步來源**:
- HTTP `/object_info` filter `python_module = 'custom_nodes.Comfyui-QwenEditUtils'`(2026-04-29 取得 14 節點清單)
- `git clone https://github.com/lrzjason/Comfyui-QwenEditUtils.git`(2026-04-29 安裝紀錄)
- 結構性比對 vs KJNodes / rgthree / controlnet_aux / alekpet / 主索引反向表(2026-04-29 全綠)
- Workflow #3a-v2 實證跑通(C 方案 8 步 92.8s,VRAM peak 23,832 MiB)
