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
