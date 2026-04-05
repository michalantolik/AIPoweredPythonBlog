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
  description = "PostgreSQL port for future database access."
  type        = number
  default     = 5432
}

variable "ecr_repository_name" {
  description = "Amazon ECR repository name used for Docker image pushes."
  type        = string
  default     = "ai-powered-python-blog"
}
