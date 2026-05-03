# session1-snapshot(2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v11,2026-05-04)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 當前 anchor

本對話 3 個 commit 全落地 origin/main + working tree clean:

- **`d64c585` audit 規則精修批次清理**(淨刪 152 行 / 8 檔 modified + 1 rename + memory 三檔刪 / dogfood test 3 任務全通 1 條回退)
- **`398e88d` v11 snapshot 蓋 v10**
- **`052f040` 規則 15 落地**(5 檔 patch + SESSION_1/2 §4 標題連帶訂正 1-14 → 1-15)

**規則 15「派工 / progress report 日期語意統一為實機執行當天」完整落地**:跨主檔 grep `規則 15` 11 hits ≥ 9 門檻;self-eat-dogfood 通過(派工檔名 = 實機今日 match=True);跨日 rename 場景待跨日跑時自然觸發實證。

**規則總數 stable 1-15**(audit + 規則 15 兩輪 follow-up 完成)。

---

## 架構演進(2026-05-04)

無新架構演進(雙 session + subagent 三角色架構穩定,本對話聚焦規則精修 + 規則 15 落地)。

---

## 規則演進(2026-05-04)

**source-of-truth 分層紀律完整實施**(audit `d64c585` + 規則 15 `052f040`):

- `SYSADMIN_BRIEFING.md` = 規則 1-15 唯一定義處
- `SESSION_1_MAINWINDOW.md` / `SESSION_2_EXECUTOR.md` / `CLAUDE.md`(user + project)/ templates = **引用層**(改規則只動 SYSADMIN_BRIEFING,引用層自然 sync;§4 標題「規則 1-N」是引用層典型 sync 點)
- `context.md` 失去獨立 source 角色(audit 已收進 SYSADMIN_BRIEFING)
- `progress-reports/README.md` 命名對齊 `.gitignore` 白名單(audit rename `progress-reports-README.md` → `README.md`)

**規則 15 完整落地**:
- SYSADMIN_BRIEFING.md 規則 14 後加 ### 規則 15 整段(為什麼 / step 1.5 verify / 主視窗派工撰寫紀律 / 實證踩坑四子段)
- SESSION_2_EXECUTOR.md §3.1 加 step 1.5 規則 15 verify PowerShell 腳本(讀派工後立刻 verify 派工檔名日期 = 實機今日,mismatch 觸發 rename + progress report 用 $today)
- ASSIGNMENT_TEMPLATE / PROGRESS_TEMPLATE / SESSION_1_MAINWINDOW 引用層 cross-reference 全對齊

詳情 `SYSADMIN_BRIEFING.md` 規則 1-15 + 3 commits bullet list。

---

## 工具演進(2026-05-04)

無工具變動。

---

## 等 Wayne 拍板(剩 1 條)

1. **(可選)雙 session 架構 ROI 評估**(已累積 6+ lane 經驗,可拍時機)— v10 / v11 既有等拍項延續

(派工日期跨日 mismatch 議題已透過規則 15 落地解;主視窗 / 執行端 step 1.5 自動處理。)

---

## Working tree

3 commits push 後 clean:

```
git log --oneline -3:
  052f040 docs(rules): 規則 15 落地
  398e88d docs(snapshot): session1-snapshot v11 蓋 v10
  d64c585 audit: 規則精修批次清理

git status: working tree clean, branch up-to-date with origin/main
```

下批 commit 預期僅含 v12 snapshot 蓋 v11:

```
本對話下批 commit 預期(1 檔):
  M progress-reports/session1-snapshot.md  ← 本檔(v12 蓋 v11)
```

---

## 旁支 / 待整合

- **教訓暫存清算**:本對話累積 5 條,4 條已落地(source-of-truth 分層 / metadata sync / memory 違反 SOP 刪 / 派工 anchor 紀律 dogfood 通過),1 條未落地(**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段)
- **跨日 mismatch dogfood 實證**:本次 match=True 不需 rename(verify path 走通);rename 場景待下次 session 2 跨日跑時自然觸發實證
- **LTX-2.3 verify**(2026-04-30):仍待整合進 `ai-models/local-models.md`(本對話未處理)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- subagent 機制 → `.claude/agents/rule-curator.md`「Invoke 場景」段
- 本對話 commits 細節 → `git show d64c585` / `git show 052f040`(commit message 含完整 bullet list)
- 對應任務 progress report → Wayne 貼來時讀

工作紀律:

1. 不在第二段就跳結論,等 Wayne 給任務再分析
2. 指控既有 MD 有 bug 前先 grep verify(規則 8 evergreen)
3. STOP 上報攤候選時按規則 9 訂正版(工程選擇可弱 / 強推 + ≤3 選項;系統決策嚴格中性)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 落地 `assignments/`(檔名日期 = 實機今日,規則 15)
5. 不主動 git commit / push,交給 session 2(紀律 source-of-truth user-level CLAUDE.md 硬規則 4)
6. invoke rule-curator subagent 場景見 `.claude/agents/rule-curator.md`「Invoke 場景」段(SESSION_1 §5.4 已改引用,不重抄)

---

## 關鍵紀律提醒(本對話新訂正)

1. **source-of-truth 分層紀律**(audit + 規則 15 兩輪實施完成):SYSADMIN_BRIEFING 是規則層唯一 source;SESSION_*/CLAUDE.md/templates 是引用層;改規則只動 SYSADMIN_BRIEFING,引用層 sync 自然(典型 sync 點:SESSION_1/2 §4 標題「規則 1-N」隨規則總數變動)
2. **dogfood test 方法論**(暫存教訓):規則精修動完後跑 3 個常用任務 mock 看缺什麼,缺資訊就回退 → 確認無回退才寫 commit 派工。實證 audit 跑出 1 回退(Python 版本配對 + 個人偏好 收進 SYSADMIN_BRIEFING)
3. **memory SOP 執行紀律**:不存「可從 current state 推導」的內容;違反會 stale 誤導(實證 user_profile / disk_strategy / setup_2026-04-20 三檔 13 days 後 stale + 路徑漂移 `D:\Models\sd\` vs `diffusion`,本對話刪)
4. **派工 anchor 紀律**(規則 15 落地實證 ✓):派工 §決策已定 patch 落點寫**文字 anchor**(規則 14 結尾文字 + `## 標題`)而非 line number,跨 audit / 規則新增仍對齊 — 規則 15 patch 後 SYSADMIN_BRIEFING `## 文件導航` 從 line 631 漂到 647(+16 行)文字 anchor 仍 0 漂移 ✓
5. **rename 跨檔 cross-reference 對齊**(audit 實施):rename 實機檔對齊既有引用前先 grep verify;若引用本來就對齊白名單命名(progress-reports/README.md),rename 後自然全對齊(本對話實證:.gitignore + assignments/README.md + skill + SYSADMIN_BRIEFING 4 處引用 0 動)
6. **規則 15 self-eat-dogfood**:派工檔名日期 = 實機執行當天(session 2 step 1.5 verify);跨日場景 rename 派工檔對齊 + progress report 用 $today;主視窗派工撰寫紀律不預判跨日,執行端 verify

---

**蓋掉**:v11(2026-05-04)
**v12 更新理由**:規則 15 落地 commit `052f040` 完成 + 規則總數 stable 1-15 + SESSION_1/2 §4 標題訂正 + dogfood 派工 anchor 紀律實證通過 + 跨日 rename 場景待跨日跑實證
