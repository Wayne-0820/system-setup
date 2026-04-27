# System Setup

Wayne 的系統建置規劃文件集,給 Claude / Claude Code 當脈絡的單一真相來源。

---

## 使用方式

### 開新對話時

#### 主窗口(Sysadmin + 決策諮詢)

把 `SYSADMIN_BRIEFING.md` 整份內容貼給新窗口,讓它接管 sysadmin 角色:

```
我要建立新的主窗口進行系統長期維護。
以下是接班簡報,請完整讀完內化:

=== SYSADMIN_BRIEFING ===
[整份貼上 D:\Work\system-setup\SYSADMIN_BRIEFING.md]
=== END ===

讀完後告訴我:
1. 你抓到的核心脈絡
2. 你準備好接手了嗎
3. 接班測試題你的回答
```

#### 執行窗口(跑特定任務)

```
我的 system-setup repo:https://github.com/Wayne-0820/system-setup

請用 web_fetch 讀(只這一份,避免 rate limit):
https://raw.githubusercontent.com/Wayne-0820/system-setup/main/START_HERE.md

你需要其他文件時告訴我檔名,我會直接貼內容給你。

我這次要做的事:[填入]
任務結束時請用 PROGRESS_TEMPLATE.md 格式產出進度報告。
```

### 任務結束時

執行窗口照 `PROGRESS_TEMPLATE.md` 格式產出進度報告,完整貼給主窗口。
主窗口產出更新後的 MD,Wayne 再 commit + push 完成同步循環。

---

## 文件索引

### 🚪 入口文件(優先讀)

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `SYSADMIN_BRIEFING.md` | **主窗口接班簡報**(sysadmin + 決策諮詢) | **新主窗口必讀** |
| `START_HERE.md` | 執行窗口 onboarding | 新執行窗口讀 |
| `context.md` | 硬體 / 使用情境 / D 槽完整結構 | 主規劃窗口必讀 |
| `decisions.md` | 已拍板的決策 + winget 安裝清單 | 重灌時逐項對照 |
| `PROGRESS_TEMPLATE.md` | 進度報告範本 | 任務結束時用 |

### 🎨 ComfyUI / 影像生成

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `comfyui/setup.md` | ComfyUI 完整實作現況、模型清單、踩坑 | 動 ComfyUI 前必讀 |
| `comfyui/workflows.md` | 已建立的 workflow 完整描述 | 要改 / 學現有 workflow |
| `comfyui/sageattention-patches.md` | 🚨 6 個 PyTorch patches 救命文件 | 升級 PyTorch / 重灌 / 重編 SageAttention 前 |
| `comfyui/huggingface-download-tricks.md` | xet bridge 繞過、Token 安全、curl 並行 | 下載 HF 模型卡住時 |

### 🤖 模型 / Agent

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `ai-models/local-models.md` | 本地模型分工(Ollama / ComfyUI / 雲端)、VRAM 限制 | 規劃 agent 後端時 |

### 🎬 創作 Pipeline

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `davinci/pipeline.md` | DaVinci + AI 整合架構規劃 | 開始做 creative-pipeline 時 |
| `davinci/media-structure.md` | D:\Media\ 資料夾結構與工作流 | 第一次開剪輯專案前 |

### 🛠️ 工具配置

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `openwebui/setup.md` | Open WebUI + LiteLLM 多模型介面(含 3 個踩坑) | 裝 Open WebUI 時 |
| `ldbot/checklist.md` | Ldbot 重灌前後備忘 | 重灌前 + Ldbot 重建時 |
| `reinstall-manifest.md` | 重灌清單自動產生系統 + 踩坑庫 | **全部裝完後執行一次** |
| `tools/README.md` | system-setup 周邊腳本工具清單(目前含 png_to_ico.py) | 寫新工具腳本前對照規範 |

### 💾 備份 / 災難還原

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `baseline-trigger.md` | 第一次 C 槽 baseline 映像觸發條件 + 完整步驟 | 何時做第一次系統映像 / 還原流程 |

---

## Repo 結構

```
system-setup/
├── *.md                              # 規劃文件(本索引列出)
├── *.patched                         # PyTorch patches 備份(救命用)
├── pip_freeze_*.txt                  # 環境快照
├── start_comfyui.bat                 # ComfyUI 啟動工具
├── generate-manifest.ps1             # 產生 manifest snapshot 的腳本
│
├── comfyui-workflows/                # ComfyUI workflow JSON
│   ├── SDXL_1.0_基準參考.json
│   ├── Klein_4B_快速草稿_4步.json
│   ├── Klein_4B_4K大圖出稿.json
│   ├── Klein_9B_Base_頂級定稿_20步.json
│   ├── flux2_klein_9b_t2i_official.json
│   ├── JoyCaption_Beta1_快速反推.json
│   └── JoyCaption_Beta1_訓練反推.json
│
├── tools/                            # 周邊腳本(Python 小工具)
│   ├── README.md                     # 工具清單 + 用法
│   └── png_to_ico.py                 # PNG → 多尺寸 ICO(內建亮度閾值去背)
│
└── sageattention_build_notes/
    └── BUILD_NOTES.md                # 9 次嘗試的完整失敗 / 解法紀錄
```

**不入 repo 的工作資產**(備份在 NAS):

- `assets/comfyui.ico` — ComfyUI 啟動捷徑圖示。重灌恢復步驟見 `reinstall-manifest.md`。

---

## 重灌前必做

1. **Ldbot**:`git push` + 備份 4 個 gitignored 檔案到 NAS(詳見 `ldbot/checklist.md`)
2. **system-setup repo**:確保所有改動已 commit + push
3. **SageAttention `.patched` 檔案**:確認都在 system-setup repo 內(救援用)
4. **D:\tmp\SageAttention\** source 整包 NAS 備份(以後重編需要)
5. **NAS 上的不入 repo 資產**確認還在(`assets/comfyui.ico` 等)
6. **其他工作資料夾**整包丟 NAS(清掉 `.venv/`、`__pycache__/`、`node_modules/`)

---

## 重灌實體資產(2026-04-26 製作)

| 資產 | 位置 | 用途 |
|---|---|---|
| **Win11 25H2 安裝 USB** | 抽屜 / 標籤明確 | 重灌作業系統(build 26200.6584) |
| **Hasleo Rescue USB** | 抽屜 / 標籤明確 | 緊急救援(已開機驗證) |
| **啟動驅動包** | `D:\Recovery\Drivers\2025-08-17_essential-bootstrap-drivers\` | 重灌後第一批驅動(網卡 / Wi-Fi / IRST / Armoury) |
| **Win11 25H2 ISO** | `D:\Recovery\Win11_25H2_*.iso` | 重做 USB 用 |

---

## 重灌後啟動順序

### Phase 1:基礎系統
1. Windows 11 乾淨安裝(從 USB)
2. NVIDIA Studio Driver(官網下載)
3. **Armoury Crate**(ASUS 官網,裝完清理背景服務)
4. `winget install Git.Git OpenJS.NodeJS.LTS`
5. `npm i -g @anthropic-ai/claude-code`

### Phase 2:Repo 進場
6. `git clone <system-setup repo>` 到 D:\Work\
7. 打開 Claude Code,讀 `START_HERE.md` + `decisions.md`,從 winget 批次清單開始

### Phase 3:重型工具
8. DaVinci Resolve Studio(`reinstall-manifest.md` 有踩坑紀錄)
9. ComfyUI portable(讀 `comfyui/setup.md`)
10. SageAttention 編譯(讀 `comfyui/sageattention-patches.md`,套用 6 個 patches)
11. Office 2021 + ODT 砍指定 app(`reinstall-manifest.md` 有 XML 範本)
12. Open WebUI + LiteLLM(讀 `openwebui/setup.md`)

### Phase 4:資料還原
13. 從 NAS 撈 Ldbot 4 個機敏檔
14. `D:\Models\` 整個從 NAS 復原(SD / Klein / JoyCaption 模型)
15. `D:\Cache\Resolve\Database\Local_D\` 從 NAS 復原(DaVinci 專案 Library)
16. `D:\Media\Assets\` 從 NAS 復原
17. **NAS 工作資產復原**:`assets/comfyui.ico` 等不入 repo 的檔案,套桌面捷徑(見 `reinstall-manifest.md`)

### Phase 5:驗證
18. 跑 `generate-manifest.ps1` 產新快照
19. 跟舊快照 diff 確認沒漏裝什麼
20. 各工具煙測(ComfyUI 跑 Klein 4B / DaVinci 開新專案 / Ldbot `uv run python main.py`)

---

**最後更新**:2026-04-27
