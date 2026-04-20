# 重灌 Manifest 系統

**目的**:所有工具與軟體裝完後,產出一份清單,**下次重灌看這份就能快速重建**(不含模型權重與專案程式碼,那些分別靠下載與 Git / NAS)。

---

## 設計理念

分兩部分:

1. **自動擷取**(PowerShell 腳本一鍵產生):winget 清單、npm 全域、VS Code 擴充、PowerShell $PROFILE、關鍵環境變數
2. **手動維護**:非 winget 軟體、應用內設定、API key 服務清單

兩部分都放 `D:\Recovery\`,一起推到 `system-setup` Git repo。

---

## 自動擷取腳本:`generate-manifest.ps1`

裝完所有軟體當天執行一次。之後每加新軟體重跑覆蓋。

```powershell
# D:\Recovery\generate-manifest.ps1
$ErrorActionPreference = "Stop"
$date = Get-Date -Format "yyyy-MM-dd"
$outRoot = "D:\Recovery"
$snapshot = Join-Path $outRoot "snapshot-$date"

New-Item -ItemType Directory -Path $snapshot -Force | Out-Null

Write-Host "=== 產生 Manifest 快照: $snapshot ===" -ForegroundColor Cyan

# 1. Winget(最重要,下次 winget import 就能還原)
Write-Host "[1/6] 匯出 winget 清單..."
winget export -o (Join-Path $snapshot "winget-apps.json") --include-versions

# 2. npm 全域套件
Write-Host "[2/6] 匯出 npm 全域..."
npm ls -g --depth=0 --json 2>$null | Out-File (Join-Path $snapshot "npm-global.json") -Encoding utf8

# 3. VS Code 擴充
Write-Host "[3/6] 匯出 VS Code 擴充..."
if (Get-Command code -ErrorAction SilentlyContinue) {
    code --list-extensions | Out-File (Join-Path $snapshot "vscode-extensions.txt") -Encoding utf8
}

# 4. PowerShell Profile
Write-Host "[4/6] 備份 PowerShell Profile..."
if (Test-Path $PROFILE) {
    Copy-Item $PROFILE (Join-Path $snapshot "PROFILE.ps1")
}

# 5. 關鍵環境變數(API keys 只記是否有設,不記值)
Write-Host "[5/6] 擷取環境變數..."
$envKeys = @(
    'OLLAMA_MODELS',
    'RESOLVE_SCRIPT_API',
    'RESOLVE_SCRIPT_LIB',
    'PYTHONPATH',
    'ANTHROPIC_API_KEY',
    'ELEVENLABS_API_KEY'
)
$envSnapshot = @{}
foreach ($k in $envKeys) {
    $v = [Environment]::GetEnvironmentVariable($k, 'User')
    if ($v) {
        if ($k -match 'KEY') {
            $envSnapshot[$k] = "[SET — 值不記錄]"
        } else {
            $envSnapshot[$k] = $v
        }
    }
}
$envSnapshot | ConvertTo-Json | Out-File (Join-Path $snapshot "env-vars.json") -Encoding utf8

# 6. 所有已安裝程式(含非 winget)
Write-Host "[6/6] 列出所有已安裝程式..."
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
    Where-Object { $_.DisplayName } |
    Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
    Sort-Object DisplayName |
    Export-Csv (Join-Path $snapshot "installed-programs.csv") -NoTypeInformation -Encoding UTF8

Write-Host "`n完成 → $snapshot" -ForegroundColor Green
Write-Host "記得檢查 manual-installs.md 是否需要更新" -ForegroundColor Yellow
```

---

## 手動維護:`manual-installs.md`

一邊裝一邊更新。模板:

```markdown
# 手動安裝清單(非 winget)

> 最後更新:YYYY-MM-DD

## 核心軟體

| 軟體 | 版本 | 下載來源 | 安裝位置 | 關鍵設定 |
|---|---|---|---|---|
| NVIDIA Studio Driver | 5xx.xx | nvidia.com | C | 乾淨安裝 |
| Office 2021 企業增強版 | LTSC | NAS:\\xxx\office | C | 停用所有背景啟動 |
| DaVinci Resolve Studio | 20.x | blackmagicdesign.com | C | Database/Cache/Gallery → D:\Cache\Resolve;RESOLVE_SCRIPT_API / LIB 環境變數 |
| LDPlayer | 9.x | ldplayer.net | D:\Emulator\LDPlayer | 實例解析度要對齊 Ldbot config |
| Synology Drive Client | x.x | synology.com | C | 同步目標 D:\Sync |
| ComfyUI portable | 最新 7z | github.com/comfyanonymous | D:\Work\ComfyUI_portable | extra_model_paths.yaml 指 D:\Models\sd |
| Stable Diffusion Forge(若裝) | git | github.com/lllyasviel | D:\Work\Forge | 模型目錄 D:\Models\sd |

## API 服務(要重新登入 / 拿 key)

| 服務 | 用途 | 登入網址 | 環境變數名 |
|---|---|---|---|
| Anthropic | Claude API / Claude Code | console.anthropic.com | ANTHROPIC_API_KEY |
| ElevenLabs | TTS | elevenlabs.io | ELEVENLABS_API_KEY |
| Kling / Runway(選) | 影片生成 | ... | ... |
| Suno(選) | 配樂 | ... | ... |
| GitHub | Git 推拉 | github.com | (gh auth login) |

## 瀏覽器 / 通訊要登入

- Chrome / Edge(雲端同步)
- Discord、Line、TeamViewer(winget 有,要重登)
- Steam(winget 有,要重登)

## 環境變數清單

- [ ] OLLAMA_MODELS = D:\Models\ollama
- [ ] RESOLVE_SCRIPT_API = (DaVinci 安裝後的路徑)
- [ ] RESOLVE_SCRIPT_LIB = (fusionscript.dll 路徑)
- [ ] LM Studio 模型目錄 → D:\Models\lmstudio(GUI 設)
- [ ] ComfyUI extra_model_paths.yaml → D:\Models\sd
```

---

## 下次重灌的還原流程

假設已把 `system-setup` repo clone 到新系統:

```powershell
# 1. 依 decisions.md 手動裝 NVIDIA 驅動、Git、Node

# 2. 還原 winget 套件
winget import D:\Recovery\snapshot-YYYY-MM-DD\winget-apps.json --accept-source-agreements --accept-package-agreements

# 3. 還原 npm 全域(對照 npm-global.json 手動 npm i -g)

# 4. 還原 VS Code 擴充
Get-Content D:\Recovery\snapshot-YYYY-MM-DD\vscode-extensions.txt | ForEach-Object {
    code --install-extension $_
}

# 5. 還原 PowerShell Profile
Copy-Item D:\Recovery\snapshot-YYYY-MM-DD\PROFILE.ps1 $PROFILE

# 6. 環境變數:對照 env-vars.json 設定(API keys 手動貼)

# 7. 手動安裝部分:照 manual-installs.md 打勾
```

---

## 維護節奏

- **裝新軟體當天**:更新 `manual-installs.md`(若非 winget)
- **每週一次**:跑 `generate-manifest.ps1` 覆蓋舊 snapshot
- **每月一次**:snapshot + manual-installs.md commit push 到 GitHub
- **下次重灌前**:最後跑一次,確認最新狀態

---

## 刻意不進 Manifest

這些走別的路徑:

- **本地模型**(Ollama / SD checkpoints):太大,重灌後重下
- **專案程式碼**:Git / NAS
- **API keys**:安全考量,只記服務清單,值手動輸入
- **DaVinci 專案 / 素材**:`D:\Media\` 與 NAS
- **`.env` 檔**:NAS 整包備份
