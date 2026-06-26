<#
.SYNOPSIS
  Paste a Civitai model id -> list every version with its base model, version id,
  file name and size. Use it to pick the version that matches YOUR base model,
  then feed the version id to WCopilot: "download civitai version <id> as <type>".

.USAGE
  pwsh .\civitai-versions.ps1 433138
  pwsh .\civitai-versions.ps1            # then paste / type the id when prompted
  (accepts a bare id, an AIR like "civitai: 433138 @ 1982303", or a models URL)
#>
param([string]$ModelRef)

if (-not $ModelRef) { $ModelRef = Read-Host "Civitai model id (or AIR / model URL)" }

# pull the FIRST number that looks like a model id
$m = [regex]::Match($ModelRef, '(\d{3,})')
if (-not $m.Success) { Write-Host "No model id found in: $ModelRef" -ForegroundColor Red; exit 1 }
$modelId = $m.Groups[1].Value

try {
    $d = Invoke-RestMethod -Uri "https://civitai.com/api/v1/models/$modelId" -TimeoutSec 25
} catch {
    Write-Host "Lookup failed for model $modelId : $_" -ForegroundColor Red; exit 1
}

Write-Host ""
Write-Host ("Model: {0}   [{1}]" -f $d.name, $d.type) -ForegroundColor Cyan
Write-Host ("{0,-10} {1,-18} {2,-26} {3}" -f "versionId", "baseModel", "versionName", "file (size)")
Write-Host ("-" * 92)
foreach ($v in $d.modelVersions) {
    $fn = if ($v.files -and $v.files.Count) { $v.files[0].name } else { "?" }
    $sz = if ($v.files -and $v.files.Count) { "{0:N0} MB" -f ($v.files[0].sizeKB / 1024) } else { "" }
    Write-Host ("{0,-10} {1,-18} {2,-26} {3} ({4})" -f $v.id, $v.baseModel, $v.name, $fn, $sz)
}
Write-Host ""
Write-Host "Pick the row whose baseModel matches the checkpoint you will use." -ForegroundColor Yellow
Write-Host "Then in WCopilot: download civitai version <versionId> as <lora|checkpoint|vae...>" -ForegroundColor Yellow
