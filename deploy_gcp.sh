#!/bin/bash
set -Ceuo pipefail

source .env

gcloud builds submit --tag "gcr.io/${PROJECT_ID}/${CONTAINER_NAME}" --project "${PROJECT_ID}"
gcloud run deploy "${CONTAINER_NAME}" \
    --image "gcr.io/${PROJECT_ID}/${CONTAINER_NAME}" \
    --platform managed \
    --region "${REGION}" \
    --port "${PORT}"
