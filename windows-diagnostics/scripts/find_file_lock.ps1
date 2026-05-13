# find_file_lock.ps1 - Automate file lock investigation (Recipe a)
# Usage: .\find_file_lock.ps1 -FilePath "C:\path\to\locked\file.txt"

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$ErrorActionPreference = "Stop"

Write-Host "=== File Lock Investigation ===" -ForegroundColor Cyan
Write-Host "Target file: $FilePath" -ForegroundColor Yellow
Write-Host ""

# Step 1 — find which process has the file open
Write-Host "[1/3] Searching for processes with file open..." -ForegroundColor Green
./nirsoft/OpenedFilesView.exe /stext ./ofv_out.txt

# Validation: Check if output file was created
if (!(Test-Path ./ofv_out.txt)) {
    Write-Error "OpenedFilesView failed. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if output contains data
if ((Get-Item ./ofv_out.txt).Length -eq 0) {
    Write-Warning "No open files found. File may not be locked or path incorrect."
    Write-Host "Falling back to handle64..." -ForegroundColor Yellow
    ./systeminternals/handle64.exe -accepteula $FilePath | findstr /V "^$"
    exit 0
}

# Parse ofv_out.txt: find rows where Filename matches target path
$lockingProcess = Select-String -Path ./ofv_out.txt -Pattern ([regex]::Escape($FilePath))
if (!$lockingProcess) {
    Write-Warning "File not found in OpenedFilesView output. Verify file path is correct."
    exit 1
}

Write-Host "Found locking process in OpenedFilesView output" -ForegroundColor Green
Write-Host ""

# Step 2 — confirm with handle64 and get handle value
Write-Host "[2/3] Confirming with handle64..." -ForegroundColor Green
$handleOutput = ./systeminternals/handle64.exe -accepteula $FilePath | findstr /V "^$"

# Validation: Verify handle64 found the file
if ($LASTEXITCODE -ne 0) {
    Write-Warning "handle64 did not find the file. Possible causes: file not locked, incorrect path, or insufficient privileges."
    Write-Host "Recommendation: Relaunch shell as administrator or reboot to release locks." -ForegroundColor Yellow
    exit 1
}

Write-Host $handleOutput
Write-Host ""

# Step 3 — launch procexp64 for visual confirmation
Write-Host "[3/3] Launching Process Explorer for visual confirmation..." -ForegroundColor Green
Write-Host "In Process Explorer: Press Ctrl+F and search for the file path to highlight the owning process." -ForegroundColor Yellow
./systeminternals/procexp64.exe /accepteula

Write-Host ""
Write-Host "=== Investigation Complete ===" -ForegroundColor Cyan
