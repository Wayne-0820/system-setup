# progress-reports/

> 本地執行端(Claude Code)的 progress report 暫存區。
> 整個目錄除本檔外 gitignored。

---

## 用途

派工給本地執行端的任務,跑完後 progress report(按 `../PROGRESS_TEMPLATE.md` 格式)寫到這個目錄,而非:

- 直接貼進對話框(對話拉太長,主窗口讀不便)
- 直接寫進對應 MD(報告未審還沒到該整合的階段)

---

## 檔名格式

`YYYY-MM-DD_<task-slug>.md`

例:

- `2026-04-28_litellm-nim-deepseek.md`
- `2026-05-02_was-node-suite-conflicts.md`

日期前綴讓同日多 report 不衝突 + 自然按時間排序(此處日期 = 實機執行當天,規則 15)。task-slug 用 kebab-case、短、描述性。

---

## 生命週期

```
執行窗口寫入 progress-reports/<file>.md
   ↓
Wayne 把 report 內容貼回主窗口
   ↓
主窗口整合進對應 MD
   (comfyui/setup.md / ai-models/local-models.md / comfyui/conflicts.md 等)
   ↓
Wayne commit 整合後的 MD
   ↓
Wayne 刪 progress-reports/<file>.md(已被分流,留著反而散)
```

---

## .gitignore 規則

```
progress-reports/*
!progress-reports/README.md
```

整個目錄不入 repo,本檔(`README.md`)是唯一例外,保留它讓 `git clone` 後目錄存在 + 未來主窗口讀得到「這目錄幹嘛的」。

---

## 不適用情境

- **遠端執行端(web Claude)**:沒檔案落地,progress report 直接貼對話框,不走這個目錄
- **多窗口主窗口接班 snapshot**(如 `SESSION_HANDOFF_*.md`):那是 sysadmin 跨 session 交接,不是任務完成回報,語意不同

---

## 相關文件

- `../PROGRESS_TEMPLATE.md` — report 內容格式範本
- `../SYSADMIN_BRIEFING.md` 「Sysadmin 慣例 / 教訓」段教訓 4 — 本目錄存在的決策脈絡
