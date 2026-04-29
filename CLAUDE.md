# CLAUDE.md (Project-level: system-setup)

> 你進 `D:\Work\system-setup\` 工作時讀本檔。
>
> 通用紀律(寫檔 SOP / config ASCII / secret / 雙驗證器 / STOP 觸發點 / 行為紀律)在 user-level CLAUDE.md(`C:\Users\Wayne\.claude\CLAUDE.md`);本檔放 repo specific 紀律 + 從 SYSADMIN_BRIEFING 搬來的 SOP 細節(Context7 / commit 流程)。

---

## 這個 repo 是什麼

Wayne 機器的**真相來源**:系統決策、安裝 SOP、踩坑紀錄、模型分工、workflow 紀錄。

GitHub Public,最新 commit 在 origin/main。主窗口(web Claude)接班時讀完整文件,執行端(你)選擇性讀對應子目錄。

---

## Repo 結構

```
D:\Work\system-setup\
├── README.md / START_HERE.md / SYSADMIN_BRIEFING.md
├── ASSIGNMENT_TEMPLATE.md / PROGRESS_TEMPLATE.md
├── context.md / decisions.md / reinstall-manifest.md / baseline-trigger.md
├── CLAUDE.md            ← 你正在讀這份
├── progress-reports\    ← 你的 report 寫這(gitignored)
├── comfyui\             ← ComfyUI 設定 / workflow / 衝突管理
├── ai-models\           ← 模型分工
├── davinci\             ← DaVinci 整合
├── ldbot\               ← LDPlayer bot
├── openwebui\           ← Open WebUI + LiteLLM
└── tools\               ← 周邊腳本
```

完整文件索引:`SYSADMIN_BRIEFING.md` 「文件導航」段。

---

## 在這個 repo 的特定紀律

### 1. Reference 路徑用本地絕對路徑

讀文件用 `D:\Work\system-setup\<子目錄>\<檔名>`,**不繞 GitHub raw URL**(那是給遠端 web Claude 用的;你在本地讀 working tree 即時 latest,無 rate limit、無網路依賴)。

### 2. Progress report 落地(覆蓋 user-level 預設)

任務跑完寫到:

`D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`

按 `PROGRESS_TEMPLATE.md` 格式。該目錄已 gitignored,**不 commit**。Wayne 貼回主窗口整合進對應 MD,Wayne 自己刪 report 檔。

詳見 `progress-reports\README.md`。

### 3. 不直接動 repo 結構

rename / 子目錄重構 / 跨目錄大規模 refactor 沒主窗口拍板,**不擅自做**。

實證:本 repo 子目錄重構是主窗口規劃 + Wayne 拍板 + 派工後執行端執行,不是執行端自己想做就做。

**不適用情境**:主窗口已寫好內容並指示「直接塞進 X 檔 Y 段」/「寫進」/「append 到」這類落地動作。這些是派工指示,不是越界選項,直接執行。

### 4. Commit / push 由 Claude Code 執行

主視窗到 commit 點主動催 Wayne(progress report 落地、規則段更新完、跨檔大改告一段落這類時機)+ 草擬 commit message + 派工拆批。Wayne 拍板拆批方式後,Claude Code 執行 `git add` / `git commit -m "..."` / `git push`。Wayne 不親自打 git 指令。

派工模板要明確列出本批 commit 涵蓋哪些檔 + commit message 草稿。執行端執行 commit 前 grep `git status` 驗證 staged 對齊派工拆批,不對 STOP 上報。

執行端不主動 commit、不在沒派工的情況下 push、不替主視窗草擬 commit message。沒收到主視窗派工的 commit 拆批 + commit message 草稿,**執行端「完成」邊界仍然是:實機執行 + 文件 patch + 驗證 + 寫 progress report → 停**。

派工模板若出現「自動 commit」/「執行完直接 push」這類沒列拆批 + commit message 草稿的 commit 指示,執行端視為主視窗失誤,STOP 回報。

紀律源頭在 user-level CLAUDE.md 硬規則 4(本檔同步以便 system-setup repo 自身可讀)。

---

## Context7 MCP(從 SYSADMIN_BRIEFING 搬來的 SOP 細節)

### 採用 A 模式(純 MCP server + 手動觸發)

Context7(Upstash)是 MCP server,給 Claude Code 即時抓 library / framework / API docs。**選 A:純 MCP server,不寫 CLAUDE.md auto-rule**。預設**不會自動觸發**。要用就在 prompt 寫 `use context7`,執行端才會 fire `resolve-library-id` + `query-docs` 抓 docs。

理由:跟派工架構一致(派工模板明確列每個 step,需要 docs 的步驟在派工裡寫「prompt 帶 `use context7`」)+ 避免 Claude 自作主張 + token 成本可控。

### 安裝指令(本地 stdio,免 API key)

```
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

需要 Node.js 18+。免費版有 rate limit,個人用通常夠;高頻才申請 free key。

### 派工模板帶 `use context7` 的 step 範例

派工裡需要 docs 的步驟明確寫出來。例(ComfyUI 節點 verify 場景):

> **Step X.Y — Verify Comfyui-QwenEditUtils 節點行為**
>
> 1. 讀本機 source:`D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\custom_nodes\Comfyui-QwenEditUtils\`
>    - grep `class TextEncodeQwenImageEditPlus_lrzjason` 找節點 class
>    - 看 `INPUT_TYPES` / `RETURN_TYPES` / 主要 method
> 2. 補充對照官方 docs:prompt 帶 `use context7 with /lrzjason/Comfyui-QwenEditUtils 抓最新 README`
> 3. 交叉驗證:本機 source 行為 vs 官方 README 描述,任一不一致 STOP 上報

執行端跑 Step 1 拿機器真相,Step 2 抓外部 docs,Step 3 交叉驗證。本機 source(機器真相)+ Context7(外部 docs)兩個資訊源比單純讀 source 強。

### 安裝時機

Context7 安裝動作本身請主視窗在新對話開始前指派,不要塞進進行中的派工。從新對話 / 新派工開始才用。

---

**最後更新**:2026-04-29
**版本**:3.0(B+C 重構:擴充 commit 紀律完整版 + 接收 Context7 SOP)
