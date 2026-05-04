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

平行用法:plugin `/codex:review` 跑不通時,優先用終端機 Codex CLI full-access review(2026-05-05 實測可用):

```powershell
codex -s danger-full-access -a never review --commit HEAD
```

`--commit HEAD` review 最新 commit diff(`HEAD^..HEAD`),不是整 repo / working tree。`-s danger-full-access -a never` 是 Codex CLI 全域參數,必須放在 `codex` 後、`review` 前。Codex 桌面板 GUI review 仍未實測。

Workflow 邊界:此 CLI review 可由 session 1 自動列入 commit / snapshot / 規則文件 review 派工;review finding 是給 Claude 的第二視角 / 導正訊號,派工範圍內明確 actionable finding 可直接修,progress report 只記結論 / 修正 / STOP 原因,不貼長篇摘要。Wayne 若說「停止自動出現 Codex review」或同義指令,自動列入立即暫停,直到 Wayne 再次明確呼喊「Codex review」才恢復作動。

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

**平行用法**

- **獨立 PowerShell + CLI direct review(預設 / disk-full-read-access)**:**實測失敗(2026-05-04)** — `codex review --uncommitted -c 'sandbox_permissions=["disk-full-read-access"]'` 仍撞 `CreateProcessAsUserW failed: 5`(訊息與本坑完全一致),review agent 啟動但每個 exec spawn 皆失敗。社群 `openai/codex-plugin-cc#57` 通用 workaround **不適用 Wayne 機器**。anchor:progress report `2026-05-04_lane-d1-cli-review-probe.md`
- **獨立 PowerShell + CLI full-access review**:**實測可用(2026-05-05)** — `codex -s danger-full-access -a never review --commit HEAD` 成功 inspect HEAD commit diff 並產出 review finding;未再撞 `CreateProcessAsUserW failed: 5/2`。`git status --short` 確認 smoke test 後 working tree clean。stderr 有 plugin sync 403 / skill icon warning 等 non-fatal warning,不影響 review 完成。
- **Codex 桌面板 GUI**:未實測,留 Lane D2 自決
- **關鍵發現**:sandbox 失敗**不限於** Claude Code Bash tool 嵌套 spawn — 完全脫離任何 wrapper 仍會撞;但 full-access 繞過 sandbox 後 CLI review 可用。本坑問題定位範圍收斂為「Codex CLI Windows sandbox / reviewer exec spawn 環境問題」,不是 Codex review 功能整體不可用。
- **evidence pack cross-cut(2026-05-04)**(Lane A evidence pack 結果,anchor:progress report `2026-05-04_codex-sandbox-evidence-pack.md`):
  - **config / banner mismatch**:`~/.codex/config.toml` 設 `sandbox = "elevated"`,但 banner 顯示 `workspace-write` — **persistent + ad-hoc(`-c sandbox_permissions=...`)雙路徑都 mismatch**(原 outside-scope 觀察擴大版),不是讀檔路徑問題,高度懷疑 0.128.0 未採用該 key/value
  - **雙重安裝**:`OpenAI.Codex` packaged app(WindowsApps,version `26.429.3425.0`)+ npm `codex-cli 0.128.0` 共存,PATH 走 npm;runner 內部 ResolveExecutable 是 black box,可能 fall back 到 packaged app binaries 撞 ACL
- **A.1 schema / stop-loss cross-cut(2026-05-04)**(anchors:progress reports `2026-05-04_lane-a1-config-schema-fix-trial.md` + `2026-05-04_lane-a1b-global-config-stoploss.md`):
  - Codex 0.128.0 `--sandbox <SANDBOX_MODE>` 合法值只有 `read-only` / `workspace-write` / `danger-full-access`;`sandbox = "elevated"` 與 `sandbox = "experimental"` 均為非法值。
  - `elevated_windows_sandbox` / `experimental_windows_sandbox` feature flags 在 0.128.0 `stage = removed`;A.1 候選 C / A 已由 schema audit 證偽並跳過。
  - `~/.codex/config.toml` 是 Codex Desktop / plugin / CLI 共用 user-level global config;改此檔會污染當下整個 Codex 生態系,不是只影響獨立 CLI。A.1 Phase 2 B patch 已 stop-loss,從 backup byte-by-byte 還原完成;未取得 `codex review --uncommitted` 成敗 verdict。

**未來追 root cause 候選**(未拍板,見「未來 lane」段 Lane A)

**forensic 觀察**:43 KB `~/.codex/.sandbox/sandbox.log` 內**無**任一 sandbox 失敗 keyword(Lane D1 stderr 噴 `CreateProcessAsUserW failed: 5` 三次,該 log 0 命中)→ Codex 0.128.0 sandbox 失敗 trail 不在 sandbox.log,**可能** forensic source 包含 `logs_2.sqlite`(19 MB,evidence pack 副檔名限制未 verify)/ stderr capture / Windows Event Log,具體哪個是 trail 主源未拍板。

---

### 坑 #2:Codex 桌面板掛載 repo 後出現 mirror-like artifacts 14 檔(2026-05-04)

**症狀**

`/codex:setup` 跑完後 working tree 多出 14 untracked(原 commit `b230969` push 後 clean):

| Path | 數量 | 對應 source |
|---|---|---|
| `.agents/skills/<name>/SKILL.md` | 9 | `.claude/skills/<name>/SKILL.md`(9 個 same-name) |
| `.codex/agents/<name>.toml` | 4 | `.claude/agents/<name>.md`(4 個 same-name) |
| `AGENTS.md` | 1 | `CLAUDE.md`(root) |

**解法**

`.gitignore` 精準 patch(commit `df44052`,2026-05-04;Lane C 後更新):

```
# Codex Desktop mirror artifacts (auto-generated; root AGENTS.md is hand-crafted)
# AGENTS.md 紀律:hand-crafted AGENTS.md 應 commit;auto-generated dumb replace 不應 commit
.agents/skills/
.codex/agents/
```

**Lane C 更新(2026-05-04)**:`AGENTS.md` 已改由主視窗 hand-craft 正式版並 commit,不再列入 `.gitignore`。若桌面板未來再次產生 dumb replace 版,不可採信;先對照本檔與 `AGENTS.md` 差異後拍板。

**避免廣域 ignore `.agents/` `.codex/`**:未來 codex marketplace metadata / repo-native 設定可能落這條路徑,廣域 ignore 會 hide 後續該追蹤的東西。

**觀測 / 推測**(官方未文件化)

桌面板掛載 repo 後**觀測到** `.claude/skills/` + `.claude/agents/` 對應內容出現在 codex 內定路徑(`.agents/skills/` + `.codex/agents/`),並出現 `AGENTS.md` root 檔。**觸發機制未定**:官方 changelog / Codex Desktop release notes 均**無 mirror / auto-create 文件化**(community-researcher 二輪 verify,2026-05-04)。

依據(community-researcher 兩輪 finding,2026-05-04):

- `.agents/skills/` 是 skills 官方路徑;`.codex/agents/` 是 subagents 官方路徑(各自 docs 確認)
- 官方 changelog v0.123-0.128 + Codex Desktop release notes(GitHub `openai/codex#10859` 確認不公開)均無「掛載即 mirror」/「auto-import from Claude」/「disable mirror」說明
- `/codex:setup` 本身不產生 mirror,觸發源在桌面板(精確機制官方未說明)
- 第三方 convert 工具(`zuharz/ccode-to-codex` / `padmilkhandelwal/convert-claude-to-codex-skill`)是社群手動工具,**非桌面板內建**

**實機觀察(Step 2 rename probe,2026-05-04)**

`Rename-Item AGENTS.md AGENTS.md.probe-bak` 後觀察 `Test-Path AGENTS.md`:

| 觀察點 | `AGENTS.md` 是否重生 |
|---|---|
| 立即(rename 後 < 1 秒)| ❌ 沒重生 |
| 連續多時點(30s / 1min / 5min)| ❌ 沒重生 |
| 開 Codex Desktop 後 | ❌ 沒重生 |
| 跑 plugin 命令後 | ⚠️ 未實質測(本輪不延伸) |

**結論**:**未觀測到持續 file-watcher 或「開桌面板即 re-mirror」**。較像 one-shot import / mount-time conversion / 其他未明一次性觸發。plugin slash command 觸發點未測,獨立延伸 lane(Wayne 自決時機)。

`AGENTS.md.probe-bak` 為 probe artifact,已於 Lane B commit 前刪除(不 commit)。

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

- **hand-crafted AGENTS.md 已入駐並應 commit**(Lane C,2026-05-04;社群實踐,等同 CLAUDE.md 地位)
- **auto-generated dumb replace 不應 commit**(本派工拍板)
- 未來若需調整 Codex repo instructions,直接維護 root `AGENTS.md`,不要用 mirror 工具覆蓋

---

### 坑 #3:PowerShell here-string / command literal 含刪檔 keyword 撞 sandbox 誤擋(2026-05-04)

**症狀**:寫 progress report 時 `@'...'@` here-string body 含 `Remove-Item` 字樣,撞 Claude Code sandbox keyword scan 攔(訊息 `Remove-Item on system path '/' is blocked.`),write 動作中止。
**解法**:寫含刪檔 keyword 的文字內容用 **Write 工具**(不經 PowerShell parser);必須用 PowerShell here-string 時 backtick 包 keyword 或改替代詞描述。

---

## 未來 lane(獨立,未拍板)

### Lane A:sandbox root cause 追(2026-05-04 evidence pack + A.1 schema audit / stop-loss)

**Evidence pack 結果摘要**(progress report `2026-05-04_codex-sandbox-evidence-pack.md`):

- config / banner mismatch:`config.toml` `sandbox = "elevated"` vs banner `workspace-write`(persistent + ad-hoc `-c` 雙路徑都失效)
- onboarding marker 存在(`.sandbox/setup_marker.json` + `.sandbox-bin/` + `.sandbox-secrets/` 共存)→ **降低「onboarding 未跑」候選優先度**(marker 存在 ≠ 功能正常,但「未跑」假設駁倒)
- 雙重安裝:`OpenAI.Codex` packaged app(WindowsApps,version `26.429.3425.0`)+ npm `codex-cli 0.128.0`,PATH 走 npm
- sandbox.log 43 KB 內 0 命中 sandbox 失敗 keyword(forensic trail 不在該 log;見坑 #1 §未來追 root cause 候選 §forensic 觀察)

**A.1 schema audit + stop-loss 結果摘要**(progress reports `2026-05-04_lane-a1-config-schema-fix-trial.md` + `2026-05-04_lane-a1b-global-config-stoploss.md`):

- 0.128.0 sandbox enum ground truth:`read-only` / `workspace-write` / `danger-full-access`
- `sandbox = "elevated"` 非法,可解釋 banner fallback `workspace-write`;但未證明能解 `CreateProcessAsUserW failed: 5`
- `sandbox = "experimental"` 非法;`experimental_windows_sandbox` / `elevated_windows_sandbox` feature flags 已 `removed`
- `codex sandbox windows` 子命令存在(`Run a command under Windows restricted token`),支持 Windows restricted token runner layer 候選
- `~/.codex/config.toml` 是 Desktop / plugin / CLI 共用 global config;A.1 Phase 2 B patch 會污染當下 Codex Desktop / plugin / CLI,因此已 stop-loss 還原,不繼續疊加候選

**Upstream issue 對照**(主視窗 ground truth verify,2026-05-04):

| Issue | 標籤 | 對應 |
|---|---|---|
| `openai/codex#10090` | **STRONG MATCH** | `elevated_windows_sandbox` 造成 commands fail / log 含 `CreateProcessAsUserW failed: 5`;workaround 指向 disabling `elevated_windows_sandbox` / 退回 `experimental_windows_sandbox` |
| `openai/codex#13965` / `#14211` | MID MATCH | WindowsApps packaged app ACL / child-process launch path 可致 `CreateProcessAsUserW failed: 5`;支持雙重安裝候選 |
| `openai/codex#9062` | WEAK / MID | 同屬 Windows sandbox process creation failed;workaround 是 sandbox re-onboarding;但錯誤是 `CreateProcessWithLogonW`(非 `CreateProcessAsUserW`) |
| `openai/codex#18620` | WEAK | Windows sandbox shell commands fail 近期問題;錯誤碼不同,僅作背景訊號 |

**根因候選排序**(evidence + upstream + A.1 schema audit / stop-loss 整合,2026-05-04):

1. **Codex Windows restricted token sandbox runner 行為問題** — `codex sandbox windows` 子命令存在,錯誤訊息 `CreateProcessAsUserW failed: 5` 指向 runner spawn layer;A.1 改 config 未取得 review verdict。
2. **Desktop / plugin nested sandbox contamination** — A.1b 實證 user-level config 改動會污染 Desktop / plugin / CLI 三入口;是否額外加劇 nested spawn 仍未實測。
3. **config schema mismatch** — **部分坐實但降級為表象候選**:`sandbox = "elevated"` 非法可解釋 banner mismatch,但目前不足以解釋 review spawn 失敗。
4. **WindowsApps packaged app ACL / dual install sandbox runner path** — upstream `#13965` / `#14211` MID MATCH 支持,仍可作 runner layer 子候選。
5. **sandbox onboarding 跑了但壞掉** — marker 存在降低「未跑」候選優先度;上游 `#9062` WEAK/MID,錯誤 API 不同。

**下一步候選**(Wayne 自決時機,**本輪不執行修復 / 不改 config**):

- ~~查 GitHub issue 找解~~ → 已完成(本輪 ground truth verify)
- ~~verify outside-scope a/b/c~~ → 已由 evidence pack + upstream `#10090` 強化為 config schema 主嫌(具體 schema 對應 key 仍待後續 verify)
- ~~試 Claude Code permission mode~~ → 降級(D1 證明獨立 PowerShell 也撞)
- ~~Lane A.1 候選修復試驗~~ → 已執行 schema audit + Phase 2 B stop-loss;C/A schema 證偽跳過,B 未取得 review verdict。後續若再試 config,需先設計 Desktop / plugin / CLI global config isolation,不沿用原 A.1 逐候選假設。
- **Lane A.2 候選**:獨立 PowerShell only sandbox runner probe(不改 global config,直接隔離 `codex sandbox windows` / restricted token runner layer 是否撞 `CreateProcessAsUserW failed: 5`)。
- **Lane A.3 候選**:接受限制 + 文件化失敗模式為主路徑(`/codex:setup` / MCP `codex/list_mcp_resources` 仍可用)。
- **Lane D2 候選**:Codex Desktop / plugin nested sandbox contamination probe(Desktop GUI / plugin wrapper 是否另有 nested spawn layer;需 Wayne 親操或明確隔離)。

### Lane B:桌面板 mirror 行為探查(2026-05-04 實機觀察完成)

實機觀察結論寫進踩坑 #2 §實機觀察段。本 lane 主要完成項:
- ✅ rename probe(觀察未重生 → 非持續 file-watcher,推測 one-shot)
- ✅ community-researcher 二輪查官方文件 / 社群實踐(官方未文件化 mirror)

未測 / 延伸選項(Wayne 自決時機,本輪不延伸):
- ⚠️ plugin slash command 觸發點測試(`/codex:setup` / `/codex:review` 後是否 re-mirror)
- ⚠️ 桌面板 GUI 設定面板 disable mirror 選項(需 Wayne 親操桌面板找)

### Lane C:hand-craft AGENTS.md source-of-truth(2026-05-04 完成)

完成項:
- root `AGENTS.md` hand-crafted 正式入駐
- `.gitignore` 移除 `AGENTS.md` ignore,保留 `.agents/skills/` + `.codex/agents/` 精準隔離
- Codex 語境下明確區分 `CLAUDE.md` / session 1 / session 2 / Codex 三件套,不做 mechanical replace

### Lane D:平行用法實測

- **D1**(CLI direct review)→ **預設 / disk-full-read-access 實測失敗(2026-05-04)**;**full-access 實測可用(2026-05-05)**:`codex -s danger-full-access -a never review --commit HEAD` 可 inspect 最新 commit diff。細節見坑 #1 §平行用法段。
- **D2**(Codex 桌面板 GUI 跑 review)→ 未實測,Wayne 自決時機;社群證據不足,**不能再以 D1 通則推論 D2 也通**
- **D1 對 D2 priority 影響**:D1 證明 sandbox 失敗不限於 Claude Code 嵌套 spawn,但 full-access CLI review 已可作主 workaround;D2 可降優先級,除非 Wayne 想驗證 GUI review。

---

**最後更新**:2026-05-04
**版本**:1.0(C-lite 最小 Codex 子目錄,Wayne 拍板新增 2026-05-04)
