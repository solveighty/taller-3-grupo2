$base = "http://localhost:8000"
$Host.UI.RawUI.WindowTitle = 'Taller3 - API'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Linea { param($t) Write-Host $t -ForegroundColor DarkGray }

Clear-Host
Write-Host "=== API de Inventario y Pedidos - Comercial Andina Digital S.A.S. ===" -ForegroundColor Cyan
Write-Host "Servidor: $base   |   Documentacion: $base/docs" -ForegroundColor DarkGray
Write-Host ""

Write-Host "1) Peticion SIN token a un endpoint protegido" -ForegroundColor Yellow
Linea '   curl.exe -w "\nHTTP %{http_code}\n" http://localhost:8000/api/v1/productos'
curl.exe -s -w "`nHTTP %{http_code}`n" "$base/api/v1/productos"
Write-Host ""

Write-Host "2) Obtencion del token JWT" -ForegroundColor Yellow
Linea '   curl.exe -X POST -d "username=analista&password=Andina2026!" http://localhost:8000/api/v1/token'
$respuesta = curl.exe -s -X POST -d "username=analista&password=Andina2026!" "$base/api/v1/token"
$respuesta
$token = ($respuesta | ConvertFrom-Json).access_token
Write-Host ("   Token recibido: " + $token.Substring(0, 45) + "...") -ForegroundColor Green
Write-Host ""

Write-Host "3) Misma peticion CON el token en el encabezado Authorization" -ForegroundColor Yellow
Linea '   curl.exe -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/productos'
curl.exe -s -w "`nHTTP %{http_code}`n" -H "Authorization: Bearer $token" "$base/api/v1/productos"
Write-Host ""

Write-Host "4) Consulta de un recurso inexistente (404)" -ForegroundColor Yellow
Linea '   curl.exe -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/productos/NO-EXISTE'
curl.exe -s -w "`nHTTP %{http_code}`n" -H "Authorization: Bearer $token" "$base/api/v1/productos/NO-EXISTE"
Write-Host ""

Write-Host "5) Credenciales incorrectas en /token (401)" -ForegroundColor Yellow
Linea '   curl.exe -X POST -d "username=analista&password=incorrecta" http://localhost:8000/api/v1/token'
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST -d "username=analista&password=incorrecta" "$base/api/v1/token"
Write-Host ""
Write-Host "=== Fin de la secuencia ===" -ForegroundColor Cyan
