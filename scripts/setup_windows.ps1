# Windows PowerShell Setup Script for ERP System
# Run this script from the ERP_SYSTEM root directory

Write-Host "=== ERP System Setup Script ===" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Check PostgreSQL installation
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
$pgVersion = psql --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: PostgreSQL may not be installed or not in PATH" -ForegroundColor Yellow
    Write-Host "Please ensure PostgreSQL is installed and added to PATH" -ForegroundColor Yellow
} else {
    Write-Host "Found: $pgVersion" -ForegroundColor Green
}

# Navigate to backend directory
Set-Location -Path "backend"

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create .env file in backend/ directory (see SETUP_GUIDE.md)" -ForegroundColor White
Write-Host "2. Create PostgreSQL database: erp_db" -ForegroundColor White
Write-Host "3. Run: python manage.py migrate" -ForegroundColor White
Write-Host "4. Run: python manage.py createsuperuser" -ForegroundColor White
Write-Host "5. Run: python manage.py runserver" -ForegroundColor White

