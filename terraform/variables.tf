# path: terraform/variables.tf

variable "project_name" {
  description = "Project name used in resource naming."
  type        = string
  default     = "ai-powered-python-blog"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for infrastructure."
  type        = string
  default     = "eu-central-1"
}

variable "owner" {
  description = "Owner tag value."
  type        = string
  default     = "michal"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets."
  type        = list(string)
  default = [
    "10.20.1.0/24",
    "10.20.2.0/24"
  ]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets."
  type        = list(string)
  default = [
    "10.20.11.0/24",
    "10.20.12.0/24"
  ]
}

variable "enable_nat_gateway" {
  description = "Whether to provision a NAT gateway for private subnet outbound internet access."
  type        = bool
  default     = false
}

variable "db_port" {
  description = "PostgreSQL port."
  type        = number
  default     = 5432
}

variable "ecr_repository_name" {
  description = "Amazon ECR repository name used for Docker image pushes."
  type        = string
  default     = "ai-powered-python-blog"
}

variable "rds_db_name" {
  description = "Initial database name created in the PostgreSQL instance."
  type        = string
  default     = "ai_powered_blog"
}

variable "rds_db_username" {
  description = "Master username for the PostgreSQL instance."
  type        = string
  default     = "blog_admin"
}

variable "rds_instance_class" {
  description = "Amazon RDS instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Initial allocated storage size in GB."
  type        = number
  default     = 20
}

variable "rds_max_allocated_storage" {
  description = "Maximum storage autoscaling limit in GB."
  type        = number
  default     = 100
}

variable "rds_storage_type" {
  description = "Amazon RDS storage type."
  type        = string
  default     = "gp3"
}

variable "rds_multi_az" {
  description = "Whether to enable Multi-AZ deployment."
  type        = bool
  default     = false
}

variable "rds_publicly_accessible" {
  description = "Whether the database should have a public endpoint."
  type        = bool
  default     = false
}

variable "rds_backup_retention_period" {
  description = "Backup retention period in days."
  type        = number
  default     = 7
}

variable "rds_deletion_protection" {
  description = "Whether deletion protection is enabled for the DB instance."
  type        = bool
  default     = false
}

variable "rds_skip_final_snapshot" {
  description = "Whether to skip taking a final snapshot before DB deletion."
  type        = bool
  default     = true
}

variable "rds_final_snapshot_identifier" {
  description = "Final snapshot identifier used when rds_skip_final_snapshot is false."
  type        = string
  default     = "ai-powered-python-blog-final-snapshot"
}

variable "rds_manage_master_user_password" {
  description = "Whether AWS should manage the master password in Secrets Manager."
  type        = bool
  default     = true
}

variable "app_runner_service_name" {
  description = "Optional explicit App Runner service name. Leave empty to derive from project/environment."
  type        = string
  default     = ""
}

variable "app_runner_image_tag" {
  description = "Container image tag in ECR that App Runner should deploy."
  type        = string
  default     = "latest"
}

variable "app_runner_port" {
  description = "Container port exposed by the web app."
  type        = number
  default     = 8000
}

variable "app_runner_cpu" {
  description = "App Runner CPU setting."
  type        = string
  default     = "1024"
}

variable "app_runner_memory" {
  description = "App Runner memory setting."
  type        = string
  default     = "2048"
}

variable "app_runner_auto_deployments_enabled" {
  description = "Whether App Runner should automatically deploy when a new image is pushed to same-account ECR."
  type        = bool
  default     = true
}

variable "app_runner_is_publicly_accessible" {
  description = "Whether the App Runner service should be publicly accessible."
  type        = bool
  default     = true
}

variable "app_runner_health_check_path" {
  description = "Health check path for App Runner."
  type        = string
  default     = "/admin/login/"
}

variable "django_allowed_hosts" {
  description = "Comma-separated Django ALLOWED_HOSTS value for the deployed service."
  type        = string
  default     = ".awsapprunner.com,localhost,127.0.0.1"
}

variable "django_csrf_trusted_origins" {
  description = "Comma-separated Django CSRF trusted origins for the deployed service."
  type        = string
  default     = "https://*.awsapprunner.com"
}

variable "django_time_zone" {
  description = "Django time zone for the deployed environment."
  type        = string
  default     = "UTC"
}
