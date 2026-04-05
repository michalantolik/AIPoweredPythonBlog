resource "random_password" "django_secret_key" {
  length  = 64
  special = true
}

resource "aws_secretsmanager_secret" "django_secret_key" {
  name                    = "${local.name_prefix}/django/secret-key"
  description             = "Django SECRET_KEY for ${local.name_prefix}"
  recovery_window_in_days = 0

  tags = {
    Name = "${local.name_prefix}-django-secret-key"
  }
}

resource "aws_secretsmanager_secret_version" "django_secret_key" {
  secret_id     = aws_secretsmanager_secret.django_secret_key.id
  secret_string = random_password.django_secret_key.result
}
