# ComfyUI rgthree-comfy 衝突明細

> Pack:**rgthree-comfy** by rgthree
> 版本:1.0.260407001
> 安裝日:**架構前已裝(< 2026-04-28),實際日期未記錄**
> 補入紀錄日:**2026-04-28**(事後 catch-up)
> 狀態:✅ active
>
> 主索引:[`comfyui-conflicts.md`](./comfyui-conflicts.md)
> 風險分級標準見主索引。
>
> 最後更新:2026-04-28

---

## TL;DR

| 結論 | 說明 |
|---|---|
| **裝這個 pack 的原因(事後追溯)** | 不確定,可能來自早期 ComfyUI 探索階段。Flux-fill OneReward 萬物移除 workflow 也需要 rgthree(`RgthreeContext` / `RgthreeSeed` 類 utility),屬剛好可用 |
| **Manager 標示衝突數** | **0**(2026-04-28 重新驗證) |
| **裝了沒問題** | ✅ 全 24 個註冊節點都帶 `Rgthree*` prefix,獨佔命名空間,跟 KJNodes 234 節點 / 主索引 4 條 active 反向索引 / 黑名單 Swwan 57 節點 / 既有 5 pack 全部 0 交集 |
| **catch-up 性質** | rgthree 在衝突管理架構建立前就已裝,本檔為事後反向收資料,**不是裝前 scoping** |

---

## 為什麼這份是 catch-up 不是裝前 scoping

2026-04-28 環境盤點時發現 `D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\` 實體有 `rgthree-comfy\`,但 `comfyui-setup.md` 的「已裝 Custom Nodes」清單沒記錄,屬於**架構建立前已存在、漏網沒記錄的 pack**。

按 `comfyui-setup.md`「裝新 custom node 流程」原本是裝前→比對→裝→產檔。但 rgthree 已在跑,只能反向走:

1. 在 Manager 已安裝列表確認版本字串 + 24 個節點
2. 從 `__init__.py` 取 NODE_CLASS_MAPPINGS 全清單
3. 結構性比對(前綴 / 命名空間)+ Manager UI 衝突數驗證
4. 產本檔,Header 標「架構前已裝」+ 補入紀錄日

以後新 pack 一律走 setup.md 標準裝前流程,本檔結構同其他 per-pack 檔但 metadata 多一行「補入紀錄日」。

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄

**rgthree 在本機完全規避了這個機制**:24 個節點全部 `Rgthree*` prefix,屬於獨佔命名空間。任何其他 pack 沒採用同 prefix,結構上不可能撞名。

---

## 衝突分類

**無衝突。**

Manager v3.39.2 conflicts UI 顯示 **0**(2026-04-28 驗證)。
全 24 個註冊節點均以 `Rgthree*` 為 prefix,跟以下對象交叉比對均為 0 交集:

- KJNodes v1.3.9(234 節點)
- 主索引「反向節點索引」4 條 active(`AudioConcatenate` / `Sleep` / `SplitImageChannels` / `WanVideoNAG`)
- 黑名單 `ComfyUI_Swwan`(57 節點)
- 既有 5 pack:LayerStyle / LayerStyle_Advance / Custom-Scripts / AlekPet / SUPIR

---

## rgthree 提供的節點清單

來源:`D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\rgthree-comfy\__init__.py` L47-76 NODE_CLASS_MAPPINGS。

### 無條件註冊(24 個)[^1]

| 分類 | 數量 | 節點(類別名) |
|---|---|---|
| Context 系列 | 6 | `RgthreeContext` / `RgthreeBigContext` / `RgthreeContextSwitch` / `RgthreeContextSwitchBig` / `RgthreeContextMerge` / `RgthreeContextMergeBig` |
| Display | 2 | `RgthreeDisplayInt` / `RgthreeDisplayAny` |
| Prompt 系列 | 4 | `RgthreePowerPrompt` / `RgthreePowerPromptSimple` / `RgthreeSDXLPowerPromptPositive` / `RgthreeSDXLPowerPromptSimple` |
| Lora / Sampler | 3 | `RgthreeLoraLoaderStack` / `RgthreePowerLoraLoader` / `RgthreeKSamplerConfig` |
| Image | 4 | `RgthreeImageInsetCrop` / `RgthreeImageComparer` / `RgthreeImageOrLatentSize` / `RgthreeImageResize` |
| 雜項 | 5 | `RgthreeSeed` / `RgthreeSDXLEmptyLatentImage` / `RgthreeAnySwitch` / `RgthreePowerPrimitive` / `RgthreePowerPuter` |

### 條件註冊(2 個)

需 `unreleased.dynamic_context.enabled = true`,預設不啟用。

- `RgthreeDynamicContext`
- `RgthreeDynamicContextSwitch`

**最多總計 26 個節點**(無條件 24 + 條件 2)。Manager UI 顯示 **24 nodes**,跟無條件註冊數對上。

[^1]:`__init__.py` L47-76 註解格式中「雜項 (6)」實際列出 5 個,本檔以**列出條目**為準(共 24)。若日後驗證到第 6 個漏列節點名,本表「雜項」欄補上,合計改 25。

### 類別名 vs UI 顯示名

ComfyUI UI 選單顯示名來自各 `py/*.py` 內 `NAME` 屬性,**跟類別名不一定相同**。例如 `RgthreePowerLoraLoader` 在 UI 可能顯示為 "Power Lora Loader (rgthree)"。

衝突偵測走**類別名**(NODE_CLASS_MAPPINGS key),不走顯示名,所以本檔列類別名即可。

---

## 對 system-setup 下一階段規劃的影響

對照 `comfyui-setup.md` 的「下一階段規劃」:

| 規劃 workflow | rgthree 節點是否會用到 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 | ⚠️ 待 Step 3 載入 workflow 時驗證(`RgthreeSeed` / `RgthreeContext` 類 utility 常見於 inpainting workflow) | 裝前驗證已通過,workflow 載入時若 missing 節點再補查 |
| Kontext + ControlNet 姿態改變 | 未知 | 解析 JSON 時驗證 |
| Qwen3 TTS 聲音克隆 / 設計 | 不太可能(TTS 跟 rgthree utility 領域不重疊) | — |
| Qwen image 擴圖 | 未知 | 解析 JSON 時驗證 |
| 智能多角度生成 | 未知 | 解析 JSON 時驗證 |
| Wan 2.2 系列 | 未知 | 解析 JSON 時驗證 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 架構前(補入紀錄 2026-04-28) | rgthree-comfy 已安裝,維持 | 事後追溯安裝動機不明,但結構驗證 0 衝突,維持比卸載安全(可能有未知 workflow 依賴) |
| 2026-04-28 | 不卸載、不版本切換 | Manager 顯示 conflicts = 0,Try update / Switch Ver 動作風險未評估;先就地維持 1.0.260407001,日後若 Flux-fill 萬物移除 workflow 載入時要求更新版本再評估 |

---

## 跟 KJNodes 共存狀態

rgthree-comfy(架構前已裝)+ KJNodes v1.3.9(2026-04-28 裝)目前共存於 `custom_nodes\`,兩者:

- 命名空間互不重疊(`Rgthree*` vs 無 prefix)
- 字母序載入順序:`ComfyUI-KJNodes` < `rgthree-comfy`,KJNodes 先載
- 無同名節點 → **誰先誰後不影響任何節點的 active 狀態**,雙方 100% 各自 active

之前擔心的「rgthree + KJNodes 同時跑了一段時間,如果有衝突早就在跑」**結構上不存在**——24 vs 234 節點清單 0 交集,不可能有暗中覆蓋。

---

## 相關文件

- [`comfyui-conflicts.md`](./comfyui-conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`comfyui-setup.md`](./comfyui-setup.md) — ComfyUI 配置全貌(本 pack 補入「已裝 Custom Nodes」清單由主窗口處理)
- [`comfyui-conflicts-kjnodes.md`](./comfyui-conflicts-kjnodes.md) — KJNodes 衝突明細(per-pack template 來源)
- [`comfyui-workflows.md`](./comfyui-workflows.md) — Workflow 清單

---

**最後更新**:2026-04-28

**同步來源**:
- ComfyUI Manager v3.39.2 已安裝列表(2026-04-28 截圖確認版本 1.0.260407001、24 nodes、Description "Making ComfyUI more comfortable.")
- ComfyUI Manager v3.39.2 conflicts UI(2026-04-28 驗證 conflicts = 0)
- `__init__.py` L47-76 NODE_CLASS_MAPPINGS(2026-04-28 取得節點清單)
