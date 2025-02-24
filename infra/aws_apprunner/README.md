<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.5.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |
| <a name="requirement_dotenv"></a> [dotenv](#requirement\_dotenv) | ~> 1.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_dotenv"></a> [dotenv](#provider\_dotenv) | 1.0.1 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_application"></a> [application](#module\_application) | ./modules/application | n/a |
| <a name="module_db"></a> [db](#module\_db) | ./modules/db | n/a |
| <a name="module_iam"></a> [iam](#module\_iam) | ./modules/iam | n/a |
| <a name="module_monitoring"></a> [monitoring](#module\_monitoring) | ./modules/monitoring | n/a |
| <a name="module_secret_manager"></a> [secret\_manager](#module\_secret\_manager) | ./modules/secret_manager | n/a |

## Resources

| Name | Type |
|------|------|
| [dotenv_dotenv.config](https://registry.terraform.io/providers/jrhouston/dotenv/latest/docs/data-sources/dotenv) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_AWS_ACCOUNT_ID"></a> [AWS\_ACCOUNT\_ID](#output\_AWS\_ACCOUNT\_ID) | n/a |
| <a name="output_AWS_DYNAMODB_TABLE_NAME_HISTORIES"></a> [AWS\_DYNAMODB\_TABLE\_NAME\_HISTORIES](#output\_AWS\_DYNAMODB\_TABLE\_NAME\_HISTORIES) | n/a |
| <a name="output_AWS_REGION"></a> [AWS\_REGION](#output\_AWS\_REGION) | n/a |
| <a name="output_AWS_SECRET_MANAGER_SECRET_NAME"></a> [AWS\_SECRET\_MANAGER\_SECRET\_NAME](#output\_AWS\_SECRET\_MANAGER\_SECRET\_NAME) | n/a |
| <a name="output_app_runner_service_url"></a> [app\_runner\_service\_url](#output\_app\_runner\_service\_url) | n/a |
<!-- END_TF_DOCS -->