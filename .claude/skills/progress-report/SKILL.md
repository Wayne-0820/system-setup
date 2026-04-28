---
name: progress-report
description: After completing a dispatched task from the main window, use this skill to generate a properly formatted progress report in progress-reports/ directory following PROGRESS_TEMPLATE.md structure. Triggers when Wayne or Claude Code finishes a multi-step task and needs to summarize results for the main window. Phrases like "寫 progress report"、"產出進度報告"、"task 完成了寫個 report"、or explicit `/progress-report` invocation.
---

# Progress Report — 產任務進度報告到 progress-reports/

## 用途

派工任務跑完後,把執行結果整理成符合 `PROGRESS_TEMPLATE.md` 格式的 report,落地到 `progress-reports/` 目錄。Wayne 之後把 report 內容貼回主窗口整合進對應 MD。

## 觸發條件

- Claude Code 跑完派工最後一 step
- Wayne 顯式說「寫 progress report」/「產進度報告」
- Wayne 顯式 `/progress-report`

## 執行流程

### Step 1:讀 PROGRESS_TEMPLATE.md

```powershell
$template = "D:\Work\system-setup\PROGRESS_TEMPLATE.md"
```

完整讀模板,理解每個 section 的用意 + 預期內容。**Report 格式對齊模板**,不自創段落。

### Step 2:確認 task slug + 日期

問 Wayne(或從 conversation context 推斷):

- **日期**:預設今天(用 `Get-Date -Format "yyyy-MM-dd"`)
- **task-slug**:kebab-case 短描述,例 `litellm-nim-deepseek` / `was-node-suite-install` / `comfyui-workflow-rebuild-flux-fill`
  - 推斷不出來 → 問 Wayne

最終檔名:`<YYYY-MM-DD>_<task-slug>.md`

### Step 3:確認 progress-reports/ 目錄存在

```powershell
$dir = "D:\Work\system-setup\progress-reports"
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
```

該目錄應已存在(repo 已 commit progress-reports/README.md),這條是保險。

### Step 4:草擬 report 內容

按 `PROGRESS_TEMPLATE.md` 格式,從 conversation context 抽出:

- **任務目標**(派工模板裡的「任務目標」段)
- **執行步驟與結果**(每個 Step 對應的實際輸出 / 驗證 / STOP)
- **變更摘要**(改了哪些檔、加了什麼 model、改了什麼 config)
- **學到的踩坑**(本任務新發現的環境問題 / docs 不準 / 上游 bug 等)
- **對 system-setup 文件的影響**(主窗口整合時應更新哪些 MD,具體 section)
- **待辦 / 風險 / 拍板選項**(本次未完成 / 下次回來要做的事 / Wayne 該決定的選項)
- **附錄**(完整 config / 關鍵驗證輸出 / 紀律覆誦)

**內容要實證,不空泛**:Step X 過了 → 寫實際驗證輸出(token 使用量、HTTP status、log line 等);Step Y 沒過 → 寫實際 error message + 推斷 root cause。

### Step 5:寫檔(三 byte 驗證)

```powershell
$report = "D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md"

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($report, $reportContent, $utf8NoBom)

# 驗證
$b = [System.IO.File]::ReadAllBytes($report)[0..2]
"BOM check: $($b -join ',')  (期望:不是 239,187,191)"
```

### Step 6:確認 gitignored + 提示貼回主窗口

```powershell
cd D:\Work\system-setup
git status
```

預期 `progress-reports/<YYYY-MM-DD>_<task-slug>.md` **不在 git status**(因 progress-reports/* gitignored)。如果出現在 modified 或 untracked → 設定有問題,STOP 回報。

最後告訴 Wayne:

> Report 寫到 `progress-reports\<YYYY-MM-DD>_<task-slug>.md`。把內容貼回主窗口,主窗口整合進對應 MD 後,你刪 report 檔。

**不自動 commit / 不貼內容回對話框**(除非 Wayne 明說要看)。

## 紀律

- **Secret 不寫進 report**:nvapi-、sk-ant- 等只寫 preview(15 字元截斷)。master_key 等 Wayne 標 "not-secret" 的 placeholder 例外
- **不修主 MD**:report 是過渡產物,主窗口才是整合者
- **不 commit progress-reports/**:該目錄 gitignored,寫進去不該出現在 git status
