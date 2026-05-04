# session1-snapshot(v20,2026-05-04)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v19 working handoff,2026-05-04;Lane A.1b stop-loss progress report 已整合進 `codex/setup.md`,等待後續 commit 派工拍板)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 立刻要做的事(接班第一動作)

**待 Wayne 拍下一步**(本檔 v20 已更新落地 working tree,等 Wayne 拍下方候選之一):

- (a)Batch Codex Lane A.1b docs + snapshot v20 commit + push(`codex/setup.md` + 本檔)
- (b)Lane A.2 sandbox runner probe 派工(獨立 PowerShell only,不改 global config,隔離 `codex sandbox windows` / restricted token runner layer)
- (c)Lane A.3 接受限制 + 主路徑切換文件化(`/codex:setup` + MCP 為主用法,`/codex:review` 標 known limitation)
- (d)Lane D2 Desktop / plugin nested sandbox contamination probe
- (f)其他(WAN2.2 / dogfood test 方法論 / 雙 session ROI / cleanup `progress-reports/`)
- (g)暫緩,本對話收尾(working tree 留 snapshot.md dirty handoff 到下次接手)

---

## 當前 anchor

**本對話新整合(working tree dirty,待 commit):Lane A.1b stop-loss + global config contamination observation**

Lane A.1 schema audit + A.1b stop-loss progress report 已整合進 `codex/setup.md`(坑 #1 cross-cut + Lane A root cause 排序 + 下一步候選更新):

- **A.1 schema audit ground truth**:Codex 0.128.0 `--sandbox <SANDBOX_MODE>` 合法值只有 `read-only` / `workspace-write` / `danger-full-access`;`sandbox = "elevated"` 與 `sandbox = "experimental"` 均非法。
- **feature flags 已廢除**:`elevated_windows_sandbox` / `experimental_windows_sandbox` 在 0.128.0 `stage = removed`;A.1 C/A 候選跳過。
- **A.1b critical observation**:`~/.codex/config.toml` 是 Desktop / plugin / CLI 共用 user-level global config;SESSION2 改 config 會污染當下整個 Codex 生態系。A.1 Phase 2 B 已 stop-loss,byte-by-byte 還原 backup,未取得 `codex review --uncommitted` verdict。
- **root cause 排序更新**:restricted token sandbox runner 行為問題升為核心候選;Desktop / plugin nested contamination 新增候選;config schema mismatch 部分坐實但降級為 banner mismatch 表象候選;dual install / onboarding 保留為次候選。

**上一批已 commit `898839f` + push origin/main:Lane A evidence pack 整合 + upstream ground truth verify**

Lane A evidence pack(read-only,2026-05-04)結果 + 4 個 upstream issue 主視窗 ground truth verify 整合進 `codex/setup.md`(三段更新 + 1 處 trim,35 insertions / 8 deletions):

- **坑 #1 §平行用法**:原 outside-scope 觀察 bullet 升級為 evidence pack cross-cut(config / banner mismatch + 雙重安裝)— **persistent + ad-hoc(`-c sandbox_permissions=...`)雙路徑都 mismatch**,**高度懷疑** 0.128.0 未採用該 key/value;雙重安裝(`OpenAI.Codex` packaged app `26.429.3425.0` + npm `codex-cli 0.128.0`)為 black box runtime 候選
- **坑 #1 §未來追 root cause 候選 §forensic 觀察**:43 KB `~/.codex/.sandbox/sandbox.log` 內 0 命中 sandbox 失敗 keyword,**可能** forensic source 含 `logs_2.sqlite`(19 MB,evidence pack 副檔名限制未 verify)/ stderr capture / Windows Event Log
- **Lane A 整段重寫**:evidence 摘要 4 點 + upstream 對照表(`#10090` STRONG / `#13965` `#14211` MID / `#9062` WEAK-MID / `#18620` WEAK)+ 根因排序(#1 `elevated_windows_sandbox` config schema 主嫌 / #2 WindowsApps packaged app ACL + 雙重安裝 / #3 onboarding 跑了但壞掉)+ 下一步候選 A.1 候選修復試驗 / A.2 雙重安裝 probe / A.3 接受限制
- **Codex review trim**:Lane A evidence 摘要「driving down」→「降低候選優先度」,降低過度定論

**本派工執行紀律驗證**:派工 §Step 2 grep verify 撞兩條合法 reference false STOP(STRONG MATCH = 2 但派工嚴格期望 1 / `^+` 行 `outside-scope 觀察` = 1 但派工嚴格期望 0)→ SESSION2 規則 9 中性紀律 STOP raise 攤兩個候選(派工撰寫疏漏 vs 真有 patch 異常)→ Wayne 中介工程選擇拍 a(patch 內容 OK,只修派工 grep 期望)→ 主視窗加 §Wayne gate continuation 段 in-place 修派工 → SESSION2 重跑全綠後續走 Stage → Commit `-F` → Push → Final verify。**機制驗證可行**(非 SESSION2 自決,Wayne 中介)。

**Lane A 累積進度更新**:
- Lane A evidence pack(read-only,2026-05-04)→ **已收進 `codex/setup.md`,commit `898839f`**
- Lane A root cause 主嫌排序 → **再次更新**(#1 restricted token sandbox runner / #2 Desktop-plugin nested contamination / #3 config schema mismatch 表象候選 / #4 dual install / #5 onboarding)
- Lane A.1 候選修復試驗 → **已中止收尾**:schema audit 完成,B patch stop-loss 還原,C/A 證偽跳過;不沿用原 A.1 設計繼續跑
- Lane A.2 sandbox runner probe → **未做**,Wayne 自決時機(不改 global config)
- Lane A.3 接受限制文件化 → **未做**,Wayne 自決時機
- Lane D2 Desktop / plugin nested contamination probe → **未做**,Wayne 自決時機

**Codex 三件套 lane 累積進度**(更新):
- Lane B(mirror artifacts probe)→ 已收尾 `9e16a6c`
- Lane C(hand-craft AGENTS.md source-of-truth)→ 已收尾 `f1d6c3f`
- Lane D1(CLI direct review workaround)→ 已收尾 `d2fb5d8`(失敗模式文件化)
- **Lane A evidence pack + upstream verify → 已收尾 `898839f`**(本對話)
- **Lane A.1 / A.1b schema audit + stop-loss → working tree 已整合,待 commit**(本輪)
- Lane D2(桌面板 GUI 平行用法)→ 未測,Wayne 自決時機
- Lane A.2 / A.3 → 未做,Wayne 自決時機

**最新 5 commit**(origin/main):

- `898839f` docs(codex): integrate Lane A evidence pack and upstream verify(本對話 Lane A evidence pack 整合)
- `dc78f7b` docs(snapshot): session1-snapshot v18 蓋 v17 — Lane D1 收尾文件化
- `d2fb5d8` docs(codex): record Lane D1 CLI review sandbox failure
- `0b4bf9f` docs(snapshot): session1-snapshot v17 蓋 v16 — 最小規則收斂落地與候選瘦身
- `e3df754` docs(rules): 最小規則收斂 — SESSION1 draft 自修紀律 + Codex sandbox 坑 #3

---

## 規則演進(2026-05-04 v20)

**無新規則**。本對話為 `codex/setup.md` 子目錄段更新(Lane A evidence pack 整合),對齊紀律 #8「Codex pitfall 落 codex/setup.md,不升級全域行為規則」+「最小規則收斂」原則(累積樣本不足不升級)。

規則總數 stable 1-15。

---

## 工具演進

無(本對話為 codex Lane A evidence pack 整合 + 文件化,非工具 / 模型新增)。

---

## v20 候選清單

### 觀察候選(保留;只是觀察,不主動推進升級)

(延續 v18 觀察候選清單,本對話無新增 / 無移出)

1. **cleanup 規則首次行使 dogfood**(v16 + cleanup 派工 2 完整實證):流程 SOP 可行,僅 step 8 撞 sandbox hook(已升級坑 #3 落地)— 累積樣本 1 例
2. **AGENTS.md 雙路徑分流紀律**(v16 Lane C 拍板落實):觀察候選,不需升級
3. **commit 派工 special verify step 模板化候選**(Lane C 派工實證 + 本對話 Lane A 派工再驗證):值得作為 commit 派工模板「special verify」段範例(Wayne 自決是否落 `ASSIGNMENT_TEMPLATE.md`)— 樣本累積中

### v17/v18 reminder 狀態變動(v19 整合)

4. **commit message 草稿 `-F file` 路線**(v17 / v18 整合衍生 #14 延續):
   - **累積樣本升至 5 次**:Batch 1(Remove-Item)/ Batch 2(multiline)/ Lane D1 commit / v18 snapshot commit / **本批 Lane A commit**(commit message 含 `()` `[]` `#` 全形引號 multiline)
   - 性質仍屬規則 11「執行端可自處」範疇,未撞 STOP
   - **列升級評估候選**(候選位:SESSION_2 §5.3 / `commit-execution` skill checklist / `dispatch-commit` skill checklist 之一)
   - **不本輪升級**(對齊 Wayne 拍板「最小規則收斂」原則;暫存等下次回潮再評估)

5. **v18 整合衍生 t2(forensic trail 不在 sandbox.log)**:**已由 `898839f` cover**(`codex/setup.md` 坑 #1 §forensic 觀察段),從暫存移出
6. **v18 整合衍生 t3(雙重安裝為 black box source)**:**已由 `898839f` cover**(`codex/setup.md` 坑 #1 §平行用法 cross-cut + Lane A 根因排序 #2),從暫存移出

### v20 整合衍生(本批新增,Wayne 拍 — 暫存 reminder,不升級)

7. **派工 grep verify 合法 reference false STOP**(本對話 progress report `2026-05-04_commit-codex-lane-a-evidence.md` §4):
   - **症狀**:派工 grep verify 期望數誤估「合法 reference 引用」(表格標籤被排序段引用 / 舊 bullet 字眼作 cross-cut 「擴大版」reference 描述)→ SESSION2 撞 false STOP raise
   - **解法**(規則 9 中性 STOP raise → Wayne / 主視窗工程選擇):候選 a 修派工 grep 期望(實採)/ 候選 b 改 patch 刪 reference 字樣
   - **Wayne gate continuation 段機制驗證可行**(Wayne 中介工程選擇,非 SESSION2 自決)
   - **累積樣本 1 例,Wayne 拍不升 SOP**(對齊「最小規則收斂」);未來主視窗撰寫派工 grep verify 期望宜傾向 `≥` 寬鬆 / 嚴格 0 / 嚴格 1 條目改用 fixed-string 限定完整 markdown header(本對話 grep #6 `**outside-scope 觀察**` `-F` 已示範該寫法)— 暫存 reminder,等再撞同坑(≥ 2 次)主視窗自決升級層級(`ASSIGNMENT_TEMPLATE.md` §設計提醒 / `draft-assignment` skill Step 3 checklist 等)

8. **Codex user-level global config 改動污染 Desktop / plugin / CLI**(progress report `2026-05-04_lane-a1b-global-config-stoploss.md` §4):
   - **症狀**:SESSION2 patch `~/.codex/config.toml` 後,Wayne 觀察 Codex Desktop / 本視窗也開始受 sandbox 行為影響。
   - **結論**:`~/.codex/config.toml` 是 Codex Desktop / plugin / CLI 共用 global config;改 config 類試驗需隔離,不能假設只影響獨立 CLI。
   - **落點**:已收進 `codex/setup.md` 坑 #1 + Lane A 段;不升全域規則。

### v18 整合衍生延續(暫存,Wayne 拍 不升級;累積樣本未變)

9. **Codex review handoff pattern(輕量候選)**(v18 既有):SESSION1 寫完 snapshot / 規則 patch / 派工草案後,若 Wayne **顯式指定** Codex review,只交 diff 摘要 + scope + dirty status 給 Codex;Codex 回 `APPROVE` / `TRIM` / `BLOCK`,SESSION1 只依 verdict 修正,不展開新決策包。**不自動 gate 所有輸出**;不寫進 `SESSION_1_MAINWINDOW.md` / 不寫進 `dispatch-commit` skill / 不新增 workflow。**本對話 Lane A patch 落地後 Wayne 顯式 invoke Codex review verdict = APPROVE with one tiny trim(driving down → 降低候選優先度),機制再次驗證可行**

### v18 reminder 延續(觀察候選,本對話無新增 / 無移出)

10. **sanity scan token-prefix regex 缺 word boundary**(v18 Lane A evidence pack progress report §observation #5 延續):派工 §sanity scan token-prefix regex(`sk-[A-Za-z0-9-]+` / `hf_[A-Za-z0-9]+` 等)缺 word boundary `\b...\b`,在含 `disk-` / `risk-` / `task-` 等前綴字串中 false positive 命中。下次 evidence 派工撰寫時可補,**不本輪升級規則**。樣本 1 例延續暫存。

---

## 剩餘 Wayne 拍板項(本對話 Lane A.1b 整合後,Lane A.x / D2 / 其他獨立列出)

1. **Commit Codex Lane A.1b docs + snapshot v20**(`codex/setup.md` + 本檔)— 高 — Wayne 自決時機
2. **Lane A.2 sandbox runner probe**(獨立 PowerShell only,不改 global config,隔離 `codex sandbox windows` / restricted token runner layer)— 中 — Wayne 自決時機
3. **Lane A.3 接受限制 + 主路徑切換文件化**(`codex/setup.md` patch:`/codex:review` 標 known limitation,主路徑改 `/codex:setup` + MCP)— 低 — Wayne 自決時機
4. **Lane D2:Desktop / plugin nested sandbox contamination probe**(確認 Desktop / plugin wrapper 是否額外加劇 nested spawn)— 低 — Wayne 自決時機
5. **WAN2.2 wrapper/native trade-off 拍板**(主視窗評估 #3c 後續路徑)— v14 延續
6. **dogfood test 方法論**(動規則後跑 N 個常用任務 mock 測試)— v12-v19 連八 snapshot 延續未落地
7. **(可選)雙 session 架構 ROI 評估**(已累積 9+ lane 經驗,可拍時機)
8. **(可選)`-F file` 路線升級時機**(v17/v18/v19 整合衍生 #14 累積樣本五次;升級層候選 SESSION_2 §5.3 / `commit-execution` skill / `dispatch-commit` skill 之一)— 低 — Wayne 自決時機

---

## Working tree

**git HEAD = origin/main = `cab9ad9`**(synced,snapshot v19 commit;本輪 Lane A.1b docs 尚未 commit)

v20 寫入後 working tree 預期:

```
git status:
  M  codex/setup.md
  M  progress-reports/session1-snapshot.md
```

下一個 commit(Wayne 若拍 (a))= **Codex Lane A.1b docs + snapshot v20**:`codex/setup.md` + 本檔同批 commit + push。

---

## 旁支 / 待整合

- **教訓暫存清算**(v12-v19 連八 snapshot 延續):**dogfood test 方法論** — 動規則後跑 N 個常用任務 mock 測試,待主視窗下次評估是否進規則段
- **跨日 mismatch dogfood 實證**:v18 / v19 主視窗派工撰寫日 = 實機今日(match=True),跨日 rename 場景仍待跨日 session 自然觸發
- **codex 後續 lane**:Lane A.2 / A.3 / D2 獨立未拍板,Wayne 自決時機(Lane A evidence pack + A.1/A.1b + D1 已收尾)
- **下次 cleanup 候選**:本檔 v20 commit + push 落地後,`progress-reports/` 可清舊 raw reports — 目前候選 3 檔:`2026-05-04_cleanup-raw-reports-v19.md` / `2026-05-04_commit-snapshot-v19.md` / `2026-05-04_lane-a1b-global-config-stoploss.md`;保留 README + session1-snapshot;**本派工不做 cleanup**,cleanup 派工由下次主視窗自決時機(避免本對話 scope 漂移)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到 v19 anchor + 等什麼。

**最優先動作**:Wayne 拍下一步(Lane A.1b docs commit / Lane A.2 / Lane A.3 / Lane D2 / 其他 / 暫緩收尾)。常見接手場景:

- (a)Wayne 想直接拍 Codex Lane A.1b docs commit 派工:主視窗草擬 `codex/setup.md` + 本檔 commit + push 派工
- (b)Wayne 暫緩 commit,只想 audit / 整合 / 對話:不需動派工(working tree 留 snapshot.md dirty handoff 到下次接手)
- (c)Wayne 想拍其他 lane(A.2 / A.3 / D2 / WAN2.2 / dogfood / 雙 session ROI / cleanup):走規劃 + 派工流程

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`(v17 Batch 1 §4 派工層紀律 +1 bullet)
- 規則段 1-15 / 系統現況 / Python 版本配對 / 個人偏好 → `SYSADMIN_BRIEFING.md`(audit 後 source-of-truth 唯一處)
- **subagent / skill 機制** → `SUBAGENT_AND_SKILL_CATALOG.md`(v14 落地;§5 規範往後新增比照辦理)
- **Codex 整合** → `codex/setup.md`(三件套配置 + sandbox / mirror / keyword scan 踩坑 + mirror 紀律 + Lane A/D + Lane A evidence pack / A.1b stop-loss 整合 + upstream verify 對照)+ root `AGENTS.md`(hand-crafted Codex source-of-truth,Lane C 落地)
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
7. **Codex 三件套整合對齊 `codex/setup.md` + root `AGENTS.md`**:plugin sandbox 半通(坑 #1)/ 桌面板 mirror-like artifacts(坑 #2)/ PowerShell sandbox keyword scan(坑 #3)/ Lane D1 CLI direct review 失敗 / Lane A evidence pack + upstream verify 已落地 / `.agents/skills/` `.codex/agents/` 精準 .gitignore 隔離 / hand-crafted AGENTS.md 入 git history
8. **progress-reports cleanup 對齊 `progress-reports/README.md`**:snapshot 蓋掉 + commit/push 落地後可清舊 raw reports(防呆:只刪 `*.md` 不刪 `README.md`;未整合 / 未拍板 STOP 不刪;不確定 STOP 問 Wayne)
9. **算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne**(已升級成 SESSION_1 §4 派工層紀律 bullet,commit `e3df754`):自實機 verify(`Get-ChildItem` / `git ls-files` / `Test-Path` 等)+ 修正 draft + 回報「已自修正」短訊息;STOP 限策略 / 範圍 / scope 變更或 STOP 真觸發
10. **派工 grep verify 期望宜寬鬆**(v19 整合衍生 #7,暫存 reminder 不升 SOP):嚴格 0 / 嚴格 1 條目改用 fixed-string `-F` 限定完整 markdown header(避免合法 reference 引用 false STOP);累積樣本 1 例,等再撞同坑時主視窗自決升級層級

---

## 關鍵紀律提醒(v15 + v16 延續 + v17 已升級 + v17/v18 整合衍生 + v19 整合衍生)

**v15 / v16 延續**(累積 11 條,本對話無新增於既有條目):

1. **subagent / skill 隸屬紀律**:新增 subagent / skill 比照 `SUBAGENT_AND_SKILL_CATALOG.md` §5
2. **§7 鬆綁實證**:主視窗想查社群實踐 → invoke `community-researcher` subagent;對齊規則 10 升級版
3. **派工 / commit / progress report 高頻動作 skill 化**:`draft-assignment` / `dispatch-commit` / `integrate-progress-report` 對應 SESSION_1 §4 / §5.3 / §5.2 標準動作
4. **措辭嚴謹度抓 over-claim**:Wayne 在 v15 階段抓 3 次主視窗 over-claim — 整合進主 MD 時要 distinguish「實證」vs「推測」vs「未實測」,**不能寫太滿**;v19 Codex review 抓「driving down」過度定論 trim 為「降低候選優先度」延續驗證紀律
5. **probe by rename, not delete**(Lane B 拍板):auto-generated artifact 探查紀律 — 用 `Rename-Item` 保留原檔當 backup,**不用刪檔當 probe**(避免污染環境判讀)
6. **派工字面執行 vs 範圍漂移**:主視窗寫派工時要對齊原拍板,session 2 STOP raise 抓到後修正
7. **session 2 step mismatch raise clarify**:派工 step 預期失效時 session 2 嚴格 verify 後 raise clarify,不擅自跳過 / 不擅自繼續(v19 Lane A commit 派工 grep #3 / #6 false STOP raise → Wayne gate continuation 修派工再次驗證)
8. **codex pitfall 範圍紀律**(Wayne 拍板):Codex setup / sandbox pitfall 落 `codex/setup.md`,**不升級成全域行為規則** — 工具 specifics 進子目錄 setup.md
9. **AGENTS.md 雙路徑分流紀律**(v16 Lane C 拍板落實):hand-crafted source-of-truth 入 git history;Codex 桌面板 auto-mirror artifacts 持續精準 .gitignore 隔離
10. **commit 派工 special verify step 模板化候選**(v16 Lane C + v19 Lane A 派工再驗證):值得作為 commit 派工模板「special verify」段範例
11. **cleanup 規則首次行使 dogfood**(v16 + cleanup 派工 2 完整實證):snapshot 蓋掉 + cleanup 流程 SOP 可行

**v17 已升級成正式落地**(commit `e3df754`,從 reminder → SESSION_1 / codex/setup.md 規則 hook):

12. ~~算術 / 列項 / 數字 mismatch 主視窗自修正不問 Wayne~~ → SESSION_1 §4 派工層紀律 bullet 落地
13. ~~PowerShell here-string 含 sandbox 敏感 keyword 誤觸 hook~~ → codex/setup.md 坑 #3 落地

**v17/v18/v19 整合衍生**(暫存 reminder,Wayne 拍不升級主 MD / skill;**累積樣本上升**):

14. **commit message 草稿含 sandbox 黑名單字樣 / multiline 含特殊字元 → SESSION2 自處 `git commit -F file` 路線**(v17 Batch 1 progress report §4 教訓 + 持續累積):
    - **累積樣本上升至 5 次**:Batch 1(Remove-Item)/ Batch 2(multiline)/ Lane D1 commit / v18 snapshot commit / **本批 Lane A commit**
    - 性質仍屬規則 11「執行端可自處」範疇,未撞 STOP
    - **列升級評估候選**(候選位:SESSION_2 §5.3 / `commit-execution` skill checklist / `dispatch-commit` skill checklist 之一)
    - **不本輪升級**(Wayne 拍對齊「最小規則收斂」);累積樣本上升,Wayne 自決升級時機

**v18 整合衍生**(Wayne 拍不升級;**v19 Codex review 機制再次驗證可行**):

15. **Codex review handoff pattern(輕量候選)**:SESSION1 寫完 snapshot / 規則 patch / 派工草案後,若 Wayne **顯式指定** Codex review,只交 diff 摘要 + scope + dirty status 給 Codex;Codex 回 `APPROVE` / `TRIM` / `BLOCK`,SESSION1 只依 verdict 修正,不展開新決策包。**不自動 gate 所有輸出**;不寫進 `SESSION_1_MAINWINDOW.md` / 不寫進 `dispatch-commit` skill / 不新增 workflow。**v19 Lane A patch 落地後 Wayne 顯式 invoke Codex review,verdict = APPROVE with one tiny trim(`driving down` → 降低候選優先度),機制再次驗證可行**

**v18 既有延續**(觀察候選,本對話無新增 / 無移出 / 已 cover 由 commit 落地的移出):

16. **sanity scan token-prefix regex 缺 word boundary**(v18 Lane A evidence pack progress report §observation #5 延續):派工 §sanity scan token-prefix regex 缺 word boundary,在含 `disk-` / `risk-` / `task-` 等前綴字串中 false positive 命中;下次 evidence 派工撰寫時可補,樣本 1 例暫存

(v18 整合衍生 t2 forensic / t3 雙重安裝 → **已由 `898839f` cover**,從暫存清單移出)

**v19 整合衍生**(本批新增,Wayne 拍 — 暫存 reminder,不升級正式規則 / 不自動 gate / 不新增 workflow):

17. **派工 grep verify 期望數誤估「合法 reference 引用」 false STOP**(本對話 progress report §4):
    - **症狀**:派工撰寫 grep verify 期望時假設「字樣只在指定區段出現 N 次」/「字樣 trim 後完全不在 + 行」,沒算到合法 reference 引用(表格標籤被排序段引用 / 舊 bullet 字樣作 cross-cut「擴大版」reference 描述)
    - **解法**(規則 9 中性 STOP raise → Wayne / 主視窗工程選擇):候選 a 修派工 grep 期望 / 候選 b 改 patch;Wayne gate continuation 段機制驗證可行(Wayne 中介工程選擇,非 SESSION2 自決)
    - **未來注意**:主視窗撰寫 grep verify 期望宜傾向 `≥` 寬鬆語意;嚴格 0 / 嚴格 1 條目改用 fixed-string `-F` 限定完整 markdown header(本對話 grep #6 `**outside-scope 觀察**` `-F` 已示範)
    - **累積樣本 1 例,Wayne 拍不升 SOP**;暫存 v19 reminder,等再撞同坑(≥ 2 次)主視窗自決升級層級(`ASSIGNMENT_TEMPLATE.md` §設計提醒 / `draft-assignment` skill Step 3 checklist 等)

(v12 既有紀律提醒延續,不重抄 — 詳見 `git show 3d28ebc`)

---

**蓋掉**:v19 working handoff(2026-05-04;HEAD/origin/main `cab9ad9`)
**v20 更新理由**:Lane A.1 schema audit + A.1b stop-loss progress report 已整合進 `codex/setup.md` 與本 snapshot。0.128.0 sandbox enum ground truth 確認 `sandbox = "elevated"` / `sandbox = "experimental"` 均非法,`experimental_windows_sandbox` / `elevated_windows_sandbox` feature flags 已 `removed`;A.1 C/A 證偽跳過,B patch 因 `~/.codex/config.toml` global config 污染 Desktop / plugin / CLI 而 stop-loss 還原,未取得 review verdict。Lane A root cause 排序更新為 #1 Windows restricted token sandbox runner / #2 Desktop-plugin nested contamination / #3 config schema mismatch 表象候選 / #4 dual install / #5 onboarding。剩餘拍板項改為 commit 本批 docs + snapshot / Lane A.2 sandbox runner probe / Lane A.3 接受限制文件化 / Lane D2 contamination probe / 其他。
