# ComfyUI_Custom_Nodes_AlekPet 衝突明細

> Pack:**ComfyUI_Custom_Nodes_AlekPet** by AlekPet
> 版本:架構前已裝(具體版本未記錄)
> 安裝日:**架構前已裝(< 2026-04-29),實際日期未記錄**
> 補入紀錄日:**2026-04-29**(事後 catch-up)
> 狀態:✅ active(部分 sub-node disabled,詳「ArgosTranslate cp950 install fail」段)
>
> 主索引:[`conflicts.md`](./conflicts.md)
> 風險分級標準見主索引。
>
> 最後更新:2026-04-29

---

## TL;DR

| 結論 | 說明 |
|---|---|
| **裝這個 pack 的原因(事後追溯)** | 早期 ComfyUI 探索階段裝,作為翻譯節點來源(`GoogleTranslateTextNode` / `DeepTranslatorTextNode`)。Workflow #6 / #7(JoyCaption 反推)用其翻譯節點接英→中 |
| **Manager UI 衝突數** | 0(結構性比對驗證) |
| **裝了沒問題** | ✅ 16 個註冊節點全部以特定領域命名(`Argos*` / `DeepTranslator*` / `GoogleTranslate*` / `Painter*`),獨佔命名空間 |
| **catch-up 性質** | alekpet 在衝突管理架構建立前就已裝,本檔為事後反向收資料,**不是裝前 scoping** |
| **⚠️ ArgosTranslate sub-node disabled** | 啟動時 ComfyUI console 報 `cp950 codec` 解碼錯誤,wheel build fail → 2 個 sub-node(`ArgosTranslateCLIPTextEncodeNode` / `ArgosTranslateTextNode`)未 register。**不修**(無 offline 翻譯需求) |

---

## 為什麼這份是 catch-up 不是裝前 scoping

2026-04-29 重組衝突管理時發現 `D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI_Custom_Nodes_AlekPet\` 已存在(`setup.md` 既有清單已列為「含 GoogleTranslateTextNode」),但無 `conflicts-alekpet.md` 對應檔。屬於**架構建立前已存在、漏網沒記錄的 pack**。

按 `setup.md`「裝新 custom node 流程」原本是裝前→比對→裝→產檔。但 alekpet 已在跑,只能反向走:

1. 在啟動 console 確認 active sub-node(看 `Failed to import` 訊息)
2. 從 `__init__.py` 讀 NODE_CLASS_MAPPINGS 全清單
3. 結構性比對(前綴 / 命名空間)
4. 產本檔,Header 標「架構前已裝」+ 補入紀錄日

以後新 pack 一律走 setup.md 標準裝前流程,本檔結構同其他 per-pack 檔但 metadata 多一行「補入紀錄日」+ 衝突段加「Active sub-node 缺漏」段。

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄

**alekpet 在本機完全規避了這個機制**:16 個節點全部以特定領域 prefix(`Argos*` / `DeepTranslator*` / `GoogleTranslate*` / `Painter*`),屬於獨佔命名空間。

---

## 衝突分類

**無命名衝突。**

但有 **sub-node load failure**(不算命名衝突,屬於 install fail):

### ⚠️ ArgosTranslate sub-node 在繁中系統 cp950 install fail

**症狀**(啟動 ComfyUI console):
```
Failed to import module ArgosTranslateNode because
UnicodeDecodeError: 'cp950' codec can't decode byte 0xe2 in position 1009: illegal multibyte sequence
```

**Disabled 節點**(2 個):
- `ArgosTranslateCLIPTextEncodeNode`
- `ArgosTranslateTextNode`

**根因**:`argos-translate` 套件的 `setup.py` 用 `open()` 不指定 `encoding=`,Windows 11 繁中系統 `locale.getpreferredencoding()` 回 `cp950`,讀檔內含的 UTF-8 byte 直接 decode 炸 → wheel build fail → ComfyUI 啟動時 alekpet 的 ArgosTranslate sub-module import 失敗 → 註冊 hook 被跳過。

**這是 user-level CLAUDE.md 教訓 5「Windows + 繁中系統:第三方工具讀 config 檔的 ASCII 紀律」的 in-the-wild 實證**(範圍從原本 yaml/json/.env 擴展到 Python wheel build 階段,體現「第三方工具不顯式帶 encoding 都可能炸」的通則)。

**解法**:**不修**。

理由:
- alekpet 的兩個翻譯節點(`GoogleTranslateTextNode` + `DeepTranslatorTextNode`)已涵蓋線上翻譯場景
- ArgosTranslate 是 offline 翻譯,本機沒有「無網路時翻譯」需求
- 修要 patch upstream `setup.py` 加 `encoding='utf-8'`(每次 reinstall 要重 patch),或改 system locale chcp 65001(影響範圍太廣),ROI 偏低

**未來重新評估觸發**:
- 出現需要 offline 翻譯場景(機密內容不能走 Google / DeepL 雲端)
- argos-translate 上游補上 encoding 修復

---

## ComfyUI_Custom_Nodes_AlekPet 提供的節點清單

來源:`D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI_Custom_Nodes_AlekPet\__init__.py` NODE_CLASS_MAPPINGS。

### 翻譯系列(active)

- `GoogleTranslateTextNode`(英→中,Workflow #6 用,走 Google 公開 endpoint 偶被 rate limit)
- `GoogleTranslateCLIPTextEncodeNode`
- `DeepTranslatorTextNode`(rate limit fallback,走 MyMemory backend)
- `DeepTranslatorCLIPTextEncodeNode`

### Argos 系列(disabled,cp950 install fail)

- ~~`ArgosTranslateTextNode`~~
- ~~`ArgosTranslateCLIPTextEncodeNode`~~

### Painter 系列(active,但本機 workflow 未用)

- `PainterNode`
- 其他 painter 子類

### 其他(active)

- 其他若干小工具節點(具體清單以 `__init__.py` 為準)

**總計**:16 個註冊條目,**14 個 active**,2 個 ArgosTranslate disabled。

---

## 對 system-setup 下一階段規劃的影響

對照 `setup.md` 的「下一階段規劃」:

| 規劃 workflow | alekpet 是否會用到 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 ✅ | 無 | — |
| 3a-v2 Qwen Edit 改姿態 | 可能(若引入翻譯節點) | 規劃時對照 |
| 3b FLUX + ControlNet 純 pose ✅ | 無 | — |
| Qwen3 TTS 聲音克隆 / 設計 | 不太可能(TTS 跟翻譯領域不重疊) | — |
| Qwen image 擴圖 | 可能(若有翻譯需求) | 規劃時對照 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 架構前(補入紀錄 2026-04-29) | ComfyUI_Custom_Nodes_AlekPet 已安裝,維持 | Workflow #6 用其 `GoogleTranslateTextNode` 接 JoyCaption 英→中翻譯;結構驗證 0 命名衝突;維持比卸載安全 |
| 2026-04-29 | ArgosTranslate sub-node disabled 不修 | 線上翻譯場景已由 Google + DeepL 覆蓋,offline 翻譯無需求,修要 patch upstream setup.py ROI 偏低 |
| 2026-04-29 | 不卸載、不版本切換 | 既有 workflow #6 / #7 依賴 GoogleTranslateTextNode,卸載風險未評估;先就地維持 |

---

## 跟其他 pack 共存狀態

ComfyUI_Custom_Nodes_AlekPet + KJNodes + rgthree-comfy + comfyui_controlnet_aux + LayerStyle 系列等 pack 共存於 `custom_nodes\`:

- 命名空間互不重疊(`Argos*` / `DeepTranslator*` / `Google*` / `Painter*` vs 其他 pack 的 prefix)
- 字母序載入:`ComfyUI-KJNodes` < `ComfyUI_Custom_Nodes_AlekPet` < `ComfyUI_LayerStyle*` < `comfyui_controlnet_aux` < `rgthree-comfy`
- 結構性 0 交集 → 不會有暗中覆蓋

---

## 相關文件

- [`conflicts.md`](./conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`setup.md`](./setup.md) — ComfyUI 配置全貌(本 pack 在「已裝 Custom Nodes」清單,踩坑 SOP §9 引用本檔)
- [`conflicts-rgthree.md`](./conflicts-rgthree.md) — rgthree-comfy 衝突明細(catch-up template 範本來源)
- [`workflows.md`](./workflows.md) — Workflow #6 / #7(`GoogleTranslateTextNode` 主要使用者)

---

**最後更新**:2026-04-29

**同步來源**:
- 啟動 ComfyUI console 訊息(2026-04-29 觀察 ArgosTranslate import fail)
- `__init__.py` NODE_CLASS_MAPPINGS(2026-04-29 取得節點清單)
- 結構性比對 vs KJNodes / rgthree / controlnet_aux / 主索引反向表(2026-04-29 全綠,無命名衝突)
