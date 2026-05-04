---
name: integrate-progress-report
description: When session 1 主視窗 reads a progress report from session 2, use this skill to extract impact-on-system-setup-MD section, draft main MD patch, propose commit batching, and update lessons backlog. Aligns with SESSION_1 §5.2. Triggers on phrases like "讀 progress-reports/<檔>", "整合 progress report", "整理進度報告", or explicit `/integrate-progress-report`.
---

# integrate-progress-report — 整合 progress report 進主 MD

> By session 1 主視窗 use 的 skill。對應 SESSION_1 §5.2 讀完 progress report 後標準動作。

## 用途

每輪 progress report 整合是主視窗高頻動作,標準流程:整理候選證據強度 / 攤下輪 verify 路線 / raise 教訓暫存 / 評估 commit 點。skill 化壓縮重複動作。

## 觸發條件

- Wayne 說「讀 progress-reports/<檔>」/「整合 progress report」/「整理進度報告」
- 顯式 `/integrate-progress-report <檔名>`

## 執行流程

### Step 1:讀 progress report

```powershell
$report = "D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md"
```

完整讀,抓:

- 變更摘要 / 環境變更
- 學到的踩坑 / 規則 9 中性 STOP 攤候選
- 對 system-setup 文件的影響(必須更新 / 建議更新 / 建議新增)
- 待辦 / 風險 / 警告

### Step 2:整理候選證據強度更新表

承前接後 — 整合本輪 verify 結果到既有候選表。每候選標:

- 證據強度(高 / 中 / 低)
- 本輪 verify 結果(達標 / 部分支持 / 證偽)
- 下輪要 verify 什麼

### Step 3:攤下輪 verify 路線(規則 9 訂正版)

按工程選擇 vs 系統決策二分:

- **工程選擇**:可弱推 / 強推 + 駁回顯然次優,≤ 3 選項
- **系統決策**:嚴格中性,給「事實 + 各候選利弊」,≤ 3 選項

### Step 4:Raise 教訓暫存

progress report 內若有可累積教訓(踩坑 / 紀律 / 派工心法):

- 候選落點(SYSADMIN_BRIEFING / SESSION_1 / SESSION_2 / setup.md / 等)
- 主題簡述
- 暫存累積到 commit 點一併拍板

### Step 5:評估 commit 點

到 commit 點 → 觸發 `dispatch-commit` skill 草擬 commit message + 拆批。

未到 commit 點 → 派下輪派工(觸發 `draft-assignment` skill)。

### Step 6:草擬主 MD patch(若 progress report 有「對 system-setup 文件的影響」段)

- 提取「必須更新」段落 → 對應主 MD 的 patch 草稿
- 對齊既有風格(grep verify 既有段落格式,規則 8)
- patch 草稿 raise Wayne ack 後落地

### Step 7:回應 Wayne

整合回應結構:

- 候選證據強度更新表(Step 2 產出)
- 下輪 verify 路線(Step 3 攤候選)
- 教訓暫存累積(Step 4 raise)
- commit 點評估(Step 5)
- 主 MD patch 草稿(Step 6,若有)

## 紀律

- **規則 9 中性紀律**:工程選擇可推 / 系統決策嚴格中性,≤ 3 選項
- **不擅自落地主 MD patch** — Step 6 草稿 raise Wayne ack 後才動
- **不擅自跳到 commit / 不擅自 trigger session 2**(SESSION_1 §5.1 / §5.3)
- **教訓暫存到 commit 點才一併拍板**(不每輪散裝寫進 SYSADMIN_BRIEFING)
