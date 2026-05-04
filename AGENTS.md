# AGENTS.md (Project-level: system-setup)

> 你進 `D:\Work\system-setup\` 工作時讀本檔。
>
> 本檔是 **hand-crafted Codex repo instructions**(Wayne 拍板 Lane C,2026-05-04),不是 Codex Desktop mirror 產生的 Claude -> Codex dumb replace 版。
>
> Claude Code 專用 source-of-truth 仍是 `CLAUDE.md` / `SESSION_1_MAINWINDOW.md` / `SESSION_2_EXECUTOR.md`。Codex 進場時用本檔,並對照 `codex/setup.md` 的 Codex 三件套實況。

---

## 這個 repo 是什麼

Wayne 機器的**真相來源**:系統決策、安裝 SOP、踩坑紀錄、模型分工、workflow 紀錄。

GitHub Public,最新 commit 在 `origin/main`。不要把 secret / token / 個人帳號資訊寫進 repo。

---

## 先讀哪些文件

一般 Codex 進場:

1. `AGENTS.md`(本檔)
2. `README.md`(文件索引)
3. `codex/setup.md`(Codex plugin + 桌面板 + CLI 三件套,含 sandbox / mirror-like artifacts 踩坑)
4. 依任務讀對應子目錄文件(例 `comfyui/setup.md` / `openwebui/setup.md` / `tools/README.md`)

若 Wayne 明確說你是 **session 1 主視窗**:

1. 讀 `SESSION_1_MAINWINDOW.md`
2. 讀 `SYSADMIN_BRIEFING.md`
3. 讀 `progress-reports/session1-snapshot.md`
4. 依 session 1 規則規劃 / 派工 / 整合,不直接跑實機

若 Wayne 明確說你是 **session 2 執行端**:

1. 讀 `SESSION_2_EXECUTOR.md`
2. 等 Wayne 給「讀 assignments/<檔>」
3. 嚴格依派工執行,寫 progress report,不擅自規劃下輪

---

## Repo 結構

```
D:\Work\system-setup\
├── README.md / START_HERE.md / SYSADMIN_BRIEFING.md
├── AGENTS.md / CLAUDE.md
├── SESSION_1_MAINWINDOW.md / SESSION_2_EXECUTOR.md
├── ASSIGNMENT_TEMPLATE.md / PROGRESS_TEMPLATE.md
├── progress-reports\    ← report 暫存(gitignored,README + session1-snapshot 例外)
├── assignments\         ← session 1 派工暫存(gitignored,README 例外)
├── codex\               ← Codex 三件套設定 / 踩坑
├── comfyui\             ← ComfyUI 設定 / workflow / 衝突管理
├── ai-models\           ← 模型分工
├── davinci\             ← DaVinci 整合
├── ldbot\               ← LDPlayer bot
├── openwebui\           ← Open WebUI + LiteLLM
└── tools\               ← 周邊腳本
```

完整文件索引看 `SYSADMIN_BRIEFING.md`「文件導航」段與 `README.md`。

---

## 在這個 repo 的特定紀律

### 1. Reference 路徑用本地絕對路徑

讀文件用 `D:\Work\system-setup\<子目錄>\<檔名>`,**不繞 GitHub raw URL**。你在本機 working tree,本地檔案才是即時真相。

遠端 / web-only 執行端才需要 GitHub raw URL;本機 Codex 不需要。

### 2. 不直接動 repo 結構

rename / 子目錄重構 / 跨目錄大規模 refactor 沒 Wayne 或主視窗拍板,**不擅自做**。

例外:Wayne 已明確指示「新增 X 子目錄」/「直接塞進 X 檔 Y 段」/「append 到」這類落地動作,即可依指示執行。

### 3. Commit / push 紀律

不主動 commit / push。Wayne 明確要求或 session 1 派 commit 派工時才做。

若同時有多批無關修改,先拆批說清楚:

- 規則 / 紀律文件
- Codex setup / AGENTS.md
- 任務實作
- snapshot / progress cleanup

不要把 unrelated dirty files 偷偷包進同一 commit。

### 4. Progress report 清理

`progress-reports/` 是本地任務暫存。主窗口完成整合 commit / push,並覆蓋 commit / push 最新 `session1-snapshot.md` 後,可清理 `progress-reports/*.md` 舊 raw reports。

防呆:

- 只刪 `progress-reports/*.md`,不刪 `progress-reports/README.md`
- 若仍有未整合 / 未拍板 / 未 commit 的 report,STOP 不刪
- 若不確定某份 report 是否已整合,STOP 問 Wayne

### 5. Public repo / secret 紀律

本 repo 是 Public。不要寫入:

- API key / token / cookie
- 真實 credential path 內容
- 個人帳號 email
- 私人 memo

需要記錄 auth 狀態時寫「本機已驗證,不記 email」。

---

## Codex-specific 紀律

### 1. AGENTS.md source-of-truth

本檔是正式 hand-crafted `AGENTS.md`,可 commit。

不要採信 Codex Desktop mirror 產生的 dumb replace 版 `AGENTS.md`。已知錯誤包含:

- `claude mcp add ...` 被替換成不存在 / 未驗證的 Codex 命令格式
- `.claude\CLAUDE.md` 被替換成虛構 `.Codex\AGENTS.md`
- 「web Claude」被替換成語意錯誤的「web Codex」

若未來桌面板再次產生 mirror-like artifacts,先對照 `codex/setup.md` 踩坑 #2,不要直接 commit。

### 2. Mirror-like artifacts

`.agents/skills/` 與 `.codex/agents/` 目前視為 Codex Desktop mirror-like artifacts,已 gitignored。

避免廣域 ignore `.agents/` / `.codex/`:未來 Codex marketplace metadata / repo-native 設定可能落在這些路徑。

### 3. `/codex:review` 半通狀態

Claude Code plugin 內的 `/codex:review` 已知在 Wayne Windows 環境撞 sandbox 嵌套 spawn:

```
companion script
  -> reviewer agent
    -> pwsh.exe (CreateProcessAsUserW access error)
```

達成:plugin install / reload / setup / auth / thread 啟動 / MCP resource list。

未達成:repo review agent inspect。

不要把這寫成「review 完整可用」。詳情看 `codex/setup.md` 踩坑 #1。

### 4. `/goal` feature

Codex CLI 0.128.0 有 `goals` feature flag,本機查到狀態為 `under development false`。未經 Wayne 拍板不要把 `/goal` 放進 system-setup 主流程。

若要試,建議先在低風險 repo / 乾淨 branch 試,並明確記錄 feature flag 與結果。

### 5. Context7

`CLAUDE.md` 裡的 Context7 MCP 安裝命令是 Claude Code 語境。不要做機械 Claude -> Codex 命令替換。

Codex 預設不自動查外部 docs。只有 Wayne 或派工明確要求「use context7」或「查官方 docs」時才使用可用 MCP / web / 官方文件;若需要安裝或改 MCP 設定,先拍板。

---

## 行為邊界

- 指控既有 MD 有 bug 前先 grep / read verify,不靠記憶。
- 碰到預期外 working tree 變更,先 STOP / 說明,不要直接整理進 commit。
- 工程選擇可主動駁回顯然次優,但系統決策要攤事實 + 候選 + 利弊,讓 Wayne 拍板。
- 寫文件時區分「實證」/「推測」/「未實測」,不要 over-claim。
- 探查 auto-generated artifact 時優先 rename probe,不要一開始就 delete probe target。
- 用繁體中文(台灣用語),技術術語英文混用 OK。

---

**最後更新**:2026-05-04
**版本**:1.0(Lane C:hand-crafted Codex AGENTS.md 入駐)
