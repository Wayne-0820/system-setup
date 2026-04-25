# SageAttention 3 Blackwell Build Notes

**編譯日期**: 2026-04-25
**環境**:
- Windows 11
- ComfyUI portable 0.19.3 (D:\Work\ComfyUI_portable\)
- Python 3.13.12 embedded
- PyTorch 2.11.0+cu130
- CUDA Toolkit 13.2
- VS 2022 Build Tools 17.14.31
- RTX 5090 Laptop (sm_120, Blackwell)

## 6 個 Patches(Wayne 必讀,以後升級會丟)

### 1. PyTorch cpp_extension.py utf-8 codec
**檔案**: `python_embeded\Lib\site-packages\torch\utils\cpp_extension.py:46`
**改動**: 'oem' → 'utf-8','replace'
**原因**: vcvarsall 改 chcp 導致 oem codec 失效
**升級風險**: PyTorch 升級會覆蓋,要重新 patch

### 2. PyTorch CUDACachingAllocator small 變數
**檔案**: `python_embeded\Lib\site-packages\torch\include\c10\cuda\CUDACachingAllocator.h:105`
**改動**: bool small → bool small_pool  
**原因**: Windows SDK <rpcndr.h> #define small char 巨集汙染
**升級風險**: PyTorch 升級會覆蓋

### 3. Embedded Python headers
**檔案**: `python_embeded\Include\` (265 files)
**動作**: 從標準 Python 3.13.13 複製
**原因**: embedded Python 沒開發標頭
**升級風險**: ComfyUI portable 重灌會丟,但 Python 版本不換就不用重做

### 4. Embedded Python import library
**檔案**: `python_embeded\libs\python313.lib`
**動作**: 從標準 Python 3.13.13 複製
**升級風險**: 同上

### 5. SageAttention setup.py 新前處理器 flag
**檔案**: `D:\tmp\SageAttention\sageattention3_blackwell\setup.py` nvcc_flags
**加入**: `-Xcompiler /Zc:preprocessor`
**原因**: CCCL 要求新式前處理器
**位置**: 編譯時設定,已生效不用維護

### 6. fp4_quantization_4d.cu 移除 torch/all.h
**檔案**: `D:\tmp\SageAttention\sageattention3_blackwell\fp4_quantization_4d.cu`
**改動**: 移除 `<torch/all.h>` include
**原因**: 觸發 compiled_autograd.h std namespace 二義性 (issue #348)
**位置**: 編譯時設定,已生效不用維護

## 已知 Runtime Bug

### bf16 + FP4 path: CUDA misaligned address (issue #357)
- 影響: sageattn3 kernel 跑 bf16 input 會 crash
- 解法: ComfyUI 用 fp16 / fp8 路徑,不要強制 bf16
- 等 SageAttention 上游修復

## 正確 import 名稱

```python
from sageattn3 import sageattn3_blackwell
```

不是 `from sageattention import sageattn`。

## 啟用方式

ComfyUI 啟動加 `--use-sage-attention` 參數。
