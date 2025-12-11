# PowerShell Script to Create Django Project and Apps
# Run this script from the ERP_SYSTEM root directory

Write-Host "=== Django Project Setup Script ===" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "backend\venv")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup_windows.ps1 first or create venv manually" -ForegroundColor Yellow
    exit 1
}

# Navigate to backend directory
Set-Location -Path "backend"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if Django is installed
Write-Host ""
Write-Host "Checking Django installation..." -ForegroundColor Yellow
$djangoVersion = python -m django --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Django is not installed!" -ForegroundColor Red
    Write-Host "Please install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host "Found Django: $djangoVersion" -ForegroundColor Green

# Check if project already exists
if (Test-Path "erp_core") {
    Write-Host ""
    Write-Host "WARNING: Django project 'erp_core' already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to continue? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit 1
    }
} else {
    # Create Django project
    Write-Host ""
    Write-Host "Creating Django project 'erp_core'..." -ForegroundColor Yellow
    django-admin startproject erp_core .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Django project created successfully!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create Django project" -ForegroundColor Red
        exit 1
    }
}

# Define apps to create
$apps = @("inventory", "vendors", "clients", "purchases", "sales", "accounts")

# Create apps
Write-Host ""
Write-Host "Creating Django apps..." -ForegroundColor Yellow
foreach ($app in $apps) {
    if (Test-Path $app) {
        Write-Host "  App '$app' already exists, skipping..." -ForegroundColor Yellow
    } else {
        Write-Host "  Creating app: $app" -ForegroundColor Cyan
        python manage.py startapp $app
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✓ Created successfully" -ForegroundColor Green
        } else {
            Write-Host "    ✗ Failed to create" -ForegroundColor Red
        }
    }
}

# Create migrations
Write-Host ""
Write-Host "Creating initial migrations..." -ForegroundColor Yellow
python manage.py makemigrations
if ($LASTEXITCODE -eq 0) {
    Write-Host "Migrations created successfully!" -ForegroundColor Green
} else {
    Write-Host "WARNING: No migrations created (this is normal for new apps)" -ForegroundColor Yellow
}

# Apply migrations
Write-Host ""
Write-Host "Applying migrations..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "Migrations applied successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to apply migrations" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit erp_core/settings.py and add all apps to INSTALLED_APPS" -ForegroundColor White
Write-Host "2. Create urls.py files in each app directory" -ForegroundColor White
Write-Host "3. Configure erp_core/urls.py to include app URLs" -ForegroundColor White
Write-Host "4. Create superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "5. Run server: python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "See docs/DJANGO_PROJECT_SETUP.md for detailed instructions" -ForegroundColor Yellow

