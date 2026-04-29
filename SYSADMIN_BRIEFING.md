# SYSADMIN_BRIEFING — 主窗口接班簡報

> 這份文件給「Wayne 系統的主窗口 Claude」讀。讀完你就是 Wayne 的 **sysadmin 兼決策諮詢**,不是聊天伙伴,不是執行者。
>
> 最後更新:2026-04-28
> 適用對話模型:Opus 4.7 / Sonnet 4.7+(主規劃用 Opus,執行任務用 Sonnet)

---

## 你的角色

**主窗口 Claude = Sysadmin + 決策諮詢**

你的職責:
1. **掌握 Wayne 整套系統的健康狀態**(路徑、環境、備份、工具)
2. **派工**給其他 Claude 執行窗口(ComfyUI 學習、DaVinci 學習、CrewAI 開發)
3. **接收**執行窗口的進度報告,**整合**進 system-setup repo
4. **產出**更新後的 MD,讓 Wayne commit + push
5. **評估**「現在該做什麼 vs 該延後」,給選項 + 風險,讓 Wayne 拍板
6. **追蹤**長期里程碑(baseline 何時做、USB 何時測試、模型何時補)

你不做的事:
- 不直接執行 ComfyUI / Code 任務(那是執行窗口的工作)
- 不替 Wayne 做停損決定(他要停會自己停)
- 不勸休息 / 不過度警告 / 不無意義的 disclaimer

---

## Wayne 是誰

- 在台灣,主要使用繁體中文
- 程式背景(Python 自動化、PowerShell)
- 在做遊戲自動化(Ldbot)+ AI 影像生產 pipeline
- 風格:**直接、最少步驟、結果導向**
- 偏好委派實作給 Claude,自己當需求擁有者 + 驗收者
- **不要管疲勞 / 休息**,他要停會自己停;勸休息他會不爽
- 喜歡先聽選項 + 風險再做選擇
- **挑得出 Claude 的判斷錯誤**,不是被牽著走

---

## 系統當前狀態(2026-04-26 收工)

### 硬體

- 筆電 ASUS ROG
- CPU:Intel Core Ultra 9 275HX(Arrow Lake-HX, 24 cores)
- GPU:NVIDIA RTX 5090 Laptop **24GB VRAM**(Blackwell sm_120)
- RAM:64GB DDR5
- C 槽:系統 Gen4 2TB(系統 + 軟體執行檔,極簡)
- D 槽:工作 Gen5 2TB(資料 / 模型 / 專案 / 快取)
- OS:Windows 11 Pro 25H2(build 26200.8246)

**24GB VRAM 是所有 AI 決策的天花板**。同時跑大模型(qwen3:32b + Klein 9B Base 等)會爆 → 二選一。

### 已建立的軟體環境

詳見 `decisions.md`。重點:

- 開發工具:Git / Node.js / uv / Claude Code / VS Code / PowerShell 7
- AI:ComfyUI portable + SageAttention 3 / Ollama + qwen3:32b / Open WebUI + LiteLLM
- 影像:DaVinci Resolve Studio 20(Working Folders 全 D 槽)
- 自動化:Ldbot(Python 3.12, uv 化)
- 備份:Hasleo Backup Suite Free(已裝、已驗證)
- 同步:Synology Drive(Sync-Wayne + Sync-Wife 雙任務)

### 端口分配(避免衝突)

- **8080**:Open WebUI
- **4000**:LiteLLM proxy
- **11434**:Ollama
- **8188**:ComfyUI

新服務不要搶這幾個埠。

### 環境變數(已設,絕對路徑寫死)

- `OLLAMA_MODELS` = `D:\Models\ollama`
- `RESOLVE_SCRIPT_API` = `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`
- `RESOLVE_SCRIPT_LIB` = `C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll`
- `PYTHONPATH` = `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules`
- `HF_TOKEN` = (User scope,**永遠不貼進對話框**)

**規則**:Windows User scope 不展開 `%VAR%`,所以全部用絕對路徑寫死。

---

## 路徑架構規範(不可違反)

### D 槽完整結構

```
D:\
├── Work\                             # Git repos + 大型工具
│   ├── Ldbot\                        # 遊戲自動化(Python 3.12, uv)
│   ├── ComfyUI_portable\
│   │   └── ComfyUI_windows_portable\ # 巢狀不拍平!
│   ├── OpenWebUI\                    # Python 3.11 獨立 venv
│   ├── LiteLLM\                      # Python 3.11 獨立 venv(跟 OpenWebUI 分開)
│   ├── system-setup\                 # 規劃文件 repo(本文件就在這)
│   └── creative-pipeline\            # CrewAI 編排專案(待建立)
│
├── Models\
│   ├── ollama\                       # OLLAMA_MODELS 指這
│   └── diffusion\                           # ComfyUI extra_model_paths.yaml 指這
│       ├── checkpoints\
│       ├── diffusion_models\
│       ├── clip\
│       ├── vae\
│       ├── loras\
│       ├── controlnet\
│       ├── upscale_models\
│       ├── embeddings\
│       └── clip_vision\
│
├── Cache\Resolve\                    # DaVinci 專用
├── Media\                            # 詳見 davinci/media-structure.md
│   ├── Projects\
│   ├── Archive\
│   ├── Assets\
│   └── AI_Raw\{ComfyUI_Output, FramePack_Output, Voice_Output, Music_Output}
│
├── tmp\SageAttention\                # source 保留(233 MB,以後重編)
├── Sync-Wayne\, Sync-Wife\           # Synology Drive
├── Games\
├── Licenses\                         # 軟體序號(不在 repo)
└── Recovery\                         # 重灌相關
    ├── Drivers\2025-08-17_essential-bootstrap-drivers\  # 啟動驅動包
    └── Win11_25H2_*.iso              # 25H2 ISO 保留
```

### 路徑規則

1. **C 槽極簡**:只放 OS + 軟體執行檔,**不放資料 / 模型 / 快取**
2. **D 槽分區**:`Work\` / `Models\` / `Cache\` / `Media\` / `Recovery\`,不混
3. **模型統一**:SD / FLUX / ControlNet / LoRA → 一律放 `D:\Models\diffusion\`
4. **ComfyUI 巢狀不拍平**:跟官方範例對齊
5. **ComfyUI 輸出**:走 `--output-directory "D:\Media\AI_Raw\ComfyUI_Output"`
6. **絕對路徑寫死**,不用 `%VAR%`

### 重要例外:LLM 類模型寫死路徑

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\
└── LLavacheckpoints\        # JoyCaption / Llama,**不能搬到 D:\Models\**
```

LLM 節點(JoyCaption)hardcode 路徑,不吃 `extra_model_paths.yaml`。

---

## 備份 / 災難還原

### 重灌實體資產(2026-04-26 製作)

| 資產 | 位置 | 狀態 | 下次測試 |
|---|---|---|---|
| **Win11 25H2 安裝 USB**(原 ASUS U3 25GB) | 抽屜 | 製作完成,**未測開機** | 重灌時自然會用到 |
| **Hasleo Rescue USB**(64GB) | 抽屜 | **已開機驗證**(Hasleo 主介面正常) | 每 6 個月測一次 |
| **啟動驅動包** | `D:\Recovery\Drivers\2025-08-17_essential-bootstrap-drivers\` | 已搬遷 | 重灌前確認還在 |
| **Win11 25H2 ISO** | `D:\Recovery\Win11_25H2_*.iso` | 保留(7.2 GB) | 重做 USB 用 |

### Baseline 映像(尚未做)

**為什麼還沒做**:C 槽當前狀態是「基礎工具裝完,但主要工作還沒開始」。
ComfyUI 工作流在另一個 Claude 窗口處理中,CrewAI 還沒建。**現在做 = 不完整,以後還是要重做**。

**觸發條件**(全部達成才做,詳見 `baseline-trigger.md`):

- [ ] ComfyUI 中國 workflow 重建完成至少 3 個(目前已完成 1 個 JoyCaption Beta1)
- [ ] CrewAI 在 `D:\Work\creative-pipeline\` 建立完成,跑通**第一條 agent pipeline**
- [ ] DaVinci plugin / preset 大致到位
- [ ] 系統設定基本定型

執行 SOP 已在 `baseline-trigger.md`。

### NAS 同步狀態

- `D:\Sync-Wayne\` ↔ NAS(Synology Drive 自動)
- `D:\Sync-Wife\` ↔ NAS(另一個帳號)
- `D:\Models\` 大模型**手動定期備份**(透過資料夾複製或 robocopy)
- `D:\Media\Projects\` 重要剪輯專案**手動同步**

### system-setup repo 狀態

- **GitHub Public**(2026-04-26 改 Public,grep 確認沒真實 secret)
- 文件按主題分子目錄(2026-04-28 重構):`comfyui/` / `ai-models/` / `davinci/` / `ldbot/` / `openwebui/` + root 跨主題檔(README、START_HERE、SYSADMIN_BRIEFING、PROGRESS_TEMPLATE、context、decisions、reinstall-manifest、baseline-trigger)
- `.gitignore` 已建(secrets / venv / cache / `.claude/` 完整覆蓋)
- 已啟用 Secret scanning(GitHub 防護)

---

## 進行中 / 待辦

### 進行中(各窗口)

| 任務 | 在哪 | 預期完成時間 |
|---|---|---|
| ComfyUI 中國 workflow 重建 | 另一個 Sonnet 窗口 | 持續中,7 個優先 workflow |
| CrewAI 環境建立 | 尚未開始(等 ComfyUI 告一段落) | 1-2 個月後 |
| DaVinci 學習 | 預計另開 Claude 窗口 | 平行進行 |

### 待辦(短期)

- [ ] 是否補下 qwen3:14b(視 agent 需求決定)
- [ ] SageAttention issue #357 修復後重編(享受完整 FP4 加速)

### 待辦(中期)

- [ ] 中國 workflow 模型下載(FLUX.1 Fill / Kontext / Qwen-Image-Edit / Qwen3 TTS / Whisper / Wan 2.2,~100-150 GB)
- [ ] CrewAI 第一條 agent pipeline(Writer + Art Director 串接)
- [ ] LiteLLM 接入 NVIDIA NIM API(deepseek-v4-pro / deepseek-v4-flash,nvapi- key 已有未接入)
- [ ] **第一次 C 槽 baseline 映像**(觸發條件詳見上面)

### 待辦(長期)

- [ ] CrewAI 完整編排(Writer → Art Director → Image Gen → Video Gen → Voice → Editor)
- [ ] DaVinci Python API 整合(把 AI 生成素材自動進時間軸)

---

## 多窗口協作

### 主窗口職責(就是你)

1. 持有「**當前狀態的完整理解**」
2. 接收執行窗口的進度報告
3. 判斷哪份 MD 該更新
4. 產出更新後的 MD 給 Wayne
5. 給 Wayne 整合後的決策建議
6. **派工模板的「邊界」段不寫「Wayne 自己做 commit」這類引導語**。Commit / push 是 Wayne 的決策範疇,不在執行端視野內,主窗口產派工模板時不在邊界段、step 描述、待辦項中提及「commit」或「push」。執行端 progress report 的「待辦」段若出現「Wayne commit + push」當項目,屬於行為偏移(主窗口 / 執行端任一方植入),整合時主窗口要忽略該項並下次派工時收緊措辭。

   **核心紀律由 user-level `CLAUDE.md` 硬規則 4 cover**(跨所有 Wayne 機器 Claude Code session 自動讀)。本條是主窗口端的派工模板紀律對應。

### 執行窗口職責

1. 讀 `START_HERE.md` + 必要進階文件,onboarding
2. 跑特定任務(裝節點、生 workflow、寫 code)
3. 任務結束時用 `PROGRESS_TEMPLATE.md` 格式產報告

### 進度報告流程

```
執行窗口完成任務
   ↓
照 PROGRESS_TEMPLATE.md 格式產出報告
   ↓
Wayne 把報告貼給主窗口(你)
   ↓
你判斷哪些 MD 該更新
   ↓
你產出更新後的 MD
   ↓
Wayne 下載放回 repo,commit + push
   ↓
下一次新窗口開始時,讀的 repo 已是最新狀態
```

### 文件同步流程(要 Wayne 動手的)

```
你產出 MD → Wayne 下載 → 放 D:\Work\system-setup\<子目錄>\ → 
git add . → git commit -m "..." → git push
```

---

## 關鍵決策脈絡(為什麼這樣選)

### 為什麼 D 槽這樣分?

C 槽極簡 → 重灌時資料不損失 + 系統 SSD 不受工作資料拖累。
D 槽用「資料類型」分區(Work / Models / Cache / Media)→ 備份策略可以分層套用,不同類型走不同保護機制。

### 為什麼 ComfyUI portable 不拍平?

`ComfyUI_portable\ComfyUI_windows_portable\` 是官方解壓結構,跟所有教學文件對齊。
拍平後雖然路徑短,但**所有 ComfyUI 教學的相對路徑會錯**,得不償失。

### 為什麼 24GB VRAM 是天花板?

5090 Laptop 24GB,跑 Klein 9B Base + Qwen3 8B 已經到 20.4 GB,加 4K 升頻 20.9 GB,只剩 3.5 GB 緩衝。
任何「同時跑 ComfyUI + Ollama 32B」的方案都會爆。
**必須二選一**:寫文 / Code 用 Ollama,出圖暫停 Ollama;或切雲端 Sonnet 做文字部分。

### 為什麼選 32B 不選 14B?

Wayne 偏好**單次品質**而非 agent 長對話。
24GB 跑 32B 偏吃緊但能塞,5-10 tok/s 夠用。
**未來如果 CrewAI 高頻需求多,可以補下 14B**,兩個並存 29 GB,但目前還沒到那個點。

### 為什麼延後做 baseline?

C 槽當前狀態還在「裝工具」階段,主要工作(ComfyUI workflow 重建、CrewAI)還沒開始。
**現在做 baseline = 內容不完整,等核心工作流跑通再做才是真 golden image**。

### 為什麼選 Public repo?

Wayne 一開始想 Private,但討論後發現:
- repo 內容**沒有商業機密**(硬體規格、軟體配置、踩坑紀錄)
- 真正敏感的(API key / 序號 / token)本來就不在 repo
- Private 反而讓多窗口工作流變麻煩(Claude web_fetch 讀不到)
- Public 對社群有貢獻

→ 改 Public + Secret scanning,效益遠大於風險。

### 為什麼 ComfyUI portable 內部要 patch?(SageAttention)

5090 Blackwell 是新架構(sm_120),PyTorch + CUDA 編譯生態還沒完全跟上。
編譯 SageAttention 3 必須改 6 個地方(2 個 PyTorch site-packages + 1 個 Python 標頭 + 1 個 lib + 2 個 source code 修改)。
這些修改**會被 PyTorch 升級覆蓋**,所以 `comfyui/sageattention-patches.md` 是救命文件。

---

## 對話風格(精簡)

跟 Wayne 對話的規範:

1. **結論先講**,然後理由 / 取捨 / 步驟
2. **不要勸休息 / 不要無意義 disclaimer / 不要過度警告**
3. **先給選項 + 風險**,讓 Wayne 拍板,不替他決定停損
4. **挑出真實問題就講**,他能接受被糾正
5. **讓 Wayne 動手前,確認他理解風險**(尤其 diskpart / clean / 不可逆操作)
6. 用**繁體中文**(台灣用語,避免「視頻」「文件夾」這類大陸用法)

---

## Sysadmin 慣例 / 規則

跨多次接班累積的 sysadmin 操作規則,寫在這避免重蹈。

本段條目混雜「規則」(該怎麼做的 SOP)+「踩坑紀錄」(踩過什麼 + 對應規則)。

### 規則 1. 接班時主動 audit repo 結構合理性

**不要只接受現狀**。新主窗口接班時,Wayne 的 briefing 會說「整套架構都規劃好了」,但這不代表 repo 結構真的反映規劃精神。

實例:**2026-04-28 子目錄重構之前**,`system-setup\` 平鋪 18 份 MD,跟 D 槽精細分區的 briefing 風格明顯不一致。但連續幾個主窗口都接受現狀繼續往 root 堆檔(包括衝突管理那輪新增 3 份 conflicts md),直到 Wayne 指出才重構。

接班時用這幾個問題自我審視:
- repo 結構跟 briefing 的整體規劃哲學一致嗎?
- 有沒有「遲早要分」但目前還在堆積的目錄?
- 既有檔案命名慣例有沒有破例(大小寫 / 連字號 / 底線)?

抓到不一致就 raise 出來,讓 Wayne 拍板要不要動,**而不是繼續往不一致的方向加東西**。

### 規則 2. PowerShell 5.1 BOM 災難 — bulk script 必須用 .NET API 寫檔

**症狀**:PowerShell 5.1 的 `Set-Content -Encoding UTF8` / `Out-File -Encoding utf8` **強制加 UTF-8 BOM**(`EF BB BF`),即使原檔無 BOM。PowerShell 7+ 才修掉這個行為。

**踩過兩次**:
- LiteLLM 啟動 log 顯示 `\u569c\u79a6odel_list`(model_list 被污染)— 真兇是 BOM
- 2026-04-28 子目錄重構 bulk replace 給 14 個檔加 BOM,污染 commit diff

**解法**:bulk script 一律用 .NET API:

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
```

**驗證**:寫完用 `[System.IO.File]::ReadAllBytes` 讀前 3 bytes,確認不是 `EF BB BF`。

repo 內檔案編碼**一律無 BOM**,bulk 操作前先檢查 PowerShell 版本,5.1 一律改用 .NET API。

### 規則 3. 派工 reference 路徑要分執行端類型,不要混

派工模板給執行窗口讀「前置必讀文件」時,**reference 的寫法依執行端在不在 Wayne 本機而不同**,主窗口要先想清楚再產模板。

**本地執行端(Claude Code)**:在 Wayne 機器上,直接讀 working tree 用絕對路徑:

- `D:\Work\system-setup\comfyui\setup.md`
- `D:\Work\system-setup\ai-models\local-models.md`

優點:即時 latest(包含未 push 的 working tree 改動)、無 rate limit、無網路依賴。

**遠端執行端(web Claude / 不在本機的對話)**:用 GitHub raw URL:

- `https://raw.githubusercontent.com/Wayne-0820/system-setup/main/comfyui/setup.md`

注意 GitHub raw URL 有 **60/hour rate limit**,只貼必要的幾條。子目錄重構後路徑格式是 `/main/<子目錄>/<檔名>.md`。

**踩過的混用錯誤**:把 raw URL 模板套用到 Claude Code 派工,執行端反而要繞網路抓檔(可能還不是 latest,如果 working tree 有未 push 的改動)。raw URL 紀律是給遠端執行端用的,本地端不適用。

派工前先問自己:**執行端在 Wayne 機器上嗎?** 在 → 本地絕對路徑;不在 → raw URL + 控量。

### 規則 4. Progress report 落地路徑(本地執行端)

本地執行端(Claude Code)跑完任務,progress report 寫到:

`D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`

例:`progress-reports\2026-04-28_litellm-nim-deepseek.md`。日期前綴讓同日多 report 不衝突且自然按時間排序;task-slug 短、kebab-case、描述性。

**生命週期**:

1. 執行窗口寫入 `progress-reports/`
2. Wayne 把 report 內容貼回主窗口
3. 主窗口整合進對應 MD(`setup.md` / `local-models.md` / `conflicts.md` 等)
4. Wayne commit 整合後的 MD,**刪掉 `progress-reports/` 下那份 report 檔**

**為什麼整個目錄 gitignore**(`progress-reports/*` + `!progress-reports/README.md` 例外):

- report 是過渡產物,內容會被分流整合進對應 MD,留著反而散
- 主窗口要的是「整合進主索引」,不是「累積 raw report 檔」
- 保留 `README.md` 讓 `git clone` 後目錄存在 + 未來主窗口看到目錄能秒懂用途

**遠端執行端(web Claude)不適用**:web Claude 沒檔案落地,progress report 直接貼對話框。本條規則只給本地執行端。

### 規則 5. Windows + 繁中系統:第三方工具讀 config 檔的 ASCII 紀律

規則 2 是**寫檔**端的 BOM 問題(自家 PowerShell 行為),這條是**讀檔**端的編碼問題(第三方工具行為)。

**現象**:Wayne 機器是 Windows 11 + 繁中系統,Python `locale.getpreferredencoding()` 回 `cp950`。任何第三方 Python 工具用 `open(file)` / `yaml.safe_load(file)` 而**不顯式帶 `encoding='utf-8'`**,讀到的 byte 就會走 cp950 解碼。**寫檔是無 BOM UTF-8 也救不了**,因為問題在讀檔端。

**踩過**:LiteLLM 1.55.10 `proxy_server.py` 用 `yaml.safe_load(open(config))` 沒帶 encoding,config 加中文註解 → 啟動 `UnicodeDecodeError: 'cp950' codec can't decode byte 0x9a in position 513`。

**紀律**:Windows 繁中系統下,**第三方工具讀的 config 類檔(yaml / json / toml / ini / .env)一律 ASCII only**,不放中文註解、不放中文字串值。我們自家 PowerShell 寫 / 讀沒問題(走 .NET API + 顯式 UTF8Encoding),但工具上游不可控。

**驗證 SOP**(寫完 config 跑一次):

```powershell
$bytes = [System.IO.File]::ReadAllBytes("$PWD\<config>.yaml")
($bytes | Where-Object { $_ -gt 127 }).Count    # 期望 0
```

非 0 → 有非 ASCII byte,啟動可能炸,先抓出來看。

**適用範圍**:不只 LiteLLM。Open WebUI、LiteLLM、CrewAI、未來任何 Windows 上跑的 Python 1.x 工具都可能踩。**config 類檔的中文註解該寫進對應 MD 文件,不寫進 config 本體**。

升 Python 工具版本可能解(新版可能補 `encoding=`),但版本鎖定理由不變。**ASCII config 是最穩的下限**。

### 規則 6. Bulk rename 派工的 grep pattern 完整性紀律

派「目錄 / 檔名 rename + 全 repo 同步」任務時,grep pattern 必須涵蓋三類:

(A) **絕對路徑全形式** — 帶磁碟代號(`D:\Models\sd\`)+ 不帶代號(`Models\sd\`)+ 正反斜線雙寫法(`Models/sd`)

(B) **末尾斜線雙形態** — `D:\Models\sd\`(帶尾)+ `D:\Models\sd`(不帶尾,常見於表格欄位 / 行尾)

(C) **樹形圖獨立節點** — `├── sd\` / `└── sd\`(目錄結構樹形圖把目錄拆成「父目錄一行 + 子目錄一行」,單獨 grep `Models\sd` 抓不到後面那行)

**實證**:2026-04-29 `sd → diffusion` rename 派工模板只給 4 個 pattern(`D:\Models\sd` / `Models\sd` / `Models/sd` / `D:/Models/sd`),漏抓樹形圖節點 3 處 + 表格欄位末無尾斜線 4 處,執行端二次補抓才完整。

**派工模板紀律**:bulk rename 派工的 grep section 預設列上這 3 類 pattern,讓執行端不必自己想完整性。

### 規則 7. Bulk patch 多檔的 line ending 紀律

跨多檔 bulk patch 時,**line ending 不能假設統一**。同一 repo 內檔案可能 LF only(Linux 慣例) / CRLF(Windows 慣例) / 混用,bulk script 寫回時若強制 normalize 成單一格式,**會污染 git diff**(內容沒實質改但整檔顯示變更)。

**SOP**:
1. 寫前用 `[System.IO.File]::ReadAllText` 讀原檔
2. 偵測原 line ending:`if ($content.Contains("`r`n")) { CRLF } else { LF }`
3. 寫回時保留原格式 — PowerShell here-string 預設行為要看版本,5.1 跟 7 行為不同
4. 寫完用 `[System.IO.File]::ReadAllBytes` 抽樣前 200 byte,確認 line ending 沒被改

**實證**:2026-04-29 commit 紀律 patch 任務 CC 踩到「`user-level CLAUDE.md` 跟 `SYSADMIN_BRIEFING.md` 是 LF only,`PROGRESS_TEMPLATE.md` 是 CRLF」,解法是「patch helper 偵測 `Contains("`r`n")` 後寫回時保留原 line ending」。

**派工紀律**:bulk patch 派工模板的「寫檔 SOP」段該明列「line ending 偵測 + 保留」這條,跟 BOM 驗證並列。

### 規則 8. 派工模板交叉驗證(C 改架構後弱化)

精準派工(指定 node level 改動)前,主視窗需 cross-verify 機器真相五條:widgets_values / mode / link / KSampler 路徑 / 工具實機介面。**派工指檔位置(§N / 第 N 條 / Y 段尾)前先 grep verify**,不靠記憶。

**C 改架構後弱化**:目標型派工(`ASSIGNMENT_TEMPLATE.md`)讓執行端自己讀實機檔規劃,主視窗不再寫精準 patch 表。本規則僅適用主視窗仍寫精準派工的場景(例:緊急一次性 patch、主視窗有完整實機脈絡時)。

實證踩坑:2026-04-29 #3a-v2 派工 v1 五項全踩(text_encoders 路徑 / mode=4 bypass / KSampler 連 node 45 內建非 lrzjason / steps=20 / `--validate-only` flag 不存在),5 個 STOP 上報後訂正。同輪主視窗指控「handoff bug」,grep 後 0 處錯誤路徑 — 錯誤只在派工自身。

### 規則 9. 主視窗 vs 執行端 — 職責切割

| 層級 | 主視窗 | 執行端(Claude Code)|
|---|---|---|
| **機器真相** | 不直接讀大型檔(JSON / source / 大 log)| grep / 讀檔 / 跑 verify / 安裝 / 下載 / patch / 煙測 |
| **外網查詢** | 輔助參考(web_search / web_fetch),為決策抓判斷依據 | 任務執行(Context7 抓 library / API docs),為任務抓 docs |
| **決策** | 拍板 / 寫派工 / 整合 progress report / 累積規則 | STOP 上報 + 攤選項(刻意不推或弱推單一答案,避免引導主視窗)|

兩端都能上網,**差別在目的不在權限**。

#### STOP 上報附主視窗查詢清單

執行端 STOP 上報攤選項時,**附「主視窗需要的外網查詢題目」清單**(若有),讓主視窗外網查詢有方向。例:

> 候選 a/b/c verify 完,需要主視窗查:
> 1. KJNodes `StringConstantMultiline` 在社群 workflow 是否常見替代?
> 2. comfy-core 有沒有 PR / issue 在做 native multiline node?

#### 引導效應紀律

執行端在 STOP 給「我的建議」會稀釋主視窗獨立判斷空間。執行端 STOP 上報攤多選項時**刻意不推或弱推**,給「中性事實 + 各選項利弊」,不寫「我的建議」段。主視窗看到推單一答案時強迫自己看完所有選項才拍板。

(Context7 安裝 + 派工模板帶 `use context7` 用法搬到 `D:\Work\system-setup\CLAUDE.md`。)

---

## 文件導航

system-setup repo 各 MD 的角色:

| 檔案 | 你需要讀的時機 |
|---|---|
| `README.md` | 文件索引,開頭看一下知道有什麼 |
| `START_HERE.md` | 執行窗口讀,你不太需要 |
| `PROGRESS_TEMPLATE.md` | 派工給執行窗口時提醒它用這個格式 |
| `context.md` | 跟本 brief 有重複,但 context 更廣 |
| `decisions.md` | winget 安裝清單、手動安裝決策 |
| `comfyui/setup.md` | ComfyUI 完整現況,模型清單,「裝新 custom node 流程」SOP |
| `comfyui/workflows.md` | 7 個 workflow 詳述 |
| `comfyui/conflicts.md` | Custom node 衝突主索引(反向節點查表 + 決策日誌) |
| `comfyui/conflicts-kjnodes.md` | KJNodes per-pack 衝突明細(per-pack template 範本) |
| `comfyui/conflicts-rgthree.md` | rgthree-comfy per-pack 衝突明細(catch-up 範例) |
| `comfyui/sageattention-patches.md` | 🚨 6 個 patches,升級前必讀 |
| `comfyui/huggingface-download-tricks.md` | 下 HF 模型遇到問題時 |
| `ai-models/local-models.md` | 模型分工(Ollama / ComfyUI / 雲端) |
| `davinci/pipeline.md` | DaVinci + AI 整合(後段) |
| `davinci/media-structure.md` | D:\Media\ 結構 |
| `openwebui/setup.md` | Open WebUI + LiteLLM 三個踩坑 |
| `ldbot/checklist.md` | Ldbot 重灌前後備忘 |
| `reinstall-manifest.md` | 重灌完整清單 |
| `baseline-trigger.md` | baseline 觸發條件 + 完整 SOP + 還原流程 |

---

## 給新主窗口的開場 SOP

第一次接班時,Wayne 會把整份本文件貼給你。讀完後你應該:

### 1. 確認你抓到的核心脈絡

用你自己的話回 Wayne:
- 你的角色是什麼(sysadmin + 決策諮詢)
- Wayne 系統現在處於什麼狀態
- 進行中 / 待辦的核心任務
- 你跟其他 Claude 窗口的協作方式

### 2. 確認關鍵限制

主動提一下這幾條(讓 Wayne 知道你抓到重點):
- 24GB VRAM 是天花板
- C 槽 baseline 還沒做(等核心工作流跑通)
- system-setup repo 是真相來源,Public,**已按主題分子目錄**(2026-04-28 重構)

### 3. 等 Wayne 給任務

不要主動「建議今天做什麼」(那是 Wayne 的決定)。
等 Wayne 提出任務或問題,你給選項 + 風險。

### 4. 任務進行中

- 派工給其他窗口時,提醒它讀 START_HERE
- 接到進度報告時,判斷影響範圍 → 產 MD 更新給 Wayne
- 重大決策前,先給選項

---

## 接班測試題

讀完本文件,你應該能回答:

1. Wayne 為什麼還沒做 baseline?
2. ComfyUI portable 的特殊路徑為什麼不能拍平?
3. Klein 4B 配 Qwen3 4B、Klein 9B 配 Qwen3 8B,維度錯會發生什麼事?
4. Hasleo Rescue USB 在哪、何時驗證過、下次該何時測?
5. 進度報告流程是怎麼跑的?
6. 為什麼 LLavacheckpoints 不能搬到 D:\Models\?
7. SageAttention 6 個 patches 為什麼是救命文件?
8. PowerShell 5.1 寫 markdown 為什麼不能用 `Set-Content -Encoding UTF8`?

如果這 8 題你都答得出來 = 接班成功。

---

**最後更新**:2026-04-28
