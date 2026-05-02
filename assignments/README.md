# assignments/ — session 1 派工落地目錄

## 用途

session 1(主視窗)寫派工給 session 2(執行端)讀的目錄。對齊 `progress-reports/` 設計。

## 生命週期

1. session 1 寫派工到 `assignments/<YYYY-MM-DD>_<task-slug>.md`
2. Wayne 通知 session 2「讀 assignments/<檔>」
3. session 2 跑派工 → 寫 progress report 到 `progress-reports/<YYYY-MM-DD>_<task-slug>.md`
4. Wayne 通知 session 1「讀 progress-reports/<檔>」
5. session 1 整合 progress report 進對應 MD,**派工檔可刪**(派工是過渡產物,內容會過 progress report 反映)

## 目錄狀態

`assignments/*` gitignored,**不入 commit**。`assignments/README.md`(本檔)例外保留,讓 `git clone` 後目錄存在。

## 命名規則

- 格式:`<YYYY-MM-DD>_<task-slug>.md`
- 日期前綴讓同日多派工不衝突且自然按時間排序
- task-slug:短、kebab-case、描述性
- 範例:
  - `2026-05-01_wan22-epsilon3-disable-dynamic-vram.md`
  - `2026-05-01_commit-wan22-mp4-conversion.md`
  - `2026-05-02_workflow-qwen3-tts-build.md`

## 關聯文件

- `SESSION_1_MAINWINDOW.md` — session 1 角色定義(含寫派工 SOP)
- `SESSION_2_EXECUTOR.md` — session 2 角色定義(含讀派工 SOP)
- `progress-reports/README.md` — 對應的另一端
- `ASSIGNMENT_TEMPLATE.md`(若有) — 派工模板格式

---

**最後更新**:2026-05-01
