# session1-snapshot(2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v15,2026-05-04)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**無立即動作**。本對話 codex-plugin-cc lane Lane C 收尾 commit `f1d6c3f` 已落地 origin/main。Lane B + Lane C 雙收尾;Lane A / D 獨立未拍板。

**下下批 commit + cleanup 待跑**(兩階段,對齊 cleanup 策略拍板 A):

- 階段 1:主視窗派下下批 commit 派工 `assignments/2026-05-04_commit-snapshot-v16.md`(本檔 v16 蓋 v15 單檔 commit + push)
- 階段 2:snapshot v16 落地 origin/main 後,主視窗派 cleanup 派工(session 2 單批 `Remove-Item` 清 Group A 14 檔 + Group B 1 檔 = 15 份 raw reports;保留 `progress-reports/README.md` + `progress-reports/session1-snapshot.md`)

cleanup 拍板理由:Group B(`2026-05-04_commit-codex-agents.md`)目前尚未被 v16 snapshot frozen 進 git history,現在不清;等 v16 落地後一次清,避免 cleanup 派工碎成兩批。

跨日場景:session 2 step 1.5 自動 rename 派工檔對齊實機今日(規則 15)— 接班時檔名可能已從 `2026-05-04_*` 變成 `<實機今日>_*`。

執行端跑完寫 progress report 落地 `progress-reports/<$today>_commit-snapshot-v16.md` → Wayne 切回 session 1「讀 progress-reports/<檔>」整合(預期無 patch、無教訓、單檔 commit 收尾)。

---

## 當前 anchor

**本對話新落地(已 commit `f1d6c3f` + push origin/main):codex-plugin-cc lane Lane C 完整收尾(hand-crafted AGENTS.md 入駐 + cleanup 規則落地)**

Lane C 收尾(6 檔單批 commit):

- **`f1d6c3f`** docs(repo): add hand-crafted Codex AGENTS instructions
  - root `AGENTS.md` 新增 178 行(hand-crafted Codex source-of-truth,非 mirror dumb replace)
  - `.gitignore` 解 ignore hand-crafted AGENTS.md(同時保留 mirror `.agents/skills/` + `.codex/agents/` ignored — 精準兩路徑分流)
  - `codex/setup.md` Lane C 完成更新(+21 行)
  - `README.md` + `SYSADMIN_BRIEFING.md` 文件導航對齊 Lane C 完成
  - `progress-reports/README.md` 新增 session1 snapshot commit 後 cleanup 規則(+13 行)
- 派工特殊 verify:`git check-ignore -v AGENTS.md` exit=1 無輸出 → 確認 `.gitignore` 解 ignore hand-crafted AGENTS.md 正確
- push origin/main:`cf1a96d..f1d6c3f` 一次成功

**Codex 三件套 lane 累積進度**:

- Lane B(mirror artifacts probe)→ 已收尾 `9e16a6c`
- Lane C(hand-craft AGENTS.md source-of-truth)→ 已收尾 `f1d6c3f`(本批)
- Lane A(sandbox root cause 追)→ 獨立未拍板
- Lane D(平行用法實測)→ 獨立未拍板

**最新 5 commit**(origin/main):

- `f1d6c3f` docs(repo): add hand-crafted Codex AGENTS instructions(Lane C 收尾)
- `cf1a96d` docs(snapshot): session1-snapshot v15 蓋 v14
- `9e16a6c` docs(codex): integrate Lane B mirror probe results
- `b37304e` docs(codex): add codex/ subdirectory + integrate codex-plugin-cc lane
- `df44052` chore(gitignore): isolate Codex Desktop mirror artifacts

---

## 架構演進(2026-05-04)

**Codex 三件套整合進入 Lane B + Lane C 雙收尾狀態**:

- v15:Lane B 收尾 + `codex/` C-lite 子目錄落地 + Codex 三件套首次整合進 system-setup
- v16:Lane C 收尾 + hand-crafted root `AGENTS.md` 入駐(178 行,Wayne hand-craft 而非 mirror dumb replace)
- **AGENTS.md 雙路徑分流落實**:
  - hand-crafted version(root `AGENTS.md`)入 git history,作為 Codex 讀取的 source-of-truth
  - Codex 桌面板 auto-mirror artifacts(`.agents/skills/` + `.codex/agents/`)持續 .gitignore 隔離(精準路徑,非廣域)
- **Lane B + Lane C 收尾組合對齊原始 codex lane 拍板**:文件 source-of-truth(Lane C)+ mirror artifact 隔離 + 觀測結論(Lane B)
- **Lane A + Lane D 獨立未拍板**:Wayne 自決時機

**progress-reports cleanup 規則新建立**(`progress-reports/README.md`「生命週期」段):

- 主窗口覆蓋並 commit/push 最新 `session1-snapshot.md` 之後,session1 可清理 `progress-reports/*.md` 舊 raw reports(保留 `README.md`)
- 防呆:只刪 `*.md` 不刪 `README.md`;未整合 / 未拍板 / 未 commit 的 report STOP 不刪;不確定 STOP 問 Wayne
- 本 v16 snapshot 為**首次行使** cleanup 規則(snapshot v16 落地後一次清 15 份 raw reports)

---

## 規則演進(2026-05-04)

**無新規則**。Lane C 收尾(hand-crafted AGENTS.md / .gitignore 解 ignore)+ cleanup 規則新建均為文件 / SOP 落地,不升級成 SYSADMIN_BRIEFING 規則段。

規則總數 stable 1-15(本對話 v15 / v16 兩階段累積無新增 / 訂正)。

---

## 工具演進(2026-05-04)

無新工具(v15 已列 Codex 三件套 + `codex/` 子目錄)。

本批 v16 階段僅 root `AGENTS.md` 新增 178 行作為 hand-crafted Codex source-of-truth(非工具,而是文件落地)。

---

## 等 Wayne 拍板(剩 5 條)

延續 v15 等拍項(Lane C 移除 — 本批收尾):

1. **Lane A:sandbox root cause 追**(中)— GitHub issue / Claude Code permission mode 試 / 接受 sandbox 限制
2. **Lane D:平行用法實測**(中)— Codex 桌面板 / CLI 直接跑 review 確認不撞 sandbox
3. **WAN2.2 wrapper/native trade-off 拍板**(主視窗評估 #3c 後續路徑)— v14 延續
4. **dogfood test 方法論**(動規則後跑 N 個常用任務 mock 測試)— v12 / v13 / v14 / v15 / v16 連五 snapshot 延續未落地
5. **(可選)雙 session 架構 ROI 評估**(已累積 7+ lane 經驗,可拍時機)

**移除**:Lane C(本批收尾)/ LTX-2.3 verify 整合(2026-05-04 Wayne 拍板放棄)

---

## Working tree

1 檔 dirty(等下下批 commit 派工):

```
git status:
  M  progress-reports/session1-snapshot.md  ← 本檔(v16 蓋 v15)
```

下下批 commit:**單檔 1 個**(本檔 v16 蓋 v15,主視窗派 commit 派工後 session 2 執行)。

下一個 cleanup 派工:**15 份 raw reports**(snapshot v16 落地 origin/main 後一次清,見「立刻要做的事」段)。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12-v16 連五 snapshot 延續):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:本次主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **codex 後續 lane**:Lane A / D 獨立未拍板,Wayne 自決時機(Lane B + C 已收尾)
- **cleanup 規則首次行使**:snapshot v16 落地後一次清 15 份 raw reports — 本批為「snapshot 蓋掉 + cleanup」流程的首次完整 dogfood,事後可評估規則 SOP 是否需精修(防呆 / 派工模板 / cleanup 拆批策略)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

**最優先動作**:Wayne 切到 session 2 跑下下批 commit 派工(snapshot v16 commit + push;見開頭「立刻要做的事」段)。snapshot v16 落地後續派 cleanup 派工(15 份 raw reports 一次清)。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(v14 落地;§5 規範往後新增比照辦理)
- **Codex 整合(本對話累積)** → `codex/setup.md`(三件套配置 + sandbox 半通踩坑 + mirror 紀律 + Lane A/D)+ root `AGENTS.md`(hand-crafted Codex source-of-truth,Lane C 落地)
- **progress-reports cleanup 規則** → `progress-reports/README.md`(生命週期段 + 防呆段)
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
7. **Codex 三件套整合對齊 `codex/setup.md` + root `AGENTS.md`**:plugin sandbox 半通 / 桌面板 mirror-like artifacts / `.agents/skills/` `.codex/agents/` 精準 .gitignore 隔離 / hand-crafted AGENTS.md 入 git history(Lane C 收尾)
8. **progress-reports cleanup 對齊 `progress-reports/README.md`**:snapshot 蓋掉 + commit/push 落地後可清舊 raw reports(防呆:只刪 `*.md` 不刪 `README.md`;未整合 / 未拍板 STOP 不刪;不確定 STOP 問 Wayne)

---

## 關鍵紀律提醒(v15 延續 + v16 新觀察)

**v15 延續**(本對話 v15 階段累積):

1. **subagent / skill 隸屬紀律**:新增 subagent / skill 比照 `SUBAGENT_AND_SKILL_CATALOG.md` §5
2. **§7 鬆綁實證**:主視窗想查社群實踐 → invoke `community-researcher` subagent;對齊規則 10 升級版(本對話 community-researcher 二輪查 codex 桌面板實證有效)
3. **派工 / commit / progress report 高頻動作 skill 化**:`draft-assignment` / `dispatch-commit` / `integrate-progress-report` 對應 SESSION_1 §4 / §5.3 / §5.2 標準動作
4. **措辭嚴謹度抓 over-claim**:Wayne 在本對話抓 3 次主視窗 over-claim — 整合進主 MD 時要 distinguish「實證」vs「推測」vs「未實測」,**不能寫太滿**
5. **probe by rename, not delete**(Lane B 拍板):auto-generated artifact 探查紀律 — 用 `Rename-Item` 保留原檔當 backup,**不用 `Remove-Item` 當 probe**(避免污染環境判讀)
6. **派工字面執行 vs 範圍漂移**:主視窗寫派工時要對齊原拍板,session 2 STOP raise 抓到後修正
7. **session 2 step mismatch raise clarify**:派工 step 預期失效時 session 2 嚴格 verify 後 raise clarify,不擅自跳過 / 不擅自繼續 — 屬好紀律 self-correct,不入規則段不入踩坑
8. **codex pitfall 範圍紀律**(Wayne 拍板):Codex setup / sandbox pitfall 落 `codex/setup.md`,**不升級成全域行為規則** — 工具 specifics 進子目錄 setup.md

**v16 新觀察**(本對話 Lane C + cleanup 規則新建累積,**未升級成規則段**,只當接班 reminder):

9. **AGENTS.md 雙路徑分流紀律**(Lane C 拍板落實):hand-crafted source-of-truth 入 git history(root `AGENTS.md`);Codex 桌面板 auto-mirror artifacts 持續 .gitignore 精準隔離(`.agents/skills/` + `.codex/agents/`)— 兩路徑分流,Lane C 不對 mirror 動手(讓 Codex 桌面板自由覆寫),只 hand-craft root version
10. **commit 派工 special verify step 模板化候選**:本批 commit 派工 step 4「`git check-ignore -v AGENTS.md` 預期 exit=1 無輸出」是針對 `.gitignore` 解 ignore 行為的精準 verify,值得作為 commit 派工模板「special verify」段範例(Wayne 自決是否落 `ASSIGNMENT_TEMPLATE.md`)
11. **cleanup 規則首次行使 dogfood**:snapshot v16 蓋 v15 落地後 cleanup 全 15 份 raw reports — 為 `progress-reports/README.md` cleanup 規則的首次完整流程實踐;事後評估是否規則段需精修(防呆 / 派工模板 / cleanup 拆批策略)

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v15(2026-05-04)
**v16 更新理由**:本對話 codex-plugin-cc lane Lane C 收尾 commit `f1d6c3f` 落地 origin/main(hand-crafted root `AGENTS.md` 入駐 178 行 + `.gitignore` 解 ignore 同時保留 mirror artifacts ignored + `codex/setup.md` 完成更新 + 三檔導航對齊 + `progress-reports/README.md` cleanup 規則新建);cleanup 策略拍板 A「snapshot v16 commit/push 落地後,session 2 單批清 Group A 14 檔 + Group B 1 檔 = 15 份 raw reports」(理由:Group B `2026-05-04_commit-codex-agents.md` 尚未被 v16 frozen 進 git history,現在不清避免派工碎成兩批);v16 新觀察 3 條接班 reminder(AGENTS.md 雙路徑分流 / commit 派工 special verify step 模板化候選 / cleanup 規則首次行使 dogfood)
