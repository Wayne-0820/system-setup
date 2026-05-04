# Codex 整合配置(plugin + 桌面板 + CLI 三件套)

> **這份文件反映實際運行狀態**(不是規劃)。
>
> 最後同步:2026-05-04
>
> Codex 在 Wayne 機器三條落地路徑:Claude Code plugin(in-Claude-Code invoke)、桌面板 GUI、Codex CLI(獨立 PowerShell)。Wayne 拍板新增最小 Codex 子目錄(2026-05-04)。

---

## 環境基線

```yaml
Codex:
  CLI:
    名稱: "@openai/codex"
    版本: 0.128.0
    安裝: npm global(`npm install -g @openai/codex`)
  Claude Code plugin:
    名稱: codex@openai-codex
    版本: 1.0.4
    來源: GitHub openai/codex-plugin-cc(HTTPS clone)
    marketplace: openai-codex(Claude Code user scope)
    cache 路徑: C:\Users\Wayne\.claude\plugins\cache\openai-codex\codex\1.0.4\
  桌面板 GUI:
    版本: (未 verify)
    掛載 repo: D:\Work\system-setup
    觀測: 桌面板安裝 + 掛載 repo 後觀測到 mirror;精確觸發條件未 verify(見踩坑 #2)
  Auth:
    模式: ChatGPT login
    狀態: 本機已驗證(不記 email)
    機制: Codex CLI 既有認證自動對接 plugin
```

需 Node.js 18.18+(verify:`node --version`)。

---

## 安裝(2026-05-04 實機落地路徑)

### 1. Codex CLI

```powershell
npm install -g @openai/codex
codex --version  # 應印 codex-cli 0.128.0
```

### 2. Claude Code plugin

選 A:Claude Code prompt 框打 slash command:

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

選 B(等價):session 2 Claude Code CLI 子命令(file-level state,可自動化前 2 步;後 2 步仍需 prompt 框親跑):

```powershell
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex
# /reload-plugins + /codex:setup 仍需 Wayne 在 prompt 框親跑
# (reload session 狀態 + interactive ChatGPT auth)
```

### 3. 桌面板

(2026-05-04)Wayne 安裝桌面板 + 掛載 `D:\Work\system-setup` 後**觀測到 mirror**(見踩坑 #2);精確觸發條件未 verify。

桌面板版本 + GUI 設定面板 disable mirror 選項 — **未 verify**(獨立 lane,見下)。

---

## 在 Claude Code 內 invoke(plugin slash command)

plugin reload 後可用(本派工已 verify):

| Slash command | 用途 | 狀態(2026-05-04) |
|---|---|---|
| `/codex:setup` | 認證 + 缺漏自動裝 | ✅ 走通 |
| `/codex:review` | 對 working tree 跑 review | ⚠️ **撞 sandbox 半通**(見踩坑 #1) |
| `/codex:rescue` | rescue 流程 | ⚠️ 未驗證(`--fresh` 已知卡 init,GitHub `openai/codex-plugin-cc#236`) |

(plugin 內部 helper skill 如 `codex:codex-result-handling` / `codex:codex-cli-runtime` / `codex:gpt-5-4-prompting` 是其他 skill 觸發時調用,user 不直接 invoke,不列)

平行用法**候選**:plugin 跑不通時 Codex 桌面板 / CLI(**推測**不受 sandbox 影響,**未實測**;見踩坑 #1)。

---

## 踩坑紀錄

### 坑 #1:`/codex:review` 撞 Claude Code Windows sandbox 嵌套 spawn(2026-05-04)

**症狀**

reviewer agent spawn `pwsh.exe -Command 'git status --s...'` / `Get-Location` 等子程序撞 `CreateProcessAsUserW access error (exit -1)`。session 1 + session 2 均撞,sandbox 限制 **Claude Code 全機級**(不是 session 級)。

**達成範圍**

- plugin install
- `/reload-plugins`
- `/codex:setup`(ChatGPT auth verified,本機已驗證;不記 email)
- Codex review thread 啟動(thread id 形如 `019df0XX-...`)
- MCP resource list(`codex/list_mcp_resources` ✓)

**未達成範圍**

repo review agent inspect — reviewer 想 spawn pwsh 跑 `git status` / `Get-Location` 收集 repo 狀態,被 sandbox 擋。

**疑似 root cause**(不下定論)

Claude Code Windows sandbox 不准 Bash tool spawn 的 child process 再 spawn 子 process。嵌套 spawn 鏈確認:

```
companion script (Bash tool)
  → reviewer agent (spawn 完成 ✓)
    → pwsh.exe (撞 CreateProcessAsUserW exit -1)
```

MCP layer 不受影響(`codex/list_mcp_resources` 走通)— **只 child process spawn 撞**。

**平行用法**(推測,未實測)

Codex 桌面板 GUI / 獨立 PowerShell 跑 `codex` CLI 不在 Claude Code Bash tool 包覆下,**邏輯上**不該撞同樣 sandbox。**未實測**;若要實測可在 PowerShell 直接跑 `codex review` 對 repo 試,結果回報主視窗整合進本檔。

**未來追 root cause 候選**(未拍板,見「未來 lane」段 Lane A)

---

### 坑 #2:Codex 桌面板掛載 repo 自動 mirror 14 檔副作用(2026-05-04)

**症狀**

`/codex:setup` 跑完後 working tree 多出 14 untracked(原 commit `b230969` push 後 clean):

| Path | 數量 | 對應 source |
|---|---|---|
| `.agents/skills/<name>/SKILL.md` | 9 | `.claude/skills/<name>/SKILL.md`(9 個 same-name) |
| `.codex/agents/<name>.toml` | 4 | `.claude/agents/<name>.md`(4 個 same-name) |
| `AGENTS.md` | 1 | `CLAUDE.md`(root) |

**解法**

`.gitignore` 精準 patch(commit `df44052`,2026-05-04):

```
# Codex Desktop mirror artifacts (auto-generated; source-of-truth stays in .claude/)
# AGENTS.md 紀律:hand-crafted AGENTS.md 應 commit;auto-generated dumb replace 不應 commit
.agents/skills/
.codex/agents/
AGENTS.md
```

**避免廣域 ignore `.agents/` `.codex/`**:未來 codex marketplace metadata / repo-native 設定可能落這條路徑,廣域 ignore 會 hide 後續該追蹤的東西。

**疑似 root cause**(主視窗 audit 推測)

codex 桌面板掛載 repo 自動 mirror 既有 `.claude/skills/` + `.claude/agents/` 到 codex 內定固定路徑(`.agents/skills/` + `.codex/agents/`),並 generate `AGENTS.md` root 索引。

依據(community-researcher finding,2026-05-04):

- `.agents/skills/` `.codex/agents/` 為 codex 內定固定路徑(官方 docs 確認 codex 不讀 `.claude/`)
- `/codex:setup` 本身不產生 mirror(只做認證 + 缺漏裝),觸發源在桌面板

**`AGENTS.md` dumb replace 錯誤**(主視窗 audit 確認,**不可採信**)

mirror 工具是 mechanical「Claude」→「Codex」字串替換,內容有錯誤:

| 錯誤 | 原文(CLAUDE.md) | dumb replace 結果(AGENTS.md) |
|---|---|---|
| 命令格式 | `claude mcp add context7 -- npx ...` | `Codex mcp add context7 -- npx ...`(❌ Codex CLI 沒這命令格式) |
| user 路徑 | `C:\Users\Wayne\.claude\CLAUDE.md` | `C:\Users\Wayne\.Codex\AGENTS.md`(❌ 虛構路徑) |
| 產品名 | 「web Claude」(Anthropic 雲端) | 「web Codex」(❌ 沒這產品) |

**`.codex/agents/*.toml` 品質尚可**

format 轉換(`.md` frontmatter + body → TOML structure)+ 內容 1:1 copy。沒換 Claude → Codex(因為原文用「主視窗」/「Wayne」/「session」不涉產品名)。

**`.agents/skills/<name>/SKILL.md` 影響小**

mechanical replace,僅 `description` 1 字「Claude Code」→「Codex」。其他內容(SOP / 紀律 / 觸發條件)100% 一致。

**AGENTS.md 紀律**

- **hand-crafted AGENTS.md 應 commit**(社群實踐,等同 CLAUDE.md 地位)
- **auto-generated dumb replace 不應 commit**(本派工拍板)
- 未來若需正式 Codex 桌面板 source-of-truth 支援,主視窗 hand-craft 正確版 + commit(獨立 lane,見下)

---

## 未來 lane(獨立,未拍板)

### Lane A:sandbox root cause 追

候選(Wayne 自決時機):
- 查 GitHub issue 找 Windows sandbox 嵌套 spawn 解
- 試 Claude Code permission mode 設定(`--permission-mode acceptEdits` / `bypassPermissions` 等)
- 接受 sandbox 限制,文件化平行用法為主路徑

### Lane B:桌面板 mirror 行為探查

候選(Wayne 自決時機,手操桌面板):
- 找桌面板 GUI 設定面板 disable mirror 選項
- 試刪 1 檔(例 `AGENTS.md`)看是否 file-watcher 持續 re-mirror
- 查觸發條件(掛載時 / 開桌面板時 / 跑 plugin 命令時)

### Lane C:hand-craft AGENTS.md source-of-truth

獨立 lane(主視窗下次有閒時 hand-craft 正確版 + 派工 commit):
- 對齊 `CLAUDE.md` 但翻譯成 Codex 語境(不用 mirror 工具產的 dumb replace 版)

### Lane D:平行用法實測

候選(Wayne 自決時機):
- 在 PowerShell 直接跑 `codex review` 對 repo 試
- 桌面板 GUI 跑 review 試
- 結果回報主視窗整合進本檔(踩坑 #1「平行用法」段)

---

**最後更新**:2026-05-04
**版本**:1.0(C-lite 最小 Codex 子目錄,Wayne 拍板新增 2026-05-04)
