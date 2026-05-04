---
name: draft-assignment
description: When session 1 主視窗 needs to draft a new assignment for session 2, use this skill to align with ASSIGNMENT_TEMPLATE.md and SESSION_1 §4 dispatch discipline. Triggers on phrases like "派工", "寫派工", "draft assignment", or explicit `/draft-assignment`.
---

# draft-assignment — 派工撰寫 SOP

> By session 1 主視窗 use 的 skill。對齊 `ASSIGNMENT_TEMPLATE.md` + SESSION_1 §4 派工層紀律,降低漏紀律機率。

## 用途

派工是主視窗高頻動作,SOP 重複度高 — 模板必含元素 / §STOP 排除執行端可自處(規則 11)/ §決策已定引用規則 12 三分 / 數值門檻標 GB GiB(規則 13)/ SHA256 mirror dropdown(規則 14)/ 規則 15 派工檔名日期語意。每寫派工都得自我覆誦,skill 化降低漏紀律。

## 觸發條件

- Wayne 說「派工 X」/「寫派工」/「draft 一個派工」
- 主視窗自己決定要派工 + 讀 progress report 完整合下輪 verify
- 顯式 `/draft-assignment <task-slug>`

## 執行流程

### Step 1:讀 ASSIGNMENT_TEMPLATE.md

```powershell
$template = "D:\Work\system-setup\ASSIGNMENT_TEMPLATE.md"
```

完整讀模板,理解每個 section 的用意。**初稿格式對齊模板,不自創段落。**

### Step 2:確認 task slug + 日期

- **日期**:實機執行當天(規則 15)— 主視窗寫派工的 session 跨日,執行端 step 1.5 verify 後 rename(規則 15 落地)
  ```powershell
  $today = Get-Date -Format 'yyyy-MM-dd'
  ```
- **task-slug**:kebab-case 短描述(例 `wan22-vram-isolation` / `litellm-deepseek-route` / `comfyui-was-node-install`)

最終檔名:`assignments/<YYYY-MM-DD>_<task-slug>.md`

### Step 3:草擬派工內容(對齊 SESSION_1 §4 紀律 checklist)

逐 section 草擬,checklist 自我覆誦:

- [ ] **目標**:1-2 句話,不混入「你應該怎麼做」(那是步驟段)
- [ ] **決策已定**:引用規則 12 三分(strict 核心 / 鬆綁 supporting / 鬆綁 I/O widget),不另抄規則
- [ ] **限制**:派工硬限制清單(不擅自 retry / 不擅自整合 MD / 不擅自延伸 verify 等);若有 model 校驗,SHA256 mirror 全部 dropdown widget(規則 14)
- [ ] **前置必讀**:具體 MD 段落,不靠記憶 — grep verify 引用準確性(規則 8)
- [ ] **步驟**:每 step 含「期望輸出」+「STOP 觸發點」 — STOP 排除執行端可自處(啟動 server / 等可 poll 狀態 / 標準 retry / 跑 verify 命令不寫 STOP,規則 11)
- [ ] **完成判定**:具體可驗證條件,不寫「測試通過」這種模糊
- [ ] **邊界**:派工沒列的不做 / 不擅自延伸
- [ ] **數值門檻標 GB / GiB**(規則 13):邊界附近強制標明(VRAM 22 GB / 18 GB / 等)
- [ ] **progress report 落地路徑**:`progress-reports/<YYYY-MM-DD>_<task-slug>.md`(實機今日,規則 15)

### Step 4:跟 Wayne 確認派工內容

不直接落地 `assignments/`,先列草稿 → Wayne 改完才往下。

特別 raise:

- 引用準確性(grep verify 結果列出來)
- §決策已定 vs §限制 邊界(strict 核心對照變數哪些)
- §STOP 觸發點是否有 redundant(執行端可自處的不寫進 STOP)

### Step 5:落地 assignments/

Wayne ack 後寫檔,**.NET API 無 BOM 三 byte verify**(user-level CLAUDE.md 硬規則 1):

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("D:\Work\system-setup\assignments\<檔>", $content, $utf8NoBom)

# 三 byte 驗證
$b = [System.IO.File]::ReadAllBytes("D:\Work\system-setup\assignments\<檔>")[0..2]
"BOM check: $($b -join ',')  (期望:不是 239,187,191)"
```

### Step 6:通知 Wayne 切去 session 2

```
派工已落地 assignments/<檔名>。請切到 session 2 跟它說「讀 assignments/<檔名>」。
```

## 紀律

- **不直接觸發 session 2**(SESSION_1 §5.1 — Wayne 中介)
- **不擅自落地** — Step 4 必跟 Wayne 拍板
- **不靠記憶引用**(規則 8 evergreen) — Step 3 grep verify 各引用點;複雜派工(引用 ≥ 5)可 invoke `assignment-verifier` subagent 並行 verify
