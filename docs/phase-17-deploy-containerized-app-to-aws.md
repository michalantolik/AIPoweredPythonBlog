# Phase 17 — Deploy the containerized app to AWS

This phase deploys the Django blog application to AWS using:

- Amazon ECR for the Docker image
- AWS App Runner for the running web service
- Amazon RDS for PostgreSQL
- AWS Secrets Manager for Django SECRET_KEY
- Terraform for infrastructure provisioning

## Architecture

- The Docker image is built and pushed to Amazon ECR.
- AWS App Runner pulls the image from ECR.
- App Runner uses a VPC connector to reach the private PostgreSQL database in RDS.
- The Django `SECRET_KEY` is stored in Secrets Manager.
- RDS credentials are injected into App Runner as a secret environment variable and parsed by Django from `DJANGO_DB_SECRET_JSON`.

## Notes

- Make sure the ECR repository already contains an image tagged `latest` before applying Terraform.
- App Runner is configured with automatic deployments from same-account ECR.
- The first VPC connector creation can take a few minutes.
- If a secret value changes, redeploy the App Runner service so the new value is loaded.

## Manual run

From repository root:

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
