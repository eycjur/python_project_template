<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.5.0 |
| <a name="requirement_dotenv"></a> [dotenv](#requirement\_dotenv) | ~> 1.0 |
| <a name="requirement_google"></a> [google](#requirement\_google) | ~> 5.38.0 |
| <a name="requirement_random"></a> [random](#requirement\_random) | 3.6.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_dotenv"></a> [dotenv](#provider\_dotenv) | 1.0.1 |
| <a name="provider_google"></a> [google](#provider\_google) | 5.38.0 |

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
| [google_project_service.api_activation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_service) | resource |
| [dotenv_dotenv.config](https://registry.terraform.io/providers/jrhouston/dotenv/latest/docs/data-sources/dotenv) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_GCP_FIRESTORE_COLLECTION_NAME_HISTORIES"></a> [GCP\_FIRESTORE\_COLLECTION\_NAME\_HISTORIES](#output\_GCP\_FIRESTORE\_COLLECTION\_NAME\_HISTORIES) | n/a |
| <a name="output_GCP_FIRESTORE_DB_NAME"></a> [GCP\_FIRESTORE\_DB\_NAME](#output\_GCP\_FIRESTORE\_DB\_NAME) | n/a |
| <a name="output_GCP_PROJECT_ID"></a> [GCP\_PROJECT\_ID](#output\_GCP\_PROJECT\_ID) | n/a |
| <a name="output_GCP_REGION"></a> [GCP\_REGION](#output\_GCP\_REGION) | n/a |
| <a name="output_GCP_SERVICE_ACCOUNT"></a> [GCP\_SERVICE\_ACCOUNT](#output\_GCP\_SERVICE\_ACCOUNT) | n/a |
<!-- END_TF_DOCS -->