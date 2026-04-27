# HuggingFace 下載繞道技巧

> 下載 HF 模型時遇到的坑與解法。每條都是實戰打出來的。
>
> 最後更新:2026-04-26

---

## 為什麼需要這份文件

Hugging Face Hub 從 2024 開始導入 **xet bridge**(類似 Git LFS 替代品),某些 repo 強制走 xet,造成:
- `huggingface_hub` Python SDK 卡 0 byte
- 即使設 `HF_HUB_DISABLE_XET=1` + 啟用 `hf_transfer` 都無效
- 沒有清楚的錯誤訊息,只是「卡住不動」

Wayne 在下載 JoyCaption Beta1(15.81 GB)時踩到這個坑,反覆嘗試後找出 **curl 並行繞道**這條穩定路線。

---

## 坑 #1:xet bridge 卡 0 byte

### 症狀

```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="fancyfeast/llama-joycaption-beta-one-hf-llava")
```

進度條停在 0% 或 0 bytes,沒錯誤,沒進度。

### 原因

repo 的 LFS 檔案被遷移到 xet bridge,`huggingface_hub` 的某些版本 + 某些網路環境下無法走 xet 通道。

### 失敗的解法(別浪費時間)

以下都試過了,**沒用**:

```python
# 失敗 1:停用 xet
os.environ["HF_HUB_DISABLE_XET"] = "1"

# 失敗 2:啟用 hf_transfer
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

# 失敗 3:同時設兩個
# 失敗 4:更新 huggingface_hub 到最新版
# 失敗 5:用 hfdownloader CLI
```

某些 repo(如 `fancyfeast/*`)就是會卡。

### 解法:curl 4 路並行繞過

直接從 HF 的 raw URL 抓檔,**用 4 路並行**:

#### Step 1:取得檔案清單

到 repo 頁面看 Files 列表,記下所有要下載的檔名。例如 JoyCaption Beta1 的 4 個 shards:

```
model-00001-of-00004.safetensors
model-00002-of-00004.safetensors
model-00003-of-00004.safetensors
model-00004-of-00004.safetensors
```

加上其他必要檔:
```
config.json
generation_config.json
special_tokens_map.json
tokenizer.json
tokenizer_config.json
preprocessor_config.json
```

#### Step 2:組 URL

格式:
```
https://huggingface.co/<repo_id>/resolve/main/<filename>
```

範例:
```
https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava/resolve/main/model-00001-of-00004.safetensors
```

#### Step 3:用 curl 並行下載

PowerShell 範例(4 路並行):

```powershell
$base = "https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava/resolve/main"
$dest = "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\LLavacheckpoints\llama-joycaption-beta-one-hf-llava"

# 確保目錄存在
New-Item -ItemType Directory -Path $dest -Force

# 4 路並行(背景跑)
$jobs = @()
$jobs += Start-Job { 
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$using:dest\model-00001-of-00004.safetensors" "$using:base/model-00001-of-00004.safetensors"
}
$jobs += Start-Job { 
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$using:dest\model-00002-of-00004.safetensors" "$using:base/model-00002-of-00004.safetensors"
}
$jobs += Start-Job { 
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$using:dest\model-00003-of-00004.safetensors" "$using:base/model-00003-of-00004.safetensors"
}
$jobs += Start-Job { 
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$using:dest\model-00004-of-00004.safetensors" "$using:base/model-00004-of-00004.safetensors"
}

# 等所有 job 完成
$jobs | Wait-Job
$jobs | Receive-Job
$jobs | Remove-Job
```

#### Step 4:下載小檔(同步即可)

config 類小檔不需要並行:

```powershell
$smalls = @("config.json", "generation_config.json", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json", "preprocessor_config.json")

foreach ($file in $smalls) {
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$dest\$file" "$base/$file"
}
```

#### Step 5:驗證 SHA256

下載完一定要驗 hash,不然壞檔不會發現:

```powershell
# 從 HF 頁面複製官方 SHA256(每個檔有自己的)
$expected = @{
    "model-00001-of-00004.safetensors" = "abc123..."  # 改成官方值
    "model-00002-of-00004.safetensors" = "def456..."
    # ...
}

foreach ($file in $expected.Keys) {
    $actual = (Get-FileHash "$dest\$file" -Algorithm SHA256).Hash.ToLower()
    if ($actual -eq $expected[$file]) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file" -ForegroundColor Red
        Write-Host "   Expected: $($expected[$file])"
        Write-Host "   Actual:   $actual"
    }
}
```

### 實測速度

4 路並行,**穩定 11 MB/s** 下載速度(Wayne 家裡頻寬)。
15.81 GB 在 24-25 分鐘下完。

---

## 坑 #2:HF Token 安全

### 為什麼這條重要

Wayne 早期不小心把 HF Token 貼到 Claude Code 對話框裡,**Token 進了雲端對話歷史**,永久外洩。

雖然 Wayne 後來 revoke 重發了,但這是不可挽回的洩漏。**規則**:**Token 永遠不貼進任何 AI 對話**。

### 正確做法

#### 1. Token 只放環境變數

```powershell
# 在 PowerShell 設定(不用每次重設,持久化進 user env)
[Environment]::SetEnvironmentVariable('HF_TOKEN', 'hf_xxxxxxxxxxxxxxxx', 'User')

# 重開 PowerShell 驗證
echo $env:HF_TOKEN
```

#### 2. 啟動 Claude Code 時繼承

Token 在 PowerShell 環境變數裡 → 啟動 Claude Code:

```powershell
claude --dangerously-skip-permissions
```

子進程會繼承父進程的環境變數,**Claude Code 內部執行 curl 等指令時拿得到 $env:HF_TOKEN**,但 Token **不會出現在對話內容裡**。

#### 3. 寫腳本時的處理

```powershell
# ✅ 好:從環境變數讀
$token = $env:HF_TOKEN
curl.exe -H "Authorization: Bearer $token" ...

# ❌ 壞:寫死 Token(連 .ps1 檔都不要寫)
$token = "hf_xxxxxxxx"  # 這個 .ps1 一旦 commit 進 git 就完了
```

#### 4. .env 裡寫的話一定要 gitignore

如果用 `.env` 管:

```bash
# .env(不進 git)
HF_TOKEN=hf_xxxxxxxxxxxx
```

```bash
# .gitignore
.env
```

### NAS 加密備份

Token / API key 寫在 `.env` 後,把整個 `.env` 加密(用 7zip + 密碼)放 NAS。重灌後從 NAS 撈回來。

---

## 坑 #3:Gated Repo(每個都要分別點 Agree)

### 症狀

下載 BFL FLUX 系列 repo(`black-forest-labs/*`)時:

```
Error: 401 Unauthorized - Repository is gated
```

### 原因

某些 repo(尤其 FLUX、Llama 系列)需要使用者**到網頁同意 license** 才能下載。即使 Token 有效,沒同意過就不給下。

### 解法

#### 步驟

1. 用瀏覽器開 repo 頁面(例如 `https://huggingface.co/black-forest-labs/FLUX.1-dev`)
2. 用對應的 HF 帳號登入
3. 頁面會顯示 **Agree to license** 區塊
4. 填表(姓名、email、用途等),**送出**
5. 等幾秒,頁面會更新成「已同意」
6. **這個帳號的 Token 就能下這個 repo 了**

#### Wayne 用兩個 HF 帳號

- `yemwei` - 第一個帳號
- `Wayne0820` - 第二個帳號

**每個 repo 要分別在兩個帳號上同意一次**(如果你都會用兩個帳號下載)。

#### 加速技巧

每換一個 BFL repo,要重新點 Agree。可以**寫成清單**:

```
□ FLUX.1-dev
□ FLUX.1-schnell
□ FLUX.1-fill-dev
□ FLUX.1-Kontext-dev
□ FLUX.1-redux-dev
□ FLUX.2-Klein-4B
□ FLUX.2-Klein-9B-Base
□ FLUX.2-Klein-9B-Distilled
```

一次去網頁 batch 同意。

---

## 坑 #4:中文路徑 + PowerShell

### 症狀

```powershell
Get-ChildItem -Path "D:\Models\sd\checkpoints" -Filter "*.safetensors"
```

回**空結果**,但目錄裡明明有檔案。

### 原因

PowerShell 5 的 `Get-ChildItem -Filter` 在父路徑含中文時,某些 Windows 版本下 filter 會失效。

### 解法

#### 方案 A:用 cmd 替代

```powershell
cmd /c dir /b "D:\Models\sd\checkpoints\*.safetensors"
```

#### 方案 B:不用 -Filter,改用 Where-Object

```powershell
Get-ChildItem "D:\Models\sd\checkpoints" | Where-Object { $_.Name -like "*.safetensors" }
```

#### 方案 C:升 PowerShell 7

PS 7 沒這個 bug,winget 裝 `Microsoft.PowerShell` 即可。

---

## 完整下載流程範例(JoyCaption Beta1)

統整以上技巧,完整流程:

```powershell
# ===== 前置 =====
# 1. 確認環境變數
echo $env:HF_TOKEN

# 2. 確認目錄
$dest = "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\models\LLavacheckpoints\llama-joycaption-beta-one-hf-llava"
New-Item -ItemType Directory -Path $dest -Force

# 3. 確認瀏覽器已同意 license(如果是 gated)
# - 開 https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava
# - 確認 Agree 過

# ===== 下載大檔(4 路並行)=====
$base = "https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava/resolve/main"
$shards = @("model-00001-of-00004.safetensors", "model-00002-of-00004.safetensors", "model-00003-of-00004.safetensors", "model-00004-of-00004.safetensors")

$jobs = $shards | ForEach-Object {
    $shard = $_
    Start-Job {
        curl.exe -L -H "Authorization: Bearer $using:env:HF_TOKEN" `
            -o "$using:dest\$using:shard" "$using:base/$using:shard"
    }
}
$jobs | Wait-Job | Receive-Job
$jobs | Remove-Job

# ===== 下載小檔 =====
$smalls = @("config.json", "generation_config.json", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json", "preprocessor_config.json")
foreach ($file in $smalls) {
    curl.exe -L -H "Authorization: Bearer $env:HF_TOKEN" -o "$dest\$file" "$base/$file"
}

# ===== 驗證 =====
cmd /c dir /b "$dest\*.safetensors"
```

---

## 進階:當 curl 也失敗

如果 4 路 curl 還是慢或斷,試試:

### 方案 1:wget 多路並行

裝 wget(`winget install JernejSimoncic.Wget`),用 `-c` 續傳:

```powershell
wget -c -t 0 "$base/model-00001-of-00004.safetensors" -O "$dest\model-00001-of-00004.safetensors"
```

### 方案 2:aria2 多連線

裝 aria2(`winget install aria2.aria2`),單一檔多連線:

```powershell
aria2c -x 16 -s 16 -d $dest "$base/model-00001-of-00004.safetensors"
```

`-x 16 -s 16` = 16 個連線下載同一個檔。

### 方案 3:Cloudflare DNS

某些網路環境下 HF 解析不穩,改用 Cloudflare DNS:

```
1.1.1.1
1.0.0.1
```

設在路由器或 Windows 網路設定,可能改善速度。

---

## 待解問題

### xet bridge 何時修

HuggingFace 預計優化 xet 通道,但短期內 `fancyfeast/*` 等 repo 仍會卡。
持續觀察,如果 Python SDK 修好了,以後可以回去用 `snapshot_download`。

### LFS quota

HF 對未認證使用者有下載 quota 限制(每月 GB 數)。
登入 + Token 認證後 quota 大幅提升。重度下載建議買 PRO($9/月)。

---

## 相關文件

- `setup.md` — ComfyUI 模型清單(裡面提到的模型大多用本文技巧下載)
- `../ai-models/local-models.md` — 整體模型分工、HF Token 安全規則
- `decisions.md` — winget 套件清單(curl / wget / aria2)

---

**最後更新**:2026-04-26
