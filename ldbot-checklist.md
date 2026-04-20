# Ldbot 重灌備忘(一頁版)

**核心事實**:Ldbot 核心已完成。影像比對**只依賴 LDPlayer 實例解析度**。帳號、實例名稱、ADB port、遊戲設定全部可隨時重建。

**舊系統路徑**:`C:\Users\Wayne\Ldbot`
**新系統路徑**:`D:\Work\Ldbot`(符合 C 系統 / D 工作區策略)

---

## 重灌前(10 分鐘)

### 1. Git 狀態確認

```powershell
cd C:\Users\Wayne\Ldbot
git status                      # 應顯示 "working tree clean"
git log origin/main..HEAD       # 應為空(無未推送)
git log HEAD..origin/main       # 應為空(無未拉取)
```

三個都乾淨 = GitHub 上就是最新版。

- [ ] `pyproject.toml` 與 `uv.lock` 在最新 commit 裡(uv 工作流,不再用 `requirements.txt`)

### 2. 備份 gitignored 的 4 個關鍵檔案

這些在 `.gitignore` 裡,Git 不會帶,要手動備份:

```powershell
$backup = "D:\Ldbot-secrets"
New-Item -ItemType Directory -Path $backup -Force | Out-Null

Copy-Item "C:\Users\Wayne\Ldbot\tools\admin_tool.py" $backup
Copy-Item "C:\Users\Wayne\Ldbot\accounts.yaml" $backup
Copy-Item "C:\Users\Wayne\Ldbot\config.yaml" $backup
Copy-Item "C:\Users\Wayne\Ldbot\config\user_settings.json" $backup

Write-Host "備份完成 → $backup" -ForegroundColor Green
```

然後把 `D:\Ldbot-secrets\` 整包丟 NAS。

| 檔案 | 內容 |
|---|---|
| `admin_tool.py` | 含 Firebase 密鑰的管理工具 |
| `accounts.yaml` | 遊戲帳號密碼 |
| `config.yaml` | 解析度等關鍵設定 |
| `user_settings.json` | 使用者個人化設定 |

> **備註**:舊系統無 `.env` 檔,所以不用備份。

---

## 重灌後

```powershell
# 1. 基礎工具(decisions.md 裡會裝)
winget install Git.Git astral-sh.uv

# 2. Clone 到 D 槽新位置
git clone <your-ldbot-url> D:\Work\Ldbot
cd D:\Work\Ldbot

# 3. 裝依賴(uv 會讀 pyproject.toml + uv.lock,自動建 .venv)
uv sync
```

### 4. 還原 4 個 gitignored 檔案(從 NAS 撈 Ldbot-secrets 回 D:\)

| 檔案 | 還原位置 |
|---|---|
| `admin_tool.py` | `D:\Work\Ldbot\tools\admin_tool.py` |
| `accounts.yaml` | `D:\Work\Ldbot\accounts.yaml`(根目錄) |
| `config.yaml` | `D:\Work\Ldbot\config.yaml`(根目錄) |
| `user_settings.json` | `D:\Work\Ldbot\config\user_settings.json` |

```powershell
Copy-Item "D:\Ldbot-secrets\admin_tool.py"       "D:\Work\Ldbot\tools\"
Copy-Item "D:\Ldbot-secrets\accounts.yaml"       "D:\Work\Ldbot\"
Copy-Item "D:\Ldbot-secrets\config.yaml"         "D:\Work\Ldbot\"
Copy-Item "D:\Ldbot-secrets\user_settings.json"  "D:\Work\Ldbot\config\"
```

### 5. 驗證

```powershell
uv run python main.py
```

能啟動 GUI 即成功。

### 6. 後續

- 裝 LDPlayer → `D:\Emulator\LDPlayer`
- 多開管理器建實例,**解析度照 config.yaml 設定**(唯一會影響運作的項目)
- 手動登入遊戲帳號
- 跑 Ldbot

---

## 踩坑紀錄

### 依賴不完整(2026 重灌)

- 舊 `requirements.txt` 漏了 `easyocr`,`uv sync` 過、但 `uv run python main.py` 啟動即 `ModuleNotFoundError: easyocr`
- 已補進 `pyproject.toml` 並 commit(`6fea5fc` → 後續 commit)
- 教訓:遷移到 uv 時先把完整依賴裝好再跑 `uv lock`,不要相信舊的 `requirements.txt`

---

## 為什麼這份這麼短

- 影像比對靠解析度,不需要備份 ADB port / 實例名
- 帳號可手動重登
- 實例照預設或照程式碼的值重建即可

**需要處理的就只有**:Git 最新狀態 + 4 個 gitignored 檔案的 NAS 備份。
