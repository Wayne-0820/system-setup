# System Setup

重灌 Windows 後,給 Claude Code 當脈絡的規劃文件集。

## 使用方式

**重灌後第一次對 Claude Code 說的話**:

> 讀 `context.md` 和 `decisions.md`,我們要開始設定新系統。先執行 winget 批次安裝,其餘照 decisions.md 的手動清單一步步來。

## 文件索引

| 檔案 | 用途 | 何時讀 |
|---|---|---|
| `context.md` | 硬體、使用情境、偏好 | **Claude Code 第一份讀這個** |
| `decisions.md` | 所有已拍板的決策 + winget 清單 | 第二份 |
| `davinci-pipeline.md` | AI 影像生產流程架構 | 開始做 creative pipeline 時 |
| `comfyui-setup.md` | ComfyUI 乾淨重來策略 + 節點基礎 | 裝 ComfyUI 時 |
| `local-models.md` | 本地 LLM 探索指南 | 裝 Ollama 時 |
| `ldbot-checklist.md` | Ldbot 重灌前後備忘 | 重灌前 + Ldbot 重建時 |
| `media-structure.md` | D:\Media 資料夾結構與工作流 | 第一次開剪輯專案前 |
| `openwebui-setup.md` | Open WebUI + LiteLLM 多模型介面 | 裝 Open WebUI 時 |
| `reinstall-manifest.md` | 重灌清單自動產生系統 | **全部裝完後執行一次** |

## 重灌前必做

1. Ldbot:`git push` + 備份 4 個 gitignored 檔案到 NAS(詳見 `ldbot-checklist.md`)
2. 其他工作資料夾整包丟 NAS(清掉 `.venv/`、`__pycache__/`、`node_modules/`)
3. 這個 `system-setup` repo push 到 GitHub

## 重灌後啟動順序

1. Windows 11 乾淨安裝
2. NVIDIA Studio Driver(官網下載)
3. **Armoury Crate**(ASUS 官網,裝完清理背景服務)
4. `winget install Git.Git OpenJS.NodeJS.LTS`
5. `npm i -g @anthropic-ai/claude-code`
6. `git clone <system-setup repo>`
7. 打開 Claude Code,讀 `context.md` 開始工作

---

**最後更新**:重灌前最後一次提交
