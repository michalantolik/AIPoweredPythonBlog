# Terraform infrastructure for AI Powered Python Blog

This folder contains the first AWS infrastructure layer for the project.

## Scope of this phase

This Terraform setup currently provisions:

- VPC
- 2 public subnets
- 2 private subnets
- Internet Gateway
- Route tables
- Optional NAT Gateway
- Security group for the future app
- Security group for the future PostgreSQL database

This phase does **not** yet provision:

- Amazon ECR
- Amazon RDS
- App Runner / ECS / EC2 deployment
- Kubernetes / EKS

Those should be added in the next phases.

---

## How to use

### 1. Copy the example variables file

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
