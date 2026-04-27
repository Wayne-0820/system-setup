# Baseline 映像觸發備忘錄

> 這份文件提醒**未來的 Wayne / Claude**:**何時** 該做第一次 C 槽 baseline 映像、**怎麼做**、**存哪**。
>
> 最後更新:2026-04-26

---

## 為什麼還沒做 baseline

2026-04-26 當天的決定:

C 槽當下狀態是「基礎工具裝完,但主要工作還沒開始」。
ComfyUI 工作流還在另一個 Claude 窗口處理中,CrewAI 環境(`D:\Work\creative-pipeline\`)還沒建。

**現在做 baseline = 不完整,以後還是要重做**。
**等完成做 baseline = 一次到位,真正可用**。

所以延後到「核心工作流跑通」再做。

---

## Baseline 觸發條件(全部達成才做)

- [ ] ComfyUI 中國 workflow 重建完成至少 3 個(目前已完成 1 個 JoyCaption Beta1)
- [ ] CrewAI 在 `D:\Work\creative-pipeline\` 建立完成,至少跑通**第一條 agent pipeline**(例如 Writer + Art Director 串接)
- [ ] DaVinci Resolve Studio 該裝的 plugin / preset 大致到位
- [ ] 系統設定基本定型,沒有明顯「等等還要裝 X」的待辦
- [ ] 各 secrets / API keys 在環境變數 + `.env` 都到位且工作正常

**這時候做 baseline = 真的「golden image」**。

---

## Baseline 執行步驟

### Step 1:準備

1. **插上 Hasleo Rescue USB**(2026-04-26 已製作驗證)
   - 標籤:HASLEO RESCUE USB / 2026-04-26 / Wayne ROG / WinPE x64
2. **確認 NAS 連線正常**
   - 測試指令:`Test-NetConnection -ComputerName [NAS-IP] -Port 445`
3. **關閉所有占用 C 槽的工作**
   - 結束 ComfyUI / Ollama / Open WebUI / DaVinci 等服務
   - 不要在備份過程中改檔案

### Step 2:預估容量

```powershell
Get-Volume -DriveLetter C | Select-Object DriveLetter, FileSystemLabel, @{Name="UsedGB";Expression={[math]::Round(($_.Size - $_.SizeRemaining)/1GB,2)}}, @{Name="FreeGB";Expression={[math]::Round($_.SizeRemaining/1GB,2)}}
```

Hasleo 用 LZ4 / Zstd 壓縮,**映像檔約已用空間的 50-70%**。

預估範例:
- C 槽已用 80 GB → 映像約 40-56 GB
- C 槽已用 150 GB → 映像約 75-105 GB

### Step 3:打開 Hasleo Backup Suite

主介面 → 選 **新建備份**。

### Step 4:選備份類型

| 類型 | 選 | 原因 |
|---|---|---|
| **系統備份** | ✅ **選這個** | 只備 C + 隱藏分割區,夠用 |
| 磁碟備份 | ❌ | 整顆 SSD,不必要 |
| 分割區備份 | ❌ | 太細不需要 |

**為什麼不備 D 槽**:

D 槽有別的保護機制:
- `D:\Sync-Wayne\` / `D:\Sync-Wife\` → Synology Drive 同步 NAS
- `D:\Models\` → 重新下載指南在 `comfyui/huggingface-download-tricks.md`
- `D:\Work\` 各 repo → GitHub 雙保險
- `D:\Media\` → 重要素材**手動定期同步 NAS**

如果有 D 槽特殊內容需要備(例如剪輯到一半的 DaVinci 專案),用「分割區備份」單獨處理該資料夾。

### Step 5:選目標位置(NAS)

#### 推薦的 NAS 路徑結構

```
\\[NAS-IP]\Backups\ASUS_ROG\
├── baseline_2026-XX-XX.img        # 完整 baseline
├── incremental_2026-XX-XX_a.img   # 增量備份 a
├── incremental_2026-XX-XX_b.img   # 增量備份 b
└── ...
```

#### 命名規範

- **Baseline**:`baseline_YYYY-MM-DD.img`(例:`baseline_2026-08-15.img`)
- **Incremental**:`incremental_YYYY-MM-DD_X.img`(X 是當月第幾次,a/b/c)

### Step 6:備份選項建議

| 選項 | 建議值 | 說明 |
|---|---|---|
| 壓縮等級 | **正常 / Normal** | 平衡速度與大小 |
| 加密 | **不加密**(NAS 已有保護) | 加密會慢很多,且 NAS 本身有權限管理 |
| 排程 | 手動 | baseline 不需要排程,改用 incremental 排程 |
| 完成後驗證 | ✅ **勾選** | 確保映像沒壞 |

### Step 7:執行 + 等待

**預估時間**:30-60 分鐘(視 C 槽大小 + 網路速度)

備份過程中可以:
- 不操作電腦(避免 C 槽被改)
- 去吃飯 / 看劇 / 休息
- 不要關螢幕(會睡眠中斷備份)→ 暫時改電源計畫「永不睡眠」

### Step 8:驗證映像可用

備份完成後,跑 Hasleo 內建的 **檢查映像** 功能:

主介面 → 工具 → 檢查映像 → 選剛備份的 .img → 執行

預期 `OK` 結果。

### Step 9:更新 reinstall-manifest.md

把這次 baseline 紀錄寫進 `D:\Work\system-setup\reinstall-manifest.md`:

```markdown
## Baseline 紀錄

| 日期 | 檔名 | 大小 | NAS 路徑 | 內容摘要 |
|---|---|---|---|---|
| 2026-XX-XX | baseline_2026-XX-XX.img | XX GB | \\NAS\Backups\ASUS_ROG\ | ComfyUI 工作流就緒 + CrewAI v1 |
```

### Step 10:commit + push

```powershell
cd D:\Work\system-setup
git add reinstall-manifest.md
git commit -m "docs: record baseline image YYYY-MM-DD"
git push
```

---

## Baseline 後的維護節奏

### Incremental(增量備份)

每次「重大改變」做一次:

- 裝完一批新工具(例如下完 100GB FLUX 系列模型)
- 跑通新 pipeline(例如 CrewAI 第二條 agent pipeline)
- 系統設定大改(例如換 GPU 驅動主版本)

每份 incremental 通常 2-10 GB,做起來快。

### 新 Baseline(每 3-6 個月)

當 incremental 累積太多 / 太大時:

- 做新 baseline 取代舊的
- 舊 baseline + 舊 incremental 全清掉(NAS 省空間)
- 寫新紀錄到 `reinstall-manifest.md`

---

## 緊急還原流程(萬一系統爆掉)

### 場景 A:Windows 還能開機,但有問題

1. 從 Windows 內打開 Hasleo Backup Suite
2. **瀏覽映像檔以進行還原**
3. 選對應的 baseline / incremental
4. 還原 → 重啟

### 場景 B:Windows 無法開機

1. 插 **Hasleo Rescue USB**(2026-04-26 製作那支)
2. 重啟 → Shift + 重新啟動 → 使用裝置 → 選 USB
3. 進入 WinPE Hasleo 環境
4. **瀏覽映像** → 連 NAS 取映像
   - 連 NAS 路徑:`\\[NAS-IP]\Backups\ASUS_ROG\`
   - 選 baseline 或 baseline + incrementals 還原到指定時間點
5. 還原 → 重啟 → 拔 USB → 進 Windows

---

## 相關文件

- `reinstall-manifest.md` — 完整重灌清單,baseline 紀錄寫這裡
- `comfyui/setup.md` — ComfyUI 配置(baseline 觸發條件之一)
- `comfyui/huggingface-download-tricks.md` — D 槽模型不備份的依據(可重下載)
- `davinci/media-structure.md` — D:\Media\ 結構,部分資料要手動同步 NAS

---

**最後更新**:2026-04-26
