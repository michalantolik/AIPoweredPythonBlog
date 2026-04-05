# path: terraform/rds.tf

resource "aws_db_subnet_group" "postgres" {
  name        = "${local.name_prefix}-db-subnet-group"
  description = "DB subnet group for ${local.name_prefix} PostgreSQL."
  subnet_ids  = aws_subnet.private[*].id

  tags = {
    Name = "${local.name_prefix}-db-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "${local.name_prefix}-postgres"

  engine         = "postgres"
  instance_class = var.rds_instance_class

  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage
  storage_type          = var.rds_storage_type
  storage_encrypted     = true

  db_name  = var.rds_db_name
  username = var.rds_db_username

  manage_master_user_password = var.rds_manage_master_user_password

  port = var.db_port

  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.db.id]

  publicly_accessible = var.rds_publicly_accessible
  multi_az            = var.rds_multi_az

  backup_retention_period = var.rds_backup_retention_period
  deletion_protection     = var.rds_deletion_protection

  skip_final_snapshot       = var.rds_skip_final_snapshot
  final_snapshot_identifier = var.rds_skip_final_snapshot ? null : var.rds_final_snapshot_identifier

  auto_minor_version_upgrade = true
  apply_immediately          = true
  copy_tags_to_snapshot      = true

  depends_on = [
    aws_db_subnet_group.postgres
  ]

  tags = {
    Name = "${local.name_prefix}-postgres"
  }
}