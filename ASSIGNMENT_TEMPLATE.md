# ASSIGNMENT_TEMPLATE — 派工模板

> **這份模板給「主視窗 Claude」用**。產派工給 Claude Code 執行端時,照這個格式寫。
>
> 設計原則:**目標型派工,非精準執行型**。主視窗不寫 patch 表 / widgets_values index / REPL 指令這類執行細節,讓執行端讀實機檔自己規劃。
>
> 主視窗職責:定義目標 + 列已決策選項 + 列限制 + 定義完成判定。

---

## 使用方式

### 主視窗端

產派工時照下方範本格式寫,**保留所有 section heading**。沒內容的 section 寫「無」(讓執行端確認主視窗考慮過該欄)。

### Wayne 轉交

主視窗產出後 Wayne 下載 → 貼給 Claude Code 執行端。

### 執行端

讀完派工後依目標自己規劃執行步驟。STOP 觸發點上報主視窗,不擅自修改決策已定的選項。

---

# 派工:[一句話標題]

> 主視窗產出,Wayne 轉交 Claude Code 執行端。
> 日期:YYYY-MM-DD
> 前置:[依賴的前一輪派工狀態,例:Step 1-2 完成 / 無前置]

---

## 目標

[2-3 句描述要達成什麼。寫「最終狀態」不寫「步驟」。]

範例:
> Qwen Edit 2509 改姿態 workflow 本地化到 Wayne 機器,跑通煙測,寫 progress report。

---

## 決策已定(主視窗已拍板,不要重新討論)

- [列出已決策的選項]

範例:
- node 35 用 PrimitiveStringMultiline(comfy-core 內建)取代 was-node-suite Text Multiline
- C 方案 unbypass 三節點(node 4 / 34 / 44)+ KSampler 改 8 步
- KSampler scheduler / cfg 由執行端 verify Lightning LoRA README 自決

如果沒有任何已決策的選項,寫「無」。

---

## 限制

- [不可違反的事項]

範例:
- 不裝 was-node-suite-comfyui(衝突,conflicts.md 既有決策)
- 不動 link 結構,只動 node mode + widgets_values + type
- 跨檔 bulk patch 時保留各檔 line ending(規則 7)

---

## 參考文件

- [本地絕對路徑,讓執行端自己讀,主視窗不重抄內容]

範例:
- `D:\Work\system-setup\comfyui\setup.md`
- `D:\Work\system-setup\comfyui\conflicts.md`(衝突主索引)
- `D:\Work\system-setup\tools\workflow_submit.py`(已知工具)

如果有外部 docs 需要查,寫:

- 用 `use context7 with /<repo>/<name>` 抓 [docs 名](規則 10 / Context7 A 模式)

---

## 完成判定

[明確的 pass/fail 條件,執行端自己跑驗證]

範例:
1. workflow JSON 落地 `D:\Work\system-setup\comfyui-workflows\<檔名>.json`,自檢 N 項全綠
2. 煙測通過(POST /prompt 後 prompt_id 有值,/history status 正常,有 output images)
3. progress report 落地 `D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`
4. 寫檔 SOP:.NET API + 無 BOM + line ending 偵測 + 三 byte 驗證(規則 2 / 規則 7)

---

## STOP 觸發條件

- [列出需要回報主視窗做決策的情境,執行端遇到 → 上報不繼續]

範例:
- 衝突檢查發現 N 個 same-name override(影響既有節點)
- 煙測 server validation fail(node_errors 非空)
- 模型路徑或檔名不存在(下載沒完整或 yaml mapping 出錯)
- 派工內容跟實機真相不一致(任一 cross-verify 失敗)

---

## 報告

完成後產 progress report,落地路徑:

`D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`

格式照 `D:\Work\system-setup\PROGRESS_TEMPLATE.md`。

主視窗整合進對應 MD 後 Wayne 刪 report 檔(progress-reports/ 目錄 gitignored)。

---

**範本結束**

---

## 給主視窗的設計提醒

寫派工前自問四件事:

1. **目標 vs 步驟**:這條是「要達成什麼」還是「怎麼做」?如果是怎麼做,改寫成怎麼判定 done。
2. **決策 vs 自決**:這個選擇是主視窗已拍板,還是執行端可根據實機 verify 決定?寫進「決策已定」段的不要再讓執行端問。
3. **重抄 vs 引用**:這份內容是不是已經在某 MD 裡?如果是,引用本地路徑讓執行端自己讀,不重抄。
4. **完成判定可機讀**:pass/fail 條件能寫成 grep / assert / curl 嗎?能 → 寫具體;不能 → 描述清楚現象。

---

## 跟 PROGRESS_TEMPLATE 的對仗

| 檔 | 給誰用 | 用途 | 何時用 |
|---|---|---|---|
| `ASSIGNMENT_TEMPLATE.md`(本檔)| 主視窗 | 產**派工模板**的格式 | 派工開始時 |
| `PROGRESS_TEMPLATE.md` | 執行端 | 產**進度報告**的格式 | 任務結束時 |

---

**最後更新**:2026-04-29
