---
name: smoke-test-comfyui
description: When session 2 執行端 needs to run a ComfyUI smoke test, use this skill to enforce pre-test SOP (POST /free, nvidia-smi VRAM check, submit with --seed). Aligns with SESSION_2 §4.3 + comfyui/setup.md 踩坑 #16 / #13. Triggers on phrases like "跑 ComfyUI 煙測", "smoke test ComfyUI", or explicit `/smoke-test-comfyui`.
---

# smoke-test-comfyui — ComfyUI 煙測前置 SOP

> By session 2 執行端 use 的 skill。對應 SESSION_2 §4.3 + comfyui/setup.md 踩坑 #16(model cache)/ #13(execution cache)。

## 用途

煙測前置 SOP 重複度高:跑前 `POST /free` 釋放 model cache + `nvidia-smi` VRAM check + submit `--seed` 強制 reseed。skill 化封裝避免漏 step。

## 觸發條件

- 派工含「跑 ComfyUI 煙測」step
- Wayne / 派工說「跑煙測」/「smoke test」
- 顯式 `/smoke-test-comfyui`

## 執行流程

### Step 1:POST /free 釋放 model cache(踩坑 #16)

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8188/free" -Method POST `
    -ContentType "application/json" `
    -Body '{"unload_models": true, "free_memory": true}'
```

預期 200 OK。失敗 STOP 上報。

### Step 2:Nvidia-smi VRAM check

```powershell
nvidia-smi --query-gpu=memory.free,memory.used,memory.total `
           --format=csv,noheader,nounits
```

讀 free VRAM。若派工有 VRAM 門檻(例 ≥ 22 GB),確認 free ≥ 門檻 — 否則 STOP 上報(規則 13:GB / GiB 邊界附近強制標明)。

### Step 3:Submit with --seed(踩坑 #13)

派工內若用 `tools/workflow_submit.py`,確認帶 `--seed <value>` 強制 reseed:

```powershell
python D:\Work\system-setup\tools\workflow_submit.py `
    --workflow <path> `
    --seed <value> `
    <其他派工指定參數>
```

不帶 `--seed` → ComfyUI execution cache 可能跳過 sampling node(踩坑 #13)→ 結果失真。

### Step 4:跑時監控

- ws disconnect 不算 STOP 觸發點(SESSION_2 §4.3)— server-side console / queue endpoint 為準
- 派工有「卡 X min 即 kill」紀律 → 不無腦等(設 timer)
- log 量大時可 invoke `log-triage` subagent 過濾(隔離 context)

### Step 5:跑完驗證

派工 §完成判定 對照(輸出檔存在 / SHA256 match / VRAM peak < 門檻 / 等)。

## 紀律

- **跑前必跑 Step 1 + Step 2**(不省略)
- **submit 必帶 `--seed`**(踩坑 #13)
- **VRAM 門檻 GB / GiB 標明**(規則 13)
- **派工沒列的不調**(不擅自改 cfg / sampler / 解析度 / 量化 / LoRA,SESSION_2 §3.2)
