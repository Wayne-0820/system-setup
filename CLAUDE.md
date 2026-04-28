# CLAUDE.md (Project-level: system-setup)

> 你進 `D:\Work\system-setup\` 工作時讀本檔。
> 通用紀律(寫檔 SOP / config ASCII / secret / 雙驗證器 / STOP 觸發點 / 行為紀律)在 user-level CLAUDE.md(`C:\Users\Wayne\.claude\CLAUDE.md`);本檔只放 repo specific 補強。

---

## 這個 repo 是什麼

Wayne 機器的**真相來源**:系統決策、安裝 SOP、踩坑紀錄、模型分工、workflow 紀錄。

GitHub Public,最新 commit 在 origin/main。主窗口(web Claude)接班時讀完整文件,執行端(你)選擇性讀對應子目錄。

---

## Repo 結構

```
D:\Work\system-setup\
├── README.md / START_HERE.md / SYSADMIN_BRIEFING.md / PROGRESS_TEMPLATE.md
├── context.md / decisions.md / reinstall-manifest.md / baseline-trigger.md
├── CLAUDE.md            ← 你正在讀這份
├── progress-reports\    ← 你的 report 寫這(gitignored)
├── comfyui\             ← ComfyUI 設定 / workflow / 衝突管理
├── ai-models\           ← 模型分工
├── davinci\             ← DaVinci 整合
├── ldbot\               ← LDPlayer bot
├── openwebui\           ← Open WebUI + LiteLLM
└── tools\               ← 周邊腳本
```

完整文件索引:`SYSADMIN_BRIEFING.md` 「文件導航」段。

---

## 在這個 repo 的特定紀律

### 1. Reference 路徑用本地絕對路徑

讀文件用 `D:\Work\system-setup\<子目錄>\<檔名>`,**不繞 GitHub raw URL**(那是給遠端 web Claude 用的;你在本地讀 working tree 即時 latest,無 rate limit、無網路依賴)。

### 2. Progress report 落地(覆蓋 user-level 預設)

任務跑完寫到:

`D:\Work\system-setup\progress-reports\<YYYY-MM-DD>_<task-slug>.md`

按 `PROGRESS_TEMPLATE.md` 格式。該目錄已 gitignored,**不 commit**。Wayne 貼回主窗口整合進對應 MD,Wayne 自己刪 report 檔。

詳見 `progress-reports\README.md`。

### 3. 不直接動 repo 結構

rename / 子目錄重構 / 跨目錄大規模 refactor 沒主窗口拍板,**不擅自做**。

實證:本 repo 子目錄重構是主窗口規劃 + Wayne 拍板 + 派工後執行端執行,不是執行端自己想做就做。

---

**最後更新**:2026-04-28
**版本**:2.0(user-level 拆分後重寫)
