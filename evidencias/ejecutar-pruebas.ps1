$Host.UI.RawUI.WindowTitle = 'Taller3 - Pytest'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Clear-Host
Write-Host "=== Pruebas automatizadas de la API ===" -ForegroundColor Cyan
Write-Host "Proyecto: C:\Users\doleh\Downloads\taller3-api" -ForegroundColor DarkGray
Write-Host ""
Write-Host "python -m pytest -v" -ForegroundColor Yellow
Write-Host ""
Set-Location "C:\Users\doleh\Downloads\taller3-api"
python -m pytest -v --no-header -p no:cacheprovider 2>&1 | Select-Object -First 22
Write-Host ""
Write-Host "=== Fin ===" -ForegroundColor Cyan
