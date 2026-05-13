# launch-form.ps1
# Launched by the project-docs skill when required metadata is missing.
# Usage: .\launch-form.ps1 [-MissingFields "name,description,email"] [-PreFilled @{license="MIT"}]
#
# The script:
#  1. Copies form.html to a temp location
#  2. Substitutes pre-filled values as URL query params
#  3. Starts a minimal HTTP listener on localhost to capture form submission
#  4. Opens the browser to the form
#  5. Waits for submission and writes the JSON result to ./doc-metadata.json
#  6. Outputs the JSON path for the calling skill to read

param(
    [string]$MissingFields = "",   # comma-separated list of field IDs to show
    [hashtable]$PreFilled = @{},   # already-known values (field => value)
    [int]$Port = 0,                # 0 = auto-pick a free port
    [string]$OutputPath = ".\doc-metadata.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── 1. Find a free port ────────────────────────────────────────────────────────
if ($Port -eq 0) {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $Port = $listener.LocalEndpoint.Port
    $listener.Stop()
}

# ── 2. Build the query string from pre-filled values ──────────────────────────
$qParts = @()
foreach ($kv in $PreFilled.GetEnumerator()) {
    $enc = [Uri]::EscapeDataString($kv.Value)
    $qParts += "$($kv.Key)=$enc"
}
$query = if ($qParts.Count -gt 0) { "?" + ($qParts -join "&") } else { "" }

# ── 3. Copy form.html to temp, inject the port ────────────────────────────────
$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceHtml = Join-Path $scriptDir "form.html"
$tmpHtml    = Join-Path $env:TEMP "project-docs-form-$Port.html"

$html = Get-Content $sourceHtml -Raw
$html = $html -replace "__PORT__", $Port
Set-Content $tmpHtml $html -Encoding UTF8

# ── 4. Start HTTP listener ────────────────────────────────────────────────────
$httpListener = [System.Net.HttpListener]::new()
$httpListener.Prefixes.Add("http://localhost:$Port/")
$httpListener.Start()
Write-Host "⏳ Waiting for form submission on http://localhost:$Port ..." -ForegroundColor Cyan

# ── 5. Open browser ───────────────────────────────────────────────────────────
$fileUrl = "file:///" + ($tmpHtml -replace "\\", "/") + $query
Start-Process $fileUrl
Write-Host "🌐 Browser opened: $fileUrl" -ForegroundColor Green

# ── 6. Wait for POST /submit ──────────────────────────────────────────────────
$resultJson = $null
while ($null -eq $resultJson) {
    $ctx = $httpListener.GetContext()
    $req = $ctx.Request
    $res = $ctx.Response

    # Allow browser CORS pre-flight
    $res.Headers.Add("Access-Control-Allow-Origin", "*")
    $res.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
    $res.Headers.Add("Access-Control-Allow-Methods", "POST, OPTIONS")

    if ($req.HttpMethod -eq "OPTIONS") {
        $res.StatusCode = 204
        $res.Close()
        continue
    }

    if ($req.HttpMethod -eq "POST" -and $req.Url.AbsolutePath -eq "/submit") {
        $reader     = [System.IO.StreamReader]::new($req.InputStream, $req.ContentEncoding)
        $resultJson = $reader.ReadToEnd()
        $reader.Close()

        $responseBytes = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok"}')
        $res.ContentType   = "application/json"
        $res.ContentLength64 = $responseBytes.Length
        $res.OutputStream.Write($responseBytes, 0, $responseBytes.Length)
        $res.Close()
        break
    }

    # Serve static assets if needed
    $res.StatusCode = 404
    $res.Close()
}

$httpListener.Stop()

# ── 7. Write output ───────────────────────────────────────────────────────────
if ($resultJson) {
    Set-Content -Path $OutputPath -Value $resultJson -Encoding UTF8
    Write-Host ""
    Write-Host "✅ Metadata saved to: $OutputPath" -ForegroundColor Green
    Write-Host $resultJson
} else {
    Write-Warning "No submission received."
    exit 1
}

# Clean up temp html
Remove-Item $tmpHtml -ErrorAction SilentlyContinue
