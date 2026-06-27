# 角色 LoRA 訓練 SOP(SDXL / Illustrious)

從 1 張參考圖到一個可用角色 LoRA,在 Wayne 機器端到端跑通的流程 + 踩雷。
生圖/篩/打標工具鏈在 `D:\Work\system-setup\tools\lora-pipeline\`(config 驅動,見該夾 README)。

> 實證:`wnboy` LoRA(底模 WAI-Illustrious-SDXL v170)2026-06-27 端到端跑通,身份穩 + generalize 到沒訓過的場景。

---

## 全流程(6 步)

1. **生圖** — `sdxl_bootstrap.py`(IPAdapter 從 1 張擴 ~64 張)或 `flux_kontext.py`(Kontext in-context 保身份)。
2. **篩** — `make_contactsheet.py` 組帶編號聯絡表 → 挑 ~25-30 張一致 + 多樣(全身/半身/特寫/側臉/動作/換裝)。
3. **資料集結構** — 複製到 `<root>\img\<repeats>_<trigger>\`(例 `D:\Work\lora-training\wnboy\img\10_wnboy\`,`10_` = 每張 repeat 10 次)。
4. **打標** — `tag_wd14.py`(WD14 → Danbooru 標籤 + 加 trigger + strip 身份外觀標籤),每張寫同名 `.txt`。
5. **訓練** — kohya sd-scripts(見下)。
6. **測** — ComfyUI LoraLoader 逐 epoch 測,挑「身份穩 + 場景可控(generalize)」的。

---

## kohya 安裝(RTX 5090 / Blackwell)

```
git clone --depth 1 https://github.com/kohya-ss/sd-scripts.git D:\Work\sd-scripts
uv venv --python 3.11 D:\Work\sd-scripts\.venv
cd D:\Work\sd-scripts
uv pip install --python .venv\Scripts\python.exe torch torchvision --index-url https://download.pytorch.org/whl/cu128
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

**關鍵**:Blackwell(sm_120)必須用 **torch cu128**(`whl/cu128`),否則 CUDA kernel 不支援、訓練炸。實測 torch 2.11+cu128 第一次就成,獨立 venv 零污染 ComfyUI。

---

## 訓練指令(SDXL 角色 LoRA,驗證過的 args)

**先 `$env:PYTHONUTF8="1"`**(見踩雷 1),再:

```
accelerate launch --num_processes=1 --mixed_precision=bf16 --dynamo_backend=no sdxl_train_network.py
  --pretrained_model_name_or_path=<底模 .safetensors>
  --train_data_dir=<root>\img  --output_dir=<root>\output  --output_name=<name>  --logging_dir=<root>\log
  --network_module=networks.lora  --network_dim=32  --network_alpha=16
  --resolution=1024,1024  --enable_bucket --min_bucket_reso=512 --max_bucket_reso=1536 --bucket_no_upscale
  --train_batch_size=2  --max_train_epochs=10  --save_every_n_epochs=1  --save_model_as=safetensors
  --learning_rate=1e-4 --unet_lr=1e-4 --text_encoder_lr=5e-5  --optimizer_type=AdamW8bit
  --lr_scheduler=cosine  --mixed_precision=bf16 --save_precision=bf16
  --sdpa --gradient_checkpointing --cache_latents  --clip_skip=2 --max_token_length=225
  --caption_extension=.txt  --min_snr_gamma=5  --no_half_vae  --seed=42
```

步數 ≈ repeats(資料夾名 `10_`)× epochs × 圖數 / batch = 10×10×27/2 ≈ 1350。每 epoch 存檔 → 逐個測挑最佳(wnboy 取 e08/e10)。

---

## 踩雷

1. **cp950**(必踩):sd-scripts 印日文 log,Windows 繁中 stdout(cp950)編不了 → `UnicodeEncodeError` 炸在訓練啟動瞬間。**launch 前 `$env:PYTHONUTF8="1"`**(同 ComfyUI 那個坑、user CLAUDE.md 硬規則 1)。
2. **Blackwell torch**:一定 cu128;別讓 requirements 拉到預設 torch(會是 CPU/舊 CUDA、Blackwell 跑不動)。
3. **AdamW8bit**:bitsandbytes 在 Blackwell/Windows OK(uv 裝最新版)。要更省可換 Prodigy(自動 LR)。
4. **SDXL no_half_vae**:SDXL VAE 跑 fp16 易出 NaN,加 `--no_half_vae`。

---

## 路徑

- 生圖/篩/打標工具鏈:`D:\Work\system-setup\tools\lora-pipeline\`
- kohya:`D:\Work\sd-scripts`(獨立 venv)
- 訓練資料 + 輸出:`D:\Work\lora-training\<name>\`(`img\` / `output\` / `log\`)
- 出圖用:複製選定 epoch 的 `.safetensors` 到 `D:\Models\diffusion\loras\`
