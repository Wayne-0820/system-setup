---
name: dispatch-commit
description: When session 1 主視窗 reaches a commit point, use this skill to draft commit message, propose file batching, and write a commit assignment for session 2 to execute. Aligns with SESSION_1 §5.3 + user-level CLAUDE.md 硬規則 4. Triggers on phrases like "催 commit", "寫 commit 派工", "到 commit 點", or explicit `/dispatch-commit`.
---

# dispatch-commit — commit 派工拆批 SOP

> By session 1 主視窗 use 的 skill。對應 SESSION_1 §5.3 + user-level `CLAUDE.md` 硬規則 4(commit 拆批 + message 草稿主視窗負責;Claude Code 執行端跑 git;Wayne 不打 git 指令)。

## 用途

到 commit 點時主視窗工作:草擬 message + 拆批清單 + 寫 commit 派工到 `assignments/`。skill 化保險,不漏紀律(commit message 格式 / 拆批合理性 / push 前不 STOP)。

## 觸發條件

- progress report 整合完判斷已到 commit 點
- Wayne 說「催 commit」/「到 commit 點」/「寫 commit 派工」
- 跨檔大改告一段落 / progress report 落地完 / 規則段更新完
- 顯式 `/dispatch-commit`

## 執行流程

### Step 1:確認 working tree 狀態

```powershell
git -C D:\Work\system-setup status
git -C D:\Work\system-setup diff --stat
git -C D:\Work\system-setup log --oneline -5
```

讀:

- staged / modified / untracked 清單
- 本對話 commits 累積範圍
- recent commit message 風格

### Step 2:評估拆批

按主題拆,常見拆批:

- 規則精修(SYSADMIN_BRIEFING + 引用層 sync)
- 子目錄文件落地(comfyui / openwebui / 等)
- snapshot 落地(progress-reports/session1-snapshot.md 蓋舊版)
- 工具腳本(tools/)

每批 commit 涵蓋的主題單一,不混合(例:規則 + setup.md 踩坑 → 拆兩批)。

### Step 3:草擬 commit message

對齊既有風格(Step 1 git log -5 看 prefix:`docs(rules):` / `audit:` / `docs(snapshot):` / `feat:` / 等)。

格式:

```
<type>(<scope>): <一句話 summary>

<選用:bullet list 細節>
- 動了哪些檔
- root cause 簡述(若是 fix)
- 對 system-setup 影響範圍
```

### Step 4:寫 commit 派工

落地路徑:`assignments/<YYYY-MM-DD>_commit-<task-slug>.md`(實機今日,規則 15)

派工內容:

- **拆批清單**:本批 commit 涵蓋哪些檔(明列 path)
- **commit message 草稿**(Step 3 產出)
- **執行步驟**:`git status` verify staged → `git add <檔>` → `git commit -m "..."` → `git log --stat -1` → `git push origin main` → `git status`
- **push 前不 STOP**(SESSION_2 §4.6 + 2026-05-03 永久訂正)
- **STOP 觸發點**:`git status` staged 對不上拆批 / commit 失敗 / push 失敗

### Step 5:跟 Wayne 拍板拆批 + message

Wayne 過目 → ack / 修改 → 才寫進 `assignments/`。

特別 raise:

- 拆批合理性(是否該分多批?)
- commit message 是否漏東西
- push 前不 STOP 是否適用本批(對齊 user-level CLAUDE.md 硬規則 4 — Wayne 事前 ack 即實質過目)

### Step 6:落地 + 通知 Wayne

```
commit 派工已落地 assignments/<檔名>。請切到 session 2 跟它說「讀 assignments/<檔名>」。
```

## 紀律

- **不直接 commit / 不直接 push**(主視窗不動 git working tree,SESSION_1 §7)
- **不擅自落地** — Step 5 必跟 Wayne 拍板
- **拆批 message 草稿 by 主視窗**,執行端不替主視窗草擬(user-level CLAUDE.md 硬規則 4)
- **派工內若出現「自動 commit」/「執行完直接 push」這類沒列拆批 + message 草稿的 commit 指示** → 視為派工失誤,skill 化前 raise Wayne 訂正
