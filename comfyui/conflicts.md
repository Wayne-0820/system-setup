# ComfyUI 節點衝突主索引

> 這份檔案是 **ComfyUI custom_node 衝突的中央索引 + 反向查表 + 決策日誌**。
> 每個 pack 的明細衝突清單放在 `conflicts-{pack}.md`(per-pack 檔案)。
> 裝新 pack 前**必查這份**,裝完更新這份。
>
> 最後更新:2026-04-29

---

## TL;DR

| 項目 | 狀態 |
|---|---|
| 已記錄 pack 數 | 2(KJNodes、rgthree-comfy) |
| 反向索引節點數 | 4(active 衝突)+ 57(同 pack 群衝突,待安裝才升級) |
| 高風險未解衝突 | 0 |
| 中風險待留意 | 3(`AudioConcatenate` / `WanVideoNAG` / `was-node-suite-comfyui` archived 替代節點對照) |

---

## 為什麼要做這份

ComfyUI 同名節點機制:兩個 pack 註冊同名節點時,**字母序後載入的 pack 覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)。
結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄。

這份檔案解決三種查詢:

1. **正向**:裝 pack X,跟現有環境衝突什麼?(看 per-pack 檔案)
2. **反向**:節點 N 是哪些 pack 提供的?目前用哪個版本?(看本檔「反向節點索引」)
3. **決策追溯**:為什麼選 A 不選 B?(看本檔「解決決策表」)

---

## 已安裝 pack 總表

| Pack 名稱 | 版本 | 安裝日 | 衝突數 | 明細檔案 | 狀態 |
|---|---|---|---|---|---|
| ComfyUI-KJNodes | v1.3.9 | 2026-04-28 | 61 | [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) | ✅ active |
| rgthree-comfy | v1.0.260407001 | < 2026-04-28(catalog 04-28) | 0 | [`conflicts-rgthree.md`](./conflicts-rgthree.md) | ✅ active |

**狀態定義**:
- ✅ active:目前在用,衝突已解決
- ⚠️ watch:有未爆發衝突,下階段規劃會碰到
- 🚫 skipped:評估後不裝
- 🗑️ removed:曾裝過,已移除

---

## 🔑 反向節點索引(active 衝突)

> 規則:**只列當前 active pack 與其他 pack 同名的節點**(同 pack 群衝突另列)。
> 未來裝新 pack 時,新增同名節點直接 append 到這張表。
> 查「節點 X 會撞嗎」grep 這張就好。

| 節點名稱 | 提供 pack | 當前勝出 | 風險 | 備註 |
|---|---|---|---|---|
| `AudioConcatenate` | KJNodes, MW-ComfyUI_AudioTools, Image Processing Suite | KJNodes | 🟡 中 | ⚠️ Qwen3 TTS 階段裝 audio pack 前回查 |
| `Sleep` | KJNodes, ComfyUI Functional | KJNodes | 🟢 低 | Functional 是 utility pack,撞到再看 |
| `SplitImageChannels` | KJNodes, ComfyUI_Swwan, cspnodes | KJNodes | 🟢 低 | cspnodes 冷門,Swwan 已決定不裝 |
| `WanVideoNAG` | KJNodes, Yaser-nodes for ComfyUI | KJNodes | 🟡 中 | ⚠️ Wan 2.2 階段裝 Wan 相關 pack 前回查 |

### 同 pack 群衝突(待新 pack 安裝才升級)

部分節點目前只跟「不打算安裝」的 pack 衝突,沒有 active 對手,先收在 per-pack 檔案,不污染本表。
範例:KJNodes 的 57 個跟 `ComfyUI_Swwan` 的衝突 → 因為 Swwan 不裝,這些節點在本反向表中不出現。
若未來真的裝了 Swwan(或類似 fork pack),把對應節點從 per-pack 檔案升級到本表。

---

## 上游 archived pack 警示

某些 ComfyUI custom_node pack 上游已被作者 archive(GitHub 不再維護,不會適配新 ComfyUI 版本)。
裝這類 pack 風險:**未來 ComfyUI / PyTorch 升級可能讓該 pack 失效,且沒人會修**。

| Pack | Archive 日期 | 仍可裝? | 我們的決策 | 替代方案 |
|---|---|---|---|---|
| `was-node-suite-comfyui`(WASasquatch) | 2025-06 | 可(Manager 仍列) | **不裝** | 看「替代節點對照」段(KJNodes / Impact-Pack 等價) |

**SOP**:Manager 推薦或 workflow 依賴 archived pack 節點時:
1. 先查本表 — 是不是已知 archived
2. 看「替代節點對照」段 — 有沒有等價節點
3. 都沒有 → raise 給主窗口拍板(權衡裝 archived pack vs 放棄該節點功能)

---

## 替代節點對照

某些節點功能在多個 pack 都有等價實作。當原 workflow 引用的 pack 不可用 / archived 時,
這張表記錄已驗證的等價對應,避免重新研究。

| 原節點 | 原 pack | 等價節點 | 等價 pack | 驗證 workflow | 等價條件 / 注意 |
|---|---|---|---|---|---|
| `Mask Fill Holes` | `was-node-suite-comfyui`(archived) | `GrowMaskWithBlur` | `ComfyUI-KJNodes` | `Flux-fill_OneReward_萬物移除_10步.json` | 設 `expand=0, blur_radius=0, fill_holes=True`,底層都用 `scipy.ndimage.binary_fill_holes`。注意 socket 名差異:WAS 是 `masks`(複數)/ 1 output,KJ 是 `mask`(單)/ 2 output(`mask` + `mask_inverted`)|

**新增規則**:每次因 pack 不可用而走替代節點路線,**實機驗證跑通後**才登記進此表(沒驗證的等價只是猜測,別寫進來)。

---

## 解決決策表

> 同名節點誰勝出 + 為什麼。每筆決策一行,有理由有日期,以後反悔也能追溯。

| 日期 | 衝突 | 決策 | 理由 |
|---|---|---|---|
| 2026-04-27 | KJNodes vs ComfyUI_Swwan(57 個節點) | KJNodes 勝出,Swwan 永不安裝 | Swwan 是疑似 fork / 抄襲的冷門 pack,KJNodes 是上游正主,星數活躍度差距巨大 |
| 2026-04-27 | KJNodes vs Image Processing Suite(`AudioConcatenate`) | KJNodes 暫勝,但 Qwen3 TTS 階段重新評估 | 目前未做 audio workflow,沒有實際衝突;TTS 階段若需要 Image Processing Suite 的功能再決定 |
| 2026-04-29 | `Mask Fill Holes`(WAS archived)vs `GrowMaskWithBlur`(KJNodes) | KJNodes 等價節點勝出,was-node-suite-comfyui **不裝** | was 已 archived 不再維護;為單一節點裝整 archived pack 維護負擔不對等;KJNodes 已裝且底層等價(`scipy.ndimage.binary_fill_holes`),Workflow #2 實機跑通驗證 |

---

## 裝新 pack 前 SOP

每次要裝新 custom_node 之前,**按順序跑這四步**:

### 1. 看 ComfyUI Manager 的 conflicts 數字
- 0 → 直接裝
- 1-10 → 看一下衝突列表,通常無害
- >10 → **打開列表逐項比對**

### 2. 比對本檔的「反向節點索引」
- 衝突節點裡有沒有你**正在用**的?(active 表裡)
- 衝突節點裡有沒有你**規劃會用**的?(per-pack 檔案的「下一階段影響」段)
- 都沒中:風險低,可以裝
- 有中:評估後決定(換 pack / 接受替代 / 不裝)

### 3. 安裝後產生 per-pack 衝突明細
- 檔名:`conflicts-{pack}.md`(pack 名小寫去 `ComfyUI-` 前綴,例如 `ComfyUI-KJNodes` → `kjnodes`、`ComfyUI_LayerStyle` → `layerstyle`、`was-node-suite-comfyui` → `was`)
- 用 [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) 當 template
- 段落:Header / TL;DR / 衝突分組(按風險)/ 對規劃 workflow 的影響 / 做的決策 / 最後更新

### 4. 更新本主索引
- **「已安裝 pack 總表」**:加一列
- **「反向節點索引」**:有新 active 衝突的節點 append
- **「解決決策表」**:重大決策一行
- 更新「最後更新」日期

---

## 風險分級標準

| 等級 | 定義 | 處理 |
|---|---|---|
| 🟢 **低** | 衝突 pack 是冷門 / 不會裝 / utility pack 偶發碰撞 | 記錄即可,不影響當前 |
| 🟡 **中** | 衝突 pack 跟 system-setup 下階段規劃 workflow 相關 | 反向索引標 ⚠️,規劃文件相互引用 |
| 🟠 **高** | 衝突節點目前正在用、行為不一致會直接壞 workflow | 立刻決策(留誰移誰),記錄到決策表 |
| 🔴 **致命** | 衝突會讓 ComfyUI 啟動失敗 / 模型載入失敗 / VRAM 異常 | 立刻移除新 pack,寫入 anti-pattern |

---

## 跟其他文件的關係

- [`setup.md`](./setup.md) — ComfyUI 配置全貌(含「裝新 custom node 流程」會引用本檔)
- [`workflows.md`](./workflows.md) — Workflow 清單(每個 workflow 用到的節點 → 出問題時回查衝突)
- [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) — KJNodes 衝突明細(per-pack template 範本)
- [`conflicts-rgthree.md`](./conflicts-rgthree.md) — rgthree-comfy 衝突明細(架構前已裝、catch-up 範例)

---

**最後更新**:2026-04-29

**維護規則**:每次新增 / 移除 / 升級 pack 後,**主索引 + per-pack 檔案**兩處都要更新。執行窗口產 per-pack 檔案 → 主窗口整合進主索引。
