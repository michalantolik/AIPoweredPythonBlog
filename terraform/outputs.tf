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
