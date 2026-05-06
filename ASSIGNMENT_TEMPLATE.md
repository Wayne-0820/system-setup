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

範例(目標型,具體 node id / 路徑由執行端讀實機檔自決):
- C 方案 unbypass 三節點 + KSampler 改 8 步(具體 node id 由執行端 audit 實機 workflow JSON)
- 用 comfy-core 內建 multiline 取代第三方(具體節點名由執行端 verify 實機 custom_nodes/ 自決)
- KSampler scheduler / cfg 由執行端 verify Lightning LoRA README 自決
- widget patch 紀律引用 SYSADMIN_BRIEFING 規則 12 三分(strict 核心對照變數 / 鬆綁 supporting model / 鬆綁 I/O widget),不另抄

如果沒有任何已決策的選項,寫「無」。

---

## 限制

- [不可違反的事項]

範例:
- 不裝 was-node-suite-comfyui(衝突,conflicts.md 既有決策)
- 不動 link 結構,只動 node mode + widgets_values + type
- 跨檔 bulk patch 時保留各檔 line ending(規則 7)
- VRAM ≥22 GB(decimal,規則 13)/ disk ≥32 GB(decimal)
- candidate JSON 全 dropdown widget 對齊(SHA256 校驗清單 mirror 全 model / file loader,規則 14)

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

> **除 §決策已定 排除項以外** — §決策已定 寫的「不做 X」是硬限制,執行端不會走到該分支,不需在 STOP 重列。違反 §決策已定 算嚴重事件 STOP 上報,但「不做 X」本身不寫成 STOP 條件。

- [列出需要回報主視窗做決策的情境,執行端遇到 → 上報不繼續]

範例(規則 11:STOP 只列需主視窗 / Wayne 介入的事,執行端可自處的不寫):
- 衝突檢查發現 N 個 same-name override(影響既有節點)
- 煙測 server validation fail(node_errors 非空)
- 模型路徑或檔名不存在(下載沒完整或 yaml mapping 出錯)
- 派工內容跟實機真相不一致(任一 cross-verify 失敗)
- 機器破壞性風險(OOM / hang / driver crash / nvlddmkm error)

**不寫進 STOP**(執行端自處):
- 啟動 server / cli tool(`Start-Process .bat` 可解)
- 等可 poll 的狀態(`Test-NetConnection` / curl 可解)
- 標準 retry(下載重連 / API rate limit 退避)
- 跑 verify 命令收集事實

---

## 報告

完成後產 progress report,落地路徑:

`D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`(此處日期 = 實機執行當天,規則 15)

格式照 `D:\Work\system-setup\PROGRESS_TEMPLATE.md`。

主視窗整合進對應 MD 後 Wayne 刪 report 檔(progress-reports/ 目錄 gitignored)。

---

**範本結束**

---

## 給主視窗的設計提醒

寫派工前自問:

1. **目標 vs 步驟**:這條是「要達成什麼」還是「怎麼做」?如果是怎麼做,改寫成怎麼判定 done
2. **決策 vs 自決**:這個選擇是主視窗已拍板,還是執行端可根據實機 verify 決定?寫進「決策已定」段的不要再讓執行端問
3. **重抄 vs 引用**:這份內容是不是已經在某 MD 裡?如果是,引用本地路徑讓執行端自己讀,不重抄
4. **完成判定可機讀**:pass/fail 條件能寫成 grep / assert / curl 嗎?能 → 寫具體;不能 → 描述清楚現象
5. **引用 verify**(規則 8 evergreen):派工引用「規則 N」「踩坑 #N」「§N」「progress report 路徑」前 grep verify,不靠記憶。引用錯誤跨 session 傳染
6. **STOP 排除執行端可自處**(規則 11):啟動 server / poll / retry / 跑 verify 命令不寫 STOP — 一行 PowerShell 能解的不寫
7. **§決策已定 widget 紀律引用三分**(規則 12):strict 核心對照變數 / 鬆綁 supporting model / 鬆綁 I/O widget,不另抄
8. **數值門檻標 GB / GiB**(規則 13):邊界附近強制標明,默認 GB decimal
9. **§限制 SHA256 校驗清單 mirror candidate JSON 全 widget**(規則 14):派工撰寫前 grep candidate JSON 列全部 model / file loader widget,不只「主模型 + LoRA」直觀
10. **派工撰寫前 audit candidate JSON 結構**:grep `definitions.subgraphs` 檢測 ComfyUI 0.19 subgraph,確認 `tools/workflow_submit.py` 兼容性
11. **派工檔名日期語意 = 實機執行當天**(規則 15):派工檔名 `<YYYY-MM-DD>` = session 2 執行當天本地系統日期;跨日場景由 session 2 step 1.5 verify + rename 派工檔對齊
12. **§參考文件 不列 `progress-reports/session1-snapshot.md`**:該檔是 session 1 主視窗 handoff anchor,session 2 ❌ 邊界明列不讀(SESSION_2_EXECUTOR.md §2),派工列入會違反 session 2 紀律

---

## 跟 PROGRESS_TEMPLATE 的對仗

| 檔 | 給誰用 | 用途 | 何時用 |
|---|---|---|---|
| `ASSIGNMENT_TEMPLATE.md`(本檔)| 主視窗 | 產**派工模板**的格式 | 派工開始時 |
| `PROGRESS_TEMPLATE.md` | 執行端 | 產**進度報告**的格式 | 任務結束時 |

---

**最後更新**:2026-05-04
