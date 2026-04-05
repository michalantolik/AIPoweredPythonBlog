# path: terraform/outputs.tf

output "vpc_id" {
  description = "VPC ID."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs."
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs."
  value       = aws_subnet.private[*].id
}

output "app_security_group_id" {
  description = "Application security group ID."
  value       = aws_security_group.app.id
}

output "db_security_group_id" {
  description = "Database security group ID."
  value       = aws_security_group.db.id
}

output "availability_zones" {
  description = "Availability zones used by this stack."
  value       = local.azs
}

output "ecr_repository_name" {
  description = "Amazon ECR repository name."
  value       = aws_ecr_repository.app.name
}

output "ecr_repository_url" {
  description = "Amazon ECR repository URL."
  value       = aws_ecr_repository.app.repository_url
}

output "ecr_registry_id" {
  description = "Amazon ECR registry ID."
  value       = aws_ecr_repository.app.registry_id
}

output "rds_instance_id" {
  description = "Amazon RDS instance identifier."
  value       = aws_db_instance.postgres.id
}

output "rds_instance_arn" {
  description = "Amazon RDS instance ARN."
  value       = aws_db_instance.postgres.arn
}

output "rds_endpoint" {
  description = "Amazon RDS endpoint address."
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "Amazon RDS port."
  value       = aws_db_instance.postgres.port
}

output "rds_db_name" {
  description = "Initial database name."
  value       = aws_db_instance.postgres.db_name
}

output "rds_master_username" {
  description = "Amazon RDS master username."
  value       = aws_db_instance.postgres.username
}

output "rds_db_subnet_group_name" {
  description = "Amazon RDS DB subnet group name."
  value       = aws_db_subnet_group.postgres.name
}

output "rds_master_user_secret_arn" {
  description = "Secrets Manager ARN for the RDS master user secret, when AWS manages the password."
  value       = try(aws_db_instance.postgres.master_user_secret[0].secret_arn, null)
  sensitive   = true
}

output "app_runner_service_arn" {
  description = "AWS App Runner service ARN."
  value       = aws_apprunner_service.app.arn
}

output "app_runner_service_id" {
  description = "AWS App Runner service ID."
  value       = aws_apprunner_service.app.service_id
}

output "app_runner_service_url" {
  description = "Public URL of the AWS App Runner service."
  value       = aws_apprunner_service.app.service_url
}

output "app_runner_vpc_connector_arn" {
  description = "AWS App Runner VPC connector ARN."
  value       = aws_apprunner_vpc_connector.app.arn
}

output "django_secret_key_secret_arn" {
  description = "Secrets Manager ARN for the Django SECRET_KEY."
  value       = aws_secretsmanager_secret.django_secret_key.arn
  sensitive   = true
}
