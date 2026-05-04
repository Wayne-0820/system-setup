# session1-snapshot(v18,2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v17 commit `0b4bf9f`,2026-05-04;Lane D1 收尾 commit `d2fb5d8` 已落地 origin/main 為 v18 trigger anchor)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**待 Wayne 拍板:Batch snapshot v18 commit 派工**(本檔 v18 single-file commit + push origin/main,對齊歷史 snapshot commit pattern,例 `0b4bf9f` v17 / `98d9cc4` v16 / `cf1a96d` v15)。

主視窗已重寫本檔 v18 落地 working tree,等 Wayne 拍板:

- (a)主視窗草擬 commit 派工 → 切 session 2 跑 → 本對話完整 close
- (b)暫緩 commit,本對話收尾(working tree 留 snapshot.md dirty handoff 到下次接手)

---

## 當前 anchor

**本對話新落地(已 commit `d2fb5d8` + push origin/main):Lane D1 收尾 — Codex CLI direct review sandbox 實測失敗文件化**

Lane D1 cross-verify 社群 `openai/codex-plugin-cc#57` 在 Wayne 機器**實測失敗**(Wayne 親跑獨立 PowerShell `codex review --uncommitted -c 'sandbox_permissions=["disk-full-read-access"]'` 仍撞 `CreateProcessAsUserW failed: 5`,訊息與既有坑 #1 完全一致)。

`d2fb5d8` 單檔 commit(`codex/setup.md` 三段更新,15 insertions / 10 deletions):

- **坑 #1 §平行用法段**:推測未實測 → 實測失敗;**關鍵發現**:sandbox 失敗**不限於** Claude Code 嵌套 spawn(完全脫離任何 wrapper 仍撞);本坑問題定位範圍暫擴大為「Codex CLI Windows sandbox 環境問題」
- **§未來 lane > Lane A**(候選清單升級):加查 `CreateProcessAsUserW` / `disk-full-read-access` GitHub issue + verify outside-scope a/b/c(`-c sandbox_permissions=...` 是否被讀);Claude Code permission mode 候選降級(D1 證明獨立 PowerShell 也撞)
- **§未來 lane > Lane D**:標 D1 失敗;D2 桌面板 GUI 未測,**不能再以 D1 通則推論 D2 也通**

**Codex 三件套 lane 累積進度**(更新):

- Lane B(mirror artifacts probe)→ 已收尾 `9e16a6c`
- Lane C(hand-craft AGENTS.md source-of-truth)→ 已收尾 `f1d6c3f`
- **Lane D1(CLI direct review workaround)→ 已收尾 `d2fb5d8`**(失敗模式文件化)
- Lane D2(桌面板 GUI 平行用法)→ 未測,Wayne 自決時機
- Lane A(sandbox root cause 追)→ 候選清單已升級(D1 失敗後反映在 `codex/setup.md`),Wayne 自決時機

**最新 5 commit**(origin/main):

- `d2fb5d8` docs(codex): record Lane D1 CLI review sandbox failure(本對話 Lane D1 收尾)
- `0b4bf9f` docs(snapshot): session1-snapshot v17 蓋 v16 — 最小規則收斂落地與候選瘦身
- `e3df754` docs(rules): 最小規則收斂 — SESSION1 draft 自修紀律 + Codex sandbox 坑 #3
- `98d9cc4` docs(snapshot): session1-snapshot v16 蓋 v15 — Lane C 收尾與 cleanup 計畫
- `f1d6c3f` docs(repo): add hand-crafted Codex AGENTS instructions(Lane C 收尾)

---

## 規則演進(2026-05-04 v18)

**無新規則**。本對話為 `codex/setup.md` 子目錄段更新(坑 #1 §平行用法 + Lane A + Lane D),對齊紀律 #8「Codex pitfall 落 codex/setup.md,不升級全域行為規則」。

規則總數 stable 1-15。

---

## 工具演進

無(本對話為 codex pitfall 文件化,非工具 / 模型新增)。

---

## v18 候選清單

### 觀察候選(保留;只是觀察,不主動推進升級)

(延續 v17 觀察候選清單,本對話無新增 / 無移出)

1. **cleanup 規則首次行使 dogfood**(v16 + cleanup 派工 2 完整實證):流程 SOP 可行,僅 step 8 撞 sandbox hook(已升級坑 #3 落地)— 累積樣本 1 例
2. **AGENTS.md 雙路徑分流紀律**(v16 Lane C 拍板落實):觀察候選,不需升級
3. **commit 派工 special verify step 模板化候選**(Lane C 派工實證):值得作為 commit 派工模板「special verify」段範例(Wayne 自決是否落 `ASSIGNMENT_TEMPLATE.md`)

### 延續 v17 reminder(暫存,Wayne 拍 c 不升級主 MD / skill;累積樣本上升)

4. **commit message 草稿含 sandbox 黑名單字樣 → SESSION2 自處 `git commit -F <file>` 路線**(v17 Batch 1 progress report §4 教訓):
   - **累積樣本**:本對話 Batch 1(Remove-Item 字樣)→ Batch 2(snapshot v17 multiline)→ Lane D1 commit(multiline + `[]` 字元)= **三次連續 SESSION2 自處用 `-F file` 路線**
   - 性質仍屬規則 11「執行端可自處」範疇,未撞 STOP
   - Wayne 拍 c 不升級主 MD / skill 仍適用,但下次寫 v19 snapshot 時可再評估升級時機(規則 / skill / progress report PROGRESS_TEMPLATE 提示)

---

## 剩餘 Wayne 拍板項(本對話 Lane D1 收尾,Lane D2 獨立列出)

1. **Lane A:sandbox root cause 追**(候選清單已升級反映在 `codex/setup.md`)— 中 — Wayne 自決時機
2. **Lane D2:Codex 桌面板 GUI 平行用法實測**(社群證據不足,D1 失敗後 D2 不能假設會通)— 低 — Wayne 自決時機
3. **WAN2.2 wrapper/native trade-off 拍板**(主視窗評估 #3c 後續路徑)— v14 延續
4. **dogfood test 方法論**(動規則後跑 N 個常用任務 mock 測試)— v12-v18 連七 snapshot 延續未落地
5. **(可選)雙 session 架構 ROI 評估**(已累積 8+ lane 經驗,可拍時機)

---

## Working tree

**git HEAD = origin/main = `d2fb5d8`**(synced,Lane D1 收尾 commit)

1 檔 dirty:

```
git status:
  M  progress-reports/session1-snapshot.md  ← 本檔(v18 rewrite,等 Batch commit)
```

下一個 commit = **Batch snapshot v18**:本檔 single-file commit + push,對齊歷史 snapshot commit pattern。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12-v18 連七 snapshot 延續):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:本次主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **codex 後續 lane**:Lane A / D2 獨立未拍板,Wayne 自決時機(Lane B + C + D1 已收尾)
- **下次 cleanup 候選**:本檔 v18 commit + push 落地後,`progress-reports/` 可清舊 raw reports — 候選 6 檔(`2026-05-04_commit-snapshot-v16.md` + `2026-05-04_cleanup-raw-reports.md` + `2026-05-04_commit-rules-batch-1.md` + `2026-05-04_commit-snapshot-v17.md` + `2026-05-04_lane-d1-cli-review-probe.md` + `2026-05-04_commit-codex-lane-d1.md`),保留 README + session1-snapshot;cleanup 派工由下次主視窗自決時機(避免本對話 scope 漂移)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到 v18 anchor + 等什麼。

**最優先動作**:Wayne 拍板 Batch snapshot v18 commit 派工 → 主視窗草擬 → 切 session 2 跑(對齊歷史 snapshot commit pattern)。常見接手場景:

- (a)Wayne 想直接拍 commit 派工:主視窗草擬本檔 single-file commit + push 派工
- (b)Wayne 暫緩 commit,只想 audit / 整合 / 對話:不需動派工(working tree 留 snapshot.md dirty handoff 到下次接手)
- (c)Wayne 想拍其他 lane(A / D2 / WAN2.2 / dogfood / 雙 session ROI):走規劃 + 派工流程

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`(v17 Batch 1 §4 派工層紀律 +1 bullet)
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(v14 落地;§5 規範往後新增比照辦理)
- **Codex 整合** → `codex/setup.md`(三件套配置 + sandbox / mirror / keyword scan 踩坑 + mirror 紀律 + Lane A/D + 本對話 Lane D1 收尾文件化)+ root `AGENTS.md`(hand-crafted Codex source-of-truth,Lane C 落地)
- **progress-reports cleanup 規則** → `progress-reports/README.md`(生命週期段 + 防呆段)
- **memory feedback** → `memory/feedback_main_window_self_correct_arithmetic.md`(已升級成 SESSION_1 §4 規則 hook,v17 commit `e3df754`)
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
7. **Codex 三件套整合對齊 `codex/setup.md` + root `AGENTS.md`**:plugin sandbox 半通(坑 #1)/ 桌面板 mirror-like artifacts(坑 #2)/ PowerShell sandbox keyword scan(坑 #3)/ Lane D1 CLI direct review 失敗(坑 #1 §平行用法段)/ `.agents/skills/` `.codex/agents/` 精準 .gitignore 隔離 / hand-crafted AGENTS.md 入 git history
8. **progress-reports cleanup 對齊 `progress-reports/README.md`**:snapshot 蓋掉 + commit/push 落地後可清舊 raw reports(防呆:只刪 `*.md` 不刪 `README.md`;未整合 / 未拍板 STOP 不刪;不確定 STOP 問 Wayne)
9. **算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne**(已升級成 SESSION_1 §4 派工層紀律 bullet,commit `e3df754`):自實機 verify(`Get-ChildItem` / `git ls-files` / `Test-Path` 等)+ 修正 draft + 回報「已自修正」短訊息;STOP 限策略 / 範圍 / scope 變更或 STOP 真觸發

---

## 關鍵紀律提醒(v15 + v16 延續 + v17 已升級 + v17/v18 整合衍生)

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

**v17 已升級成正式落地**(commit `e3df754`,從 reminder → SESSION_1 / codex/setup.md 規則 hook):

12. ~~算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne~~ → SESSION_1 §4 派工層紀律 bullet 落地
13. ~~PowerShell here-string 含 sandbox 敏感 keyword 誤觸 hook~~ → codex/setup.md 坑 #3 落地

**v17/v18 整合衍生**(暫存 reminder,Wayne 拍 c 不升級主 MD / skill;**累積樣本上升**):

14. **commit message 草稿含 sandbox 黑名單字樣 → SESSION2 自處 `git commit -F <file>` 路線**(v17 Batch 1 progress report §4 教訓 + v18 持續累積):
    - **累積樣本**:Batch 1(Remove-Item)/ Batch 2(multiline)/ Lane D1 commit(multiline + `[]` 字元)= **三次連續 SESSION2 自處**
    - 性質仍屬規則 11「執行端可自處」範疇,未撞 STOP
    - Wayne 拍 c 不升級仍適用,下次寫 v19 snapshot 可再評估升級時機

**v18 整合衍生**(本批新增,Wayne 拍 — 不升級正式規則 / 不自動 gate / 不新增 workflow):

15. **Codex review handoff pattern(輕量候選)**:SESSION1 寫完 snapshot / 規則 patch / 派工草案後,若 Wayne **顯式指定** Codex review,只交 diff 摘要 + scope + dirty status 給 Codex;Codex 回 `APPROVE` / `TRIM` / `BLOCK`,SESSION1 只依 verdict 修正,不展開新決策包。**不自動 gate 所有輸出**;不寫進 `SESSION_1_MAINWINDOW.md` / 不寫進 `dispatch-commit` skill / 不新增 workflow

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v17 commit `0b4bf9f`(2026-05-04)
**v18 更新理由**:本對話 Lane D1 收尾 commit `d2fb5d8` 落地 origin/main(`codex/setup.md` 三段更新:坑 #1 §平行用法段「推測未實測 → 實測失敗」+ Lane A 候選清單升級 + Lane D 標 D1 失敗 / D2 不能假設會通)。Codex 三件套 lane 累積:Lane B + C + D1 已收尾 / Lane D2 + Lane A 仍 Wayne 自決時機。剩 5 條等拍項(Lane A 候選清單已升級反映在 codex/setup.md / Lane D2 從 Lane D 細分獨立 / WAN2.2 / dogfood / 雙 session ROI 延續)。v17 整合衍生 #14(commit message `-F` 路線)累積樣本上升至三次,Wayne 拍 c 不升級仍適用,下次寫 v19 可再評估升級時機。
