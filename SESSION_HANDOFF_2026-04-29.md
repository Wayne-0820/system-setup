# SESSION_HANDOFF_2026-04-29_v6

(同日蓋 v5)

## 0. 蓋掉理由(v5 → v6)

v5 結束時 #3a-v2 (Qwen Edit) 完整收尾(workflow JSON 落地 + 煙測通過 + 跨檔 MD 整合 + progress report)+ 規則段重構初版完成(段名改「規則」+ 規則 8/9/10/11 寫入)+ 兩批 commit 已 push origin/main。

Wayne 啟動 B+C 重構(精簡規則 + 改架構成目標型派工)。本 v6 是 B+C 重構落地後的乾淨 handoff。

v6 蓋 v5 的核心變動:

1. **規則段精簡**:11 條 → 9 條(刪規則 9 / 規則 11 搬到 project-level CLAUDE.md / 規則 8 大幅縮減 / 規則 10 簡化 + Context7 細節搬走)+ 規則 1-7 heading 統一加「規則」prefix
2. **架構改變**:派工從「精準到 node level / patch 表 / REPL 指令」改成「目標型派工」(目標 / 決策已定 / 限制 / 參考文件 / 完成判定 / STOP 觸發 / 報告)
3. **新增 ASSIGNMENT_TEMPLATE.md**(派工模板範本,跟 PROGRESS_TEMPLATE.md 對仗)
4. **handoff 自身精簡**:從 v5 的 16.7 KB / 223 行縮減到約 5 KB(刪派工 v1 6 bug 揭露 / 訂正過程 / 雙端紀律補丁細節 — 這些已沉澱進規則段)

---

## 1. Git 狀態

`origin/main` vs working tree:

**已 commit + push**:批次 1(規則段重構初版)+ 批次 2(#3a-v2 Qwen Edit workflow 落地)。

**working tree 餘留**(批次 3,3c 決策不動,等下次主視窗 git diff 自己分主題拆):

```
M  tools/README.md
?? comfyui-workflows/FLUX_ControlNet_純pose生人物_20步.json
?? comfyui/conflicts-alekpet.md
?? comfyui/conflicts-controlnet-aux.md
?? tools/workflow_submit.py
```

**B+C 重構批次 4 待 commit**(本輪精簡落地後):
- SYSADMIN_BRIEFING.md(規則段精簡)
- CLAUDE.md(project-level,擴充 Context7 + commit 流程完整版)
- README.md(文件導航補 ASSIGNMENT_TEMPLATE)
- ASSIGNMENT_TEMPLATE.md(新檔)
- SESSION_HANDOFF_2026-04-29_v6.md(本檔,蓋 v5)

下個 commit 點:本批落地完成後,主視窗主動催 + 草擬 commit message(規則 11)。

---

## 2. 中國 workflow 重建路線

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成(04-26)|
| 2 | Flux-fill OneReward 萬物移除 | ✅ 完成(04-29)|
| ~~3a~~ | ~~Kontext + ControlNet 改姿態~~ | ❌ Deprecated(04-29)|
| 3a-v2 | Qwen Edit 2509 改姿態保留人物 | ✅ 完成(04-29)|
| 3b | FLUX + ControlNet 純 pose 生人物 | ✅ 完成(04-29)|
| 4 | (待定)| 待開始 |
| 5-7 | (略)| 待開始 |

下一個 workflow 目標待 Wayne 拍板。

---

## 3. 主視窗端待整合 patch 清單

無。

---

## 4. 待辦(從前期延續)

| # | 待辦 | 觸發條件 |
|---|---|---|
| 1 | qwen3:14b 補下 | 視 agent 需求決定 |
| 2 | SageAttention issue #357 修復後重編 | 上游修好 |
| 3 | FLUX.1 Fill / Kontext / Qwen3 TTS / Whisper / Wan 2.2 系列下載(~100-150 GB)| Workflow #4 起需要 |
| 4 | CrewAI 第一條 agent pipeline | Workflow 重建告一段落 |
| 5 | LiteLLM 接入 NVIDIA NIM API | 想用 deepseek-v4 時 |
| 6 | 第一次 C 槽 baseline 映像 | 觸發條件詳見 baseline-trigger.md |
| 7 | Context7 安裝 + 派工模板帶 `use context7` | 下次新派工 / 新對話開始前由主視窗指派 |

主視窗紀律:**到 commit 點主動催 Wayne** + 草擬 commit message + 派工 Claude Code 執行(規則 11)。

---

## 5. Wayne 工作風格觀察(累積)

- **直接、最少步驟、結果導向**。挑得出 Claude 的判斷錯誤,不被牽著走
- **不要管疲勞 / 休息**,他要停會自己停;勸休息他會不爽
- 切「執行端 vs 主視窗」邊界很清楚 — 主視窗字面瑕疵 Wayne 不替主視窗辯護,讓執行端 grep verify 後直接訂正
- 偏好委派實作給 Claude,自己當需求擁有者 + 驗收者
- 喜歡先聽選項 + 風險再做選擇
- 對「教訓」「拍」這類拗口字眼會直接挑出來;主視窗用語要直接 / 自然

---

## 6. 接班開場 SOP

新主視窗開場時,Wayne 會貼 SYSADMIN_BRIEFING + 本 handoff。讀完後:

1. **不要在第二段就跳結論**(例如「Qwen Edit 是主軸」這種主動推斷)。等 Wayne 給任務再分析
2. **指控 handoff / SYSADMIN_BRIEFING / 既有 MD 有 bug 前先 grep verify**(規則 8 擴充)。本輪曾發生主視窗錯指控 handoff 路徑 bug,grep 後 0 處錯誤路徑 — 直接照字面改會誤改正確檔
3. **STOP 上報攤選項時刻意不推或弱推單一答案**(規則 10)— 給主視窗獨立拍板空間
4. **派工用 ASSIGNMENT_TEMPLATE.md 格式**,寫目標 + 決策已定 + 限制 + 完成判定,不寫精準 patch 指令(C 改架構紀律)

---

## 7. 連結速查

| 檔 | 本地路徑 |
|---|---|
| 主視窗接班簡報 | `D:\Work\system-setup\SYSADMIN_BRIEFING.md` |
| 執行端 onboarding | `D:\Work\system-setup\START_HERE.md` |
| 派工模板 | `D:\Work\system-setup\ASSIGNMENT_TEMPLATE.md` |
| 進度報告模板 | `D:\Work\system-setup\PROGRESS_TEMPLATE.md` |
| project-level Claude 紀律 | `D:\Work\system-setup\CLAUDE.md` |
| user-level Claude 紀律 | `C:\Users\Wayne\.claude\CLAUDE.md` |
| ComfyUI 設定 | `D:\Work\system-setup\comfyui\setup.md` |
| Workflow 紀錄 | `D:\Work\system-setup\comfyui\workflows.md` |
| Custom node 衝突主索引 | `D:\Work\system-setup\comfyui\conflicts.md` |
| 模型分工 | `D:\Work\system-setup\ai-models\local-models.md` |
| Progress reports(過渡)| `D:\Work\system-setup\progress-reports\` |

---

## 8. Session 結束時 repo 的乾淨指標

- [ ] working tree 沒有未追蹤的「主視窗 / 執行端對話副產物」
- [ ] progress-reports/ 下的 report 已整合進對應 MD,Wayne 刪檔
- [ ] 規則段條目跟對應實證一致(規則新增時要附實證)
- [ ] 任何「待整合 patch」清單(§3)為空,或明確標出阻塞原因

任一不成立 → 跟 Wayne 釐清。

---

**本快照建立日期**:2026-04-29(v6)
**蓋掉**:同日 v5(v1-v4 在 v3-v5 階段已蓋)
**v6 更新理由**:B+C 重構落地 — 規則段從 11 條精簡到 9 條 + 派工架構改成目標型 + 新增 ASSIGNMENT_TEMPLATE + handoff 自身精簡 75%。**v6 的核心區別是 handoff 從「事件記錄器」變回「狀態快照」**,踩坑細節沉澱進規則段,handoff 只記現況 + 待辦 + 接班 SOP。
