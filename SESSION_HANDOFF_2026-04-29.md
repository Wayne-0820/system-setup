# SESSION_HANDOFF_2026-04-29_v5

(同日蓋 v4 — v4 蓋 v3,v3 蓋 v1/v2)

## 0. 蓋掉理由(v4 → v5)

v4 結束時主窗口端待整合 patch 已清空,留 #3a-v2 verify + 派工模板給下個主窗口接力。**新主窗口接班後產出派工模板 v1**(2026-04-29,Verify by 主窗口已完成,Batch 1 三項全綠)。**派工執行端(Claude Code 獨立視窗,Wayne 自啟)收到派工 v1 後讀 workflow JSON 發現 4 項派工跟 JSON 衝突 STOP 上報**,主窗口拍板 C 方案 + 7 條跟進指示。本輪到目前 Step 1 安裝 + Step 2 下載進行中,Step 3-5 跟進 C 方案 patch。

v5 蓋 v4 的核心變動:
1. **派工模板 v1 落地 + 6 項 bug 揭露 + 主窗口拍板 C(主答 + dry-run 後續)** — Wayne 派工流程踩到首次「派工 vs 機器真相不一致」系統性案例;教訓 8 / 9 已寫進 SYSADMIN_BRIEFING(本輪 Step 5 落地)
2. **路徑認知 bug 訂正** — 主窗口拍板訊息說「修 handoff §1 / SYSADMIN_BRIEFING 內 ComfyUI portable 路徑(handoff bug)」,執行端 grep verify 後**確認 handoff 0 處 / SYSADMIN_BRIEFING 3 處全部正確路徑 / repo 全文 0 處錯誤路徑形式 — 「handoff bug」是主窗口記憶錯誤,錯誤路徑只存在於派工模板 v1 本身**
3. **#3a-v2 派工執行進入 Step 1-2** — v4 的「Qwen Edit verify + 派工模板待產」狀態解除

---

## 1. Git 狀態(本輪 v5 中段時)

`origin/main` 跟 working tree 累積**多批未 commit 變更**(Wayne 自己決定何時 commit / 拆批)。**v3 + v4 + v5(進行中)累積的所有變更都還沒進 commit**。

**v3 / v4 累積**:詳 v4 handoff §1(若 v4 已蓋,從 git 還原)
- v3:sd→diffusion rename(yaml + 9 MD 22 處)/ 教訓 6-7 / commit-push 紀律 / Workflow #2
- v4:#3 派工 / #3a 抽掉 / #3b 完成 / 2 新 pack(controlnet_aux + alekpet) / 3 新模型 / 8 件 patch by Claude Code

**v5 階段累積**(本輪到目前):
- 派工模板 v1 收到(Wayne 上傳,主窗口寫,涵蓋 #3a-v2 5 step)
- 執行端 STOP 上報 4 項 bug(§2.1 詳述)
- 主窗口拍板 C 方案 + 7 條跟進指示(§2.2 詳述)
- 路徑認知 bug verify 完成(repo 全文無錯誤路徑,§2.3)
- node 35 Text Multiline verify 完成(§2.4),等主窗口拍替代節點
- Step 1 進行中(裝前 baseline 已抓 1.86 MB,clone Comfyui-QwenEditUtils 待 fire)
- Step 2 進行中(text_encoders + loras/qwen-image dir 已 mkdir,5 個下載 jobs 待 fire)

**累積總量**:約 30+ 檔變更,Wayne 未來決定 commit 批次。本輪 v5 跑通後預期再 +6-7 檔(本地化 JSON / setup.md / workflows.md / conflicts.md / conflicts-qweneditutils.md / local-models.md / progress report)+ SYSADMIN_BRIEFING 教訓 8 / 9。

---

## 2. v4 → v5 差別(快速 catch-up)

### 2.1 派工模板 v1 4 項衝突

| # | 衝突 | 派工字面 vs JSON 實際 |
|---|---|---|
| 1 | ComfyUI portable 路徑 | 派工 line 50 / 56 / 151 / 173 寫 `D:\Work\ComfyUI_portable\ComfyUI\` 缺一層 — 實機是 `...\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\`(setup.md / SYSADMIN_BRIEFING 既寫對) |
| 2 | 三節點預設 mode=4(bypass) | 派工 line 13 「Lightning 8 步 + Consistence Edit v2 + lrzjason」要全啟用,但 JSON node 4(Lightning LoRA)/ 34(consistence_edit)/ 44(lrzjason)預設 mode=4 |
| 3 | KSampler positive 接內建非 lrzjason | KSampler (id=7) positive ← link 104 = node 45 `TextEncodeQwenImageEditPlus`(comfy-core 內建),不是 node 44 lrzjason。預設 steps=20 cfg=2.5,**不是 Lightning 8 步路線** |
| 4 | node 35 `Text Multiline` 來自 was-node-suite-comfyui | conflicts.md 既有決策(2026-04-29)= **不裝**(archived)。workflow load 會 unknown node。沒登記過替代節點 |
| 5 | `tools\workflow_submit.py` dry-run 介面 + 紀律本身錯誤 | 派工 §4.1 line 174-177 寫 `--workflow` flag(實機 positional argument)+ `--validate-only` flag(實機不存在)+ dry-run 紀律本身在邏輯上**抓不到**要抓的(server validation 只在 POST 時跑,任何離線 dry-run 都跑不到 server 端 — 跟 v4 §2.6「server validation 不可 bypass」訂正內容矛盾)|
| 6 | `text_encoders/` 路徑 yaml 沒映射 | 派工 §2.1 line 85 寫檔下到 `D:\Models\diffusion\text_encoders\`,但實機 `extra_model_paths.yaml` 只映射 `clip: clip/`(setup.md line 39 既有規範),CLIPLoader dropdown 看不到下到 `text_encoders/` 的檔。執行端 Step 4 才揭露,自修 mv 到 `clip\` |

**派工系統性自相矛盾**:line 13(目標 = 雙 LoRA + lrzjason) vs line 159(KSampler 不動參數)字面合一 = 跑普通 Qwen Edit 內建 + 20 步,**派工三大關鍵元件全部沒生效**。bug 5 又跟 v4 §2.6 訂正自相矛盾。**6 項 bug 同根**:主窗口寫派工時沒對機器真相(實機 JSON / 實機工具介面 / 既有紀律 / yaml 配置)交叉 verify。

### 2.2 主窗口拍板 C 方案 + 7 條跟進指示

執行端 STOP 上報後給三選一(A 字面 / B 完整重接 link / C 折衷),主窗口拍板:

**C — unbypass 3 節點 + KSampler 改 8 步,不動 link**
- KSampler positive 仍走 node 45 內建 → 雙 LoRA 載入(影響 KSampler model)生效
- node 44 lrzjason enable 但下游沒被 KSampler 消費 → 浪費計算,輸出去 ConditioningZeroOut → 廢棄
- 8 步生效,雙 LoRA 生效,lrzjason 客製 prompt instruction 沒進 KSampler

7 條跟進指示:
1. 路徑錯誤 — 自修,順便修 handoff §1 / SYSADMIN_BRIEFING 內 ComfyUI portable 路徑(主窗口稱「handoff bug」,**執行端 grep verify 後確認認知錯誤,詳 §2.3**)
2. Step 1 先做(裝 Comfyui-QwenEditUtils + 衝突檢查)— 進行中
3. 同步 verify Text Multiline (node 35) outputs + widgets_values,回報主窗口拍板替代節點 — verify 完成(§2.4),等拍板
4. Step 2 下載開始(31.4 GB,並行於 verify)— 進行中
5. Step 3 JSON 本地化 — 用 C 方案 patch 表(取代派工 line 139-147),含 Text Multiline 替代(等拍)+ KSampler scheduler 選擇(verify Lightning 推薦值,自決)
6. Step 4 雙煙測:**改 C 方案(直接 POST /prompt,跳過 dry-run script)+ 風險緩解** — 派工 v1 line 173 dry-run 紀律本身錯誤(bug 5),A/B 兩種離線 dry-run 都抓不到 server validation 端。風險緩解:(1) REPL `to_api()` 0 成本 sanity check(import workflow_submit + json.load 不 POST,抓 KeyError / IndexError / hidden widget mismatch);(2) POST /prompt → 看 response 的 `node_errors`(非空 → server validation fail,STOP)/ `prompt_id`(有值 → pass + 進 queue,poll /history)
7. Step 5 progress report 必記:C 方案代價清單 / 派工 v1 自相矛盾教訓 / 主窗口攤選項自動推單一答案教訓 → SYSADMIN_BRIEFING 教訓 8 / 9

### 2.3 路徑認知 bug 訂正(handoff bug 不存在)

主窗口拍板訊息指控「handoff §1 / SYSADMIN_BRIEFING 內 ComfyUI portable 路徑(handoff bug)」。執行端 grep verify:

- `SESSION_HANDOFF_2026-04-29.md`(v4)全文 grep `ComfyUI_portable` → **0 match**
- `SYSADMIN_BRIEFING.md` grep `ComfyUI_portable` → **3 match,全部正確路徑**(line 96 / 144 / 277,均含 `ComfyUI_windows_portable`)
- system-setup repo 全文 grep `D:\Work\ComfyUI_portable\ComfyUI\` 或 `D:\Work\ComfyUI_portable\python_embeded\`(錯誤形式)→ **0 file match**

**結論:錯誤路徑只在派工模板 v1 本身**。handoff / SYSADMIN_BRIEFING / repo 都不需修。執行端不擅自改正確檔,改在派工自身 patch(本地化 JSON 用正確路徑,不動派工模板原稿)。

**這要進 SYSADMIN_BRIEFING 教訓段**:**主窗口指控 handoff bug 前先 grep verify**。本輪主窗口認為 handoff 有 bug 並指示執行端修,執行端 grep 後確認認知錯誤 — 主窗口若直接讓執行端修就會誤改正確檔。

### 2.4 node 35 Text Multiline verify 完成

- type:`Text Multiline`
- properties.cnr_id:`was-node-suite-comfyui`(版本 1cd8d304eda256c412b8589ce1f00be3c61cf9ec)
- inputs[0]:widget.name=`text`,type=`STRING`
- outputs[0]:name=`STRING`,type=`STRING`,links=[94, 111]
- widgets_values:`["让image1中的模特改变为image2的姿势，保持人物一致性，保持背景一致性。"]`(簡體中文)
- 下游:link 94 → node 44 lrzjason input 7 (prompt) / link 111 → node 45 內建 input 5 (prompt)

**等同**「STRING widget(multi-line text input)→ STRING output」單純文字節點,輸出送兩個 TextEncode 的 prompt input。

替代候選:
- a. ComfyUI 內建 string 類節點(待 verify comfy-core 有沒有獨立 STRING widget node)
- b. KJNodes 等價(`StringConstantMultiline` 或類似 — 待 baseline JSON verify)
- c. rgthree-comfy 等價(待 verify)
- d. 裝 was-node-suite-comfyui — **違反 conflicts.md 決策,不選**

主窗口待拍 a/b/c。

---

## 3. v4 階段內容(沿用,不重抄)

完整 v4 紀錄保留在 v4 handoff(若 v4 已蓋,從 git 還原)。本輪重要 v4 結論:#3a Kontext deprecated / #3b 完成 / #3a-v2 升 Qwen Edit 主軸 / Wayne 工作風格 4 條觀察。

---

## 4. 中國 workflow 重建路線(更新後)

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成(04-26)|
| 2 | Flux-fill OneReward 萬物移除 | ✅ 完成(04-29)|
| ~~3a~~ | ~~Kontext + ControlNet 改姿態~~ | ❌ Deprecated(04-29)|
| **3a-v2** | **Qwen Edit 2509 改姿態保留人物** | ⏳ **進行中**(派工 v1 → STOP → C 拍板 → Step 1-2 進行中)|
| 3b | FLUX + ControlNet 純 pose 生人物 | ✅ 完成(04-29)|
| 4-7 | (略,同 v4)| 待開始 |

---

## 5. ⚠️ 主窗口端「待整合 patch」清單

v4 結束時清空。**v5 階段新累積 3 件**:

1. **派工模板 v2 重寫**(主窗口端職責)— 修 v1 6 項 bug:
   - 路徑(全部加 `ComfyUI_windows_portable\` 一層)
   - 三節點預設 mode=4 警示 + C 方案 patch 步驟
   - KSampler positive link 接 node 45 內建非 node 44 lrzjason 的事實
   - node 35 Text Multiline 替代節點待 verify(本輪 Wayne 拍 a = `PrimitiveStringMultiline` comfy-core 內建)
   - `tools\workflow_submit.py` 介面 fix(positional path,無 `--workflow` flag,無 `--validate-only`)+ dry-run 紀律邏輯錯誤訂正(改 C 方案直接 POST + 風險緩解)
   - 模型路徑紀律:寫派工模型落地路徑前 grep `extra_model_paths.yaml` 確認規範(本輪 `text_encoders/` vs `clip:` yaml 沒映射,執行端自修 mv 到 clip\)
2. **SYSADMIN_BRIEFING 段名改「規則」+ 規則 8 / 9 / 10 / 11 全部落地**(本輪 Step 5 + follow-up):
   - 段名「Sysadmin 慣例 / 教訓」→「Sysadmin 慣例 / 規則」+ 段頂插入說明(規則 / 踩坑紀錄混合段);既有 1-7 條編號 / 內容 / 標題不動
   - 規則 8(派工模板 v1 系統性自相矛盾 + 位置指示紀律補強)— ✅ 已落地。要點:主窗口寫派工前要交叉驗證**五條**:widgets_values / mode / link / KSampler 路徑 / 引用工具的實機介面。本輪 6 項 bug 全部對應這五條(bug 6 「`text_encoders/` 路徑」是 widgets_values + 實機 yaml 規範驗證,屬第 1 條的擴充 — 寫派工模型路徑前要 grep `extra_model_paths.yaml`)。**段尾補強**:派工含「§N / 第 N 條 / X 段 / Y 段尾」這類具體位置指示時,主視窗派工前先 grep verify(讓 Wayne 貼檔 / 執行端 grep 回報 / GitHub raw URL),不靠記憶
   - 規則 9(主窗口攤選項時自動推單一答案)— ✅ 已落地。要點:STOP 上報攤選項時刻意不推或弱推,主窗口看到推單一答案時強迫自己看完所有選項才拍板
   - 規則 10(主視窗 / 執行端職責切割 + 外網查詢分工 + Context7 A 模式)— ✅ 已落地。要點:主視窗外網查詢為決策、執行端外網為任務 docs(Context7 A 模式手動 `use context7` 觸發);STOP 上報附主視窗外網查詢題目清單;Context7 安裝由主視窗在新對話開始前指派,不塞進進行中派工
   - 規則 11(Commit / push 流程)— ✅ 已落地。要點:取代原「Wayne 親自 commit / push」紀律;主視窗主動催 commit 點 + 草擬 commit message + 派工拆批,Claude Code 執行 git add / commit / push,push 前 grep `git status` 驗證
   - 教訓 9(主窗口攤選項時自動推單一答案)— 本輪 STOP 上報時執行端推 C 加多選項,結果讓主窗口決策容易順著推薦走;未來執行端 STOP 上報攤選項時要刻意不推或弱推,避免引導
3. **路徑認知 bug 訂正寫入主窗口接班測試題**(§9 新增測試題 16)

落地時機:本輪 Step 5 progress report 觸發,執行端產出後主窗口整合。

---

## 6. 還沒做的待辦(從前期延續 + v5 新增)

延續 v4 §6 1-10 條(略,同 v4)。

**v5 新增**:
| # | 待辦 | 觸發條件 |
|---|---|---|
| 11 | **#3a-v2 (Qwen Edit) Step 1-5 完成**(本輪)| 進行中 |
| 12 | **派工模板 v2 重寫**(修 v1 4 bug)| 本輪完成後 |
| 13 | **SYSADMIN_BRIEFING 教訓 8 + 9 落地** | 本輪 progress report 觸發 |

主窗口紀律:**到 commit 點主動催 Wayne** + 草擬 commit message + 派工 Claude Code 執行(規則 11)。

---

## 7. Wayne 工作風格(v5 新增觀察)

延續 04-28 + 04-29 v1-v4。

### v5 新增

- **Wayne 切「執行端 vs 主窗口」邊界很清楚**:本輪派工 v1 + 主窗口拍板 C 訊息 Wayne 當 messenger 貼給執行端,**主窗口字面瑕疵(handoff bug 認知錯誤)Wayne 不替主窗口辯護**,讓執行端 grep verify 後直接說「主窗口記錯了」。
- **Wayne 在執行端啟動下載前忘了更新 handoff**:本輪 Wayne 自承「我忘了更新 HANDOFF 給他」 — 主窗口寫派工 v1 時手上是過期 handoff(可能 v3 / v2),不是 v4。**handoff 流程既有缺口:Wayne 切換主窗口會話時要主動把最新 handoff 貼上,如果忘了主窗口會用舊版資訊寫派工**。本輪 Wayne 中段補上(本檔)。

---

## 8. 接班開場 SOP

跟前期一致,加新提醒:

- **不要在第二段就跳「Qwen Edit 是主軸」這種主動結論**(沿用 v4)
- **(v5 新)指控 handoff bug 前 grep verify**:本輪主窗口錯指控 handoff 路徑 bug,grep 後 0 處錯誤路徑。未來主窗口看派工 / handoff / repo 對不起來時,先 grep 各檔確認哪一份是錯的,**不要直接讓執行端改正確檔**
- **(v5 新)STOP 上報攤選項時刻意不推或弱推單一答案**:本輪執行端推 C 加多子問題,主窗口順著走。未來 STOP 上報時把選項擺平,推薦標「弱推薦」或不寫推薦,讓主窗口看完全貌再拍板(這條也是執行端紀律)

---

## 9. 接班測試題

承襲既有 15 題,**v5 新增第 16 題**:

**16. 主窗口拍板訊息中說「修 handoff §1 / SYSADMIN_BRIEFING 內 ComfyUI portable 路徑(handoff bug)」,執行端應該怎麼處理?**

預期答案:**先 grep verify**。本輪執行端 grep 後確認 handoff 0 處 / SYSADMIN_BRIEFING 3 處全部正確 / repo 全文 0 處錯誤路徑形式 — 「handoff bug」是主窗口記憶錯誤,錯誤路徑只在派工模板 v1 本身。**直接照主窗口字面去改 handoff / SYSADMIN_BRIEFING 會誤改正確檔**。執行端要把 verify 結果回報主窗口,讓主窗口修自己的派工模板而非 handoff。

---

## 10. Session 結束時 repo 的乾淨指標

延續 v4 §10,**v5 新增**:
- [ ] `comfyui-workflows\Qwen_Edit_2509_保留人物改姿勢_8步.json` 存在(本輪 Step 3 落地)
- [ ] `comfyui\conflicts-qweneditutils.md` 存在(本輪 Step 1 落地)
- [ ] 5 個 Qwen 模型 SHA256 全綠(本輪 Step 2 落地)
- [ ] `progress-reports\2026-04-29_Workflow_3a-v2_QwenEdit_smoke.md` 存在
- [ ] `SYSADMIN_BRIEFING.md` 規則段有 **11 條**(段名改「規則」+ 本輪 +4:規則 8、9、10、11)

任一不成立 → 跟 Wayne 釐清。

---

## 11. ~~Qwen Edit (#3a-v2) Verify 三項~~ — 過渡完成

v4 line 279 三項 verify 已被本輪 Batch 1(主窗口端 verify)+ 派工 v1 涵蓋。**v5 階段這段移除**(資訊已過時)。

---

## 12. 連結速查

延續 v4 §12,**v5 新增**:

| 檔 | 本地路徑 |
|---|---|
| **comfyui conflicts-qweneditutils**(v5 新)| `D:\Work\system-setup\comfyui\conflicts-qweneditutils.md` |
| **#3a-v2 workflow JSON**(v5 新)| `D:\Work\system-setup\comfyui-workflows\Qwen_Edit_2509_保留人物改姿勢_8步.json` |
| **派工模板 v1**(主窗口寫,Wayne 上傳)| `C:\Users\Wayne\Downloads\QwenEdit_3a-v2_派工模板_v1.md` |
| **原 workflow JSON**(網路源,Wayne 上傳簡體版)| `C:\Users\Wayne\Downloads\Pose姿势参考-千问Edit2509图像编辑.json` |

---

**本快照建立日期**:2026-04-29(v5)
**蓋掉**:同日 v4(v1/v2/v3 在 v3/v4 階段已蓋)
**v5 更新理由**:#3a-v2 派工模板 v1 落地 → 揭露 4 項 bug → STOP 上報 → 主窗口拍板 C → 路徑認知 bug 訂正 → Step 1-2 進行中。**v5 的核心區別是派工模板 v1 4 bug 揭露 + 主窗口端待整合 patch 從 0 件變回 3 件 + 兩條新教訓待落地 SYSADMIN_BRIEFING + 接班測試題 +1**。
