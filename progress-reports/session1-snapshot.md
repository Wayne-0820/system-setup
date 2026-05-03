# session1-snapshot(2026-05-03)

> **你是 session 1 主視窗**(雙 session + subagent 三角色架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v9,2026-05-03)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 當前 anchor

**Wan 2.2 #3c 8 輪 root cause 釘死 + native I2V 落地**:

- **wrapper 是性能瓶頸**(實證 corroboration setup.md 踩坑 #18 ε 系列 finding 2「WanVideoWrapper sampler 0 個 `mm.load_models_gpu` 呼叫,完全脫離主框架」)
- **native 路線快 3.84×**:HIGH s1 = 99.87s(wrapper baseline 180s,1.80× faster);total 221.21s(wrapper baseline 850s,3.84× faster)
- **(A) strict 條件全達標**(候選 B 煙測 + ws monitor per-step verify)
- **路線 (b) 雙路線並存已落地**:T2V split wrapper(`Wan2.2_A14B_T2V_720P_81幀_4步.json`)+ I2V native(`Wan2.2_A14B_I2V_720P_81幀_4步.json`,Comfy-Org subgraph)
- **過時檔已刪**:合一檔 / wrapper split I2V / `build_wan22_workflow.py`

---

## 架構演進(2026-05-03)

**雙 session + subagent 三角色**:

- session 1 主視窗(規劃 / 派工 / 整合)
- session 2 執行端(實機跑派工)
- **rule-curator subagent**(規則精修員,by session 1 invoke)— `D:\Work\system-setup\.claude\agents\rule-curator.md`

詳情:`SESSION_1_MAINWINDOW.md` §5.4 + `SYSADMIN_BRIEFING.md` 規則 9「主視窗 invoke subagent 場景」段。

---

## 規則演進(2026-05-03)

1. **規則 8 訂正**(C 改架構後弱化 → **evergreen**):派工撰寫前 grep verify 引用準確性 — 規則 / 踩坑編號 / 檔位置 / candidate JSON 結構三類
2. **規則 9 訂正**(刻意不推/弱推 → **工程選擇 vs 系統決策二分**):
   - 工程選擇:主動駁回顯然次優 + 弱推/強推可接受, **選項數 ≤3 給 Wayne**(2 是常態,3 是邊界)
   - 系統決策:嚴格中性攤 ≤3 候選,不推
3. **補規則 11-14**:
   - 11:派工 §STOP 觸發點排除執行端可自處(啟 server / poll / retry 等不寫 STOP)
   - 12:派工 §決策已定 鬆綁範圍三分(strict 核心對照變數 / 鬆綁 supporting model / 鬆綁 I/O widget)
   - 13:數值門檻明標 GB / GiB(邊界附近強制標明,默認 GB decimal)
   - 14:§限制 SHA256 校驗清單 mirror candidate JSON 全 dropdown widget(不只「主模型 + LoRA」直觀)
4. **commit 紀律永久訂正**:**push 前不 STOP**(Wayne 事前 ack commit 派工的拆批 + message 草稿即實質過目;SESSION_1 §5.3 + SESSION_2 §4.6 / §5.3 對應)

詳情 `SYSADMIN_BRIEFING.md` 規則 1-14。

---

## 工具演進(2026-05-03)

`tools/workflow_submit.py` 從「flat workflow only 實驗版」升級為**穩定版**:

- ComfyUI 0.19+ subgraph 自動 unfold(`unfold_subgraphs()`)
- Schema-based to_api(走 backend `/object_info` INPUT_TYPES + `_is_widget_type` 含 COMBO)
- `--validate-only` flag(POST 拿 prompt_id 立退)
- `--ws-monitor` opt-in flag(RFC 6455 stdlib client + monitor_ws() per-node + per-step timing)
- 純 stdlib(無新外部依賴)
- `FRONTEND_ONLY_TYPES` 過濾(Note / MarkdownNote / Reroute / PrimitiveNode 跳過)

詳情 `tools/README.md` workflow_submit.py 條目 + 檔名變動史。

---

## 等 Wayne 拍板(剩 1-2 條)

1. **派工日期跨日 mismatch 處理**(既有等拍項目,本對話沒拍延後)
   - A: 接受混用 / B: 統一 rename 對齊實機 / C: 派工模板改寫成「執行當天」相對描述
   - 中性傾向 B+C 並用
2. **(可選)雙 session 架構 ROI 評估**(本對話累積 5+ lane 經驗,可拍時機)

---

## Working tree

預期本對話 commit 後 clean(對齊 commit `fbfc814` + 本對話 commit 拆批 8 檔):

```
本對話 commit 涵蓋(8 檔):
  A .claude/agents/rule-curator.md
  M .gitignore
  M SYSADMIN_BRIEFING.md
  M SESSION_1_MAINWINDOW.md
  M SESSION_2_EXECUTOR.md
  M tools/README.md
  M tools/workflow_submit.py
  M progress-reports/session1-snapshot.md  ← 本檔(v10 蓋 v9)
```

---

## Wan 2.2 #3c root cause 結論(8 輪 + ε 系列 + native verify)

跨輪 HIGH s1:`180s baseline → 210s (α-0) → 784s (α-1) → ≥1380s (β-1a) → [reboot] → 403s (γ-1) → ε 系列收尾 → candidate B native: 99.87s ✓`

候選最終結論:

- **(A) 路線實證落地**:wrapper 是 root cause,native 路線快 3.84×
- 候選 11 (attention_mode 解讀):**irrelevant**(wrapper 框架本身才是 root cause,attention_mode 是次因)
- 候選 10 (--disable-dynamic-vram) / 6 (升 ComfyUI master) / 9 (Nsight ETW trace):**N/A**(root cause 已釘死,不必驗)

8 輪 progress report 已整合進:
- `comfyui/setup.md` 踩坑 #18 ε 系列(含 (A) 路線實證)
- `comfyui/setup.md` 踩坑 #19(supporting model state_dict cross-verify)
- `comfyui/setup.md` Wan 2.2 distribution map(Kijai vs Comfy-Org)

---

## 旁支 / 待整合

- **教訓暫存清算**:本對話累積 ≥29 條,已落地 ~27 條(規則 11-14 / §4 三分 / 規則 12 cross-verify / setup.md 踩坑 #19 / Comfy-Org 5 新檔清單 / Wan 2.2 distribution map / commit 紀律訂正)。**剩 ~2 條未落地**:派工日期跨日 mismatch / 雙 session ROI 評估
- **LTX-2.3 verify**(2026-04-30):Wayne 收到的 6 條訊息全錯或部分錯,Blackwell 5090 三條 open issue → 暫不上路。仍待整合進 `ai-models/local-models.md`(本對話未處理)

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

需要更深資訊時:

- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 / 系統現況 → `SYSADMIN_BRIEFING.md`
- subagent 機制 → `.claude/agents/rule-curator.md`(rule-curator definition)
- Wan 2.2 8 輪細節 → `comfyui/setup.md` 踩坑 #18 + #19
- 對應任務 progress report → Wayne 貼來時讀

工作紀律:

1. 不在第二段就跳結論,等 Wayne 給任務再分析
2. 指控既有 MD 有 bug 前先 grep verify(規則 8 evergreen)
3. STOP 上報攤候選時按規則 9 訂正版(工程選擇可弱/強推 + ≤3 選項;系統決策嚴格中性)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 落地 `assignments/`,告訴 Wayne 切去 session 2 跑
5. 不主動 git commit / push,交給 session 2(commit 紀律仍 source-of-truth)
6. invoke rule-curator subagent 場景見 `SESSION_1_MAINWINDOW.md` §5.4

---

## 關鍵紀律提醒(本對話新訂正)

1. **規則 8 evergreen**:派工撰寫前 grep verify 引用準確性(實證:本對話 §5 引用踩坑 #11 錯誤)
2. **規則 9 訂正版**:工程選擇可弱/強推 + ≤3 選項給 Wayne(實證:本對話 4 輪 STOP 每輪 4-5 候選堆給 Wayne,Wayne 嫌「跳這麼多給我選」)
3. **規則 11**:STOP 排除執行端可自處(實證:派工 §STOP 第 3 條 ComfyUI 啟動寫進 STOP 是錯,Wayne 嫌「派工的還想偷懶叫他啟動」)
4. **規則 12 (B) cross-verify**:supporting model state_dict key naming 跟檔名分離(實證:Kijai vs Comfy-Org meta tensor `NotImplementedError`)
5. **規則 13 GB / GiB**:邊界附近強制標明(實證:VRAM ≥22 GB decimal vs binary 解讀爭議)
6. **commit 紀律永久訂正**:push 前不 STOP(實證:Wayne 拍板,事前 ack 派工拆批 + message 草稿即實質過目)
7. **派工 candidate audit 含 JSON 結構**(規則 8 (C)):grep `definitions.subgraphs` 檢測 ComfyUI 0.19+ subgraph(實證:candidate B 派工撰寫盲點)
8. **§限制 SHA256 校驗清單 mirror 全 widget**(規則 14):不只直觀「主模型 + LoRA」(實證:candidate B 漏 CLIP / VAE / LoadImage 連續撞 STOP 三輪)

---

**蓋掉**:v9(2026-05-02)
**v10 更新理由**:Wan 2.2 #3c 8 輪結論釘死 + native I2V 落地 + rule-curator subagent 落地 + 規則 8/9 訂正 + 補規則 11-14 + commit 紀律永久訂正 + workflow_submit.py ws monitor 升級 + 教訓暫存清算
