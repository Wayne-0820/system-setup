# SESSION_HANDOFF_2026-04-30_v8

(蓋掉 v7,2026-04-30)

---

## 0. 蓋掉理由(v7 → v8)

v7 結束時跑了 5 大塊任務(Context7 / Wan 2.2 下載 / WanVideoWrapper / pip_overrides / Wan 2.2 Lightx2v T2V workflow + 煙測)+ 4 commit。

今日(2026-04-30)持續到尾段,跑 1 大塊 + 1 commit:

1. Wan 2.2 I2V 煙測補完(待辦 #8),14.17 min/段達標,/old/ rank64 LoRA 接 4-step + sageattn + fp8_scaled 環境正常出片
2. 副產出:診斷 SaveAnimatedWEBP 寫出 .webp 81 frame `duration=None` 是 VLC 不能播的根因(下輪 .mp4 改造的確切依據)
3. FFmpeg 裝機(`winget install Gyan.FFmpeg`,8.1-full)
4. 規則 10「速度 / VRAM / 品質異常先查社群實踐」落進 SYSADMIN_BRIEFING 規則段
5. 三條踩坑進 setup.md(#15 SaveAnimatedWEBP duration / #16 POST /free unload / #17 ffmpeg 沒裝)+ 新紀律段「ComfyUI 輸入圖落點」
6. workflows.md §11 I2V 煙測時間表 + 標準輸入紀律落地
7. conflicts-wanvideowrapper.md 補 I2V mode patch 流程(8 變動表)
8. decisions.md winget 清單擴充 Gyan.FFmpeg

v8 蓋 v7 是因為 #8 從「待辦」變「✅ 完成」+ 新增 #10/#11 待辦 + 新規則進規則段,繼續疊在 v7 上會掩蓋當前狀態。

---

## 1. Git 狀態

本 v8 隨「Wan 2.2 I2V 煙測收尾 + 規則 10 + handoff v8」commit 一同 push,push 後 working tree 乾淨。

最近 commits(含本批):

```
docs(workflows+sysadmin): Wan 2.2 I2V 煙測收尾 + 規則 10 + handoff v8  ← 本批
a083215 docs(comfyui): Wan 2.2 Lightx2v 4-step workflow 落地(#3c)
59fd41a docs: 補入 controlnet-aux / alekpet 衝突明細 + FLUX pose workflow + workflow_submit
fae35d6 docs(comfyui): Wan 2.2 A14B 下載完成 + WanVideoWrapper 安裝
```

---

## 2. 中國 workflow 重建路線

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成(04-26)|
| 2 | Flux-fill OneReward 萬物移除 | ✅ 完成(04-29)|
| 3a | Kontext + ControlNet 改姿態 | ❌ Deprecated(04-29)|
| 3a-v2 | Qwen Edit 2509 改姿態保留人物 | ✅ 完成(04-29)|
| 3b | FLUX + ControlNet 純 pose 生人物 | ✅ 完成(04-29)|
| 3c | Wan 2.2 T2V/I2V 合一 720P/81幀 4 步 | ✅ T2V 12.91 min(04-30)+ I2V 14.17 min(04-30 達標)|
| 4 | Qwen3 TTS 聲音克隆 | 待辦 |
| 5-7 | (略) | 待辦 |

#3c 整體達標,但留下兩條尾巴:
- SaveAnimatedWEBP 出片不可播(待辦 #10 改造)
- /old/ rank64 I2V LoRA 跟 250928 新版 T2V 不對等(待辦 #9 待 upstream)

下一個 workflow 目標待 Wayne 拍板(進 #4 Qwen3 TTS / 先處理 #10 .mp4 改造收尾 #3c / 其他)。

---

## 3. 主視窗端待整合 patch 清單

無。

---

## 4. 待辦(從前期延續 + 今日新增)

| # | 待辦 | 觸發條件 | 狀態 |
|---|---|---|---|
| 1 | qwen3:14b 補下 | 視 agent 需求決定 | 待辦 |
| 2 | SageAttention issue #357 修復後重編 | 上游修好 | 待辦(blocked)|
| 3 | FLUX.1 Fill / Kontext / Qwen3 TTS / Whisper / Wan 2.2 系列下載 | Workflow #4 起需要 | 部分完成:Wan 2.2 + Lightx2v LoRA 已下;其他模型待 workflow 需要時再下 |
| 4 | CrewAI 第一條 agent pipeline | Workflow 重建告一段落 | 待辦 |
| 5 | LiteLLM 接入 NVIDIA NIM API | 想用 deepseek-v4 時 | 待辦 |
| 6 | 第一次 C 槽 baseline 映像 | 觸發條件詳見 `baseline-trigger.md` | 待辦 |
| 7 | Context7 安裝 | — | ✅ 完成(04-30)|
| 8 | Wan 2.2 I2V 煙測 | 用 human.png 煙測 I2V workflow | ✅ 完成(04-30,14.17 min 達標)|
| 9 | Kijai 釋出 I2V 250928+ 新版 LoRA 後更新 | upstream 釋出 | 待辦,blocked on upstream |
| 10 | Wan 2.2 #3c .mp4 改造 | SaveAnimatedWEBP → SaveVideo / VHS 任一條;雙檔分離 vs 維持合一拍板;`patch_workflow_to_i2v.py`(目前 D:\tmp\)是否進 tools/ 拍板 | 新增(04-30),前置 FFmpeg 已裝 |
| 11 | 用真實 I2V 輸入圖測動畫品質 | human.png 跑通後想驗 Wan 2.2 真實題材表現 | 新增(04-30)|

主視窗紀律:到 commit 點主動催 Wayne + 草擬 commit message + 派工 Claude Code 執行(規則 11 / project-level CLAUDE.md)。

---

## 5. Wayne 工作風格觀察(累積 + 今日強化)

延續 v7 觀察 + 今日新增:

- **規則 vs 教訓 vs 踩坑紀錄,Wayne 分得清楚**。今日把規則 10 候選混進「教訓暫存表」被罵 — Wayne 從對話開頭就講「速度異常先查社群實踐要不要進規則段」,我一直在「等 progress report 整合再拍板」拖時機。**規則性條目該即時 raise 進規則段拍板,不等其他事整合**。

- **派工拍腦袋寫具體值是高風險**。今日兩起實證:
  1. 派工寫 `example.png`,實機是 `example_inputs/{human,env,thing}.png` 三選一,執行端 STOP 上報攤選項
  2. 派工寫 `CRF 18`,實機 comfy-core SaveVideo 鎖 CRF 23,執行端 inspect 後攤「滿足 CRF 18 vs 立即可動」三選項給 Wayne

  共通根因:**主視窗手上沒實機資訊就寫死具體值**。正確做法:寫死前 verify 機器真相,verify 不到就寫「pack 自帶測試圖任一張(場景優先)」/「採用工具預設值」這種留判斷給執行端的措辭。

  規則候選但 Wayne 本輪沒拍板進規則段(本人話「規則 10」不含其他)。本條留在 §5 風格觀察累積,下次有第三起實證再 raise。

- **Wayne 對「token 浪費」感受強烈,試錯路線是真實 token 成本**(沿用 v7)。

- **Wayne 對「拍腦袋的建議」零容忍**(沿用 v7)。

---

## 6. 接班開場 SOP

新主視窗開場時,Wayne 會貼 SYSADMIN_BRIEFING + 本 handoff。讀完後:

1. 不要在第二段就跳結論。等 Wayne 給任務再分析
2. 指控 handoff / SYSADMIN_BRIEFING / 既有 MD 有 bug 前先 grep verify(規則 8)
3. STOP 上報攤選項時刻意不推或弱推單一答案(規則 9 / 規則 10 對齊 — 異常數字先查社群實踐)
4. 派工用 `ASSIGNMENT_TEMPLATE.md` 格式,寫目標 + 決策已定 + 限制 + 完成判定
5. 派工指具體檔名 / 路徑 / 參數值前先 verify 機器真相;verify 不到寫「留判斷給執行端」措辭(本輪 §5 觀察累積,規則候選未進規則段)

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
| WanVideoWrapper per-pack | `D:\Work\system-setup\comfyui\conflicts-wanvideowrapper.md` |
| 模型分工 | `D:\Work\system-setup\ai-models\local-models.md` |
| Progress reports(過渡)| `D:\Work\system-setup\progress-reports\` |

---

## 8. Session 結束時 repo 的乾淨指標

- [x] working tree 沒有未追蹤的「主視窗 / 執行端對話副產物」
- [x] `progress-reports/` 下 `2026-04-30_wan22-i2v-smoke-test.md` 已整合進對應 MD,執行端刪檔
- [x] 規則段條目跟對應實證一致(規則 10 + Wan 2.2 sdpa 試錯失誤實證)
- [x] 任何「待整合 patch」清單(§3)為空

全部達成。

---

**本快照建立日期**:2026-04-30(v8)
**蓋掉**:v7(2026-04-30)

**v8 更新理由**:今日尾段跑 I2V 煙測收尾 + .webp 體質診斷 + FFmpeg 裝機 + 規則 10 落地 + 三條踩坑 + ComfyUI 輸入圖落點紀律段 + I2V mode patch 流程紀錄,#8 從待辦變 ✅ + 新增 #10/#11 待辦,繼續疊在 v7 上會掩蓋當前狀態。v8 的核心區別是規則 10 已進規則段(v7 的「累積待拍」狀態結案),§5 累積一條新觀察「派工拍腦袋寫具體值是高風險」(規則候選但本輪未拍板進規則段)。