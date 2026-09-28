#!/usr/bin/env bash
#
# Crea el bucket S3 del estado remoto de Terraform para un ambiente.
# El pipeline NO crea el bucket: ejecutar una vez por cuenta AWS antes del
# primer `terraform init`. Ambos stacks (database, apps) comparten el bucket
# con keys distintas.
#
# Uso:
#   scripts/bootstrap-state.sh student1
#   ENV=student1 scripts/bootstrap-state.sh
#
# Requiere: awscli v2 con credenciales válidas de la cuenta destino (incluido
# el session token del Learner Lab).

set -euo pipefail

ENV_NAME="${1:-${ENV:-}}"
REGION="us-east-1"

if [[ -z "${ENV_NAME}" ]]; then
    echo "Falta el nombre del ambiente. Uso: scripts/bootstrap-state.sh <studentN>" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_FILE="${REPO_ROOT}/terraform/environments/${ENV_NAME}/apps/backend.tfvars"

if [[ ! -f "${BACKEND_FILE}" ]]; then
    echo "No existe ${BACKEND_FILE}. ¿'${ENV_NAME}' es un ambiente válido?" >&2
    exit 1
fi

BUCKET="$(grep '^bucket' "${BACKEND_FILE}" | cut -d'"' -f2)"

if [[ -z "${BUCKET}" ]]; then
    echo "No se pudo leer 'bucket' de ${BACKEND_FILE}" >&2
    exit 1
fi

echo "Ambiente     : ${ENV_NAME}"
echo "Region       : ${REGION}"
echo "Bucket estado: ${BUCKET}"

if aws s3api head-bucket --bucket "${BUCKET}" 2>/dev/null; then
    echo "El bucket ya existe."
else
    echo "Creando bucket..."
    # us-east-1 no admite LocationConstraint.
    aws s3api create-bucket --bucket "${BUCKET}" --region "${REGION}"
    aws s3api wait bucket-exists --bucket "${BUCKET}"
    echo "Bucket creado."
fi

echo "Habilitando versionado..."
aws s3api put-bucket-versioning \
    --bucket "${BUCKET}" \
    --versioning-configuration Status=Enabled

echo "Habilitando cifrado por defecto..."
aws s3api put-bucket-encryption \
    --bucket "${BUCKET}" \
    --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

echo "Bloqueando acceso público..."
aws s3api put-public-access-block \
    --bucket "${BUCKET}" \
    --public-access-block-configuration \
    'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true'

echo "Bucket '${BUCKET}' listo."
