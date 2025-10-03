# Start demo script: activates venv, starts Flask app, and opens browser
# Run from project root in PowerShell

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual env activation script not found. Make sure .venv exists and is created." -ForegroundColor Yellow
}
else {
    Write-Host "Activating venv..."
    & .venv\Scripts\Activate.ps1
}

Write-Host "Starting Flask app in new window..."
Start-Process -FilePath "$PWD\.venv\Scripts\python.exe" -ArgumentList '-m','src.webapp'
Start-Sleep -Seconds 1
Write-Host "Opening browser..."
Start-Process "http://127.0.0.1:5000/"
