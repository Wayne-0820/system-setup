# ComfyUI-WanVideoWrapper 衝突明細

> Pack:**ComfyUI-WanVideoWrapper** by Kijai
> 版本:repo HEAD(透過 `cm-cli install` 安裝)
> 安裝日:2026-04-30
> 狀態:✅ active
>
> 主索引:[`conflicts.md`](./conflicts.md)
> 風險分級標準見主索引。
>
> 最後更新:2026-04-30

---

## TL;DR

| 結論 | 說明 |
|---|---|
| **裝這個 pack 的原因** | Wan 2.2 A14B T2V/I2V workflow(派工 2026-04-30)需要 Kijai wrapper 路線(`WanVideoModelLoader` / `WanVideoSampler` / `WanVideoTextEncode` / `WanVideoVAELoader` 等);與 ComfyUI 內建 `comfy_extras.nodes_wan`(17 節點)是兩套並存路線,wrapper 提供更多 sampler / NAG / cache / sub-pack 整合 |
| **Manager UI 衝突數** | 0(走 cm-cli 安裝,無 GUI conflicts UI;走結構性比對,詳「ComfyUI Manager cm-cli 限制」段) |
| **裝了沒問題** | 142 個節點全部前綴獨佔(`WanVideo*` / `LoadWanVideo*` / `MochaEmbeds` / `HuMoEmbeds` / `MultiTalk*` / `LynxEncode*` / `Wav2VecModelLoader` 等),跟既有 11 個 active pack(KJNodes 234 / LayerStyle 169 / LayerStyle_Advance 77 / controlnet_aux 64 / rgthree 24 / SUPIR 10 / alekpet 16 / Custom-Scripts 13 / QwenEditUtils 14 / websocket_image_save 1)0 交集,跟主索引「反向節點索引」4 條 active(`AudioConcatenate` / `Sleep` / `SplitImageChannels` / `WanVideoNAG`)0 交集 |
| **同 NAG 概念不同 class name** | KJNodes 有 `WanVideoNAG`、WanVideoWrapper 有 `WanVideoApplyNAG`(class name 不同 → 0 same-name override,可並存) |
| **依賴自動裝** | Manager prestartup 第一次啟動自動 pip install:`ftfy` / `accelerate>=1.2.1` / `einops` / `diffusers>=0.33.0` / `peft>=0.17.0` / `sentencepiece>=0.2.0` / `protobuf` / `pyloudnorm` / `gguf>=0.17.1` / `opencv-python` / `scipy` |
| **Optional sub-module 缺失** | `FantasyPortrait` 需要 `onnx` 模組(本機未裝),啟動 emit 一行 WARNING `WanVideoWrapper WARNING: FantasyPortrait nodes not available: No module named 'onnx'`;設計就是 optional,不影響核心 Wan 2.2 T2V/I2V workflow,要用 FantasyPortrait 才裝 onnx |

---

## ComfyUI 衝突機制(原理回顧)

當兩個 custom_node pack 註冊**同名節點**時:
- ComfyUI 載入順序按 `custom_nodes\` 目錄字母序
- **後載入的會覆蓋先載入的**(以 `NODE_CLASS_MAPPINGS` 為準)
- 結果:你以為在用 pack A 的節點,實際跑的是 pack B 的同名節點 → 行為不一致 → 除錯地獄

**WanVideoWrapper 在本機完全規避了這個機制**:142 個節點全部以 `WanVideo*` 命名空間獨佔(少數 sub-pack 用 `LoadWanVideo*` / `MochaEmbeds` / `HuMoEmbeds` / `MultiTalk*` / `Lynx*` / `Wav2VecModelLoader` / `WhisperModelLoader` / `QwenLoader` / `NLF*` / `WanMove_native` 等獨佔前綴),無其他 pack 採用相同命名。

注意:KJNodes 有 `WanVideoNAG`、WanVideoWrapper 有 `WanVideoApplyNAG` — **同 NAG 概念但不同 class name**,Wayne workflow 用哪個自選,沒 import 失敗或 dropdown 重複問題。

---

## 衝突分類

**無衝突。**

結構性比對(因 `cm-cli` 無 conflicts UI,需走 HTTP `/object_info` 結構比對)結果:

| 對比 pack | 節點數 | 交集 |
|---|---:|---:|
| comfyui-kjnodes | 234 | 0 |
| ComfyUI_LayerStyle | 169 | 0 |
| ComfyUI_LayerStyle_Advance | 77 | 0 |
| comfyui_controlnet_aux | 64 | 0 |
| rgthree-comfy | 24 | 0 |
| comfyui_custom_nodes_alekpet | 16 | 0 |
| Comfyui-QwenEditUtils | 14 | 0 |
| comfyui-custom-scripts | 13 | 0 |
| ComfyUI-SUPIR | 10 | 0 |
| websocket_image_save | 1 | 0 |
| **主索引反向表 4 active** | 4 | **0** |

---

## ComfyUI Manager cm-cli 限制(複用 controlnet-aux 段落)

執行窗口透過 `cm-cli.py install` 安裝新 pack 時,**沒有等價於 GUI Manager 的 conflicts UI 數字**。cm-cli 僅提供 install / uninstall / show-list 等基本操作,conflicts UI 是 Manager web frontend 的 feature。

**結構性比對 SOP**(派工模板未來引用):
1. ComfyUI 啟動後 HTTP `GET /object_info`
2. 按 `python_module` 分組,對新 pack 的節點集合 vs 既有 pack 集合做交集
3. 0 交集 = 結構性 0 衝突

**派工模板「看 Manager conflicts 數字」這條紀律**要區分:
- **GUI 派工**(Wayne 親手在 ComfyUI Manager web UI 操作):看 Manager 數字
- **執行端派工**(Claude Code 用 cm-cli 自動化):走結構性比對(本檔寫法)

---

## WanVideoWrapper 提供的節點(類型概覽)

來源:HTTP `/object_info` filter `python_module = 'custom_nodes.ComfyUI-WanVideoWrapper'`(2026-04-30 取得 142 節點)

| 類別 | 範例節點 | 計數(粗分) |
|---|---|---:|
| WanVideo 核心:Loader / Sampler / Scheduler | `WanVideoModelLoader` / `WanVideoSampler` / `WanVideoSamplerv2` / `WanVideoScheduler` / `WanVideoSamplerSettings` / `WanVideoVAELoader` / `WanVideoTinyVAELoader` / `WanVideoControlnetLoader` | ~10 |
| WanVideo Encode / Decode / Embeds 主流程 | `WanVideoTextEncode` / `WanVideoTextEncodeCached` / `WanVideoTextEncodeSingle` / `WanVideoImageToVideoEncode` / `WanVideoEncode` / `WanVideoDecode` / `WanVideoClipVisionEncode` / `WanVideoEmptyEmbeds` / `WanVideoCombineEmbeds` | ~10 |
| Sub-pack Embeds(整合外部專案 latents) | `WanVideoVACEEncode` / `WanVideoPhantomEmbeds` / `WanVideoAnimateEmbeds` / `WanVideoControlEmbeds` / `WanVideoAddS2VEmbeds` / `WanVideoAddOneToAll*Embeds` / `WanVideoAddSCAIL*Embeds` / `WanVideoAddBindweaveEmbeds` / `WanVideoAddLynxEmbeds` / `WanVideoSVIProEmbeds` / `WanVideoFunCameraEmbeds` / `WanVideoUni3C_embeds` / `WanVideoRealisDanceLatents` / `WanVideoAddMTVMotion` / `WanVideoAddTTMLatents` / `WanVideoAddStoryMemLatents` / `WanVideoAddLucyEditLatents` / `WanVideoMiniMaxRemoverEmbeds` / `WanVideoUniLumosEmbeds` / `WanVideoLongCatAvatarExtendEmbeds` | ~25 |
| LoRA 操作 | `WanVideoLoraSelect` / `WanVideoLoraSelectMulti` / `WanVideoLoraSelectByName` / `WanVideoLoraBlockEdit` / `WanVideoSetLoRAs` | 5 |
| Cache / 加速 | `WanVideoTeaCache` / `WanVideoEasyCache` / `WanVideoMagCache` / `WanVideoTorchCompileSettings` / `WanVideoSetRadialAttention` / `WanVideoSetAttentionModeOverride` / `WanVideoBlockSwap` / `WanVideoSetBlockSwap` / `WanVideoBlockList` / `WanVideoVRAMManagement` | ~10 |
| NAG / Guidance | `WanVideoApplyNAG`(對應 KJNodes `WanVideoNAG` 但不同 class name) / `WanVideoSLG` / `WanVideoOviCFG` / `WanVideoUltraVicoSettings` | 4 |
| Audio 整合(Wav2Vec / Whisper / TTS) | `Wav2VecModelLoader` / `WhisperModelLoader` / `MultiTalkModelLoader` / `MultiTalkWav2VecEmbeds` / `MultiTalkSilentEmbeds` / `FantasyTalkingModelLoader` / `FantasyTalkingWav2VecEmbeds` / `MochaEmbeds` / `HuMoEmbeds` / `OviMMAudioVAELoader` / `WanVideoEncodeOviAudio` / `WanVideoDecodeOviAudio` / `WanVideoEmptyMMAudioLatents` / `WanVideoAddOviAudioToLatents` / `NormalizeAudioLoudness` | ~15 |
| Pose / Control 預處理 | `WanVideoUniAnimateDWPoseDetector` / `WanVideoUniAnimatePoseInput` / `WanVideoControlnet` / `WanVideoAddDualControlEmbeds` / `WanVideoAddControlEmbeds` / `MTVCrafterEncodePoses` / `DrawNLFPoses` / `DrawArcFaceLandmarks` / `FaceMaskFromPoseKeypoints` / `WanVideoSCAILPoseEmbeds` | ~10 |
| ReCamMaster / SkyReels / FlashVSR | `WanVideoReCamMasterCameraEmbed` / `WanVideoReCamMasterDefaultCamera` / `WanVideoReCamMasterGenerateOrbitCamera` / `ReCamMasterPoseVisualizer` / `WanVideoImageToVideoSkyreelsv3_audio` / `WanVideoFlashVSRDecoderLoader` / `WanVideoAddFlashVSRInput` | ~7 |
| 圖像 / Latent 處理 | `WanVideoImageResizeToClosest` / `WanVideoImageClipEncode` / `WanVideoLatentReScale` / `WanVideoEncodeLatentBatch` / `ExtractStartFramesForContinuations` / `WanVideoPassImagesFromSamples` / `WanVideoPreviewEmbeds` / `DrawGaussianNoiseOnImage` | ~8 |
| Prompt 工具 | `WanVideoPromptExtender` / `WanVideoPromptExtenderSelect` / `TextImageEncodeQwenVL` / `QwenLoader` | 4 |
| Context / Loop / Args | `WanVideoContextOptions` / `WanVideoLoopArgs` / `WanVideoExperimentalArgs` / `WanVideoFreeInitArgs` / `WanVideoSamplerExtraArgs` / `WanVideoSamplerFromSettings` / `WanVideoSchedulerv2` / `WanVideoSigmaToStep` / `WanVideoExtraModelSelect` / `WanVideoVACEModelSelect` / `WanVideoVACEStartToEndFrame` / `WanVideoTextEmbedBridge` / `WanVideoRoPEFunction` | ~13 |
| 其他 sub-pack helper | `LoadVQVAE` / `LoadNLFModel` / `DownloadAndLoadNLFModel` / `DownloadAndLoadWav2VecModel` / `LoadLynxResampler` / `LynxInsightFaceCrop` / `LynxEncodeFaceIP` / `NLFPredict` / `WanMove_native` / `WanVideoWanDrawWanMoveTracks` / `WanVideoAddWanMoveTracks` / `WanVideoATI_comfy` / `WanVideoATITracks` / `WanVideoATITracksVisualize` / `WanVideoAddPusaNoise` / `WanVideoAddExtraLatent` / `WanVideoAddStandInLatent` / `WanVideoEnhanceAVideo` / `WanVideoDiffusionForcingSampler` / `WanVideoImageToVideoMultiTalk` / `DummyComfyWanModelObject` / `CreateScheduleFloatList` / `CreateCFGScheduleFloatList` | ~20 |

**總計 142 節點**(`/object_info` filter `python_module = 'custom_nodes.ComfyUI-WanVideoWrapper'` 全清單)。

註:WanVideoWrapper `__init__.py` 列出 24 個 OPTIONAL_MODULES sub-pack(S2V / FlashVSR / Mocha / FunCamera / Uni3C / ControlNet / ATI / MultiTalk / RecamMaster / SkyReels / FantasyTalking / Qwen / FantasyPortrait / UniAnimate / MTV / HuMo / Lynx / Ovi / SteadyDancer / OneToAll / WanMove / SCAIL / LongCat / LongVie2),其中 **FantasyPortrait** 因缺 `onnx` 模組而 skip,其餘 23 個 sub-pack 全部成功載入(142 = 主 nodes.py 約 40+ optional 約 100,符合預期範圍)。

---

## 對 system-setup 下一階段規劃的影響

對照 `setup.md` 的「下一階段規劃」:

| 規劃 workflow | 用到 WanVideoWrapper 哪些節點 | 處理 |
|---|---|---|
| Flux-fill OneReward 萬物移除 ✅ | 無 | — |
| Kontext + ControlNet 改姿態 ❌ Deprecated | 無 | 已棄 |
| 3a-v2 Qwen Edit 改姿態 ✅ | 無 | — |
| 3b FLUX + ControlNet 純 pose ✅ | 無 | — |
| Qwen3 TTS 聲音克隆 / 設計 | 不會 | — |
| Qwen image 擴圖 | 不會 | — |
| 智能多角度生成 | 不會 | — |
| **Wan 2.2 A14B T2V/I2V 720P(本派工目標)** | `WanVideoModelLoader` / `WanVideoSampler` / `WanVideoTextEncode` / `WanVideoVAELoader` / `WanVideoImageToVideoEncode` / `WanVideoDecode` 等核心鏈 | 本 pack 的主要使用者 |

---

## 做的決策(本 pack 相關)

| 日期 | 決策 | 理由 |
|---|---|---|
| 2026-04-30 | 安裝 ComfyUI-WanVideoWrapper(repo HEAD) | Wan 2.2 A14B T2V/I2V workflow(派工 2026-04-30)— Kijai wrapper 路線比 ComfyUI 內建 `nodes_wan`(17 節點)提供更完整的 sub-pack / sampler / cache 生態 |
| 2026-04-30 | 透過 `cm-cli install` 而非 Manager web UI | 執行端自動化派工流程(per `conflicts-controlnet-aux.md` 同 SOP);走 HTTP `/object_info` 結構性比對替代 conflicts UI |
| 2026-04-30 | opencv 衝突補修走 `--force-reinstall opencv-contrib-python` | WanVideoWrapper `requirements.txt` 含 `opencv-python` → Manager prestartup 自動 install → 跟 `opencv-contrib-python` 衝突(教訓 #8 場景再現)。第一次補修只 `pip uninstall opencv-python` **不夠**:cv2 module 共用檔案被破壞,LayerStyle `cv2.ximgproc.guidedFilter` import fail。**正確補修**:`pip install --force-reinstall --no-deps opencv-contrib-python==4.13.0.92`,把 cv2 整套檔案完整放回 |
| 2026-04-30 | 不裝 `onnx`(放棄 FantasyPortrait sub-pack) | 派工沒要求 FantasyPortrait,WanVideoWrapper 設計就是 optional,核心 Wan 2.2 T2V/I2V 不受影響;要用再裝 |

---

## pip_overrides 設定(opencv 長期解,2026-04-30 待 Wayne 拍板)

### Manager v3.39.2 pip_overrides 機制 — 已驗證

**載入路徑**(`prestartup_script.py` line 93+97 + `glob/manager_core.py` line 233):

```
D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\user\__manager\pip_overrides.json
```

**目錄狀態**:`__manager\` 已存在(Manager runtime files 跟 `config.ini` / `channels.list` / `snapshots\` / `startup-scripts\` / `cache\` 同位),`pip_overrides.json` **目前不存在**(只有 `pip_overrides.json.template` 在 ComfyUI-Manager pack 目錄,Manager **不讀** template)。

**機制**(`glob/manager_core.py` line 265-269):

```python
def remap_pip_package(pkg):
    if pkg in cm_global.pip_overrides:
        res = cm_global.pip_overrides[pkg]
        print(f"[ComfyUI-Manager] '{pkg}' is remapped to '{res}'")
        return res
    else:
        return pkg
```

Manager 在 prestartup install dependencies 時對每個 requirements.txt entry 跑 `remap_pip_package`,如果命中 dict key 就改裝 mapped value(同時 print 一行 console 訊息可驗證生效)。

**Manager template 預設**(`pip_overrides.json.template` line 9-13):

```json
{
    "opencv-contrib-python": "opencv-contrib-python-headless",
    "opencv-python": "opencv-contrib-python-headless",
    "opencv-python-headless": "opencv-contrib-python-headless",
    "opencv-python-headless[ffmpeg]<=4.7.0.72": "opencv-contrib-python-headless",
    "opencv-python>=4.7.0.72": "opencv-contrib-python-headless"
}
```

**注意:不能照搬 template**。Template 把所有 opencv 都導向 `opencv-contrib-python-headless`(GUI-less 版,缺 imshow / namedWindow / waitKey)。本機紀律(教訓 #8)用 `opencv-contrib-python` **完整版**(含 GUI),因為 LayerStyle guidedFilter 來自 contrib + ximgproc,且某些 custom node(尤其 preprocessor / preview 類)可能用 cv2.imshow 系列。

### 建議 pip_overrides.json 內容

```json
{
    "opencv-python": "opencv-contrib-python",
    "opencv-python-headless": "opencv-contrib-python",
    "opencv-python>=4.7.0.72": "opencv-contrib-python",
    "opencv-python-headless[ffmpeg]<=4.7.0.72": "opencv-contrib-python"
}
```

key 設計:
- `opencv-python` 跟 `opencv-python-headless` 是裸 spec(WanVideoWrapper requirements.txt 用裸 spec)
- 後 2 條是 template 帶版本 spec 變體(防其他 pack 帶版本約束)
- value 一律 `opencv-contrib-python`(完整 GUI 版,符合教訓 #8)

### 落地步驟(Wayne 拍板後執行)

```powershell
# Step 1: 寫 pip_overrides.json(.NET API + UTF-8 無 BOM,符合 user-level CLAUDE.md 硬規則 1)
$content = @'
{
    "opencv-python": "opencv-contrib-python",
    "opencv-python-headless": "opencv-contrib-python",
    "opencv-python>=4.7.0.72": "opencv-contrib-python",
    "opencv-python-headless[ffmpeg]<=4.7.0.72": "opencv-contrib-python"
}
'@
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\user\__manager\pip_overrides.json", $content, $utf8NoBom)

# Step 2: 驗證(純 ASCII,user-level CLAUDE.md 硬規則 2)
$bytes = [System.IO.File]::ReadAllBytes("D:\Work\ComfyUI_portable\ComfyUI_windows_portable\ComfyUI\user\__manager\pip_overrides.json")
($bytes | Where-Object { $_ -gt 127 }).Count   # 期望:0

# Step 3: 觸發 Manager prestartup 驗證(故意卸 opencv 全套,讓 Manager 補裝時走 remap)
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip uninstall opencv-python opencv-python-headless opencv-contrib-python -y

# Step 4: 重啟 ComfyUI,看 console 是否 emit "[ComfyUI-Manager] 'opencv-python' is remapped to 'opencv-contrib-python'"
# 如有 emit + opencv-contrib-python 被裝 → remap 生效
& "D:\Work\system-setup\start_comfyui.bat"

# Step 5: 啟動完成後驗證
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -m pip list | Select-String "opencv"
# 期望:只剩 opencv-contrib-python(無 opencv-python / opencv-python-headless)
& "D:\Work\ComfyUI_portable\ComfyUI_windows_portable\python_embeded\python.exe" -c "import cv2; print(cv2.__version__); from cv2 import ximgproc; print('guidedFilter OK')"
```

### 風險 / 限制

- **覆蓋範圍**:Manager 的 `remap_pip_package` 只對 **Manager prestartup install dependencies 路徑**生效。如果 custom node 自己在 `__init__.py` 跑 `subprocess.run(['pip', 'install', 'opencv-python'])`(繞過 Manager 自己 install),remap 不會擋。實測 WanVideoWrapper 走 Manager 路線,沒踩這條
- **未來 Manager 升級格式變動風險**:本機 Manager v3.39.2 行為,未來 Manager v4 可能改格式(看 `pip_overrides.json.template` 是否還在 / `remap_pip_package` 簽章是否變)
- **不影響已裝套件**:寫 pip_overrides.json 不會自動清掉現有 opencv-python — 第一次寫完要手動 `pip uninstall opencv-python` + restart 觸發 Manager 用新規則重新 install

### 拍板選項(Wayne 主視窗評估)

- (A) **採用**:寫 pip_overrides.json + uninstall opencv-python + restart 驗證 → 永久修復(下次 update WanVideoWrapper / 任何含 opencv-python 的新 pack 都不會再打破教訓 #8)
- (B) **不採用**:每次踩到再跑教訓 #8 force-reinstall SOP(本檔 §「做的決策」line 4 的修法),問題每次重現但是 known + 已記在教訓 #8
- (C) **延後**:現在沒踩,等下次 install 帶 opencv-python 的新 pack 再評估(風險:會多一次 LayerStyle 炸 + 補修循環)

執行端推薦 (A) — 寫一次 4 行 JSON 永久解,額外維護負擔極低,跟 user-level CLAUDE.md 紀律「不過度解、但能根治就根治」對齊。但這是主視窗決策,執行端只攤事實 + 選項。

---

## 相關文件

- [`conflicts.md`](./conflicts.md) — 主索引(反向節點查表 + 決策日誌 + SOP)
- [`setup.md`](./setup.md) — ComfyUI 配置全貌(本 pack 進「已裝 Custom Nodes」清單 + 教訓 #8 opencv 補修紀律)
- [`conflicts-controlnet-aux.md`](./conflicts-controlnet-aux.md) — per-pack template 來源 + cm-cli 限制 + 結構性比對 SOP
- [`conflicts-kjnodes.md`](./conflicts-kjnodes.md) — KJNodes `WanVideoNAG` 紀律(本 pack `WanVideoApplyNAG` 不撞)

---

**最後更新**:2026-04-30

**同步來源**:
- HTTP `/object_info` filter `python_module = 'custom_nodes.ComfyUI-WanVideoWrapper'`(2026-04-30 取得 142 節點清單)
- `cm-cli install https://github.com/kijai/ComfyUI-WanVideoWrapper`(2026-04-30 安裝紀錄)
- 結構性比對 vs 11 個 active pack + 主索引反向表 4 條(2026-04-30 全綠)
