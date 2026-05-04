# SUBAGENT_AND_SKILL_CATALOG.md — Session 1 / Session 2 subagent 與 skill 目錄

> 本 repo 雙 session + subagent 三角色架構下,subagent / skill 各自隸屬 **session 1 主視窗**(規劃 / 派工 / 整合)、**session 2 執行端**(實機操作 / 跑派工)、或兩端共用。
> 落地新 subagent / skill 時依本檔分類補進對應段(往後比照辦理,紀律見文末)。
>
> 最後更新:2026-05-04
> 版本:1.1(v1.0 提案 9 條全部落地)

---

## 0. subagent 與 skill 機制差異

| 機制 | 觸發方式 | context | 適用場景 |
|---|---|---|---|
| **subagent** | 主 thread 用 `Agent` tool spawn | 獨立 context,return finding 給 spawn 端 | context-heavy / 並行加速 / 隔離污染 / 長 finding |
| **skill** | 主 thread 用 `Skill` tool 觸發 | 共用主 thread context | 重複性 SOP / 自動化動作 / 標準格式產出 |

skill 是「主 thread 自己跑 SOP 文件」,不開新 context;subagent 是「spawn 獨立 worker」,有獨立 context。同一個需求兩種機制都可實作,但 ROI 不同 — 看資訊量 + context 污染風險。

---

## 1. 現有 subagent

### 1.1 Session 1 主視窗 subagent

#### `rule-curator` — 規則精修員

- **路徑**:`D:\Work\system-setup\.claude\agents\rule-curator.md`
- **功能**:audit `SYSADMIN_BRIEFING.md` / `SESSION_*` / `CLAUDE.md` / templates 等規則文件矛盾 / 缺漏 / 表述對不上,寫 patch 訂正,維護跨檔 cross-reference 對齊
- **典型 invoke 場景**:本對話踩坑 raise 規則矛盾 / 接班一致性 audit / 教訓暫存統整 / commit 拆批前 verify 規則精修完整性
- **紀律**:不替代主視窗決策,不直接 commit;working tree dirty 留主視窗派 commit 派工 session 2 處理

#### `community-researcher` — 社群實踐查詢員

- **路徑**:`D:\Work\system-setup\.claude\agents\community-researcher.md`
- **功能**:並行多 source(GitHub issues / reddit / 上游 maintainer 動向 / 程式碼 audit)查社群實踐,return 精簡 finding 給主視窗
- **典型 invoke 場景**:時間 / VRAM / 品質異常或退化期 trial-and-error 進入前先查社群(規則 10 升級版「社群查詢可用 subagent 並行加速」落地)
- **紀律**:不替主視窗下 root cause,不直接 patch 主 MD;return 內容 ≤ 500 字 + URL anchor

#### `assignment-verifier` — 派工撰寫 verify 員

- **路徑**:`D:\Work\system-setup\.claude\agents\assignment-verifier.md`
- **功能**:主視窗寫派工時 spawn 並行 grep verify 多個引用點(MD 路徑 / 踩坑編號 / 規則編號 / progress report 路徑),return verify 結果給主視窗
- **典型 invoke 場景**:複雜派工(引用點 ≥ 5)/ 跨子目錄派工 / 新編號落地後派工(對應 SESSION_1 §4 「派工撰寫前 verify 引用準確性」、規則 8)
- **紀律**:不擅自 patch 派工;只 verify 主視窗指定的引用點清單

### 1.2 Session 2 執行端 subagent

#### `log-triage` — 實機 log 過濾員

- **路徑**:`D:\Work\system-setup\.claude\agents\log-triage.md`
- **功能**:讀 ComfyUI / openwebui / litellm 等 server log,過濾 ERROR / WARNING / 對照既有 setup.md 踩坑段,return 精簡 finding 給 session 2 主 thread
- **典型 invoke 場景**:派工跑時撞錯 + log 量大主 thread 易塞 context / 回歸測試前 audit log / conflicts audit 過濾啟動 log
- **紀律**:不下 root cause,不擅自延伸 verify;return 控在 ≤ 500 字內

### 1.3 共用 subagent

(無)

---

## 2. 現有 skill(repo-level)

### 2.1 Session 1 主視窗 skill

#### `log-lesson` — 沉澱跨 session 教訓進 SYSADMIN_BRIEFING.md

- **路徑**:`D:\Work\system-setup\.claude\skills\log-lesson\SKILL.md`
- **觸發**:「這個寫進教訓」/「sysadmin 教訓」/「記著下次別再」/ 顯式 `/log-lesson`
- **功能**:讀現有 briefing → 對齊格式 → 草擬新教訓段 → Wayne ack → 寫檔(無 BOM 三 byte verify)→ 提示 commit
- **紀律**:不自動 commit;Step 4 必跟 Wayne 拍板才寫檔

#### `draft-assignment` — 派工撰寫 SOP

- **路徑**:`D:\Work\system-setup\.claude\skills\draft-assignment\SKILL.md`
- **觸發**:「派工 X」/「寫派工」/「draft 一個派工」/ 顯式 `/draft-assignment`
- **功能**:從 task slug + 場景 → 對齊 `ASSIGNMENT_TEMPLATE` + SESSION_1 §4 派工層紀律(模板必含元素 / §STOP 排除執行端可自處 / §決策已定引用規則 12 / 數值門檻標 GB GiB / SHA256 mirror dropdown / 規則 15 派工檔名日期語意)→ 草擬派工初稿
- **紀律**:不直接觸發 session 2(Wayne 中介);不擅自落地;複雜派工(引用 ≥ 5)可 invoke `assignment-verifier` subagent 並行 verify

#### `integrate-progress-report` — 整合 progress report 進主 MD

- **路徑**:`D:\Work\system-setup\.claude\skills\integrate-progress-report\SKILL.md`
- **觸發**:「讀 progress-reports/<檔>」/「整合 progress report」/「整理進度報告」/ 顯式 `/integrate-progress-report`
- **功能**:讀 progress report → 整理候選證據強度更新表 / 攤下輪 verify 路線(規則 9 訂正版)/ raise 教訓暫存 / 評估 commit 點 / 草擬主 MD patch
- **紀律**:工程選擇可推 / 系統決策嚴格中性,≤ 3 選項;不擅自落地主 MD patch;教訓暫存到 commit 點才一併拍板

#### `dispatch-commit` — commit 派工拆批 SOP

- **路徑**:`D:\Work\system-setup\.claude\skills\dispatch-commit\SKILL.md`
- **觸發**:「催 commit」/「到 commit 點」/「寫 commit 派工」/ 顯式 `/dispatch-commit`
- **功能**:讀 working tree status + recent commits → 評估拆批 → 草擬 commit message(對齊既有風格)→ 寫 commit 派工到 `assignments/`
- **紀律**:不直接 commit / 不直接 push;拆批 message 草稿 by 主視窗(對齊 user-level CLAUDE.md 硬規則 4);Step 5 必跟 Wayne 拍板才落地

### 2.2 Session 2 執行端 skill

#### `progress-report` — 產任務進度報告到 progress-reports/

- **路徑**:`D:\Work\system-setup\.claude\skills\progress-report\SKILL.md`
- **觸發**:派工跑完最後一 step / Wayne 說「寫 progress report」/ 顯式 `/progress-report`
- **功能**:讀 `PROGRESS_TEMPLATE.md` → 草擬 report → 寫檔到 `progress-reports/<YYYY-MM-DD>_<task-slug>.md`(無 BOM)→ 提示貼回主視窗
- **紀律**:secret 不寫進 report;不自動 commit(progress-reports/ gitignored)

#### `rule-15-verify` — 派工檔名日期驗證

- **路徑**:`D:\Work\system-setup\.claude\skills\rule-15-verify\SKILL.md`
- **觸發**:讀派工剛完(step 0)/ 顯式 `/rule-15-verify <檔名>`
- **功能**:跑 SESSION_2 §3.1 step 1.5 PowerShell 腳本 — verify 派工檔名日期 = 實機今日,mismatch 觸發 rename + progress report 用 `$today`
- **紀律**:每份派工讀完都跑(不選擇性跳過);mismatch 自動 rename 不 STOP;progress report 路徑必用 `$today`

#### `smoke-test-comfyui` — ComfyUI 煙測前置 SOP

- **路徑**:`D:\Work\system-setup\.claude\skills\smoke-test-comfyui\SKILL.md`
- **觸發**:派工含「跑 ComfyUI 煙測」/「smoke test」/ 顯式 `/smoke-test-comfyui`
- **功能**:封裝煙測前置 SOP — `POST /free` 釋放 model cache(踩坑 #16)/ `nvidia-smi` VRAM check / submit `--seed` 強制 reseed(踩坑 #13)
- **紀律**:跑前必跑 Step 1 + Step 2;submit 必帶 `--seed`;VRAM 門檻 GB / GiB 標明(規則 13);派工沒列的不調(SESSION_2 §3.2)

#### `commit-execution` — commit 派工執行 SOP

- **路徑**:`D:\Work\system-setup\.claude\skills\commit-execution\SKILL.md`
- **觸發**:Wayne 說「讀 assignments/<commit-檔>」/ 顯式 `/commit-execution <檔名>`
- **功能**:封裝 commit 派工執行流程 — `git status` verify staged / `git add` / `commit -m` / `log --stat -1` / `push origin main` / 最終 `git status`
- **紀律**:commit 前 verify staged 對齊拆批(SESSION_2 §4.6);push 前不 STOP(2026-05-03 永久訂正);不繞 hook(不 `--no-verify`);不替主視窗草擬 commit message

### 2.3 共用 skill

#### `raise-pitfall` — 把踩坑寫進對應子目錄 setup.md

- **路徑**:`D:\Work\system-setup\.claude\skills\raise-pitfall\SKILL.md`
- **觸發**:「這個踩坑要記下來」/「加進 setup.md 踩坑」/「記到 conflicts.md」/ 顯式 `/raise-pitfall`
- **功能**:確認目標檔(comfyui / openwebui / ai-models / 等)→ grep 既有坑編號 → 草擬新坑 → Wayne ack → 寫檔 → 提示 commit
- **隸屬**:任一 session 撞到環境踩坑都可觸發,執行端機率較高(實機跑時撞到的多)

---

## 3. 內建 / plugin skill(跨 session 通用)

從 user-level / plugin 載入,任一 session 都可呼叫。常用清單:

| skill | 用途 | session 1 主用 | session 2 主用 |
|---|---|:-:|:-:|
| `update-config` | 改 `settings.json` / hooks / 權限 / env vars | ✓ | ✓ |
| `loop` | 重複 / 自我節奏的任務(每 N 分鐘 / 自定觸發) | — | ✓ |
| `schedule` | 建 / 改 / 列遠端 cron agent(routine) | ✓ | — |
| `claude-api` | Claude API / Anthropic SDK 開發、prompt caching、模型升級 | ✓ | ✓ |
| `simplify` | 跑完 task 複查改動代碼可重用 / 品質 / 效率 | — | ✓ |
| `fewer-permission-prompts` | scan transcripts → 加白名單到 `settings.json` | ✓ | — |
| `init` | 初始化 `CLAUDE.md` 描述 codebase | ✓ | — |
| `review` | review pull request | ✓ | — |
| `security-review` | security review pending changes | ✓ | — |
| `keybindings-help` | 改 `~/.claude/keybindings.json` | ✓ | ✓ |

「主用」= 該 session 場景上最常觸發;另一個 session 也可用,只是頻率低。

---

## 4. 候選池(待發掘)

(本檔 v1.0 提案 9 條已全部落地進 §1 / §2;候選池目前為空。)

未來新需求識別出 subagent / skill 候選時,先寫進本段(動機 / ROI 評估 / 待拍板要點),Wayne ack 後落地進 §1 / §2。

---

## 5. 紀律:往後新增 subagent / skill 比照辦理

新增 subagent / skill 時依本檔分類補進對應段。**規則:**

### 5.1 隸屬判定

- **session 1 主視窗**(規劃 / 派工 / 整合 / 不執行)→ 進 §1.1 / §2.1
- **session 2 執行端**(實機操作 / 跑派工 / 寫 progress report)→ 進 §1.2 / §2.2
- **兩 session 都會用** → 進 §1.3 / §2.3
- 隸屬不清楚 → 主視窗 raise 給 Wayne 拍板,不擅自分類

### 5.2 落地路徑

- **subagent**:`.claude/agents/<name>.md`(YAML frontmatter:`name` / `description` / `tools` / `model`)
- **skill**:`.claude/skills/<name>/SKILL.md`(YAML frontmatter:`name` / `description`)

新增後本 catalog 對應段加 entry — 路徑 / 功能 / 觸發或 invoke 場景 / 紀律。

### 5.3 規則 source-of-truth 不破壞

subagent / skill 內部紀律對齊 `SYSADMIN_BRIEFING.md` 規則 1-N 既有定義 — 改規則改 source-of-truth(`SYSADMIN_BRIEFING.md`),本 catalog 是引用層,自然 sync。

### 5.4 commit 走 session 2

本檔修改視同規則文件變動 — 主視窗 raise → Wayne ack → 寫 commit 派工 → session 2 跑(對齊 user-level `CLAUDE.md` 硬規則 4)。

### 5.5 命名規則

- 名稱用 kebab-case 英文(對齊既有 `rule-curator` / `log-lesson` / `progress-report` / `raise-pitfall` / `community-researcher` 等)
- 名稱要 self-explanatory,看到名稱大致知道做什麼(例 `rule-15-verify` / `community-researcher` 比 `helper-1` / `tool-2` 好)
- session 隸屬**不寫進名稱**(由本 catalog 分類段管理),避免 session 架構變動時 rename rolling

---

**最後更新**:2026-05-04
**版本**:1.1(v1.0 提案 9 條全部落地;subagent 4 + repo skill 9 + 內建 plugin skill 10)
