# Session 交接快照 — 給下一個主窗口 Claude

> **建立日期**:2026-04-29
> **適用對話**:Wayne 接續本次 sysadmin session 後開新對話用
> **使用方式**:Claude Projects 已啟用,本檔在 project knowledge 中自動載入,新主窗口開新對話即讀
> **角色定位**:你是接班的主窗口 = sysadmin + 決策諮詢

---

## 1. 你接到的 repo 在什麼狀態

### 結構現況(2026-04-29)

跟 04-28 handoff 結構一致 + 新增 `.claude/skills/`:

```
D:\Work\system-setup\
├── README.md
├── START_HERE.md
├── SYSADMIN_BRIEFING.md         ← 教訓 1-5(本次新增 5)
├── PROGRESS_TEMPLATE.md
├── CLAUDE.md                    ← project-level(本次 v2.0,從 v1.0 拆分)
├── context.md
├── decisions.md
├── reinstall-manifest.md
├── baseline-trigger.md
├── .claude\skills\              ← 本次新增
│   ├── log-lesson\SKILL.md
│   ├── progress-report\SKILL.md
│   └── raise-pitfall\SKILL.md
├── progress-reports\            ← gitignored 整體,README.md 例外
├── comfyui\
├── ai-models\                   ← local-models.md 雲端 API 表 + 已駁回段更新
├── davinci\
├── ldbot\
├── openwebui\                   ← setup.md 加擴充 NIM 段 + 踩坑 #4
└── tools\
```

**Wayne user-level CLAUDE.md** 在 `C:\Users\Wayne\.claude\CLAUDE.md`(不入這個 repo,跨所有 working directory 自動載入)。

### Git 狀態

main 分支跟 origin/main 同步,working tree 應該乾淨。最近 commit 鏈(從新到舊,概略):

```
feat(skills): add three project-level skills for workflow acceleration
docs: gitignore exception for .claude/skills/
docs(claude.md): split into user-level + project-level
docs: integrate NIM deepseek deployment + cp950 lesson
docs: add progress-reports/ for local exec handoffs
docs(briefing): clarify exec-target routing for handoff references
docs(ai-models): add 'rejected options' section
docs: post-restructure cleanup + rgthree catch-up landing
```

(實際 commit message 可能略有差異,以 `git log --oneline -10` 為準)

---

## 2. 本次 session 完成的事 + 為什麼這樣設計

### 2.1 LiteLLM proxy 加 NVIDIA NIM 兩個 deepseek 模型

**任務目標**:`D:\Work\LiteLLM\litellm_config.yaml` 加 `deepseek-v4-pro` / `deepseek-v4-flash` 透過 NIM 雲端呼叫,兌現 `ai-models/local-models.md` 「已駁回 → DeepSeek V4-Pro 本地化」段的「替代方案」承諾。

**結果**:
- v4-pro:三層驗證全通,production-ready
- v4-flash:NIM upstream 暫停服務(build.nvidia.com「We'll Be Right Back / high traffic」),config 條目就位待復服。**復服後直接重打 chat completion 即可,無需改 config**

**踩坑(三個)**:
1. .env 的 NVIDIA_API_KEY 前綴重複 `nvapi-nvapi-`(Notepad 編輯時複製貼上多帶一次前綴)+ Notepad 預設加 BOM
2. **LiteLLM 1.55.10 在 Windows 繁中系統讀含中文註解的 config → `UnicodeDecodeError: cp950`** — Python `yaml.safe_load(open(file))` 沒帶 `encoding='utf-8'`,Windows 預設 codepage = cp950 解 UTF-8 中文 byte 失敗。**這條已沉澱進 SYSADMIN_BRIEFING 教訓 5 + openwebui/setup.md 踩坑 #4**
3. NIM upstream 服務性下線時 LiteLLM 不吐 error log,看起來像 hang(實際是 silent timeout)— 派工要求「不能靠 LiteLLM 端 200 就宣告成功」,真打 chat completion 才知

**派工 progress report**:已在 Wayne 整合進 MD 後刪除(progress-reports/ 內無遺留)。

### 2.2 SYSADMIN_BRIEFING.md 新增教訓 5

**教訓 5:Windows + 繁中系統下,第三方工具讀 config 檔的 ASCII 紀律**。延伸自教訓 2(BOM)— 教訓 2 是**寫檔**端,教訓 5 是**讀檔**端,寫檔再正確也救不了讀檔端的 cp950 預設 encoding。**Config 類檔(yaml/json/toml/.env)一律純 ASCII**,中文進對應 MD 不進 config 本體。

### 2.3 CLAUDE.md 拆分成 user-level + project-level

原本單一 `D:\Work\system-setup\CLAUDE.md`(v1.0)。本次拆成兩份:

| 層級 | 路徑 | 範圍 |
|---|---|---|
| User-level | `C:\Users\Wayne\.claude\CLAUDE.md` | 跨所有 repo 通用:寫檔 SOP / config ASCII / secret / 不 commit / 雙驗證器 / STOP 觸發點 / 行為紀律 |
| Project-level | `D:\Work\system-setup\CLAUDE.md`(v2.0) | 只 system-setup 適用:repo 介紹、結構導航、本地絕對路徑、progress-reports 落地、不擅自動 repo 結構 |

**理由**:user-level 自動載入任何 working directory(包括 LiteLLM、ComfyUI、LDPlayer 等),通用紀律全 cover;project-level 只放 repo specific。

### 2.4 三個 Skills 落地(Claude Code 工作流加速)

Project-level skills 在 `.claude/skills/`:

| Skill | 觸發 | 動作 |
|---|---|---|
| `log-lesson` | 「這個寫進教訓」/「sysadmin 教訓」/ `/log-lesson` | 把當下教訓格式化 append 到 SYSADMIN_BRIEFING.md 教訓段 |
| `progress-report` | 派工跑完最後 step / 「寫 progress report」 | 按 PROGRESS_TEMPLATE 產 report 到 progress-reports/(不 commit) |
| `raise-pitfall` | 「這個踩坑要記下來」/ `/raise-pitfall <工具> <簡述>` | 把環境踩坑寫進對應子目錄的 setup.md 踩坑段 |

**全 project-level**(不放 user-level)— 因為三個都寫死 `D:\Work\system-setup\` 路徑。

`.gitignore` 改例外規則:`.claude/*` 仍 ignore,但 `!.claude/skills/` 例外。

### 2.5 Claude Projects 啟用

Wayne 在 claude.ai 建 Project(主窗口接班用),pre-load:

- SYSADMIN_BRIEFING.md
- CLAUDE.md(project-level)
- 最新 SESSION_HANDOFF_*.md(就是這份)
- README.md
- context.md

Custom instructions 已寫進 Project 設定。新主窗口開新對話自動帶上下文,**不必再貼 SYSADMIN_BRIEFING + handoff**。

子目錄 MD(comfyui/setup.md / openwebui/setup.md / ai-models/local-models.md 等)**不在 Project knowledge** — 主窗口需要時讓 Wayne 直接貼。

---

## 3. 進行中 / 等 Wayne 拍板

### 主線:依舊是 ComfyUI 中國 workflow 重建(7 個優先)

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成 |
| 2 | Flux-fill OneReward 萬物移除 | 待開始 |
| 3 | Kontext + ControlNet 姿態改變 | 待開始 |
| 4 | Qwen3 TTS 聲音克隆 | 待開始 |
| 5 | Qwen image 擴圖 | 待開始 |
| 6 | 智能多角度生成 | 待開始 |
| 7 | Qwen3 TTS 聲音設計 | 待開始 |

### 路線決策(本次新增,**重要**)

Wayne 在 session 末段拍板路線 **(A) 維持現有優先級:影片是主軸,系統建置是基礎設施**,但有三個問題 Wayne 自己該想清楚才動工(主窗口可在合適時機 raise,但不主動催):

1. **第一集真有上 YouTube 嗎?**(SYSADMIN_BRIEFING 寫「未上傳,存檔處理」)沒上傳 = 受眾假設(視障 + 幼童 + 純聽眾)還沒驗證,「1 週沒起色」停損條件還沒啟動
2. **「系統建好」對 Wayne 的定義是什麼?** ComfyUI 7 workflow 全建?CrewAI 跑通?C 槽 baseline?還是模糊「定型」?沒明確標準的目標可能是逃避產出的合理化
3. **Wayne 是不是其實只是不想做第二集?** 第一集踩 8 個坑,第二集會踩更多,「先建系統」可能是繞開累活的潛意識行為

主窗口接班時**不主動催 Wayne 回答這三題**,Wayne 自己會回來談。但記著當 Wayne 又想「先建系統再產內容」時,主窗口該禮貌 raise 這三題當提醒。

### Subagent 安排(暫不裝,等真要用)

本次 session 探索過 agency-agents(86.9k star repo,147 個 markdown agent files),驗證過 4 個對 Wayne 工作流有交集:

| Agent | 觸發時機 | 狀態 |
|---|---|---|
| Codebase Onboarding Engineer | scope ComfyUI custom node / 接 LDPlayer 模組 | **暫不裝**(等真高頻時) |
| Git Workflow Master | 日常 commit / rebase 紀律 | **暫不裝** |
| Image Prompt Engineer | 第二集動工後出視覺 | **不裝** |
| Video Optimization Specialist | 第一集真上傳後 review packaging | **不裝** |

**為什麼暫不裝**:Subagent 比 stock Claude Code **多 7 倍 token**(官方數字),自動 delegate 觸發頻率高時 Pro plan 額度可能 15 分鐘耗完。先把 Skills + Projects 用一段時間驗證價值,再決定要不要加 subagent。

**未來裝的條件**:Wayne 體感「stock Claude Code 在 scope 別人 code 時建議太多 / 太雜」、「日常 commit 有 git history 越來越亂的趨勢」,才回來裝前 2 個。

### 衝突管理:WAS 安裝在等(跟 04-28 同)

`was-node-suite-comfyui` 計畫中的下一個 pack,Wayne 會去 ComfyUI Manager 點 Install 看 conflicts 數字,然後派工執行窗口。派工模板格式詳見 04-28 handoff 第 3 段。

---

## 4. 還沒做的待辦(Wayne 沒主動要,但記著)

延續 04-28 那份,跟本次 session 結尾狀態一致:

| # | 待辦 | 觸發條件 |
|---|---|---|
| 1 | NIM 復服後重試 v4-flash chat completion | NIM upstream 復服(看 build.nvidia.com 服務 banner) |
| 2 | 中國 workflow 模型下載(~100-150 GB) | 重建 workflow 進到優先 2 之後 |
| 3 | CrewAI 第一條 agent pipeline | 1-2 個月後,等 ComfyUI workflow 告一段落 + 第二集做完 |
| 4 | 第一次 C 槽 baseline 映像 | 觸發條件全達成才做(workflow ≥3 + CrewAI 跑通 + DaVinci preset + 系統定型) |
| 5 | SageAttention issue #357 修復後重編 | 上游修復通知 |
| 6 | Hasleo Rescue USB 6 個月驗證 | 約 2026-10 月底 |
| 7 | 繁中 TTS 避雷字典(累積已知會錯字) | 第二集動工前該整理 |

主窗口紀律:**這些是「記著但不主動催 Wayne 做」**。Wayne 自己會決定何時做。主窗口角色是「他來問就提供選項 + 風險」,不是「主動建議他做什麼」。

---

## 5. Wayne 工作風格(本次 session 觀察補充)

延續 04-28 那份(細節 / 容易誤解的點都還適用)。本次 session 補幾條觀察:

### 細節

- **不接受過早推薦**:本次 session 我推 subagent 太早,沒講清楚 token 成本,Wayne 拍 (A) 路線後我才回認「之前推得太早 + 資訊不對等」。**主窗口推方案要先講成本 / 限制 / 適配條件**,不只講優點
- **要求邏輯一致性**:本次 session 我推「MCP 接 GitHub 讓主窗口讀 repo」,Wayne 抓「web_fetch 對 GitHub 60/hour rate limit + raw URL allowlist 拒絕,你自己 SYSADMIN_BRIEFING 教訓 3 都寫了這條紀律」— **主窗口推方案前要對照自己寫過的紀律,不前後矛盾**
- **拍板簡短回答**:Wayne 經常用一個字母 (A/B/C) 拍板,不重複 context。主窗口收到單字回應要對照上文準確 parse,不要追問

### 容易誤解的點

- **「想知道適合什麼應用」≠ 「列功能清單」**:Wayne 問 agency-agents 適合他什麼應用,我第一輪寫了一堆通用建議,Wayne 重問後我才聚焦到「**對他工作流真有交集的 agent**」。raise 推薦時優先看「對 Wayne 三條主軸(YouTube / ComfyUI / Coding)真有交集」,不是 agent 自身名氣
- **「能不能做」要拆成兩條**:Wayne 問「subagent 開三個做 context / 紀錄錯誤 / 彙整能不能?」,我先答「subagent 不能跨 session 持久化」(架構問題),後答「skill inject 不必要」(實作問題)。**主窗口要先指出方向錯,再講細節技術問題**,不要直接陷進實作細節
- **「工作流加速」是真實需求**:Wayne 說「最需要工作流加速」是 session 中最明確的真實需求,Skills + Projects 對這條有差異化價值,subagent 對「替代主窗口決策」沒辦法解(已認證)。記著 Wayne 真正體感的是「省接班貼 MD」「省派工模板手寫」「省教訓格式化」,不是「叫 Claude 變多個變很厲害」

---

## 6. 接班開場 SOP

跟 04-28 一致(主窗口 SOP 沒變),補一條:

### 你接班時做的事

1. Project knowledge 自動載入(SYSADMIN_BRIEFING + CLAUDE.md + 本 handoff + README + context),**不需要 Wayne 貼**
2. 用你自己的話回 Wayne 三件事:
   - 你的角色(sysadmin + 決策諮詢)
   - repo 現況(最近完成的事、待辦、進行中)
   - 進行中的脈絡(影片產出主軸、ComfyUI workflow 重建狀態、subagent 待裝)
3. 等 Wayne 給任務,**不主動建議今天做什麼**

### 接班測試題(本次 session 補一題)

承襲 04-28 的 9 題,本次 session 補一題:

**10. Wayne 拍 (A) 路線維持影片優先後,主窗口看到 Wayne 又說「先建系統再產內容」該怎麼回應?**

(預期答案:**禮貌 raise 三個 Wayne 自己該回答的問題**——第一集是否上傳、「系統建好」定義、是不是其實不想做第二集——不替 Wayne 拍板,讓 Wayne 自己面對這三條。不要直接同意「切換成系統優先」。)

---

## 7. Session 結束時 repo 的乾淨指標

下一個 session 接班時應該確認以下都成立:

- [ ] `git status` working tree clean
- [ ] `git log --oneline -10` 顯示本次 session 的 commit 鏈
- [ ] `SYSADMIN_BRIEFING.md` 教訓段有 5 條(教訓 5 = cp950 ASCII 紀律)
- [ ] `D:\Work\system-setup\CLAUDE.md` 是 v2.0(file 開頭寫 "Project-level: system-setup",有提到 user-level 拆分)
- [ ] `C:\Users\Wayne\.claude\CLAUDE.md` 存在(user-level,跨 repo 通用紀律)
- [ ] `.claude\skills\` 三份 SKILL.md 都在 git ls-files 裡
- [ ] `.gitignore` 包含 `!.claude/skills/` 例外規則
- [ ] `progress-reports\` 內**只有** README.md(本次 NIM 任務的 report 已被 Wayne 刪除)
- [ ] `openwebui\setup.md` 有「擴充:接入 NVIDIA NIM」H2 段 + 踩坑 #4
- [ ] `ai-models\local-models.md` 雲端 API 表有 deepseek 兩條 + 已駁回段「替代方案」改成「已接入」
- [ ] Claude Projects 設定:
  - knowledge 含本 handoff(`SESSION_HANDOFF_2026-04-29.md`)
  - knowledge **已移除舊的** `SESSION_HANDOFF_2026-04-28.md`(避免兩份混淆)
  - custom instructions 已貼

任一不成立 → 跟 Wayne 釐清。

---

## 8. 連結速查

主要檔的本地絕對路徑(主窗口派工執行端用本地路徑,不用 raw URL):

| 檔 | 本地路徑 |
|---|---|
| SYSADMIN_BRIEFING | `D:\Work\system-setup\SYSADMIN_BRIEFING.md` |
| CLAUDE.md (project) | `D:\Work\system-setup\CLAUDE.md` |
| CLAUDE.md (user) | `C:\Users\Wayne\.claude\CLAUDE.md` |
| openwebui setup | `D:\Work\system-setup\openwebui\setup.md` |
| ai-models local-models | `D:\Work\system-setup\ai-models\local-models.md` |
| skills 三份 | `D:\Work\system-setup\.claude\skills\<skill-name>\SKILL.md` |

GitHub raw URL **只在執行端不在 Wayne 機器上**(遠端 web Claude)時才用,本機 Claude Code 一律走絕對路徑(SYSADMIN_BRIEFING 教訓 3)。

---

**本快照建立日期**:2026-04-29
**建立背景**:本次 session 完成 LiteLLM NIM deepseek 對接(v4-pro 通、v4-flash 待 NIM 復服)+ SYSADMIN_BRIEFING 教訓 5(cp950)+ CLAUDE.md 拆 user/project + 三個 Skills + Claude Projects 啟用,共 ~8 個 commit。Wayne 路線拍板 (A) 維持影片優先,subagent 暫不裝。Wayne 收工,要交接給下個 session。
