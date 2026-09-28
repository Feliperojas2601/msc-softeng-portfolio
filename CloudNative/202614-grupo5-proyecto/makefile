# Los pasos en este archivo pueden ser usados para su pipeline de Unit testing
# en el caso que usted decida usar Python.

.PHONY: lintfix lintcheck unittest bootstrap-state tf-init tf-plan tf-apply tf-destroy tf-fmt deploy

lintfix:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run black .
	poetry --directory=${DIR} run isort . --profile black
	poetry --directory=${DIR} run bandit -c pyproject.toml -r .
	poetry --directory=${DIR} run ruff check --fix

lintcheck:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run black --check .
	poetry --directory=${DIR} run isort --check . --profile black
	poetry --directory=${DIR} run bandit -c pyproject.toml -r .
	poetry --directory=${DIR} run ruff check

unittest:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing

# Agregue nuevas a partir de esta línea

# --- Terraform -------------------------------------------

ENV ?= student1
STACK ?= database
TF_STACK_DIR := terraform/stacks/$(STACK)
TF_ENV_REL := ../../environments/$(ENV)/$(STACK)
TF := terraform -chdir=$(TF_STACK_DIR)

bootstrap-state:
	scripts/bootstrap-state.sh $(ENV)

tf-fmt:
	terraform fmt -recursive terraform/

tf-init:
	$(TF) init -reconfigure -backend-config=$(TF_ENV_REL)/backend.tfvars

tf-plan:
	$(TF) plan -var-file=$(TF_ENV_REL)/terraform.tfvars -out=.tfplan

tf-apply:
	$(TF) apply .tfplan

tf-destroy:
	$(TF) destroy -var-file=$(TF_ENV_REL)/terraform.tfvars

# Aplica ambos stacks en orden (database, luego apps).
deploy:
	$(MAKE) tf-init tf-plan tf-apply ENV=$(ENV) STACK=database
	$(MAKE) tf-init tf-plan tf-apply ENV=$(ENV) STACK=apps