# kohya SDXL LoRA 訓練 GUI

獨立 PySide6 桌面工具,包 kohya `sdxl_train_network.py`:填參數 → 按鈕跑訓練 → 即時 log/進度 → 可停。**跟 WCopilot 無關**(那是 ComfyUI sidebar;這是獨立視窗)。

## 安裝(一次性)

GUI 用 kohya 的 venv 跑(同一個 torch cu128 環境)。該 venv 是 **uv 建的、沒有 pip**,所以用 uv 裝 PySide6:

```
uv pip install --python "D:\Work\sd-scripts\.venv\Scripts\python.exe" PySide6
```

**不加進 kohya `requirements.txt`**(保訓練環境可重建、最小)。

## 跑

- 雙擊 `train_gui.bat`(無 console 視窗),或
- `D:\Work\sd-scripts\.venv\Scripts\python.exe train_gui.py`
- debug 看 traceback:`train_gui_debug.bat`(留 console)

## 欄位

**常駐**:底模 checkpoint(`.safetensors`)、資料集 root(內含 `img\<repeats>_<trigger>\`,例 `img\10_wnboy\`)、LoRA 名稱、dim / alpha / batch / epochs / learning rate / 解析度。

**進階**(折疊,帶 wnboy 驗證過的預設):optimizer(AdamW8bit)、scheduler(cosine)、unet_lr、text_encoder_lr、clip_skip、min_snr_gamma、save_every、seed、bucket(512-1536)。固定帶 `no_half_vae / sdpa / cache_latents / gradient_checkpointing / bf16`。

## 注意

- ⚠ 訓練吃滿 GPU,期間 ComfyUI 等 GPU 工作會卡到結束(單卡 5090)。
- **停止**用 `taskkill /T /F` 殺整個 `accelerate → python` tree —— 否則孤兒 `python.exe` 會繼續訓練鎖 VRAM。關視窗時若訓練中也會問是否停止。
- **訓練前驗證**:會擋下「底模不存在 / `img\` 缺 `<repeats>_<trigger>` 子夾(kohya 會 silent 訓 0 張) / 名稱含非法字元」。
- 訓練完 → 下方 dropdown 選 epoch → 「複製選定 epoch 到 loras」鈕複製到 `D:\Models\diffusion\loras\`(手動選,因最終 epoch 不一定最佳)。
- 上次填的值存 `train_gui_settings.json`(同目錄),下次自動還原。
- cp950 坑已內建處理:child 進程帶 `PYTHONUTF8=1`。

## 路徑(寫死在 train_gui.py 頂部常數,要改改那)

- kohya:`D:\Work\sd-scripts`(`accelerate.exe` + `sdxl_train_network.py`)
- 訓練資料:`D:\Work\lora-training\<name>\`(`img\` / `output\` / `log\`)
- LoRA 輸出:`D:\Models\diffusion\loras\`

完整訓練 SOP / 踩雷:`D:\Work\system-setup\comfyui\lora-training.md`。
