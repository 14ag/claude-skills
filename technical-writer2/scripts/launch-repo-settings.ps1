# launch-repo-settings.ps1
param(
    [string]$SuggestedTopics = "",
    [int]$Port = 0,
    [string]$OutputPath = ".\repo-settings.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Port -eq 0) {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $Port = $listener.LocalEndpoint.Port
    $listener.Stop()
}

$enc = [Uri]::EscapeDataString($SuggestedTopics)
$query = "?suggestions=$enc"

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceHtml = Join-Path $scriptDir "repo-settings.html"
$tmpHtml    = Join-Path $env:TEMP "repo-settings-form-$Port.html"

$html = Get-Content $sourceHtml -Raw
$html = $html -replace "__PORT__", $Port
Set-Content $tmpHtml $html -Encoding UTF8

$httpListener = [System.Net.HttpListener]::new()
$httpListener.Prefixes.Add("http://localhost:$Port/")
$httpListener.Start()
Write-Host "⏳ Waiting for repository settings submission on http://localhost:$Port ..." -ForegroundColor Cyan

$fileUrl = "file:///" + ($tmpHtml -replace "\\", "/") + $query
Start-Process $fileUrl
Write-Host "🌐 Browser opened: $fileUrl" -ForegroundColor Green

$resultJson = $null
while ($null -eq $resultJson) {
    $ctx = $httpListener.GetContext()
    $req = $ctx.Request
    $res = $ctx.Response

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

    $res.StatusCode = 404
    $res.Close()
}

$httpListener.Stop()

if ($resultJson) {
    Set-Content -Path $OutputPath -Value $resultJson -Encoding UTF8
    Write-Host ""
    Write-Host "✅ Settings saved to: $OutputPath" -ForegroundColor Green
    Write-Host $resultJson
} else {
    Write-Warning "No submission received."
    exit 1
}

Remove-Item $tmpHtml -ErrorAction SilentlyContinue
