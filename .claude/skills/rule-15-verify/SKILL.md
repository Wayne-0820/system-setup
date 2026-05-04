---
name: rule-15-verify
description: When session 2 執行端 receives an assignment, use this skill immediately after reading to verify the assignment filename date matches today (rule 15 step 1.5). If mismatch, rename the assignment file and use $today for progress report path. Triggers on phrases like "rule 15 verify", "派工日期 verify", or explicit `/rule-15-verify <filename>`.
---

# rule-15-verify — 派工檔名日期驗證

> By session 2 執行端 use 的 skill。對應 SESSION_2 §3.1 step 1.5 + SYSADMIN_BRIEFING 規則 15「派工 / progress report 日期語意統一為實機執行當天」。

## 用途

每份派工讀完後立刻跑 verify(派工檔名日期 = 實機今日)— 若 mismatch(主視窗跨日寫的派工),rename 派工檔對齊實機今日 + progress report 用 `$today`。skill 化降低漏 step 機率。

## 觸發條件

- 執行端讀「assignments/<檔>」剛完(派工讀完 step 0)
- 顯式 `/rule-15-verify <派工檔名>`

## 執行流程

### Step 1:讀派工檔名

```powershell
$assignFile = '<派工檔名,例 2026-05-04_foo.md>'
$today = Get-Date -Format 'yyyy-MM-dd'
$assignDate = $assignFile.Substring(0, 10)
```

### Step 2:Verify

```powershell
if ($today -ne $assignDate) {
    # mismatch: 跨日場景,rename 派工 + progress report 用 $today
    $newName = "${today}_$($assignFile.Substring(11))"
    Rename-Item "D:\Work\system-setup\assignments\$assignFile" `
                "D:\Work\system-setup\assignments\$newName"
    "派工檔名 mismatch: $assignFile → $newName(rename 對齊實機今日 $today)"
} else {
    "派工檔名 match: $assignDate = 實機今日 $today"
}
```

### Step 3:Progress report 路徑用 $today

跑完 task 寫 progress report 時,落地路徑必用 `$today`(而非派工原檔名日期):

```
progress-reports/<$today>_<task-slug>.md
```

對應 SYSADMIN_BRIEFING 規則 15「progress report 用 $today」紀律。

### Step 4:回報

- match 場景:不需 rename,繼續跑派工
- mismatch 場景:已 rename,跑派工時用新檔名

## 紀律

- **每份派工讀完都跑**(不選擇性跳過)
- **mismatch 自動 rename**(不 STOP 等 Wayne — 規則 15 已落地)
- **progress report 路徑必用 `$today`**,不沿用派工原檔名日期
- **跨日場景由執行端自動處理**,主視窗派工撰寫不預判跨日
