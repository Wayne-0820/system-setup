# D:\Media 資料夾結構說明

> 這是 DaVinci Resolve 剪輯素材與 AI 生成素材的統一存放位置。
> 不含 DaVinci 內部系統檔案(Database / Cache / Proxy / Gallery → 在 D:\Cache\Resolve\)。

---

## 結構總覽

```
D:\Media\
├── AI_Raw\           AI 生成的原始池(未分類、還沒進專案的素材)
│   ├── ComfyUI_Output\        ComfyUI 產的圖片、動圖
│   ├── FramePack_Output\      FramePack 產的首尾幀影片段
│   ├── Voice_Output\          ElevenLabs / F5-TTS 合成配音
│   └── Music_Output\          Suno / Udio 生成配樂
│
├── Archive\          已結案封存的專案(定期搬 NAS 備份)
│
├── Assets\           跨專案共用資源(一次取得,反覆使用)
│   ├── Fonts\                 授權字體
│   ├── Logos\                 常用 logo、浮水印
│   ├── LUTs\                  調色 LUT(.cube / .3dl)
│   ├── Music\                 授權音樂、無版權音樂庫
│   └── SFX\                   音效庫(轉場音、環境音等)
│
└── Projects\         當前進行中的剪輯專案
    └── YYYY-MM_ProjectName\   每個專案一個資料夾,以日期+名稱命名
        ├── AI_Generated\      這個專案挑選進來的 AI 素材(從 AI_Raw 搬過來)
        ├── Audio\             原始錄音、旁白、單獨配樂
        ├── Exports\           DaVinci Deliver 輸出的成品
        ├── Footage\           原始影片素材(拍攝 / 下載)
        └── Graphics\          字卡、Logo、PNG、圖形元素
```

---

## 四大資料夾定位

### Projects(正在剪的)

- **誰會動**:DaVinci Resolve 匯入素材時指向這裡
- **命名規則**:`YYYY-MM_ProjectName`
  - 例:`2026-04_TravelVlog`、`2026-05_ClientAd`
  - 日期前綴幫你區分「這是什麼時候做的」,不是為了排序
- **子結構**:每個專案固定 5 個資料夾(Footage / Audio / Graphics / AI_Generated / Exports)
- **重要**:專案開始後,**素材路徑不要亂搬**,DaVinci 會找不到

### Assets(反覆用的資源)

- **誰會動**:你買了音樂、下載了 LUT、找到好字體,就丟這裡
- **性質**:跨專案共用,不屬於任何單一專案
- **備份優先度**:最高。這些是你累積的資產,消失了要重新買 / 找很麻煩
- **注意**:購買的音樂 / LUT 有授權憑證,單獨存到 NAS 或 `D:\Licenses\`

### AI_Raw(AI 產的原始池)

- **誰會動**:ComfyUI、FramePack、ElevenLabs、Suno 等工具的預設輸出路徑
- **性質**:暫存。AI 生成通常會產一堆草稿,先都丟這裡
- **處理流程**:
  1. AI 工具產出 → 自動存到對應子資料夾
  2. 你挑選要用的 → 搬到 `Projects\[專案名]\AI_Generated\`
  3. 定期清理沒用到的草稿(AI 生成可重跑,不捨得佔空間才佔)
- **不備份**:這裡是垃圾桶前站,選用的會進專案,其他該砍

### Archive(結案封存)

- **誰會動**:專案完成後,你手動從 Projects 搬過來
- **搬遷時機**:影片發佈後 1-2 個月確認不改了
- **搬遷內容**:整個專案資料夾(含成品、原始素材、DaVinci 匯出的專案檔)
- **備份**:定期(每月?)同步 NAS,雙重保險

---

## 實戰工作流範例

### 建新專案(以「旅遊 vlog」為例)

```powershell
# 1. 建專案資料夾
$project = "D:\Media\Projects\2026-04_TravelVlog"
New-Item -ItemType Directory -Path "$project\Footage" -Force
New-Item -ItemType Directory -Path "$project\Audio" -Force
New-Item -ItemType Directory -Path "$project\Graphics" -Force
New-Item -ItemType Directory -Path "$project\AI_Generated" -Force
New-Item -ItemType Directory -Path "$project\Exports" -Force

# 2. 丟原始素材到 Footage\
# 3. DaVinci 新專案 → Media Pool 匯入 Footage\
# 4. 剪接 / 調色 / 輸出到 Exports\
```

### AI 素材進專案(從 AI_Raw 挑)

```
假設 ComfyUI 今天產了 30 張圖(存在 AI_Raw\ComfyUI_Output\),
只有 5 張會用到這個專案:

[挑選 5 張] → 搬到 D:\Media\Projects\2026-04_TravelVlog\AI_Generated\
[其他 25 張] → 留在 AI_Raw 等看要不要用,或直接砍
```

### 結案歸檔

```powershell
# 影片發佈 2 個月後,確認不改了
Move-Item "D:\Media\Projects\2026-04_TravelVlog" "D:\Media\Archive\"
```

---

## DaVinci Resolve 對應設定

這些在 DaVinci 的 Project Settings → Working Folders 已經設好:

| 項目 | 路徑 | 說明 |
|---|---|---|
| Project media location | `D:\Media` | DaVinci 匯入素材時的預設起點 |
| Proxy generation location | `D:\Cache\Resolve\ProxyMedia` | Proxy 檔,不在 Media |
| Cache files location | `D:\Cache\Resolve\Cache` | 預覽快取,不在 Media |
| Gallery stills location | `D:\Cache\Resolve\Gallery` | Still 截圖,不在 Media |

**記住**:素材和快取分開放。Media 是你的資產(要備份),Cache 是可重建的(不用備份)。

---

## 備份策略對照

| 資料夾 | 備份頻率 | 備份方式 |
|---|---|---|
| Projects(進行中) | 每週 | Synology Drive 同步 / 手動複製 |
| Assets | 變更時立即 | NAS(最重要,不能遺失) |
| AI_Raw | 不備份 | 短期暫存,定期清理 |
| Archive | 每月 | NAS 整包同步 |

---

## 常見問題

### Q: 為什麼不用數字前綴(01_、02_)?

早期剪輯工作室為了在 Finder/Explorer 強制排序才用數字。你一個人用、Windows 11 可以釘選資料夾,數字是多餘的噪音。

### Q: 專案資料夾那 5 個子資料夾(Footage/Audio/Graphics/AI_Generated/Exports)必須都建嗎?

是。即使某個專案沒用到 AI_Generated,保留空資料夾讓結構一致。下次找東西不用想「這次是哪套規則」。

### Q: AI_Raw 會不會爆掉?

會。設個習慣:每月 15 號檢查一次,沒進專案的超過 1 個月就砍。AI 生成可以重跑,不要心疼。

### Q: 專案結案後多久搬 Archive?

建議 1-2 個月。確保真的沒客戶要改、沒想補內容。搬到 Archive 後就當「冰起來」,不再碰。

---

**最後更新**:2026-04-20
