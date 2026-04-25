# SageAttention 3 Blackwell — 編譯與 Patches 完整紀錄

> **這份文件是救命文件**。SageAttention 3 編譯依賴 6 個必要 patches,任何 PyTorch 升級或 ComfyUI portable 重灌都會覆蓋它們,沒有這份文件你會花一整天重摸索。
>
> 編譯日期:**2026-04-25 晚**
> 編譯者:Wayne(本人,共 9 次嘗試)
> 編譯成果:Klein 9B Base 速度 50s → 41s(~17% 加速)

---

## 為什麼需要 SageAttention 3

- 標準的 PyTorch SDPA(Scaled Dot Product Attention)在 Blackwell 架構(sm_120)上不是最佳化的
- SageAttention 3 是 Blackwell 專用的 attention kernel
- 對 FLUX.2 Klein 9B Base 這類大模型推理,有可量測的 speedup
- **限制**:bf16 + FP4 path 有 CUDA misaligned address bug(SageAttention issue #357),所以 Klein 9B Base 走 bf16 只享受到部分加速

---

## 編譯前置條件

| 元件 | 版本 | 路徑 |
|---|---|---|
| Python | 3.13.12 embedded | `D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\` |
| PyTorch | 2.11.0+cu130 | site-packages |
| CUDA Toolkit | **13.2** | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2\` |
| Visual Studio | **2022 Build Tools 17.14.31** | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\` |
| CUDA Driver | 580.x | - |
| GPU | RTX 5090 Laptop(Blackwell sm_120, 24GB VRAM) | - |
| Source code | SageAttention 3 source | `D:\tmp\SageAttention\sageattention3_blackwell\` |

**注意**:
- VS Build Tools 必須勾選「**C++ Desktop workload**」(否則 nvcc 找不到 cl.exe)
- CUDA 13.2 必須在 VS Build Tools **之後**或**之前**裝都可以,但裝完要重啟讓 PATH 生效

---

## 6 個必要 Patches(全部都會被覆蓋!)

升級風險矩陣:

| # | 檔案 | 改動 | 升級風險 | source 是否保留 |
|---|---|---|---|---|
| 1 | `python_embeded\Lib\site-packages\torch\utils\cpp_extension.py:46` | `'oem'` → `'utf-8','replace'` | 🔴 PyTorch 升級會覆蓋 | N/A(改 site-packages) |
| 2 | `python_embeded\Lib\site-packages\torch\include\c10\cuda\CUDACachingAllocator.h:105` | `bool small` → `bool small_pool` | 🔴 PyTorch 升級會覆蓋 | N/A |
| 3 | `python_embeded\Include\` | 從標準 Python 3.13.13 複製 265 個標頭 | 🔴 ComfyUI portable 重灌會丟 | 標準 Python 仍在系統 |
| 4 | `python_embeded\libs\python313.lib` | 從標準 Python 3.13.13 複製 | 🔴 同上 | 標準 Python 仍在系統 |
| 5 | `D:\tmp\SageAttention\sageattention3_blackwell\setup.py` | nvcc_flags 加 `-Xcompiler /Zc:preprocessor` | 🟢 source 已存,重編 OK | ✅ 在 D:\tmp\ |
| 6 | `D:\tmp\SageAttention\sageattention3_blackwell\fp4_quantization_4d.cu` | 移除 `<torch/all.h>` | 🟢 source 已存,重編 OK | ✅ 在 D:\tmp\ |

**備份檔位置**(這些是已 patch 的檔案,救援時可直接複製):

```
D:\Work\system-setup\cpp_extension.py.patched
D:\Work\system-setup\CUDACachingAllocator.h.patched
```

(對應 patch #1 和 #2)

---

## Patch 詳解

### Patch #1:cpp_extension.py 的編碼問題

**檔案**:`python_embeded\Lib\site-packages\torch\utils\cpp_extension.py`
**行數**:46(可能因版本微調)

**問題**:中文 Windows 預設 cp950 / oem 編碼,nvcc 輸出含非 ASCII 字元時 PyTorch 解碼炸 UnicodeDecodeError。

**改動**:
```python
# 原本
encoding='oem'

# 改成
encoding='utf-8', errors='replace'
```

**未來如何驗證**:
```powershell
Select-String -Path "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Lib\site-packages\torch\utils\cpp_extension.py" -Pattern "encoding="
```
應該看到 `encoding='utf-8', errors='replace'`,不是 `encoding='oem'`。

---

### Patch #2:CUDACachingAllocator.h 變數命名衝突

**檔案**:`python_embeded\Lib\site-packages\torch\include\c10\cuda\CUDACachingAllocator.h`
**行數**:105 附近

**問題**:`small` 在某些編譯器(VS 2022 / cl.exe)是保留字或被 C++ runtime 預定義的 macro,導致編譯衝突。

**改動**:
```cpp
// 原本
bool small;

// 改成
bool small_pool;
```

**注意**:可能要連帶改該檔案內所有 `small` 的 reference(用 search & replace 全檔處理)。

---

### Patch #3:Python C 標頭缺失

**問題**:ComfyUI portable 的 `python_embeded\` **沒有 `Include/` 目錄**(節省體積),但編譯 C++ extension 一定要 Python.h 等 265 個標頭。

**解法**:從標準 Python 3.13.13 安裝(`C:\Python313\` 或類似)複製整個 `Include\` 進去:

```powershell
# 假設標準 Python 在 C:\Python313\
Copy-Item -Path "C:\Python313\include\*" -Destination "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Include\" -Recurse -Force
```

**驗證**:
```powershell
Test-Path "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Include\Python.h"
```
應該回 `True`。

---

### Patch #4:python313.lib 缺失

**問題**:同 #3,linker 階段需要 `python313.lib`,portable 沒有。

**解法**:
```powershell
Copy-Item -Path "C:\Python313\libs\python313.lib" -Destination "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\libs\" -Force
```

**驗證**:
```powershell
Test-Path "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\libs\python313.lib"
```

---

### Patch #5:setup.py 加 nvcc 旗標

**檔案**:`D:\tmp\SageAttention\sageattention3_blackwell\setup.py`

**問題**:VS 2022 預設用舊版 preprocessor,跟 CUDA 13.2 的某些 macro 衝突。

**改動**:在 `nvcc_flags` list 加:
```python
'-Xcompiler', '/Zc:preprocessor'
```

完整範例:
```python
nvcc_flags = [
    '-O3',
    '-std=c++17',
    # ... 原有旗標 ...
    '-Xcompiler', '/Zc:preprocessor',  # ← 新增
]
```

---

### Patch #6:移除 torch/all.h include

**檔案**:`D:\tmp\SageAttention\sageattention3_blackwell\fp4_quantization_4d.cu`

**問題**:`#include <torch/all.h>` 會引入太多 PyTorch 標頭,跟 CUDA kernel 編譯衝突,移除後只保留必要的 includes。

**改動**:刪除以下這行(或註解掉):
```cpp
#include <torch/all.h>
```

通常檔案頭部會這樣:
```cpp
// 原本:
#include <torch/all.h>
#include <cuda_runtime.h>
// ... 其他

// 改成:
// #include <torch/all.h>  ← 移除
#include <cuda_runtime.h>
// ... 其他
```

---

## 完整編譯流程(救命用,從零重建)

### Step 1:準備環境

```powershell
# 確認 CUDA 13.2
nvcc --version

# 確認 VS Build Tools
& "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

# 確認 ComfyUI 的 Python
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" --version
# 應該是 Python 3.13.12
```

### Step 2:套用 Patches #1-#4(modify ComfyUI 內部檔)

如果有 `.patched` 備份就直接複製:

```powershell
# Patch #1
Copy-Item "D:\Work\system-setup\cpp_extension.py.patched" `
          "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Lib\site-packages\torch\utils\cpp_extension.py" -Force

# Patch #2
Copy-Item "D:\Work\system-setup\CUDACachingAllocator.h.patched" `
          "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Lib\site-packages\torch\include\c10\cuda\CUDACachingAllocator.h" -Force

# Patch #3 + #4(從標準 Python 複製)
Copy-Item "C:\Python313\include\*" "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\Include\" -Recurse -Force
Copy-Item "C:\Python313\libs\python313.lib" "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\libs\" -Force
```

如果沒備份,請手動編輯(參考上面 patch 詳解)。

### Step 3:套用 Patches #5-#6(modify source code)

進入 source 目錄:

```powershell
cd D:\tmp\SageAttention\sageattention3_blackwell
```

手動編輯 `setup.py` 和 `fp4_quantization_4d.cu` 套用 patch #5、#6。

### Step 4:啟動 VS 編譯環境並編譯

```powershell
# 啟動 VS 編譯環境(必須在這個 shell 裡跑後續編譯)
& "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

cd D:\tmp\SageAttention\sageattention3_blackwell

# 用 ComfyUI 的 Python 編譯
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" setup.py install
```

**編譯時間**:約 15-30 分鐘(取決於 CPU)
**輸出**:成功訊息 + 安裝到 ComfyUI 的 site-packages

### Step 5:套用 ComfyUI shim

ComfyUI 內部用 `from sageattention import sageattn` 這個 v2 介面。
SageAttention 3 的 import name 是 `from sageattn3 import sageattn3_blackwell`。

需要建一個 shim 把 v2 介面導向 PyTorch SDPA(讓 ComfyUI 的 import 不報錯):

**檔案**:`python_embeded\Lib\site-packages\sageattention\__init__.py`

```python
# Shim: ComfyUI 期望 v2 sageattention 介面,我們轉發給 PyTorch SDPA
import torch
from torch.nn.functional import scaled_dot_product_attention as _sdpa

def sageattn(q, k, v, *args, **kwargs):
    """委派 v2 sageattn 給 PyTorch SDPA(因為 ComfyUI 沒直接用 sageattn3 API)"""
    return _sdpa(q, k, v)

__all__ = ['sageattn']
```

**驗證**:啟動 ComfyUI 不應出現 `ModuleNotFoundError: sageattention`。

### Step 6:啟動參數加 --use-sage-attention

編輯 `D:\Work\ComfyUI_portable\ComfyUI_windows_portable\run_nvidia_gpu.bat`,在啟動指令加:

```
--use-sage-attention
```

備份檔:`run_nvidia_gpu.bat.before_sageattention.bak`

### Step 7:驗證

啟動 ComfyUI,跑 Klein 9B Base 20 步 workflow,測試生成時間:

- **未開 sageattention**:~50 秒
- **開 sageattention**:~41 秒(~17% 加速)

---

## 已知問題

### bf16 + FP4 path bug(SageAttention issue #357)

- bf16 + FP4 path 有 CUDA misaligned address bug
- fp16 path **完全正常**
- Klein 9B Base 走 bf16 → 沒享受到 100% FP4 加速,只 ~17%
- 等 SageAttention 修復後重編可能可以再加速

### 升級風險

| 動作 | 影響 | 重做需求 |
|---|---|---|
| PyTorch 升級(`pip install torch -U`) | Patch #1, #2 被覆蓋 | 從 .patched 備份重套 |
| ComfyUI portable 整包重灌 | Patch #3, #4 全失效 | 從 C:\Python313 重新複製 |
| SageAttention 升級 | Patch #5, #6 失效但 source 仍在 | 重新編輯 source + 重編 |

**建議**:升級前先讀這份文件,做一份完整備份。

---

## 重編觸發時機

以下情況**需要重編 SageAttention**:

1. SageAttention 官方更新(可能修了 #357 bug)
2. PyTorch 大版本升級(2.11 → 2.12)
3. CUDA Toolkit 升級(13.2 → 13.3)
4. ComfyUI portable 整包升級(Python 從 3.13 → 3.14)

**不需要重編**:
- ComfyUI 本體升級(只動 ComfyUI\ 內部,不動 python_embeded\)
- Custom nodes 更新

---

## 補充紀錄

### 完整編譯筆記

`D:\Work\system-setup\sageattention_build_notes\BUILD_NOTES.md`(完整 9 次嘗試的失敗紀錄、錯誤訊息、解法,讀這個能完整還原當天的思路)

### Source 保留位置

`D:\tmp\SageAttention\`(233 MB,以後重編用,不要刪)

### pip freeze 快照

`D:\Work\system-setup\pip_freeze_before_sageattention.txt`(編譯前的 PyTorch 完整環境,救援時可比對)

---

**最後更新**:2026-04-26
