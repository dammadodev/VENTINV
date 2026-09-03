# Script para inicializar y subir VENTINV a GitHub (dammado.dev)

$repoUrl = "https://github.com/dammado.dev/VENTINV.git"

Write-Host "Checking Git installation..." -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found in PATH. Installing Git via winget..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
    
    # Update PATH for current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "Initializing Git Repository..." -ForegroundColor Green
    git init
    git add .
    git commit -m "Inicialización del sistema VENTINV (Ventas e Inventario Django)"
    git branch -M main
    
    # Remove existing remote if present
    git remote remove origin 2>$null
    git remote add origin $repoUrl
    
    Write-Host "Pushing code to GitHub ($repoUrl)..." -ForegroundColor Green
    git push -u origin main
    
    Write-Host "Done! VENTINV code successfully uploaded to GitHub." -ForegroundColor Green
} else {
    Write-Host "Please complete the Git installer UAC prompt on your screen, then re-run this script." -ForegroundColor Red
}
