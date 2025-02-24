rule  "terraform_typed_variables" {
  enabled = false
}

rule  "terraform_required_version" {
  enabled = false
}

rule  "terraform_required_providers" {
  enabled = false
}

# 本番環境ではignoreしなくてもよい
rule  "terraform_unused_declarations" {
  enabled = false
}

plugin "google" {
  enabled = true
  version = "0.31.0"
  source  = "github.com/terraform-linters/tflint-ruleset-google"
}

plugin "aws" {
    enabled = true
    version = "0.37.0"
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

plugin "azurerm" {
    enabled = true
    version = "0.27.0"
    source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}
