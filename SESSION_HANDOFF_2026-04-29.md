# Session 交接快照 — 給下一個主窗口 Claude

> **建立日期**:2026-04-29(v2,蓋掉同日 v1)
> **適用對話**:Wayne 接續本次 sysadmin session 後開新對話用
> **使用方式**:Claude Projects 已啟用,本檔在 project knowledge 中自動載入,新主窗口開新對話即讀
> **角色定位**:你是接班的主窗口 = sysadmin + 決策諮詢

---

## 1. 你接到的 repo 在什麼狀態

### 結構現況(2026-04-29)

跟 04-28 結構一致 + `.claude/skills/`(04-29 v1 已加)+ 本輪新增 `comfyui-workflows/Flux-fill_OneReward_萬物移除_10步.json`:

```
D:\Work\system-setup\
├── README.md
├── START_HERE.md
├── SYSADMIN_BRIEFING.md         ← 教訓 1-6(本輪新增 6;教訓 7 暫存主窗口待整合)
├── PROGRESS_TEMPLATE.md         ← 本輪修使用說明 5-6 行(commit 紀律)
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
│   └── Flux-fill_OneReward_萬物移除_10步.json   ← 本輪新增
├── comfyui\                     ← 本輪有「待整合 patch」未進(見第 4 段)
├── ai-models\                   ← 本輪有「待整合 patch」未進
├── davinci\                     ← 路徑 sd → diffusion 已同步
├── ldbot\
├── openwebui\
└── tools\
```

**Wayne user-level CLAUDE.md** 在 `C:\Users\Wayne\.claude\CLAUDE.md`(不入 repo,跨所有 working directory 自動載入)。本輪改寫硬規則 4(commit 紀律)。

### Git 狀態(本輪結束時)

`origin/main` 跟 working tree 之間累積**多批未 commit 變更**(Wayne 自己決定何時 commit / 拆批)。最近 commit 鏈反映 04-28 + 04-29 v1 的內容。本輪 04-29 v2 涉及的所有變更**都還沒進 commit**:

- `D:\Models\sd\` → `D:\Models\diffusion\` rename(yaml + 9 MD,22 處引用)
- 教訓 6(grep pattern 完整性)+ huggingface-download-tricks.md 兩段 SOP append
- Commit / push 紀律改寫(user-level CLAUDE.md 硬規則 4 / PROGRESS_TEMPLATE 使用說明 / SYSADMIN_BRIEFING 主窗口職責第 6 條)
- Workflow #2 重建(comfyui-workflows/ 新增 1 檔;模型本身在 D:\Models\,不入 repo)
- **6 份待整合 patch(主窗口端尚未產,本檔第 4 段詳述)**

---

## 2. 本輪 session 完成的事 + 為什麼這樣設計

### 2.1 D 槽 Models 資料夾 rename:`sd\` → `diffusion\`

**動機**:Wayne 接班 audit 時抓到「sd 命名是 SD WebUI 時代慣例,實際內容是 FLUX/Klein/SDXL/未來 Qwen Image,語意不一致」。這是 SYSADMIN_BRIEFING 教訓 1「audit repo 結構合理性」的延伸應用 — 主窗口接班時應主動檢查資料夾命名是否反映實際內容。

**執行**:
- 實機 rename `D:\Models\sd\` → `D:\Models\diffusion\`(同槽 metadata 操作,59.88 GB / 17 檔 / 9 子資料夾不動)
- `extra_model_paths.yaml` `base_path` 改路徑
- 全 repo 9 份 MD 22 處引用同步
- 雙驗證器(stale-name grep + BOM 殘留)全綠
- ComfyUI 煙測**用 HTTP API `/object_info` 拉 dropdown**(比 GUI 載 workflow 更直接驗 yaml 解析端,本輪首次驗證有效)

**踩坑沉澱為教訓 6**(在 SYSADMIN_BRIEFING):bulk rename 派工的 grep pattern 必須涵蓋三類 — 絕對路徑全形式 / 末尾斜線雙形態 / 樹形圖獨立節點。原派工漏抓樹形圖 3 處 + 表格欄位末無尾斜線 4 處,執行端二次補抓才完整。

### 2.2 huggingface-download-tricks.md 兩段 SOP append

**「命名」段**:HF 通用 placeholder 檔名(`unet_fp8` / `diffusion_pytorch_model`)→ 必須加 repo 識別前綴改名。例外:HF 原檔名已含識別性 → 維持原檔名。

**「路徑慣例」段**:模型落地分類表 + LLM 類例外(寫死 `LLavacheckpoints`)+ HTTP API 驗證範例。

**為何沉澱**:#2 workflow 重建時遇到 2 例 placeholder 需改名,#1 workflow 本輪驗證命名實踐有效,把 SOP 落入文件以後重建中國 workflow 不必每次重新討論。

### 2.3 Commit / push 紀律核心改寫(三檔同步)

**動機**:Wayne 在第二輪整合報告時抓到執行端 progress report 的「待辦」段列「Wayne commit + push」當項目,等同把 Wayne 決策動作植入執行端流程,職責越界。

**改寫**:
- **user-level `CLAUDE.md` 硬規則 4** — 從「不主動 git commit / push」加強成「不在 progress report 列、不在對話暗示、不草擬 message,且不存在『自動 commit』例外」
- **PROGRESS_TEMPLATE.md 使用說明** — 5-6 行改成「由 Wayne 決定何時 commit + push」(時機、訊息、批次都是 Wayne 決策)
- **SYSADMIN_BRIEFING.md 主窗口職責第 6 條** — 派工模板的「邊界」段不寫「Wayne 自己做 commit」這類引導語

**為何走核心紀律改寫不是教訓段**:這不是「踩坑後的紀律」,是「角色邊界本來就該這樣」,該直接改 CLAUDE.md 的核心條目,不該降階成教訓。

### 2.4 Workflow #2「Flux-fill OneReward 萬物移除」完整重建

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

**JSON 本地化 5 處**:
- LoRA 名去中文後綴(`removal_timestep_alpha-2-1740_物品移除.safetensors` → `removal_timestep_alpha-2-1740.safetensors`)
- RunningHub auth token 清空(rgthree Image Comparer widget_values)
- LoadImage clipspace 路徑清空
- VAELoader 名 `ae.sft` → `ae.safetensors` 對齊本地實際檔
- **#113 Mask Fill Holes 節點換成 KJNodes `GrowMaskWithBlur`**(等價替代,參數設 `expand=0, blur_radius=0, fill_holes=True`)

**為何不裝 was-node-suite-comfyui 而走替代節點路線**:該 pack 2025-06 已被作者 archived,為了 1 個節點裝整 archived pack 維護負擔不對等。KJNodes 已裝且有等價節點,優選。Wayne 拍板。

**雙煙測通過**:
- HTTP API `/object_info`:6 個檔 + 17 個節點 type 全可達
- GUI 跑通:VRAM 高峰 **24088 MB**(逼近 5090 Laptop 24 GB 物理上限)、生成時間 **93.68 秒 / 10 步**(這是 Wayne 第二次有畫 mask 的真實數據;首跑 84.08 秒沒畫 mask,**不採用**)
- 輸出檔:`D:\Media\AI_Raw\ComfyUI_Output\ComfyUI_00002_.png`(3.45 MB)

### 2.5 兩個 STOP 點處理

**STOP 1**:Mask Fill Holes 節點不存在,候選 pack `was-node-suite-comfyui` 已 archived。Wayne 拍板走「找替代節點」路線(選項 3),CC 找到 KJNodes `GrowMaskWithBlur` 等價(都用 `scipy.ndimage.binary_fill_holes`)。

**STOP 2**:派工指定的 ae.sft 來源 `Comfy-Org/flux1-dev` 沒 ae 單檔(只有 all-in-one 整合包)。Wayne 拍板走 `Comfy-Org/z_image_turbo/split_files/vae/ae.safetensors`(Comfy-Org 官方鏡像,非 gated)。

**派工模板教訓**:下次寫派工時 ae 來源更正成 `Comfy-Org/z_image_turbo`,別再寫 `Comfy-Org/flux1-dev`。

---

## 3. 中國 workflow 重建路線(本輪不變)

| 優先 | Workflow | 狀態 |
|---|---|---|
| 1 | JoyCaption Beta1 反推 | ✅ 完成(04-26) |
| 2 | **Flux-fill OneReward 萬物移除** | ✅ **本輪完成(04-29)** |
| 3 | Kontext + ControlNet 姿態改變 | 待開始(下個主軸候選) |
| 4 | Qwen3 TTS 聲音克隆 | 待開始 |
| 5 | Qwen image 擴圖 | 待開始 |
| 6 | 智能多角度生成 | 待開始 |
| 7 | Qwen3 TTS 聲音設計 | 待開始 |

---

## 4. ⚠️ 主窗口端「待整合 patch」清單(下次接班務必處理)

本輪 #2 workflow 跑完後產生的工作成果**還沒整合進對應 MD**。下次主窗口接班時,Wayne 會貼這張清單給你,你逐一產 patch:

| # | 目標 MD | 該加的內容 |
|---|---|---|
| 1 | `comfyui/setup.md` — Diffusion / LoRA / CLIP / VAE 表格 | 6 個新檔(OneReward fp8 11.085 GB / Flux-Turbo-Alpha 0.646 GB / removal_timestep 0.086 GB / clip_l 0.229 GB / t5xxl_fp8 4.558 GB / ae.safetensors 0.312 GB)|
| 2 | `comfyui/workflows.md` — 圖像編輯系列 | 加新 workflow 條目(18 節點 / VRAM 24088 MB / 93.68 秒 / 10 步,**不要寫首跑 84.08 秒**),「待建立 workflow」清單優先 2 打勾 |
| 3 | `comfyui/conflicts.md` | (a) 新增「上游 archived pack 警示」段,was-node-suite-comfyui 進去 (b) 「KJNodes `GrowMaskWithBlur` ≡ WAS `Mask Fill Holes`」等價對應 |
| 4 | `comfyui/conflicts-kjnodes.md` | 記下 #2 workflow 對 `GrowMaskWithBlur` 的依賴(KJNodes 上游若 breaking change 會失效) |
| 5 | `comfyui/huggingface-download-tricks.md` 命名段 | 實例表加 2 例(`unet_fp8` / `diffusion_pytorch_model` 改名前後對照) |
| 6 | `ai-models/local-models.md` | FLUX.1 系列補 OneReward fp8 + Turbo-Alpha 條目 |

**還有兩條教訓候選暫存**(下次主窗口可問 Wayne 是否要進):

- **教訓 7 候選**(line ending bulk patch):2026-04-29 commit 紀律改寫時 CC 踩到「兩檔 LF only 一檔 CRLF」,解法是「寫回時保留原 line ending,避免污染 git diff」。我推進 SYSADMIN_BRIEFING 教訓段。
- 教訓 8(中國 workflow 簡轉繁)**已撤銷**,Wayne 不做。

---

## 5. 還沒做的待辦(從 SESSION_HANDOFF v1 延續)

| # | 待辦 | 觸發條件 |
|---|---|---|
| 1 | NIM 復服後重試 v4-flash chat completion | NIM upstream 復服 |
| 2 | 中國 workflow #3-#7 模型下載(~100-150 GB,不含本輪已下的) | #2 完成後可開始 |
| 3 | CrewAI 第一條 agent pipeline | 1-2 個月後 |
| 4 | 第一次 C 槽 baseline 映像 | 觸發條件全達成才做 |
| 5 | SageAttention issue #357 修復後重編 | 上游修復通知 |
| 6 | Hasleo Rescue USB 6 個月驗證 | 約 2026-10 月底 |
| 7 | 繁中 TTS 避雷字典 | 第二集動工前 |

主窗口紀律:這些**記著但不主動催 Wayne 做**。Wayne 自己會決定何時做,他來問就提供選項 + 風險。

---

## 6. Wayne 工作風格(本輪 session 觀察補充)

延續 04-28 + 04-29 v1 的觀察。本輪補幾條:

### 細節

- **接班 audit 比想像中更主動**:本輪 Wayne 是看到派工模板裡 `D:\Models\sd\` 才回頭問「sd 是不是 SD WebUI 命名」,**主窗口應該在接班時就抓到**,而不是等 Wayne 順手提才察覺。教訓 1 的「audit repo 結構合理性」要加一條子問題:**資料夾命名跟實際內容對齊嗎?**
- **Wayne 抓邏輯一致性極快**:本輪兩個強烈例子 — (a) 「commit/push 是 Wayne 決策範疇」直接點出主窗口 / 執行端的職責邊界沒寫清楚 (b) 教訓 9 候選(GUI 互動驗證標準)Wayne 直接拒絕(理由沒寫,但合理推測 — 不該為單次失誤沉澱成系統規則)
- **拍板極簡**:單字母 / 兩字組合(`A` / `B+B` / `A`)是 Wayne 標準回覆,不重複 context。主窗口收到要對照上文準確 parse

### 容易誤解的點

- **「workflows IGNORE」≠ 「整個目錄 gitignore」**:Wayne 一句「我想讓 comfyui-workflows 裡面的 IGNORE,對結構有什麼影響?」我第一輪解讀成「整個目錄 gitignore」並寫了一大段論證為什麼不該做。Wayne 二輪補一句「裡面有簡體字,改繁體字」我才發現他是在問「個別檔內容處理的副作用」,**根本跟 gitignore 沒關係**。教訓:**Wayne 講話省略主詞時,我該先問「你說的 IGNORE 是指 git 還是 OpenCC 那種 ignore」**,不要直接往一個解讀深挖
- **「測試圖選擇」是建議不是要求**:本輪 Wayne 最終用藤椅照片(自選),我前面建議的「鏤空椅子 / 戒指」沒被採用 — Wayne 會聽建議但用自己判斷選素材,主窗口別堅持自己的建議
- **「重測」是因為流程沒到位,不是結果有疑**:本輪 Wayne 第一次跑沒畫 mask 是因為**派工模板 Step 6b 沒寫「右鍵 MaskEditor 畫 mask」**這條使用前置。Wayne 收工時提「需要重測」,我問清是 A(功能沒過)還是 B(數據污染),他選 B — **派工漏寫 + 數據要清理 + Wayne 不要為單次失誤沉澱規則**,三條並存

---

## 7. 接班開場 SOP(本輪 session 不變動)

跟 04-28 + 04-29 v1 一致。要做的事:

1. Project knowledge 自動載入(SYSADMIN_BRIEFING + CLAUDE.md + 本 handoff + README + context)
2. 用你自己的話回 Wayne:
   - 你的角色(sysadmin + 決策諮詢)
   - repo 現況(本輪 #2 workflow 完成 + **6 份待整合 patch 還沒產**)
   - 進行中脈絡
3. 等 Wayne 給任務,**不主動建議今天做什麼**

---

## 8. 接班測試題(本輪新增 2 題)

承襲 04-28 + 04-29 v1 共 10 題,本輪補 2 題:

**11. Wayne 派工跑完 ComfyUI workflow 後,執行端 progress report 的「待辦」段該不該列「Wayne commit + push」當項目?**

預期答案:**不該**。Commit / push 是 Wayne 的決策範疇,不在執行端視野內 — 這是 user-level CLAUDE.md 硬規則 4 跟 SYSADMIN_BRIEFING 主窗口職責第 6 條的核心。執行端「完成」邊界 = 實機執行 + 文件 patch + 驗證 + 寫 report **停**。Commit message / 時機 / 批次全部不在執行端視野。

**12. 派工模板邊界段該怎麼寫 commit 紀律?**

預期答案:**完全不寫**。不寫「Wayne 自己做 commit」、不寫「不擅自 commit」、不寫「commit 後通知」等任何提到 commit / push 的引導語。讓 commit 完全脫離執行端視野。核心紀律已由 user-level CLAUDE.md 硬規則 4 cover,不必在每份派工模板重提。

---

## 9. Session 結束時 repo 的乾淨指標

下一個 session 接班時應該確認以下都成立:

- [ ] `git status` 顯示有「多批未 commit 變更」(預期狀態 — Wayne 未 commit 完所有累積)
- [ ] `git log --oneline -10` 顯示截至 04-29 v1 的 commit 鏈(本輪 v2 變更**還沒進 commit log**)
- [ ] `SYSADMIN_BRIEFING.md` 教訓段有 6 條(教訓 6 = grep pattern 完整性)
- [ ] `SYSADMIN_BRIEFING.md` 主窗口職責段有 6 條(第 6 條 = 派工模板邊界段不寫 commit 引導語)
- [ ] `D:\Work\system-setup\CLAUDE.md` 是 v2.0(project-level)
- [ ] `C:\Users\Wayne\.claude\CLAUDE.md` 硬規則 4 標題是「Commit / push 是 Wayne 的決策範疇」(不是「不主動 git commit / push」)
- [ ] `PROGRESS_TEMPLATE.md` 使用說明 5-6 行寫「由 Wayne 決定何時 commit」
- [ ] `D:\Models\diffusion\`(不是 `D:\Models\sd\`)存在,內 17 檔 / 59.88 GB / 9 子資料夾
- [ ] `extra_model_paths.yaml` `base_path` 指向 `D:\Models\diffusion\`
- [ ] `comfyui-workflows\Flux-fill_OneReward_萬物移除_10步.json` 存在
- [ ] `D:\Models\diffusion\diffusion_models\flux.1-fill-dev-OneReward-fp8.safetensors` 存在(11.085 GB)
- [ ] `D:\Models\diffusion\loras\` 含 `Flux-Turbo-Alpha.safetensors` + `removal_timestep_alpha-2-1740.safetensors`
- [ ] `D:\Models\diffusion\clip\` 含 `clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors`
- [ ] `D:\Models\diffusion\vae\ae.safetensors` 存在
- [ ] `progress-reports\` 內**只有** README.md(本輪 4 份 report 已被 Wayne 整合 + 刪除)
- [ ] Claude Projects 設定:
  - knowledge 含本 handoff(`SESSION_HANDOFF_2026-04-29.md` v2)
  - knowledge **已移除舊版** `SESSION_HANDOFF_2026-04-29.md` v1
  - custom instructions 已貼

任一不成立 → 跟 Wayne 釐清。

**特別留意**:第 4 段「待整合 patch 清單」**6 份 MD patch + 教訓 7 候選還沒產**。下次主窗口接班的開場任務(假設 Wayne 拍板要整合)就是處理這 6 份。

---

## 10. 連結速查

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

**本快照建立日期**:2026-04-29(v2)
**蓋掉**:同日 v1
**v2 更新理由**:本輪 session 在 v1 基礎上完成 4 大批變更(`sd → diffusion` rename / 教訓 6 + HF SOP / commit 紀律改寫 / Workflow #2 重建),v1 沒記;且累積 6 份待整合 patch 主窗口端尚未產出,需要明確 handoff 給下次接班。
