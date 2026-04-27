# Ldbot 重灌備忘(一頁版)

**核心事實**:Ldbot 核心已完成。影像比對**只依賴 LDPlayer 實例解析度**。帳號、實例名稱、ADB port、遊戲設定全部可隨時重建。

**Ldbot 路徑**:`D:\Work\Ldbot`(C 系統 / D 工作區策略)

---

## 重灌前(10 分鐘)

### 1. Git 狀態確認

```powershell
cd D:\Work\Ldbot
git status                      # 應顯示 "working tree clean"
git log origin/main..HEAD       # 應為空(無未推送)
git log HEAD..origin/main       # 應為空(無未拉取)
```

三個都乾淨 = GitHub 上就是最新版。

- [ ] `pyproject.toml` 與 `uv.lock` 在最新 commit 裡(uv 工作流,不再用 `requirements.txt`)
- [ ] `pyproject.toml` 的 `requires-python` 鎖在 `>=3.12,<3.13`(避免下次 uv 跟著系統 Python 升級)

### 2. 備份 gitignored 的 4 個關鍵檔案

這些在 `.gitignore` 裡,Git 不會帶,要手動備份:

```powershell
$backup = "D:\Ldbot-secrets"
New-Item -ItemType Directory -Path $backup -Force | Out-Null

Copy-Item "D:\Work\Ldbot\tools\admin_tool.py"           $backup
Copy-Item "D:\Work\Ldbot\accounts.yaml"                 $backup
Copy-Item "D:\Work\Ldbot\config.yaml"                   $backup
Copy-Item "D:\Work\Ldbot\config\user_settings.json"     $backup

Write-Host "備份完成 → $backup" -ForegroundColor Green
```

然後把 `D:\Ldbot-secrets\` 整包丟 NAS。

| 檔案 | 內容 |
|---|---|
| `admin_tool.py` | 含 Firebase 密鑰的管理工具 |
| `accounts.yaml` | 遊戲帳號密碼 |
| `config.yaml` | 解析度等關鍵設定 |
| `user_settings.json` | 使用者個人化設定 |

> **備註**:無 `.env` 檔,所以不用備份。

---

## 重灌後

```powershell
# 1. 基礎工具(decisions.md 裡會裝)
winget install Git.Git astral-sh.uv

# 2. Clone 到 D 槽
git clone <your-ldbot-url> D:\Work\Ldbot
cd D:\Work\Ldbot

# 3. 裝依賴(uv 會讀 pyproject.toml + uv.lock,自動建 .venv)
#    pyproject.toml 鎖了 requires-python >=3.12,<3.13,
#    uv 會自動下載 Python 3.12.x 到 ~\.local\share\uv\python\
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
uv run python main.py                                    # GUI 啟動 → 主環境 OK
uv run python tools\admin_tool.py list                   # CLI 列表 → tools/ 環境 OK
```

兩個都跑得起來即成功。

---

## Python 環境紀律 🚨

**Ldbot 鎖 Python 3.12.13(uv 管理),系統 Python 是 3.14.x(daily driver)。版本不一致 → 永遠走 `uv run`。**

### 規則

**Ldbot 內任何 Python 操作,一律用 `uv run`,不要打系統 `python`。**

| ✅ 正確 | ❌ 錯誤 |
|---|---|
| `uv run python main.py` | `python main.py` |
| `uv run python tools\admin_tool.py list` | `python tools\admin_tool.py list` |
| `uv run python tools\admin_tool.py add` | `python tools\admin_tool.py add` |
| `uv run pip list` | `pip list` |

### 為什麼

- **Ldbot 主環境是 Python 3.12.13**(uv 管的,在 `~\.local\share\uv\python\`)
- **系統 PATH 上的 `python` 是 3.14.x**(daily driver,見 `decisions.md`)
- 直接打 `python tools\xxx.py` → 系統 3.14 接到,**跟 Ldbot 主環境版本不一致**
- 簡單腳本(只用 stdlib)碰巧能跑 → 假象,**不代表整個 Ldbot 系統 OK**
- 哪天該腳本引入 Ldbot 主依賴(memory、ADB 操控庫、firebase 等)→ 系統 3.14 沒裝 → 炸

### 例外:**沒有例外**

不要因為「就一個小腳本」「reload 一下測試」就走系統 `python`。一致比方便重要。

---

## 踩坑紀錄

### 1. 依賴不完整(2026 早期 uv 遷移)

- 舊 `requirements.txt` 漏了 `easyocr`,`uv sync` 過、但 `uv run python main.py` 啟動即 `ModuleNotFoundError: easyocr`
- 已補進 `pyproject.toml` 並 commit
- **教訓**:遷移到 uv 時先把完整依賴裝好再跑 `uv lock`,不要相信舊的 `requirements.txt`

### 2. MS Store python.exe stub 攔截(2026-04-27)

- **症狀**:在 `D:\Work\Ldbot\` 打 `python tools\admin_tool.py add`,跳 Microsoft Store 廣告而不是執行腳本
- **原因**:Windows 11 預設在 `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\` 放兩個 0-byte 假 `python.exe` / `python3.exe`,系統 PATH 順序很前面,把所有 `python` 指令攔截到 Store 廣告頁
- **解法**(順序不能反):
  1. **先**關別名:Win+I → 應用程式 → 進階應用程式設定 → 應用程式執行別名 → 把 `python.exe` / `python3.exe` 兩個 toggle 關掉
  2. **再**裝真 Python:python.org 下對應版本(系統級用最新 stable),勾「Add python.exe to PATH」
  3. 驗證:**新開** PowerShell → `where.exe python` 第一行**不能是** WindowsApps
- **完整踩坑紀錄**:`reinstall-manifest.md` → 「Windows 基礎」段
- **長期解**:套用上方「Python 環境紀律」 — Ldbot 永遠走 `uv run`,根本不碰系統 `python`,連帶這個坑也踩不到
- **教訓**:即使解了系統 stub 攔截,**Ldbot 還是要走 uv** — 因為版本不一致才是真正的長期風險,stub 只是觸發點

---

## 為什麼這份這麼短

- 影像比對靠解析度,不需要備份 ADB port / 實例名
- 帳號可手動重登
- 實例照預設或照程式碼的值重建即可

**需要處理的就只有**:Git 最新狀態 + 4 個 gitignored 檔案的 NAS 備份 + Ldbot 走 `uv run` 紀律。

---

## 後續(重灌完一切都好之後)

- 裝 LDPlayer → `D:\Emulator\LDPlayer`
- 多開管理器建實例,**解析度照 config.yaml 設定**(唯一會影響運作的項目)
- 手動登入遊戲帳號
- 跑 Ldbot

---

**最後更新**:2026-04-27
