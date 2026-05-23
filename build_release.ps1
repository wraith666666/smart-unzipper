# Build and release script for BulkZipExtractor
# Usage: .\build_release.ps1 -Version "1.0.0"

param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$ExeName = "BulkZipExtractor"
$TagName = "v$Version"

# 1. Build the EXE
Write-Host "Building EXE..." -ForegroundColor Cyan
pip install pyinstaller --quiet
pyinstaller --onefile --windowed --icon=icon.ico --name $ExeName unzipper.py

if (-not (Test-Path "dist\$ExeName.exe")) {
    Write-Error "Build failed - EXE not found in dist\"
    exit 1
}

Write-Host "Build successful: dist\$ExeName.exe" -ForegroundColor Green

# 2. Tag and push
Write-Host "Tagging $TagName..." -ForegroundColor Cyan
git tag $TagName
git push origin $TagName

# 3. Create GitHub release and upload EXE (requires GitHub CLI: https://cli.github.com)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "Creating GitHub release $TagName..." -ForegroundColor Cyan
    $notes = "## What's new`n`n- Initial release`n`n## Download`nRun $ExeName.exe directly - no Python required."
    gh release create $TagName "dist\$ExeName.exe" `
        --title "$TagName" `
        --notes $notes
    Write-Host "Release published!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "GitHub CLI not found. Install it from https://cli.github.com" -ForegroundColor Yellow
    Write-Host "Then re-run, or manually upload dist\$ExeName.exe on GitHub Releases." -ForegroundColor Yellow
}
