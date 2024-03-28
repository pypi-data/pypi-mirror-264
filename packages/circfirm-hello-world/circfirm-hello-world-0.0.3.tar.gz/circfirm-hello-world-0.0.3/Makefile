# SPDX-FileCopyrightText: 2024 Alec Delaney
#
# SPDX-License-Identifier: MIT
#
# From the circfirm repository

.PHONY: lint
lint:
	@pre-commit run ruff --all-files

.PHONY: format
format:
	@pre-commit run ruff-format --all-files

.PHONY: check
check:
	@pre-commit run --all-files

.PHONY: prepare
prepare: check test

.PHONY: test
test:
	@coverage run -m pytest
	@coverage report
	@coverage html
