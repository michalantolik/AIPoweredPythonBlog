resource "aws_apprunner_vpc_connector" "app" {
  vpc_connector_name = "${local.name_prefix}-vpc-connector"
  subnets            = aws_subnet.private[*].id
  security_groups    = [aws_security_group.app.id]

  tags = {
    Name = "${local.name_prefix}-vpc-connector"
  }
}

resource "aws_apprunner_service" "app" {
  service_name = length(trimspace(var.app_runner_service_name)) > 0 ? var.app_runner_service_name : "${local.name_prefix}-service"

  source_configuration {
    auto_deployments_enabled = var.app_runner_auto_deployments_enabled

    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.app.repository_url}:${var.app_runner_image_tag}"
      image_repository_type = "ECR"

      image_configuration {
        port = tostring(var.app_runner_port)

        runtime_environment_variables = {
          DJANGO_ENV                  = "prod"
          DJANGO_DEBUG                = "0"
          DJANGO_ALLOWED_HOSTS        = "*"
          DJANGO_CSRF_TRUSTED_ORIGINS = var.django_csrf_trusted_origins
          DJANGO_TIME_ZONE            = var.django_time_zone

          DJANGO_DB_ENGINE = "django.db.backends.postgresql"
          DJANGO_DB_NAME   = var.rds_db_name
          DJANGO_DB_HOST   = aws_db_instance.postgres.address
          DJANGO_DB_PORT   = tostring(aws_db_instance.postgres.port)

          DJANGO_SESSION_COOKIE_SECURE = "True"
          DJANGO_CSRF_COOKIE_SECURE    = "True"
          DJANGO_SECURE_SSL_REDIRECT   = "False"

          INTRO_OVERLAY_ENABLED        = "0"
          SHOW_SIDEBAR_ON_HOME_STARTUP = "0"
        }

        runtime_environment_secrets = {
          DJANGO_SECRET_KEY  = aws_secretsmanager_secret.django_secret_key.arn
          DJANGO_DB_USER     = "${aws_db_instance.postgres.master_user_secret[0].secret_arn}:username::"
          DJANGO_DB_PASSWORD = "${aws_db_instance.postgres.master_user_secret[0].secret_arn}:password::"
        }
      }
    }
  }

  instance_configuration {
    cpu               = var.app_runner_cpu
    memory            = var.app_runner_memory
    instance_role_arn = aws_iam_role.apprunner_instance.arn
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = var.app_runner_health_check_path
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  network_configuration {
    ingress_configuration {
      is_publicly_accessible = var.app_runner_is_publicly_accessible
    }

    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.app.arn
    }
  }

  tags = {
    Name = "${local.name_prefix}-apprunner-service"
  }

  depends_on = [
    aws_iam_role_policy_attachment.apprunner_ecr_access,
    aws_iam_role_policy.apprunner_instance_secrets,
    aws_secretsmanager_secret_version.django_secret_key,
    aws_db_instance.postgres
  ]
}
