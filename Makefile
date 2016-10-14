ENV  ?= dev

export TF_LOG := debug
export TF_LOG_PATH := ../terraform.$(ENV).log
export GOPATH := $(HOME)/go

export apex=bin/apex

default: infra

infra: plan apply projectfile

plan:
	$(apex) infra get -update
	$(apex) infra plan -module-depth=-1 -state=../terraform.$(ENV).tfstate -var-file ../../terraform.tfvars -out ../terraform.$(ENV).tfplan
.PHONY: plan

apply:
	$(apex) infra apply -state=../terraform.$(ENV).tfstate -var-file ../../terraform.tfvars 
.PHONY: apply

tfvars:
	$(apex) list --tfvars > functions/functions.$(ENV).tfvars
.PHONY: appl

api-lab1: tfvars
	bin/env add permissions lab1
	vendor/scripts/env.py render api --tfstate=infrastructure/terraform.$(ENV).tfstate --tfvars=functions/functions.$(ENV).tfvars templates/lab1.yaml
	vendor/scripts/env.py import api --tfstate=infrastructure/terraform.$(ENV).tfstate --tfvars=functions/functions.$(ENV).tfvars templates/lab1.yaml
.PHONY: tfvars]

api-lab2: tfvars
	bin/env add permissions lab2
	vendor/scripts/env.py render api --tfstate=infrastructure/terraform.$(ENV).tfstate --tfvars=functions/functions.$(ENV).tfvars templates/lab2.yaml
	vendor/scripts/env.py import api --tfstate=infrastructure/terraform.$(ENV).tfstate --tfvars=functions/functions.$(ENV).tfvars templates/lab2.yaml
.PHONY: tfvars

import:
	aws dynamodb batch-write-item --request-items file://infrastructure/$(ENV)/data/data000.json
	aws dynamodb batch-write-item --request-items file://infrastructure/$(ENV)/data/data001.json
	aws dynamodb batch-write-item --request-items file://infrastructure/$(ENV)/data/data002.json
.PHONY: import

destroy:
	$(apex) infra plan -destroy -var-file ../../terraform.tfvars -state=../terraform.$(ENV).tfstate -out ../terraform.$(ENV).tfplan
	terraform apply -backup=- -state-out=infrastructure/terraform.$(ENV).tfstate infrastructure/terraform.$(ENV).tfplan
.PHONY: destroy

clean: destroy
	rm -f infrastructure/terraform.$(ENV).tfplan
	rm -f infrastructure/terraform.$(ENV).tfstate
	rm -f infrastructure/terraform.$(ENV).tfstate.backup
	rm -f infrastructure/terraform.$(ENV).log
	rm -fR infrastructure/$(ENV)/.terraform
.PHONY: clean

projectfile:
	bin/env write project $(ENV) --tfstate=infrastructure/terraform.$(ENV).tfstate
.PHONY: projectfile

init:
	bin/env init from dev $(ENV)
.PHONY: init

apex: 
	@go get github.com/mitchellh/gox
	cd $(GOPATH)/src/github.com/apex/apex; go get ./...
	gox -rebuild -osarch="darwin/amd64 linux/amd64" -output=bin/apex_{{.OS}} github.com/apex/apex/...
.PHONY: apex
