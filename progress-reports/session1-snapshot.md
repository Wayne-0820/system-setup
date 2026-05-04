# session1-snapshot(v17,2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v16 commit `98d9cc4`,2026-05-04;Batch 1 規則 patch commit `e3df754` 已落地 origin/main 為 v17 trigger anchor)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**待 Wayne 拍板:Batch 2 snapshot v17 commit 派工**(本檔 v17 single-file commit + push origin/main,對齊歷史 snapshot commit pattern,例 `cf1a96d` v15 / `98d9cc4` v16)。

主視窗已重寫本檔 v17 落地 working tree,等 Wayne 拍板:

- (a)主視窗草擬 Batch 2 commit 派工 → 切 session 2 跑 → 本對話完整 close
- (b)暫緩 Batch 2,本對話收尾(working tree 留 snapshot.md dirty handoff 到下次接手)

---

## 當前 anchor

**本對話新落地(已 commit `e3df754` + push origin/main):最小規則收斂 Batch 1**

Batch 1 兩 patch 同批 commit(2 檔 / +8 行 / -0):

- **`e3df754`** docs(rules): 最小規則收斂 — SESSION1 draft 自修紀律 + Codex sandbox 坑 #3
  - `SESSION_1_MAINWINDOW.md` §4 派工層紀律 新增 bullet「Draft 數字 mismatch 自修不問」(+1 行):draft 派工 / snapshot / MD patch 撞列項數 / 加總 / 總數不一致時 SESSION1 自實機 verify + 修正 draft;僅限算術 / 列項類,改策略 / 刪檔範圍 / commit scope 仍 STOP
  - `codex/setup.md` §踩坑紀錄 新增坑 #3(+7 行):PowerShell here-string body 含 `Remove-Item` 字樣撞 Claude Code sandbox keyword scan 攔(訊息 `Remove-Item on system path '/' is blocked.`)— 解法用 Write 工具
  - memory `feedback_main_window_self_correct_arithmetic.md` 升級成 SESSION_1 規則 hook(接班 session 1 讀角色定義即拿到紀律)

**Codex 三件套 lane 累積進度**(延續 v16):

- Lane B(mirror artifacts probe)→ 已收尾 `9e16a6c`
- Lane C(hand-craft AGENTS.md source-of-truth)→ 已收尾 `f1d6c3f`
- Lane A(sandbox root cause 追)→ 獨立未拍板
- Lane D(平行用法實測)→ 獨立未拍板

**最新 5 commit**(origin/main):

- `e3df754` docs(rules): 最小規則收斂 — SESSION1 draft 自修紀律 + Codex sandbox 坑 #3(本對話 Batch 1)
- `98d9cc4` docs(snapshot): session1-snapshot v16 蓋 v15 — Lane C 收尾與 cleanup 計畫
- `f1d6c3f` docs(repo): add hand-crafted Codex AGENTS instructions(Lane C 收尾)
- `cf1a96d` docs(snapshot): session1-snapshot v15 蓋 v14
- `9e16a6c` docs(codex): integrate Lane B mirror probe results

---

## 規則演進(2026-05-04 v17)

`SESSION_1_MAINWINDOW.md` §4 派工層紀律 +1 bullet「Draft 數字 mismatch 自修不問」:

- 不升級成 SYSADMIN_BRIEFING.md 規則段(屬主視窗 draft 自修紀律,非全機器通用規則)
- 對齊 memory `feedback_main_window_self_correct_arithmetic.md` 升級成正式 hook
- 規則總數 stable 1-15(本批屬 SESSION_1 派工層紀律 list 內精修)

`codex/setup.md` §踩坑紀錄 +坑 #3「PowerShell here-string sandbox keyword scan 誤擋」:

- 對齊 v16 紀律提醒 #8「codex pitfall 範圍紀律」(子目錄 setup.md 落地,不升級全域行為規則)
- 樣本 1 例;同類延伸場景則往坑 #3 §解法添加(本對話新增「commit message 含敏感字樣」場景已暫存 v17 候選 reminder,不入主 MD)

---

## 工具演進

無(本對話為純規則 patch 收斂)。

---

## v17 候選清單(瘦身後)

### 已落地(從未決候選移出,本批 commit `e3df754`)

1. ~~17/18 算術 mismatch~~ → SESSION_1 §4 bullet 已落地
2. ~~PowerShell here-string sandbox keyword 誤觸~~ → codex/setup.md 坑 #3 已落地

### 觀察候選(保留;只是觀察,不主動推進升級)

3. **cleanup 規則首次行使 dogfood**(v16 + cleanup 派工 2 完整實證):流程 SOP 可行,僅 step 8 撞 sandbox hook(已升級坑 #3 落地)。評估規則段是否需精修(防呆 / 派工模板 / cleanup 拆批策略)— 累積樣本 1 例
4. **AGENTS.md 雙路徑分流紀律**(v16 Lane C 拍板落實):hand-crafted source-of-truth 入 git history;Codex 桌面板 auto-mirror 持續精準 .gitignore 隔離 — 觀察候選,不需升級
5. **commit 派工 special verify step 模板化候選**(Lane C 派工實證):值得作為 commit 派工模板「special verify」段範例(Wayne 自決是否落 `ASSIGNMENT_TEMPLATE.md`)

### 本批整合衍生(暫存 snapshot reminder,Wayne 拍 c — 不升級主 MD / skill)

6. **commit message 草稿含 sandbox 黑名單字樣 → SESSION2 自處 `git commit -F <file>` 路線**(本批 progress report `2026-05-04_commit-rules-batch-1.md` §4 教訓):性質屬坑 #3 同源延伸(sandbox keyword scan 從 here-string body → command line literal);Wayne 拍板 c 暫存 reminder,僅 1 例樣本累積後再評估升級。SESSION2 在派工沒明寫情況下自處(規則 11「執行端可自處」),未撞 STOP

---

## 剩餘 Wayne 拍板項(延續 v16,本對話無新增 lane)

1. **Lane A:sandbox root cause 追**(中)— GitHub issue / Claude Code permission mode 試 / 接受 sandbox 限制
2. **Lane D:平行用法實測**(中)— Codex 桌面板 / CLI 直接跑 review 確認不撞 sandbox
3. **WAN2.2 wrapper/native trade-off 拍板**(主視窗評估 #3c 後續路徑)— v14 延續
4. **dogfood test 方法論**(動規則後跑 N 個常用任務 mock 測試)— v12 / v13 / v14 / v15 / v16 / v17 連六 snapshot 延續未落地
5. **(可選)雙 session 架構 ROI 評估**(已累積 7+ lane 經驗,可拍時機)

---

## Working tree

**git HEAD = origin/main = `e3df754`**(synced,Batch 1 規則 patch commit)

1 檔 dirty:

```
git status:
  M  progress-reports/session1-snapshot.md  ← 本檔(v17 rewrite,等 Batch 2 commit)
```

下一個 commit = **Batch 2**:本檔 single-file commit + push,對齊歷史 snapshot commit pattern。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12-v17 連六 snapshot 延續):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:本次主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **codex 後續 lane**:Lane A / D 獨立未拍板,Wayne 自決時機(Lane B + C 已收尾)
- **下次 cleanup 候選**:本檔 v17 commit + push 落地後,`progress-reports/` 可清舊 raw reports — 候選 3 檔(`2026-05-04_commit-snapshot-v16.md` + `2026-05-04_cleanup-raw-reports.md` + `2026-05-04_commit-rules-batch-1.md`),保留 README + session1-snapshot;cleanup 派工由下次主視窗自決時機(避免本對話 scope 漂移)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到 v17 anchor + 等什麼。

**最優先動作**:Wayne 拍板 Batch 2 snapshot v17 commit 派工 → 主視窗草擬 → 切 session 2 跑(對齊歷史 snapshot commit pattern)。常見接手場景:

- (a)Wayne 想直接拍 Batch 2 commit 派工:主視窗草擬本檔 single-file commit + push 派工
- (b)Wayne 暫緩 Batch 2,只想 audit / 整合 / 對話:不需動派工(working tree 留 snapshot.md dirty handoff 到下次接手)
- (c)Wayne 想拍其他 lane(A / D / WAN2.2 / dogfood / 雙 session ROI):走規劃 + 派工流程

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`(本對話 §4 派工層紀律 +1 bullet)
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(v14 落地;§5 規範往後新增比照辦理)
- **Codex 整合** → `codex/setup.md`(三件套配置 + sandbox 半通踩坑 + mirror 紀律 + Lane A/D + 本對話新增坑 #3)+ root `AGENTS.md`(hand-crafted Codex source-of-truth,Lane C 落地)
- **progress-reports cleanup 規則** → `progress-reports/README.md`(生命週期段 + 防呆段)
- **memory feedback** → `memory/feedback_main_window_self_correct_arithmetic.md`(已升級成 SESSION_1 §4 規則 hook)
- subagent invoke 細節 → 個別 `.claude/agents/<name>.md`「Invoke 場景」段
- skill 觸發細節 → 個別 `.claude/skills/<name>/SKILL.md`「觸發條件」段
- 對應任務 progress report → Wayne 貼來時讀

工作紀律:

1. 不在第二段就跳結論,等 Wayne 給任務再分析
2. 指控既有 MD 有 bug 前先 grep verify(規則 8 evergreen)
3. STOP 上報攤候選時按規則 9 訂正版(工程選擇可弱 / 強推 + ≤3 選項;系統決策嚴格中性)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 落地 `assignments/`(檔名日期 = 實機執行當天,規則 15;可觸發 `draft-assignment` skill 加速)
5. 不主動 git commit / push,交給 session 2(紀律 source-of-truth user-level CLAUDE.md 硬規則 4;觸發 `dispatch-commit` skill 草擬 commit 派工)
6. invoke subagent 場景見對應 `.claude/agents/<name>.md`「Invoke 場景」段(主視窗可用:`rule-curator` / `community-researcher` / `assignment-verifier`)
7. **Codex 三件套整合對齊 `codex/setup.md` + root `AGENTS.md`**:plugin sandbox 半通(坑 #1)/ 桌面板 mirror-like artifacts(坑 #2)/ PowerShell sandbox keyword scan(坑 #3,本對話新增)/ `.agents/skills/` `.codex/agents/` 精準 .gitignore 隔離 / hand-crafted AGENTS.md 入 git history
8. **progress-reports cleanup 對齊 `progress-reports/README.md`**:snapshot 蓋掉 + commit/push 落地後可清舊 raw reports(防呆:只刪 `*.md` 不刪 `README.md`;未整合 / 未拍板 STOP 不刪;不確定 STOP 問 Wayne)
9. **算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne**(已升級成 SESSION_1 §4 派工層紀律 bullet,commit `e3df754`):自實機 verify(`Get-ChildItem` / `git ls-files` / `Test-Path` 等)+ 修正 draft + 回報「已自修正」短訊息;STOP 限策略 / 範圍 / scope 變更或 STOP 真觸發

---

## 關鍵紀律提醒(v15 + v16 延續 + v17 整合衍生)

**v15 / v16 延續**(累積 11 條,本對話無新增於既有條目):

1. **subagent / skill 隸屬紀律**:新增 subagent / skill 比照 `SUBAGENT_AND_SKILL_CATALOG.md` §5
2. **§7 鬆綁實證**:主視窗想查社群實踐 → invoke `community-researcher` subagent;對齊規則 10 升級版
3. **派工 / commit / progress report 高頻動作 skill 化**:`draft-assignment` / `dispatch-commit` / `integrate-progress-report` 對應 SESSION_1 §4 / §5.3 / §5.2 標準動作
4. **措辭嚴謹度抓 over-claim**:Wayne 在 v15 階段抓 3 次主視窗 over-claim — 整合進主 MD 時要 distinguish「實證」vs「推測」vs「未實測」,**不能寫太滿**
5. **probe by rename, not delete**(Lane B 拍板):auto-generated artifact 探查紀律 — 用 `Rename-Item` 保留原檔當 backup,**不用刪檔當 probe**(避免污染環境判讀)
6. **派工字面執行 vs 範圍漂移**:主視窗寫派工時要對齊原拍板,session 2 STOP raise 抓到後修正
7. **session 2 step mismatch raise clarify**:派工 step 預期失效時 session 2 嚴格 verify 後 raise clarify,不擅自跳過 / 不擅自繼續
8. **codex pitfall 範圍紀律**(Wayne 拍板):Codex setup / sandbox pitfall 落 `codex/setup.md`,**不升級成全域行為規則** — 工具 specifics 進子目錄 setup.md
9. **AGENTS.md 雙路徑分流紀律**(v16 Lane C 拍板落實):hand-crafted source-of-truth 入 git history;Codex 桌面板 auto-mirror artifacts 持續精準 .gitignore 隔離
10. **commit 派工 special verify step 模板化候選**(v16 Lane C 派工實證):值得作為 commit 派工模板「special verify」段範例
11. **cleanup 規則首次行使 dogfood**(v16 + cleanup 派工 2 完整實證):snapshot 蓋掉 + cleanup 流程 SOP 可行

**v17 已升級成正式落地**(本對話 Batch 1 commit `e3df754`,從 reminder → SESSION_1 / codex/setup.md 規則 hook):

12. ~~算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne~~ → SESSION_1 §4 派工層紀律 bullet 落地
13. ~~PowerShell here-string 含 sandbox 敏感 keyword 誤觸 hook~~ → codex/setup.md 坑 #3 落地

**v17 整合衍生**(2026-05-04 Batch 1 progress report 整合衍生,**未升級成規則段**,僅接班 reminder,Wayne 拍 c):

14. **commit message 草稿含 sandbox 黑名單字樣 → SESSION2 自處 `git commit -F <file>` 路線**(性質屬坑 #3 同源延伸):Write 工具寫 message 到 `$env:TEMP\<file>.txt` → `git commit -F <path>`(命令列只含路徑,不含敏感字樣)。SESSION2 規則 11 範疇自處未撞 STOP;暫存 reminder,Wayne 拍板 c 不升級主 MD / skill

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v16 commit `98d9cc4`(2026-05-04)
**v17 更新理由**:本對話最小規則收斂 Batch 1 commit `e3df754` 落地 origin/main(`SESSION_1_MAINWINDOW.md` §4 派工層紀律 +1 bullet「Draft 數字 mismatch 自修不問」+ `codex/setup.md` §踩坑紀錄 +坑 #3「PowerShell here-string sandbox keyword scan 誤擋」)。v17 候選清單瘦身:已落地 2 條移出未決候選,觀察候選保留 3 條(cleanup dogfood / AGENTS.md 雙路徑 / commit special verify 模板化),本批整合衍生 1 條(commit message `-F` 路線)暫存 reminder,Wayne 拍 c 不升級主 MD / skill。剩 5 條等拍項延續 v16(Lane A / D / WAN2.2 / dogfood / 雙 session ROI)。
