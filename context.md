# Context — 系統脈絡與規劃

> 給 Claude / Claude Code 的單一真相來源。第一次對話時讀這份。
> 最後更新:2026-05-04

---

## 硬體 / 磁碟策略 / 端口配置

詳見 `SYSADMIN_BRIEFING.md`「系統當前狀態」段(硬體規格 / 端口分配 / 環境變數)+「路徑架構規範」段(D 槽完整結構 / LLM 類模型寫死路徑例外)。

**24GB VRAM 是所有 AI 決策的天花板** — 同時跑大模型會爆,二選一。

---

## 使用情境優先序(高到低)

1. **AI 影像生產 pipeline**(主軸):Claude Code + CrewAI 編排,DaVinci Studio 組裝,ComfyUI(Klein / FLUX) + FramePack 生成影片。詳見 `davinci/pipeline.md`、`comfyui/setup.md`
2. **Ldbot 收尾維護**:核心已完成,偶爾修 bug。詳見 `ldbot/checklist.md`
3. **DaVinci 一般剪輯**(非 AI 流程)
4. 一般生產力:Office、瀏覽器、通訊
5. 休閒娛樂:Steam 遊戲 / 獨立遊戲(裝 D 槽)

---

## 已完成的階段

### 系統建置(2026-04-19/20 重灌)
- Windows 11 Pro + 全驅動 + Armoury Crate
- 開發工具:Git / Node / uv / Claude Code / VS Code / PowerToys 等
- DaVinci Resolve Studio 20(Working Folders 全 D 槽,Default Preset 已存)
- LDPlayer 9
- Synology Drive(Wayne + Wife 雙任務)
- Office 2021 精簡(砍 Outlook / Publisher / Access / Teams / OneDrive / Groove / Lync)
- Ollama + qwen3:32b
- ComfyUI portable + Manager
- Open WebUI + LiteLLM(三個踩坑文件化)

### ComfyUI 工程(2026-04-25/26)
- CUDA Toolkit 13.2 + Visual Studio 2022 Build Tools 安裝
- SageAttention 3 Blackwell 編譯成功(9 次嘗試,6 個 patches)
- Klein 系列模型完整下載(4B / 9B distilled / 9B Base + 對應 Qwen3 CLIP)
- JoyCaption Beta1 下載(15.81 GB)
- 5 個 workflow 中文命名建立完成
- 4K 升頻流程驗證(Klein 9B Base + UltraSharp = 20.9 GB VRAM 極限)

---

## 待推進階段

### 短期
1. Hasleo Rescue USB + 第一次 System Backup(golden image)
2. ComfyUI 啟動圖示底圖生成 + 桌面捷徑
3. 開始重建中國 workflow(Flux-fill / Qwen3 TTS / Kontext + ControlNet 三選一)

### 中期
1. SageAttention issue #357 修復後重編,享受完整 FP4 加速
2. 下載 FLUX.1 Fill / Kontext / Qwen-Image-Edit / Qwen3 TTS / Whisper / Wan 2.2 系列(約 100-150 GB)
3. 建 `D:\Work\creative-pipeline\` 跑 CrewAI

### 長期
1. CrewAI agent 編排:Writer(Sonnet API)→ Art Director → ComfyUI / FramePack / Voice → DaVinci 組裝
2. 完整 AI 影像 pipeline 跑通

---

## 文件導航

詳見 `README.md`。每份文件用途、何時讀:

- 通用先讀:`context.md`(本文件) + `decisions.md`
- 新對話 onboarding:`START_HERE.md`(精簡版,給執行窗口讀)
- 任務結束時:用 `PROGRESS_TEMPLATE.md` 格式產進度報告

---

**最後更新**:2026-05-04
