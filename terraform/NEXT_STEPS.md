# path: terraform/NEXT_STEPS.md

# Next steps after Phase 16

Phase 16 adds Amazon RDS PostgreSQL to the existing AWS foundation.

## What was added

- DB subnet group using the existing private subnets
- Amazon RDS PostgreSQL instance
- private-only database networking
- encrypted storage
- AWS-managed master password in Secrets Manager
- Terraform outputs required for deployment

## Commands to run

From repository root:

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```
