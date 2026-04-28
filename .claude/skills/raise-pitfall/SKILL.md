---
name: raise-pitfall
description: When Wayne or Claude Code hits an environment-level pitfall during execution (config error, version conflict, encoding issue, API behavior surprise, etc.) that should be recorded in the relevant subdirectory's setup.md pitfall section, use this skill. Triggers on phrases like "這個踩坑要記下來"、"加進 setup.md 踩坑"、"這條進 pitfall"、"記到 conflicts.md"、or explicit `/raise-pitfall` invocation.
---

# Raise Pitfall — 把踩坑寫進對應子目錄 setup.md

## 用途

執行中撞到的環境級踩坑 — 跟特定工具 / 配置 / 版本 / OS / 網路相關 — 寫進對應子目錄文件的踩坑段,讓未來重灌或別人裝同一套時不必再踩。

**跟 `/log-lesson` 的差別**:
- `/log-lesson` 是**跨工具的 sysadmin 紀律 / 派工心法**(進 SYSADMIN_BRIEFING.md 教訓段)
- `/raise-pitfall` 是**特定工具的環境踩坑**(進 `<工具>/setup.md` 或對應檔的踩坑段)

不確定走哪條 → 先問 Wayne。一條教訓可能兩邊都該記(briefing 教訓 + setup.md 踩坑連動)。

## 觸發條件

- 「這個踩坑要記下來」/「加進 setup.md 踩坑」/「這條進 pitfall」
- 「記到 conflicts.md」/ 其他特定 MD
- Wayne 顯式 `/raise-pitfall <工具名> <踩坑簡述>`

## 執行流程

### Step 1:確定目標檔

問 Wayne 或從 conversation 推斷,當下踩坑歸屬:

| 踩坑類型 | 目標檔 |
|---|---|
| Open WebUI / LiteLLM / Ollama | `D:\Work\system-setup\openwebui\setup.md` 踩坑段 |
| ComfyUI 環境 / 模型 / SageAttention | `D:\Work\system-setup\comfyui\setup.md` 踩坑段 |
| ComfyUI custom node 衝突 | `D:\Work\system-setup\comfyui\conflicts.md` 或 `conflicts-<pack>.md` |
| 模型分工 / 量化 / 雲端 API | `D:\Work\system-setup\ai-models\local-models.md` 踩坑段 |
| LDPlayer bot | `D:\Work\system-setup\ldbot\checklist.md` 踩坑段 |
| DaVinci 整合 | `D:\Work\system-setup\davinci\pipeline.md` 踩坑段 |

不在已知列表 → 問 Wayne。**不擅自選**。

### Step 2:讀目標檔現狀

```powershell
$target = "<完整路徑>"
```

定位踩坑段(通常 `## 踩坑紀錄` 或類似 H2)。grep 既有編號:

```powershell
Select-String -Path $target -Pattern '^### 坑 #\d+' | Select-Object LineNumber, Line
```

確認:
- 現有最大坑編號 N → 新坑 = N+1
- 該段在檔案哪個 line range
- 已有踩坑段標題形式(「坑 #N」/「Pitfall #N」/「⚠️ 踩坑紀錄」等),對齊既有格式

### Step 3:草擬踩坑內容(對齊既有格式)

讀既有坑 #1-N 既存格式,新坑同樣有:

- **症狀**:具體錯誤訊息 / 行為 / log line
- **原因 / Root cause**:為什麼會踩(技術原因)
- **解法**:具體指令 / 配置 / 改動
- **未來注意 / SOP**(可選):新增的紀律 / 驗證指令
- **適用範圍 / 延伸**(可選):這條只影響當前工具,還是會擴散到其他工具

對齊既有寫作風格(看坑 #1-N 用的 H4 / bold / code block 模式)。

### Step 4:跟 Wayne 確認內容

不直接動筆,先列草稿 → Wayne 改完才往下。**特別 raise**:

- 是否同時該進 SYSADMIN_BRIEFING.md 教訓段(若是跨工具紀律)?
- 是否該更新 `decisions.md` 的重灌 SOP(若是安裝步驟級的踩坑)?

Wayne 拍板後再往下。

### Step 5:寫檔(三 byte 驗證)

```powershell
$content = [System.IO.File]::ReadAllText($target, [System.Text.UTF8Encoding]::new($false))

# 字串替換 — anchor 是踩坑段下一個 H2(例「## 重建流程」)
$newPitfall = @"
### 坑 #N+1:<標題>

**症狀**:
...

**原因**:
...

**解法**:
...

"@

$content = $content.Replace("<下一個 H2 anchor>", "$newPitfall<下一個 H2 anchor>")

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($target, $content, $utf8NoBom)

# 驗證
$b = [System.IO.File]::ReadAllBytes($target)[0..2]
"BOM check: $($b -join ',')  (期望:不是 239,187,191)"
```

### Step 6:diff + commit 提示

```powershell
cd D:\Work\system-setup
git diff <target 相對路徑>
```

Wayne 看 diff 確認,然後給建議 commit message:

```
docs(<子目錄>): add pitfall #N+1 — <標題>

<簡述 root cause 一句>
<簡述解法一句>
```

提醒:`git add <檔> && git commit && git push`。**不自動 commit**。

## 紀律

- **Step 4 必跟 Wayne 確認**,不直接動筆改主 MD
- **不修舊踩坑**(只 append 新的),修舊條走手動流程
- **踩坑段超過 6-8 條** → 提醒 Wayne 考慮拆檔或合併(但不主動拆)
- **跨工具教訓**(影響不只當前工具)→ raise 是否同時 `/log-lesson` 進 briefing
