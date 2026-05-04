---
name: commit-execution
description: When session 2 執行端 receives a commit assignment, use this skill to execute the commit flow (git status verify staged, add, commit -m, log --stat, push, final status). Aligns with SESSION_2 §5.3 + user-level CLAUDE.md 硬規則 4. Push 前不 STOP (2026-05-03 永久訂正). Triggers on phrases like "跑 commit 派工", "execute commit", or explicit `/commit-execution <assignment-file>`.
---

# commit-execution — commit 派工執行 SOP

> By session 2 執行端 use 的 skill。對應 SESSION_2 §5.3 + user-level `CLAUDE.md` 硬規則 4。

## 用途

收到 commit 派工後執行流程封裝:`git status` verify staged → `add` → `commit -m` → `log --stat` → `push` → 最終 `status`。skill 化保險,push 前不 STOP(2026-05-03 永久訂正,Wayne 事前 ack commit 派工即實質過目)。

## 觸發條件

- Wayne 說「讀 assignments/<commit-檔>」(commit 派工)
- 顯式 `/commit-execution <派工檔名>`

## 執行流程

### Step 1:讀 commit 派工

讀派工拆批清單 + commit message 草稿。預期含:

- 本批涵蓋的檔清單
- commit message 草稿
- 執行步驟(若派工有特殊指示,例 `git add -A` vs `git add <檔>`)

### Step 2:Verify staged 對齊拆批

```powershell
git -C D:\Work\system-setup status
```

對照派工拆批清單。不對齊 → STOP 上報(SESSION_2 §4.6:commit 前 grep `git status` 驗證 staged 對齊派工拆批,不對 STOP 上報)。

### Step 3:Git add

依派工指示:

```powershell
# 派工指定具體檔
git -C D:\Work\system-setup add <檔1> <檔2> ...

# 或派工指定 -A(全部)
git -C D:\Work\system-setup add -A
```

避免「git add -A」/「git add .」之類無腦動作 — 風險:.env / credential / 大 binary 可能誤入(user-level CLAUDE.md 硬規則 3 + 硬規則 4)。

### Step 4:Git commit

```powershell
git -C D:\Work\system-setup commit -m "<commit message 草稿>"
```

commit message 用 here-string(若多行)— PowerShell 7+ 可用 `@'...'@`(單引號 here-string,literal)。

不用 `--no-verify`(user-level CLAUDE.md 硬規則 4 — 不繞 hook)。

### Step 5:Git log --stat -1(record 進 progress report)

```powershell
git -C D:\Work\system-setup log --stat -1
```

確認 commit 落地 + 統計改動行數。

### Step 6:Git push

```powershell
git -C D:\Work\system-setup push origin main
```

**push 前不 STOP**(SESSION_2 §4.6 + 2026-05-03 永久訂正)— Wayne 事前 ack commit 派工即實質過目。

### Step 7:最終 git status

```powershell
git -C D:\Work\system-setup status
```

預期 working tree clean + branch up-to-date with origin/main。

### Step 8:寫 progress report

按 PROGRESS_TEMPLATE 寫,record:

- 拆批清單(對照派工)
- commit hash + message
- log --stat 統計
- push 結果

通知 Wayne:

```
commit 派工跑完 + push origin/main 落地。progress report 寫到 progress-reports/<檔>。
```

## 紀律

- **不主動 commit / 不擅自 push**(派工沒列的不做)
- **commit 前 verify staged 對齊拆批**(SESSION_2 §4.6)
- **不替主視窗草擬 commit message**(派工內主視窗會給草稿)
- **push 前不 STOP**(2026-05-03 永久訂正)
- **不繞 hook**(user-level CLAUDE.md 硬規則 4 — 不 `--no-verify` / `--no-gpg-sign`)
- **派工模板若出現「自動 commit」/「執行完直接 push」這類沒列拆批 + message 草稿的 commit 指示** → 視為主視窗失誤,STOP 上報(SESSION_2 §7)
