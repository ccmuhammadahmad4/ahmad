# Infrastructure as Code with Terraform

## Project Overview
This project provisions cloud infrastructure using Terraform on AWS, including VPC, EC2, RDS, and S3 resources.

## Tools Used
- Terraform
- AWS
- Git

## Setup Instructions
1. Install Terraform CLI
2. Configure AWS credentials
3. Create Git repository for Terraform code

## Implementation Steps
- Write Terraform code to create VPC with public/private subnets
- Provision EC2 instances with security groups
- Create RDS database and S3 bucket
- Use Terraform modules for reusable components
- Configure remote state with S3 and DynamoDB

## Bonus Tasks
- Add Terraform workspaces for environment separation
- Implement CI/CD for Terraform using GitHub Actions
- Use Terraform Cloud or Terragrunt for advanced workflows
