# Simple Production Test for Vortex API
# ========================================

param(
    [string]$ApiUrl = "https://vortex-automotive-analytics-1.onrender.com"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VORTEX API PRODUCTION TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Testing API: $ApiUrl" -ForegroundColor Yellow
Write-Host ""

$ErrorActionPreference = 'Continue'

# Test 1: Root
Write-Host "[1] Testing Root Endpoint... " -NoNewline
try {
    $result = Invoke-RestMethod -Uri "$ApiUrl/" -TimeoutSec 30
    Write-Host "[OK]" -ForegroundColor Green
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 2: Health
Write-Host "[2] Testing Health Check... " -NoNewline
try {
    $health = Invoke-RestMethod -Uri "$ApiUrl/health" -TimeoutSec 30
    Write-Host "[OK]" -ForegroundColor Green
    Write-Host "    Database: $($health.database)" -ForegroundColor DarkGray
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 3: Vehicles
Write-Host "[3] Testing Get Vehicles... " -NoNewline
try {
    $vehicles = Invoke-RestMethod -Uri "$ApiUrl/api/v1/data/vehicles?limit=5" -TimeoutSec 30
    Write-Host "[OK] - Count: $($vehicles.Count)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 4: Sales
Write-Host "[4] Testing Get Sales... " -NoNewline
try {
    $sales = Invoke-RestMethod -Uri "$ApiUrl/api/v1/data/sales?limit=5" -TimeoutSec 30
    Write-Host "[OK] - Count: $($sales.Count)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 5: Inventory
Write-Host "[5] Testing Get Inventory... " -NoNewline
try {
    $inventory = Invoke-RestMethod -Uri "$ApiUrl/api/v1/data/inventory?limit=5" -TimeoutSec 30
    Write-Host "[OK] - Count: $($inventory.Count)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Calculate dates for analytics
$endDate = Get-Date -Format "yyyy-MM-dd"
$startDate = (Get-Date).AddDays(-30).ToString("yyyy-MM-dd")

# Test 6: KPIs
Write-Host "[6] Testing Get KPIs... " -NoNewline
try {
    $kpisUrl = '{0}/api/analytics/kpis?start_date={1}&end_date={2}' -f $ApiUrl, $startDate, $endDate
    $kpis = Invoke-RestMethod -Uri $kpisUrl -TimeoutSec 30
    Write-Host "[OK]" -ForegroundColor Green
    Write-Host "    Revenue: $$($kpis.total_revenue)" -ForegroundColor DarkGray
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 7: Top Vehicles
Write-Host "[7] Testing Top Vehicles... " -NoNewline
try {
    $top = Invoke-RestMethod -Uri "$ApiUrl/api/analytics/top-vehicles?limit=5" -TimeoutSec 30
    Write-Host "[OK] - Count: $($top.Count)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

# Test 8: Inventory Analytics
Write-Host "[8] Testing Inventory Analytics... " -NoNewline
try {
    $invAnalytics = Invoke-RestMethod -Uri "$ApiUrl/api/analytics/inventory" -TimeoutSec 30
    Write-Host "[OK]" -ForegroundColor Green
    Write-Host "    Total Units: $($invAnalytics.total_units)" -ForegroundColor DarkGray
} catch {
    Write-Host "[FAIL]" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Documentation: $ApiUrl/docs" -ForegroundColor Yellow
Write-Host ""

