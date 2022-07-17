#!/bin/bash

# Exit in case of error
set -e

# Initialize enviornment-files
(python3.10 -m venv ./.devcontainer/.venv && \
./.devcontainer/.venv/bin/python3.10 -m pip --quiet install --upgrade pip && \
./.devcontainer/.venv/bin/python3.10 -m pip --quiet install tomli && \
./.devcontainer/.venv/bin/python3.10 ./.devcontainer/scripts/load_envs.py env.toml)
