# Cài đặt trên Windows. Chạy: powershell -ExecutionPolicy Bypass -File setup.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$ok = $true
foreach ($c in "node","npm","python","ffmpeg") {
  if (Get-Command $c -ErrorAction SilentlyContinue) { Write-Host "OK $c" }
  else { Write-Host "THIEU $c  (winget install OpenJS.NodeJS.LTS / Python.Python.3.12 / Gyan.FFmpeg)"; $ok = $false }
}
if (-not $ok) { Write-Host "Cai cac cong cu con thieu roi chay lai."; exit 1 }
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\pip install -q -r requirements.txt
npm install --silent
if (-not (Test-Path config\machine.yaml)) { Copy-Item config\machine.example.yaml config\machine.yaml }
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Xong. Dien .env, kiem tra config\machine.yaml, roi chay: .\.venv\Scripts\python core\scripts\doctor.py"
