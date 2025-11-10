# GitOps with ArgoCD

## Project Overview
This project implements GitOps using ArgoCD to manage Kubernetes deployments directly from Git repositories.

## Tools Used
- ArgoCD
- Kubernetes
- GitHub
- Helm / Kustomize

## Setup Instructions
1. Install Kubernetes cluster
2. Deploy ArgoCD using Helm or manifests
3. Create Git repository with app manifests

## Implementation Steps
- Configure ArgoCD to sync with Git repository
- Deploy app using Helm or Kustomize
- Automate sync and rollback
- Set up RBAC and audit logging

## Bonus Tasks
- Add multi-environment support
- Integrate ArgoCD notifications
- Use ArgoCD Image Updater for auto-deployments
