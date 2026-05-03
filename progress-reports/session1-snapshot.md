# session1-snapshot(2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v10,2026-05-04)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 當前 anchor

**audit 規則精修批次 commit `d64c585` 落地**(本對話最大產出):

- 8 檔 modified + 1 rename(`progress-reports/progress-reports-README.md` → `README.md` 對齊 `.gitignore` 白名單)+ memory 三檔 stale 刪 + user-level CLAUDE.md 角色段改寫(working tree 外連動)
- **淨刪 152 行**(working tree 範圍 +17 / -169)
- **dogfood test 3 任務**(寫派工 / 整合 progress report / 接班 audit)全通,1 條回退(Python 版本配對 + 個人偏好 從 context.md / memory 收進 `SYSADMIN_BRIEFING.md`「已建立的軟體環境」段)
- **規則精修主軸**:重複收斂(寫檔 SOP 從 5 處 → 1 source-of-truth + 引用)/ 角色定位 fix(user CLAUDE.md「執行端」改「視 session 而定」)/ metadata sync(全 2026-05-04)/ 結構精修(memory 三檔 13-day-old + stale `D:\Models\sd\` 刪)

**規則 15「派工 / progress report 日期語意統一為實機執行當天」派工已寫對齊 audit rename**(`assignments/2026-05-04_rule-15-cross-day-relanding.md`),等 session 2 跑落地。

---

## 架構演進(2026-05-04)

無新架構演進(雙 session + subagent 三角色架構已穩,本對話聚焦規則精修 + audit)。

---

## 規則演進(2026-05-04)

**source-of-truth 分層紀律確立**(audit commit `d64c585`):

- `SYSADMIN_BRIEFING.md` = 規則 1-14 唯一定義處
- `SESSION_1_MAINWINDOW.md` / `SESSION_2_EXECUTOR.md` / project CLAUDE.md / user-level CLAUDE.md = **引用層**(改規則只動 SYSADMIN_BRIEFING,不擴散)
- `context.md` 失去獨立 source 角色:硬體 / 磁碟策略 / 工具偏好 / 端口配置 4 段刪,改 SYSADMIN_BRIEFING 引用;留「使用情境優先序 + 已完成 / 待推進階段」

**規則 15 待落地**:派工已寫,session 2 跑完落地進 `SYSADMIN_BRIEFING.md` 規則 15 + 5 檔 cross-reference(預期跨主檔 grep `規則 15` ≥9 hits)。

詳情 `SYSADMIN_BRIEFING.md` 規則 1-14 + commit `d64c585` bullet list。

---

## 工具演進(2026-05-04)

無工具變動。

---

## 等 Wayne 拍板(剩 1 條)

1. **(可選)雙 session 架構 ROI 評估**(已累積 6+ lane 經驗,可拍時機)— v10 既有等拍項目延續

(v10 既有「派工日期跨日 mismatch」議題已透過規則 15 派工拍板執行中,等 session 2 跑完即落地。)

---

## Working tree

audit commit `d64c585` 落地後 working tree clean。本對話 audit 後動的:

- `assignments/2026-05-04_rule-15-cross-day-relanding.md`(gitignored,動了 4 處對齊 audit rename)— 不入 commit
- `progress-reports/session1-snapshot.md`(本檔,v11 蓋 v10)

下批 commit 預期僅含 1 檔:

```
本對話下批 commit 預期(1 檔):
  M progress-reports/session1-snapshot.md  ← 本檔(v11 蓋 v10)
```

---

## 旁支 / 待整合

- **教訓暫存清算**:本對話累積 4 條,3 條已落地(source-of-truth 分層 / metadata sync / memory 違反 SOP 刪),1 條未落地(**dogfood test 規則精修方法論** — 動規則後跑 N 個常用任務 mock 測試 → 缺資訊就回退 → 確認無回退才 commit;本對話實證 1 回退,值不值得進規則段待主視窗下次評估)
- **規則 15 派工** — 等 session 2 跑(派工已對齊 audit rename;5 檔 patch + 1 verify-only)
- **LTX-2.3 verify**(2026-04-30):仍待整合進 `ai-models/local-models.md`(本對話未處理)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- subagent 機制 → `.claude/agents/rule-curator.md`「Invoke 場景」段
- audit 動了什麼 → `git show d64c585`(commit message 含完整 bullet list)
- 規則 15 派工狀態 → `assignments/2026-05-04_rule-15-cross-day-relanding.md`
- 對應任務 progress report → Wayne 貼來時讀

工作紀律:

1. 不在第二段就跳結論,等 Wayne 給任務再分析
2. 指控既有 MD 有 bug 前先 grep verify(規則 8 evergreen)
3. STOP 上報攤候選時按規則 9 訂正版(工程選擇可弱 / 強推 + ≤3 選項;系統決策嚴格中性)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 落地 `assignments/`,告訴 Wayne 切去 session 2 跑
5. 不主動 git commit / push,交給 session 2(紀律 source-of-truth user-level CLAUDE.md 硬規則 4)
6. invoke rule-curator subagent 場景見 `.claude/agents/rule-curator.md`「Invoke 場景」段(SESSION_1 §5.4 已改引用,不重抄)

---

## 關鍵紀律提醒(本對話新訂正)

1. **source-of-truth 分層紀律**(audit 確立):SYSADMIN_BRIEFING 是規則層唯一 source,SESSION_* / CLAUDE.md / templates 是引用層;改規則只動 SYSADMIN_BRIEFING,引用層自然 sync
2. **dogfood test 方法論**(暫存教訓):規則精修動完後跑 3 個常用任務 mock 看缺什麼,缺資訊就回退 → 確認無回退才寫 commit 派工。實證 audit 跑出 1 回退(Python 版本配對 + 個人偏好 收進 SYSADMIN_BRIEFING),其他 0 回退
3. **memory SOP 執行紀律**:不存「可從 current state 推導」的內容(可推導的會 stale 誤導;實證 user_profile / disk_strategy / setup_2026-04-20 三檔 13 days 後 stale + 路徑漂移,本對話刪)
4. **派工 anchor 紀律**:派工 §決策已定 patch 落點寫**文字 anchor**(規則 14 結尾文字 + `## 標題`)而非 line number,跨 audit 仍可用 — 實證 audit 動 SYSADMIN_BRIEFING.md 但規則 15 派工 anchor 仍對齊 ✓
5. **rename 跨檔 cross-reference 對齊**:rename 實機檔對齊既有 4 處引用前先 grep verify(本次 progress-reports README rename 4 處引用本來就寫「README.md」標準命名,實機檔對齊白名單後自然全對齊;若引用是「progress-reports-README」則需同步動)

---

**蓋掉**:v10(2026-05-03)
**v11 更新理由**:audit 規則精修批次 commit `d64c585` 落地 + 規則 15 派工已寫等 session 2 跑 + source-of-truth 分層紀律確立 + dogfood test 方法論暫存教訓 + memory 三檔 stale 刪
