# path: terraform/README.md

# Terraform infrastructure for AI Powered Python Blog

This folder contains the AWS infrastructure for the project.

## Current scope

This Terraform setup now provisions:

- VPC
- 2 public subnets
- 2 private subnets
- Internet Gateway
- Route tables
- Optional NAT Gateway
- Security group for the future app
- Security group for PostgreSQL
- Amazon ECR repository
- Amazon RDS for PostgreSQL
- DB subnet group for RDS

## Not yet included

This phase still does **not** provision:

- ECS / EC2 / App Runner deployment
- Load balancer
- Domain / TLS
- Kubernetes / EKS

Those belong to the next phases.

---

## How to use

### 1. Copy the example variables file

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
