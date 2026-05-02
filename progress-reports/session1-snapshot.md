# session1-snapshot(2026-05-02)

> **你是 session 1 主視窗**(雙 session 架構,規劃 + 派工 + 整合 progress report,不執行)。
> Wayne 只貼本 handoff,讀完即可工作。
> 詳細角色 / IPC 流程查 `SESSION_1_MAINWINDOW.md`(需要時才讀)。
> 系統現況 / 規則段查 `SYSADMIN_BRIEFING.md`(需要時才讀)。

(蓋掉 v8,2026-05-02)

詳情查 `progress-reports/` 跟對應 MD,本 handoff 只給接班 anchor + 等什麼 + 紀律提醒。

---

## 當前 anchor

**Wan 2.2 #3c root cause 卡 (ε-2),等 Wayne 拍候選 11 解讀**:

(ε-1)(ε-2) 確認 Wayne 合一檔 `attention_mode = "sageattn"` 走 shim → PyTorch SDPA,不是 `sageattn_3` 走 sm_120 fp4 kernel。

- 解讀 A:Wayne 期待走 fp4 kernel,設定錯,改 `sageattn_3` 試
- 解讀 B:Wayne 故意選 sageattn 避開 sage3 #357 bug,候選 11 是「事實澄清」不是 mismatch

無法純從 workflow JSON 判,需 Wayne 拍板期待是哪條。詳情 `progress-reports\2026-05-02_wan22-epsilon1-2-workflow-json-audit.md`。

---

## 雙 session 架構已落地(2026-05-02)

3 新檔 + `.gitignore` patch 在 working tree(`SESSION_1_MAINWINDOW.md` / `SESSION_2_EXECUTOR.md` / `assignments/README.md`),session 1 寫派工 → `assignments/` / session 2 寫 progress report → `progress-reports/`,Wayne 中介 IPC。

詳情 `progress-reports\2026-05-01_session-arch-落地.md`。

---

## 等 Wayne 拍板(4 條)

1. **候選 11 解讀 A vs B**(見當前 anchor)
2. **lane A 雙 session 架構獨立 commit?**(中性傾向 A;不獨立就被 Wan 2.2 root cause 拖)
3. **`progress-reports/progress-reports-README.md` 命名 mismatch**(A: rename 對齊白名單 / B: 改白名單對齊檔名 / C: 不動;中性傾向 A)
4. **派工日期跨日 mismatch 處理**(session arch 落地 + (ε-1)(ε-2) 兩次踩到;A: 接受混用 / B: 統一 rename 對齊實機 / C: 派工模板改寫成「執行當天」相對描述;中性傾向 B+C 並用)

---

## Working tree(2 lane)

```
lane A 雙 session 架構落地(可獨立成批):
  M .gitignore
  ?? SESSION_1_MAINWINDOW.md
  ?? SESSION_2_EXECUTOR.md
  ?? assignments/README.md
  ?? progress-reports/session1-snapshot.md  ← 本 anchor(白名單後可進 git tracking)

lane B Wan 2.2 #3c 改造(等 root cause 釘死後一批):
  ?? comfyui-workflows/Wan2.2_A14B_T2V_720P_81幀_4步.json   (.mp4 跑通)
  ?? comfyui-workflows/Wan2.2_A14B_I2V_720P_81幀_4步.json   (SaveAnimatedWEBP 版,filename_prefix Wan2.2_I2V_retry_b1a)
```

註:5/1 brief 寫的 `M` 合一檔已不在 git status,(γ-1) Step 0 (A) verify 過合一檔嚴格對齊 (β-1a) 紀錄沒被改動。

---

## Wan 2.2 #3c root cause 8 輪結論摘要

跨輪 HIGH s1:`180s baseline → 210s (α-0) → 784s (α-1) → ≥1380s (β-1a) → [reboot] → 403s (γ-1)`

候選收斂:
- **證偽**:1(連跑 fragmentation)/ 2(SaveVideo+CreateVideo)/ 5(Manager fetch)/ 8(4/30→5/1 升級)
- **弱-中(下修)**:6(ComfyUI v0.3.75+ regression)/ 7(OS reboot 才解)
- **重大轉折(δ-2)**:#11568 reporter 自己重解讀為 reporting issue 不是 true regression / #11775 closed by reporter 自己沒 maintainer commit;原依賴的「強證據」需 downgrade
- **新候選**:10(dynamic VRAM × Wan 2.2 swap,中)/ 11(attention_mode 命中,意涵待拍)/ 12(workflow pinned,N/A 移除)

8 輪 progress report 路徑:`progress-reports\2026-04-30_wan22-mp4-conversion-and-split.md` + `2026-05-01_wan22-{retry-fragmentation,retry-savechain,degradation-research,gamma1-os-reboot,delta1-version-diff,delta2-code-audit}-*.md` + `2026-05-02_wan22-epsilon1-2-workflow-json-audit.md`

剩下 verify 路線候選(等 Wayne 拍 11 解讀後決定):
- (ε-1a) 候選 11A:改 `sageattn_3` 跑煙測(中成本,sage3 #357 bug 風險)
- (ε-3) 候選 10:`--disable-dynamic-vram` 跑煙測(中成本,低風險)
- (ε-4) 候選 6:升 ComfyUI master HEAD(高成本,高風險,前一輪傾向擱置)
- (ε-5) 候選 9:NVIDIA Nsight ETW trace 抓 nvlddmkm 153(高成本,設定複雜)

---

## 旁支 / 待整合(等 Wayne 拍板)

- **LTX-2.3 verify**(4/30):Wayne 收到的 6 條訊息全錯或部分錯,Blackwell 5090 三條 open issue → LTX-2.3 暫不上路。待整合進待辦 / `ai-models/local-models.md`。詳情 `progress-reports\2026-04-30_ltx23-verify.md`
- **教訓暫存累積 ≥18 條**:Wan 2.2 root cause 調查 + 雙 session 架構落地踩到的踩坑,候選落點 SYSADMIN_BRIEFING 規則段 / setup.md / ASSIGNMENT_TEMPLATE / 雙 session SOP。等 commit 點一併拍板進規則段
- **`comfyui/setup.md` 新踩坑批量待加**:詳情各 progress report §5「對 system-setup 文件的影響」段

---

## 接班開場 SOP

Wayne 只貼本 handoff。讀完拿到當前 anchor + 等什麼。

需要更深資訊時:
- 角色 / IPC 流程細節 → `SESSION_1_MAINWINDOW.md`
- 規則段 / 系統現況 → `SYSADMIN_BRIEFING.md`
- Wan 2.2 8 輪細節 → `progress-reports\` 對應檔(本檔 §「Wan 2.2 結論摘要」末段路徑)
- 對應任務 progress report → Wayne 貼來時讀

工作紀律:

1. 不在第二段就跳結論,等 Wayne 給任務再分析
2. 指控既有 MD 有 bug 前先 grep verify(規則 8)
3. STOP 上報攤選項時不推或弱推單一答案(規則 9)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 落地 `assignments/`,告訴 Wayne 切去 session 2 跑
5. 不主動 git commit / push,交給 session 2

---

## 關鍵紀律提醒(最近踩到的)

1. **依賴單一 GitHub issue 做強推論前讀完整 thread**(實證 (δ-2) #11568 / #11775 reporter 自己重解讀)
2. **派工日期寫「執行當天」相對描述,不寫死**(實證 session arch 落地 + (ε-1)(ε-2) 兩次踩到)
3. **subagent web_fetch heavy 派工邊界拉到 4 小時以上**(實證 (δ-2) 跑 10.25 小時)
4. **規則 10 升級版「subagent 並行查訊息」三次落地成功**((γ-0) 6 sub / (δ-1) 4 sub / (δ-2) 3 sub),範本強制 + 規則 9 中性穿透 + 硬限制清單(read-only audit / web_fetch 範圍)有效

---

**蓋掉**:v8(2026-04-30)
**v9 更新理由**:#3c 從「達標」轉「卡 (ε-2) 等候選 11 解讀」+ 雙 session 架構落地 + 8 輪 root cause 調查 + ≥18 條教訓暫存
