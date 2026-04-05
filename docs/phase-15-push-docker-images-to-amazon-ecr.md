# Phase 15 — Push Docker images to Amazon ECR

This phase adds:

- an Amazon ECR repository in Terraform
- a GitHub Actions workflow that builds the Docker image
- Docker image push to Amazon ECR on every push to `main`
- support for manual workflow runs via `workflow_dispatch`

---

## What this phase does not do yet

This phase does **not** deploy the application.

It only prepares the image pipeline so that later phases can pull the image from ECR and run it on AWS.

---

## 1. Create the ECR repository with Terraform

From the repository root:

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
