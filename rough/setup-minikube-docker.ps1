<#!
.SYNOPSIS
  Setup Minikube on Windows using Docker Desktop (no extra VM required).
.DESCRIPTION
  - Checks prerequisites (Admin, Docker Desktop)
  - Installs Chocolatey (if missing)
  - Installs kubectl and minikube (if missing)
  - Starts a Minikube cluster with Docker driver
  - Optionally opens the Kubernetes dashboard
.NOTES
  Run this script in PowerShell as Administrator.
  Save as: setup-minikube-docker.ps1
#>

param(
  [string] $ProfileName = "minikube-docker",
  [int]    $CPUs        = 2,
  [int]    $MemoryMB    = 4096,
  [switch] $OpenDashboard,
  [switch] $Force
)

function Assert-Admin {
  $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
  if (-not $isAdmin) {
    Write-Error "Please run PowerShell as Administrator."
    exit 1
  }
}

function Ensure-Chocolatey {
  if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Chocolatey found." -ForegroundColor Green
    return
  }
  Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
  Set-ExecutionPolicy Bypass -Scope Process -Force
  [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
  Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
  if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Error "Chocolatey installation failed. Install manually from https://chocolatey.org/install"
    exit 1
  }
}

function Ensure-Package($name) {
  if (Get-Command $name -ErrorAction SilentlyContinue) {
    Write-Host "$name already installed." -ForegroundColor Green
  } else {
    Write-Host "Installing $name via Chocolatey..." -ForegroundColor Yellow
    choco install $name -y --no-progress
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
      Write-Error "Failed to install $name."
      exit 1
    }
  }
}

function Ensure-DockerRunning {
  # Check docker CLI
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI not found. Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
  }
  # Try docker ping
  try {
    docker version --format '{{.Server.Version}}' | Out-Null
  } catch {
    Write-Host "Attempting to start Docker Desktop service..." -ForegroundColor Yellow
    try { Start-Service -Name com.docker.service -ErrorAction Stop } catch {}
    Start-Sleep -Seconds 5
  }
  $maxWait = 60
  $elapsed = 0
  while ($elapsed -lt $maxWait) {
    try {
      docker version --format '{{.Server.Version}}' | Out-Null
      Write-Host "Docker Desktop is running." -ForegroundColor Green
      return
    } catch {
      Start-Sleep -Seconds 3
      $elapsed += 3
    }
  }
  Write-Error "Docker Desktop is not running. Launch Docker Desktop and try again."
  exit 1
}

function Start-MinikubeCluster {
  $args = @(
    'start',
    "--driver=docker",
    "--cpus=$CPUs",
    "--memory=${MemoryMB}",
    "--profile=$ProfileName"
  )
  if ($Force) { $args += '--force' }
  Write-Host "Starting Minikube: minikube $($args -join ' ')" -ForegroundColor Cyan
  & minikube @args
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Minikube start failed."
    exit 1
  }
  Write-Host "Setting current context to profile $ProfileName" -ForegroundColor Green
  & minikube profile $ProfileName | Out-Null
}

function Verify-Cluster {
  Write-Host "Cluster status:" -ForegroundColor Cyan
  & minikube -p $ProfileName status
  Write-Host "Kubernetes nodes:" -ForegroundColor Cyan
  & kubectl get nodes -o wide
}

function Open-DashboardIfRequested {
  if ($OpenDashboard) {
    Write-Host "Opening Kubernetes dashboard..." -ForegroundColor Cyan
    & minikube -p $ProfileName dashboard --url
  }
}

# -------- Main --------
Assert-Admin
Ensure-DockerRunning
Ensure-Chocolatey
Ensure-Package kubernetes-cli
Ensure-Package minikube
Start-MinikubeCluster
Verify-Cluster
Open-DashboardIfRequested

Write-Host "\nDone! Use the following commands next:" -ForegroundColor Green
Write-Host "  kubectl get pods -A" -ForegroundColor Gray
Write-Host "  minikube -p $ProfileName dashboard" -ForegroundColor Gray
Write-Host "  minikube stop -p $ProfileName" -ForegroundColor Gray
Write-Host "  minikube delete -p $ProfileName" -ForegroundColor Gray
