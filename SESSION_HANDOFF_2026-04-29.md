# Session 交接快照 — 給下一個主窗口 Claude

> **建立日期**:2026-04-29(v3,蓋掉同日 v2)
> **適用對話**:Wayne 接續本次 sysadmin session 後開新對話用
> **使用方式**:Claude Projects 已啟用,本檔在 project knowledge 中自動載入,新主窗口開新對話即讀
> **角色定位**:你是接班的主窗口 = sysadmin + 決策諮詢

---

## 1. 你接到的 repo 在什麼狀態

### 結構現況(2026-04-29 v3)

跟 04-28 結構一致 + `.claude/skills/`(04-29 v1 已加)+ `comfyui-workflows/Flux-fill_OneReward_萬物移除_10步.json`(v2 完成)+ 5 份 MD 整合 patch 全部入 working tree(v3 完成):

```
D:\Work\system-setup\
├── README.md
├── START_HERE.md
├── SYSADMIN_BRIEFING.md         ← 教訓 1-7(教訓 7 = bulk patch 多檔 line ending 紀律)
├── PROGRESS_TEMPLATE.md         ← v2 修使用說明 5-6 行(commit 紀律)
├── CLAUDE.md                    ← project-level
├── context.md                   ← 路徑 sd → diffusion 已同步
├── decisions.md                 ← 路徑 sd → diffusion 已同步
├── reinstall-manifest.md        ← 路徑 sd → diffusion 已同步
├── baseline-trigger.md
├── .claude\skills\
│   ├── log-lesson\SKILL.md
│   ├── progress-report\SKILL.md
│   └── raise-pitfall\SKILL.md
├── progress-reports\            ← gitignored 整體,README.md 例外
├── comfyui-workflows\
│   ├── (5 個既有 workflow JSON)
│   └── Flux-fill_OneReward_萬物移除_10步.json   ← v2 新增
├── comfyui\                     ← v3 整合完成(setup / workflows / conflicts / conflicts-kjnodes)
├── ai-models\                   ← v3 整合完成(local-models)
├── davinci\                     ← 路徑 sd → diffusion 已同步
├── ldbot\
├── openwebui\
└── tools\
```

**Wayne user-level CLAUDE.md** 在 `C:\Users\Wayne\.claude\CLAUDE.md`(不入 repo,跨所有 working directory 自動載入)。本輪硬規則 4 為「Commit / push 是 Wayne 的決策範疇」(v2 改寫)。

### Git 狀態(本輪 v3 結束時)

`origin/main` 跟 working tree 之間累積**多批未 commit 變更**(Wayne 自己決定何時 commit / 拆批)。本輪 04-29 整個 session 累積的所有變更都還沒進 commit:

- `D:\Models\sd\` → `D:\Models\diffusion\` rename(yaml + 9 MD,22 處引用)
- 教訓 6(grep pattern 完整性)+ huggingface-download-tricks.md 兩段 SOP append
- Commit / push 紀律改寫(user-level CLAUDE.md 硬規則 4 / PROGRESS_TEMPLATE 使用說明 / SYSADMIN_BRIEFING 主窗口職責第 6 條)
- Workflow #2 重建(comfyui-workflows/ 新增 1 檔;模型本身在 D:\Models\,不入 repo)
- **5 份 MD 整合 patch + 教訓 7**(comfyui/setup / workflows / conflicts / conflicts-kjnodes / ai-models/local-models / SYSADMIN_BRIEFING 教訓段)

**累積總量**:約 20+ 檔變更(去重),Wayne 拍板 commit 批次。

---

## 2. v2 → v3 的差別(本段給快速 catch-up 用)

v3 在 v2 基礎上完成兩件事:

### 2.1 5 份 MD 整合 patch 全部執行完畢

v2 列了「6 份待整合 patch」清單(其中 huggingface-download-tricks.md 後來確認不需 patch,變 5 份)。v3 完成執行:

| 檔 | 內容 |
|---|---|
| `comfyui/setup.md` | Diffusion 表 +1 / CLIP 表 +2 / VAE 表 +1 / **新增 LoRA 子段**(從無到有,+2 列) |
| `comfyui/workflows.md` | 索引新增「圖像編輯系列」表 / 新增 #8 workflow 詳述 / 待建表優先 2 ✅ |
| `comfyui/conflicts.md` | TL;DR 中風險 +1 / 新段「上游 archived pack 警示」 / 新段「替代節點對照」 / 解決決策表 +1 |
| `comfyui/conflicts-kjnodes.md` | 影響表更新 + 決策表 +1 |
| `ai-models/local-models.md` | 主力分工表 +1 |

雙驗證器全綠(BOM 6 檔 OK / line ending 4 LF + 2 CRLF 全保留 / 18 個 grep pattern 命中數對得上)。

### 2.2 教訓 7 沉澱完成(`bulk patch 多檔的 line ending 紀律`)

從「2026-04-29 commit 紀律 patch 任務 CC 踩到 LF/CRLF 不統一」沉澱進 SYSADMIN_BRIEFING 教訓段。**本任務(整合 patch)首次同步遵守教訓 7 自身紀律**(預先 LE 偵測 → 寫回保留 → 驗證),紀律落地閉環。

---

## 3. 本輪 session 完整脈絡(若你只想看 v3 變動跳第 2 段)

### 3.1 D 槽 Models 資料夾 rename:`sd\` → `diffusion\`

**動機**:Wayne 接班 audit 抓到「sd 命名是 SD WebUI 時代慣例,實際內容是 FLUX/Klein/SDXL/未來 Qwen Image」。

**執行**:同槽 rename(59.88 GB / 17 檔 / 9 子資料夾不動)+ yaml + 全 repo 22 處引用同步。煙測用 ComfyUI HTTP API `/object_info` 拉 dropdown(本輪首次驗證有效,寫進 huggingface-download-tricks.md 路徑慣例段)。

**踩坑沉澱為教訓 6**:bulk rename 派工的 grep pattern 必須涵蓋三類 — 絕對路徑全形式 / 末尾斜線雙形態 / 樹形圖獨立節點。

### 3.2 huggingface-download-tricks.md 兩段 SOP append

**「命名」段**:HF 通用 placeholder 檔名(`unet_fp8` / `diffusion_pytorch_model`)→ 必須加 repo 識別前綴改名。例外:HF 原檔名已含識別性 → 維持原檔名。

**「路徑慣例」段**:模型落地分類表 + LLM 類例外(寫死 `LLavacheckpoints`)+ HTTP API 驗證範例。

### 3.3 Commit / push 紀律核心改寫(三檔同步)

**動機**:Wayne 抓到執行端 progress report 的「待辦」段列「Wayne commit + push」當項目,等同把 Wayne 決策動作植入執行端流程,職責越界。

**改寫**:
- **user-level `CLAUDE.md` 硬規則 4** — 「Commit / push 是 Wayne 的決策範疇」+「不存在『自動 commit』例外」
- **PROGRESS_TEMPLATE.md 使用說明** — 5-6 行改成「由 Wayne 決定何時 commit + push」
- **SYSADMIN_BRIEFING.md 主窗口職責第 6 條** — 派工模板的「邊界」段不寫「Wayne 自己做 commit」這類引導語

**為何走核心紀律改寫不是教訓段**:這不是「踩坑後的紀律」,是「角色邊界本來就該這樣」,該直接改 CLAUDE.md 的核心條目。

### 3.4 Workflow #2「Flux-fill OneReward 萬物移除」完整重建

**主軸任務**。18 節點從 RunningHub 雲端版移植本地版。

**模型下載清單**(總 16.83 GB):

| 檔 | 來源 | 大小 | 備註 |
|---|---|---|---|
| `flux.1-fill-dev-OneReward-fp8.safetensors` | `yichengup/flux.1-fill-dev-OneReward` | 11.085 GB | placeholder 改名(原 `unet_fp8`) |
| `Flux-Turbo-Alpha.safetensors` | `alimama-creative/FLUX.1-Turbo-Alpha` | 0.646 GB | placeholder 改名(原 `diffusion_pytorch_model`) |
| `removal_timestep_alpha-2-1740.safetensors` | `lrzjason/ObjectRemovalFluxFill`(Wayne 預下) | 0.086 GB | 原檔名已有識別性,不改 |
| `clip_l.safetensors` | `comfyanonymous/flux_text_encoders` | 0.229 GB | 不改 |
| `t5xxl_fp8_e4m3fn.safetensors` | 同上 | 4.558 GB | 不改 |
| `ae.safetensors` | `Comfy-Org/z_image_turbo/split_files/vae/` | 0.312 GB | 不改 |

**JSON 本地化 5 處**:LoRA 名去中文後綴 / RH auth token 清空 / clipspace 路徑清空 / VAELoader 名 `ae.sft` → `ae.safetensors` / **#113 Mask Fill Holes 換成 KJNodes `GrowMaskWithBlur`**(等價替代,參數 `expand=0, blur_radius=0, fill_holes=True`)。

**為何不裝 was-node-suite-comfyui 而走替代節點路線**:該 pack 2025-06 已被作者 archived,為了 1 個節點裝整 archived pack 維護負擔不對等。KJNodes 已裝且有等價節點,優選。

**雙煙測通過**:
- HTTP API `/object_info`:6 個檔 + 17 個節點 type 全可達
- GUI 跑通:VRAM 高峰 **24,088 MB**(逼近 5090 Laptop 24 GB 物理上限)、生成時間 **93.68 秒 / 10 步**(這是 Wayne 第二次有畫 mask 的真實數據;首跑 84.08 秒沒畫 mask,**不採用**)
- 輸出檔:`D:\Media\AI_Raw\ComfyUI_Output\ComfyUI_00002_.png`(3.45 MB)

### 3.5 兩個 STOP 點處理(v2 階段)

**STOP 1**:Mask Fill Holes 節點不存在,候選 pack `was-node-suite-comfyui` 已 archived。Wayne 拍板走「找替代節點」路線,CC 找到 KJNodes `GrowMaskWithBlur` 等價(都用 `scipy.ndimage.binary_fill_holes`)。

**STOP 2**:派工指定的 ae.sft 來源 `Comfy-Org/flux1-dev` 沒 ae 單檔(只有 all-in-one 整合包)。Wayne 拍板走 `Comfy-Org/z_image_turbo/split_files/vae/ae.safetensors`(Comfy-Org 官方鏡像,非 gated)。

---

## 4. 中國 workflow 重建路線

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成(04-26) |
| 2 | **Flux-fill OneReward 萬物移除** | ✅ **完成(04-29)** |
| 3 | Kontext + ControlNet 姿態改變 | 待開始(下個主軸候選) |
| 4 | Qwen3 TTS 聲音克隆 | 待開始 |
| 5 | Qwen image 擴圖 | 待開始 |
| 6 | 智能多角度生成 | 待開始 |
| 7 | Qwen3 TTS 聲音設計 | 待開始 |

---

## 5. ⚠️ 主窗口端「待整合 patch」清單 — **本輪已清空**

v2 列的 6 份待整合 patch(後降為 5 份)**v3 全部執行完畢**。當前主窗口端**無累積待整合 patch**。

下次接班的主窗口接到任務時,從乾淨基線開始,不必處理本輪歷史包袱。

---

## 6. 還沒做的待辦(從前期延續)

| # | 待辦 | 觸發條件 |
|---|---|---|
| 1 | NIM 復服後重試 v4-flash chat completion | NIM upstream 復服 |
| 2 | 中國 workflow #3-#7 模型下載(~100-150 GB,不含已下的) | #2 完成後可開始 |
| 3 | CrewAI 第一條 agent pipeline | 1-2 個月後 |
| 4 | 第一次 C 槽 baseline 映像 | 觸發條件全達成才做 |
| 5 | SageAttention issue #357 修復後重編 | 上游修復通知 |
| 6 | Hasleo Rescue USB 6 個月驗證 | 約 2026-10 月底 |
| 7 | 繁中 TTS 避雷字典 | 第二集動工前 |

主窗口紀律:這些**記著但不主動催 Wayne 做**。Wayne 自己會決定何時做,他來問就提供選項 + 風險。

---

## 7. Wayne 工作風格(本輪累積觀察)

延續 04-28 + 04-29 v1/v2 的觀察。

### 細節

- **接班 audit 比想像中更主動**:Wayne 看到派工模板裡 `D:\Models\sd\` 才回頭問「sd 是不是 SD WebUI 命名」,**主窗口接班時就該抓到**。教訓 1 的「audit repo 結構合理性」要加一條子問題:**資料夾命名跟實際內容對齊嗎?**
- **Wayne 抓邏輯一致性極快**:本輪兩個強烈例子 — (a) 「commit/push 是 Wayne 決策範疇」直接點出主窗口 / 執行端的職責邊界沒寫清楚 (b) 教訓 9 候選(GUI 互動驗證標準)Wayne 直接拒絕(理由沒寫,但合理推測 — 不該為單次失誤沉澱成系統規則)
- **拍板極簡**:單字母 / 兩字組合(`A` / `B+B` / `A`)是 Wayne 標準回覆,不重複 context。主窗口收到要對照上文準確 parse
- **不為單次失誤沉澱規則**:本輪兩個觀察(派工 ae 來源錯誤 / 6.1 子串 grep / 6.2 雙 `---` 合併)Wayne 都沒拍板進教訓段,主窗口記在心裡就好。**過度沉澱會稀釋既有教訓的權重**。

### 容易誤解的點

- **「workflows IGNORE」≠ 「整個目錄 gitignore」**:Wayne 一句「我想讓 comfyui-workflows 裡面的 IGNORE,對結構有什麼影響?」我第一輪解讀成「整個目錄 gitignore」並寫了一大段論證為什麼不該做。Wayne 二輪補一句「裡面有簡體字,改繁體字」我才發現他是在問「個別檔內容處理的副作用」,**根本跟 gitignore 沒關係**。教訓:**Wayne 講話省略主詞時,先問「你說的 IGNORE 是指 git 還是 OpenCC 那種 ignore」**,不要直接往一個解讀深挖
- **「測試圖選擇」是建議不是要求**:Wayne 最終用藤椅照片(自選),主窗口建議的「鏤空椅子 / 戒指」沒被採用 — Wayne 會聽建議但用自己判斷選素材
- **「重測」是因為流程沒到位,不是結果有疑**:#2 workflow 第一次跑沒畫 mask 是因為**派工 Step 6b 沒寫「右鍵 MaskEditor 畫 mask」**這條使用前置。Wayne 收工時提「需要重測」,主窗口問清是 A(功能沒過)還是 B(數據污染),他選 B
- **Wayne 撤回過 OpenCC 派工**:「我想讓 comfyui-workflows 裡面的 IGNORE → 改繁體字」釐清後,主窗口給 Q1+Q2 派工準備產 OpenCC 派工模板,但 Wayne 後來決定「簡轉繁不做了」,**派工撤銷**。教訓 8 候選同步撤銷

---

## 8. 接班開場 SOP(不變動)

跟前期一致。要做的事:

1. Project knowledge 自動載入(SYSADMIN_BRIEFING + CLAUDE.md + 本 handoff + README + context)
2. 用你自己的話回 Wayne:
   - 你的角色(sysadmin + 決策諮詢)
   - repo 現況(本輪 #2 workflow 完成 + 整合 patch 全部清空)
   - 進行中脈絡(commit 待 Wayne 決定批次)
3. 等 Wayne 給任務,**不主動建議今天做什麼**

---

## 9. 接班測試題

承襲既有 12 題(04-28 + 04-29 v1 共 10 + v2 加 11/12)。本輪新增 1 題:

**13. 主窗口看到 CC progress report 觀察「`ae.safetensors` 是 `vae.safetensors` 子串造成 grep 命中 2 不是 1」,該不該沉澱進教訓段?**

預期答案:**不該**。這是技術細節層次(grep pattern 鎖定行首 / 反引號的寫法),只要主窗口寫派工模板時注意短檔名的 pattern 該加錨點就好,**不到教訓的層次**。教訓段過度沉澱會稀釋既有教訓權重(本輪已 7 條),Wayne 工作風格觀察「不為單次失誤沉澱規則」也支持這個判斷。

---

## 10. Session 結束時 repo 的乾淨指標

下一個 session 接班時應該確認以下都成立:

- [ ] `git status` 顯示有「多批未 commit 變更」(預期狀態 — Wayne 未 commit 完所有累積)
- [ ] `git log --oneline -10` 顯示截至 04-29 v1 的 commit 鏈(本輪 v2/v3 變更**還沒進 commit log**,除非 Wayne 在 v3 產出後 commit 了)
- [ ] `SYSADMIN_BRIEFING.md` 教訓段有 7 條(教訓 6 = grep pattern 完整性 / 教訓 7 = bulk patch 多檔 line ending 紀律)
- [ ] `SYSADMIN_BRIEFING.md` 主窗口職責段有 6 條(第 6 條 = 派工模板邊界段不寫 commit 引導語)
- [ ] `D:\Work\system-setup\CLAUDE.md` 是 v2.0(project-level)
- [ ] `C:\Users\Wayne\.claude\CLAUDE.md` 硬規則 4 標題是「Commit / push 是 Wayne 的決策範疇」
- [ ] `PROGRESS_TEMPLATE.md` 使用說明 5-6 行寫「由 Wayne 決定何時 commit」
- [ ] `D:\Models\diffusion\`(不是 `D:\Models\sd\`)存在,內 17 檔 / 59.88 GB / 9 子資料夾
- [ ] `extra_model_paths.yaml` `base_path` 指向 `D:\Models\diffusion\`
- [ ] `comfyui-workflows\Flux-fill_OneReward_萬物移除_10步.json` 存在
- [ ] `D:\Models\diffusion\diffusion_models\flux.1-fill-dev-OneReward-fp8.safetensors` 存在(11.085 GB)
- [ ] `D:\Models\diffusion\loras\` 含 `Flux-Turbo-Alpha.safetensors` + `removal_timestep_alpha-2-1740.safetensors`
- [ ] `D:\Models\diffusion\clip\` 含 `clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors`
- [ ] `D:\Models\diffusion\vae\ae.safetensors` 存在
- [ ] `comfyui/setup.md` 含 LoRA 子段(從無到有新增)
- [ ] `comfyui/workflows.md` 含「圖像編輯系列」段 + #8 workflow 詳述
- [ ] `comfyui/conflicts.md` 含「上游 archived pack 警示」+「替代節點對照」兩個新段
- [ ] `progress-reports\` 內**只有** README.md(本輪 5 份 report 已被 Wayne 整合 + 刪除)
- [ ] Claude Projects 設定:
  - knowledge 含本 handoff(`SESSION_HANDOFF_2026-04-29.md` v3)
  - knowledge **已移除舊版** v1 + v2
  - custom instructions 已貼

任一不成立 → 跟 Wayne 釐清。

**特別留意**:**主窗口端待整合 patch 已全部清空**。下次接班從乾淨基線開始,接到任務直接做新工作,不必先處理歷史包袱。

---

## 11. 連結速查

主要檔的本地絕對路徑:

| 檔 | 本地路徑 |
|---|---|
| SYSADMIN_BRIEFING | `D:\Work\system-setup\SYSADMIN_BRIEFING.md` |
| CLAUDE.md (project) | `D:\Work\system-setup\CLAUDE.md` |
| CLAUDE.md (user) | `C:\Users\Wayne\.claude\CLAUDE.md` |
| PROGRESS_TEMPLATE | `D:\Work\system-setup\PROGRESS_TEMPLATE.md` |
| comfyui setup | `D:\Work\system-setup\comfyui\setup.md` |
| comfyui workflows | `D:\Work\system-setup\comfyui\workflows.md` |
| comfyui conflicts | `D:\Work\system-setup\comfyui\conflicts.md` |
| comfyui conflicts-kjnodes | `D:\Work\system-setup\comfyui\conflicts-kjnodes.md` |
| huggingface tricks | `D:\Work\system-setup\comfyui\huggingface-download-tricks.md` |
| ai-models local-models | `D:\Work\system-setup\ai-models\local-models.md` |
| 新 workflow JSON | `D:\Work\system-setup\comfyui-workflows\Flux-fill_OneReward_萬物移除_10步.json` |
| skills 三份 | `D:\Work\system-setup\.claude\skills\<skill-name>\SKILL.md` |

GitHub raw URL **只在執行端不在 Wayne 機器上**(遠端 web Claude)時才用,本機 Claude Code 一律走絕對路徑(SYSADMIN_BRIEFING 教訓 3)。

---

**本快照建立日期**:2026-04-29(v3)
**蓋掉**:同日 v2(v1 在 v2 階段已蓋)
**v3 更新理由**:v2 列的 6 份待整合 patch(後降 5 份)在本輪 session 全部執行完畢 + 教訓 7 沉澱完成。v3 的核心區別是**第 5 段標明「待整合 patch 清單已清空」**,下次接班從乾淨基線開始,不再背歷史整合包袱。
