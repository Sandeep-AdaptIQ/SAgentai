# SAgentai - Download Bundled Extensions Script
# Downloads VSIX files from VS Code Marketplace into bootstrap/extensions/
# Run this whenever you want to update the bundled extensions.

param(
	[string]$OutputDir = (Join-Path $PSScriptRoot "..\bootstrap\extensions")
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$extensions = @(
	@{ publisher = "GitHub"; name = "copilot-chat" },
	@{ publisher = "salesforce"; name = "salesforcedx-vscode" },
	@{ publisher = "Equinusocio"; name = "vsc-material-theme" }
)

$galleryApi = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

function Get-LatestVersion {
	param($publisher, $name)
	$body = @{
		filters = @(@{
				criteria   = @(@{ filterType = 7; value = "$publisher.$name" })
				pageNumber = 1
				pageSize   = 1
				sortBy     = 0
				sortOrder  = 0
			})
		flags   = 914
	} | ConvertTo-Json -Depth 10

	$headers = @{
		"Accept"       = "application/json;api-version=3.0-preview.1"
		"Content-Type" = "application/json"
	}
	try {
		$result = Invoke-RestMethod -Uri $galleryApi -Method Post -Body $body -Headers $headers -TimeoutSec 30
		return $result.results[0].extensions[0].versions[0].version
	}
 catch {
		Write-Warning "Failed to query version for $publisher.$name: $_"
		return $null
	}
}

function Download-VSIX {
	param($publisher, $name, $version, $outFile)
	$url = "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/$publisher/vsextensions/$name/$version/vspackage"
	Write-Host "  Downloading $publisher.$name v$version..."
	try {
		Invoke-WebRequest -Uri $url -OutFile $outFile -TimeoutSec 300 -UseBasicParsing
		$sizeMB = [math]::Round((Get-Item $outFile).Length / 1MB, 1)
		Write-Host "  -> Saved to $outFile ($sizeMB MB)"
		return $true
	}
 catch {
		Write-Warning "  Failed to download: $_"
		return $false
	}
}

# Ensure output directory exists
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Write-Host "Output directory: $OutputDir"
Write-Host ""

foreach ($ext in $extensions) {
	Write-Host "Processing $($ext.publisher).$($ext.name)..."
	$version = Get-LatestVersion -publisher $ext.publisher -name $ext.name
	if (-not $version) {
		Write-Warning "Skipping $($ext.publisher).$($ext.name) - could not determine version"
		continue
	}
	Write-Host "  Latest version: $version"
	$outFile = Join-Path $OutputDir "$($ext.publisher).$($ext.name)-$version.vsix"
	if (Test-Path $outFile) {
		$sizeMB = [math]::Round((Get-Item $outFile).Length / 1MB, 1)
		Write-Host "  Already downloaded ($sizeMB MB) - skipping"
		continue
	}
	# Remove older versions
	Get-ChildItem -Path $OutputDir -Filter "$($ext.publisher).$($ext.name)-*.vsix" | Remove-Item -Force
	Download-VSIX -publisher $ext.publisher -name $ext.name -version $version -outFile $outFile
	Write-Host ""
}

Write-Host ""
Write-Host "=== Downloaded extensions ==="
Get-ChildItem -Path $OutputDir -Filter "*.vsix" | ForEach-Object {
	$sizeMB = [math]::Round($_.Length / 1MB, 1)
	Write-Host "  $($_.Name) ($sizeMB MB)"
}
