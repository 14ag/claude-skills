# memory_leak_check.ps1 - Automate memory leak investigation (Recipe c)
# Usage: .\memory_leak_check.ps1 [-PID <process_id>]

param(
    [Parameter(Mandatory=$false)]
    [int]$PID
)

$ErrorActionPreference = "Stop"

Write-Host "=== Memory Leak Investigation ===" -ForegroundColor Cyan
Write-Host ""

# Validation: Check if shell is elevated (required for memory tools)
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Error "Administrator privileges required for RAMMap64 and vmmap64. Relaunch shell as administrator."
    exit 1
}

# Step 1 — review physical memory breakdown
if (!$PID) {
    Write-Host "[1/3] Launching RAMMap64 to identify memory consumers..." -ForegroundColor Green
    Write-Host "Instructions: Check 'Process Private' tab for largest consumers and note the PID" -ForegroundColor Yellow
    ./systeminternals/RAMMap64.exe /accepteula
    
    # Prompt for PID
    Write-Host ""
    $PID = Read-Host "Enter PID of suspect process from RAMMap64"
    if (!$PID -or $PID -notmatch '^\d+$') {
        Write-Error "Invalid PID. Must be a numeric process ID."
        exit 1
    }
}

Write-Host ""
Write-Host "Investigating PID: $PID" -ForegroundColor Yellow
Write-Host ""

# Step 2 — inspect virtual memory layout of suspect process
Write-Host "[2/3] Launching vmmap64 to inspect memory layout..." -ForegroundColor Green
Write-Host "Instructions: Look for large Private Data or Heap regions" -ForegroundColor Yellow
./systeminternals/vmmap64.exe -accepteula $PID

Write-Host ""
$confirm = Read-Host "Capture memory dump? (y/n)"

if ($confirm -eq 'y') {
    # Step 3 — capture dump if leak is confirmed
    Write-Host "[3/3] Capturing memory dump..." -ForegroundColor Green
    $dumpPath = "./memleak_$PID.dmp"
    ./systeminternals/procdump64.exe -accepteula -ma $PID $dumpPath
    
    # Validation: Verify dump was created
    if (!(Test-Path $dumpPath)) {
        Write-Error "procdump64 failed to create dump. Check if process still exists and shell is elevated."
        exit 1
    }
    
    # Report dump path to user for analysis with WinDbg or Visual Studio
    $dumpSize = (Get-Item $dumpPath).Length / 1MB
    Write-Host ""
    Write-Host "=== Dump Created ===" -ForegroundColor Cyan
    Write-Host "Path: $dumpPath" -ForegroundColor Yellow
    Write-Host "Size: $($dumpSize.ToString('F2')) MB" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Analyze with WinDbg: windbg -z $dumpPath" -ForegroundColor Green
    Write-Host "Or Visual Studio: devenv /debugexe $dumpPath" -ForegroundColor Green
} else {
    Write-Host "Dump capture cancelled" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Investigation Complete ===" -ForegroundColor Cyan
