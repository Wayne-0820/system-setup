# session1-snapshot(2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v13,2026-05-04)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**無立即動作**。本對話架構深化批次 commit `5f3f5fe` 已落地 origin/main(11 檔單批),progress report 整合完成。

**下下批 commit 待跑**(僅本檔 v14 蓋 v13,1 檔):

- 主視窗已派下下批 commit 派工 `assignments/2026-05-04_commit-snapshot-v14.md`(若已落地)
- Wayne 切到 session 2 貼派工執行 commit + push 即可

跨日場景:session 2 step 1.5 自動 rename 派工檔對齊實機今日(規則 15)— 接班時檔名可能已從 `2026-05-04_*` 變成 `<實機今日>_*`。

執行端跑完寫 progress report 落地 `progress-reports/<$today>_commit-snapshot-v14.md` → Wayne 切回 session 1「讀 progress-reports/<檔>」整合(預期無 patch、無教訓、單檔 commit 收尾)。

---

## 當前 anchor

**本對話新落地(已 commit `5f3f5fe` + push origin/main):雙 session subagent / skill 架構深化批次**

- **`SUBAGENT_AND_SKILL_CATALOG.md`(root,新增)** — subagent / skill 分 session 1 / 2 / 共用 catalog,§5 規範往後新增比照辦理
- **3 個 subagent 落地**(`.claude/agents/`):
  - `community-researcher`(S1,規則 10 升級版「社群查詢可用 subagent 並行加速」落地)
  - `assignment-verifier`(S1,規則 8 派工撰寫前 verify)
  - `log-triage`(S2,實機 log context 隔離)
- **6 個 skill 落地**(`.claude/skills/<name>/SKILL.md`):
  - `draft-assignment` / `integrate-progress-report` / `dispatch-commit`(S1)
  - `rule-15-verify` / `smoke-test-comfyui` / `commit-execution`(S2)
- **SESSION_1 §7 鬆綁**:web search / web_fetch 從「不替代 session 2」鬆綁為「主 thread 不直接跑,可 invoke subagent 隔離 context」(對齊規則 10 升級版 + community-researcher 落地)

**最新 4 commit**(origin/main):

- `5f3f5fe` SUBAGENT_AND_SKILL_CATALOG 落地 + §7 鬆綁(本批)
- `3d28ebc` v12 snapshot 蓋 v11 — 規則 15 落地收尾
- `052f040` 規則 15 落地
- `398e88d` v11 snapshot 蓋 v10 — audit 批次 + 規則 15 派工就緒

---

## 架構演進(2026-05-04)

**雙 session + subagent 三角色架構深化**:

- 從 v12「subagent 1 條(rule-curator)+ repo skill 3 條」
- 演進到 v14「subagent 4 條 + repo skill 9 條 + 內建 plugin skill 10 條」
- `SUBAGENT_AND_SKILL_CATALOG.md` 落地後 subagent / skill 隸屬清楚分 session 1 / 2 / 共用,§5 規範往後新增比照辦理

---

## 規則演進(2026-05-04)

**SESSION_1 §7 鬆綁(對齊規則 10 升級版)**:

- 舊版「❌ 不 web search / web_fetch 替代 session 2 工作」過嚴 — 主視窗想查社群實踐還得繞 session 2 派工
- 訂正版「❌ 不在主 thread 直接跑 web search / web_fetch(會塞 context);查社群實踐透過 subagent 隔離(規則 10 升級版)— session 2 跑社群查詢派工的路徑仍可用,二擇一」
- 配套落地:`community-researcher` subagent

規則總數 stable 1-15(本對話無新增規則,只 §7 鬆綁 + subagent / skill 落地)。

---

## 工具演進(2026-05-04)

- **catalog**:`SUBAGENT_AND_SKILL_CATALOG.md`(root,v1.1)
- **subagent**:3 個新落地(`.claude/agents/`)
- **skill**:6 個新落地(`.claude/skills/`)
- harness 自動載入 — 主視窗 / 執行端開新 session 後 system-reminder 列表會看到新 skill

---

## 等 Wayne 拍板(剩 1 條)

1. **(可選)雙 session 架構 ROI 評估**(已累積 6+ lane 經驗,可拍時機)— v10 / v11 / v12 / v13 既有等拍項延續

---

## Working tree

1 檔 dirty(等下下批 commit 派工):

```
git status:
  M  progress-reports/session1-snapshot.md  ← 本檔(v14 蓋 v13)
```

下下批 commit:**單檔 1 個**(本檔 v14 蓋 v13,主視窗派 commit 派工後 session 2 執行)。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12 / v13 延續 1 條未落地):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:本次主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **LTX-2.3 verify**(2026-04-30):仍待整合進 `ai-models/local-models.md`(本對話未處理)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

**最優先動作**:Wayne 切到 session 2 跑下下批 commit 派工(見開頭「立刻要做的事」段)。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(本批新落地;§5 規範往後新增比照辦理)
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

---

## 關鍵紀律提醒(v13 新訂正延續)

1. **subagent / skill 隸屬紀律**:新增 subagent / skill 比照 `SUBAGENT_AND_SKILL_CATALOG.md` §5 — 隸屬判定(session 1 / session 2 / 共用)/ 落地路徑(`.claude/agents/<name>.md` 或 `.claude/skills/<name>/SKILL.md`)/ source-of-truth 不破壞 / commit 走 session 2 / 命名規則(kebab-case + session 隸屬不寫進名稱,避免 session 架構變動 rename rolling)
2. **§7 鬆綁實證**:主視窗想查社群實踐 → invoke `community-researcher` subagent(隔離 context),不在主 thread 直接跑 — 對齊規則 10 升級版「社群查詢可用 subagent 並行加速」
3. **派工 / commit / progress report 高頻動作 skill 化**:`draft-assignment` / `dispatch-commit` / `integrate-progress-report` 對應 SESSION_1 §4 / §5.3 / §5.2 標準動作;觸發即跑 SOP 不漏紀律

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v13(2026-05-04)
**v14 更新理由**:本對話架構深化批次 commit `5f3f5fe` 落地 origin/main(11 檔單批)+ progress report 整合完成 + working tree 收斂到單檔 dirty 等下下批 commit
