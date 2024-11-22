# Lambdaで使用するIAMロールを作成する

resource "aws_iam_role" "role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "role-attach1" {
  role     = aws_iam_role.role.name
  for_each = toset(["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", "arn:aws:iam::aws:policy/PowerUserAccess"])

  policy_arn = each.value
}
