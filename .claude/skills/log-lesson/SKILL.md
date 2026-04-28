---
name: log-lesson
description: When Wayne identifies a new sysadmin lesson, discipline, or workflow rule that should be persisted across sessions, use this skill to format it and append to SYSADMIN_BRIEFING.md's lessons section. Triggers on phrases like "這個寫進教訓"、"這條紀律該記下來"、"這要進 briefing"、"sysadmin 教訓"、"記著下次別再"、or explicit `/log-lesson` invocation.
---

# Log Lesson — 沉澱跨 session 教訓進 SYSADMIN_BRIEFING.md

## 用途

Wayne 認定當下對話冒出的新教訓 / 紀律值得跨 session 沉澱時,用本 skill 自動化「讀現有 briefing → 對齊格式 → 產新教訓段 → 寫檔 → 提示 commit」流程。

## 觸發條件(描述命中)

Claude Code 看到下列訊號自動觸發:

- 「這個寫進教訓」/「這條紀律該記下來」/「這要進 briefing」
- 「sysadmin 教訓」/「記著下次別再」
- Wayne 顯式 `/log-lesson <教訓主題>`

不確定該不該觸發 → 問 Wayne「這條要進教訓段嗎?」,得到「對」再走流程。

## 執行流程

### Step 1:讀現有 SYSADMIN_BRIEFING.md

```powershell
$briefing = "D:\Work\system-setup\SYSADMIN_BRIEFING.md"
```

定位「Sysadmin 慣例 / 教訓」H2 段。grep 既有編號:

```powershell
Select-String -Path $briefing -Pattern '^### \d+\.' | Select-Object LineNumber, Line
```

確認:
- 現有最大編號 N → 新教訓 = N+1
- 教訓段在 briefing 哪個 line range → 新教訓 append 到該段尾、下一個 H2 之前

### Step 2:跟 Wayne 確認教訓內容

不直接動筆,先草擬 + 列給 Wayne:

- **教訓編號**:N+1
- **教訓標題**(一句話 H3)
- **現象 / Context**:踩坑或情境
- **原因 / Root cause**:為什麼會踩
- **紀律 / Rule**:下次怎麼避(1-3 點)
- **延伸閱讀**:相關 MD(子目錄 setup.md 踩坑段、其他教訓編號)

對齊既有教訓 1-N 的寫作風格(看 briefing 教訓 1-N 既存格式)。Wayne 改完才往下。

### Step 3:寫檔(三 byte 驗證)

定位插入點(現有最後一條教訓的尾行 + 下一個 H2 之前的空行)。用 .NET API 寫:

```powershell
# 先讀整檔
$content = [System.IO.File]::ReadAllText($briefing, [System.Text.UTF8Encoding]::new($false))

# 字串替換(找最後一條教訓尾的 anchor + append 新教訓)
# anchor 可以是已知的下一段 H2 標題(例如 "## 文件導航")
$newLesson = @"
### N+1. <教訓標題>

<內容...>

"@

$content = $content.Replace("---`n`n## 文件導航", "---`n`n$newLesson---`n`n## 文件導航")

# 寫回(無 BOM)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($briefing, $content, $utf8NoBom)

# 三 byte 驗證
$b = [System.IO.File]::ReadAllBytes($briefing)[0..2]
"BOM check: $($b -join ',')  (期望:不是 239,187,191)"
```

是 BOM → STOP,從新 string 重寫。

### Step 4:diff 給 Wayne 確認

```powershell
cd D:\Work\system-setup
git diff SYSADMIN_BRIEFING.md
```

讓 Wayne 看 diff,確認:
- 編號正確(N+1)
- 位置正確(教訓段尾,文件導航之前)
- 內容對齊既有風格
- 沒污染其他段

### Step 5:提示 commit(不自動執行)

print 建議 commit message:

```
docs(briefing): add lesson #N+1 — <教訓標題>

<簡述 root cause 一句>
<簡述 rule 一句>
```

提醒 Wayne:`git add SYSADMIN_BRIEFING.md && git commit && git push`。**不要自己 commit**。

## 注意

- 教訓段是跨 session 真相,寫錯影響大,**Step 2 一定要 Wayne 拍板才往下**
- 不修現有教訓 1-N(只 append),修舊條走另一條手動流程
- 教訓 5 條 → 6 條 → 越多越無感,如果發現 Wayne 一次想加多條,提醒他「教訓段超過 8-10 條會降低可讀性,考慮合併或下放到對應子目錄 MD」
