# session1-snapshot(2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v14,2026-05-04)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**無立即動作**。本對話 codex-plugin-cc lane(install + Lane B 探查)三 batch commit 全落地 origin/main:`df44052` / `b37304e` / `9e16a6c`。

**下下批 commit 待跑**(僅本檔 v15 蓋 v14,1 檔):

- 主視窗已派下下批 commit 派工 `assignments/2026-05-04_commit-snapshot-v15.md`(若已落地)
- Wayne 切到 session 2 貼派工執行 commit + push 即可

跨日場景:session 2 step 1.5 自動 rename 派工檔對齊實機今日(規則 15)— 接班時檔名可能已從 `2026-05-04_*` 變成 `<實機今日>_*`。

執行端跑完寫 progress report 落地 `progress-reports/<$today>_commit-snapshot-v15.md` → Wayne 切回 session 1「讀 progress-reports/<檔>」整合(預期無 patch、無教訓、單檔 commit 收尾)。

---

## 當前 anchor

**本對話新落地(已 commit `df44052` + `b37304e` + `9e16a6c` + push origin/main):codex-plugin-cc lane 完整收尾(install + 整合 + Lane B)**

Codex 三件套整合(plugin v1.0.4 in-Claude-Code + 桌面板 + CLI 0.128.0):

- **`df44052`** chore(gitignore): isolate Codex Desktop mirror artifacts — `.agents/skills/` + `.codex/agents/` + `AGENTS.md` 精準隔離(避免廣域 ignore)
- **`b37304e`** docs(codex): add codex/ subdirectory + integrate codex-plugin-cc lane — Wayne 拍板新 `codex/` C-lite 最小子目錄;`codex/setup.md` 三件套配置 / sandbox 半通踩坑 / mirror 紀律;README + SYSADMIN_BRIEFING 文件導航更新
- **`9e16a6c`** docs(codex): integrate Lane B mirror probe results — 5 點 patch scope 修正(措辭精準化:「自動 mirror」→「mirror-like artifacts」/ root cause 段降格「觀測 / 推測」+ 標官方未文件化 / Lane B 段改 rename probe + 寫進實機觀察結果)

**Lane B 探查結論**(rename probe + community-researcher 兩輪):

- 官方文件**無 mirror / auto-create / disable** 文件化(changelog v0.123-0.128 / Codex Desktop release notes 不公開 `openai/codex#10859`)
- 實機 rename probe(`AGENTS.md → AGENTS.md.probe-bak`):立即 / 連續多時點 / 開桌面板後均**未觀測重生**
- 結論:**較像 one-shot import / mount-time conversion / 其他未明一次性觸發**;plugin slash command 觸發點未測(獨立延伸)

**最新 4 commit**(origin/main):

- `9e16a6c` docs(codex): integrate Lane B mirror probe results
- `b37304e` docs(codex): add codex/ subdirectory + integrate codex-plugin-cc lane
- `df44052` chore(gitignore): isolate Codex Desktop mirror artifacts
- `b230969` docs(snapshot): session1-snapshot v14(本對話接班 anchor)

---

## 架構演進(2026-05-04)

**Codex 三件套首次整合進 system-setup**:

- 從 v14「subagent 4 條 + repo skill 9 條 + 內建 plugin skill 10 條」純 Claude Code 生態
- 演進到 v15 加 Codex 三件套(plugin / 桌面板 / CLI)+ `codex/` C-lite 最小子目錄
- **`codex/setup.md` 為三件套整合入口**:環境基線 / 安裝 / 在 Claude Code 內 invoke / 踩坑 #1 sandbox 嵌套 spawn / 踩坑 #2 mirror-like artifacts / 未來 lane A/B/C/D
- **Lane B 已收尾**(實機觀察 + community-researcher 兩輪),Lane A/C/D 獨立未拍板

**.gitignore 精準隔離紀律新建立**:

- **避免廣域 ignore `.agents/` `.codex/`**(未來 codex marketplace metadata / repo-native 設定可能落這條路徑)
- 精準隔離:`.agents/skills/` + `.codex/agents/` + `AGENTS.md`
- AGENTS.md 紀律:hand-crafted 應 commit / auto-generated dumb replace 不應 commit

---

## 規則演進(2026-05-04)

**無新規則**。Wayne 拍板「Codex setup / sandbox pitfall 落 `codex/setup.md`,不升級成全域行為規則」 — Codex 範圍 specifics 進子目錄 setup.md,不升級成 SYSADMIN_BRIEFING 規則段。

規則總數 stable 1-15(本對話無新增 / 訂正,只 codex 子目錄落地)。

---

## 工具演進(2026-05-04)

- **Codex CLI 0.128.0**(npm global `@openai/codex`)
- **Codex plugin 1.0.4**(`codex@openai-codex` Claude Code user scope marketplace)
- **Codex 桌面板**(版本未 verify,掛載 `D:\Work\system-setup` 後出現 mirror-like artifacts)
- **新子目錄 `codex/setup.md`**(C-lite 最小,Wayne 拍板 2026-05-04 新增)
- harness 自動載入 codex plugin skills:`/codex:setup` ✅ / `/codex:review` ⚠️ 半通 / `/codex:rescue` ⚠️ 未驗證

---

## 等 Wayne 拍板(剩 6 條)

新增 3 條(本對話 codex lane 衍生):

1. **Lane A:sandbox root cause 追**(中)— GitHub issue / Claude Code permission mode 試 / 接受 sandbox 限制
2. **Lane C:hand-craft AGENTS.md source-of-truth**(低)— 主視窗 hand-craft 正確版,非 mirror dumb replace
3. **Lane D:平行用法實測**(中)— Codex 桌面板 / CLI 直接跑 review 確認不撞 sandbox

延續 v14 等拍項:

4. **WAN2.2 wrapper/native trade-off 拍板**(主視窗評估 #3c 後續路徑)— v14 延續
5. **dogfood test 方法論**(動規則後跑 N 個常用任務 mock 測試)— v12 / v13 / v14 / v15 連四 snapshot 延續未落地
6. **(可選)雙 session 架構 ROI 評估**(已累積 7+ lane 經驗,可拍時機)

**移除**:LTX-2.3 verify 整合(2026-05-04 Wayne 拍板放棄)

---

## Working tree

1 檔 dirty(等下下批 commit 派工):

```
git status:
  M  progress-reports/session1-snapshot.md  ← 本檔(v15 蓋 v14)
```

下下批 commit:**單檔 1 個**(本檔 v15 蓋 v14,主視窗派 commit 派工後 session 2 執行)。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12-v15 連四 snapshot 延續):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:本次主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **codex 後續 lane**(本對話新增):Lane A / C / D 獨立未拍板,Wayne 自決時機
- **AGENTS.md.probe-bak**(本對話 Lane B probe artifact):Wayne 已自處(commit `9e16a6c` 前刪除),不留歷史

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

**最優先動作**:Wayne 切到 session 2 跑下下批 commit 派工(見開頭「立刻要做的事」段)。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(v14 落地;§5 規範往後新增比照辦理)
- **Codex 整合(本對話新落地)** → `codex/setup.md`(三件套配置 + sandbox 半通踩坑 + mirror 紀律 + Lane A/C/D)
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
7. **Codex 三件套整合對齊 `codex/setup.md`**:plugin sandbox 半通 / 桌面板 mirror-like artifacts / `.agents/skills/` `.codex/agents/` `AGENTS.md` 精準 .gitignore 隔離 / hand-crafted vs auto-generated AGENTS.md 紀律

---

## 關鍵紀律提醒(v14 延續 + v15 新觀察)

**v14 延續**:

1. **subagent / skill 隸屬紀律**:新增 subagent / skill 比照 `SUBAGENT_AND_SKILL_CATALOG.md` §5
2. **§7 鬆綁實證**:主視窗想查社群實踐 → invoke `community-researcher` subagent;對齊規則 10 升級版(本對話 community-researcher 二輪查 codex 桌面板實證有效)
3. **派工 / commit / progress report 高頻動作 skill 化**:`draft-assignment` / `dispatch-commit` / `integrate-progress-report` 對應 SESSION_1 §4 / §5.3 / §5.2 標準動作

**v15 新觀察**(本對話累積,**未升級成規則段**,只當接班 reminder):

4. **措辭嚴謹度抓 over-claim**:Wayne 在本對話抓 3 次主視窗 over-claim(「主目標達成」/「掛載即觸發 mirror」/「平行用法不受影響」)— 整合進主 MD 時要 distinguish「實證」vs「推測」vs「未實測」,**不能寫太滿**
5. **probe by rename, not delete**(Lane B 拍板):auto-generated artifact 探查紀律 — 用 `Rename-Item` 保留原檔當 backup,**不用 `Remove-Item` 當 probe**(避免污染環境判讀)
6. **派工字面執行 vs 範圍漂移**:主視窗寫派工時要對齊原拍板(本對話 finale 派工 §決策已定「執行端自決 sanity check」違反原 (C) 拍板「Wayne 親打 `/codex:review`」),session 2 STOP raise 抓到後修正
7. **session 2 step mismatch raise clarify**:派工 step 預期失效時 session 2 嚴格 verify 後 raise clarify,不擅自跳過 / 不擅自繼續 — 屬好紀律 self-correct,不入規則段不入踩坑
8. **codex pitfall 範圍紀律**(Wayne 拍板):Codex setup / sandbox pitfall 落 `codex/setup.md`,**不升級成全域行為規則** — 工具 specifics 進子目錄 setup.md

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v14(2026-05-04)
**v15 更新理由**:本對話 codex-plugin-cc lane(install + Lane B 探查)完整收尾;三 batch commit `df44052` + `b37304e` + `9e16a6c` 落地 origin/main;Codex 三件套首次整合進 system-setup(`codex/` C-lite 最小子目錄落地);Lane B 探查結論「未觀測持續 file-watcher,推測 one-shot」+ Lane A/C/D 獨立未拍板;v15 新觀察 5 條接班 reminder(over-claim 抓 / probe by rename / 派工範圍漂移 / step mismatch raise clarify / codex pitfall 範圍)
