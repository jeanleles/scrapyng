$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path '.venv\Scripts\python.exe')) {
  throw 'Ambiente virtual nao encontrado. Crie-o com: py -m venv .venv'
}

$env:FLASK_DEBUG = if ($env:FLASK_DEBUG) { $env:FLASK_DEBUG } else { 'true' }
$env:PORT = if ($env:PORT) { $env:PORT } else { '5555' }

& .venv\Scripts\python.exe app.py