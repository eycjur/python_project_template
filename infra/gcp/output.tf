output "GCP_PROJECT_ID" {
  value = local.common.project_id
}

output "GCP_REGION" {
  value = local.common.region
}

output "GCP_SERVICE_ACCOUNT" {
  value = module.iam.service_account
}

output "GCP_FIRESTORE_DB_NAME" {
  value = local.db.name
}

output "GCP_FIRESTORE_COLLECTION_NAME_HISTORIES" {
  # terraformで作成しないので、任意
  value = "firestore-collection-histories"
}
