# Restart all apps with monitoring enabled

Write-Host "`n🔄 Restarting all applications with Prometheus monitoring..." -ForegroundColor Cyan

# Kill existing python processes on ports 5001-5005
Write-Host "`n📛 Stopping existing apps..." -ForegroundColor Yellow
for ($port = 5001; $port -le 5005; $port++) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    if ($process) {
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped app on port $port" -ForegroundColor Green
    }
}

Start-Sleep -Seconds 2

# Start all apps with venv activated
Write-Host "`n🚀 Starting apps with monitoring..." -ForegroundColor Cyan

for ($i = 1; $i -le 5; $i++) {
    $port = 5000 + $i
    $appDir = "app$i"
    
    Write-Host "  Starting App$i on port $port..." -ForegroundColor Yellow
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd c:\Users\muhammadahmad4\applications
        .\.venv\Scripts\Activate.ps1
        cd $appDir
        Write-Host 'App$i running on port $port with Prometheus metrics' -ForegroundColor Green
        python main.py
"@
    
    Start-Sleep -Milliseconds 500
}

Write-Host "`n✅ All apps started!" -ForegroundColor Green
Write-Host "`n📊 Monitoring URLs:" -ForegroundColor Cyan
Write-Host "  Grafana:    http://localhost:3000 (admin/admin123)" -ForegroundColor White
Write-Host "  Prometheus: http://localhost:9090" -ForegroundColor White

Write-Host "`n📈 App Metrics:" -ForegroundColor Cyan
for ($i = 1; $i -le 5; $i++) {
    $port = 5000 + $i
    Write-Host "  App$i: http://localhost:$port/metrics" -ForegroundColor White
}

Write-Host "`n🌐 Applications:" -ForegroundColor Cyan
Write-Host "  http://172.25.25.140/app1/" -ForegroundColor White
Write-Host "  http://172.25.25.140/app2/" -ForegroundColor White
Write-Host "  http://172.25.25.140/app3/" -ForegroundColor White
Write-Host "  http://172.25.25.140/app4/" -ForegroundColor White
Write-Host "  http://172.25.25.140/app5/" -ForegroundColor White

Write-Host "`n⏳ Waiting 5 seconds for apps to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test metrics endpoints
Write-Host "`n🔍 Verifying metrics endpoints..." -ForegroundColor Cyan
for ($i = 1; $i -le 5; $i++) {
    $port = 5000 + $i
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/metrics" -UseBasicParsing -TimeoutSec 2
        Write-Host "  ✓ App$i metrics available" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ App$i metrics not yet available (may need more time)" -ForegroundColor Yellow
    }
}

Write-Host "`n🎉 Setup complete!" -ForegroundColor Green
Write-Host "Open Grafana and search for 'App1', 'App2', etc. to see individual dashboards!" -ForegroundColor Cyan
