data "aws_iam_policy_document" "apprunner_ecr_access_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "apprunner_ecr_access" {
  name               = "${local.name_prefix}-apprunner-ecr-access"
  assume_role_policy = data.aws_iam_policy_document.apprunner_ecr_access_assume_role.json

  tags = {
    Name = "${local.name_prefix}-apprunner-ecr-access"
  }
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

data "aws_iam_policy_document" "apprunner_instance_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["tasks.apprunner.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "apprunner_instance" {
  name               = "${local.name_prefix}-apprunner-instance"
  assume_role_policy = data.aws_iam_policy_document.apprunner_instance_assume_role.json

  tags = {
    Name = "${local.name_prefix}-apprunner-instance"
  }
}

data "aws_iam_policy_document" "apprunner_instance_secrets" {
  statement {
    sid    = "ReadAppSecrets"
    effect = "Allow"

    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]

    resources = compact([
      aws_secretsmanager_secret.django_secret_key.arn,
      try(aws_db_instance.postgres.master_user_secret[0].secret_arn, null)
    ])
  }
}

resource "aws_iam_role_policy" "apprunner_instance_secrets" {
  name   = "${local.name_prefix}-apprunner-instance-secrets"
  role   = aws_iam_role.apprunner_instance.id
  policy = data.aws_iam_policy_document.apprunner_instance_secrets.json
}
