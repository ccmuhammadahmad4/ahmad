# DevSecOps Pipeline

## Project Overview
This project adds security scanning to a CI/CD pipeline using Trivy for container vulnerabilities and SonarQube for code quality.

## Tools Used
- Trivy
- SonarQube
- GitHub Actions
- Docker

## Setup Instructions
1. Install Trivy and SonarQube locally or via Docker
2. Configure GitHub Actions workflow
3. Set up sample web app repository

## Implementation Steps
- Scan Docker images for vulnerabilities using Trivy
- Analyze code quality with SonarQube
- Fail builds on critical issues
- Generate security reports and upload artifacts

## Bonus Tasks
- Integrate with Jira or GitHub Issues
- Add dependency scanning with Snyk or OWASP tools
- Automate security policy enforcement
