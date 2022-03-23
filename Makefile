# Makefile

## Configuration

BUILD_TIME := $(shell date +%FT%T%z)
PROJECT    := $(shell basename $(PWD))


## Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt

## Setup developement environment
.PHONY: dev
dev:
	cd app && ln -sf config_dev.py config.py

## Setup production environment
.PHONY: prod
prod:
	cd app && ln -sf config_prod.py config.py
