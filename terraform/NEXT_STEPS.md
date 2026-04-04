2. Authenticate to AWS

Make sure your AWS credentials are available in your shell, for example through:

aws configure
AWS SSO
environment variables
3. Initialize Terraform
cd terraform
terraform init
4. Validate
terraform validate
5. Review the execution plan
terraform plan -var-file=dev.tfvars
6. Apply
terraform apply -var-file=dev.tfvars
7. Destroy when needed
terraform destroy -var-file=dev.tfvars
Notes
NAT Gateway is disabled by default to avoid unnecessary cost during the first infrastructure phase.
The DB security group already allows PostgreSQL access from the future app security group.
The private subnets are intended for the future database and private app connectivity.

---

# Why this is the right scope for Phase 13

Because your roadmap separates the next work into:

- Terraform infra
- ECR
- RDS
- deployment
- Kubernetes later

So this phase should create only the **foundation**.

That gives you a clean sequence:

1. **Phase 13** → Terraform base infra  
2. **Phase 14** → add ECR resources + image push pipeline  
3. **Phase 15** → add RDS resources  
4. **Phase 16** → deploy the app runtime  
5. **Phase 17** → only then evaluate Kubernetes

---

# Commands to run after adding files

From repo root:

```bash
cp terraform/dev.tfvars.example terraform/dev.tfvars
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan -var-file=dev.tfvars
Recommended commit message
Add Terraform foundation for AWS networking and security groups
Important implementation note

For this repository, I recommend keeping Terraform at the repo root rather than inside the Django app folder.
That is cleaner because Terraform manages the whole deployment platform, not the Python package itself.