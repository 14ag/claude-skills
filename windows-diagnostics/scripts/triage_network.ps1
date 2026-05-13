# triage_network.ps1 - Automate network connection triage (Recipe b)
# Usage: .\triage_network.ps1 -RemoteIP "203.0.113.42"

param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteIP
)

$ErrorActionPreference = "Stop"

Write-Host "=== Network Connection Triage ===" -ForegroundColor Cyan
Write-Host "Target IP: $RemoteIP" -ForegroundColor Yellow
Write-Host ""

# Step 1 — list all connections with owning process
Write-Host "[1/4] Listing all network connections..." -ForegroundColor Green
./systeminternals/tcpvcon64.exe -accepteula -a -c > ./tcpvcon_out.csv

# Validation: Check if output file was created
if (!(Test-Path ./tcpvcon_out.csv)) {
    Write-Error "tcpvcon64 failed. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if target IP is in output
if (!(Select-String -Path ./tcpvcon_out.csv -Pattern $RemoteIP)) {
    Write-Warning "Target IP not found in connections. Verify IP address or check if connection closed."
    exit 1
}

# Parse CSV to find owning process
$connection = Import-Csv ./tcpvcon_out.csv | Where-Object { $_.'Remote Address' -eq $RemoteIP } | Select-Object -First 1

if ($connection) {
    Write-Host "Connection found:" -ForegroundColor Green
    Write-Host "  Process: $($connection.Process)" -ForegroundColor Yellow
    Write-Host "  PID: $($connection.PID)" -ForegroundColor Yellow
    Write-Host "  Local: $($connection.'Local Address'):$($connection.'Local Port')" -ForegroundColor Yellow
    Write-Host "  Remote: $($connection.'Remote Address'):$($connection.'Remote Port')" -ForegroundColor Yellow
    Write-Host "  State: $($connection.State)" -ForegroundColor Yellow
    Write-Host ""
    
    $processPath = $connection.Process
} else {
    Write-Error "Could not parse connection information from CSV"
    exit 1
}

# Step 2 — WHOIS the remote IP
Write-Host "[2/4] Looking up WHOIS information..." -ForegroundColor Green
./systeminternals/whois64.exe -accepteula $RemoteIP
Write-Host ""

# Step 3 — verify the owning process binary signature
Write-Host "[3/4] Verifying process signature..." -ForegroundColor Green
./systeminternals/sigcheck64.exe -accepteula -v $processPath

# Validation: Verify sigcheck64 completed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "sigcheck64 failed. Possible causes: file not found, access denied, or network issue."
    exit 1
}
Write-Host ""

# Step 4 — capture traffic window
Write-Host "[4/4] Launching NetworkTrafficView for traffic capture..." -ForegroundColor Green
Write-Warning "NetworkTrafficView will capture network traffic. Captured data may contain credentials or sensitive information."
Write-Host "Filter by remote IP: $RemoteIP" -ForegroundColor Yellow
./nirsoft/NetworkTrafficView.exe /stext ./ntv_out.txt

Write-Host ""
Write-Host "=== Triage Complete ===" -ForegroundColor Cyan
Write-Host "Review ./tcpvcon_out.csv and ./ntv_out.txt for detailed information" -ForegroundColor Yellow
