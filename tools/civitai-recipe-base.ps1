<#
.SYNOPSIS
  Paste a generation recipe -> tell you which CHECKPOINT (base model) it used,
  by looking up its "Model hash: XXXX" on Civitai. Also resolves any LoRA hashes
  in the recipe if present. Answers "what base model do I need for this recipe?".

.USAGE
  # copy the recipe text to the clipboard, then:
  pwsh .\civitai-recipe-base.ps1
  # or pass it explicitly:
  pwsh .\civitai-recipe-base.ps1 -Recipe "Steps: 25, ... Model hash: bdb59bac77, ..."
#>
param([string]$Recipe)

if (-not $Recipe) {
    try { $Recipe = (Get-Clipboard -Raw) } catch { }
    if (-not $Recipe) { $Recipe = Read-Host "Paste the recipe (single line)" }
}

function Resolve-Hash([string]$hash, [string]$label) {
    try {
        $d = Invoke-RestMethod -Uri "https://civitai.com/api/v1/model-versions/by-hash/$hash" -TimeoutSec 25
    } catch {
        Write-Host ("  {0}: hash {1} -> not on Civitai (private / non-Civitai source)" -f $label, $hash) -ForegroundColor DarkYellow
        return
    }
    $fn = if ($d.files -and $d.files.Count) { $d.files[0].name } else { "?" }
    Write-Host ("  {0}: {1}  (version {2})" -f $label, $d.model.name, $d.name) -ForegroundColor Cyan
    Write-Host ("       baseModel={0}  type={1}  file={2}" -f $d.baseModel, $d.model.type, $fn)
    Write-Host ("       page: https://civitai.com/models/{0}?modelVersionId={1}" -f $d.modelId, $d.id)
    Write-Host ("       WCopilot: download civitai version {0} as {1}" -f $d.id, $d.model.type.ToLower())
}

Write-Host ""
# --- checkpoint (the base model) ---
$cm = [regex]::Match($Recipe, 'Model hash:\s*([0-9a-fA-F]{8,})')
if (-not $cm.Success) {
    $bare = [regex]::Match($Recipe.Trim(), '^[0-9a-fA-F]{8,}$')   # they may paste just a hash
    if ($bare.Success) { $cm = $bare }
}
if ($cm.Success) {
    Write-Host "CHECKPOINT (base model for this recipe):" -ForegroundColor Green
    Resolve-Hash $cm.Groups[1].Value "checkpoint"
} else {
    Write-Host "No 'Model hash:' found in the recipe." -ForegroundColor Red
}

# --- loras referenced in the recipe (optional) ---
$lh = [regex]::Matches($Recipe, 'Lora hashes:\s*"?([^"\r\n]+)')
if ($lh.Count) {
    Write-Host ""
    Write-Host "LORAS in the recipe:" -ForegroundColor Green
    foreach ($pair in ($lh[0].Groups[1].Value -split ',')) {
        $p = $pair.Trim()
        $hm = [regex]::Match($p, '([0-9a-fA-F]{8,})\s*$')
        if ($hm.Success) { Resolve-Hash $hm.Groups[1].Value ($p -replace ':\s*[0-9a-fA-F]+$','').Trim() }
    }
}
Write-Host ""
Write-Host "Rule: checkpoint + lora + tags + clip-skip must all be the same family." -ForegroundColor Yellow
